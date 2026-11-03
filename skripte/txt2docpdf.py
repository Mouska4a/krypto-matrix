import sys,re,subprocess,os
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
def is_head(l):
    s=l.strip()
    return len(s)>3 and s==s.upper() and re.search('[A-ZÄÖÜ]{3}',s) and '\t' not in s and not s.startswith('HTTP')
def conv(txt):
    lines=open(txt,encoding='utf-8').read().split('\n')
    d=Document(); st=d.styles['Normal']; st.font.name='Calibri'; st.font.size=Pt(11)
    first=True
    for l in lines:
        if not l.strip(): continue
        if first:
            d.add_heading(l.strip().title() if False else l.strip(),0); first=False; continue
        if is_head(l):
            lvl=1 if re.match(r'^(TEIL|ANHANG|EINLEITUNG|GLIEDERUNG|HINWEIS|[A-ZÄÖÜ]+ENS:)',l.strip()) else 2
            d.add_heading(l.strip(),lvl)
        else:
            p=d.add_paragraph(l.strip()); p.paragraph_format.space_after=Pt(6)
    out=txt[:-4]+'.docx'; d.save(out)
    subprocess.run(['soffice','--headless','--convert-to','pdf','--outdir',os.path.dirname(out),out],check=True,capture_output=True,timeout=180)
    print(out, os.path.exists(txt[:-4]+'.pdf'))
for t in sys.argv[1:]: conv(t)
