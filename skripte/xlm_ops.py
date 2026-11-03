import json,time,urllib.request,sys
from collections import Counter
H='https://horizon.stellar.org'
def get(u):
    for i in range(6):
        try: return json.load(urllib.request.urlopen(u,timeout=60))
        except Exception as e: print('retry',e,file=sys.stderr); time.sleep(3+3*i)
    raise SystemExit('fehlgeschlagen '+u)
acc=json.load(open('sdf_konten.json')); START='2025-11-01T00:00:00Z'
out={'quelle':H+' /accounts/{id}/operations','abruf_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'konten':{}}
for a,lab in acc.items():
    u=H+f'/accounts/{a}/operations?order=desc&limit=200'; ops=[]; earliest=None
    while u:
        r=get(u); recs=r['_embedded']['records']; stop=False
        for x in recs:
            if x['created_at']<START: stop=True; break
            ops.append(x); earliest=x['created_at']
        if stop or not recs: break
        u=r['_links']['next']['href']
    c=Counter(x['type'] for x in ops)
    keep=[x for x in ops if x['type'] not in ('payment','create_account','path_payment_strict_send','path_payment_strict_receive','account_merge')]
    out['konten'][a]={'label':lab,'anzahl':len(ops),'typen':dict(c),'frueheste':earliest,'sonstige_ops':keep}
    print(lab,len(ops),dict(c),earliest,file=sys.stderr)
json.dump(out,open('roh/horizon_sdf_operationen_2025-11-02_bis_2026-11-03.json','w'))
print('fertig')
