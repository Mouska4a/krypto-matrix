import json,glob,hashlib,os,datetime
from openpyxl import Workbook
from openpyxl.styles import Font,Alignment,PatternFill
from openpyxl.utils import get_column_letter
R=sorted(glob.glob('/home/claude/work/vp/roh_*'))[-1]
o=json.load(open('/home/claude/work/vp/ergebnis.json'))
de=lambda x,d=0: (f"{x:,.{d}f}".replace(',','X').replace('.',',').replace('X','.')) if x is not None else ''
for s,r in o.items():
    th=r.get('schwelle'); mu=r.get('mult_upper'); mm=r.get('mult_metric')
    maß={'Plattform':'Gesamtgebühren der Kette (Obergrenze der Nettogebühren)','DeFi':'Halter-Erträge; Obergrenze: Erträge','Umsatz':'Erträge; Obergrenze: Gesamtgebühren'}.get(r['typ'],'')
    r['maß']=maß
    if r['ergebnis']=='scheidet aus (robust)':
        r['grund']=f"Voll verwässerte Bewertung das {de(mu)}-Fache der Obergrenze des Ertrags; Punkte erst bis zum {th}-Fachen, robust ausgeschlossen ab dem {de(1.25*th)}-Fachen."
    elif r['ergebnis']=='besteht → Erstbewertung':
        r['grund']=f"Voll verwässerte Bewertung das {de(mm)}-Fache des Ertrags; Schwelle {th}. Mindestbedingung erfüllt; Nettogebühren und alle Noten erst in der Erstbewertung."
    elif r['ergebnis']=='grenznah → Erstbewertung':
        extra=r['grund'].split('. Identität:')[1] if 'Identität:' in r['grund'] else ''
        if mm and mu<=th: r['grund']=f"Großzügigste Obergrenze des Ertrags das {de(mu)}-Fache und damit unter der Schwelle {th}, Klassenmaß das {de(mm)}-Fache darüber. Welcher Ertrag nach D-02 maßgeblich ist, liegt dazwischen und wird in der Erstbewertung bestimmt."
        elif mm: r['grund']=f"Klassenmaß das {de(mm)}-Fache, knapp über der Schwelle {th} und unter der Robustheitsgrenze {de(1.25*th)}; die Näherung lässt kein sicheres Urteil zu."
        else: r['grund']=f"Obergrenze das {de(mu)}-Fache (Schwelle {th}); Halter-Erträge bei DefiLlama null oder nicht ausgewiesen – ob nachweislich null oder nur nicht gemessen, klärt die Erstbewertung (§ 9 Absatz 6)."
        if extra: r['grund']+=' Identität:'+extra
    elif r['ergebnis']=='Klassenfrage → Erstbewertung':
        r['grund']=f"Als Plattform das {de(mu)}-Fache der Gebühren, also weit über 500. Als Geldwert wäre der MVRV {de(r['mvrv'],2)} (Coin Metrics, {datetime.date.fromisoformat(r['mvrv_datum']).strftime('%d.%m.%Y')}) punktfähig. Die Klasse ist in der Erstbewertung nach § 5 zu begründen und von der Zweitprüfung blind zu prüfen."
json.dump(o,open('/home/claude/work/vp/ergebnis.json','w'),indent=1,ensure_ascii=False)
wb=Workbook(); ws=wb.active; ws.title='Vorprüfung Block 1'
hdr=['Kürzel','Name (Bitvavo)','Ergebnis','Begründung','Klassenvorschlag','Kurs Bitvavo (€)','Abweichung zu CoinPaprika','Menge','Mengenart','Voll verwässerte Bewertung (€)','Gebühren 365 Tage (€)','Erträge 365 Tage (€)','Halter-Erträge 365 Tage (€)','Maß','Multiplikator Obergrenze','Multiplikator Klassenmaß','Schwelle','MVRV (Geldwert)','DefiLlama-Einträge','Kennzeichen']
ws.append(['Maschinelle Vorprüfung, Block 1 (52 Coins) – Stand 02.11.2026, Abruf 17:16 Uhr Weltzeit; Prüfvorschrift festgeschrieben 17:20 Uhr Weltzeit, vor der Rechnung'])
ws.append(['Keine Status- oder Notenvergabe. „Scheidet aus (robust)“ heißt: Eine Bewertungsnote über null ist nach der Matrix mit keinem zulässigen Wert erreichbar. Euro-Beträge aus US-Dollar mit dem EZB-Referenzkurs vom 02.11.2026 (1,1216 US-Dollar je Euro).'])
ws.append(hdr)
order={'besteht → Erstbewertung':0,'grenznah → Erstbewertung':1,'Klassenfrage → Erstbewertung':2,'Daten klären':3,'scheidet aus (robust)':4}
rows=sorted(o.items(),key=lambda kv:(order[kv[1]['ergebnis']],kv[0]))
for i,(s,r) in enumerate(rows):
    n=4+i
    ws.append([s,r['name'],r['ergebnis'],r['grund'],r['klasse'],r['preis'],r['pdev'],r['menge'],r['mengenart'],
        f'=IF(OR(F{n}="",H{n}=""),"",F{n}*H{n})',r['fees'],r['rev'],r['hold'],r['maß'],r.get('mult_upper'),r.get('mult_metric'),r.get('schwelle'),r.get('mvrv'),
        ', '.join(r['quellen']),'Kurs: Bitvavo, Herkunft P; Menge: CoinPaprika, Herkunft M/S; Erträge: DefiLlama, Herkunft A; alle einfach belegt (E); Jahreswert als Näherung (365 Tage)'])
fmt={6:'#,##0.000000',7:'0.0%',8:'#,##0',10:'#,##0',11:'#,##0',12:'#,##0',13:'#,##0',15:'#,##0',16:'#,##0',17:'#,##0',18:'0.00'}
for row in ws.iter_rows(min_row=4,max_row=ws.max_row):
    for c in row:
        c.font=Font(name='Arial',size=10); c.alignment=Alignment(vertical='top',wrap_text=c.column in (4,5,14,19,20))
        if c.column in fmt: c.number_format=fmt[c.column]
        if c.column in (1,2,3,5,6,8,9,11,12,13,14,17,18,19,20): c.font=Font(name='Arial',size=10,color='0000FF')
for c in ws[3]: c.font=Font(name='Arial',size=10,bold=True); c.alignment=Alignment(wrap_text=True,vertical='top')
for r_ in (1,2): ws.cell(r_,1).font=Font(name='Arial',size=10,bold=(r_==1))
w={1:9,2:22,3:26,4:70,5:30,6:14,7:11,8:16,9:12,10:16,11:15,12:15,13:15,14:30,15:14,16:14,17:9,18:9,19:30,20:40}
for k,v in w.items(): ws.column_dimensions[get_column_letter(k)].width=v
ws.freeze_panes='B4'
# Prüfvorschrift
ws2=wb.create_sheet('Prüfvorschrift')
for line in open('/home/claude/work/vp/Pruefvorschrift_Vorpruefung_Stufe1_2026-11-02.txt',encoding='utf-8').read().split('\n'):
    ws2.append([line]); ws2.cell(ws2.max_row,1).font=Font(name='Arial',size=10); ws2.cell(ws2.max_row,1).alignment=Alignment(wrap_text=True)
ws2.column_dimensions['A'].width=140
ws3=wb.create_sheet('Rohbelege')
ws3.append(['Datei','SHA-256','Größe (Byte)']); [c.__setattr__('font',Font(name='Arial',size=10,bold=True)) for c in ws3[1]]
for f in sorted(glob.glob(R+'/**/*',recursive=True)):
    if os.path.isfile(f):
        h=hashlib.sha256(open(f,'rb').read()).hexdigest()
        ws3.append([os.path.relpath(f,os.path.dirname(R)),h,os.path.getsize(f)])
for row in ws3.iter_rows(min_row=2):
    for c in row: c.font=Font(name='Arial',size=10)
ws3.column_dimensions['A'].width=70; ws3.column_dimensions['B'].width=70
os.makedirs('/home/claude/work/vp/out',exist_ok=True)
wb.save('/home/claude/work/vp/out/Vorpruefung_Block1_2026-11-02.xlsx'); print('ok')
