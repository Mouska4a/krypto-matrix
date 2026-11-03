import json,time,urllib.request,hashlib,sys,os
URL='https://xrplcluster.com'
def rpc(m,p):
    for i in range(6):
        try:
            req=urllib.request.Request(URL,data=json.dumps({"method":m,"params":[p]}).encode(),headers={'Content-Type':'application/json'})
            return json.load(urllib.request.urlopen(req,timeout=60))['result']
        except Exception as e:
            print('retry',m,e,file=sys.stderr); time.sleep(3+3*i)
    raise SystemExit('Abruf fehlgeschlagen')
out=sys.argv[1]
L=rpc('ledger',{"ledger_index":"validated"})
li=int(L['ledger']['ledger_index']); ct=L['ledger']['close_time_human']
print('Ledger',li,ct)
objs=[];marker=None;n=0
while True:
    p={"ledger_index":li,"type":"escrow","limit":2048,"binary":False}
    if marker: p['marker']=marker
    r=rpc('ledger_data',p); objs+= [o for o in r['state'] if o.get('LedgerEntryType')=='Escrow']; n+=1
    marker=r.get('marker')
    if n%20==0: print(n,len(objs),file=sys.stderr)
    if not marker: break
json.dump({"ledger_index":li,"close_time_human":ct,"abruf_utc":time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),"quelle":URL+" ledger_data type=escrow","escrows":objs},open(out,'w'))
print('Escrow-Objekte',len(objs),'Seiten',n)
