import sys,datetime
from openpyxl import load_workbook
def ser(v):
    if v is None: return ''
    if isinstance(v,datetime.datetime):
        s=(v-datetime.datetime(1899,12,30)).total_seconds()/86400
        return str(int(s)) if s==int(s) else repr(s)
    if isinstance(v,datetime.date): return str((v-datetime.date(1899,12,30)).days)
    if isinstance(v,bool): return 'TRUE' if v else 'FALSE'
    if isinstance(v,float):
        return str(int(v)) if v==int(v) and abs(v)<1e15 else repr(v)
    return str(v).replace('\n',' ')
wb=load_workbook(sys.argv[1],data_only=True)
out=[]
for ws in wb:
    out.append(f'## Sheet: {ws.title}'); out.append('')
    for row in ws.iter_rows(values_only=True):
        cells=[ser(v) for v in row]
        while cells and cells[-1]=='': cells.pop()
        if cells: out.append('\t'.join(cells))
    out.append('')
open(sys.argv[2],'w',encoding='utf-8').write('\n'.join(out))
