"""Dump all user-visible text of the site pages (incl. placeholders, hidden form settings). Usage: python3 tools/extract_copy.py > evidence/landing-copy.txt"""
import re
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(s): super().__init__(); s.out=[]; s.skip=0
    def handle_starttag(s,t,a):
        a=dict(a)
        if t in('script','style'): s.skip+=1
        if t in('h1','h2','h3','legend'): s.out.append('\n\n'+{'h1':'# ','h2':'## ','h3':'### ','legend':'### '}[t])
        elif t in('p','li','label','div','option','button','footer','header'): s.out.append('\n'+('- ' if t=='li' else ''))
        if t in('input','textarea') and a.get('placeholder'): s.out.append(f' [placeholder: {a["placeholder"]}]')
        if t=='input' and a.get('type')=='hidden': s.out.append(f'\n[hidden {a["name"]}={a.get("value")}]')
        if a.get('data-branch'): s.out.append(f'\n[shown for: {a["data-branch"]}]')
    def handle_endtag(s,t):
        if t in('script','style'): s.skip-=1
    def handle_data(s,d):
        if not s.skip: s.out.append(re.sub(r'\s+',' ',d))
for f in ['docs/index.html','docs/thanks/index.html','docs/privacy/index.html','docs/404.html']:
    p=P(); src=open(f).read(); t=re.search(r'<title>(.*?)</title>',src).group(1); m=re.search(r'name="description" content="(.*?)"',src)
    p.feed(src.split('<body>')[1]); txt=re.sub(r'\n\s*\n+','\n\n',''.join(p.out)); txt=re.sub(r'\n +','\n',txt)
    print(f'==================== {f}\nTITLE: {t}'+(f'\nMETA DESCRIPTION: {m.group(1)}' if m else '')+'\n'+txt.strip()+'\n')
