import re,json
files=['/home/claude/work/eb/Einfuegezeilen_Erstbewertung_Gruppe1_2026-11-02.txt','/home/claude/work/eb2/Erstbewertung_Gruppe2_2026-11-02.txt','/home/claude/work/eb3/Erstbewertung_Klassenfrage_2026-11-02.txt']
D={}
for f in files:
    sec=None
    for line in open(f):
        line=line.rstrip('\n')
        if line.startswith('Block A bis M'): sec='AM'; continue
        if line.startswith('Spalte Q') or line.startswith('Spalten Q'): sec='QT'; continue
        if line.startswith('Block X bis AD'): sec='XAD'; continue
        if line.startswith('Block AF'): sec=None; continue
        if line.startswith('Block AL bis AX'): sec='ALAX'; continue
        if not line.strip() or line.startswith('Erwartete') or line.startswith('Hinweis'): 
            if sec in('ALAX','XAD','QT','AM') and not line.strip(): sec=sec
            continue
        p=line.split('\t')
        if sec=='AM' and len(p)==13: D.setdefault(p[0],{})['AM']=p
        elif sec=='QT' and len(p)>=2 and p[1].startswith('Q:'):
            D.setdefault(p[0],{})['Q']=p[1][2:].strip(); D[p[0]]['T']=p[2][2:].strip()
        elif sec=='XAD' and len(p)>=2: D.setdefault(p[0],{})['XAD']=(p[1:]+['']*7)[:7]
        elif sec=='ALAX' and len(p)>=2: D.setdefault(p[0],{})['ALAX']=(p[1:]+['']*13)[:13]
# AXIS manuell
D['AXIS']={'AM':'AXIS	Axis Robotics	Compute / KI / DePIN	nein	ja	02.11.2026	4	1	1	1	0	0	1'.split('\t'),'Q':'leer','T':'leer',
 'XAD':['C','Umsatz nicht belegt; Freigabeplan nur aus zweiter Hand; Eigentümervertrag nicht geprüft','0,165','1,52','0','Monatsraten ab 11/2026 rund 20 Mio. AXIS (Ökosystem); gesamter Bestand durch Mehrfachunterschrift jederzeit abziehbar',''],
 'ALAX':['Daten für physische künstliche Intelligenz','Zahlende Abnehmer der Daten; Abgabe der Eigentümerrechte','Erste belegte Umsätze; Änderung der Eigentümerrechte','','F1 Robotik-Trainingsdaten, großer wachsender Markt; F3 kein Vorsprung belegt; F7 aktualisierbarer Vertrag mit Prägerecht des Eigentümers (Basescan)','Claude, Neuzugang Q-18','Umsatz nicht gelistet; Zuteilung S/E; Vertragsrechte P/V; Umlauf M/E','','','','keine','stabil','']}
for k,v in D.items(): print(k, sorted(v.keys()), v.get('Q'), v.get('T'))
json.dump(D,open('/home/claude/work/fs/neu/coins22.json','w'),ensure_ascii=False,indent=0)
print(len(D))
