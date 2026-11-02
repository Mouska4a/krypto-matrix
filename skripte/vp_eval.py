import json,glob,datetime
R=sorted(glob.glob('/home/claude/work/vp/roh_*'))[-1]
J=lambda f: json.load(open(f'{R}/{f}'))
fx_ecb=1.1216  # USD je EUR, EZB 02.11.2026 (Rohbeleg Kaufprüfung)
tick={p['market']:float(p['price']) for p in J('bitvavo_ticker_price.json')}
assets={a['symbol']:a['name'] for a in J('bitvavo_assets.json')}
pap={p['id']:p for p in J('coinpaprika_tickers.json')}
F={e['name']:e for e in J('llama_fees.json')['protocols']}
RV={e['name']:e for e in J('llama_revenue.json')['protocols']}
H={e['name']:e for e in J('llama_holdersrevenue.json')['protocols']}
mv={}
for x in J('coinmetrics_mvrv_etc_xrp_xlm.json')['data']: mv[x['asset']]=(x['time'][:10],float(x['CapMVRVCur']))
TH={'Plattform':400,'DeFi':150,'Umsatz':200}
# Klasse und Datenquelle je Coin – festgelegt nach der Prüfvorschrift (Klasse vor Ansicht des Multiplikators)
S={
'1INCH':('DeFi','DeFi und Cashflow (DEX-Aggregator)',['1inch Aqua'],'1inch-1inch',None),
'ADA':('Plattform','Plattform L1',['Cardano'],'ada-cardano',None),
'ALGO':('Plattform','Plattform L1',['Algorand'],'algo-algorand',None),
'ANKR':('DeFi','DeFi und Cashflow (Liquid Staking)',['Ankr'],'ankr-ankr-network',None),
'API3':('Umsatz','Oracle, Daten und Infrastruktur',['Api3'],'api3-api3',None),
'APT':('Plattform','Plattform L1',['Aptos'],'apt-aptos',None),
'ATOM':('Plattform','Plattform L1 (Cosmos Hub)',['CosmosHub'],'atom-cosmos',None),
'BLUR':('DeFi','DeFi und Cashflow (NFT-Marktplatz)',['Blur Bids'],'blur-blur','Nur „Blur Bids“ bei DefiLlama zugeordnet; Marktplatzgebühren prüfen'),
'BNT':('DeFi','DeFi und Cashflow (DEX)',['Bancor V2.1','Bancor V3'],'bnt-bancor',None),
'CHZ':('Plattform','Plattform L1 (Chiliz Chain)',['Chiliz'],'chz-chiliz',None),
'CRO':('Plattform','Plattform L1 (Cronos)',['Cronos'],'cro-cryptocom-chain',None),
'DEEP':('DeFi','DeFi und Cashflow (Orderbuch-DEX)',['DeepBook V3'],'deep-deepbook-protocol',None),
'DOT':('Plattform','Plattform L1 (Polkadot)',['Polkadot'],'dot-polkadot',None),
'EDEN':('Umsatz','RWA-Infrastruktur',['OpenEden TBILL','OpenEden USDO'],'eden-openeden',None),
'EGLD':('Plattform','Plattform L1',['MultiversX'],'egld-elrond',None),
'ETC':('Plattform','Plattform L1 (Proof of Work) – Klassenfrage Geldwert',['EthereumClassic'],'etc-ethereum-classic','etc'),
'FIL':('Umsatz','Compute, KI und DePIN (Speicher)',['Filecoin'],'fil-filecoin',None),
'FLR':('Plattform','Plattform L1',['Flare'],'flr-flare-network',None),
'FRAX':('DeFi','DeFi und Cashflow (Frax Finance)',['Frax','Fraxlend','Frax Swap','Frax Ether','Frax USD'],'fxs-frax-share','FRAXID'),
'GRT':('Umsatz','Oracle, Daten und Infrastruktur (Indexierung)',['The Graph'],'grt-the-graph',None),
'ICP':('Plattform','Plattform L1',['ICP'],'icp-internet-computer',None),
'KAIA':('Plattform','Plattform L1',['Kaia'],'kaia-kaia',None),
'LAYER':('DeFi','DeFi und Cashflow (Restaking)',['Solayer Restaking'],'layer-solayer',None),
'LINEA':('Plattform','Plattform L2',['Linea'],'linea-linea',None),
'LPT':('Umsatz','Compute, KI und DePIN (Video)',['Livepeer'],'lpt-livepeer',None),
'MANTA':('Plattform','Plattform L2',['Manta'],'manta-manta-network',None),
'MEGA':('Plattform','Plattform L2',['MegaETH'],'mega-megaeth',None),
'METIS':('Plattform','Plattform L2',['Metis'],'metis-metis-token',None),
'MOVE':('Plattform','Plattform L2',['Movement'],'move-movement',None),
'PUFFER':('DeFi','DeFi und Cashflow (Liquid Restaking)',['Puffer Stake','Puffer Vaults'],'puffer-puffer',None),
'RON':('Plattform','Plattform (Ronin)',['Ronin'],'ron-ronin-token',None),
'S':('Plattform','Plattform L1 (Sonic)',['Sonic'],'s-sonic',None),
'SCR':('Plattform','Plattform L2',['Scroll'],'scr-scroll',None),
'STX':('Plattform','Plattform (Bitcoin-L2)',['Stacks'],'stx-stacks',None),
'SWELL':('DeFi','DeFi und Cashflow (Liquid Staking)',['Swell Liquid Staking','Swell Liquid Restaking'],'swell-swell-network',None),
'SYN':('DeFi','DeFi und Cashflow (Brücke)',['Synapse Cross Chain Bridge','Hypercall Perps'],'syn-synapse',None),
'TAIKO':('Plattform','Plattform L2',['Taiko'],'taiko-taiko',None),
'TIA':('Plattform','Plattform (Datenverfügbarkeit)',['Celestia'],'tia-celestia',None),
'VVV':('Umsatz','Compute, KI und DePIN (KI-Inferenz)',['Venice'],'vvv-venice-token',None),
'WLD':('Plattform','Plattform (World Chain)',['World Chain'],'wld-worldcoin','World Chain bei DefiLlama als Kette geführt; Zuordnung der Gebühren zum Token prüfen'),
'XLM':('Plattform','Plattform L1 (Zahlungsnetz) – Klassenfrage Geldwert',['Stellar'],'xlm-stellar','xlm'),
'XPL':('Plattform','Plattform L1 (Plasma)',['Plasma'],'xpl-plasma',None),
'XRP':('Plattform','Plattform L1 (Zahlungsnetz) – Klassenfrage Geldwert',['XRPL'],'xrp-xrp','xrp'),
'XTZ':('Plattform','Plattform L1',['Tezos'],'xtz-tezos',None),
'ZETA':('Plattform','Plattform L1',['ZetaChain'],'zeta-zetachain',None),
'ZK':('Plattform','Plattform L2',['ZKsync Era'],'zk-zksync',None),
'PEAQ':('Plattform','Plattform L1 (DePIN-Kette)',['Peaq'],'peaq-peaq-network',None),
'VELO':(None,'offen',[],'velo-velo','VELO'),
'AIOZ':(None,'Compute, KI und DePIN (vermutet)',[],'aioz-aioz-network','NODATA'),
'ACH':(None,'offen (Zahlungsdienstleister; Firmenumsatz zählt nach D-12 nur über das Netzwerk)',[],'ach-alchemy-pay','NODATA'),
'TRAC':(None,'Oracle, Daten und Infrastruktur (vermutet)',[],'trac-origintrail','NODATA'),
'AXIS':(None,'offen',[],None,'NODATA'),
}
def ann(names,src):
    v=[src[n].get('total1y') for n in names if n in src and src[n].get('total1y') is not None]
    return sum(v)/fx_ecb if v else None
out={}
for s,(cls,cltxt,names,pid,flag) in S.items():
    price=tick.get(s+'-EUR'); p=pap.get(pid) if pid else None
    maxs=p.get('max_supply') if p else None; tots=p.get('total_supply') if p else None
    sup=maxs if maxs else tots; supsrc=('Höchstmenge' if maxs else 'Gesamtmenge') if sup else None
    pp=p['quotes']['EUR']['price'] if p and p.get('quotes') else None
    pdev=(price/pp-1) if price and pp else None
    fdv=price*sup if price and sup else None
    fees=ann(names,F); rev=ann(names,RV); hold=ann(names,H)
    r=dict(name=assets.get(s),klasse=cltxt,typ=cls,preis=price,preis_pap=pp,pdev=pdev,menge=sup,mengenart=supsrc,fdv=fdv,fees=fees,rev=rev,hold=hold,quellen=names,flag=flag)
    # Kennzahl
    if flag=='IDENT':
        r['ergebnis']='Daten klären'; r['grund']='Identität mehrdeutig: Bitvavo „Frax“ kann den früheren Stablecoin FRAX oder den Governance-Token Frax (vorher FXS) bezeichnen (Q-01)'
    elif flag=='VELO':
        r['ergebnis']='Daten klären'; r['grund']='Identität der Ertragsdaten widersprüchlich: DefiLlama ordnet die Kennung „velo“ dem Protokoll „Velo Finance“ zu, Bitvavo führt Velo (Velo Labs) – bekannter Fehlerfall aus Q-01'
    elif flag=='NODATA':
        r['ergebnis']='Daten klären'; r['grund']='Keine Ertragsdaten bei DefiLlama; Primärquellen der Projekterträge sind einzeln zu prüfen (Grundsatz 7)'
    elif fdv is None:
        r['ergebnis']='Daten klären'; r['grund']='Menge oder Kurs fehlt'
    else:
        th=TH[cls]
        if cls=='Plattform': upper=fees; metric=fees
        elif cls=='DeFi': upper=rev if (rev is not None and rev>0) else fees; metric=hold if (hold is not None and hold>0) else None
        else: upper=fees; metric=rev if rev is not None else fees
        r['mult_upper']=fdv/upper if upper else None
        r['mult_metric']=fdv/metric if metric else None
        r['schwelle']=th
        if upper is None or upper<=0:
            r['ergebnis']='Daten klären'; r['grund']='Ertrag nicht belegt'
        elif fdv/upper>1.25*th:
            r['ergebnis']='scheidet aus (robust)'; r['grund']=f'FDV das {fdv/upper:,.0f}-Fache des großzügigsten Ertragsmaßes; Schwelle {th}, Robustheitsgrenze {1.25*th:,.0f}'
        elif metric and fdv/metric<=th:
            r['ergebnis']='besteht → Erstbewertung'; r['grund']=f'FDV das {fdv/metric:,.0f}-Fache, Schwelle {th}'
        else:
            r['ergebnis']='grenznah → Erstbewertung'; r['grund']=f'zwischen Schwelle und Robustheitsgrenze oder Klassenmaß fehlt'
        if flag in ('etc','xrp','xlm'):
            d,v=mv[flag]; r['mvrv']=v; r['mvrv_datum']=d
            if r['ergebnis'].startswith('scheidet') and v<=5:
                r['ergebnis']='Klassenfrage → Erstbewertung'
                r['grund']+=f'. Als Geldwert wäre der MVRV {v:.2f} ({d}, Coin Metrics) punktfähig; die Klasse ist in der Erstbewertung zu begründen und von der Zweitprüfung blind zu prüfen'
        elif flag=='FRAXID':
            r['grund']+='. Identität: Bitvavo-Kurs weicht nur '+f"{r['pdev']*100:+.1f}".replace('.',',')+' % vom Kurs von „Frax (vorher FXS)“ ab; der frühere Stablecoin hätte rund 0,89 €. Zuordnung damit belegt (Q-01)'
        elif flag:
            r['grund']+='. Hinweis: '+flag
    out[s]=r
json.dump(out,open('/home/claude/work/vp/ergebnis.json','w'),indent=1,ensure_ascii=False)
import collections
print(collections.Counter(r['ergebnis'] for r in out.values()))
for s,r in out.items():
    print(f"{s:6} {r['ergebnis']:30} {r['typ']} FDV {r['fdv'] and round(r['fdv']/1e6,1)} Mio | fees {r['fees'] and round(r['fees'])} rev {r['rev'] and round(r['rev'])} hold {r['hold'] and round(r['hold'])} | multU {r.get('mult_upper') and round(r['mult_upper'])} multM {r.get('mult_metric') and round(r['mult_metric'])} | pdev {r['pdev'] and round(r['pdev']*100,1)}%")
