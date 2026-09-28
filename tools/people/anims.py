# The shared clip library: one rig, every mocap clip, exported with no mesh. Any character with the same bones plays them.
import sys, os, json, bpy
SP = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, SP)
import addon_utils
addon_utils.enable('bl_ext.user_default.mpfb', default_set=True)
from bl_ext.user_default.mpfb.services.humanservice import HumanService
from bl_ext.user_default.mpfb.services.targetservice import TargetService
import retarget
bpy.context.scene.render.fps = 30
for o in list(bpy.data.objects): bpy.data.objects.remove(o)
m = TargetService.get_default_macro_info_dict(); m.update(gender=1.0, age=0.5, muscle=0.5, weight=0.5)
bm = HumanService.create_human(macro_detail_dict=m, detailed_helpers=True, extra_vertex_groups=False)
rig = HumanService.add_builtin_rig(bm, 'cmu_mb')
B = SP + '/../bvh/'
CLIPS = [
    dict(name='walk', bvh='07_01', loop=(0.9, 1.4), in_place=True),
    dict(name='walkslow', bvh='07_04', loop=(1.1, 1.8), in_place=True),
    dict(name='run', bvh='09_02', loop=(0.5, 0.9), in_place=True),
    dict(name='march', bvh='20_06', loop=(0.9, 1.4), in_place=True),
    dict(name='idle', bvh='40_11', start=300, end=3000, loop=(5.0, 9.0)),
    dict(name='talk', bvh='18_08', start=100, end=1500, loop=(5.0, 9.0)),
    dict(name='sit', bvh='13_04', start=500, end=1060, loop=(3.0, 4.4)),
    dict(name='kneel', bvh='23_03', start=260, end=560, loop=(1.4, 2.4)),
    dict(name='sweep', bvh='13_23', start=200, end=2400, loop=(2.5, 5.0)),
    dict(name='drink', bvh='13_09', start=100, end=1000, loop=(4.0, 7.0)),
    dict(name='laugh', bvh='13_14', start=100, end=1500, loop=(3.0, 6.0)),
    dict(name='wave', bvh='13_26', start=100, end=1500, loop=(2.5, 5.0)),
    dict(name='dance', bvh='60_01', start=200, end=2000, loop=(3.0, 6.0)),
]
meta = {}
for c in CLIPS:
    a = retarget.retarget(rig, B + c['bvh'] + '.bvh', c['name'], start=c.get('start', 0), end=c.get('end'), loop=c.get('loop'), in_place=c.get('in_place', False))
    meta[c['name']] = {'stride': round(a['stride'], 3), 'dur': round(a['dur'], 3)}
hips = rig.data.bones['Hips'].head_local
legs = sum(rig.data.bones[k].length for k in ('LeftUpLeg', 'LeftLeg'))
meta['_rig'] = {'hipsZ': round(hips.z, 4), 'hipsY': round(hips.y, 4), 'legs': round(legs, 4)}
for o in list(bpy.data.objects):
    if o.type == 'MESH': bpy.data.objects.remove(o)
out = SP + '/../chars/anims.glb'
bpy.ops.export_scene.gltf(filepath=out, export_format='GLB', export_animation_mode='NLA_TRACKS', export_materials='NONE')
json.dump(meta, open(SP + '/../chars/anims.json', 'w'), indent=1)
print('exported', out, os.path.getsize(out)); print(json.dumps(meta))
