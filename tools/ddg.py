import sys,json,urllib.request,urllib.parse,time,re,os
from bs4 import BeautifulSoup
out=json.load(open('serps.json')) if os.path.exists('serps.json') else {}
UA='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'
for q in sys.argv[1:]:
    data=urllib.parse.urlencode({'q':q,'kl':'se-sv'}).encode()
    try:
        h=urllib.request.urlopen(urllib.request.Request('https://html.duckduckgo.com/html/',data=data,headers={'User-Agent':UA}),timeout=25).read().decode('utf-8','ignore')
    except Exception as e:
        out[q]={'time':time.strftime('%Y-%m-%d %H:%M'),'error':str(e)}; continue
    fn='serps/ddg_'+re.sub(r'[^\wåäöÅÄÖ]+','_',q)+'.html'; open(fn,'w').write(h)
    s=BeautifulSoup(h,'lxml'); res=[]
    for r in s.select('div.result'):
        if 'result--ad' in r.get('class',[]): continue
        a=r.select_one('a.result__a')
        if not a: continue
        href=a['href']
        m=re.search(r'uddg=([^&]+)',href)
        if m: href=urllib.parse.unquote(m.group(1))
        sn=r.select_one('.result__snippet')
        res.append([href,a.get_text(' ',strip=True),sn.get_text(' ',strip=True)[:300] if sn else ''])
    out[q]={'time':time.strftime('%Y-%m-%d %H:%M'),'file':fn,'ddg':res[:10]}
    time.sleep(2.5)
json.dump(out,open('serps.json','w'),ensure_ascii=False,indent=1)
