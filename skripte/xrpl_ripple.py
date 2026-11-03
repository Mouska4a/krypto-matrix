import json,time,urllib.request,sys
URL='https://xrplcluster.com'
def rpc(m,p):
    for i in range(6):
        try:
            req=urllib.request.Request(URL,data=json.dumps({"method":m,"params":[p]}).encode(),headers={'Content-Type':'application/json'})
            return json.load(urllib.request.urlopen(req,timeout=60))['result']
        except Exception as e:
            print('retry',m,e,file=sys.stderr); time.sleep(3+3*i)
    raise SystemExit('Abruf fehlgeschlagen '+m)
wk=json.load(open('roh/xrpscan_names_well-known.json'))
acc=[x['account'] for x in wk if x.get('name')=='Ripple' and 'ripple.com' in (x.get('domain') or '')]
L=rpc('ledger',{"ledger_index":"validated"}); li=int(L['ledger']['ledger_index'])
res={"ledger_index":li,"close_time_human":L['ledger']['close_time_human'],"abruf_utc":time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),"quelle":URL,"konten":{}}
for a in acc:
    ai=rpc('account_info',{"account":a,"ledger_index":li})
    objs=[];m=None
    while True:
        p={"account":a,"ledger_index":li,"type":"escrow","limit":400}
        if m: p['marker']=m
        r=rpc('account_objects',p); objs+=r.get('account_objects',[]); m=r.get('marker')
        if not m: break
    res['konten'][a]={"account_info":ai.get('account_data'),"escrows":objs}
    print(a, int(ai.get('account_data',{}).get('Balance',0))/1e6, len(objs), file=sys.stderr)
json.dump(res,open('roh/xrpl_ripple_konten_escrow.json','w'))
