import csv,sys,collections,datetime
from decimal import Decimal as D
sys.path.insert(0,'/home/claude/scripts'); from shot import S
rows=list(csv.DictReader(open('/home/claude/work/export.csv',newline='',encoding='utf-8')))
for i,r in enumerate(rows): r['_i']=i
tx=[r for r in rows if r['Type'] in('buy','sell')]
def key(r): return (r['Date'],r['Time'].ljust(12,'0'), -r['_i'])  # CSV is newest-first: higher index = earlier
tx.sort(key=key)
lots=collections.defaultdict(list); real=collections.defaultdict(D); amb=[]
for r in tx:
    c=r['Currency'];a=abs(D(r['Amount']));q=D(r['Quote Price']);f=D(r['Fee amount'])
    if r['Type']=='buy':
        lots[c].append([r['Date'],r['Time'],a,a*q+f,r['Transaction ID']])
    else:
        rem=a
        while rem>0:
            L=lots[c][0]
            take=min(rem,L[2]); cost=L[3]*take/L[2]
            # ambiguity: partial consumption of lot sharing timestamp with others
            if take<L[2] and len(lots[c])>1 and lots[c][1][0]==L[0] and lots[c][1][1][:8]==L[1][:8]: amb.append((c,L[0],L[1]))
            L[3]-=cost;L[2]-=take;rem-=take
            if L[2]==0: lots[c].pop(0)
print('ambiguous partial at same timestamp:',amb)
res={}
for c,ls in sorted(lots.items()):
    q=sum(l[2] for l in ls)
    if q==0: continue
    cost=sum(l[3] for l in ls); paid=sum(-D(r['Received / Paid Amount']) for r in tx if r['Currency']==c and r['Type']=='buy')
    p,g,m,u=S[c]; bitcost=D(g)-D(u)
    res[c]=(ls[0][0],ls[0][1],q,cost)
    print(f"{c:8} oldest {ls[0][0]} {ls[0][1][:8]} qty {q} shotqty {m} {'OK' if q==D(m) else 'ABW'} FIFO {cost:.2f} totalpaid {paid:.2f} bitvavo-implied {bitcost:.2f} diff {cost-bitcost:.2f}  qty*price {q*D(p):.2f} vs {g}")
print('coins',len(res),'shot',len(S),set(S)^set(res))
