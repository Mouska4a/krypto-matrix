import json,glob,datetime,sys,shutil
from decimal import Decimal as D
from openpyxl import load_workbook
sys.path.insert(0,'/home/claude/scripts'); from shot import S
SRC='/home/claude/work/out/Krypto-Bewertungsmatrix_Arbeitsfassung_Version_1.2.30.xlsx'
OUT='/home/claude/work/out2/Krypto-Bewertungsmatrix_Arbeitsfassung_Version_1.2.30.xlsx'
d=sorted(glob.glob('/home/claude/work/belege/kaufpruefung_*'))[-1]
kp=json.load(open('/home/claude/work/kp.json'))
t={p['market']:D(p['price']) for p in json.load(open(f'{d}/ticker_price.json'))}
ABRUF='02.11.2026, 16:48:29 Uhr Weltzeit'
wb=load_workbook(SRC)
K=wb['Kaufprüfung (Stufe 2)']; P=wb['Zeitpunkt & Portfolio']
# Portfolio: Kurse aus Schnittstelle
for r in range(67,102):
    c=P.cell(r,1).value; p_,g,q,u=S[c]
    if c+'-EUR' in t:
        P.cell(r,14).value=float(t[c+'-EUR']); P.cell(r,2).value=float(round(D(q)*t[c+'-EUR'],2))
        m=P.cell(r,13).value
        P.cell(r,13).value=m.split(' Wert und Kurs:')[0]+f" Kurs: Bitvavo /v2/ticker/price, Abruf {ABRUF}; Wert = Bestand mal Kurs."
    else:
        m=P.cell(r,13).value
        P.cell(r,13).value=m.split(' Wert und Kurs:')[0]+" Wert und Kurs: Bitvavo-Bildschirmfoto 02.11.2026 (Bestandsansicht). Der Coin ist im Pro-Modus und über die Schnittstelle nicht verfügbar (Watchlist-Foto 02.11.2026: „Im Pro Mode nicht verfügbar“); Handelbarkeit in der normalen App klären."
# Marktfilter
btc=kp['BTC']
K['H5'].value=btc['D']; K['H6'].value=round(btc['F'],2)
rows={K.cell(r,1).value:r for r in range(14,44) if K.cell(r,1).value}
for c,o in kp.items():
    r=rows[c]
    K.cell(r,4).value=o['D']; K.cell(r,5).value=o['E']; K.cell(r,6).value=o['F'] if o['F'] is not None else 'n. b.'
    K.cell(r,7).value=o['G']; K.cell(r,9).value=o['I']; K.cell(r,10).value=o['J']
    if c=='BTC': K.cell(r,11).value=1.446503145463846
    K['AA%d'%r].value=round(o['AA'],2); K['AB%d'%r].value=o['AB']; K['AC%d'%r].value=round(o['AC'],2); K['AD%d'%r].value=o['AD']
    K['AJ%d'%r].value=datetime.datetime(2026,11,2); K['AK%d'%r].value='Kaufprüfung 02.11.2026 (Erstprüfung)'
    K['AN%d'%r].value=0
    K['AP%d'%r].value=f"{ABRUF}, Folgenummer {o['nonce']}"
import os; os.makedirs('/home/claude/work/out2',exist_ok=True)
wb.save(OUT); print('saved')
