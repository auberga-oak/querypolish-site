import sys,json,re,glob,os
from bs4 import BeautifulSoup
out={}
for f in sorted(glob.glob('pages/*.html')):
    h=open(f,encoding='utf-8',errors='ignore').read()
    s=BeautifulSoup(h,'lxml'); d={}
    d['lang']=s.html.get('lang') if s.html else None
    d['title']=s.title.get_text(strip=True) if s.title else None
    d['title_len']=len(d['title'] or '')
    m=s.find('meta',attrs={'name':'description'}); d['meta_desc']=m.get('content') if m else None
    d['meta_len']=len(d['meta_desc'] or '')
    m=s.find('meta',attrs={'name':'robots'}); d['robots']=m.get('content') if m else None
    m=s.find('meta',attrs={'name':'generator'}); d['generator']=[x.get('content') for x in s.find_all('meta',attrs={'name':'generator'})]
    c=s.find('link',rel='canonical'); d['canonical']=c.get('href') if c else None
    d['hreflang']=[(l.get('hreflang'),l.get('href')) for l in s.find_all('link',hreflang=True)]
    d['jsonld']=[x.string for x in s.find_all('script',type='application/ld+json')]
    d['og']={m.get('property'):m.get('content') for m in s.find_all('meta') if (m.get('property') or '').startswith('og:')}
    for t in s(['script','style','noscript','svg']): t.decompose()
    for lvl in range(1,4): d['h%d'%lvl]=[x.get_text(' ',strip=True) for x in s.find_all('h%d'%lvl)]
    main=s.find('main') or s.find(id='content') or s.body
    txt=main.get_text(' ',strip=True) if main else ''
    full=s.body.get_text(' ',strip=True) if s.body else ''
    d['words_main']=len(re.findall(r'\w+',txt)); d['words_body']=len(re.findall(r'\w+',full))
    d['text']=txt[:8000]
    links=[]
    for a in s.find_all('a',href=True): links.append((a['href'],a.get_text(' ',strip=True)[:60]))
    d['links']=sorted(set(links))
    imgs=s.find_all('img'); d['imgs']=len(imgs); d['imgs_no_alt']=sum(1 for i in imgs if not (i.get('alt') or '').strip())
    out[os.path.basename(f)]=d
json.dump(out,sys.stdout,ensure_ascii=False,indent=1)
