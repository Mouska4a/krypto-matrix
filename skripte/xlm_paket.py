import json,hashlib,shutil,os,re
from collections import defaultdict
def de(x,dec=0):
    s=f"{x:,.{dec}f}"; return s.replace(',','X').replace('.',',').replace('X','.')
SRC='/home/claude/work/eb3/Datenpakete/Datenpaket_XLM_2026-11-02'
DST='/home/claude/work/xlm/Datenpaket_XLM_2026-11-03'
shutil.rmtree(DST,ignore_errors=True); shutil.copytree(SRC,DST); os.remove(DST+'/Datenpaket_XLM_2026-11-02.txt')
new={'roh/horizon_sdf_konten_2025-11-01_bis_2026-11-03.json':'horizon_sdf_konten_zahlungen_2025-11-02_bis_2026-11-03.json',
     'roh/horizon_void_account.json':'horizon_konto_GALAXYVOID_2026-11-03.json',
     'roh/stellar_org_foundation_mandate_2026-11-03.html':'stellar_org_foundation_mandate_2026-11-03.html',
     'roh/coinmetrics_xlm_CapRealUSD_nicht_verfuegbar.json':'coinmetrics_xlm_CapRealUSD_nicht_verfuegbar.json'}
for s,n in new.items(): shutil.copy(s,DST+'/'+n)
d=json.load(open('roh/horizon_sdf_konten_2025-11-01_bis_2026-11-03.json'))
SDF=set(d['konten']); L=d['ledger']
void=json.load(open('roh/horizon_void_account.json'))
vb=float([b['balance'] for b in void['balances'] if b['asset_type']=='native'][0])
bal={a:float([b['balance'] for b in v['account']['balances'] if b['asset_type']=='native'][0]) for a,v in d['konten'].items()}
seen=set(); out=0; inn=0; intern=0; mon=defaultdict(lambda:[0.0,0.0]); n_ops=0
def moves(x):
    t=x['type']
    if t=='payment' and x.get('asset_type')=='native': return [(x['from'],x['to'],float(x['amount']))]
    if t=='create_account': return [(x['funder'],x['account'],float(x['starting_balance']))]
    if t.startswith('path_payment'):
        r=[]
        if x.get('asset_type')=='native': r.append((None,x['to'],float(x['amount'])))
        if x.get('source_asset_type')=='native': r.append((x['from'],None,float(x['source_amount'])))
        return r
    if t=='invoke_host_function': return [(c.get('from'),c.get('to'),float(c['amount'])) for c in x.get('asset_balance_changes') or [] if c.get('asset_type')=='native']
    return []
merges=0
for a,v in d['konten'].items():
    for x in v['payments']:
        if x['id'] in seen: continue
        seen.add(x['id']); n_ops+=1
        if x['type']=='account_merge': merges+=1
        for f,t,amt in moves(x):
            fs=f in SDF; ts=t in SDF; m=x['created_at'][:7]
            if fs and ts: intern+=amt
            elif fs: out+=amt; mon[m][0]+=amt
            elif ts: inn+=amt; mon[m][1]+=amt
monl='; '.join(f"{k[5:7]}.{k[:4]}: an andere Konten {de(v[0]/1e6,1)} Mio., von anderen Konten {de(v[1]/1e6,1)} Mio." for k,v in sorted(mon.items()))
konten='; '.join(f"{v['label']} {a}: {de(bal[a]/1e6,1)} Mio." for a,v in d['konten'].items())
old=open(SRC+'/Datenpaket_XLM_2026-11-02.txt',encoding='utf-8').read()
head,files=old.split('DATENPAKET XLM FÜR DIE ZWEITPRÜFUNG\n',1)[1].split('DATEIEN UND PRÜFSUMMEN (SHA-256)\n')
head=head.replace('die Daten wurden unverändert übernommen','die Daten vom 02.11.2026 wurden unverändert übernommen').replace('Eingefrorener Datenstand vom 02.11.2026, Abrufe 22:25 bis 22:45 Uhr Weltzeit (Gebührenübersicht DefiLlama: 17:16 Uhr Weltzeit).',
 'Eingefrorener Datenstand: Markt-, Mengen- und Kennzahldaten vom 02.11.2026, Abrufe 22:25 bis 22:45 Uhr Weltzeit (Gebührenübersicht DefiLlama: 17:16 Uhr Weltzeit); Blockchain-Prüfung vom 03.11.2026, 21:43 bis 21:50 Uhr Weltzeit (Abschnitt BLOCKCHAIN-PRÜFUNG). Dieses Paket ersetzt „Datenpaket_XLM_2026-11-02.zip“ vollständig.')
chain=f"""BLOCKCHAIN-PRÜFUNG (Stellar-Netz, öffentliche Schnittstelle Horizon https://horizon.stellar.org, Abruf 03.11.2026; P/V, eigene Abfrage, wiederholbar)
Ledger {L['sequence']}, geschlossen {L['closed_at']}: total_coins {de(float(L['total_coins']),2)} XLM; fee_pool {de(float(L['fee_pool']),2)} XLM.
Konto GALAXYVOIDAOPZTDLHILAJQKCVVFMD4IKLXLSZV5YHO7VY74IWZILUTO: Guthaben {de(vb,2)} XLM; einziger Unterzeichner ist der Hauptschlüssel mit Gewicht 0, alle Schwellen 0 (Datei horizon_konto_GALAXYVOID_2026-11-03.json). total_coins minus dieses Guthaben: {de(float(L['total_coins'])-vb,2)} XLM.
Konten der Stellar-Stiftung: Die Stiftung veröffentlicht auf https://stellar.org/foundation/mandate 13 Konten mit Bezeichnung (Datei stellar_org_foundation_mandate_2026-11-03.html; vom Projekt selbst veröffentlicht, Q-11). Die Seite vermerkt, die Aufteilung werde derzeit neu geordnet und die laufenden Guthaben würden „in Kürze“ wieder angezeigt. Guthaben in XLM am 03.11.2026: {konten} Summe: {de(sum(bal.values())/1e6,1)} Millionen XLM.
Zahlungsverkehr dieser 13 Konten in XLM (Zahlungen, Kontoeröffnungen, Pfadzahlungen, Vertragsaufrufe), {n_ops} Vorgänge vom 02.11.2025, 14:18 Uhr Weltzeit, bis 03.11.2026; ein früherer Verlauf wird von dieser Schnittstelle nicht mehr vorgehalten, der 01.11.2025 fehlt daher. Übertragungen zwischen den 13 Konten: {de(intern/1e6,1)} Mio. An Konten außerhalb der 13 Konten: {de(out/1e6,1)} Mio. Von Konten außerhalb: {de(inn/1e6,1)} Mio. Je Kalendermonat: {monl} Kontozusammenlegungen (account_merge): {merges}, ohne Betragsangabe. Nicht erfasst: Guthaben, die über beanspruchbare Salden (claimable balances) oder Liquiditätspools bewegt wurden, und Konten der Stiftung, die nicht auf der Seite stehen. Ob die Empfänger Dritte oder weitere Konten der Stiftung sind, ist aus den Daten nicht erkennbar.
Hinweis: Der Abgleich mit dem Dashboard der Stiftung (sdfMandate {de(14472680436.733994/1e6,1)} Mio. am 02.11.2026) ergibt eine Differenz von {de((14472680436.733994-sum(bal.values()))/1e6,1)} Mio. XLM zur Summe der 13 Konten.
Coin Metrics: Der realisierte Marktwert (CapRealUSD), aus dem sich das MVRV ohne die Coins auf dem Konto GALAXYVOID nachrechnen ließe, ist in der kostenfreien Schnittstelle nicht verfügbar (Fehlermeldung archiviert); eine Bereinigung des MVRV ist ohne Annahme über die Berechnungsweise des Anbieters nicht möglich.

"""
sums=[]
for fn in sorted(os.listdir(DST)):
    sums.append(f"{fn}: {hashlib.sha256(open(DST+'/'+fn,'rb').read()).hexdigest()}")
txt='DATENPAKET XLM FÜR DIE ZWEITPRÜFUNG\n'+head+chain+'DATEIEN UND PRÜFSUMMEN (SHA-256)\n'+'\n'.join(sums)+'\n'
open(DST+'/Datenpaket_XLM_2026-11-03.txt','w',encoding='utf-8').write(txt)
print(txt)
