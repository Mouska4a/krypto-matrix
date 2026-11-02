import json,glob,datetime,statistics,sys
from decimal import Decimal as D
d=sorted(glob.glob('/home/claude/work/belege/kaufpruefung_*'))[-1]
t={p['market']:float(p['price']) for p in json.load(open(f'{d}/ticker_price.json'))}
L=datetime.date(2026,11,1); TODAY=datetime.date(2026,11,2)
PLAN={'BTC':1000,'ETH':1000,'TRX':667,'CAKE':667,'UNI':333,'SKY':333,'LTC':333,'BCH':333,'POL':333}
def candles(c):
    k=json.load(open(f'{d}/{c}-EUR_1d_300.json'))
    by={datetime.datetime.fromtimestamp(x[0]/1000,datetime.timezone.utc).date():x for x in k}
    by.pop(TODAY,None)  # laufende Kerze verwerfen
    return by,min(by)
def avg(by,first,N):
    days=[L-datetime.timedelta(days=i) for i in range(N)]
    vals=[float(by[x][4]) for x in days if x in by]
    hist_missing=sum(1 for x in days if x<first)
    gaps=sum(1 for x in days if x>=first and x not in by)
    miss=N-len(vals)
    if miss>0.05*N: return None,len(vals),miss,hist_missing,gaps
    return sum(vals)/len(vals),len(vals),miss,hist_missing,gaps
def close_back(by,n):
    for k in range(0,4):
        x=L-datetime.timedelta(days=n+k)
        if x in by: return float(by[x][4]),x
    return None,None
out={}
bby,bfirst=candles('BTC'); bc=float(bby[L][4]); b90,_=close_back(bby,90)
rb90=bc/b90-1
for c,plan in PLAN.items():
    by,first=candles(c)
    a50=avg(by,first,50); a200=avg(by,first,200)
    cl=float(by[L][4]); c30,d30=close_back(by,30); c90,d90=close_back(by,90)
    ch30=cl/c30-1; r90=cl/c90-1; rs90=(1+r90)/(1+rb90)-1
    med=statistics.median([float(D(by[x][5])*D(by[x][4])) for x in [L-datetime.timedelta(days=i) for i in range(30)] if x in by])
    n30=sum(1 for x in [L-datetime.timedelta(days=i) for i in range(30)] if x in by)
    bk=json.load(open(f'{d}/{c}-EUR_book.json'))
    bids=[(float(p),float(q)) for p,q in bk['bids']]; asks=[(float(p),float(q)) for p,q in bk['asks']]
    bb,ba=bids[0][0],asks[0][0]; mid=(bb+ba)/2; spr=(ba-bb)/mid
    vol1=sum(p*q for p,q in bids if p>=mid*0.99)
    big=0.4*plan; rem=big; acc=0; disc=0
    for p,q in bids:
        e=min(rem,p*q); disc+=e*(mid-p)/mid; acc+=e; rem-=e
        if rem<=1e-9: break
    abschlag=disc/acc if rem<=1e-9 else None
    out[c]=dict(D=t[f'{c}-EUR'],E=a50[0],E_n=a50[1],F=a200[0],F_n=a200[1],F_hist=a200[3],F_gap=a200[4],G=ch30,J=rs90,AA=med,AA_n=n30,AB=spr,AC=vol1,AD=abschlag,nonce=bk.get('nonce'),I=plan,close=cl,first=str(first),d30=str(d30),d90=str(d90),bid=bb,ask=ba)
    o=out[c]
    print(f"{c:5} Kurs {o['D']:>10} 50d {o['E']:.6g}({o['E_n']}/50) 200d {o['F'] if o['F'] is None else round(o['F'],6)}({o['F_n']}/200,hist{o['F_hist']},gap{o['F_gap']}) 30d {ch30:+.1%} RS90 {rs90:+.1%} Z1abst {o['D']/o['E']-1:+.1%} trend {'auf' if o['F'] and o['D']>=o['F'] else 'ab'} Med {med:,.0f}({n30}) Spread {spr:.3%} Vol-1% {vol1:,.0f} Abschl {abschlag if abschlag is None else round(abschlag*100,3)}% nonce {o['nonce']} first {first}")
print('BTC 90d ret',rb90,'BTC close',bc)
json.dump(out,open('/home/claude/work/kp.json','w'),indent=1)
