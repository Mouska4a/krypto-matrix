#!/usr/bin/env python3
"""Wöchentlicher Listungsabgleich nach Q-18 (Regelwerk Version 1.2.31).
Lädt die Bitvavo-Märkte und -Assets, vergleicht die Euro-Märkte mit dem jüngsten Stand in
datenstaende/listung/, schreibt neuen Stand, Prüfsummen und einen Bericht. Keine Schlüssel, keine Aufträge."""
import json, glob, os, sys, hashlib, datetime, urllib.request
BASE=os.path.join(os.path.dirname(__file__),'..','datenstaende','listung')
now=datetime.datetime.now(datetime.UTC); tag=now.strftime('%Y-%m-%d')
def get(u):
    for i in range(3):
        try:
            with urllib.request.urlopen(u,timeout=60) as r: return r.read()
        except Exception as e: err=e
    raise SystemExit(f'Abruffehler {u}: {err}')
raw_m=get('https://api.bitvavo.com/v2/markets'); raw_a=get('https://api.bitvavo.com/v2/assets')
prev=sorted(f for f in glob.glob(os.path.join(BASE,'bitvavo_markets_*.json')) if tag not in f)
if not prev: raise SystemExit('Kein früherer Stand gefunden')
old=json.load(open(prev[-1])); old_a={x['symbol']:x for x in json.load(open(prev[-1].replace('markets','assets')))}
open(os.path.join(BASE,f'bitvavo_markets_{tag}.json'),'wb').write(raw_m); open(os.path.join(BASE,f'bitvavo_assets_{tag}.json'),'wb').write(raw_a)
new=json.loads(raw_m); new_a={x['symbol']:x for x in json.loads(raw_a)}
E1={x['base']:x for x in old if x['quote']=='EUR'}; E2={x['base']:x for x in new if x['quote']=='EUR'}
held=set(l.strip() for l in open(os.path.join(BASE,'bestaende_kuerzel.txt')) if l.strip())
neu=sorted(set(E2)-set(E1)); weg=sorted(set(E1)-set(E2))
status=sorted(b for b in set(E1)&set(E2) if E1[b]['status']!=E2[b]['status'])
namen=sorted(b for b in set(E1)&set(E2) if b in old_a and b in new_a and old_a[b].get('name')!=new_a[b].get('name'))
L=[f'LISTUNGSABGLEICH BITVAVO (Q-18) vom {now:%d.%m.%Y, %H:%M} Uhr Weltzeit',f'Vergleichsstand: {os.path.basename(prev[-1])}',
   f'Euro-Märkte: vorher {len(E1)}, jetzt {len(E2)}','']
L.append('Neue Märkte (Erstbewertung binnen sieben Tagen fällig): '+(', '.join(f"{b} ({new_a.get(b,{}).get('name','?')}, Netz {','.join(new_a.get(b,{}).get('networks',[]))})" for b in neu) or 'keine'))
L.append('Eingestellte Märkte: '+(', '.join(weg) or 'keine'))
L.append('EIGENER BESTAND BETROFFEN (sofort melden, N4): '+(', '.join(b for b in weg if b in held) or 'nein'))
L.append('Statuswechsel: '+(', '.join(f"{b} {E1[b]['status']} → {E2[b]['status']}" for b in status) or 'keine'))
L.append('Statuswechsel bei eigenem Bestand: '+(', '.join(b for b in status if b in held) or 'nein'))
L.append('Umbenennungen: '+(', '.join(f"{b}: {old_a[b].get('name')} → {new_a[b].get('name')}" for b in namen) or 'keine'))
L+=['',"Prüfsummen (SHA-256):"]
for f in (f'bitvavo_markets_{tag}.json',f'bitvavo_assets_{tag}.json'):
    L.append(f'{f}: '+hashlib.sha256(open(os.path.join(BASE,f),'rb').read()).hexdigest())
txt='\n'.join(L)+'\n'; open(os.path.join(BASE,f'Listungsabgleich_{tag}.txt'),'w').write(txt); print(txt)
json.dump({'neu':neu,'weg':weg,'status':status,'namen':namen,'bestand_betroffen':[b for b in weg+status if b in held]},open(os.path.join(BASE,f'Listungsabgleich_{tag}.json'),'w'),ensure_ascii=False)
