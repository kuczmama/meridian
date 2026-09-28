import { NodeIO } from '@gltf-transform/core';
import { ALL_EXTENSIONS } from '@gltf-transform/extensions';
import { getBounds } from '@gltf-transform/core';
import { execFileSync } from 'child_process';
import fs from 'fs';
import path from 'path';
const SRC = '../dl/mdl', OUT = process.argv[2];
const big = /Bed|Cabinet|Commode|cabinet|bookshelf|Table|table|sofa|Sofa|day_bed|drawer|display|spinning|screen|Chandelier|chandelier|Chair|chair/;
import { MeshoptDecoder, MeshoptEncoder } from 'meshoptimizer';
await MeshoptDecoder.ready;
const io = new NodeIO().registerExtensions(ALL_EXTENSIONS).registerDependencies({ 'meshopt.decoder': MeshoptDecoder, 'meshopt.encoder': MeshoptEncoder });
const man = {};
for (const n of fs.readdirSync(SRC).sort()) {
  const src = `${SRC}/${n}/${n}.gltf`, dst = `${OUT}/${n}.glb`;
  if (!fs.existsSync(src)) continue;
  try {
    const doc0 = await io.read(src);
    let tris = 0; for (const m of doc0.getRoot().listMeshes()) for (const p of m.listPrimitives()) { const ix = p.getIndices(); tris += (ix ? ix.getCount() : p.getAttribute('POSITION').getCount()) / 3; }
    const ratio = tris > 12000 ? Math.max(0.05, 12000 / tris) : 1;
    const args = ['gltf-transform', 'optimize', src, dst, '--compress', 'meshopt', '--texture-compress', 'webp', '--texture-size', big.test(n) ? '1024' : '512', '--instance', 'false', '--palette', 'false'];
    if (ratio < 1) args.push('--simplify-ratio', String(ratio.toFixed(3)), '--simplify-error', '0.002'); else args.push('--simplify', 'false');
    if (!fs.existsSync(dst)) execFileSync('npx', args, { stdio: 'pipe' });
    const doc = await io.read(dst);
    const b = getBounds(doc.getRoot().listScenes()[0]);
    man[n] = { min: b.min.map(v => +v.toFixed(3)), max: b.max.map(v => +v.toFixed(3)), tris: Math.round(tris * ratio), kb: Math.round(fs.statSync(dst).size / 1024) };
    console.log(n, man[n].tris, man[n].kb + 'KB', man[n].max.map((v, i) => (v - man[n].min[i]).toFixed(2)).join('x'));
  } catch (e) { console.log('FAIL', n, String(e.message || e).slice(0, 200)); }
}
fs.writeFileSync(`${OUT}/models.json`, JSON.stringify(man));
