# Retarget CMU (cgspeed MotionBuilder-friendly) BVH clips onto an MPFB cmu_mb rig.
# The mocap's zero pose is a T-pose and the MakeHuman rest pose is not, so every target bone is first
# swung onto its source bone's rest direction; world rotations are then transferred frame by frame.
import bpy, math
from mathutils import Matrix, Quaternion, Vector

_c = lambda deg, ax='X': Matrix.Rotation(math.radians(deg), 3, ax)
HAND_CURL = {'LeftHand': _c(0), 'RightHand': _c(0), 'LeftFingerBase': _c(18), 'RightFingerBase': _c(18),
             'LeftHandFinger1': _c(28), 'RightHandFinger1': _c(28), 'LThumb': _c(10, 'Z'), 'RThumb': _c(-10, 'Z')}
NAME_MAP = {'LeftHandFinger1': 'LeftHandIndex1', 'RightHandFinger1': 'RightHandIndex1'}


def _world_rest(arm):
    out = {}
    for b in arm.data.bones:
        m = arm.matrix_world @ b.matrix_local
        out[b.name] = (m.to_3x3().normalized(), m.to_translation(), (arm.matrix_world @ b.tail_local) - (arm.matrix_world @ b.head_local))
    return out


def import_bvh(path):
    before = set(bpy.data.objects)
    bpy.ops.import_anim.bvh(filepath=path, rotate_mode='NATIVE', update_scene_fps=False, update_scene_duration=False)
    src = [o for o in bpy.data.objects if o not in before][0]
    return src


def pose_diff(a, b):
    return sum(1.0 - abs(a[k].dot(b[k])) for k in a)


def find_loop(frames, min_len, max_len):
    """frames: list of {bone: quat}. Pick the pair (i, j) whose poses match best, j - i within [min_len, max_len]."""
    best = (1e9, 0, min_len)
    n = len(frames)
    for i in range(0, max(1, n - max_len - 1), 2):
        for j in range(i + min_len, min(n, i + max_len)):
            d = pose_diff(frames[i], frames[j])
            if d < best[0]:
                best = (d, i, j)
    return best


def retarget(tgt, bvh_path, name, start=0, end=None, step=4, loop=None, in_place=False, face=True):
    """loop: (min_seconds, max_seconds) to search for a seamless cycle inside [start, end)."""
    src = import_bvh(bvh_path)
    scn = bpy.context.scene
    act = src.animation_data.action
    f0, f1 = int(act.frame_range[0]), int(act.frame_range[1])
    end = min(end or f1, f1)
    start = max(start + f0, f0)
    srest, trest = _world_rest(src), _world_rest(tgt)
    tbones = [b for b in tgt.data.bones]
    sname = {b.name: NAME_MAP.get(b.name, b.name) for b in tbones}
    # target reference (T-pose) orientation per bone: swing each target bone so the line to its child joint
    # matches the source's. Zero-length source bones (hips, hand roots) carry no direction and are left as they are.
    sb = {b.name: b for b in src.data.bones}
    def child_dir(bone, rest, bones_by_name, names):
        acc = Vector((0, 0, 0))
        for c in bone.children:
            if c.name not in names:
                continue
            d = rest[c.name][1] - rest[bone.name][1]
            if d.length > 1e-4:
                acc += d.normalized()
        return acc.normalized() if acc.length > 1e-4 else None
    src_names = set(sb)
    inv_map = {v: k for k, v in sname.items()}
    ref = {}
    for b in tbones:
        s = sname[b.name]
        ref[b.name] = trest[b.name][0]
        if s not in sb:
            continue
        common_t = set(c.name for c in b.children if sname.get(c.name) in src_names)
        common_s = set(sname[c] for c in common_t)
        dt = child_dir(b, trest, None, common_t)
        ds = child_dir(sb[s], srest, None, common_s)
        if dt is None or ds is None:
            continue
        ref[b.name] = dt.rotation_difference(ds).to_matrix() @ trest[b.name][0]
    legs = lambda R: sum(R[k][2].length for k in ('LeftUpLeg', 'LeftLeg'))
    scale = legs(trest) / max(1e-6, legs(srest))
    # sample the source
    samples = []
    for f in range(start, end, step):
        scn.frame_set(f)
        rot, hip, pos = {}, None, {}
        for pb in src.pose.bones:
            m = src.matrix_world @ pb.matrix
            rot[pb.name] = m.to_3x3().normalized()
            pos[pb.name] = m.to_translation()
        hip = pos['Hips']
        side = pos['RightUpLeg'] - pos['LeftUpLeg']
        samples.append((rot, hip, side))
    if loop:
        fps = 120.0 / step
        qs = [{k: v.to_quaternion() for k, v in r.items()} for r, _, _ in samples]
        d, i, j = find_loop(qs, int(loop[0] * fps), int(loop[1] * fps))
        samples = samples[i:j + 1]
        print(f'  {name}: loop frames {i}..{j} ({(j - i) / fps:.2f}s) match {d:.3f}')
    # heading: turn the clip so the body faces -Y (MakeHuman's front); walks face along their travel
    rz = Matrix.Identity(3)
    if face:
        if in_place:
            f = samples[-1][1] - samples[0][1]
        else:
            f = Vector((0, 0, 0))
            for _, _, side in samples:
                f += Vector((0, 0, 1)).cross(side).normalized()
        phi = math.atan2(f.x, -f.y)
        rz = Matrix.Rotation(-phi, 3, 'Z')
    h0 = samples[0][1]
    n = len(samples)
    drift = (samples[-1][1] - samples[0][1]) if in_place else Vector((0, 0, 0))
    new_stride = (Vector((drift.x, drift.y, 0)).length * scale) if in_place else 0.0
    new = bpy.data.actions.new(name)
    new.use_fake_user = True
    tgt.animation_data_create()
    tgt.animation_data.action = new
    for pb in tgt.pose.bones:
        pb.rotation_mode = 'QUATERNION'
    prevq = {}
    order = [b for b in tbones]  # data.bones is parent-before-child
    for k, (rot, hip, _side) in enumerate(samples):
        R = {}
        for b in order:
            s = sname[b.name]
            if b.name in HAND_CURL and b.parent:
                # CMU's hand channels are sparse and noisy: hands follow the forearm, fingers rest gently curled
                R[b.name] = R[b.parent.name] @ trest[b.parent.name][0].inverted() @ trest[b.name][0] @ HAND_CURL[b.name]
            elif s in rot:
                R[b.name] = rz @ rot[s] @ srest[s][0].inverted() @ ref[b.name]
            else:
                R[b.name] = (R[b.parent.name] @ trest[b.parent.name][0].inverted() @ trest[b.name][0]) if b.parent else trest[b.name][0]
        for b in order:
            pb = tgt.pose.bones[b.name]
            Rr = trest[b.name][0]
            if b.parent:
                basis = Rr.inverted() @ trest[b.parent.name][0] @ R[b.parent.name].inverted() @ R[b.name]
            else:
                basis = Rr.inverted() @ R[b.name]
                off = rz @ (hip - h0 - drift * (k / max(1, n - 1))) * scale
                th = trest['Hips'][1]
                head = Vector((off.x, off.y, hip.z * scale - th.z))
                pb.location = Rr.inverted() @ head
                pb.keyframe_insert('location', frame=k + 1)
            q = basis.to_quaternion()
            if b.name in prevq and prevq[b.name].dot(q) < 0:
                q.negate()
            prevq[b.name] = q
            pb.rotation_quaternion = q
            pb.keyframe_insert('rotation_quaternion', frame=k + 1)
    bpy.data.objects.remove(src)
    for a in list(bpy.data.actions):
        if a.users == 0 and not a.use_fake_user:
            bpy.data.actions.remove(a)
    track = tgt.animation_data.nla_tracks.new()
    track.name = name
    track.strips.new(name, 1, new)
    tgt.animation_data.action = None
    new['stride'] = new_stride
    new['dur'] = (len(samples) - 1) / (120.0 / step)
    print(f'  {name}: {len(samples)} frames, {new["dur"]:.2f}s, travels {new_stride:.2f} m per loop')
    return new
