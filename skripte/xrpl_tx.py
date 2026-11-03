import json,time,urllib.request,sys
URL='https://xrplcluster.com'
def rpc(m,p):
    for i in range(6):
        try:
            req=urllib.request.Request(URL,data=json.dumps({"method":m,"params":[p]}).encode(),headers={'Content-Type':'application/json'})
            r=json.load(urllib.request.urlopen(req,timeout=90))['result']
            if r.get('status')=='error' and r.get('error') in ('slowDown','tooBusy'): raise Exception(r['error'])
            return r
        except Exception as e:
            print('retry',m,e,file=sys.stderr); time.sleep(3+3*i)
    raise SystemExit('Abruf fehlgeschlagen '+m)
RE=946684800
# Ledger zum 01.11.2025 00:00 UTC per Bisektion
target=int(time.mktime(time.strptime('2025-11-01','%Y-%m-%d')))-time.timezone
def ct(li): return rpc('ledger',{"ledger_index":li})['ledger']['close_time']+RE
lo,hi=95000000,108096366
while hi-lo>1:
    mid=(lo+hi)//2
    if ct(mid)<target: lo=mid
    else: hi=mid
start=hi; print('Startledger',start,time.strftime('%Y-%m-%d %H:%M:%S',time.gmtime(ct(start))),file=sys.stderr)
d=json.load(open('roh/xrpl_ripple_konten_escrow.json')); end=d['ledger_index']
acc=list(d['konten'].keys())
out={"start_ledger":start,"end_ledger":end,"quelle":URL+" account_tx","abruf_utc":time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),"tx":[]}
for a in acc:
    m=None;k=0;keep=0
    while True:
        p={"account":a,"ledger_index_min":start,"ledger_index_max":end,"limit":400,"forward":True}
        if m: p['marker']=m
        r=rpc('account_tx',p)
        for t in r.get('transactions',[]):
            tx=t.get('tx') or t.get('tx_json'); 
            if tx and tx.get('TransactionType') in ('EscrowCreate','EscrowFinish','EscrowCancel'):
                out['tx'].append({"konto":a,"tx":tx,"meta_result":t['meta'].get('TransactionResult'),"meta":t['meta'],"ledger":t.get('ledger_index') or tx.get('ledger_index'),"date":(tx.get('date') or t.get('date'))}); keep+=1
        k+=len(r.get('transactions',[])); m=r.get('marker')
        if not m or k>40000: break
    print(a,k,keep,'ABGEBROCHEN' if m else '',file=sys.stderr)
json.dump(out,open('roh/xrpl_ripple_escrow_tx_2025-11-01_bis_2026-11-03.json','w'))
print('fertig',len(out['tx']))
