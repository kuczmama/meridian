# Interior assets

Everything in `interiors/` is CC0 and rebuilt by these scripts (run from a scratch folder, not the repo).

- `dltex.py a,b,c` downloads Poly Haven texture sets (1k diffuse, OpenGL normal, roughness, AO) into `dl/tex`.
  They are converted with ImageMagick to `interiors/tex/<name>_c.webp` (colour), `_n.webp` (normal) and
  `_r.webp` (AO in red, roughness in green), 1024 px for floors and walls, 512 px for fabrics and furniture woods.
- `dlmdl.py a,b,c` downloads Poly Haven models (1k glTF) into `dl/mdl`.
- `models.mjs <out>` turns them into meshopt-compressed GLBs with WebP textures and writes `models.json`
  (each model's bounds, used to fit it to the furniture's nominal size); needs `npm i @gltf-transform/cli`.
- `simplify.mjs <out>` decimates each model by its physical size (small props ~1.2k triangles, furniture 5-8k).
- `dlart.py` fetches public-domain paintings and hanging scrolls from The Met's Open Access API; they are trimmed,
  resized to 512 px WebP and listed in `interiors/art/art.json` as `[file, group, width, height, title, artist, date]`.

Models that don't belong in the period (oil drums, blowtorches, electric chandeliers, labelled bottles, modern frames)
were removed by hand after rendering a contact sheet of every model.
