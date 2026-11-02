import csv, sys, collections, datetime, copy
from decimal import Decimal as D
from openpyxl import load_workbook
from openpyxl.formula.translate import Translator
sys.path.insert(0,'/home/claude/scripts'); from shot import S

SRC='/home/claude/work/AF.xlsx'; OUT='/home/claude/work/out/Krypto-Bewertungsmatrix_Arbeitsfassung_Version_1.2.30.xlsx'
CSV_SHA='722a1598025b44887e9c9af59f85861436ca6c15923c62ae393cf5ef6b0bb919'
STAMP=datetime.datetime(2026,11,2,17,15)
EXPORT_DATE='02.11.2026'
LASTROW=1504

rows=list(csv.DictReader(open('/home/claude/work/export.csv',newline='',encoding='utf-8')))
for i,r in enumerate(rows): r['_i']=i
tx=[r for r in rows if r['Type'] in('buy','sell')]
tx.sort(key=lambda r:(r['Date'],r['Time'].ljust(12,'0'),-r['_i']))
def dt(r):
    t=r['Time']; f='%Y-%m-%d %H:%M:%S.%f' if '.' in t else '%Y-%m-%d %H:%M:%S'
    return datetime.datetime.strptime(r['Date']+' '+t,f)

# FIFO
lots=collections.defaultdict(list); sales=[]
for r in tx:
    c=r['Currency'];a=abs(D(r['Amount']));q=D(r['Quote Price']);f=D(r['Fee amount'])
    if r['Type']=='buy': lots[c].append([dt(r),a,a*q+f])
    else:
        rem=a; cost=D(0); short=False; holds=[]
        while rem>0:
            L=lots[c][0]; take=min(rem,L[1]); part=L[2]*take/L[1]
            cost+=part; holds.append((L[0],take)); L[2]-=part; L[1]-=take; rem-=take
            if L[1]==0: lots[c].pop(0)
        sales.append((dt(r),c,a,D(r['Received / Paid Amount']),cost,holds))
held={c:ls for c,ls in lots.items() if sum(l[1] for l in ls)>0}

wb=load_workbook(SRC)
T=wb['Tranchen']
# 1) capacity: copy row 504 template down to LASTROW
for r in range(505,LASTROW+1):
    T.row_dimensions[r].height=T.row_dimensions[504].height
    for c in range(1,15):
        src=T.cell(504,c); dst=T.cell(r,c)
        dst._style=copy.copy(src._style)
        if isinstance(src.value,str) and src.value.startswith('='):
            dst.value=Translator(src.value,origin=src.coordinate).translate_formula(dst.coordinate)
dv=T.data_validations.dataValidation[0]; dv.sqref=type(dv.sqref)(f'C5:C{LASTROW}')
# 2) rows
assert len(tx)<=LASTROW-4
for k,r in enumerate(tx):
    row=5+k
    T.cell(row,1).value=dt(r)
    T.cell(row,2).value=r['Currency']
    T.cell(row,3).value='Kauf' if r['Type']=='buy' else 'Verkauf'
    T.cell(row,4).value=float(abs(D(r['Amount'])))
    T.cell(row,5).value=float(D(r['Quote Price']))
    T.cell(row,7).value=float(D(r['Fee amount']))
    T.cell(row,8).value='Bitvavo'
    T.cell(row,13).value=STAMP.replace(hour=0,minute=0)
    T.cell(row,14).value=f"Bitvavo-Export {EXPORT_DATE}, Kennung {r['Transaction ID']}"
    if T.cell(row,13).number_format=='General': T.cell(row,13).number_format='dd\\.mm\\.yyyy'
for row in range(5,LASTROW+1): T.cell(row,1).number_format='dd\\.mm\\.yyyy\\ hh:mm:ss'

# 3) Portfolioübersicht
P=wb['Zeitpunkt & Portfolio']
rowof={P.cell(r,1).value:r for r in range(67,116) if P.cell(r,1).value}
assert set(rowof)==set(held)==set(S), (set(rowof)^set(held), set(held)^set(S))
summary={}
for c,r in rowof.items():
    ls=held[c]; qty=sum(l[1] for l in ls); cost=sum(l[2] for l in ls)
    price,val,mq,_=S[c]; assert D(mq)==qty
    P.cell(r,2).value=float(D(val))
    P.cell(r,4).value=datetime.datetime(ls[0][0].year,ls[0][0].month,ls[0][0].day)
    P.cell(r,5).value=float(round(cost,2))
    P.cell(r,14).value=float(D(price))
    P.cell(r,13).value=(f"Bestand {str(qty).replace('.',',')} {c} (Export = Bildschirmfoto). Einstand: FIFO je Wallet, einschließlich Kaufgebühren, aus Bitvavo-Export {EXPORT_DATE}. "
        f"Wert und Kurs: Bitvavo-Bildschirmfoto {EXPORT_DATE}, Uhrzeit nicht im Bild; kein Abruf über /v2/ticker/price (Schnittstelle in dieser Umgebung gesperrt) – nachholen.")
    summary[c]=(r,ls[0][0],qty,cost)
# 4) Protokoll
L=wb['Protokoll']
pr=5
assert all(L.cell(pr,c).value in (None,'') for c in range(1,27))
L.cell(pr,1).value=STAMP
L.cell(pr,2).value='alle Bestände (35)'
L.cell(pr,3).value='Datenübernahme'
L.cell(pr,4).value='Betriebsdokument Erstprüfung C 7; Kanon § 31 Abs. 3; A9a; Q-07'
L.cell(pr,7).value=(f"{len(tx)} Zeilen in „Tranchen“ (5–{4+len(tx)}): {sum(1 for r in tx if r['Type']=='buy')} Käufe, {sum(1 for r in tx if r['Type']=='sell')} Verkäufe; "
    "keine Zugänge ohne Kauf, keine Abgänge ohne Verkauf. Portfolioübersicht Zeilen 67–101 gefüllt (B, D, E, M, N). Gegenprobe: alle 35 Bestände stimmen mit dem Bildschirmfoto exakt überein.")
L.cell(pr,8).value=("Kaufhistorie belegen (A9a) und Werte, Kaufdatum und Einstand für A6, A10 und Haltefristen bereitstellen. Nicht übernommen: 30 Euro-Einzahlungen und 11 Affiliate-Gutschriften in Euro (zusammen 0,98 €), "
    "weil Euro-Bewegungen nach C 7 Nr. 3 keine Tranchen sind. Kurs und Wert aus dem Bildschirmfoto statt aus /v2/ticker/price, weil die Schnittstelle in dieser Umgebung gesperrt war.")
L.cell(pr,15).value=f"Bitvavo-Export vom {EXPORT_DATE} (Zeitraum 01.01.2001 bis 02.11.2026, Zeitzone Europe/Berlin); Bildschirmfoto der Bestände vom {EXPORT_DATE}"
L.cell(pr,32).value=(f"Rohbeleg: CSV-Datei, SHA-256 {CSV_SHA}, 674 Datenzeilen, davon {len(tx)} übernommen; Ablage Krypto-Matrix/Belege/Bitvavo-Export_2026-11-02.csv. "
    "Zusatzbelege: PDF-Fassung desselben Exports (SHA-256 8bb19d9f87e8e28cc8de4dc3f0c6afe9283b19604c4210b9beaf335e24871937; inhaltlich mit der CSV-Datei geprüft, alle 674 Kennungen und Mengen gleich) "
    "und Bildschirmfoto (SHA-256 7e686784c3436a674723ca8dbcfbddf3ead3eb8dabbf8f171d2717358f39da3b), beide ebenfalls nach „Belege“. "
    f"Blatt „Tranchen“ von 500 auf {LASTROW-4} Zeilen erweitert (Formeln F, I–L und Auswahlliste C unverändert nach unten fortgeführt), weil 633 Ausführungen einzeln zu buchen waren; förmlich bei der nächsten Fortschreibung nachziehen (Änderungsprotokoll, Prüffassung).")
wb.save(OUT)

# report
print('rows',len(tx))
for c,(r,d0,q,cost) in sorted(summary.items(),key=lambda x:x[1][0]): print(c,r,d0.date(),q,round(cost,2))
print('SALES')
for s in sales:
    d,c,a,proc,cost,holds=s
    within=[ (h[0].date(),h[1]) for h in holds if (d - h[0]).days < 366 and not (d.date() > h[0].date().replace(year=h[0].year+1))]
    print(d,c,a,proc,round(cost,2),'gain',round(proc-cost,2),'oldest',holds[0][0].date(),'newest',holds[-1][0].date(),'within1y' if within else 'over1y')
