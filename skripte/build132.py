import openpyxl,copy,datetime as dt
from openpyxl.worksheet.datavalidation import DataValidation
SRC='/home/claude/work/v132/AF_1.2.31_Anleger.xlsx'
OUT='/home/claude/work/v132/Krypto-Bewertungsmatrix_Arbeitsfassung_Version_1.2.32.xlsx'
D=lambda s: dt.datetime.strptime(s,'%d.%m.%Y')
wb=openpyxl.load_workbook(SRC)
E_=wb['Erfassungsbogen']
def row(t):
    r=[r for r in range(6,206) if E_.cell(r,1).value==t]; assert len(r)==1,t; return r[0]
col=lambda L: openpyxl.utils.column_index_from_string(L)
def setv(r,L,v): 
    c=E_.cell(r,col(L)); assert not (isinstance(c.value,str) and c.value.startswith('=')),(r,L); c.value=v
# ---- XRP
r=row('XRP')
setv(r,'F',D('03.11.2026')); setv(r,'L',2); setv(r,'AB',None)
setv(r,'Y','Künftige Wiedersperrung der Treuhand freiwillig, nicht vertraglich – nach § 11 Abs. 1 Satz 2 nicht anrechenbar; Zuordnung der Konten zu Ripple nur aus XRPSCAN (Hinweis); MVRV nur aus einer Quelle')
setv(r,'Z',0.689); setv(r,'AA',0.174)
setv(r,'AC','1 Mrd. XRP je Monat aus Treuhand (Ripple), frühestens ab 01.12.2026 bis 01.06.2029, Rest 0,1 Mrd. am 01.07.2029; Wiedersperrung freiwillig')
setv(r,'AN','Vertragliche Verpflichtung zur Wiedersperrung; neuer Treuhand- oder Freigabeplan; MVRV über 2,5')
setv(r,'AO',D('01.07.2029'))
setv(r,'AP','F1 Zahlungsverkehr nach D-18; F3 Liquidität und Rechtslage; F6 nach D-14 mit frei übertragbaren Unternehmensguthaben im Umlauf (68,9 Mrd.); F7 Abhängigkeit von Ripple')
setv(r,'AQ','Claude, Klassenfrage; berichtigt nach Abgleich 03.11.2026')
setv(r,'AR','Treuhand, Freigaben und Gesamtmenge P/V (XRP Ledger 108096366); Kontenzuordnung S/E; MVRV A/E; 200-Wochen R aus P; Umlauf R aus P')
# ---- XLM
r=row('XLM')
setv(r,'F',D('03.11.2026')); setv(r,'C','Plattform (L1/L2)')
for L,v in zip('GHIJKLM',[4,3,2,5,4,2,2]): setv(r,L,v)
setv(r,'Q',15860); setv(r,'T',None)
setv(r,'Y','Gebühren nur als 365-Tage-Wert (Monatsreihe nach D-03 fehlt), ohne Folge beim 15.860-Fachen; Kontrollkennzahl Burn/Emission nicht bestimmbar (keine Emission); Empfänger der Stiftungsabflüsse nicht zugeordnet (Obergrenze verwendet)')
setv(r,'Z',0.705); setv(r,'AA',0.099); setv(r,'AB',None)
setv(r,'AC','Verteilungen der Stiftung ohne festen Plan; in zwölf Monaten bis 03.11.2026 höchstens 3,48 Mrd. XLM an andere Konten (Horizon)')
setv(r,'AN','Gebühren auf mehr als das Zwanzigfache; Änderung des Gebührentopfs; Änderung des Stiftungsmandats')
setv(r,'AP','F1 Zahlungsverkehr und Tokenisierung nach D-18; F3 Nischenführer; F4 Gebühr in XLM für jede Transaktion zwingend; F5 Gebührentopf als dauerhafte Sperre, durch Abstimmung änderbar, höchstens 4 (developers.stellar.org/docs/learn/fundamentals/lumens); F7 Abhängigkeit von der Stiftung')
setv(r,'AQ','Claude, Klassenfrage; Klasse nach Abgleich 03.11.2026 Plattform')
setv(r,'AR','Gebühren A/E; Gebührentopf, Gesamtmenge und Stiftungsabflüsse P/V (Horizon, Ledger 65291245); Kurs P/E')
setv(r,'AV','Burn')
# ---- Zweitprüfung
Z=wb['Zweitprüfung']
def zrow(t):
    r=[r for r in range(6,106) if Z.cell(r,1).value==t]; assert len(r)==1,t; return r[0]
def zset(r,vals):
    for L,v in vals.items():
        c=Z.cell(r,col(L)); assert not (isinstance(c.value,str) and c.value.startswith('=')),(r,L); c.value=v
zset(zrow('XRP'),dict(N=D('03.11.2026'),O=3,P=3,Q=2,R=5,S=3,T=2,U=2,V=100,W='C',X='Investment-Sperre',Y='Investment-Sperre bis Wiedervorlage',
 AF='Investment-Sperre bis Wiedervorlage',
 AG='Abgleich 03.11.2026, Entscheidung des Anlegers vom selben Tag: Gate nach § 11 Abs. 2 – Zuwachs 12 Mrd. XRP (17,4 % des Umlaufs nach D-04, D-14, Ledger 108096366); künftige Absorption nicht bestimmbar, weil die Wiedersperrung der Treuhand freiwillig ist (§ 11 Abs. 1 Satz 2, Version 1.2.32). Erstbewertung berichtigt: F6 = 2 (D-14). Restabweichung Qualitätsnote 61 gegen 56 aus F1 (4 gegen 3; D-18 ordnet Zahlungsverkehr den Noten 4 bis 5 zu) und F3 (3 gegen 2, Deutung), je eine Note, ohne Folge für den Status, weil Regel 6 in beiden Fällen greift. Belege: Abgleich_XRP_XLM_2026-11-03.txt, Nachtrag_Datenpaket_XRP_2026-11-03.zip.',
 AH='Zweitprüfung 03.11.2026 nach Nachtrag; erste Fassung vorläufig „unvollständig“ wegen fehlender Belege im Datenpaket'))
zset(zrow('XLM'),dict(N=D('03.11.2026'),O=5,P=3,Q=3,R=5,S=4,T=2,U=2,V=0,W='C',X='ok',Y='Qualität ja – Bewertung abwarten',
 AF='Qualität ja – Bewertung abwarten',
 AG='Abgleich 03.11.2026, Entscheidung des Anlegers vom selben Tag: Klasse Plattform (§ 5 Abs. 1 – Wert entsteht als Abwicklungsplattform für Stablecoins und tokenisierte Werte; XLM dient für Gebühren und Reserven). Bewertungsnote 0 (FDV/Gebühren rund 15.860-fach). F5 = 4 nach Klärung B 2 (Gebührentopf als dauerhafte Sperre, durch Abstimmung änderbar; developers.stellar.org). Gate ok: Stiftungsabflüsse höchstens 9,9 % (Horizon, Obergrenze nach Q-04). Restabweichung Qualitätsnote 62 gegen 67 (F1, F3, Deutung) ohne Folge für den Status, weil Regel 9 in beiden Fällen greift.',
 AH='Erste Zweitprüfung ohne Regelkanon Version 1.2.31 wiederholt; Wiederholung 03.11.2026 Optionsliste (F5 = 0), nach Klärung B 2 korrigiert'))
# ---- Protokoll
P=wb['Protokoll']
last=max(r for r in range(5,505) if P.cell(r,1).value is not None)
def prow(vals):
    global last
    last+=1
    for L,v in vals.items(): P.cell(last,col(L)).value=v
    for c in range(1,33):
        if P.cell(last-1,c).has_style: P.cell(last,c)._style=copy.copy(P.cell(last-1,c)._style)
prow(dict(A=dt.datetime(2026,11,2,17,16),B='alle Märkte (427)',C='Listungsabgleich',D='Q-18; Kanon § 4 Abs. 3',G='Neu seit dem vorigen Abgleich: AXIS-EUR (gelistet seit 21.10.2026); eingestellt: keiner mit Bestand',H='Basisstand für den wöchentlichen Abgleich; Erstbewertung AXIS am 02.11.2026 (Frist nach Q-18 überschritten, weil der wöchentliche Abgleich fehlte)',O='Bitvavo /v2/markets, Abruf 02.11.2026 17:16 Uhr Weltzeit',AF='Nachgetragen mit Version 1.2.32; ab 09.11.2026 wöchentlich als geplante Aufgabe (montags 7:47 Uhr), Stände im Archiv krypto-matrix unter datenstaende/listung'))
prow(dict(A=dt.datetime(2026,11,3,23,30),B='XRP',C='Abschluss Abgleich',D='Kanon § 16; § 11 Abs. 1 Satz 2 (Version 1.2.32)',E='Investment-Sperre bis Wiedervorlage',F=100,G='Ergebnis nach Abgleich: Investment-Sperre bis Wiedervorlage',H='Zuwachs 17,4 % nach D-04; freiwillige Wiedersperrung nicht anrechenbar; Erstbewertung berichtigt (F6 = 2, Qualitätsnote 61)',O='XRP Ledger 108096366 (03.11.2026); Datenpaket 02.11.2026',AF='Abschlussbericht: Krypto-Matrix/Berichte/Abschluss_XRP_2026-11-03.txt; Kursantrieb: marktgetrieben (Deutung; RS90 +0,1 Prozentpunkte, Gleichlauf mit Bitcoin 0,88)'))
prow(dict(A=dt.datetime(2026,11,3,23,31),B='XRP',C='Statuswechsel',D='Kanon § 14 Regel 6; § 16 Abs. 4',E='Investment-Sperre bis Wiedervorlage',F=100,G='Satellit (Erstbewertung) → Investment-Sperre bis Wiedervorlage',H='Gate Investment-Sperre nach Abgleich',I=1.11511,O='Bitvavo /v2/ticker/price 02.11.2026 22:25 Uhr Weltzeit'))
prow(dict(A=dt.datetime(2026,11,3,23,50),B='XLM',C='Abschluss Abgleich',D='Kanon § 16; § 5 Abs. 1; § 7 Abs. 9',E='Qualität ja – Bewertung abwarten',F=0,G='Ergebnis nach Abgleich: Qualität ja – Bewertung abwarten',H='Klasse Plattform; Bewertungsnote 0; F5 = 4 nach Klärung; Gate ok (Obergrenze 9,9 %)',O='Horizon Ledger 65291245 (03.11.2026); Datenpaket 02.11.2026',AF='Abschlussbericht: Krypto-Matrix/Berichte/Abschluss_XLM_2026-11-03.txt; Kursantrieb: marktgetrieben mit relativer Schwäche (Deutung; RS90 -22,1 Prozentpunkte, Gleichlauf mit Bitcoin 0,74)'))
prow(dict(A=dt.datetime(2026,11,3,23,51),B='XLM',C='Statuswechsel',D='Kanon § 14 Regel 9',E='Qualität ja – Bewertung abwarten',F=0,G='Satellit (Erstbewertung) → Qualität ja – Bewertung abwarten',H='Klasse Plattform statt Geldwert-Asset nach Abgleich',I=0.14645,O='Bitvavo /v2/ticker/price 02.11.2026 22:25 Uhr Weltzeit'))
OHNE='OR(C{r}="Datenübernahme",C{r}="Listungsabgleich",C{r}="Abruffehler",C{r}="Abschluss Abgleich")'
for rr in range(5,505):
    f=P.cell(rr,col('AE')).value
    assert f.startswith(f'=IF(A{rr}="","",IF(C{rr}="A13-Signal"'),rr
    P.cell(rr,col('AE')).value=f'=IF(A{rr}="","",IF({OHNE.format(r=rr)},"entfällt (ohne Kursbezug)",'+f[len(f'=IF(A{rr}="","",'):]+')'
for dv in P.data_validations.dataValidation:
    if 'Datenübernahme' in (dv.formula1 or ''): dv.formula1=dv.formula1[:-1]+',Listungsabgleich"'
P['A2'].value=P['A2'].value.rstrip()+' Seit Version 1.2.32: Vorgänge ohne Kursbezug (Datenübernahme, Listungsabgleich, Abruffehler, Abschluss Abgleich) erhalten keine Nachschau; „Nachtrag fällig“ zeigt dort „entfällt (ohne Kursbezug)“ (Kanon § 31 Abs. 2). Jeder Listungsabgleich mit Ergebnis erhält eine Zeile „Listungsabgleich“ (Kanon § 31 Abs. 1).'
# ---- Tranchen: noch gehaltene Menge
T=wb['Tranchen']
T['O4'].value='Noch gehaltene Menge (FIFO je Coin und Wallet)'; T['O4']._style=copy.copy(T['N4']._style)
T.column_dimensions['O'].width=22
for rr in range(5,1505):
    T.cell(rr,15).value=(f'=IF(OR(A{rr}="",AND(C{rr}<>"Kauf",C{rr}<>"Zugang ohne Kauf")),"",MAX(0,MIN(D{rr},'
      f'SUMPRODUCT(($B$5:$B$1504=B{rr})*($H$5:$H$1504=H{rr})*(($C$5:$C$1504="Kauf")+($C$5:$C$1504="Zugang ohne Kauf"))*(($A$5:$A$1504<A{rr})+($A$5:$A$1504=A{rr})*(ROW($A$5:$A$1504)<=ROW(A{rr}))),$D$5:$D$1504)'
      f'-SUMPRODUCT(($B$5:$B$1504=B{rr})*($H$5:$H$1504=H{rr})*(($C$5:$C$1504="Verkauf")+($C$5:$C$1504="Abgang ohne Verkauf")),$D$5:$D$1504))))')
    if T.cell(rr,14).has_style: T.cell(rr,15)._style=copy.copy(T.cell(rr,4)._style)
T['A2'].value=T['A2'].value.rstrip()+' Seit Version 1.2.32: Spalte O zeigt je Kauf und Zugang die noch gehaltene Menge nach FIFO je Coin und Wallet (Verkäufe und Abgänge verbrauchen die ältesten Zeilen zuerst); Grundlage für die Verkaufsmenge „nur abgelaufene Haltefrist“ und für Einstand und Kaufdatum der Portfolioübersicht.'
# ---- Gates & Status
G=wb['Gates & Status']
G['A15'].value=G['A15'].value.rstrip()+' Seit Version 1.2.32 (Kanon § 11 Abs. 1 Satz 2): Für die kommenden zwölf Monate zählen Rückkäufe, Burns und neue Sperren nur, soweit ein Vertrag oder ein Protokollmechanismus sie auslöst; freiwillige Maßnahmen einer Firma, Stiftung oder Projektkasse zählen erst, wenn sie vollzogen sind, und werden für die Prognose nur vermerkt (wie geringere Abrufe nach D-04). Ist die Absorption danach nicht bestimmbar, bleibt Spalte AB leer und gilt als zu gering.'
# ---- Leitfaden, Versionsangaben
L=wb['Leitfaden']
L['A1'].value=L['A1'].value.replace('Version 1.2.31 (Regelstand 02.11.2026','Version 1.2.32 (Regelstand 04.11.2026')
assert 'Version 1.2.32' in L['A1'].value
L['B18'].value=L['B18'].value.replace('Regelkanon Version 1.2.31','Regelkanon Version 1.2.32'); assert '1.2.32' in L['B18'].value
L.cell(29,1).value='Stand Version 1.2.32 (04.11.2026)'
L.cell(29,1)._style=copy.copy(L.cell(28,1)._style); L.cell(29,2)._style=copy.copy(L.cell(28,2)._style)
L.cell(29,2).value=('Entscheidungen des Anlegers vom 03.11.2026. Regel: Kanon § 11 Abs. 1 Satz 2 neu – künftige Absorption nur aus Vertrag oder Protokollmechanismus; freiwillige Maßnahmen zählen erst nach Vollzug (Gates & Status A15). Betroffen nach Prüfung aller Coins mit mehr als 15 % Zuwachs: nur XRP (CC verbrennt protokollseitig, CAKE unter 15 %). '
 'Verfahren: Datenpakete für Kandidaten stets mit Blockchain-Prüfung und Quellenregister; die Zweitprüfung erhebt fehlende Belege zu den Kriterien selbst. '
 'Formales: Kanon § 31 – Vorgang „Listungsabgleich“ im Protokoll; Vorgänge ohne Kursbezug ohne Nachschau (Protokoll, Spalte AE); Tranchen Spalte O „noch gehaltene Menge“ nach FIFO. '
 'Ergebnisse nach Abgleich vom 03.11.2026: XRP Investment-Sperre bis Wiedervorlage (F6 = 2 berichtigt); XLM Klasse Plattform, Qualität ja – Bewertung abwarten. Bewertungskern Version 1.1, Gewichte, Schwellen, Definitionen und Statusreihenfolge unverändert.')
Z.cell(107,1).value=Z.cell(107,1).value.replace('Version 1.2.31','Version 1.2.32'); assert '1.2.32' in Z.cell(107,1).value
for sh in ['Zeitpunkt & Portfolio','Kaufprüfung (Stufe 2)']:
    v=wb[sh]['A1'].value; wb[sh]['A1'].value=v.replace('Version 1.2.31','Version 1.2.32'); assert '1.2.32' in wb[sh]['A1'].value
# ---- Änderungsprotokoll
A=wb['Änderungsprotokoll']
for c in range(1,6): A.cell(45,c)._style=copy.copy(A.cell(44,c)._style)
A.cell(45,1).value='1.2.32'; A.cell(45,2).value=dt.datetime(2026,11,4)
A.cell(45,3).value='Kanon § 11 Abs. 1 Satz 2 neu (künftige Absorption nur aus Vertrag oder Protokollmechanismus); § 31 Abs. 1 und 2 (Vorgang Listungsabgleich, keine Nachschau ohne Kursbezug). Verfassung Teil F und G (Blockchain-Prüfung und Quellenregister im Datenpaket für Kandidaten; eigene Erhebung fehlender Belege durch die Zweitprüfung). Excel: Gates & Status A15, Protokoll Spalte AE und Auswahlliste, Tranchen Spalte O, Leitfaden; Ergebnisse nach Abgleich XRP und XLM.'
A.cell(45,4).value='Entscheidungen des Anlegers vom 03.11.2026 nach dem Abgleich XRP (freiwillige Wiedersperrung der Treuhand als Absorption angerechnet, von der Zweitprüfung abgelehnt) und XLM (Klasse); Verfahrensmängel: Datenpaket ohne Blockchain-Prüfung führte zu einer unvollständigen Zweitprüfung.'
A.cell(45,5).value='XRP: Gate ok → Investment-Sperre, Status Satellit → Investment-Sperre bis Wiedervorlage; Qualitätsnote 58 → 61 (F6 1 → 2). XLM: Geldwert-Asset → Plattform, Bewertungsnote 88 → 0, Qualitätsnote 58 → 62, Satellit → Qualität ja – Bewertung abwarten. Keine weiteren Coins betroffen.'
# ---- Kalibrierung Teil 15
KB=wb['Kalibrierung']
start=KB.max_row+2
lines=['Teil 15. Abgleich XRP und Stellar mit der Zweitprüfung (03.11.2026) und Fortschreibung Version 1.2.32',
 'Ergebnis: XRP Investment-Sperre bis Wiedervorlage (Erstbewertung 58/100/C/ok/Satellit, Zweitprüfung 56/100/C/Investment-Sperre; berichtigt 61/100/C/Investment-Sperre). XLM Qualität ja – Bewertung abwarten (Erstbewertung Geldwert 58/88/C/ok/Satellit; Zweitprüfung Plattform 67/0/C/ok; berichtigt Plattform 62/0/C/ok). Zählung zu Teil 14 berichtigt: bewertet wurden 16 der 34 Anwärter und AXIS; 18 Anwärter offen.',
 'K-37 (entschieden 03.11.2026, Version 1.2.32): Absorption der kommenden zwölf Monate nur aus Vertrag oder Protokollmechanismus; freiwillige Maßnahmen zählen erst nach Vollzug (§ 11 Abs. 1 Satz 2). Anlass XRP: 70 % Wiedersperrung in zwölf Monaten belegt (Ledger), aber freiwillig. Ersetzt die Deutung aus K-34. Geprüft: CC (protokollseitige Verbrennung) und CAKE (Zuwachs 1,7 %) unverändert.',
 'K-38 (Klassenfrage, ersetzt K-36 für Stellar): Maßgeblich ist, womit das Netz tatsächlich Wert schafft. Stellar ist Abwicklungsplattform für Stablecoins und tokenisierte Werte; XLM dient für Gebühren und Reserven → Plattform. XRP bleibt Geldwert-Asset, weil der Coin selbst die Zahlungsfunktion als Brückenwährung trägt. Lehre: Bauart und Selbstbeschreibung sind nach § 5 Abs. 1 kein Maßstab.',
 'K-39 (Ankerfall F5): Ein protokollseitiger Gebührentopf ohne Zugriff (Stellar fee_pool) ist eine dauerhafte Sperre nach § 7 Abs. 9; durch Abstimmung der Validatoren änderbar, daher höchstens 4. Die Zweitprüfung hatte zunächst 0 vergeben und nach Klärung korrigiert.',
 'K-40 (Definition D-14): Frei übertragbare Guthaben einer Firma (Ripple, 4,1 Mrd. XRP) gehören zum Umlauf; nur vertraglich gesperrte oder treuhänderische Bestände nicht. Stiftungsreserven ohne Plan (Stellar) bleiben nach D-11 außerhalb des Umlaufs. Folge XRP: F6 13,2 % statt 16 %, Note 2.',
 'K-41 (Beobachtung D-18): Die Zweitprüfung vergab bei XRP F1 = 3, obwohl D-18 Zahlungsverkehr den Noten 4 bis 5 zuordnet; Erstbewertung blieb bei 4. Hinweis bei der nächsten Gegenprüfung, ohne Folge für den Status.',
 'K-42 (Verfahren): Das erste Datenpaket XRP enthielt nur Markt- und Mengendaten; die Zweitprüfung ließ sechs Noten offen („unvollständig“). Erst Ledgerdaten (Treuhand, Freigaben, Wiedersperrung) und die Aufforderung zur eigenen Erhebung führten zu einem vollständigen Ergebnis. Folge: Verfassung Teil F und G sowie beide Betriebsdokumente fortgeschrieben (Version 1.2.32).',
 'Lehre: Bei Kandidaten mit großen Treuhand-, Stiftungs- oder Firmenbeständen entscheiden Primärdaten der Blockchain über Gate und F6; sie gehören von Anfang an ins Datenpaket.']
for i,t in enumerate(lines):
    KB.cell(start+i,1).value=t
    KB.cell(start+i,1)._style=copy.copy(KB.cell(243 if i==0 else 244,1)._style)
wb.save(OUT); print('gespeichert',OUT,'Protokoll bis Zeile',last,'Kalibrierung ab',start)
