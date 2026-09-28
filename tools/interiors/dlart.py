import json, urllib.request, urllib.parse, os, sys, concurrent.futures as cf
op=urllib.request.build_opener(); op.addheaders=[('User-Agent','Mozilla/5.0 meridian')]; urllib.request.install_opener(op)
B='https://collectionapi.metmuseum.org/public/collection/v1/'
def J(u): return json.load(urllib.request.urlopen(u, timeout=30))
def search(q, dept, n):
    r = J(B + f'search?hasImages=true&departmentId={dept}&q=' + urllib.parse.quote(q))
    return (r.get('objectIDs') or [])[:n]
plan = [('west','portrait',11,40),('west','landscape',11,40),('west','still life',11,30),('west','Madonna',11,25),('west','saint',11,20),('west','village',11,20),('west','harbor',11,15),
        ('east','hanging scroll landscape',6,40),('east','hanging scroll bird',6,30),('east','hanging scroll flowers',6,30)]
meta=[]
def one(args):
    grp, oid = args
    try:
        o = J(B + f'objects/{oid}')
        if not o.get('isPublicDomain') or not o.get('primaryImageSmall'): return None
        if grp=='west' and o.get('classification') not in ('Paintings',): return None
        if grp=='east' and 'scroll' not in (o.get('objectName','')+o.get('classification','')).lower(): return None
        p = f'dl/art/{grp}_{oid}.jpg'
        if not os.path.exists(p): urllib.request.urlretrieve(o['primaryImageSmall'], p)
        return dict(file=p, grp=grp, title=o.get('title'), artist=o.get('artistDisplayName'), date=o.get('objectDate'), id=oid)
    except Exception as e: return None
jobs=[]; seen=set()
for grp,q,d,n in plan:
    try:
        for oid in search(q,d,n):
            if oid not in seen: seen.add(oid); jobs.append((grp,oid))
    except Exception as e: print('search fail',q,e)
with cf.ThreadPoolExecutor(6) as ex:
    for m in ex.map(one, jobs):
        if m: meta.append(m)
json.dump(meta, open('dl/art/meta.json','w'), indent=1)
print(len(meta), sum(m['grp']=='west' for m in meta), sum(m['grp']=='east' for m in meta))
