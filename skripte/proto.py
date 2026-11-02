import json,datetime
from openpyxl import load_workbook
F='/home/claude/work/out2/Krypto-Bewertungsmatrix_Arbeitsfassung_Version_1.2.30.xlsx'
vals=load_workbook(F,data_only=True)['Kaufprüfung (Stufe 2)']
kp=json.load(open('/home/claude/work/kp.json')); od=json.load(open('/home/claude/work/orders.json'))
wb=load_workbook(F); L=wb['Protokoll']
rows={vals.cell(r,1).value:r for r in range(14,44) if vals.cell(r,1).value}
def de(x,d=2): return f"{x:,.{d}f}".replace(',','X').replace('.',',').replace('X','.')
def pct(x): return f"{x*100:+.1f} %".replace('.',',')
pr=6
order=['BTC','ETH','TRX','CAKE','UNI','SKY','LTC','BCH','POL']
for c in order:
    r=rows[c]; g=lambda col: vals[f'{col}{r}'].value; o=kp[c]
    assert L.cell(pr,1).value in (None,'')
    L.cell(pr,1).value=datetime.datetime(2026,11,2,17,48)
    L.cell(pr,2).value=c; L.cell(pr,3).value='Kaufprüfung'
    reg={'Ja – drei Tranchen':'§ 19 Nr. 8','Ja – drei Tranchen, weite Abstände':'§ 19 Nr. 9','Teilweise – nur Tranche 1 (RS90 negativ)':'§ 19 Nr. 8 (RS90 negativ)'}[g('R')]
    L.cell(pr,4).value=f"§ 17 bis § 21, Z1 bis Z5; {reg}"
    L.cell(pr,5).value=g('B'); L.cell(pr,6).value=g('C'); L.cell(pr,7).value=g('R')
    z3=f"Z3 {g('P')}: Kurs {de(o['D'],6 if o['D']<1 else 2)} € zu 200-Tage-Ø {de(o['F'],6 if o['F']<1 else 2)} € ({pct(o['D']/o['F']-1)})"
    rs='' if c=='BTC' else f", RS90 {pct(o['J'])}"
    z4=f"Z4 {g('Q')}"+(" (MVRV 1,45 vom 01.11.2026)" if c=='BTC' else f" (VS {g('C')})")
    L.cell(pr,8).value=(f"Z1 ok: {pct(o['D']/o['E']-1)} zum 50-Tage-Ø, 30 Tage {pct(o['G'])}. Z2 ok: Median-Tagesumsatz {de(o['AA'],0)} €, Spread {de(o['AB']*100,3)} %. {z3}{rs}. {z4}. Z5: keine erfasste Einzelfreigabe. "
                        f"Marktfilter: BTC {de(kp['BTC']['D'],0)} € über 200-Tage-Ø {de(kp['BTC']['F'],0)} €.")
    L.cell(pr,9).value=o['D']
    lims=[float(x[0]) for x in od[c]['orders']]
    for i,lv in enumerate(lims): L.cell(pr,10+i).value=lv
    L.cell(pr,13).value=round(sum(x[2] for x in od[c]['orders']),2)
    if g('AI') not in (None,''): L.cell(pr,14).value=g('AI')
    L.cell(pr,15).value="Bitvavo /v2/ticker/price, Tageskerzen (300, laufende verworfen, letzter Tag 01.11.2026), Orderbuch, Abruf 02.11.2026 16:48:29 Uhr Weltzeit; MVRV Coin Metrics Community, 01.11.2026"
    L.cell(pr,16).value=datetime.datetime(2026,11,2)
    L.cell(pr,32).value=(f"Geplante Gesamtposition {de(o['I'],0)} € (Vorschlag: Budget rund 5.000 € nach Grundeinheiten aufgeteilt, Anleger am 02.11.2026: Budget rund 5.000 €). "
        f"Zulässige Position {de(g('AH'),0)} € (Grenzen: Grundeinheiten {de(g('AG'),0)} €, Liquidität {de(g('AF'),0)} €), zulässiger Zukauf {de(g('AO'),0)} €. "
        f"Limits auf den Tick von Bitvavo abgerundet; Mengen: "+"; ".join(f"{x[1]} zu {x[0]} €" for x in od[c]['orders'])+". "
        f"Q-23: Kaufvolumen bis −1 % {de(o['AC'],0)} €, Abschlag größte Teilorder {de(o['AD']*100,3)} %, Folgenummer {o['nonce']}. Umsatz aller Börsen (nur Information) nicht erhoben: CoinGecko-Abruf zweimal gedrosselt. Nur Limitaufträge; Aufträge setzt der Anleger.")
    pr+=1
wb.save(F); print('rows to',pr-1)
