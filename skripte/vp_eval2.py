import json,re,collections,glob,datetime
R=sorted(glob.glob('/home/claude/work/vp/roh_*'))[-1]
J=lambda f: json.load(open(f'{R}/{f}'))
FX=1.1216
REST=json.load(open('/home/claude/work/vp/rest.json'))
assets={a['symbol']:a['name'] for a in J('bitvavo_assets.json')}
tick={p['market']:float(p['price']) for p in J('bitvavo_ticker_price.json')}
norm=lambda s: re.sub(r'[^a-z0-9]','',(s or '').lower())
cg=J('coingecko_coins_list.json'); bysym=collections.defaultdict(list)
for c in cg: bysym[c['symbol'].lower()].append(c)
pap=J('coinpaprika_tickers.json'); psym=collections.defaultdict(list)
for p in pap: psym[p['symbol'].strip().upper()].append(p)
prot=J('llama_protocols.json'); byg=collections.defaultdict(list)
for p in prot:
    if p.get('gecko_id'): byg[p['gecko_id']].append(p)
chains=J('llama_chains.json'); chg={c['gecko_id']:c for c in chains if c.get('gecko_id')}; chsym=collections.defaultdict(list)
for c in chains:
    if c.get('tokenSymbol'): chsym[c['tokenSymbol'].upper()].append(c)
OV={k:J(f)['protocols'] for k,f in (('fees','llama_fees.json'),('rev','llama_revenue.json'),('hold','llama_holdersrevenue.json'))}
IDX={k:{str(e['defillamaId']):e for e in v} for k,v in OV.items()}
mv={x['asset']:(x['time'][:10],float(x['CapMVRVCur'])) for x in J('coinmetrics_mvrv_dgb_xvg.json')['data']}
CAT={'Dexs':'DeFi','DEX Aggregator':'DeFi','Derivatives':'DeFi','Lending':'DeFi','CDP':'DeFi','Yield':'DeFi','Liquid Staking':'DeFi','Restaking':'DeFi','Liquid Restaking':'DeFi','Bridge':'DeFi','Cross Chain Bridge':'DeFi','Prediction Market':'DeFi','Basis Trading':'DeFi','Indexes':'DeFi','Onchain Capital Allocator':'DeFi','Launchpad':'DeFi','NFT Marketplace':'DeFi','Services':'DeFi',
     'Oracle':'Umsatz','Developer Tools':'Umsatz','Data':'Umsatz','RWA':'Umsatz','Gaming':'Umsatz','Decentralized AI':'Umsatz','AI Agents':'Umsatz','DePIN':'Umsatz','Storage':'Umsatz'}
TXT={'DeFi':'DeFi und Cashflow','Umsatz':'Umsatzklasse (Oracle, RWA, Gaming oder Compute)','Plattform':'Plattform','offen':'Klasse offen'}
TH={'Plattform':400,'DeFi':150,'Umsatz':200,'offen':400}
out={}
for s in REST:
    name=assets.get(s); price=tick.get(s+'-EUR')
    # Paprika per Kurs
    pc=[p for p in psym.get(s,[]) if price and p.get('quotes',{}).get('EUR',{}).get('price') and abs(p['quotes']['EUR']['price']/price-1)<=0.10]
    pp=pc[0] if len(pc)==1 else None
    # CoinGecko
    cands=bysym.get(s.lower(),[])
    ex=[c for c in cands if norm(c['name'])==norm(name)] or ([c for c in cands if pp and norm(c['name'])==norm(pp['name'])])
    cid=ex[0]['id'] if len(ex)==1 else (cands[0]['id'] if len(cands)==1 else None)
    ident=('belegt' if (pp or cid) else 'klären')
    # DefiLlama
    pid={str(p['id']):p for p in prot} if 'PID' not in globals() else PID
    globals()['PID']=pid
    nn=norm(name); sel={}; weak=False
    for e in OV['fees']:
        i=str(e['defillamaId']); p=pid.get(i,{})
        psy=(p.get('symbol') or '').upper(); pg=p.get('gecko_id')
        if e.get('protocolType')=='chain': continue
        bn=[norm(w) for w in re.split(r'[\s.()]+',name or '') if len(norm(w))>=3]
        en=norm(e['name'])
        namesim=any(w in en for w in bn) or any(norm(w) in nn for w in re.split(r'[\s.()]+',e['name']) if len(norm(w))>=3)
        strong=(cid and pg==cid) or (psy==s and namesim)
        exactname=nn and len(nn)>=4 and norm(e['name'])==nn and psy in ('','-') and not pg
        if strong: sel[i]=e
        elif exactname: sel[i]=e; weak=True
    par={e.get('parentProtocol') for e in sel.values() if e.get('parentProtocol')}
    for e in OV['fees']:
        if e.get('protocolType')!='chain' and e.get('parentProtocol') in par: sel[str(e['defillamaId'])]=e
    chain=None
    cands_ch=([chg[cid]] if cid in chg else [])+[c for c in chsym.get(s,[]) if norm(c['name'])==nn]
    for c in cands_ch:
        for e in OV['fees']:
            if e.get('protocolType')=='chain' and e['name'].lower()==c['name'].lower(): sel[str(e['defillamaId'])]=e; chain=c['name']
    tot={k:(sum((IDX[k].get(i,{}).get('total1y') or 0) for i in sel)/FX if any(i in IDX[k] for i in sel) else None) for k in ('fees','rev','hold')}
    cats=collections.Counter(e.get('category') for e in sel.values())
    if chain: typ='Plattform'
    elif sel:
        mapped={CAT.get(c) for c in cats}; typ=mapped.pop() if len(mapped)==1 and None not in mapped else 'offen'
    else: typ=None
    sup=None; sart=None
    if pp:
        if pp.get('max_supply'): sup=pp['max_supply']; sart='Höchstmenge'
        elif pp.get('total_supply'): sup=pp['total_supply']; sart='Gesamtmenge'
    fdv=price*sup if price and sup else None
    r=dict(name=name,cg=cid,pap=pp and pp['id'],ident=ident,preis=price,pdev=(price/pp['quotes']['EUR']['price']-1) if pp else None,menge=sup,mengenart=sart,fdv=fdv,quellen=[e['name']+' ('+str(e.get('category'))+')' for e in sel.values()],typ=typ,klasse=TXT.get(typ,'') ,**tot,weak=weak)
    if s in ('DGB','XVG'):
        d,v=mv.get(s.lower(),(None,None)); r['mvrv']=v; r['mvrv_datum']=d
        r['klasse']='Geldwert (Proof of Work) – Klassenfrage'
        r['ergebnis']='Klassenfrage → Erstbewertung' if v is not None and v<=5 else 'Daten klären'
        r['grund']=(f"Kein Ertragsmodell als Plattform; als Geldwert MVRV {v:.2f}".replace('.',',')+f" (Coin Metrics, {d}). Klasse in der Erstbewertung nach § 5 begründen, Zweitprüfung blind." ) if v else 'MVRV nicht verfügbar'
    elif ident=='klären':
        r['ergebnis']='Daten klären'; r['grund']='Identität nicht eindeutig belegbar (Q-01): kein Eintrag mit passendem Kurs bei CoinPaprika und keine eindeutige CoinGecko-Kennung'
    elif not sel or (tot['fees'] in (None,0) and tot['rev'] in (None,0)):
        r['ergebnis']='kein messbarer Ertrag'
        r['grund']='Bei DefiLlama kein Ertrag auffindbar (Kennung, Kürzel und Name geprüft'+ (f'; Treffer ohne Ertrag: {", ".join(r["quellen"])}' if sel else '') +'). Ohne Hauptkennzahl keine Bewertungsnote (§ 9 Absatz 4); derzeit höchstens „Bewertung ausstehend“. Vorläufig: Quellen außerhalb DefiLlama nicht abgefragt.'
    elif fdv is None:
        r['ergebnis']='Daten klären'; r['grund']='Ertrag vorhanden, aber Menge nicht belegt (keine Mengenangabe bei CoinPaprika)'
    else:
        th=TH[typ]
        if typ=='Plattform': upper=tot['fees']; metric=tot['fees']
        elif typ=='DeFi': upper=tot['rev'] if tot['rev'] else tot['fees']; metric=tot['hold'] if tot['hold'] else None
        elif typ=='Umsatz': upper=tot['fees'] or tot['rev']; metric=tot['rev'] if tot['rev'] else None
        else: upper=max(x for x in (tot['fees'],tot['rev'],tot['hold']) if x); metric=None
        mu=fdv/upper; mm=fdv/metric if metric else None
        r.update(mult_upper=mu,mult_metric=mm,schwelle=th)
        if mu>1.25*th and weak: r['ergebnis']='Daten klären'; r['grund']='Ertragsdaten nur über den Namen zugeordnet; für ein belegtes Ausscheiden reicht das nicht (Q-01)'
        elif mu>1.25*th: r['ergebnis']='scheidet aus (robust)'
        elif mm is not None and mm<=th: r['ergebnis']='besteht → Erstbewertung'
        else: r['ergebnis']='grenznah → Erstbewertung'
        r.setdefault('grund','')
        if weak and not r['grund']: r['grund']='Hinweis: Ertragsdaten teils nur über den Namen zugeordnet. '
    out[s]=r
json.dump(out,open('/home/claude/work/vp/ergebnis2.json','w'),indent=1,ensure_ascii=False)
print(collections.Counter(r['ergebnis'] for r in out.values()))
for s,r in out.items():
    if r['ergebnis'] not in ('kein messbarer Ertrag',):
        print(f"{s:7} {r['ergebnis']:28} {r['typ']} | FDV {r['fdv'] and round(r['fdv']/1e6,1)} | fees {r['fees'] and round(r['fees'])} rev {r['rev'] and round(r['rev'])} hold {r['hold'] and round(r['hold'])} | U {r.get('mult_upper') and round(r['mult_upper'])} M {r.get('mult_metric') and round(r['mult_metric'])} | {r['quellen'][:4]} | {r['grund'][:80]}")
