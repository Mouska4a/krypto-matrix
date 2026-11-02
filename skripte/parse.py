import pdfplumber, re, json, sys
pdf=pdfplumber.open(sys.argv[1])
recs=[]; problems=[]
cols=['date','type','cur','amount','quote','recv','fee','status','txid','addr']
hdrnames=[('Date',None),('Type',None),('Currency',None),('Amount',303),('Quote',None),('Received',None),('Fee',None),('Status',None),('Transaction',None),('Address',None)]
for pi,p in enumerate(pdf.pages):
    ws=p.extract_words(keep_blank_chars=False)
    hdr={}
    for w in ws:
        t=w['text']
        for i,(n,_) in enumerate(hdrnames):
            if t==n and cols[i] not in hdr:
                if n=='Amount' and w['x0']>400: continue
                hdr[cols[i]]=w['x0']
    if 'date' not in hdr: continue
    htop=max(w['top'] for w in ws if w['text'] in ('Date','Status'))
    bounds=sorted((v-4,k) for k,v in hdr.items())
    def col(x):
        c=bounds[0][1]
        for b,k in bounds:
            if x>=b: c=k
        return c
    body=[w for w in ws if w['top']>htop+6]
    dates=[w for w in body if re.fullmatch(r'20\d\d-\d\d-\d\d',w['text']) and w['x0']<60]
    for d in dates:
        T=d['top']
        band=[w for w in body if abs(w['top']-T)<=5.5]
        r={c:[] for c in cols}
        for w in sorted(band,key=lambda w:(w['top'],w['x0'])):
            r[col(w['x0'])].append((w['top'],w['text']))
        rec={c:' '.join(t for _,t in sorted(v)) for c,v in r.items()}
        rec['page']=pi+1
        recs.append(rec)
json.dump(recs,open(sys.argv[2],'w'),ensure_ascii=False,indent=0)
print(len(recs))
