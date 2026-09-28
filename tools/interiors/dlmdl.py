import json, urllib.request, os, sys, concurrent.futures as cf
op=urllib.request.build_opener(); op.addheaders=[('User-Agent','meridian-asset-fetch/1.0')]; urllib.request.install_opener(op)
names = sys.argv[1].split(',')
def get(n):
    try:
        f = json.load(urllib.request.urlopen(f'https://api.polyhaven.com/files/{n}', timeout=30))
        g = f['gltf']['1k']['gltf']; d = f'dl/mdl/{n}'; os.makedirs(d, exist_ok=True)
        open(f"{d}/{n}.gltf","wb").write(urllib.request.urlopen(g["url"],timeout=60).read())
        for p, inc in g.get('include', {}).items():
            os.makedirs(os.path.dirname(f'{d}/{p}') or d, exist_ok=True)
            open(f"{d}/{p}","wb").write(urllib.request.urlopen(inc["url"],timeout=120).read())
        return n, 'ok'
    except Exception as e: return n, 'ERR ' + str(e)
with cf.ThreadPoolExecutor(8) as ex:
    for n, g in ex.map(get, names): print(n, g, flush=True)
