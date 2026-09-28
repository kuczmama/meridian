import { NodeIO, getBounds } from '@gltf-transform/core';
import { ALL_EXTENSIONS } from '@gltf-transform/extensions';
import { MeshoptDecoder, MeshoptEncoder, MeshoptSimplifier } from 'meshoptimizer';
import { simplify, weld, meshopt } from '@gltf-transform/functions';
import fs from 'fs';
await MeshoptDecoder.ready; await MeshoptEncoder.ready; await MeshoptSimplifier.ready;
const io = new NodeIO().registerExtensions(ALL_EXTENSIONS).registerDependencies({ 'meshopt.decoder': MeshoptDecoder, 'meshopt.encoder': MeshoptEncoder });
const R = process.argv[2];
for (const f of fs.readdirSync(R).filter(f => f.endsWith('.glb'))) {
  const doc = await io.read(`${R}/${f}`);
  const b = getBounds(doc.getRoot().listScenes()[0]), size = Math.max(...b.max.map((v, i) => v - b.min[i]));
  let tris = 0; for (const m of doc.getRoot().listMeshes()) for (const p of m.listPrimitives()) tris += (p.getIndices() ? p.getIndices().getCount() : p.getAttribute('POSITION').getCount()) / 3;
  const target = size < 0.35 ? 1200 : size < 0.8 ? 2500 : size < 1.5 ? 5000 : 8000;
  if (tris <= target * 1.1) { console.log(f, 'keep', tris); continue; }
  await doc.transform(weld(), simplify({ simplifier: MeshoptSimplifier, ratio: target / tris, error: 0.01 }), meshopt({ encoder: MeshoptEncoder, level: 'high' }));
  let t2 = 0; for (const m of doc.getRoot().listMeshes()) for (const p of m.listPrimitives()) t2 += (p.getIndices() ? p.getIndices().getCount() : p.getAttribute('POSITION').getCount()) / 3;
  await io.write(`${R}/${f}`, doc);
  console.log(f, size.toFixed(2), tris, '->', t2);
}
