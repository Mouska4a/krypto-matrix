import json,sys,datetime as dt,glob,os
os.chdir(sys.argv[1])
EZB=1.1216  # USD je EUR, EZB 02.11.2026 (aus Vorprüfung)
def series(f):
    try: d=json.load(open(f))
    except: return None
    if 'totalDataChart' not in d: return None
    return {dt.datetime.utcfromtimestamp(t).date():v for t,v in d['totalDataChart']}
def msum(s,y,m):
    return sum(v for k,v in s.items() if k.year==y and k.month==m)
def months(start,n):
    y,m=start; out=[]
    for i in range(n):
        out.append((y,m)); m+=1
        if m==13: y+=1;m=1
    return out
TTM=months((2025,11),12); PRE=months((2024,11),12); Q3=months((2026,7),3)
for f in sorted(glob.glob('llama_*_daily*.json')):
    s=series(f)
    name=f[6:-5]
    if not s: print(name,'— keine Reihe'); continue
    first=min(s); last=max(s)
    ttm=sum(msum(s,*x) for x in TTM); pre=sum(msum(s,*x) for x in PRE); q=sum(msum(s,*x) for x in Q3)
    # count days present in TTM window
    days=sum(1 for k in s if dt.date(2025,11,1)<=k<=dt.date(2026,10,31))
    mon=[round(msum(s,*x)/1e3) for x in TTM]
    rr=(q*4/ttm-1) if ttm else None
    print(f"{name}: erster {first} letzter {last} Tage_TTM {days}/365 | TTM {ttm/EZB:,.0f} € | Vorjahr {pre/EZB:,.0f} € | Wachstum {((ttm/pre-1) if pre else float('nan')):.3f} | Q3x4/TTM-1 {rr if rr is None else round(rr,3)} | Monate Tsd$ {mon}")
