import bpy, os
SP = os.path.dirname(os.path.abspath(__file__))
bpy.ops.preferences.extension_repo_add(name='user_default', type='LOCAL') if 'user_default' not in [r.module for r in bpy.context.preferences.extensions.repos] else None
print([ (r.module, r.directory) for r in bpy.context.preferences.extensions.repos])
r = bpy.ops.extensions.package_install_files(repo='user_default', filepath=SP + '/mpfb_ext.zip', enable_on_install=True)
print('install', r)
bpy.ops.wm.save_userpref()
import addon_utils
print([m.__name__ for m in addon_utils.modules() if 'mpfb' in m.__name__])
