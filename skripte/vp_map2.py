import json,re,collections,glob
R=sorted(glob.glob('/home/claude/work/vp/roh_*'))[-1]
J=lambda f: json.load(open(f'{R}/{f}'))
REST=json.load(open('/home/claude/work/vp/rest.json'))
assets={a['symbol']:a['name'] for a in J('bitvavo_assets.json')}
cg=J('coingecko_coins_list.json'); bysym=collections.defaultdict(list)
for c in cg: bysym[c['symbol'].lower()].append(c)
norm=lambda s: re.sub(r'[^a-z0-9]','',(s or '').lower().replace('token','').replace('protocol','').replace('network','').replace('coin',''))
prot=J('llama_protocols.json'); byg=collections.defaultdict(list)
for p in prot:
    if p.get('gecko_id'): byg[p['gecko_id']].append(p)
chains=J('llama_chains.json'); chg={c['gecko_id']:c for c in chains if c.get('gecko_id')}
F=J('llama_fees.json')['protocols']; Fid={str(e['defillamaId']):e for e in F}; Fname={e['name'].lower():e for e in F}
out={}
for s in REST:
    name=assets.get(s); cands=bysym.get(s.lower(),[])
    exact=[c for c in cands if norm(c['name'])==norm(name)]
    if len(exact)==1: cid=exact[0]['id']; how='exakt'
    elif len(cands)==1: cid=cands[0]['id']; how='Kürzel eindeutig ('+cands[0]['name']+')'
    else:
        part=[c for c in cands if norm(name) and (norm(name) in norm(c['name']) or norm(c['name']) in norm(name))]
        cid=part[0]['id'] if len(part)==1 else None
        how='Name enthält' if cid else f'mehrdeutig/fehlt ({len(cands)})'
    ids=set(); parents=set()
    for p in byg.get(cid,[]) if cid else []:
        ids.add(str(p['id']))
        if p.get('parentProtocol'): parents.add(p['parentProtocol'])
    sel=[e for e in F if str(e['defillamaId']) in ids or e.get('parentProtocol') in parents]
    ch=chg.get(cid) if cid else None
    che=Fname.get(ch['name'].lower()) if ch else None
    out[s]=dict(name=name,cg=cid,how=how,prot=[(e['name'],e.get('category')) for e in sel],chain=ch and ch['name'],chainfee=bool(che))
json.dump(out,open('/home/claude/work/vp/map2.json','w'),indent=1,ensure_ascii=False)
cats=collections.Counter(c for v in out.values() for _,c in v['prot'])
print(cats)
print('ohne Identität',[s for s,v in out.items() if not v['cg']])
print('mit Kette',sum(1 for v in out.values() if v['chainfee']),'mit Protokoll',sum(1 for v in out.values() if v['prot']),'ohne beides',sum(1 for v in out.values() if not v['prot'] and not v['chainfee']))
