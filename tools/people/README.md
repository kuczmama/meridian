# Building the townsfolk

The bodies, clothes and motion clips in `people/` are generated here with Blender run headless as a Python module.

1. `uv venv -p 3.11 bl && uv pip install -p bl/bin/python bpy==4.5.4 pillow`
2. Get [MPFB](https://github.com/makehumancommunity/mpfb2) (v2.0.17), zip `src/mpfb` to `mpfb_ext.zip` next to these scripts, then `BLENDER_USER_RESOURCES=$PWD/blres bl/bin/python install.py`.
3. Put the MakeHuman core assets (CC0) in `mhassets/base/` (skins, eyes with `high-poly`, eyebrows, eyelashes, hair), and CMU BVH clips (cgspeed conversion) in `../bvh/`.
4. `./cast.sh` builds the eight body archetypes into `../chars/`; `bl/bin/python anims.py` builds the shared clip library `anims.glb` and `anims.json`.
5. Compress each with `npx @gltf-transform/cli meshopt in.glb out.glb` and copy into `people/`.

- `build.py`: one character from a JSON spec (sex, age, build, hair, brows, outfit).
- `tailor.py`: cuts, drapes and lofts the clothes from the body, and hides the skin under them.
- `retarget.py`: CMU BVH onto the MPFB `cmu_mb` rig, looped and made in-place.
