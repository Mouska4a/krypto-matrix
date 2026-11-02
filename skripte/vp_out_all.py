import json,glob,hashlib,os,datetime,collections
from openpyxl import Workbook
from openpyxl.styles import Font,Alignment
from openpyxl.utils import get_column_letter
R=sorted(glob.glob('/home/claude/work/vp/roh_*'))[-1]
o1=json.load(open('/home/claude/work/vp/ergebnis.json')); o2=json.load(open('/home/claude/work/vp/ergebnis2.json'))
de=lambda x,d=0: (f"{x:,.{d}f}".replace(',','X').replace('.',',').replace('X','.')) if x is not None else ''
rest=sorted(o2); blocks={s:1 for s in o1}
for i,s in enumerate(rest): blocks[s]=2+i//52
for s,r in o2.items():
    th=r.get('schwelle'); mu=r.get('mult_upper'); mm=r.get('mult_metric'); pre=r.get('grund') or ''
    r['maß']={'Plattform':'Gesamtgebühren der Kette (Obergrenze der Nettogebühren)','DeFi':'Halter-Erträge; Obergrenze: Erträge','Umsatz':'Erträge; Obergrenze: Gesamtgebühren','offen':'Klasse offen; großzügigstes Maß, Schwelle 400'}.get(r.get('typ'),'')
    if r['ergebnis']=='scheidet aus (robust)':
        r['grund']=pre+f"Voll verwässerte Bewertung das {de(mu)}-Fache der Obergrenze des Ertrags; Punkte erst bis zum {th}-Fachen, robust ausgeschlossen ab dem {de(1.25*th)}-Fachen."
    elif r['ergebnis']=='besteht → Erstbewertung':
        r['grund']=pre+f"Voll verwässerte Bewertung das {de(mm)}-Fache des Ertrags; Schwelle {th}. Mindestbedingung erfüllt; Nettogebühren und alle Noten erst in der Erstbewertung."
    elif r['ergebnis']=='grenznah → Erstbewertung':
        if r.get('typ')=='offen': g=f"Klasse nach der Kategorie bei DefiLlama offen; selbst mit der großzügigsten Schwelle nicht auszuschließen (das {de(mu)}-Fache des Ertrags). Klasse und maßgeblicher Ertrag werden in der Erstbewertung bestimmt."
        elif mm and mu<=th: g=f"Großzügigste Obergrenze des Ertrags das {de(mu)}-Fache und damit unter der Schwelle {th}, Klassenmaß das {de(mm)}-Fache darüber. Welcher Ertrag nach D-02 maßgeblich ist, wird in der Erstbewertung bestimmt."
        elif mm: g=f"Klassenmaß das {de(mm)}-Fache, knapp über der Schwelle {th}; die Näherung lässt kein sicheres Urteil zu."
        else: g=f"Obergrenze das {de(mu)}-Fache (Schwelle {th}); Halter-Erträge bei DefiLlama null oder nicht ausgewiesen – ob nachweislich null oder nur nicht gemessen, klärt die Erstbewertung (§ 9 Absatz 6)."
        r['grund']=pre+g
    elif r['ergebnis']=='Klassenfrage → Erstbewertung':
        r['grund']=pre.replace('2026-11-01','01.11.2026') if pre else ''
ALL={**o1,**o2}
wb=Workbook(); ws=wb.active; ws.title='Vorprüfung gesamt'
ws.append(['Maschinelle Vorprüfung des Bitvavo-Universums, Blöcke 1 bis 5 (260 Coins) – Datenstand 02.11.2026, Abruf 17:16 Uhr Weltzeit; Prüfvorschrift festgeschrieben 17:20 Uhr Weltzeit, Nachtrag für die Blöcke 2 bis 5 um 17:45 Uhr Weltzeit, jeweils vor der Rechnung'])
ws.append(['Keine Status- oder Notenvergabe. „Scheidet aus (robust)“: Eine Bewertungsnote über null ist mit keinem zulässigen Wert erreichbar. „Keine Ertragsdaten bei DefiLlama“: vorläufig; ohne belegten Ertrag aus anderer Quelle bliebe die Bewertungsnote leer und der Status höchstens „Bewertung ausstehend“. Mehrere bekannte Protokolle mit echten Erträgen stehen hier, weil DefiLlama sie nicht erfasst; sie werden nacherhoben. Euro-Beträge aus US-Dollar mit dem EZB-Referenzkurs vom 02.11.2026 (1,1216).'])
hdr=['Block','Kürzel','Name (Bitvavo)','Ergebnis','Begründung','Klassenvorschlag','Kurs Bitvavo (€)','Abweichung zu CoinPaprika','Menge','Mengenart','Voll verwässerte Bewertung (€)','Gebühren 365 Tage (€)','Erträge 365 Tage (€)','Halter-Erträge 365 Tage (€)','Maß','Multiplikator Obergrenze','Multiplikator Klassenmaß','Schwelle','MVRV (Geldwert)','DefiLlama-Einträge']
ws.append(hdr)
order={'besteht → Erstbewertung':0,'grenznah → Erstbewertung':1,'Klassenfrage → Erstbewertung':2,'weiter zur Erstbewertung (Nacherhebung)':2.5,'Daten klären':3,'scheidet aus (robust)':4,'keine Ertragsdaten bei DefiLlama (vorläufig)':5}
rows=sorted(ALL.items(),key=lambda kv:(order[kv[1]['ergebnis']],kv[0]))
for i,(s,r) in enumerate(rows):
    n=4+i
    q=r['quellen']; q=', '.join(q) if isinstance(q,list) else q
    ws.append([blocks[s],s,r['name'],r['ergebnis'],r.get('grund',''),r.get('klasse',''),r.get('preis'),r.get('pdev'),r.get('menge'),r.get('mengenart'),
        f'=IF(OR(G{n}="",I{n}=""),"",G{n}*I{n})',r.get('fees'),r.get('rev'),r.get('hold'),r.get('maß',''),r.get('mult_upper'),r.get('mult_metric'),r.get('schwelle'),r.get('mvrv'),q])
fmt={7:'#,##0.000000',8:'0.0%',9:'#,##0',11:'#,##0',12:'#,##0',13:'#,##0',14:'#,##0',16:'#,##0',17:'#,##0',18:'#,##0',19:'0.00'}
for row in ws.iter_rows(min_row=4,max_row=ws.max_row):
    for c in row:
        c.font=Font(name='Arial',size=10,color=None if c.column==11 else '0000FF'); c.alignment=Alignment(vertical='top',wrap_text=c.column in (5,6,15,20))
        if c.column in fmt: c.number_format=fmt[c.column]
for c in ws[3]: c.font=Font(name='Arial',size=10,bold=True); c.alignment=Alignment(wrap_text=True,vertical='top')
for r_ in (1,2): ws.cell(r_,1).font=Font(name='Arial',size=10,bold=(r_==1))
for k,v in {1:6,2:9,3:22,4:26,5:70,6:28,7:14,8:11,9:16,10:12,11:16,12:15,13:15,14:15,15:28,16:14,17:14,18:9,19:9,20:34}.items(): ws.column_dimensions[get_column_letter(k)].width=v
ws.freeze_panes='C4'; ws.auto_filter.ref=f"A3:T{ws.max_row}"
# Übersicht
w2=wb.create_sheet('Übersicht')
cnt=collections.Counter((blocks[s],r['ergebnis']) for s,r in ALL.items())
w2.append(['Ergebnis']+[f'Block {b}' for b in range(1,6)]+['Gesamt'])
for e in order:
    w2.append([e]+[cnt[(b,e)] for b in range(1,6)]+[f'=SUM(B{w2.max_row+1}:F{w2.max_row+1})'])
last=w2.max_row
w2.append(['Summe']+[f'=SUM({get_column_letter(c)}2:{get_column_letter(c)}{last})' for c in range(2,8)])
for row in w2.iter_rows():
    for c in row: c.font=Font(name='Arial',size=10,bold=(c.row in (1,w2.max_row)))
w2.column_dimensions['A'].width=32
ws3=wb.create_sheet('Prüfvorschrift')
for line in open('/home/claude/work/vp/Pruefvorschrift_Vorpruefung_Stufe1_2026-11-02.txt',encoding='utf-8').read().split('\n'):
    ws3.append([line]); ws3.cell(ws3.max_row,1).font=Font(name='Arial',size=10); ws3.cell(ws3.max_row,1).alignment=Alignment(wrap_text=True)
ws3.column_dimensions['A'].width=140
ws4=wb.create_sheet('Rohbelege'); ws4.append(['Datei','SHA-256','Größe (Byte)'])
for f in sorted(glob.glob(R+'/**/*',recursive=True)):
    if os.path.isfile(f): ws4.append([os.path.relpath(f,os.path.dirname(R)),hashlib.sha256(open(f,'rb').read()).hexdigest(),os.path.getsize(f)])
for row in ws4.iter_rows():
    for c in row: c.font=Font(name='Arial',size=10,bold=(c.row==1))
ws4.column_dimensions['A'].width=70; ws4.column_dimensions['B'].width=70
wb.save('/home/claude/work/vp/out/Vorpruefung_Bitvavo_Bloecke_1-5_2026-11-02.xlsx')
json.dump({s:dict(block=blocks[s],**r) for s,r in ALL.items()},open('/home/claude/work/vp/ergebnis_alle.json','w'),indent=1,ensure_ascii=False)
print(sorted(cnt.items()))
