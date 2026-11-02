import openpyxl,re,json,datetime,copy
from openpyxl.formula.translate import Translator
from openpyxl.worksheet.cell_range import MultiCellRange
SRC='/home/claude/work/out2/Krypto-Bewertungsmatrix_Arbeitsfassung_Version_1.2.30.xlsx'
OUT='/home/claude/work/fs/neu/Krypto-Bewertungsmatrix_Arbeitsfassung_Version_1.2.31.xlsx'
NEWLAST=205
wb=openpyxl.load_workbook(SRC)
E_=wb['Erfassungsbogen']
# 1) Bereichserweiterung Erfassungsbogen 6:105 -> 6:205 in allen Formeln
rx=re.compile(r"(Erfassungsbogen!\$?[A-Z]{1,3}\$?6:\$?[A-Z]{1,3}\$?)105(?![0-9])")
n=0
for ws in wb:
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value,str) and c.value.startswith('=') and 'Erfassungsbogen!' in c.value:
                new=rx.sub(lambda m:m.group(1)+str(NEWLAST),c.value)
                if new!=c.value: c.value=new; n+=1
print('Formeln erweitert',n)
# 2) Formeln und Formate der Zeilen 106..205 aus Zeile 105 (bzw. 103) übernehmen
src_r=103
for r in range(104,NEWLAST+1):
    for col in range(1,54):
        s=E_.cell(src_r,col); t=E_.cell(r,col)
        if isinstance(s.value,str) and s.value.startswith('='):
            if t.value is None or r>105:
                t.value=Translator(s.value,origin=s.coordinate).translate_formula(t.coordinate)
        if s.has_style: t._style=copy.copy(s._style)
# DV und CF erweitern
for dv in E_.data_validations.dataValidation:
    dv.sqref=MultiCellRange(str(dv.sqref).replace('105',str(NEWLAST)))
from openpyxl.formatting.formatting import ConditionalFormattingList
old=E_.conditional_formatting; newcf=ConditionalFormattingList()
for cf in old:
    rng=str(cf.sqref).replace('105',str(NEWLAST))
    for rule in cf.rules: newcf.add(rng,rule)
E_.conditional_formatting=newcf
# 3) 17 Coins eintragen
D=json.load(open('/home/claude/work/fs/neu/coins22.json'))
def val(s):
    if s is None: return None
    s=s.strip()
    if s in ('','leer'): return None
    if re.fullmatch(r'\d\d\.\d\d\.\d{4}',s): return datetime.datetime.strptime(s,'%d.%m.%Y')
    if re.fullmatch(r'-?\d+(,\d+)?',s): return float(s.replace(',','.')) if ',' in s else int(s)
    return s
order=['OSMO','LPT','EDEN','CHIP','SCR','LINEA','AXIS','FUEL','KAT','MERL','EDGE','AEVO','XRP','XLM','DGB','XVG','ETC']
WV={'XRP':'02.02.2027','XLM':'02.02.2027','DGB':'02.02.2027','XVG':'02.02.2027','ETC':'02.02.2027'}
r=104
rows={}
for coin in order:
    d=D[coin]
    for i,v in enumerate(d['AM']): E_.cell(r,1+i).value=val(v)
    E_.cell(r,17).value=val(d['Q']); E_.cell(r,20).value=val(d['T'])
    for i,v in enumerate(d['XAD']): E_.cell(r,24+i).value=val(v)
    E_.cell(r,32).value='nein'
    if coin=='AXIS': E_.cell(r,33).value='möglicher Grund § 6 Abs. 1 c geprüft: Eigentümer kann Programmlogik austauschen und prägen; Zeitsperre und Abstimmung nicht belegt – Neubewertung nach § 6 Abs. 3 (Version 1.2.31) fällig'
    for i,v in enumerate(d['ALAX']): E_.cell(r,38+i).value=val(v)
    if coin in WV: E_.cell(r,41).value=val(WV[coin])
    rows[coin]=r; r+=1
json.dump(rows,open('/home/claude/work/fs/neu/rows.json','w'))
# 4) Zweitprüfung: XRP und XLM vormerken
Z=wb['Zweitprüfung']
Z.cell(103,1).value='XRP'; Z.cell(104,1).value='XLM'
# 5) Versionsangaben
L=wb['Leitfaden']
L['A1'].value=L['A1'].value.replace('Version 1.2.30 (Regelstand 01.11.2026','Version 1.2.31 (Regelstand 02.11.2026')
L['B18'].value=L['B18'].value.replace('Regelkanon Version 1.2.30','Regelkanon Version 1.2.31')
L.cell(28,1).value='Stand Version 1.2.31 (02.11.2026)'
L.cell(28,1)._style=copy.copy(L.cell(27,1)._style); L.cell(28,2)._style=copy.copy(L.cell(27,2)._style)
L.cell(28,2).value=('Entscheidung des Anlegers vom 02.11.2026: Kanon § 6 Abs. 3 neu – ein aktualisierbarer Token-Vertrag ist ein dauerhafter Ausschlussgrund nach § 6 Abs. 1 c, wenn die Änderung weder an eine Zeitsperre von mindestens 48 Stunden (Startwert) noch an eine Abstimmung der Tokenhalter gebunden ist; ein von den Tokenhaltern gewähltes und abwählbares Gremium gilt als Abstimmung; ein Prägerecht bis zur festen Höchstmenge ohne Austausch der Programmlogik wirkt nur über Gate und F6. '
 'Eintrag in Erfassungsbogen Spalte AF/AG wie bisher von Hand, Nachweis am Vertrag im Explorer. Keine Formeländerung an Noten, Gate oder Status. '
 'Kapazität: Erfassungsbogen auf Zeilen 6–205 erweitert; alle Verweise auf Erfassungsbogen!…6:…105 in den Blättern Zweitprüfung, Kaufprüfung, Zeitpunkt & Portfolio und STA-Vergleich auf …205 nachgezogen, Auswahllisten und bedingte Formatierung ebenso. Blatt „Tranchen“ seit 02.11.2026 bis Zeile 1504. '
 'Neu im Erfassungsbogen: 17 Erstbewertungen vom 02.11.2026 (Zeilen 104–120); Blatt „Vorfilter Universum“ mit den Ergebnissen der Vorprüfung vom 02.11.2026. Bewertungskern Version 1.1 und Statusregeln unverändert.')
Z.cell(107,1).value=Z.cell(107,1).value.replace('Version 1.2.30','Version 1.2.31')
P=wb['Zeitpunkt & Portfolio']; P['A1'].value=P['A1'].value.replace('Version 1.2.30','Version 1.2.31')
K=wb['Kaufprüfung (Stufe 2)']; K['A1'].value=K['A1'].value.replace('Version 1.2.30','Version 1.2.31')
G=wb['Gates & Status']
G['A6'].value=G['A6'].value.rstrip()+' Seit Version 1.2.31 (Kanon § 6 Abs. 3): auch ein aktualisierbarer Token-Vertrag, dessen Änderung weder an eine Zeitsperre von mindestens 48 Stunden noch an eine Abstimmung der Tokenhalter (oder eines von ihnen gewählten, abwählbaren Gremiums) gebunden ist; Prägerecht bis zur festen Höchstmenge nur über Gate und F6; eigenständige Coins ohne Token-Vertrag nicht betroffen.'
# 6) Änderungsprotokoll
A=wb['Änderungsprotokoll']
for c in range(1,6): A.cell(44,c)._style=copy.copy(A.cell(43,c)._style)
A.cell(44,1).value='1.2.31'; A.cell(44,2).value=datetime.datetime(2026,11,2)
A.cell(44,3).value='Kanon § 6 Abs. 3 neu (aktualisierbare Token-Verträge ohne Zeitsperre von mindestens 48 Stunden und ohne Abstimmung der Tokenhalter als Ausschlussgrund nach § 6 Abs. 1 c); § 35 Startwert ergänzt. Excel: Text in „Gates & Status“ A6 und Leitfaden; Kapazität Erfassungsbogen 6–205 mit allen Verweisen; 17 neue Erstbewertungen; Vorfilter Universum mit Vorprüfung 02.11.2026.'
A.cell(44,4).value='Entscheidung des Anlegers vom 02.11.2026 nach dem Fall AXIS (Eigentümer kann Programmlogik austauschen und prägen). Parameter: Zeitsperre mindestens 48 Stunden (Startwert); gewähltes Gremium zählt als Abstimmung; Prägerecht bis Höchstmenge nur über Gate und F6.'
A.cell(44,5).value='Keine Scoreänderung, keine Änderung an Gewichten, Schwellen, Definitionen oder Statusreihenfolge. Prüfauftrag: Token-Verträge der bisherigen Kandidaten und Bestände nach § 6 Abs. 3 prüfen (zuerst POL und SKY, binnen sieben Tagen nach N2).'
# 7) Kalibrierung Teil 14
KB=wb['Kalibrierung']
start=243
lines=['Teil 14. Erstbewertungen vom 02.11.2026 (34 Anwärter der Vorprüfung, davon 17 bewertet) und Entscheidung zu § 6 Abs. 1 c',
 'Ergebnis: 13 von 17 ohne Kandidatenstatus; Kandidaten der Erstbewertung XRP und XLM (Satellit, Zweitprüfung fehlt); Optionsliste OSMO, DGB, XVG, ETC; übrige Kein Kandidat. Hauptursachen: F5 ohne Wertrückfluss, F6 mit großen Freigaben, Run-Rate-Einbrüche über minus 50 Prozent.',
 'K-32 (Beobachtung, keine Änderung): D-01 und Delegierende – bei Netzen mit Delegation (Livepeer, Osmosis) ist nicht ausdrücklich geregelt, ob der Gebührenanteil der Delegierenden Ausschüttung an passive Halter ist. Erstbewertung wertet ihn wie Validatorenvergütung (kein Wertrückfluss). Folge bei anderer Lesart: LPT F5 bis 4, OSMO F5 unverändert. Entscheidung frühestens 22.04.2027.',
 'K-33 (Beobachtung): D-06 Wachstum bei Beginn eines Mechanismus am Ende des Vorjahreszeitraums (Definitive, +905 Prozent) überzeichnet die Kontrollkennzahl; regelgerecht gerechnet, ohne Folge für den Status.',
 'K-34 (Deutungsfrage für den Abgleich): XRP – freiwillige Wiedersperrung in neue Treuhandverträge über mehr als zwölf Monate als Absorption nach § 11 angerechnet (historisch 70 bis 80 Prozent), analog zur geschätzten Verbrennung bei CAKE. Ohne Anrechnung: Investment-Sperre.',
 'K-35 (Datenbeobachtung): Coin Metrics SplyCur für XLM enthält die 2019 auf ein gesperrtes Konto übertragenen 55,4 Mrd. XLM; MVRV dadurch verzerrt. Nach Grundsatz 4 ungünstigerer zulässiger Wert (1,31, 80 Punkte).',
 'K-36 (Klassenfrage): Zahlungsnetze mit absichtlich minimalen, vernichteten Gebühren (XRP, XLM) als Geldwert-Asset geführt, Programmplattform ohne Nutzung (ETC) als Plattform. Maßstab: Bauart des Wertmodells, nicht Ergebnis. Blinde Zweitprüfung der Klasse bei XRP und XLM.',
 'Entscheidung des Anlegers 02.11.2026 zu § 6 Abs. 1 c: aktualisierbare Token-Verträge ohne Zeitsperre von mindestens 48 Stunden und ohne Abstimmung der Tokenhalter sind Ausschlussgrund (neuer § 6 Abs. 3, Version 1.2.31). Anlass AXIS (Basescan: UUPS-Vertrag, Eigentümer kann Logik austauschen und prägen).',
 'Lehre: Vertragsrechte sind Primärdaten, die sich am Explorer in Minuten prüfen lassen; sie gehören vor jede Notenvergabe bei Token mit Vertrag.']
for i,t in enumerate(lines):
    KB.cell(start+i,1).value=t
    KB.cell(start+i,1)._style=copy.copy(KB.cell(233 if i==0 else 234,1)._style)
wb.save(OUT); print('gespeichert',OUT)
