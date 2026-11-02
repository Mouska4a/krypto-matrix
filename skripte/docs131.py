import re
A='/home/claude/work/fs/alt/'; N='/home/claude/work/fs/neu/'
def rep(s,a,b,count=1):
    k=s.count(a)
    assert k>=1, ('fehlt',a[:80])
    if count==1: assert k==1, ('mehrfach',k,a[:80])
    return s.replace(a,b)
# ---------- Regelkanon
s=open(A+'Regelkanon_Version_1.2.30.txt').read()
s=rep(s,'Version 1.2.30 vom 1. November 2026 · verbindliche Festlegungen','Version 1.2.31 vom 2. November 2026 · verbindliche Festlegungen')
s=rep(s,'(2) Der Grund wird angegeben und belegt. Eine zuschaltbare Privatsphäre-Funktion allein ist kein Ausschlussgrund nach a; maßgeblich ist der konkret nachgewiesene Konflikt mit dem Handel in der Europäischen Union.\n',
'(2) Der Grund wird angegeben und belegt. Eine zuschaltbare Privatsphäre-Funktion allein ist kein Ausschlussgrund nach a; maßgeblich ist der konkret nachgewiesene Konflikt mit dem Handel in der Europäischen Union.\n'
'(3) Ein einseitig änderbares Token-Recht nach Absatz 1 Buchstabe c liegt auch vor, wenn der Vertrag des Tokens aktualisierbar ist, seine Programmlogik also ausgetauscht werden kann, und diese Änderung weder an eine Zeitsperre von mindestens 48 Stunden noch an eine Abstimmung der Tokenhalter gebunden ist. Als Abstimmung der Tokenhalter gilt auch die Entscheidung eines Gremiums, das von den Tokenhaltern gewählt wird und von ihnen abgewählt werden kann. Ein Prägerecht bis zu einer vertraglich festen Höchstmenge ohne Austausch der Programmlogik fällt nicht darunter; es wird über das Angebots-Gate und F6 erfasst (D-04, D-17). Eigenständige Coins ohne Token-Vertrag fallen nicht darunter; Änderungen ihres Protokolls bewertet F7. Nachgewiesen wird am Vertrag im Blockchain-Explorer: Aktualisierbarkeit, Eigentümer oder Berechtigte, Zeitsperre und Abstimmungsweg. Die Mindestdauer der Zeitsperre ist ein Startwert (§ 35).\n')
s=rep(s,'die Bedingungen von A12 und A13; die Schwelle für Insider-Transfers; die Wirkung von RS90; die Bedingungen von A6.','die Bedingungen von A12 und A13; die Schwelle für Insider-Transfers; die Wirkung von RS90; die Bedingungen von A6; die Mindestdauer der Zeitsperre nach § 6 Absatz 3.')
s=rep(s,'ÄNDERUNGSVERMERK\n\nVersion 1.2.30 vom 1. November 2026:','ÄNDERUNGSVERMERK\n\nVersion 1.2.31 vom 2. November 2026, auf Entscheidung des Anlegers vom selben Tag: § 6 Absatz 3 neu. Ein aktualisierbarer Token-Vertrag ist ein einseitig änderbares Token-Recht und damit ein dauerhafter Ausschlussgrund nach § 6 Absatz 1 Buchstabe c, wenn die Änderung weder an eine Zeitsperre von mindestens 48 Stunden noch an eine Abstimmung der Tokenhalter gebunden ist; ein von den Tokenhaltern gewähltes und abwählbares Gremium gilt als Abstimmung; ein Prägerecht bis zur festen Höchstmenge ohne Austausch der Programmlogik wirkt nur über Gate und F6. Die Mindestdauer ist ein Startwert (§ 35). Anlass war ein Token, dessen Eigentümer die Programmlogik jederzeit austauschen und neue Token prägen kann. Bisher war offen, ob ein solches Recht unter § 6 Absatz 1 Buchstabe c fällt. Gewichte, Schwellen, Notenskalen, Definitionen und Statusreihenfolge sind unverändert; § 6 gehört nicht zum eingefrorenen Kern nach § 2 Absatz 1. In der Excel-Datei wurde die Kapazität des Erfassungsbogens erweitert; die Rechenweise ist unverändert.\n\nVersion 1.2.30 vom 1. November 2026:')
s=rep(s,'Ende des Regelkanons, Version 1.2.30.','Ende des Regelkanons, Version 1.2.31.')
assert '1.2.31' in s
open(N+'Regelkanon_Version_1.2.31.txt','w').write(s)
# ---------- Gesamtdarstellung
g=open(A+'Gesamtdarstellung_Version_1.2.30.txt').read()
g=rep(g,'Version 1.2.30 vom 1. November 2026 · erklärende Darstellung zum Regelkanon Version 1.2.30','Version 1.2.31 vom 2. November 2026 · erklärende Darstellung zum Regelkanon Version 1.2.31')
g=rep(g,'Verbindlich ist der Regelkanon in der Version 1.2.30,','Verbindlich ist der Regelkanon in der Version 1.2.31,')
g=rep(g,'hier in der Version 1.2.30, ordnet','hier in der Version 1.2.31, ordnet')
g=rep(g,'nachgewiesener Betrug oder Marktmanipulation durch das Team sowie eine Widerstandsfähigkeit F7 von null.\n',
'nachgewiesener Betrug oder Marktmanipulation durch das Team sowie eine Widerstandsfähigkeit F7 von null.\n'
'Was „einseitig änderbare Token-Rechte“ bei Token mit eigenem Vertrag heißt, ist seit Version 1.2.31 genauer bestimmt. Viele Token-Verträge lassen sich aktualisieren: Ihr Eigentümer kann die Programmlogik gegen eine neue austauschen und damit nachträglich alles ändern, auch die Höchstmenge, Sperren oder Gebühren. Ein solcher Vertrag ist ein Ausschlussgrund, wenn der Austausch weder an eine Zeitsperre von mindestens 48 Stunden noch an eine Abstimmung der Tokenhalter gebunden ist. Eine Zeitsperre bedeutet, dass eine beschlossene Änderung erst nach Ablauf einer Frist wirksam wird; in dieser Zeit können Halter reagieren und verkaufen. Als Abstimmung gilt auch die Entscheidung eines Gremiums, das die Tokenhalter wählen und abwählen können, etwa eines Sicherheitsrats für Notfälle. Ein bloßes Recht, neue Token bis zu einer festen Höchstmenge zu prägen, ist dagegen kein Ausschlussgrund; es wirkt wie eine Freigabe und wird im Angebots-Gate und in F6 mit der vollen möglichen Menge gezählt. Eigenständige Coins wie Bitcoin haben keinen Token-Vertrag; Änderungen ihres Protokolls brauchen die Zustimmung der Netzbetreiber und werden in F7 bewertet. Erfundenes Beispiel: Ein Token liegt in einem aktualisierbaren Vertrag, dessen Eigentümer eine Mehrfachunterschrift aus vier von sechs Mitarbeitern des Projekts ist, ohne Zeitsperre. Das Team könnte morgen eine neue Logik einspielen, die die Höchstmenge aufhebt. Das ist ein Ausschlussgrund. Läge dieselbe Mehrfachunterschrift hinter einer Zeitsperre von sieben Tagen, wäre es keiner; die Abhängigkeit vom Team würde dann in F7 bewertet.\n'
'Begründung: Ein Recht, die Regeln des Tokens jederzeit und ohne Vorwarnung zu ändern, macht jede Bewertung der Tokenomics hinfällig, denn bewertet würde ein Vertrag, der morgen ein anderer sein kann. Die Zeitsperre ist ein üblicher Schutz; 48 Stunden reichen an einem liquiden Markt, um zu verkaufen. Der Wert ist ein Startwert und wird mit dem Protokoll überprüft.\n')
g=rep(g,'die Positionsgrenzen in Grundeinheiten, der Höchstanteil außerhalb der Matrix und die Schwelle für Insider-Transfers von 1 Prozent in 30 Tagen.','die Positionsgrenzen in Grundeinheiten, der Höchstanteil außerhalb der Matrix, die Schwelle für Insider-Transfers von 1 Prozent in 30 Tagen und die Mindestdauer der Zeitsperre von 48 Stunden für aktualisierbare Token-Verträge.')
g=rep(g,'Die verbindlichen Festlegungen stehen im Regelkanon Version 1.2.30.','Die verbindlichen Festlegungen stehen im Regelkanon Version 1.2.31.')
g=rep(g,'Q-01 bis Q-23 im Wortlaut der Datenquellen-Verfassung Version 1.2.30.','Q-01 bis Q-23 im Wortlaut der Datenquellen-Verfassung Version 1.2.31.')
g=rep(g,'Diese Version 1.2.30 vom 1. November 2026 ersetzt die Version 1.2.29 und ändert keine Regel.',
'Diese Version 1.2.31 vom 2. November 2026 ersetzt die Version 1.2.30. Neu ist eine Klarstellung der Ausschlussgründe auf Entscheidung des Anlegers: Ein aktualisierbarer Token-Vertrag, dessen Programmlogik ohne Zeitsperre von mindestens 48 Stunden und ohne Abstimmung der Tokenhalter ausgetauscht werden kann, ist ein Ausschlussgrund (Kapitel 8). Gewichte, Schwellen, Notenskalen und Definitionen sind unverändert.\nDie Version 1.2.30 vom 1. November 2026 ersetzte die Version 1.2.29 und änderte keine Regel.')
open(N+'Gesamtdarstellung_Version_1.2.31.txt','w').write(g)
# ---------- Datenquellen-Verfassung
v=open(A+'Datenquellen-Verfassung_Version_1.2.30.txt').read()
v=rep(v,'Version 1.2.30 vom 1. November 2026 · Baustein des Regelwerks','Version 1.2.31 vom 2. November 2026 · Baustein des Regelwerks')
v=rep(v,'Der Regelkanon in der Version 1.2.30 verweist','Der Regelkanon in der Version 1.2.31 verweist')
v=rep(v,'- Zweck: Verträge, Kontostände, Transaktionen und Ereignisse auf Ethereum','- Zweck: Verträge, Kontostände, Transaktionen und Ereignisse auf Ethereum, auch die Aktualisierbarkeit eines Token-Vertrags, sein Eigentümer, eine Zeitsperre und die Prägerechte nach Regelkanon § 6 Absatz 3,')
v=rep(v,'Version 1.2.30 vom 1. November 2026, ohne Auswirkung auf Noten: gemeinsame Version mit Regelkanon und Excel-Datei; die Datenregeln Q-01 bis Q-23 sind unverändert.\n',
'Version 1.2.30 vom 1. November 2026, ohne Auswirkung auf Noten: gemeinsame Version mit Regelkanon und Excel-Datei; die Datenregeln Q-01 bis Q-23 sind unverändert.\nVersion 1.2.31 vom 2. November 2026, ohne Auswirkung auf Noten: gemeinsame Version mit dem Regelkanon, der in § 6 Absatz 3 aktualisierbare Token-Verträge ohne Zeitsperre und ohne Abstimmung als Ausschlussgrund bestimmt; in C 7 ist der Zweck des Explorers um diese Vertragsrechte ergänzt. Die Datenregeln Q-01 bis Q-23 sind unverändert.\n')
v=rep(v,'Ende der Datenquellen-Verfassung, Version 1.2.30.','Ende der Datenquellen-Verfassung, Version 1.2.31.')
open(N+'Datenquellen-Verfassung_Version_1.2.31.txt','w').write(v)
# ---------- Betriebsdokument Erstprüfung
e=open(A+'Betriebsdokument_Erstpruefung_Version_1.2.30.txt').read()
marker='ANHANG 4. LÖSCHLISTE'
head,tail=e.split('\nANHANG 4. LÖSCHLISTE')
head=head.replace('Version 1.2.30 vom 1. November 2026','Version 1.2.31 vom 2. November 2026').replace('Version 1.2.30','Version 1.2.31').replace('Version_1.2.30','Version_1.2.31')
head=rep(head,'- Identität geprüft (Kürzel, CoinGecko-Kennung, Netz, Vertrag;','- Token-Vertrag geprüft (Kanon § 6 Abs. 3): aktualisierbar? Eigentümer oder Berechtigte, Zeitsperre von mindestens 48 Stunden, Abstimmung der Tokenhalter oder gewähltes Gremium; Prägerecht bis Höchstmenge nur in Gate und F6; Beleg im Explorer mit Blockhöhe?\n- Identität geprüft (Kürzel, CoinGecko-Kennung, Netz, Vertrag;')
head=rep(head,'16. Geplante Aufgaben: wöchentlich Gültigkeitsprüfung und Listungsabgleich,','16. Geplante Aufgaben: wöchentlich Gültigkeitsprüfung und Listungsabgleich (der Listungsabgleich ist seit 2. November 2026 als geplante Aufgabe eingerichtet, montags 7:47 Uhr, Skript und Stände im Archiv krypto-matrix unter datenstaende/listung),')
tail=tail.replace('Version 1.2.30','Version 1.2.31')
tail=rep(tail,'In beiden Projekten, im Ordner „Aktuell“ und in Notion löschen oder nach „Archiv“ verschieben:\n','In beiden Projekten, im Ordner „Aktuell“ und in Notion löschen oder nach „Archiv“ verschieben:\n- alle Dateien der Version 1.2.30 vom 1. November 2026: Regelkanon, Gesamtdarstellung, Datenquellen-Verfassung, Arbeitsfassung, Prüffassung und beide Betriebsdokumente, ebenso die Projektanweisungen der Version 1.2.30 in beiden Projekten;\n')
e=head+'\nANHANG 4. LÖSCHLISTE'+tail
open(N+'Betriebsdokument_Erstpruefung_Version_1.2.31.txt','w').write(e)
# ---------- Betriebsdokument Zweitprüfung
z=open(A+'Betriebsdokument_Zweitpruefung_Version_1.2.30.txt').read()
z=rep(z,'alle Fassungen von Regelkanon, Gesamtdarstellung und Datenquellen-Verfassung vor Version 1.2.30, die Prüffassungen Version 1.2.23 bis 1.2.29','alle Fassungen von Regelkanon, Gesamtdarstellung und Datenquellen-Verfassung vor Version 1.2.31, die Prüffassungen Version 1.2.23 bis 1.2.30')
z=z.replace('Version 1.2.30 vom 1. November 2026','Version 1.2.31 vom 2. November 2026').replace('Version 1.2.30','Version 1.2.31').replace('Version_1.2.30','Version_1.2.31')
z=rep(z,'Gib keine Kauf- oder Verkaufsempfehlung.\n','Gib keine Kauf- oder Verkaufsempfehlung. Bei Token mit eigenem Vertrag prüfe im Explorer, ob der Vertrag aktualisierbar ist, wer ihn ändern darf und ob eine Zeitsperre von mindestens 48 Stunden oder eine Abstimmung der Tokenhalter vorgeschaltet ist (§ 6 Absatz 3).\n')
z=rep(z,'Der Text hat rund 5.600 Zeichen;','Der Text hat rund 5.900 Zeichen;')
open(N+'Betriebsdokument_Zweitpruefung_Version_1.2.31.txt','w').write(z)
print('ok')
