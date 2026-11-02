import json,sys,re,collections,glob
R=sorted(glob.glob('/home/claude/work/vp/roh_*'))[-1]
J=lambda f: json.load(open(f'{R}/{f}'))
BLOCK=['1INCH','ADA','ALGO','ANKR','API3','APT','ATOM','BLUR','BNT','CHZ','CRO','DEEP','DOT','EDEN','EGLD','ETC','FIL','FLR','FRAX','GRT','ICP','KAIA','LAYER','LINEA','LPT','MANTA','MEGA','METIS','MOVE','PUFFER','RON','S','SCR','STX','SWELL','SYN','TAIKO','TIA','VVV','WLD','XLM','XPL','XRP','XTZ','ZETA','ZK','PEAQ','VELO','AIOZ','ACH','TRAC','AXIS']
assets={a['symbol']:a['name'] for a in J('bitvavo_assets.json')}
tick={p['market']:float(p['price']) for p in J('bitvavo_ticker_price.json')}
cg=J('coingecko_coins_list.json')
bysym=collections.defaultdict(list)
for c in cg: bysym[c['symbol'].lower()].append(c)
norm=lambda s: re.sub(r'[^a-z0-9]','',s.lower().replace('token','').replace('protocol','').replace('network',''))
pap=J('coinpaprika_tickers.json'); papsym=collections.defaultdict(list)
for p in pap: papsym[p['symbol'].upper()].append(p)
prot=J('llama_protocols.json'); byg=collections.defaultdict(list)
for p in prot:
    if p.get('gecko_id'): byg[p['gecko_id']].append(p)
chains=J('llama_chains.json'); chg={c['gecko_id']:c for c in chains if c.get('gecko_id')}
ov={k:{str(e['defillamaId']):e for e in J(f)['protocols']} for k,f in (('fees','llama_fees.json'),('rev','llama_revenue.json'),('hold','llama_holdersrevenue.json'))}
ovname={k:{e['name'].lower():e for e in v.values()} for k,v in ov.items()}
res={}
for s in BLOCK:
    name=assets.get(s); cands=bysym.get(s.lower(),[])
    exact=[c for c in cands if norm(c['name'])==norm(name or '')]
    if len(exact)==1: cid=exact[0]['id']; how='Kürzel+Name exakt'
    elif len(cands)==1: cid=cands[0]['id']; how='Kürzel eindeutig, Name abweichend: '+cands[0]['name']
    else:
        part=[c for c in cands if norm(name or 'x') in norm(c['name']) or norm(c['name']) in norm(name or 'x')]
        cid=part[0]['id'] if len(part)==1 else None; how=('Name enthält' if cid else f'mehrdeutig ({len(cands)}): '+', '.join(c['id'] for c in cands[:6]))
    # paprika
    pc=[p for p in papsym.get(s,[]) if norm(p['name'])==norm(name or '')] or papsym.get(s,[])
    pp=sorted(pc,key=lambda p:p.get('rank') or 1e9)[0] if pc else None
    # llama
    ids=set(); parents=set()
    for p in byg.get(cid,[]) if cid else []:
        ids.add(str(p['id']))
        if p.get('parentProtocol'): parents.add(p['parentProtocol'])
    tot={}
    matched=[]
    for k in ('fees','rev','hold'):
        sel=[e for e in ov[k].values() if str(e['defillamaId']) in ids or (e.get('parentProtocol') in parents)]
        tot[k]=sum((e.get('total1y') or 0) for e in sel) if sel else None
        if k=='fees': matched=[(e['name'],e.get('category'),e.get('protocolType'),e.get('total1y')) for e in sel]
    chain=chg.get(cid) if cid else None
    if chain:
        ce={k:ovname[k].get(chain['name'].lower()) for k in ov}
        tot['chainfees']=ce['fees'].get('total1y') if ce['fees'] else None
        tot['chainrev']=ce['rev'].get('total1y') if ce['rev'] else None
        tot['chainname']=chain['name']
    res[s]=dict(name=name,cg=cid,how=how,price=tick.get(s+'-EUR'),pap=pp and pp['id'],max=pp and pp.get('max_supply'),total=pp and pp.get('total_supply'),circ=pp and pp.get('circulating_supply'),llama=matched,**tot)
json.dump(res,open('/home/claude/work/vp/map.json','w'),indent=1)
for s,r in res.items(): print(s,'|',r['name'],'|',r['cg'],'|',r['how'][:50],'| pap',r['pap'],r['max'],r['total'],'| fees',r.get('fees'),'rev',r.get('rev'),'hold',r.get('hold'),'| chain',r.get('chainname'),r.get('chainfees'),'|',r['llama'][:3])
