# Build one character: body from MakeHuman, CMU rig, eyes/brows/lashes/teeth/hair, tailored clothes, mocap clips.
# usage: python build.py '<json spec>'
import sys, os, json, bpy, bmesh
SP = os.path.dirname(os.path.abspath(__file__)); A = SP + '/mhassets/base/'
sys.path.insert(0, SP)
import addon_utils
addon_utils.enable('bl_ext.user_default.mpfb', default_set=True)
from bl_ext.user_default.mpfb.services.humanservice import HumanService
from bl_ext.user_default.mpfb.services.targetservice import TargetService
import retarget, tailor

spec = json.loads(sys.argv[-1])
bpy.context.scene.render.fps = 30
for o in list(bpy.data.objects): bpy.data.objects.remove(o)
m = TargetService.get_default_macro_info_dict()
for k in ('gender', 'age', 'muscle', 'weight', 'height', 'proportions', 'cupsize', 'firmness'):
    if k in spec: m[k] = spec[k]
m['race'] = spec.get('race', {'caucasian': 0.9, 'african': 0.05, 'asian': 0.05})
bm = HumanService.create_human(macro_detail_dict=m, detailed_helpers=True, extra_vertex_groups=False)
rig = HumanService.add_builtin_rig(bm, 'cmu_mb')
parts = [('eyes/high-poly/high-poly.mhclo', 'Eyes'), (f"eyebrows/{spec.get('brow', 'eyebrow001')}/{spec.get('brow', 'eyebrow001')}.mhclo", 'Eyebrows'),
         ('eyelashes/eyelashes01/eyelashes01.mhclo', 'Eyelashes')]
if spec.get('hair'):
    parts.append((f"hair/{spec['hair']}/{spec['hair']}.mhclo", 'Hair'))
for f, t in parts:
    HumanService.add_mhclo_asset(A + f, bm, asset_type=t, subdiv_levels=0, material_type='MAKESKIN')
# bake MakeHuman's shape targets into the mesh, so everything below measures the body as it really is
def bake_keys(o):
    if o.type == 'MESH' and o.data.shape_keys:
        bpy.context.view_layer.objects.active = o
        for q in bpy.context.selected_objects: q.select_set(False)
        o.select_set(True)
        bpy.ops.object.shape_key_remove(all=True, apply_mix=True)
for o in bpy.data.objects: bake_keys(o)
# MakeHuman's helper geometry goes for good once the rig is fitted
for md in [md for md in bm.modifiers if md.type == 'MASK']: bm.modifiers.remove(md)
gi = bm.vertex_groups['body'].index
b2 = bmesh.new(); b2.from_mesh(bm.data)
dl = b2.verts.layers.deform.active
bmesh.ops.delete(b2, geom=[v for v in b2.verts if gi not in v[dl] or v[dl][gi] < 0.5], context='VERTS')
b2.to_mesh(bm.data); b2.free()
bones = set(b.name for b in rig.data.bones)
for g in list(bm.vertex_groups):
    if g.name not in bones: bm.vertex_groups.remove(g)
if spec.get('outfit'):
    made = tailor.dress(bm, rig, spec['outfit'])
    # one mesh for the whole outfit (one draw call): each garment's id rides in the colour's green channel
    GID = {'tunic': 0, 'tunicskirt': 1, 'kirtle': 2, 'kirtleskirt': 3, 'apron': 4, 'hose': 5, 'boots': 6, 'belt': 7}
    for o in made:
        gid = GID[o.name[6:]]
        ca = o.data.color_attributes[0]
        for c in ca.data:
            r = c.color[0]
            c.color = (r, (gid + 0.5) / 8.0, 0.0, 1.0)
    for q in bpy.context.selected_objects: q.select_set(False)
    for o in made: o.select_set(True)
    bpy.context.view_layer.objects.active = made[0]
    bpy.ops.object.join()
    made[0].name = 'cloth'; made[0].data.name = 'cloth'
    made = [made[0]]
    print('clothes', [(o.name, len(o.data.vertices)) for o in made])
    L = tailor.landmarks(rig); print('landmarks knee', round(L['knee'].z, 3), 'ankle', round(L['ankle'].z, 3), 'hips', round(L['hips'].z, 3))
    for o in made + [bm]:
        zs = [v.co.z for v in o.data.vertices]; print('  zrange', o.name, round(min(zs), 3), round(max(zs), 3))
    lz = sorted(v.co.z for v in bm.data.vertices if abs(v.co.x) > 0.05 and v.co.z < 0.9); print('  body leg z samples', [round(z, 2) for z in lz[::max(1, len(lz) // 25)]])
print('body verts', len(bm.data.vertices))
# every mesh gets a plain placeholder material; the game assigns real ones by name
for o in bpy.data.objects:
    if o.type == 'MESH':
        o.data.materials.clear()
B = SP + '/../bvh/'
for clip in spec.get('clips', []):
    retarget.retarget(rig, B + clip['bvh'] + '.bvh', clip['name'], start=clip.get('start', 0), end=clip.get('end'), loop=tuple(clip['loop']) if clip.get('loop') else None, in_place=clip.get('in_place', False))
out = SP + '/../chars/' + spec['out'] + '.glb'
bpy.ops.export_scene.gltf(filepath=out, export_format='GLB', export_apply=False, export_animation_mode='NLA_TRACKS' if spec.get('clips') else 'ACTIONS',
                          export_animations=bool(spec.get('clips')), export_materials='NONE', export_vertex_color='ACTIVE', export_all_vertex_colors=False)
print('exported', out, os.path.getsize(out))
