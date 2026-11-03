# Prüffassung Version 1.2.31 aus Arbeitsfassung 1.2.31 (Formeln) und Prüffassung 1.2.30 (Testeingaben), Modus L
import openpyxl,copy,sys
A0=openpyxl.load_workbook('/home/claude/work/out2/Krypto-Bewertungsmatrix_Arbeitsfassung_Version_1.2.30.xlsx')
P0=openpyxl.load_workbook('/home/claude/work/pf/PF_1.2.30.xlsx')
W=openpyxl.load_workbook('/home/claude/work/fs/neu/Krypto-Bewertungsmatrix_Arbeitsfassung_Version_1.2.31.xlsx')
OUT='/home/claude/work/pf/Krypto-Bewertungsmatrix_Prueffassung_Version_1.2.31.xlsx'
for s in ['Ranking','Vorfilter Universum','Kalibrierung','Änderungsprotokoll']:
    del W[s]
assert [ws.title for ws in W.worksheets]==[ws.title for ws in P0.worksheets]
isf=lambda v:isinstance(v,str) and v.startswith('=')
LABEL={('Leitfaden','A1'),('Leitfaden','B18'),('Gates & Status','A6'),('Zeitpunkt & Portfolio','A1'),('Kaufprüfung (Stufe 2)','A1')}
n_in=n_clr=0
for ws in W.worksheets:
    p=P0[ws.title]; a0=A0[ws.title]
    for row in ws.iter_rows(min_row=1,max_row=ws.max_row,max_col=ws.max_column):
        for c in row:
            v=c.value
            if isf(v): continue
            if c.row<=p.max_row:
                if (ws.title,c.coordinate) in LABEL: continue
                pv=p[c.coordinate].value
                assert not isf(pv),(ws.title,c.coordinate)
                if v!=pv: c.value=pv; n_in+=1
            else:
                if ws.title=='Leitfaden': continue
                if v is not None: c.value=None; n_clr+=1
print('aus Prüffassung 1.2.30 übernommen',n_in,'geleert',n_clr)
L=W['Leitfaden']
L['A1'].value=P0['Leitfaden']['A1'].value.replace('PRÜFFASSUNG Version 1.2.30','PRÜFFASSUNG Version 1.2.31')
L['B18'].value=P0['Leitfaden']['B18'].value.replace('Regelkanon Version 1.2.30','Regelkanon Version 1.2.31')
L['A28'].value='Stand Version 1.2.31 (02.11.2026)'
L['B28'].value=('Kanon § 6 Abs. 3 neu: Ein aktualisierbarer Token-Vertrag ist ein dauerhafter Ausschlussgrund nach § 6 Abs. 1 c, wenn die Änderung weder an eine Zeitsperre von mindestens 48 Stunden (Startwert) noch an eine Abstimmung der Tokenhalter gebunden ist; ein von den Tokenhaltern gewähltes und abwählbares Gremium gilt als Abstimmung; ein Prägerecht bis zur festen Höchstmenge ohne Austausch der Programmlogik wirkt nur über Gate und F6. '
 'Eintrag im Erfassungsbogen Spalte AF/AG wie bisher von Hand; keine Formeländerung an Noten, Gate oder Status. '
 'Kapazität: Erfassungsbogen auf Zeilen 6–205 erweitert; alle Verweise auf Erfassungsbogen!…6:…105 in den Blättern Zweitprüfung, Kaufprüfung, Zeitpunkt & Portfolio und STA-Vergleich auf …205 nachgezogen, Auswahllisten und bedingte Formatierung ebenso; Blatt „Tranchen“ bis Zeile 1504. '
 'Neuer Handtest „Bereichsende“ im Abschnitt Prüffassung (Zeile 19). Bewertungskern Version 1.1 und Statusregeln unverändert.')
G=W['Gates & Status']; g0=P0['Gates & Status']['A6'].value
assert A0['Gates & Status']['A6'].value==g0
G['A6'].value=W['Gates & Status']['A6'].value  # Wortlaut 1.2.31, ergebnisfrei
for sh in ['Zeitpunkt & Portfolio','Kaufprüfung (Stufe 2)']:
    W[sh]['A1'].value=P0[sh]['A1'].value.replace('Version 1.2.30)','Version 1.2.31)').replace('– Version 1.2.30','– Version 1.2.31')
b19=P0['Leitfaden']['B19'].value
anker=' Ohne Zweitprüfung:'
assert b19.count(anker)==1
L['B19'].value=b19.replace(anker,' Bereichsende (seit Version 1.2.31): die Eingaben der Zeile von TESTE im Erfassungsbogen vorübergehend in die letzte Zeile 205 kopieren, das Kürzel dort in TESTV ändern und TESTV in eine freie Zeile der Zweitprüfung mit den Eingaben von TESTE eintragen – dann müssen Qualitätsnote, Bewertungsnote, Gate und Status von TESTV im Erfassungsbogen wie in der Zweitprüfung genau denen von TESTE entsprechen (Investment-Sperre bis Wiedervorlage, Abgleich übereinstimmend); danach beide Zeilen wieder leeren.'+anker)
W.save(OUT); print('gespeichert',OUT)
