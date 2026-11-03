import json
from collections import Counter,defaultdict
d=json.load(open('roh/horizon_sdf_konten_2025-11-01_bis_2026-11-03.json'))
SDF=set(d['konten'])
types=Counter(); out_ext=0; in_ext=0; intern=0; seen=set(); earliest={}
monthly=defaultdict(lambda:[0.0,0.0]); bigout=[]; other_assets=Counter()
def native_moves(x):
    t=x['type']
    if t=='payment' and x.get('asset_type')=='native': return [(x['from'],x['to'],float(x['amount']))]
    if t=='create_account': return [(x['funder'],x['account'],float(x['starting_balance']))]
    if t=='account_merge': return [(x['account'],x['into'],None)]
    if t.startswith('path_payment'):
        r=[]
        if x.get('asset_type')=='native': r.append((None,x['to'],float(x['amount'])))
        if x.get('source_asset_type')=='native': r.append((x['from'],None,float(x['source_amount'])))
        return r
    if t=='invoke_host_function':
        return [(c.get('from'),c.get('to'),float(c['amount'])) for c in x.get('asset_balance_changes') or [] if c.get('asset_type')=='native']
    return []
for a,v in d['konten'].items():
    ts=[x['created_at'] for x in v['payments']]; earliest[v['label']]=(min(ts) if ts else None,len(ts))
    for x in v['payments']:
        if x['id'] in seen: continue
        seen.add(x['id']); types[x['type']]+=1
        if x['type']=='payment' and x.get('asset_type')!='native': other_assets[x.get('asset_code')]+=1
        for f,t,amt in native_moves(x):
            if amt is None: types['merge_ohne_betrag']+=1; continue
            fs=f in SDF; tsd=t in SDF; m=x['created_at'][:7]
            if fs and tsd: intern+=amt
            elif fs and not tsd: out_ext+=amt; monthly[m][0]+=amt; bigout.append((amt,x['created_at'][:10],t,x['type']))
            elif tsd and not fs: in_ext+=amt; monthly[m][1]+=amt
print('Typen',types); print('andere Werte',other_assets.most_common(5))
print('frühester Eintrag je Konto',earliest)
print('Abfluss an Dritte %.0f  Zufluss von Dritten %.0f  intern %.0f'%(out_ext,in_ext,intern))
for k in sorted(monthly): print(k,'ab %.1f Mio'%(monthly[k][0]/1e6),'zu %.1f Mio'%(monthly[k][1]/1e6))
bigout.sort(reverse=True); print('größte Abflüsse',[(round(a/1e6,1),dd,t[:8],ty) for a,dd,t,ty in bigout[:12]])
bal={v['label']:float([b['balance'] for b in v['account']['balances'] if b['asset_type']=='native'][0]) for a,v in d['konten'].items()}
print(bal); print('Summe SDF %.1f Mio'%(sum(bal.values())/1e6))
L=d['ledger']; print('total_coins',L['total_coins'],'void',[b['balance'] for b in d['void']['balances'] if b['asset_type']=='native'])
