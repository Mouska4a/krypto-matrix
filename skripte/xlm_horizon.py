import json,time,urllib.request,sys
H='https://horizon.stellar.org'
def get(u):
    for i in range(6):
        try: return json.load(urllib.request.urlopen(u,timeout=60))
        except urllib.error.HTTPError as e:
            if e.code==404: return None
            print('retry',u,e,file=sys.stderr); time.sleep(3+3*i)
        except Exception as e: print('retry',u,e,file=sys.stderr); time.sleep(3+3*i)
    raise SystemExit('Abruf fehlgeschlagen '+u)
acc=json.load(open('sdf_konten.json'))
VOID='GALAXYVOIDAOPZTDLHILAJQKCVVFMD4IKLXLSZV5YHO7VY74IWZILUTO'
led=get(H+'/ledgers?order=desc&limit=1')['_embedded']['records'][0]
out={'quelle':H,'abruf_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'ledger':led,'konten':{},'void':get(H+'/accounts/'+VOID)}
START='2025-11-01T00:00:00Z'
for a,lab in acc.items():
    info=get(H+'/accounts/'+a)
    rec={'label':lab,'account':info,'payments':[],'trades':[]}
    for kind in ('payments','trades'):
        u=H+f'/accounts/{a}/{kind}?order=desc&limit=200'
        n=0
        while u:
            r=get(u); recs=r['_embedded']['records']
            stop=False
            for x in recs:
                ts=x.get('created_at') or x.get('ledger_close_time')
                if ts<START: stop=True; break
                rec[kind].append(x)
            n+=len(recs)
            if stop or not recs or n>60000: break
            u=r['_links']['next']['href']
        print(lab,kind,len(rec[kind]),'ABBRUCH' if n>60000 else '',file=sys.stderr)
    out['konten'][a]=rec
json.dump(out,open('roh/horizon_sdf_konten_2025-11-01_bis_2026-11-03.json','w'))
print('fertig',led['sequence'],led['closed_at'])
