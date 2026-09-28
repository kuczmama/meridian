import json, urllib.request, os, sys, concurrent.futures as cf
op=urllib.request.build_opener(); op.addheaders=[('User-Agent','meridian-asset-fetch/1.0')]; urllib.request.install_opener(op)
names = sys.argv[1].split(',')
out = 'dl/tex'
def get(n):
    try:
        f = json.load(urllib.request.urlopen(f'https://api.polyhaven.com/files/{n}', timeout=30))
        got = []
        for key, alts in [('Diffuse', ['Diffuse']), ('nor_gl', ['nor_gl']), ('Rough', ['Rough', 'rough']), ('AO', ['AO'])]:
            for a in alts:
                if a in f and '1k' in f[a]:
                    fm = f[a]['1k'].get('jpg') or f[a]['1k'].get('png')
                    p = f'{out}/{n}_{key}.jpg'
                    if not os.path.exists(p): urllib.request.urlretrieve(fm['url'], p)
                    got.append(key); break
        return n, got
    except Exception as e: return n, 'ERR ' + str(e)
with cf.ThreadPoolExecutor(8) as ex:
    for n, g in ex.map(get, names): print(n, g)
