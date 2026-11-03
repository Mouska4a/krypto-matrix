# Prüffassung Version 1.2.32: Formeln aus Arbeitsfassung 1.2.32, Testeingaben aus Prüffassung 1.2.31 (Modus L)
import openpyxl
P0=openpyxl.load_workbook('/home/claude/work/pf/Krypto-Bewertungsmatrix_Prueffassung_Version_1.2.31.xlsx')
W=openpyxl.load_workbook('/home/claude/work/v132/Krypto-Bewertungsmatrix_Arbeitsfassung_Version_1.2.32.xlsx')
OUT='/home/claude/work/v132/Krypto-Bewertungsmatrix_Prueffassung_Version_1.2.32.xlsx'
for s in ['Ranking','Vorfilter Universum','Kalibrierung','Änderungsprotokoll']: del W[s]
assert [ws.title for ws in W.worksheets]==[ws.title for ws in P0.worksheets]
isf=lambda v:isinstance(v,str) and v.startswith('=')
KEEP_W={('Gates & Status','A6'),('Gates & Status','A15'),('Zeitpunkt & Portfolio','A1'),('Kaufprüfung (Stufe 2)','A1'),('Tranchen','O4'),('Tranchen','A2'),('Protokoll','A2')}
n=0
for ws in W.worksheets:
    p=P0[ws.title]
    for row in ws.iter_rows(min_row=1,max_row=ws.max_row,max_col=ws.max_column):
        for c in row:
            if isf(c.value) or (ws.title,c.coordinate) in KEEP_W: continue
            if c.row<=p.max_row:
                pv=p[c.coordinate].value
                assert not isf(pv),(ws.title,c.coordinate)
                if c.value!=pv: c.value=pv; n+=1
            elif ws.title!='Leitfaden' and c.value is not None: c.value=None; n+=1
print('angepasst',n)
L=W['Leitfaden']
L['A1'].value=P0['Leitfaden']['A1'].value.replace('PRÜFFASSUNG Version 1.2.31','PRÜFFASSUNG Version 1.2.32'); assert '1.2.32' in L['A1'].value
L['B18'].value=P0['Leitfaden']['B18'].value.replace('Regelkanon Version 1.2.31','Regelkanon Version 1.2.32'); assert '1.2.32' in L['B18'].value
anker=' Ohne Zweitprüfung:'
b19=P0['Leitfaden']['B19'].value; assert b19.count(anker)==1
L['B19'].value=b19.replace(anker,' Ohne Kursbezug (seit Version 1.2.32): im Blatt „Protokoll“ den Vorgang einer Testzeile vorübergehend auf „Listungsabgleich“ setzen – dann zeigt „Nachtrag fällig“ (AE) „entfällt (ohne Kursbezug)“; danach zurücksetzen. Noch gehaltene Menge (seit Version 1.2.32): im Blatt „Tranchen“ vorübergehend eine Zeile „Verkauf“ für TESTA mit einer Menge kleiner als die erste Kaufzeile eintragen – dann sinkt Spalte O nur in der ältesten Kaufzeile von TESTA um diese Menge; danach leeren.'+anker)
L['A29'].value='Stand Version 1.2.32 (04.11.2026)'
L['B29'].value=('Kanon § 11 Abs. 1 Satz 2 neu: Für die Absorption der kommenden zwölf Monate zählen Rückkäufe, Burns und neue Sperren nur, soweit ein Vertrag oder ein Protokollmechanismus sie auslöst; freiwillige Maßnahmen einer Firma, Stiftung oder Projektkasse zählen erst nach Vollzug (Text in Gates & Status A15; keine Formeländerung, die Eingabe in Erfassungsbogen AB folgt der Regel). '
 'Kanon § 31: Vorgang „Listungsabgleich“ in der Auswahlliste des Protokolls; Vorgänge ohne Kursbezug (Datenübernahme, Listungsabgleich, Abruffehler, Abschluss Abgleich) zeigen in Spalte AE „entfällt (ohne Kursbezug)“. Tranchen Spalte O neu: noch gehaltene Menge je Kauf nach FIFO je Coin und Wallet. '
 'Bewertungskern Version 1.1, Gewichte, Schwellen, Definitionen und Statusreihenfolge unverändert; Testfälle TESTA bis TESTU unverändert, zwei neue Handtests im Abschnitt Prüffassung (Zeile 19).')
W.save(OUT); print('gespeichert',OUT)
