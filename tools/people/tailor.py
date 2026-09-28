# Tailoring medieval clothes onto a rigged MakeHuman body, in Blender.
# Fitted parts (bodice, sleeves, hose, boots) are cut from the body's own surface so they carry its skin weights;
# skirts and tunic hems are lofted rings hung from the waist or hips, weighted between the hips and thighs.
# Everything is placed from the body's own skeleton, so one pattern fits any build, sex or age.
import bpy, bmesh, math
from mathutils import Vector, kdtree

ARM_BONES = ['LeftShoulder', 'LeftArm', 'LeftForeArm', 'RightShoulder', 'RightArm', 'RightForeArm']
HAND_BONES = ['LeftHand', 'RightHand', 'LThumb', 'RThumb', 'LeftFingerBase', 'RightFingerBase', 'LeftHandFinger1', 'RightHandFinger1']
LEG_BONES = ['LeftUpLeg', 'RightUpLeg', 'LeftLeg', 'RightLeg']
FOOT_BONES = ['LeftFoot', 'RightFoot', 'LeftToeBase', 'RightToeBase']


def landmarks(rig):
    B = rig.data.bones
    h = lambda n: B[n].head_local.copy()
    L = {
        'hips': h('Hips'), 'knee': (h('LeftLeg') + h('RightLeg')) / 2, 'ankle': (h('LeftFoot') + h('RightFoot')) / 2,
        'neck': h('Neck'), 'head': h('Head'), 'chest': h('Spine1'), 'waist': h('Spine'), 'belly': h('LowerBack'),
        'lwrist': h('LeftHand'), 'rwrist': h('RightHand'), 'lelbow': h('LeftForeArm'), 'relbow': h('RightForeArm'),
        'lsh': h('LeftArm'), 'rsh': h('RightArm'),
    }
    L['crotch'] = L['hips'].z - (L['hips'].z - L['knee'].z) * 0.2
    return L


def weights(obj):
    names = {g.index: g.name for g in obj.vertex_groups}
    out = []
    for v in obj.data.vertices:
        out.append({names[g.group]: g.weight for g in v.groups if g.weight > 0.001})
    return out


def wsum(w, bones):
    return sum(w.get(b, 0.0) for b in bones)


def arm_t(co, L, side):
    """How far along the arm a point lies: 0 at the shoulder joint, 1 at the elbow, 2 at the wrist."""
    s, e, w = (L['lsh'], L['lelbow'], L['lwrist']) if side > 0 else (L['rsh'], L['relbow'], L['rwrist'])
    def proj(a, b, p):
        ab = b - a
        return max(0.0, min(1.0, (p - a).dot(ab) / ab.length_squared)), (a + ab * max(0.0, min(1.0, (p - a).dot(ab) / ab.length_squared)) - p).length
    t1, d1 = proj(s, e, co)
    t2, d2 = proj(e, w, co)
    return t1 if d1 < d2 else 1.0 + t2


def cut(body, name, keep, thickness, smooth=0):
    """Copy the body faces whose every vertex passes keep(i), push them out along the normals by thickness."""
    me = body.data
    bm = bmesh.new(); bm.from_mesh(me)
    bm.verts.ensure_lookup_table()
    ok = [keep(v.index) for v in bm.verts]
    dead = [f for f in bm.faces if not all(ok[v.index] for v in f.verts)]
    bmesh.ops.delete(bm, geom=dead, context='FACES')
    loose = [v for v in bm.verts if not v.link_faces]
    bmesh.ops.delete(bm, geom=loose, context='VERTS')
    bm.normal_update()
    for v in bm.verts:
        v.co += v.normal * thickness
    for _ in range(smooth):
        bmesh.ops.smooth_vert(bm, verts=bm.verts, factor=0.5, use_axis_x=True, use_axis_y=True, use_axis_z=True)
    nm = bpy.data.meshes.new(name); bm.to_mesh(nm); bm.free()
    ob = bpy.data.objects.new(name, nm)
    bpy.context.collection.objects.link(ob)
    for g in body.vertex_groups:
        ob.vertex_groups.new(name=g.name)
    # the cut keeps the deform layer, so weights come along with the vertices
    ob.parent = body.parent
    mod = ob.modifiers.new('Armature', 'ARMATURE'); mod.object = body.parent
    for p in nm.polygons: p.use_smooth = True
    return ob


def loft_skirt(name, rig, L, top_z, hem_z, top_r, hem_flare, rings=10, segs=64, folds=16, fold_amp=0.012, full_r=None, full_z=None):
    """A skirt hung from a ring at top_z: rings of vertices lofted down to hem_z, flaring out, with hanging folds.
    top_r: callable(theta) -> radius of the body at the waistband. Weighted to the hips and blended onto the thighs."""
    bm = bmesh.new()
    cx, cy = L['hips'].x, L['hips'].y
    rows = []
    for r in range(rings + 1):
        h = r / rings
        z = top_z + (hem_z - top_z) * h
        row = []
        for s in range(segs):
            th = s / segs * math.tau
            base = top_r(th)
            if full_r is not None:
                k = min(1.0, max(0.0, (top_z - z) / max(1e-3, top_z - full_z)))
                k = k * k * (3 - 2 * k)
                base = base + (max(base, full_r(th)) - base) * k
            below = max(0.0, (min(top_z, full_z if full_z is not None else top_z) - z) / max(1e-3, top_z - hem_z))
            rad = base * (1.0 + hem_flare * (below ** 1.3))
            # hanging folds: deeper toward the hem, a little irregular
            rad += fold_amp * (h ** 0.8) * (math.sin(th * folds + math.sin(th * 3.0) * 1.3) * 0.75 + math.sin(th * folds * 1.9 + 1.7) * 0.25)
            x, y = cx + math.sin(th) * rad, cy - math.cos(th) * rad
            row.append(bm.verts.new((x, y, z)))
        rows.append(row)
    for r in range(rings):
        for s in range(segs):
            a, b = rows[r][s], rows[r][(s + 1) % segs]
            c, d = rows[r + 1][(s + 1) % segs], rows[r + 1][s]
            bm.faces.new((a, d, c, b))
    bm.normal_update()
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    for p in me.polygons: p.use_smooth = True
    gH = ob.vertex_groups.new(name='Hips')
    gL = ob.vertex_groups.new(name='LeftUpLeg'); gR = ob.vertex_groups.new(name='RightUpLeg')
    gLL = ob.vertex_groups.new(name='LeftLeg'); gRL = ob.vertex_groups.new(name='RightLeg')
    thigh = L['hips'].z - L['knee'].z
    for v in me.vertices:
        # how far below the hips this vertex hangs, in thigh lengths: the legs take over as it goes down
        d = max(0.0, (L['hips'].z - v.co.z) / thigh)
        legk = min(0.85, d * 0.75) if d > 0 else 0.0
        side = max(-1.0, min(1.0, (v.co.x - cx) / 0.09))
        wl, wr = (1 + side) / 2, (1 - side) / 2
        below_knee = max(0.0, min(0.5, (d - 1.0) * 0.6))
        gH.add([v.index], 1.0 - legk, 'REPLACE')
        if legk > 0:
            gL.add([v.index], legk * wl * (1 - below_knee), 'REPLACE'); gR.add([v.index], legk * wr * (1 - below_knee), 'REPLACE')
            if below_knee > 0:
                gLL.add([v.index], legk * wl * below_knee, 'REPLACE'); gRL.add([v.index], legk * wr * below_knee, 'REPLACE')
    ob.parent = rig
    mod = ob.modifiers.new('Armature', 'ARMATURE'); mod.object = rig
    return ob


def _armish(ob):
    names = {g.index: g.name for g in ob.vertex_groups}
    arm = set(ARM_BONES + HAND_BONES) - {'LeftShoulder', 'RightShoulder'}
    return [sum(g.weight for g in v.groups if names.get(g.group) in arm) > 0.2 for v in ob.data.vertices]


def radius_profile(body, z, L, pad):
    """Distance from the body axis to the skin at height z, by angle, plus padding: the waistband's shape."""
    cx, cy = L['hips'].x, L['hips'].y
    bins = [0.0] * 72
    arm = _armish(body)
    for v in body.data.vertices:
        if abs(v.co.z - z) < 0.025 and not arm[v.index]:
            dx, dy = v.co.x - cx, v.co.y - cy
            th = math.atan2(dx, -dy) % math.tau
            k = int(th / math.tau * 72) % 72
            bins[k] = max(bins[k], math.hypot(dx, dy))
    # fill gaps and smooth
    for _ in range(3):
        bins = [max(bins[i], (bins[i - 1] + bins[(i + 1) % 72]) / 2) for i in range(72)]
    bins = [(bins[i - 2] + bins[i - 1] * 2 + bins[i] * 3 + bins[(i + 1) % 72] * 2 + bins[(i + 2) % 72]) / 9 for i in range(72)]
    return lambda th: bins[int((th % math.tau) / math.tau * 72) % 72] + pad


def hip_ring_radius(body, L, pad, z0, z1):
    """Widest the body gets between z0 and z1, by angle, so a skirt hung over it clears the thighs and seat."""
    cx, cy = L['hips'].x, L['hips'].y
    bins = [0.0] * 72
    arm = _armish(body)
    for v in body.data.vertices:
        if z1 <= v.co.z <= z0 and not arm[v.index]:
            dx, dy = v.co.x - cx, v.co.y - cy
            th = math.atan2(dx, -dy) % math.tau
            k = int(th / math.tau * 72) % 72
            bins[k] = max(bins[k], math.hypot(dx, dy))
    for _ in range(4):
        bins = [max(bins[i], (bins[i - 1] + bins[(i + 1) % 72]) / 2) for i in range(72)]
    bins = [(bins[i - 2] + bins[i - 1] * 2 + bins[i] * 3 + bins[(i + 1) % 72] * 2 + bins[(i + 2) % 72]) / 9 for i in range(72)]
    return lambda th: bins[int((th % math.tau) / math.tau * 72) % 72] + pad


def drape(ob, L, W_of, chest_z, cinch_z=None, cinch_pad=0.012, loose=0.0):
    floor_z = (cinch_z - 0.03) if cinch_z is not None else -1e9
    """Let fabric fall from the widest point above it (the chest, the shoulder blades) instead of wrapping the belly,
    and gather it back in where a belt cinches. Sleeves are left alone."""
    me = ob.data
    cx, cy = L['hips'].x, (L['hips'].y + L['neck'].y) / 2
    NB = 48
    rows = {}
    verts = [v for v in me.vertices if W_of(v) < 0.3]
    for v in verts:
        th = math.atan2(v.co.x - cx, -(v.co.y - cy)) % math.tau
        k = int(th / math.tau * NB) % NB
        zb = int(v.co.z * 100)
        r = math.hypot(v.co.x - cx, v.co.y - cy)
        rows.setdefault(zb, [0.0] * NB)
        rows[zb][k] = max(rows[zb][k], r)
    zs = sorted(rows)
    top = int(chest_z * 100)
    run = [0.0] * NB
    maxabove = {}
    for zb in reversed(zs):
        for k in range(NB):
            if zb <= top:
                run[k] = max(run[k], rows[zb][k])
        maxabove[zb] = run[:] if zb <= top else rows[zb][:]
    for v in verts:
        if v.co.z > chest_z or v.co.z < floor_z:
            continue
        th = math.atan2(v.co.x - cx, -(v.co.y - cy)) % math.tau
        k = int(th / math.tau * NB) % NB
        ma = maxabove[int(v.co.z * 100)]
        want = max(ma[k], ma[k - 1] * 0.97, ma[(k + 1) % NB] * 0.97) + loose
        if cinch_z is not None:
            d = abs(v.co.z - cinch_z)
            ck = max(0.0, 1.0 - d / 0.07)
            ck = ck * ck * (3 - 2 * ck)
            own = rows[int(v.co.z * 100)][k] if v.co.z > cinch_z - 0.2 else want
            want = want + (own + cinch_pad * 0.3 - want) * ck
        dx, dy = v.co.x - cx, v.co.y - cy
        r = math.hypot(dx, dy)
        if r > 1e-4 and want > r:
            v.co.x = cx + dx / r * want
            v.co.y = cy + dy / r * want


def relax(ob, iters=4, factor=0.5, keep=None, boundary_only=False):
    """Laplacian smoothing: irons out the anatomy under the cloth and straightens ragged cut edges."""
    bm = bmesh.new(); bm.from_mesh(ob.data)
    bm.verts.ensure_lookup_table()
    for _ in range(iters):
        new = {}
        for v in bm.verts:
            if keep and keep(v):
                continue
            if boundary_only and not v.is_boundary:
                continue
            nb = [e.other_vert(v) for e in v.link_edges if (not boundary_only) or e.is_boundary]
            if not nb:
                continue
            avg = sum((n.co for n in nb), Vector()) / len(nb)
            new[v] = v.co.lerp(avg, factor)
        for v, c in new.items():
            v.co = c
    bm.to_mesh(ob.data); bm.free()


def taubin(ob, iters=20, lam=0.5, mu=-0.53, keep=None):
    """Volume-preserving smoothing (alternate shrink and inflate): irons out nipples and ribs without deflating the chest."""
    bm = bmesh.new(); bm.from_mesh(ob.data)
    for it in range(iters * 2):
        f = lam if it % 2 == 0 else mu
        new = {}
        for v in bm.verts:
            if v.is_boundary or (keep and keep(v)):
                continue
            nb = [e.other_vert(v) for e in v.link_edges]
            avg = sum((n.co for n in nb), Vector()) / len(nb)
            new[v] = v.co + (avg - v.co) * f
        for v, c in new.items():
            v.co = c
    bm.to_mesh(ob.data); bm.free()


def smooth_neckline(ob, lim_fn, above_z):
    """Snap the cut edge round the neck onto the neckline curve, so it reads as a sewn edge, not a staircase."""
    bm = bmesh.new(); bm.from_mesh(ob.data)
    for v in bm.verts:
        if v.is_boundary and v.co.z > above_z:
            v.co.z = min(v.co.z, lim_fn(v.co))
    bm.to_mesh(ob.data); bm.free()


def crease_shading(ob):
    """Bake cavity darkening into a colour attribute: seams, folds and the insides of creases."""
    bpy.context.view_layer.objects.active = ob
    for o in bpy.context.selected_objects: o.select_set(False)
    ob.select_set(True)
    if not ob.data.color_attributes:
        ob.data.color_attributes.new('Col', 'BYTE_COLOR', 'POINT')
    ob.data.color_attributes.active_color = ob.data.color_attributes[0]
    bpy.ops.object.mode_set(mode='VERTEX_PAINT')
    try:
        bpy.ops.paint.vertex_color_dirt(blur_strength=1.0, blur_iterations=2, clean_angle=3.0, dirt_angle=0.0, dirt_only=True)
    except Exception as e:
        print('dirt failed', e)
    bpy.ops.object.mode_set(mode='OBJECT')


def hide_under(body, covered):
    """Delete the body faces hidden under clothes (every vertex covered), so skin can never poke through."""
    bm = bmesh.new(); bm.from_mesh(body.data)
    bm.verts.ensure_lookup_table()
    dead = [f for f in bm.faces if all(covered[v.index] for v in f.verts)]
    bmesh.ops.delete(bm, geom=dead, context='FACES')
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if not v.link_faces], context='VERTS')
    bm.to_mesh(body.data); bm.free()


def dress(body, rig, outfit):
    """outfit: 'peasant_m' (tunic, belt, hose, boots) or 'peasant_f' (kirtle, apron, shoes)."""
    L = landmarks(rig)
    W = weights(body)
    co = [v.co.copy() for v in body.data.vertices]
    n = len(co)
    ankle_z = L['ankle'].z + 0.03
    boot_top = L['ankle'].z + (L['knee'].z - L['ankle'].z) * 0.45
    neck_z = L['neck'].z - 0.035
    made = []

    def sleeve_ok(i, end):
        w = W[i]
        if wsum(w, HAND_BONES) > 0.25:
            return False
        a = wsum(w, ARM_BONES)
        if a < 0.2:
            return True
        side = 1 if co[i].x > 0 else -1
        return arm_t(co[i], L, side) < end

    def neck_lim(c, depth):
        front = max(0.0, min(1.0, (L['neck'].y - c.y) / 0.06 + 0.5))
        dx = max(0.0, 1.0 - abs(c.x - L['neck'].x) / 0.13)
        return neck_z - depth * (0.25 + 0.75 * front) * (dx * dx * (3 - 2 * dx))

    def neckline(i, depth):
        return co[i].z < neck_lim(co[i], depth)

    if outfit == 'peasant_m':
        waist_z = L['hips'].z + 0.07
        chest_z = L['chest'].z + 0.02
        top = [(i < n) and neckline(i, 0.05) and sleeve_ok(i, 1.93) and co[i].z > L['hips'].z - 0.06 for i in range(n)]
        tunic = cut(body, 'cloth_tunic', lambda i: top[i], 0.012)
        armw = lambda v: sum(g.weight for g in v.groups if tunic.vertex_groups[g.group].name in ARM_BONES + HAND_BONES)
        smooth_neckline(tunic, lambda c: neck_lim(c, 0.05) + 0.004, L['chest'].z)
        taubin(tunic, iters=25, keep=lambda v: False)
        drape(tunic, L, armw, chest_z, cinch_z=waist_z, loose=0.012)
        relax(tunic, iters=3, factor=0.45)
        relax(tunic, iters=25, factor=0.6, boundary_only=True)
        wprof = radius_profile(tunic, waist_z, L, 0.008)
        pb = hip_ring_radius(body, L, 0.03, L['hips'].z + 0.02, L['hips'].z - (L['hips'].z - L['knee'].z) * 0.55)
        pt = hip_ring_radius(tunic, L, 0.012, waist_z - 0.02, L['hips'].z - 0.07)
        prof = lambda th: max(pb(th), pt(th))
        skirt = loft_skirt('cloth_tunicskirt', rig, L, waist_z + 0.015, L['knee'].z + (L['hips'].z - L['knee'].z) * 0.28, wprof, 0.2,
                           rings=10, folds=13, fold_amp=0.011, full_r=prof, full_z=L['hips'].z - 0.05)
        belt = cut(body, 'cloth_belt', lambda i: abs(co[i].z - waist_z) < 0.02 and wsum(W[i], ARM_BONES + HAND_BONES) < 0.1, 0.0)
        bwp = radius_profile(tunic, waist_z, L, 0.0)
        cx, cy = L['hips'].x, (L['hips'].y + L['neck'].y) / 2
        for v in belt.data.vertices:
            dx, dy = v.co.x - cx, v.co.y - cy; r = math.hypot(dx, dy); th = math.atan2(dx, -dy)
            want = bwp(th) + 0.006
            v.co.x, v.co.y = cx + dx / r * want, cy + dy / r * want
        relax(belt, iters=4, factor=0.5, boundary_only=True)
        hose = cut(body, 'cloth_hose', lambda i: co[i].z < waist_z and co[i].z > boot_top - 0.1 and wsum(W[i], HAND_BONES + ARM_BONES) < 0.1, 0.005)
        relax(hose, iters=2, factor=0.4)
        boots = cut(body, 'cloth_boots', lambda i: co[i].z < boot_top + 0.03 and wsum(W[i], HAND_BONES + ARM_BONES) < 0.1, 0.01)
        relax(boots, iters=10, factor=0.5, keep=lambda v: v.co.z < 0.004)
        relax(boots, iters=6, factor=0.6, boundary_only=True)
        made = [tunic, skirt, belt, hose, boots]
        covered = [(top[i] and co[i].z < neck_lim(co[i], 0.05) - 0.05 and sleeve_ok(i, 1.86)) or (co[i].z < waist_z and wsum(W[i], HAND_BONES + ARM_BONES) < 0.05) for i in range(n)]
    elif outfit == 'peasant_f':
        waist_z = L['waist'].z - 0.02
        top = [neckline(i, 0.09) and sleeve_ok(i, 1.9) and co[i].z > L['hips'].z - 0.06 for i in range(n)]
        bodice = cut(body, 'cloth_kirtle', lambda i: top[i], 0.009)
        smooth_neckline(bodice, lambda c: neck_lim(c, 0.09) + 0.004, L['chest'].z - 0.05)
        taubin(bodice, iters=25)
        armw = lambda v: sum(g.weight for g in v.groups if bodice.vertex_groups[g.group].name in ARM_BONES + HAND_BONES)
        drape(bodice, L, armw, L['chest'].z - 0.02, cinch_z=waist_z + 0.02, loose=0.004)
        relax(bodice, iters=2, factor=0.4)
        relax(bodice, iters=25, factor=0.6, boundary_only=True)
        wprof = radius_profile(bodice, waist_z, L, 0.008)
        pb = hip_ring_radius(body, L, 0.03, L['hips'].z + 0.03, L['hips'].z - (L['hips'].z - L['knee'].z) * 0.5)
        pt = hip_ring_radius(bodice, L, 0.012, waist_z, L['hips'].z - 0.07)
        prof = lambda th: max(pb(th), pt(th))
        full_z = L['hips'].z - 0.06
        skirt = loft_skirt('cloth_kirtleskirt', rig, L, waist_z, L['ankle'].z - 0.02, wprof, 0.42, rings=16, folds=17, fold_amp=0.016, full_r=prof, full_z=full_z)
        apron = loft_skirt('cloth_apron', rig, L, waist_z + 0.005, L['knee'].z - 0.12, lambda th: wprof(th) + 0.01, 0.3, rings=10, folds=9, fold_amp=0.008, full_r=lambda th: prof(th) + 0.014, full_z=full_z)
        # an apron covers only the front: cut away the back of the ring
        abm = bmesh.new(); abm.from_mesh(apron.data)
        cx, cy = L['hips'].x, L['hips'].y
        bmesh.ops.delete(abm, geom=[f for f in abm.faces if abs(math.atan2(f.calc_center_median().x - cx, -(f.calc_center_median().y - cy))) > 1.25], context='FACES')
        bmesh.ops.delete(abm, geom=[v for v in abm.verts if not v.link_faces], context='VERTS')
        abm.to_mesh(apron.data); abm.free()
        shoes = cut(body, 'cloth_boots', lambda i: co[i].z < L['ankle'].z + 0.07 and wsum(W[i], HAND_BONES + ARM_BONES) < 0.1, 0.008)
        relax(shoes, iters=10, factor=0.5, keep=lambda v: v.co.z < 0.004)
        relax(shoes, iters=6, factor=0.6, boundary_only=True)
        belt = cut(body, 'cloth_belt', lambda i: abs(co[i].z - waist_z) < 0.014 and wsum(W[i], ARM_BONES + HAND_BONES) < 0.1, 0.012)
        made = [bodice, skirt, apron, shoes, belt]
        covered = [(top[i] and co[i].z < neck_lim(co[i], 0.09) - 0.05 and sleeve_ok(i, 1.84)) or (co[i].z < waist_z and co[i].z > L['ankle'].z + 0.07 and wsum(W[i], HAND_BONES + ARM_BONES) < 0.05) or (co[i].z < L['ankle'].z + 0.03 and wsum(W[i], HAND_BONES) < 0.05) for i in range(n)]
    for ob in made:
        crease_shading(ob)
    import os
    if not os.environ.get('NOHIDE'):
        hide_under(body, covered)
    return made
