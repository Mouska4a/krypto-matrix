import re
SRC=[('TEIL 2. GRUPPE 1: OSMOSIS, LIVEPEER, OPENEDEN, USD.AI, SCROLL, LINEA','/home/claude/work/eb/Erstbewertung_Gruppe1_2026-11-02.txt'),
     ('TEIL 3. AXIS ROBOTICS','/home/claude/work/eb2/Erstbewertung_AXIS_2026-11-02.txt'),
     ('TEIL 4. GRUPPE 2: FUEL, KATANA, MERLIN CHAIN, DEFINITIVE, AEVO','/home/claude/work/eb2/Erstbewertung_Gruppe2_2026-11-02.txt'),
     ('TEIL 5. DIE FÜNF COINS MIT KLASSENFRAGE: XRP, STELLAR, DIGIBYTE, VERGE, ETHEREUM CLASSIC','/home/claude/work/eb3/Erstbewertung_Klassenfrage_2026-11-02.txt')]
def part(title,path,tn):
    L=open(path,encoding='utf-8').read().split('\n')
    i=next(k for k,l in enumerate(L) if re.match(r'^1\. [A-ZÄÖÜ]',l))
    meta=[l.strip() for l in L[1:i] if l.strip()]
    body=[]
    for l in L[i:]:
        if l.startswith('EINFÜGEZEILEN'): break
        m=re.match(r'^(\d+)\. ([A-ZÄÖÜ].*)$',l)
        if m and m.group(2)==m.group(2).upper(): l=f'{tn}.{m.group(1)} {m.group(2)}'
        body.append(l)
    while body and not body[-1].strip(): body.pop()
    return [title,'',' '.join(meta),'']+body+['','']
intro='''ERSTBEWERTUNGEN DER NEUEN ANWÄRTER VOM 2. NOVEMBER 2026
Siebzehn Coins aus der Vorprüfung des Bitvavo-Universums, mit Stand der Zweitprüfung vom 3. November 2026
Zusammenfassung der vier Einzelberichte vom 2. November 2026 (Regelwerk Version 1.2.30); Hinweise zum Stand nach Regelwerk Version 1.2.31 in Teil 1


EINLEITUNG

Die Vorprüfung vom 2. November 2026 hat aus den 260 bis dahin nie geprüften Coins des Bitvavo-Universums diejenigen herausgefiltert, die nach den Regeln überhaupt eine Bewertungsnote über null erreichen können. Siebzehn davon sind am selben Tag vollständig bewertet worden; dieser Bericht fasst die vier Einzelberichte dazu in einem Dokument zusammen.

Eine Erstbewertung beurteilt jeden Coin nach zwei Größen. Die Qualitätsnote von 0 bis 100 fasst sieben Kriterien zusammen: Bedarf außerhalb der Kryptowelt (F1), wirtschaftlicher Beleg (F2), Vorsprung vor Konkurrenten (F3), Notwendigkeit des Tokens (F4), Rückfluss des erwirtschafteten Werts an die Tokenhalter (F5), Entwicklung der Tokenmenge (F6) und Widerstandsfähigkeit (F7). Die Bewertungsnote von 0 bis 100 misst den Preis im Verhältnis zum Ertrag oder, bei Geldwerten wie Bitcoin, im Verhältnis zum durchschnittlichen Einstandspreis der Halter. Dazu kommen das Angebots-Gate, das bei stark wachsender Tokenmenge sperrt, und die Belegsicherheit von A bis D, die angibt, wie gut die Zahlen belegt sind. Aus allem folgt nach festen Regeln der Status, etwa „Satellit“ als kleinster Kaufkandidat, „Optionsliste“ für einen Kauf nur nach Einzelentscheidung oder „Kein Kandidat“.

Ein Kandidatenstatus berechtigt noch nicht zum Kauf. Vorher muss eine unabhängige Zweitprüfung den Coin blind, also ohne Kenntnis dieser Ergebnisse, nachbewerten, und beide Ergebnisse werden abgeglichen.


GLIEDERUNG

Teil 1: Gesamtergebnis, Stand vom 3. November 2026 und offene Punkte.
Teil 2: Gruppe 1 mit Osmosis, Livepeer, OpenEden, USD.AI, Scroll und Linea.
Teil 3: Axis Robotics, den am 21. Oktober 2026 neu gelisteten Markt.
Teil 4: Gruppe 2 mit Fuel, Katana, Merlin Chain, Definitive und Aevo.
Teil 5: Die fünf Coins mit Klassenfrage: XRP, Stellar, DigiByte, Verge und Ethereum Classic.
Die Einfügezeilen für den Erfassungsbogen sind hier weggelassen; sie sind in der Arbeitsfassung Version 1.2.31 eingetragen (Zeilen 104 bis 120) und im GitHub-Archiv gesichert.


TEIL 1. GESAMTERGEBNIS, STAND UND OFFENE PUNKTE

1.1 ERGEBNIS IN KÜRZE

Von den siebzehn Coins erreichen zwei den Status „Satellit“: XRP und Stellar (XLM), beide als Geldwert-Asset mit Qualitätsnote 58, Klasse C, Bewertungsnote 100 beziehungsweise 88, Belegsicherheit C und Gate ok. Auf die Optionsliste kommen Osmosis (Qualitätsnote 52), DigiByte (53), Verge (54) und Ethereum Classic (49). Elf Coins erhalten „Kein Kandidat“: Livepeer, OpenEden, USD.AI, Scroll, Linea, Axis Robotics, Fuel, Katana, Merlin Chain, Definitive und Aevo.

Das gemeinsame Muster: Fast alle Anwärter sind im Verhältnis zu ihren Erträgen günstig bewertet, scheitern aber an der Qualität. Meist kommt beim Token vom erwirtschafteten Wert wenig an (F5), die Tokenmenge wächst in den nächsten Jahren stark (F6), oder die Erträge sind zuletzt eingebrochen. Die Vorprüfung hat nur ausgeschlossen, was rechnerisch chancenlos war; über die Anlagequalität entscheidet erst die Erstbewertung.

Wiedervorlage: Satelliten und Optionsliste vierteljährlich, also am 2. Februar 2027 (XRP, Stellar, Osmosis, DigiByte, Verge, Ethereum Classic). Für „Kein Kandidat“ gibt es keine regelmäßige Wiedervorlage, nur eine Neubewertung bei Anlass.

1.2 STAND DER ZWEITPRÜFUNG VOM 3. NOVEMBER 2026

XRP: Die Zweitprüfung hat am 3. November 2026 nur ein vorläufiges Ergebnis geliefert. Sie vergab allein F4 (Note 5, wie die Erstbewertung) und ließ die übrigen Noten offen, weil das Datenpaket nur Markt- und Mengendaten enthielt; Status „unvollständig“, Belegsicherheit D, Gate offen. Die Bewertungsnote 100 für ein Geldwert-Asset hat sie bestätigt. Bis zum Abschluss gilt nach Kanon § 16 Absatz 4 der vorsichtigere Status „unvollständig“; ein Kauf ist nicht möglich. Ein Nachtrag mit Primärdaten aus dem XRP Ledger liegt seit dem 3. November 2026 vor: 31,1 Milliarden XRP in 99 Treuhandverträgen, frühestmögliche Freigabe 1 Milliarde je Monat, in den letzten dreizehn Monaten jeweils 700 Millionen wieder für 31 bis 35 Monate gesperrt. Damit stützt sich das Gate „ok“ der Erstbewertung jetzt auf Primärdaten statt auf Fachberichte.

Stellar: Die Zweitprüfung steht noch aus. Das Datenpaket wurde am 3. November 2026 um eine Blockchain-Prüfung ergänzt und als „Datenpaket_XLM_2026-11-03.zip“ neu ausgegeben; es ersetzt das Paket vom 2. November 2026. Die Blockchain-Daten bestätigen Gate ok (Abflüsse der Stiftung rund 9,8 Prozent des Umlaufs in zwölf Monaten) und F6 Note 2 (rund 12 Prozent Wachstum im Jahr).

Optionsliste: Für Osmosis, DigiByte, Verge und Ethereum Classic ist keine Zweitprüfung vorgeschrieben (Kanon § 16 Absatz 1). Ein Kauf ist nur nach A6 möglich und derzeit gesperrt, weil der Anteil außerhalb der Matrix über dem Höchstanteil von 20 Prozent liegt (A10).

1.3 WAS SICH SEIT DEN EINZELBERICHTEN GEÄNDERT HAT

Regelwerk Version 1.2.31: Auf Ihre Entscheidung vom 2. November 2026 hin gilt Kanon § 6 Absatz 3. Ein aktualisierbarer Token-Vertrag ist ein dauerhafter Ausschlussgrund, wenn eine Änderung weder an eine Zeitsperre von mindestens 48 Stunden noch an eine Abstimmung der Tokenhalter gebunden ist. Die in Teil 3, Abschnitt 3.5, beschriebene Vorlage ist damit entschieden. Für Axis Robotics steht die Prüfung nach dem neuen Absatz noch aus, weil offen ist, ob der Eigentümervertrag eine Zeitsperre hat. Am Ergebnis für Sie ändert das nichts, denn ein Kauf ist in beiden Fällen ausgeschlossen. Die fünf Coins der Klassenfrage haben eigene Blockchains und sind nicht betroffen.

Die übrigen Einzelberichte gelten unverändert. Wo sie von „Version 1.2.30“ sprechen, ist der Regelstand ihres Erstellungstags gemeint.

1.4 OFFENE PUNKTE

Erstens: Abschluss der Zweitprüfung von XRP und Zweitprüfung von Stellar, danach Abgleich und Abschlussbericht.
Zweitens: Prüfung der Token-Verträge der bisherigen Kandidaten und Bestände nach § 6 Absatz 3, zuerst POL und SKY, sowie von Axis Robotics.
Drittens: Erstbewertung der übrigen siebzehn Anwärter aus der Vorprüfung.
Viertens: Wiedervorlage der bestehenden Kandidaten aus dem Oktober vor dem 17. November 2026.
Fünftens: Vorschlag zur Fortschreibung der Betriebsdokumente: Datenpakete für Kandidaten stets mit Blockchain-Prüfung und Quellenregister; die Zweitprüfung erhebt fehlende Belege selbst, auch wenn ein Datenpaket vorliegt. Entscheidung offen.


'''
out=intro.split('\n')
for k,(t,p) in enumerate(SRC): out+=part(t,p,k+2)
out+=['','Ende des Berichts.']
txt='\n'.join(out)
txt=txt.replace('Teil 3, Abschnitt 3.5','Teil 3, Abschnitt 3.5')
open('/home/claude/work/berichte/Erstbewertungen_2026-11-02.txt','w',encoding='utf-8').write(txt)
print(len(txt))
