import re
A='/home/claude/work/fs/neu/doc/'; N='/home/claude/work/fs/v132/doc/'
def rep(s,a,b,count=1):
    k=s.count(a); assert k>=1,('fehlt',a[:90])
    if count==1: assert k==1,('mehrfach',k,a[:90])
    return s.replace(a,b)
ABS_SATZ=('Für die kommenden zwölf Monate zählen Rückkäufe, Burns und neue Sperren nur, soweit ein Vertrag oder ein Protokollmechanismus sie auslöst; '
 'freiwillige Maßnahmen einer Firma, einer Stiftung oder einer Projektkasse zählen erst, wenn sie vollzogen sind, und werden für die kommenden zwölf Monate wie geringere Abrufe nach D-04 nur vermerkt.')
# ---------------- Regelkanon
s=open(A+'Regelkanon_Version_1.2.31.txt',encoding='utf-8').read()
s=rep(s,'Version 1.2.31 vom 2. November 2026 · verbindliche Festlegungen','Version 1.2.32 vom 4. November 2026 · verbindliche Festlegungen')
s=rep(s,'geteilt durch die neu in Umlauf kommenden Token. Jeder Token wird nur einmal gezählt; jederzeit lösbares Staking ist keine Sperre.\n',
 'geteilt durch die neu in Umlauf kommenden Token. '+ABS_SATZ+' Jeder Token wird nur einmal gezählt; jederzeit lösbares Staking ist keine Sperre.\n')
s=rep(s,'jedes Signal nach A13, jeder Notfall, jeder Statuswechsel und jeder Abruffehler bei Kursdaten.\n(2)',
 'jedes Signal nach A13, jeder Notfall, jeder Statuswechsel, jeder Abruffehler bei Kursdaten, jeder Listungsabgleich mit seinem Ergebnis, jede Datenübernahme und jeder Abschluss eines Abgleichs mit der Zweitprüfung.\n(2)')
s=rep(s,'sowie eine Nachschau nach 90, 180 und 365 Tagen, bei gelöschten Aufträgen mit der Angabe, ob sie ausgeführt worden wären.\n',
 'sowie eine Nachschau nach 90, 180 und 365 Tagen, bei gelöschten Aufträgen mit der Angabe, ob sie ausgeführt worden wären. Vorgänge ohne Kursbezug, nämlich Datenübernahme, Listungsabgleich, Abruffehler und Abschluss eines Abgleichs, erhalten keine Nachschau.\n')
s=rep(s,'ÄNDERUNGSVERMERK\n\nVersion 1.2.31 vom 2. November 2026,',
 'ÄNDERUNGSVERMERK\n\nVersion 1.2.32 vom 4. November 2026, auf Entscheidungen des Anlegers vom 3. November 2026: § 11 Absatz 1 Satz 2 neu. Für die Absorptionsquote der kommenden zwölf Monate zählen Rückkäufe, Burns und neue Sperren nur, soweit ein Vertrag oder ein Protokollmechanismus sie auslöst; freiwillige Maßnahmen einer Firma, Stiftung oder Projektkasse zählen erst nach ihrem Vollzug und werden für die Prognose nur vermerkt, wie geringere Abrufe nach D-04. Anlass war ein Coin, dessen Betreiber freigegebene Treuhandmengen seit Jahren zu einem großen Teil freiwillig wieder sperrt, ohne dazu verpflichtet zu sein; Erst- und Zweitprüfung hatten das unterschiedlich gedeutet. Die Schwellen des Gates (§ 2 Absatz 1) und die Definitionen sind unverändert. § 31 Absatz 1 und 2: Listungsabgleich, Datenübernahme und Abschluss eines Abgleichs sind eigene Vorgänge im Protokoll; Vorgänge ohne Kursbezug erhalten keine Nachschau. In der Datenquellen-Verfassung sind Teil F und Teil G ergänzt: Datenpakete für Kandidaten enthalten stets die Blockchain-Prüfung und ein Quellenregister, und die Zweitprüfung erhebt Belege, die das Datenpaket nicht enthält, selbst. In der Excel-Datei zeigt das Blatt „Tranchen“ zusätzlich die nach FIFO noch gehaltene Menge je Kauf. Gewichte, Schwellen, Notenskalen, Definitionen und Statusreihenfolge sind unverändert.\n\nVersion 1.2.31 vom 2. November 2026,')
s=rep(s,'Ende des Regelkanons, Version 1.2.31.','Ende des Regelkanons, Version 1.2.32.')
open(N+'Regelkanon_Version_1.2.32.txt','w',encoding='utf-8').write(s)
# ---------------- Gesamtdarstellung
g=open(A+'Gesamtdarstellung_Version_1.2.31.txt',encoding='utf-8').read()
g=rep(g,'Version 1.2.31 vom 2. November 2026 · erklärende Darstellung zum Regelkanon Version 1.2.31','Version 1.2.32 vom 4. November 2026 · erklärende Darstellung zum Regelkanon Version 1.2.32')
g=rep(g,'Verbindlich ist der Regelkanon in der Version 1.2.31,','Verbindlich ist der Regelkanon in der Version 1.2.32,')
g=rep(g,'hier in der Version 1.2.31, ordnet','hier in der Version 1.2.32, ordnet')
g=rep(g,'Jeder Token wird nur einmal gezählt: Werden zurückgekaufte Token anschließend verbrannt, ist das ein Vorgang und nicht ein Rückkauf und zusätzlich ein Burn.\n',
 'Jeder Token wird nur einmal gezählt: Werden zurückgekaufte Token anschließend verbrannt, ist das ein Vorgang und nicht ein Rückkauf und zusätzlich ein Burn.\n'
 'Seit Version 1.2.32 gilt für die Absorption eine Klarstellung. Weil das Gate in die Zukunft blickt, zählen Rückkäufe, Burns und neue Sperren der kommenden zwölf Monate nur, wenn ein Vertrag oder ein Mechanismus des Protokolls sie auslöst, etwa eine Verbrennung, die bei jeder Transaktion automatisch geschieht. Freiwillige Maßnahmen einer Firma, einer Stiftung oder einer Projektkasse zählen erst, wenn sie tatsächlich geschehen sind; für die Vorschau werden sie nur vermerkt. Erfundenes Beispiel: Eine Firma darf jeden Monat 1 Milliarde Token aus einer Treuhand entnehmen und hat im vergangenen Jahr jeweils 700 Millionen davon freiwillig wieder für drei Jahre gesperrt. Für das Gate zählen die vollen 12 Milliarden der möglichen Entnahme; die bisherige Wiedersperrung wird vermerkt, aber nicht angerechnet, weil die Firma sie jederzeit einstellen kann.\n'
 'Begründung: Das Gate soll vor Mengen schützen, die auf den Markt kommen können. Eine freiwillige Zurückhaltung ist wirtschaftlich dasselbe wie eine angekündigte geringere Entnahme, und die zählt nach D-04 ebenfalls nicht. Ein Mechanismus im Protokoll dagegen läuft weiter, solange niemand die Regeln ändert.\n')
g=rep(g,'Zu jedem Eintrag gehören der Kurs am Tag der Entscheidung und eine Nachschau nach 90, 180 und 365 Tagen, bei gelöschten Aufträgen mit der Angabe, ob sie ausgeführt worden wären.',
 'Zu jedem Eintrag gehören der Kurs am Tag der Entscheidung und eine Nachschau nach 90, 180 und 365 Tagen, bei gelöschten Aufträgen mit der Angabe, ob sie ausgeführt worden wären. Ebenfalls festgehalten werden jeder Listungsabgleich mit seinem Ergebnis und jede Übernahme von Daten aus dem Bitvavo-Export; sie haben keinen Kursbezug und erhalten deshalb, wie auch Abruffehler und der Abschluss eines Abgleichs, keine Nachschau. Im Blatt „Tranchen“ zeigt eine eigene Spalte, welche Menge aus jedem Kauf nach der Reihenfolge „zuerst angeschafft, zuerst veräußert“ noch gehalten wird; das ist die Grundlage für Haltefristen und Einstand.')
g=rep(g,'Was sie nicht selbst abrufen kann, bleibt als nicht bestätigt gekennzeichnet.\n',
 'Was sie nicht selbst abrufen kann, bleibt als nicht bestätigt gekennzeichnet.\n'
 'Seit Version 1.2.32 gilt zweierlei ausdrücklich. Das Datenpaket für einen Kandidaten enthält stets auch die Prüfung auf der Blockchain, etwa Treuhand- und Stiftungsbestände, Freigaben und Vertragsrechte, und ein Quellenregister mit den Primärquellen zu Bedarf, Burggraben und Widerstandsfähigkeit. Und die Zweitprüfung erhebt Belege, die das Datenpaket nicht enthält, selbst an Primärquellen; sie lässt eine Note nicht einfach offen, sondern vergibt sie nach dem belegten Stand und begründet einzeln, wenn ein Kriterium auch dann nicht beurteilbar bleibt.\n'
 'Begründung: Ein Datenpaket nur mit Kursen und Mengen lässt die Zweitprüfung bei den Qualitätskriterien ohne Grundlage; das führte einmal dazu, dass sechs von sieben Noten offen blieben und der Coin nur wegen fehlender Unterlagen als unvollständig galt.\n')
g=rep(g,'Absorptionsquote = (Rückkauf plus Burn plus neue Sperren von mindestens zwölf Monaten, jeder Token nur einmal gezählt) geteilt durch neu in Umlauf kommende Token.',
 'Absorptionsquote = (Rückkauf plus Burn plus neue Sperren von mindestens zwölf Monaten, jeder Token nur einmal gezählt) geteilt durch neu in Umlauf kommende Token. Für die kommenden zwölf Monate zählen nur Maßnahmen, die ein Vertrag oder ein Protokollmechanismus auslöst; freiwillige Maßnahmen einer Firma, Stiftung oder Projektkasse werden mit ihrer bisherigen Höhe nur vermerkt (Regelkanon § 11 Absatz 1).')
g=rep(g,'Die verbindlichen Festlegungen stehen im Regelkanon Version 1.2.31.','Die verbindlichen Festlegungen stehen im Regelkanon Version 1.2.32.')
g=rep(g,'Q-01 bis Q-23 im Wortlaut der Datenquellen-Verfassung Version 1.2.31.','Q-01 bis Q-23 im Wortlaut der Datenquellen-Verfassung Version 1.2.32.')
g=rep(g,'Diese Version 1.2.31 vom 2. November 2026 ersetzt die Version 1.2.30.',
 'Diese Version 1.2.32 vom 4. November 2026 ersetzt die Version 1.2.31. Neu ist auf Entscheidung des Anlegers eine Klarstellung zum Angebots-Gate: Künftige Rückkäufe, Burns und Sperren zählen in der Absorption nur, wenn ein Vertrag oder das Protokoll sie auslöst; freiwillige Maßnahmen zählen erst nach ihrem Vollzug (Kapitel 8). Dazu kommen Verbesserungen des Verfahrens: Datenpakete für Kandidaten enthalten stets die Blockchain-Prüfung und ein Quellenregister, die Zweitprüfung erhebt fehlende Belege selbst (Kapitel 9), und das Protokoll kennt den Listungsabgleich als eigenen Vorgang (Kapitel 14). Gewichte, Schwellen, Notenskalen und Definitionen sind unverändert.\nDie Version 1.2.31 vom 2. November 2026 ersetzte die Version 1.2.30.')
open(N+'Gesamtdarstellung_Version_1.2.32.txt','w',encoding='utf-8').write(g)
# ---------------- Datenquellen-Verfassung
v=open(A+'Datenquellen-Verfassung_Version_1.2.31.txt',encoding='utf-8').read()
v=rep(v,'Version 1.2.31 vom 2. November 2026 · Baustein des Regelwerks','Version 1.2.32 vom 4. November 2026 · Baustein des Regelwerks')
v=rep(v,'Der Regelkanon in der Version 1.2.31 verweist','Der Regelkanon in der Version 1.2.32 verweist')
v=rep(v,'keine Ergebnisse der Erstbewertung im Paket; eingefrorener Stand mit Prüfsumme.',
 'keine Ergebnisse der Erstbewertung im Paket; eingefrorener Stand mit Prüfsumme; für jeden Kandidaten die Blockchain-Prüfung aus dem sechsten Schritt (Gesamtmenge, Treuhand-, Stiftungs- und Firmenbestände, Freigaben und neue Sperren der letzten zwölf Monate, bei Token mit Vertrag die Vertragsrechte nach Regelkanon § 6 Absatz 3) und ein Quellenregister mit den Primärquellen zu F1, F3 und F7, beides ohne Bewertung. Fehlt beides, geht das Paket nicht an die Zweitprüfung.')
v=rep(v,'Zweitens alle entscheidungsrelevanten Werte der Kandidaten: eigene Kontrolle an der Primärquelle oder unabhängige Nachrechnung.',
 'Zweitens alle entscheidungsrelevanten Werte der Kandidaten: eigene Kontrolle an der Primärquelle oder unabhängige Nachrechnung. Belege, die das Datenpaket nicht enthält, etwa zu Marktgröße, tatsächlicher Nutzung, Wettbewerb, Adressverteilung oder Validatoren, erhebt die Zweitprüfung selbst an Primärquellen und kennzeichnet sie nach Teil D; Unsicherheit bildet sie über die Belegsicherheit ab, nicht durch offene Noten. Bleibt ein Kriterium trotz eigener Erhebung nicht beurteilbar, begründet sie das einzeln.')
v=rep(v,'Version 1.2.31 vom 2. November 2026, ohne Auswirkung auf Noten: gemeinsame Version mit dem Regelkanon,',
 'Version 1.2.32 vom 4. November 2026: gemeinsame Version mit dem Regelkanon, der in § 11 Absatz 1 die Absorption der kommenden zwölf Monate auf vertraglich oder protokollseitig ausgelöste Maßnahmen begrenzt. Teil F: Datenpakete für Kandidaten enthalten stets die Blockchain-Prüfung und ein Quellenregister. Teil G: Die Zweitprüfung erhebt Belege, die das Datenpaket nicht enthält, selbst. Die Datenregeln Q-01 bis Q-23 sind unverändert.\nVersion 1.2.31 vom 2. November 2026, ohne Auswirkung auf Noten: gemeinsame Version mit dem Regelkanon,')
v=rep(v,'Ende der Datenquellen-Verfassung, Version 1.2.31.','Ende der Datenquellen-Verfassung, Version 1.2.32.')
open(N+'Datenquellen-Verfassung_Version_1.2.32.txt','w',encoding='utf-8').write(v)
# ---------------- Betriebsdokument Erstprüfung
e=open(A+'Betriebsdokument_Erstpruefung_Version_1.2.31.txt',encoding='utf-8').read()
head,tail=e.split('\nANHANG 4. LÖSCHLISTE')
head=head.replace('Version 1.2.31 vom 2. November 2026','Version 1.2.32 vom 4. November 2026').replace('Version 1.2.31','Version 1.2.32').replace('Version_1.2.31','Version_1.2.32')
head=rep(head,'Rohwerte mit Quelle, Abrufzeit, Bezugszeitraum und Kennzeichen, eingefroren mit Prüfsumme, ohne Klasse, Noten, Status oder sonstige Ergebnisse. Als Textdatei, die ich ins ChatGPT-Projekt hochladen kann.',
 'Rohwerte mit Quelle, Abrufzeit, Bezugszeitraum und Kennzeichen, eingefroren mit Prüfsumme, ohne Klasse, Noten, Status oder sonstige Ergebnisse; dazu die Blockchain-Prüfung (Gesamtmenge, Treuhand-, Stiftungs- und Firmenbestände, Freigaben und neue Sperren der letzten zwölf Monate, Vertragsrechte nach Kanon § 6 Abs. 3) und ein Quellenregister mit den Primärquellen zu F1, F3 und F7 (Verfassung Teil F). Als ZIP-Datei mit Textdatei und Rohdaten, die ich im Gespräch anhänge.')
head=rep(head,'Kennzeichen je Wert, Konsistenzprüfungen (Q-16), Stand einfrieren; das Datenpaket enthält keine Klasse, keine Noten und keinen Status.',
 'Kennzeichen je Wert, Konsistenzprüfungen (Q-16), Stand einfrieren; das Datenpaket enthält keine Klasse, keine Noten und keinen Status. Für Kandidaten stets mit Blockchain-Prüfung und Quellenregister nach Teil F der Verfassung; ohne beides geht kein Paket an die Zweitprüfung. Zum Anhang gehört der Auftragstext nach Prompt B 1 des Betriebsdokuments Zweitprüfung mit Coin-Angaben und Prüfsumme.')
head=rep(head,'- Rückkauf und Burn derselben Token in der Absorptionsquote doppelt gezählt?',
 '- Rückkauf und Burn derselben Token in der Absorptionsquote doppelt gezählt? Freiwillige Maßnahmen einer Firma, Stiftung oder Projektkasse als künftige Absorption angerechnet? (Kanon § 11 Abs. 1 Satz 2)\n- Datenpaket für einen Kandidaten mit Blockchain-Prüfung und Quellenregister? (Verfassung Teil F)')
head=rep(head,'16. Geplante Aufgaben: wöchentlich Gültigkeitsprüfung und Listungsabgleich (',
 '16. Geplante Aufgaben: wöchentlich Gültigkeitsprüfung und Listungsabgleich (jeder Listungsabgleich mit Ergebnis als Protokollzeile „Listungsabgleich“, Kanon § 31 Abs. 1; ')
tail=tail.replace('Version 1.2.31','Version 1.2.32')
tail=rep(tail,'In beiden Projekten, im Ordner „Aktuell“ und in Notion löschen oder nach „Archiv“ verschieben:\n',
 'In beiden Projekten, im Ordner „Aktuell“ und in Notion löschen oder nach „Archiv“ verschieben:\n- alle Dateien der Version 1.2.31 vom 2. November 2026: Regelkanon, Gesamtdarstellung, Datenquellen-Verfassung, Arbeitsfassung, Prüffassung und beide Betriebsdokumente, ebenso die Projektanweisungen der Version 1.2.31 in beiden Projekten;\n')
e=head+'\nANHANG 4. LÖSCHLISTE'+tail
open(N+'Betriebsdokument_Erstpruefung_Version_1.2.32.txt','w',encoding='utf-8').write(e)
# ---------------- Betriebsdokument Zweitprüfung
z=open(A+'Betriebsdokument_Zweitpruefung_Version_1.2.31.txt',encoding='utf-8').read()
z=rep(z,'alle Fassungen von Regelkanon, Gesamtdarstellung und Datenquellen-Verfassung vor Version 1.2.31, die Prüffassungen Version 1.2.23 bis 1.2.30','alle Fassungen von Regelkanon, Gesamtdarstellung und Datenquellen-Verfassung vor Version 1.2.32, die Prüffassungen Version 1.2.23 bis 1.2.31')
z=z.replace('Version 1.2.31 vom 2. November 2026','Version 1.2.32 vom 4. November 2026').replace('Version 1.2.31','Version 1.2.32').replace('Version_1.2.31','Version_1.2.32')
z=rep(z,'Weicht ein eigener Wert vom Datenpaket ab, nenne beide und entscheide im ungünstigeren Fall (Q-06).',
 'Weicht ein eigener Wert vom Datenpaket ab, nenne beide und entscheide im ungünstigeren Fall (Q-06). Belege, die das Datenpaket nicht enthält (etwa zu Marktgröße, tatsächlicher Nutzung, Wettbewerb, Adressverteilung, Validatoren), erhebst du auch dann selbst an Primärquellen und kennzeichnest sie, wenn ein Datenpaket vorliegt. Vergib alle sieben Noten nach dem belegten Zustand (§ 7 Absatz 1); was nicht belegt ist, senkt die Note, Unsicherheit bildest du über die Belegsicherheit ab. Bleibt ein Kriterium trotz eigener Erhebung nicht beurteilbar, begründe das einzeln.')
z=rep(z,'Bitte zuerst die Ergebniszeile mit 12 Werten im Kopierblock, dann Begründungen, Bewertungsnote mit Rechenweg, Angebot, Prüfprotokoll und Beobachtungen.\n',
 'Ergänzend zum Prüfumfang:\n1. Vergib alle sieben Noten nach dem belegten Zustand (§ 7 Absatz 1); Belege, die das Datenpaket nicht enthält, erhebst du selbst an Primärquellen und kennzeichnest sie nach Teil D der Verfassung.\n2. Lege die Klasse nach § 5 Absatz 1 fest und begründe sie. Kommen zwei Klassen in Betracht, nenne das Ergebnis für beide und entscheide dich für eine.\n3. Bestimme das Gate nach § 11 Absatz 2 in der dort festgelegten Reihenfolge, mit dem Zuwachs nach D-04, D-11 und D-14 und der Absorptionsquote nach § 11 Absatz 1.\n4. Bestimme F6 nach D-08 und begründe, welche Bestände du zum heutigen Umlauf nach D-14 rechnest.\nBitte zuerst die Ergebniszeile mit 12 Werten im Kopierblock, dann Begründungen, Bewertungsnote mit Rechenweg, Angebot, Prüfprotokoll und Beobachtungen.\n')
open(N+'Betriebsdokument_Zweitpruefung_Version_1.2.32.txt','w',encoding='utf-8').write(z)
# Länge Teil A
ta=z.split('TEIL A. PROJEKTANWEISUNG FÜR DAS CHATGPT-PROJEKT\n',1)[1].split('TEIL B.')[0]
body=ta.strip().split('\n\n',1)[1].strip()
print('Teil A Zweitprüfung Zeichen:',len(body))
print('ok')
