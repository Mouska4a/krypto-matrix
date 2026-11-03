import json,datetime as dt,hashlib,os,shutil
from collections import defaultdict
RE=dt.datetime(2000,1,1)
def de(x,dec=0):
    s=f"{x:,.{dec}f}"; return s.replace(',','X').replace('.',',').replace('X','.')
d=json.load(open('roh/xrpl_ripple_konten_escrow.json'))
L=json.load(open('roh/xrpl_ledger_108096366.json'))['result']['ledger']
rows=[(RE+dt.timedelta(seconds=e['FinishAfter']),int(e['Amount'])/1e6,a) for a,v in d['konten'].items() for e in v['escrows']]
assert all(e['Destination']==a and 'Condition' not in e and 'CancelAfter' not in e for a,v in d['konten'].items() for e in v['escrows'])
m=defaultdict(float)
for fa,amt,a in rows: m[fa.date()]+=amt
sched='; '.join(f"{k.strftime('%d.%m.%Y')}: {de(v/1e6)} Mio." for k,v in sorted(m.items()))
t=json.load(open('roh/xrpl_ripple_escrow_tx_2025-11-01_bis_2026-11-03.json'))
fin=defaultdict(float);cre=defaultdict(float);dur=defaultdict(list);ncan=0;nfin=ncre=0
for x in t['tx']:
    tx=x['tx']
    if x['meta_result']!='tesSUCCESS': continue
    date=RE+dt.timedelta(seconds=x['date'] or tx['date']); k=(date.year,date.month)
    if tx['TransactionType']=='EscrowCreate' and isinstance(tx['Amount'],str):
        cre[k]+=int(tx['Amount'])/1e6; ncre+=1; dur[k].append(round(((RE+dt.timedelta(seconds=tx['FinishAfter']))-date).days/30.44))
    elif tx['TransactionType'] in ('EscrowFinish','EscrowCancel'):
        for n in x['meta']['AffectedNodes']:
            y=n.get('DeletedNode')
            if y and y['LedgerEntryType']=='Escrow' and isinstance(y['FinalFields']['Amount'],str):
                if tx['TransactionType']=='EscrowFinish': fin[k]+=int(y['FinalFields']['Amount'])/1e6; nfin+=1
                else: ncan+=1
keys=sorted(set(fin)|set(cre))
txl='; '.join(f"{k[1]:02d}.{k[0]}: freigegeben {de(fin[k]/1e6)} Mio., neu gesperrt {de(cre[k]/1e6)} Mio. (Laufzeit {min(dur[k])} bis {max(dur[k])} Monate)" for k in keys)
big=sorted(((int(v['account_info']['Balance'])/1e6,a) for a,v in d['konten'].items() if v['account_info']),reverse=True)
freisum=sum(b for b,a in big)
os.makedirs('paket',exist_ok=True)
files={'roh/xrpl_ledger_108096366.json':'xrpl_ledger_108096366.json','roh/xrpl_ripple_konten_escrow.json':'xrpl_konten_escrow_ledger_108096366.json','roh/xrpl_ripple_escrow_tx_2025-11-01_bis_2026-11-03.json':'xrpl_escrow_transaktionen_2025-11-01_bis_2026-11-03.json','roh/xrpscan_names_well-known.json':'xrpscan_names_well-known_2026-11-03.json'}
sums=[]
for s,n in files.items():
    shutil.copy(s,'paket/'+n); sums.append(f"{n}: {hashlib.sha256(open(s,'rb').read()).hexdigest()}")
txt=f"""NACHTRAG ZUM DATENPAKET XRP FÜR DIE ZWEITPRÜFUNG
Ergänzt das Datenpaket „Datenpaket_XRP_2026-11-02.zip“ (Stichtag 02.11.2026) um Primärdaten aus dem XRP Ledger. Abruf am 03.11.2026 zwischen 21:24 und 21:40 Uhr Weltzeit über die öffentliche Schnittstelle https://xrplcluster.com (rippled Version 3.4.1); Ledger-Stand {L['ledger_index']}, Schlusszeit 03.11.2026, 21:24:22 Uhr Weltzeit. Für die Prüfung gilt Regelwerk Version 1.2.31.
Inhalt: nur Rohwerte und daraus summierte Mengen mit Quelle und Kennzeichen (Herkunft / Prüfstatus / Wertstatus nach Teil D der Datenquellen-Verfassung). Keine Klasse, keine Noten, kein Gate, kein Status. Jeder Wert lässt sich mit denselben Abfragen (ledger, account_info, account_objects mit type escrow, account_tx) an jedem öffentlichen Server des XRP Ledger wiederholen.

1. GESAMTMENGE
Feld total_coins des Ledgers {L['ledger_index']}: {de(int(L['total_coins'])/1e6,2)} XRP (P/V, eigene Abfrage).

2. ZUORDNUNG DER KONTEN
Abgefragt wurden die {len(d['konten'])} Konten, die der Blockchain-Explorer XRPSCAN in seiner Liste bekannter Konten unter dem Namen „Ripple“ mit der Adresse ripple.com führt (Datei xrpscan_names_well-known_2026-11-03.json). Diese Zuordnung stammt von einem Analyseanbieter und ist nach Q-11 nur ein Hinweis (S/E); auf dem Ledger selbst tragen die Konten kein Domain-Feld. Die Mengen und Fristen der Treuhandverträge sind dagegen Primärdaten des Ledgers, gleich wem die Konten gehören.

3. TREUHANDVERTRÄGE (ESCROW) DIESER KONTEN, STAND LEDGER {L['ledger_index']} (P/V)
{len(rows)} Treuhandverträge in XRP, zusammen {de(sum(r[1] for r in rows)/1e6,1)} Millionen XRP, auf 8 Konten. Bei allen ist der Empfänger zugleich der Eigentümer (Feld Destination gleich Account); keiner hat eine Bedingung (Condition) oder eine Verfallsfrist (CancelAfter). Frühester Freigabezeitpunkt (FinishAfter), zusammengefasst je Datum: {sched}

4. FREIGABEN UND NEUE TREUHANDVERTRÄGE IN XRP VOM 01.11.2025 BIS 03.11.2026 (P/V)
Ausgewertet sind alle erfolgreichen Transaktionen der Typen EscrowFinish, EscrowCreate und EscrowCancel dieser {len(d['konten'])} Konten zwischen Ledger {t['start_ledger']} (01.11.2025, 00:00 Uhr Weltzeit) und Ledger {t['end_ledger']}: {nfin} Freigaben und {ncre} neue Treuhandverträge in XRP. Je Kalendermonat: {txl}. Abgebrochene Treuhandverträge in XRP (EscrowCancel): {ncan}. Laufzeit meint den Abstand zwischen Erstellung und frühestem Freigabezeitpunkt. Die Rohdatei enthält daneben Treuhandverträge in anderen Werten als XRP; sie sind hier nicht mitgezählt.

5. FREIE GUTHABEN DIESER KONTEN, STAND LEDGER {L['ledger_index']}
Summe der freien XRP-Guthaben (Feld Balance) aller {len(d['konten'])} Konten: {de(freisum/1e6,1)} Millionen XRP (Menge P/V, Zuordnung S/E). Größte Einzelguthaben: {'; '.join(f'{a}: {de(b/1e6,1)} Mio.' for b,a in big[:8])}

6. HINWEISE
Die Gebührenangabe im Datenpaket vom 02.11.2026 bezieht sich auf rollierende 365 Tage, nicht auf die letzten zwölf abgeschlossenen Kalendermonate nach D-03; eine Monatsreihe liegt nicht bei.
Nicht abgefragt: die zehn größten Adressen ohne Börsen insgesamt sowie die empfohlene Liste der Validatoren und deren Betreiber.

DATEIEN UND PRÜFSUMMEN (SHA-256)
""" + '\n'.join(sums) + '\n'
open('paket/Nachtrag_Datenpaket_XRP_2026-11-03.txt','w',encoding='utf-8').write(txt)
print(txt)
