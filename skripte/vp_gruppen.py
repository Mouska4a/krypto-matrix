import json,re,glob,collections
R=sorted(glob.glob('/home/claude/work/vp/roh_*'))[-1]
J=lambda f: json.load(open(f'{R}/{f}'))
o=json.load(open('/home/claude/work/vp/ergebnis2.json'))
norm=lambda s: re.sub(r'[^a-z0-9]','',(s or '').lower())
P=J('llama_protocols.json'); vols={k:J(f'llama_overview_{k}.json')['protocols'] for k in ('dexs','options','aggregators')}
pid={str(p['id']):p for p in P}
def sim(name,pname):
    bn=[norm(w) for w in re.split(r'[\s.()]+',name or '') if len(norm(w))>=3]
    en=norm(pname); return any(w in en for w in bn) or any(norm(w) in norm(name) for w in re.split(r'[\s.()]+',pname) if len(norm(w))>=3)
res={}
for s,r in o.items():
    if not r['ergebnis'].startswith('keine Ertragsdaten'): continue
    cid=r.get('cg'); nm=r['name']
    tvl=[p for p in P if (cid and p.get('gecko_id')==cid) or ((p.get('symbol') or '').upper()==s and sim(nm,p['name']))]
    ids={str(p['id']) for p in tvl}; par={p.get('parentProtocol') for p in tvl if p.get('parentProtocol')}
    vol={}
    for k,lst in vols.items():
        sel=[e for e in lst if str(e.get('defillamaId')) in ids or (e.get('parentProtocol') in par)]
        if sel: vol[k]=sum((e.get('total1y') or 0) for e in sel)/1.1216
    t=sum((p.get('tvl') or 0) for p in tvl)/1.1216
    res[s]=dict(name=nm,protokolle=[p['name']+' ('+str(p.get('category'))+')' for p in tvl][:5],tvl=t,vol=vol,gruppe='A' if (tvl or vol) else 'B',fdv=r.get('fdv'))
json.dump(res,open('/home/claude/work/vp/gruppen.json','w'),indent=1,ensure_ascii=False)
A={s:v for s,v in res.items() if v['gruppe']=='A'}
print('A',len(A),'B',len(res)-len(A))
for s,v in sorted(A.items(),key=lambda kv:-(kv[1]['fdv'] or 0)):
    print(f"{s:7} {v['name'][:22]:22} FDV {round((v['fdv'] or 0)/1e6)} Mio | TVL {round(v['tvl']/1e6,1)} Mio | Vol {({k:round(x/1e6) for k,x in v['vol'].items()})} | {v['protokolle'][:3]}")
