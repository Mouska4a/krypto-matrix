import json
p='/home/claude/work/vp/ergebnis2.json'; o=json.load(open(p)); FX=1.1216
KM='Bei DefiLlama kein Ertrag auffindbar (Kennung, Kürzel und Name geprüft). Ohne Hauptkennzahl keine Bewertungsnote (§ 9 Absatz 4); derzeit höchstens „Bewertung ausstehend“. Vorläufig: Quellen außerhalb DefiLlama nicht abgefragt.'
o['MASK'].update(ergebnis='kein messbarer Ertrag',typ=None,klasse='',quellen=[],mult_upper=None,mult_metric=None,schwelle=None,grund=KM+' Der Namenstreffer „Nullmask“ ist ein anderes Projekt als Mask Network und wurde verworfen (Q-01).')
o['TREE']['quellen']=['Treehouse Protocol (DOR)']; o['TREE']['grund']='Der Namenstreffer „Tree News“ ist ein anderes Projekt und wurde verworfen (Q-01). '
o['GAS'].update(ergebnis='Daten klären',quellen=[],grund='Bitvavo führt den Gas-Token des Neo-Netzes; der Treffer „Gas (Gaming)“ bei DefiLlama ist ein anderes Projekt (Q-01). Gebühren des Neo-Netzes sind bei DefiLlama nicht erfasst; Klasse und Ertragszuordnung klären.')
g=o['G']; fees=25005.84/FX
g.update(typ='Plattform',klasse='Plattform',quellen=['Gravity by Galxe (Chain)'],fees=fees,rev=None,hold=None,mult_upper=g['fdv']/fees,mult_metric=g['fdv']/fees,schwelle=400,ergebnis='scheidet aus (robust)',grund='Zuordnung über die Kette „Gravity by Galxe“ (Gas-Token G); der Namenstreffer „Gravity Finance“ ist ein anderes Projekt und wurde verworfen. ')
for s,pid,nm,note in [('MIOTA','miota-iota','IOTA','Bei DefiLlama nur das Nebennetz „IOTA EVM“ mit rund 830 € Gebühren im Jahr; das Hauptnetz ist nicht erfasst.'),('LUNA','luna-terra','Terra Classic',''),('LUNA2','luna-terra-v2','Terra',''),('CROSS','cross-cross','ONEchain','')]:
    o[s].update(ident='belegt',pap=pid,ergebnis='kein messbarer Ertrag',grund=f'Identität über Name und Kurs belegt ({nm}). '+KM+(' '+note if note else ''))
o['DATAIP']['grund']='Identität nicht eindeutig: Zwei Einträge mit dem Kürzel DATA (Streamr und Data Network) liegen beide innerhalb von 1 % des Bitvavo-Kurses (Q-01).'
o['FLOCK']['grund']='Ertrag bei DefiLlama vorhanden (FLock.io, rund 240.000 € in 365 Tagen), aber keine Mengenangabe bei CoinPaprika; voll verwässerte Bewertung nicht bestimmbar.'
o['XVG']['grund']='Klassenfrage Geldwert vorab festgelegt; Coin Metrics liefert für Verge derzeit keinen MVRV. Ersatz nach § 5 Absatz 3: Kurs zum 200-Wochen-Durchschnitt, in der Erstbewertung zu erheben.'
json.dump(o,open(p,'w'),indent=1,ensure_ascii=False)
import collections; print(collections.Counter(r['ergebnis'] for r in o.values()))
