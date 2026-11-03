import json,datetime as dt,sys
RE=dt.datetime(2000,1,1)
d=json.load(open('roh/xrpl_ripple_escrow_tx_2025-11-01_bis_2026-11-03.json'))
seen=set(); rows=[]; skipped=0
for t in d['tx']:
    tx=t['tx']; h=tx.get('hash') or t.get('hash')
    if h in seen: continue
    seen.add(h)
    if t['meta_result']!='tesSUCCESS': continue
    date=RE+dt.timedelta(seconds=t['date'] or tx.get('date'))
    typ=tx['TransactionType']; amt=None; fa=None
    if typ=='EscrowCreate':
        a=tx.get('Amount')
        if not isinstance(a,str): skipped+=1; continue
        amt=int(a)/1e6; fa=RE+dt.timedelta(seconds=tx['FinishAfter']) if 'FinishAfter' in tx else None
    else:
        for n in t['meta']['AffectedNodes']:
            x=n.get('DeletedNode')
            if x and x['LedgerEntryType']=='Escrow':
                a=x['FinalFields']['Amount']
                if isinstance(a,str): amt=int(a)/1e6; fa=RE+dt.timedelta(seconds=x['FinalFields'].get('FinishAfter',0))
        if amt is None: skipped+=1; continue
    rows.append((date,typ,amt,tx['Account'],tx.get('Destination') or tx.get('Owner'),fa,h))
rows.sort()
fin=[r for r in rows if r[1]=='EscrowFinish']; cre=[r for r in rows if r[1]=='EscrowCreate']; can=[r for r in rows if r[1]=='EscrowCancel']
print('übersprungen (kein XRP):',skipped)
print('Freigaben (EscrowFinish):',len(fin),'Summe XRP',round(sum(r[2] for r in fin)))
print('Neue Sperren (EscrowCreate):',len(cre),'Summe XRP',round(sum(r[2] for r in cre)))
lang=sum(r[2] for r in cre if r[5] and (r[5]-r[0]).days>=365)
print('davon Laufzeit mindestens zwölf Monate:',round(lang))
print('Abbrüche (EscrowCancel):',len(can))
F=sum(r[2] for r in fin)
print('Absorptionsquote (neue Sperren >= 12 Monate / Freigaben): %.1f %%'%(100*lang/F))
from collections import defaultdict
m=defaultdict(lambda:[0,0])
for r in fin: m[r[0].strftime('%Y-%m')][0]+=r[2]
for r in cre: m[r[0].strftime('%Y-%m')][1]+=r[2]
for k in sorted(m): print(k,'frei %5.0f Mio'%(m[k][0]/1e6),'neu gesperrt %5.0f Mio'%(m[k][1]/1e6))
print('Laufzeiten neuer Sperren in Monaten:',sorted(set(round((r[5]-r[0]).days/30.44) for r in cre if r[5])))
print('Konten Freigabe:',sorted(set(r[3] for r in fin))); print('Konten Sperre:',sorted(set(r[3] for r in cre)))
print('fremde Ziele bei Sperren:',[(r[0].date(),r[2],r[4]) for r in cre if r[4]!=r[3]][:5])
print('Zeitraum:',rows[0][0],'bis',rows[-1][0])
