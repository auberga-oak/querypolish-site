import pathlib
"""Query Polish test-deploy checks. Local: QP_PORT=28765 python3 run_tests.py   Live: QP_BASE=https://auberga-oak.github.io/querypolish-site python3 run_tests.py
Every request leaving the site origin is aborted; the Web3Forms request is intercepted (aborted or answered by a local mock). Nothing is sent."""
import json, re, sys, os, threading, http.server, socketserver, urllib.request
from urllib.parse import parse_qs
from playwright.sync_api import sync_playwright
SITE='/workspace/querypolish/docs'; EV='/workspace/querypolish/evidence'; PREFIX='/querypolish-site'
LIVE=os.environ.get('QP_BASE'); TAG='live-' if LIVE else ''
if LIVE: BASE=LIVE.rstrip('/'); ORIGIN=re.match(r'https?://[^/]+',BASE).group(0)
else:
    PORT=int(os.environ.get('QP_PORT','28765')); ORIGIN=f'http://127.0.0.1:{PORT}'; BASE=ORIGIN+PREFIX
    class H(http.server.SimpleHTTPRequestHandler):
        def log_message(self,*a): pass
        def translate_path(self,path):
            p=path.split('?')[0].split('#')[0]
            if not (p==PREFIX or p.startswith(PREFIX+'/')): return '/nonexistent'
            return super().translate_path(path[len(PREFIX):] or '/')
        def send_error(self,code,message=None,explain=None):
            if code==404:
                b=open(SITE+'/404.html','rb').read(); self.send_response(404); self.send_header('Content-Type','text/html'); self.end_headers(); self.wfile.write(b)
            else: super().send_error(code,message,explain)
    socketserver.TCPServer.allow_reuse_address=True
    srv=socketserver.TCPServer(('127.0.0.1',PORT),lambda *a,**k: H(*a,directory=SITE,**k))
    threading.Thread(target=srv.serve_forever,daemon=True).start()
R={'pass':[],'fail':[]}
def ok(c,msg): (R['pass'] if c else R['fail']).append(msg); print(('PASS ' if c else 'FAIL ')+msg)
PAGES=['/','/thanks/','/privacy/','/no-such-page/']
BANNER="Test version. This site is being tested and isn't open for requests yet."
KEY='c9f5ef0c-dc1b-4ead-8727-fabec3abdc98'; REDIRECT='https://auberga-oak.github.io/querypolish-site/thanks/'
REQ={'Website','email','Consent'}
FILL={'Website':'https://querypolish.com','email':os.environ.get('QP_TEST_EMAIL','test@example.com')}  # intercepted, never sent
external=[]
def guard(route):
    u=route.request.url
    if u.startswith(ORIGIN): return route.continue_()
    external.append(u); return route.abort()
def invalid(p): return set(p.evaluate('[...document.querySelectorAll("#intake input:invalid,#intake select:invalid,#intake textarea:invalid")].map(e=>e.name)'))
def name(path): return path.strip('/').replace('no-such-page','404') or 'home'
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    # 1. every page, every width: status, banner, noindex, overflow, console, screenshot
    for w in (360,390,1280):
        for dpr in ((1,2) if w in (390,1280) else (1,)):
            ctx=b.new_context(viewport={'width':w,'height':800},device_scale_factor=dpr); ctx.route('**/*',guard)
            p=ctx.new_page(); errs=[]; cur=['']
            p.on('console',lambda m,errs=errs,cur=cur: m.type in('error','warning') and not (cur[0]=='/no-such-page/' and '404' in m.text) and errs.append(cur[0]+' '+m.type+': '+m.text))
            p.on('pageerror',lambda e,errs=errs: errs.append('pageerror: '+str(e)))
            for path in PAGES:
                cur[0]=path; resp=p.goto(BASE+path); st=resp.status
                if dpr==1 or path=='/': p.screenshot(path=f'{EV}/{TAG}{name(path)}-{w}{"@2x" if dpr==2 else ""}.png',full_page=True)
                ok(st==(404 if path=='/no-such-page/' else 200),f'{path} @{w}px dpr{dpr}: status {st}')
                ok(p.evaluate('getComputedStyle(document.querySelector("link[rel=stylesheet]")?document.body:document.body).backgroundColor')=='rgb(247, 248, 246)',f'{path} @{w}px: stylesheet applied (subpath assets resolve)')
                sw=p.evaluate('document.documentElement.scrollWidth'); ok(sw<=w,f'{path} @{w}px dpr{dpr}: no horizontal overflow ({sw})')
                if w==1280 and dpr==1:
                    ok(p.locator('.testbanner').inner_text().strip()==BANNER and p.locator('.testbanner').is_visible(),f'{path}: test banner visible')
                    ok(p.eval_on_selector_all('meta[name=robots]','e=>e.map(x=>x.content)')==['noindex, nofollow'],f'{path}: meta robots noindex, nofollow')
                    ok(p.locator('link[rel=canonical]').count()==0,f'{path}: no canonical to querypolish.com')
                    txt=p.inner_text('body'); src=p.content()
                    ok(not re.search(r'10[\s\u00a0.,]?000|\bkr\b|/\s*month|per month',txt,re.I),f'{path}: no price / subscription text')
                    ok('contact@' not in src,f'{path}: no contact@ address')
                    ok(not re.search(r'not for (shops|restaurants)|inte för butiker',txt,re.I),f'{path}: no "not for shops or restaurants"')
                    ok(not re.search(r'every (week)?day|varje vardag|daily change',txt,re.I),f'{path}: no daily-change subscription wording')
                    ok('stores nothing' not in txt.lower() and '7 days and 3 years' not in txt,f'{path}: no "stores nothing" / no retention range')
                    ok(not re.search(r'\bwe\b[^.]{0,30}\b(put|ask|check|test|run)\b[^.]{0,60}\b(ChatGPT|Perplexity|AI Overviews|AI tools?)|answers? (mention|name|include)s?\b|whether the answers|does the (AI )?answer',txt,re.I),f'{path}: no claim that we check AI answers')
                    ok('keeps it for 30 days' not in txt,f'{path}: no unverified 30-day retention claim')
                    ok(len(re.findall(r'reads? (every|the) report',txt,re.I))<=1,f'{path}: report review mentioned at most once')
                    ok('henrik reads' not in src.lower(),f'{path}: no "Henrik reads" anywhere in served HTML (text, meta, JSON-LD)')
                    ok('?' not in p.title() and all('?' not in h for h in p.eval_on_selector_all('h1,h2,h3','e=>e.map(x=>x.innerText)')),f'{path}: no question mark in title or headings')
                    ok(p.eval_on_selector_all('script[src]','e=>e.map(x=>new URL(x.src).origin)')in([],[p.evaluate('location.origin')]),f'{path}: only same-origin scripts (no hCaptcha/analytics)')
                    ok(p.evaluate('document.cookie')=='' and ctx.cookies()==[],f'{path}: no cookies set')
            ok(not errs,f'@{w}px dpr{dpr}: no console errors/warnings (expected 404 doc on /no-such-page/ excluded) {errs}')
            ctx.close()
    if not LIVE:
        _d=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','docs'); _hits=[]
        for _r,_ds,_fs in os.walk(_d):
            for _f in _fs:
                try: _t=open(os.path.join(_r,_f),encoding='utf-8').read()
                except Exception: continue
                if 'henrik reads' in _t.lower(): _hits.append(os.path.relpath(os.path.join(_r,_f),_d))
        ok(not _hits,f'docs/: no "Henrik reads" in any file {_hits}')
    # robots.txt, sitemap, CNAME
    def fetch(u):
        try: r=urllib.request.urlopen(u,timeout=20); return r.status,r.read().decode('utf-8','replace')
        except Exception as e: return getattr(e,'code',str(e)),''
    st,body=fetch(BASE+'/robots.txt'); ok(st==200 and 'Disallow: /' in body,f'robots.txt: {st} Disallow: /')
    ok(fetch(BASE+'/sitemap.xml')[0]==404,'sitemap.xml removed (404)')
    ok(fetch(BASE+'/CNAME')[0]==404,'no CNAME file served')
    # 2. form structure + validation (JS on)
    ctx=b.new_context(viewport={'width':1280,'height':800}); ctx.route('**/*',guard); p=ctx.new_page(); p.goto(BASE+'/')
    names=p.eval_on_selector_all('#intake [name]','els=>els.map(e=>({n:e.name,t:e.type,r:e.required}))')
    json.dump(names,open(f'{EV}/{TAG}form-fields.json','w'),indent=1)
    req={n['n'] for n in names if n['r']}
    ok(req==REQ,f'required fields = {sorted(req)} (Website, email, Consent)')
    ok(p.eval_on_selector('[name=Website]','e=>e.type=="url"') and p.eval_on_selector('[name=email]','e=>e.type=="email"') and p.eval_on_selector('#consent','e=>e.type=="checkbox"'),'types: url, email, checkbox')
    ok(not any(n['t']=='password' or re.search(r'pass|login|user ?name',n['n'],re.I) for n in names),'no password/login fields')
    ok(p.locator('[name=business_type]').count()==0,'branching question removed')
    ok(p.eval_on_selector('#lang-en','e=>e.checked') and not p.eval_on_selector('#lang-sv','e=>e.checked'),'report language defaults to English')
    hid={n['n']:p.eval_on_selector(f'input[type=hidden][name="{n["n"]}"]','e=>e.value') for n in names if n['t']=='hidden'}
    ok(hid.get('access_key')==KEY and hid.get('redirect')==REDIRECT,f'hidden: key unchanged, redirect={hid.get("redirect")}')
    ok('Finansium AB' in p.locator('footer').inner_text(),'footer names Finansium AB')
    ok(p.locator('#intake a[href^="mailto:"]').count()==0 and p.eval_on_selector('#intake','f=>f.action')=='https://api.web3forms.com/submit' and p.eval_on_selector('#intake','f=>f.method')=='post','form: no mailto, posts to Web3Forms')
    if p.locator('.example').count(): ok('ExampleCo is invented' in p.inner_text('.example'),'example section labelled as invented')
    if 'copy-ai' in os.environ.get('QP_EXPECT',''):
        t=p.inner_text('body')
        ok(t.count('A Finansium SEO expert reads every report before it is sent. Then we email it to the address you give us.')==1,'home: "A Finansium SEO expert reads every report before it is sent." exactly once')
        ok('Henrik reads' not in t,'home: no "Henrik reads"')
        ok('add us as a user in Google Search Console and Google Analytics. You never share a password.' in t,'home: Zinsser GSC/GA4 line')
        ok('This page uses no cookies or analytics.' in t,'home: storage line present')
        ok('Your Google Business Profile, if we can find one: categories,' in t,'home: Zinsser GBP edit')
        ok('Web3Forms, which keeps it for 1 year and then deletes it.' in t,'home: Web3Forms retention 1 year')
        pv=pathlib.Path(__file__).resolve().parent.parent.joinpath('docs/privacy/index.html').read_text()
        ok('Web3Forms keeps it for 1 year and then deletes it.' in pv and 'We keep your answers and the report for 12 months after we send it, then delete them.' in pv,'privacy: Web3Forms 1 year + our 12 months')
    posts=[]
    def backend(route): posts.append(route.request.post_data); route.abort()
    p.route('https://api.web3forms.com/**',backend)
    p.click('#submit'); p.wait_for_timeout(400)
    ok(not posts and invalid(p)==REQ,f'empty submit blocked, invalid={sorted(invalid(p))}')
    ok('required fields' in p.inner_text('#status'),'status message shown on invalid')
    ok(p.evaluate('document.activeElement.name')=='Website','focus moved to first invalid field (Website)')
    p.fill('[name=Website]','not a url'); p.fill('[name=email]',FILL['email']); p.check('#consent'); p.click('#submit'); p.wait_for_timeout(300)
    ok(not posts and invalid(p)=={'Website'},'invalid website URL blocks submit')
    p.fill('[name=Website]',FILL['Website']); p.fill('[name=email]','not-an-email'); p.click('#submit'); p.wait_for_timeout(300)
    ok(not posts and invalid(p)=={'email'},'invalid email blocks submit')
    p.fill('[name=email]',FILL['email']); p.uncheck('#consent'); p.click('#submit'); p.wait_for_timeout(300)
    ok(not posts and invalid(p)=={'Consent'},'missing consent blocks submit')
    p.check('#consent'); p.fill('[name=Notes]','TEST submission by Kent Beck, please ignore.')
    p.click('#submit'); p.wait_for_timeout(800)
    ok(len(posts)==1,'valid submit fires exactly 1 backend request (intercepted + aborted)')
    body=json.loads(posts[0]) if posts else {}
    json.dump(body,open(f'{EV}/{TAG}payload-aborted.json','w'),indent=1,ensure_ascii=False)
    ok(all(body.get(k)==v for k,v in FILL.items()) and body.get('Consent')=='Yes' and body.get('report_language')=='English','payload: Website, email, Consent=Yes, report_language=English')
    ok(body.get('access_key')==KEY and body.get('redirect')==REDIRECT and 'botcheck' not in body,'payload: key, redirect, honeypot unchecked')
    ok('not sent' in p.inner_text('#status') and p.url.rstrip('/')==BASE,'aborted -> error shown, stays on page')
    p.screenshot(path=f'{EV}/{TAG}submit-aborted-1280.png')
    p.unroute('https://api.web3forms.com/**'); posts2=[]
    def mock(route): posts2.append(1); route.fulfill(status=200,content_type='application/json',body='{"success":true,"message":"mock"}')
    p.route('https://api.web3forms.com/**',mock)
    p.click('#submit'); p.wait_for_url(BASE+'/thanks/',timeout=8000)
    ok(p.url==BASE+'/thanks/' and len(posts2)==1,'mocked success -> thanks/ under the subpath')
    ok("We'll email the report" in p.inner_text('main'),'thanks page says we will email the report')
    ctx.close()
    # 3. JS off
    for w in (360,390,1280):
        ctx=b.new_context(java_script_enabled=False,viewport={'width':w,'height':800}); nat=[]
        def mk(nat):
            def g2(route):
                u=route.request.url
                if u.startswith(ORIGIN): return route.continue_()
                nat.append((u,route.request.method,route.request.post_data)); route.abort()
            return g2
        ctx.route('**/*',mk(nat)); p=ctx.new_page(); p.goto(BASE+'/')
        p.screenshot(path=f'{EV}/{TAG}home-nojs-{w}.png',full_page=True)
        sw=p.evaluate('document.documentElement.scrollWidth'); ok(sw<=w,f'JS off @{w}px: no horizontal overflow ({sw})')
        if w==390:
            p.click('#submit'); p.wait_for_timeout(500); ok(not nat,'JS off: empty submit blocked by native validation')
            for k,v in FILL.items(): p.fill(f'[name="{k}"]',v)
            p.check('#consent')
            try:
                with p.expect_request('https://api.web3forms.com/**',timeout=5000): p.click('#submit')
            except Exception: pass
            p.wait_for_timeout(500)
            q=parse_qs(nat[0][2] or '',keep_blank_values=True) if nat else {}
            json.dump(q,open(f'{EV}/{TAG}payload-nojs.json','w'),indent=1)
            ok(len(nat)==1 and nat[0][1]=='POST' and q.get('redirect')==[REDIRECT],'JS off: native POST to Web3Forms, redirect to github.io thanks/ (aborted)')
            ok(q.get('Website')==[FILL['Website']] and q.get('email')==[FILL['email']] and q.get('Consent')==['Yes'] and q.get('report_language')==['English'],'JS off: payload fields correct')
        ctx.close()
    # 4. contrast + links
    ctx=b.new_context(viewport={'width':1280,'height':800}); ctx.route('**/*',guard); p=ctx.new_page()
    js=open('/workspace/querypolish/tests/contrast.js').read(); allc=[]; links=set()
    for path in PAGES:
        p.goto(BASE+path)
        if path!='/no-such-page/': allc+=[dict(r,page=path) for r in p.evaluate(js)]
        links|={l for l in p.eval_on_selector_all('a[href]','as=>as.map(a=>a.href)') if not (path=='/no-such-page/' and '/no-such-page/' in l)}
        links|=set(p.eval_on_selector_all('link[href]','as=>as.map(a=>a.href)'))
        for frag in p.eval_on_selector_all('a[href^="#"]','as=>as.map(a=>a.getAttribute("href").slice(1))'):
            ok(frag=='' or p.locator('#'+frag).count()==1,f'{path}: anchor #{frag} exists')
        bad=p.eval_on_selector_all('a[href],link[href],script[src]',f'els=>els.map(e=>e.getAttribute("href")||e.getAttribute("src")).filter(h=>h.startsWith("/")&&!h.startsWith("{PREFIX}/"))')
        ok(not bad,f'{path}: no root-absolute paths outside {PREFIX}/ {bad}')
    json.dump(sorted(allc,key=lambda r:r['ratio'])[:15],open(f'{EV}/{TAG}contrast-lowest.json','w'),indent=1)
    low=[r for r in allc if r['ratio']<(3 if r['large'] else 4.5)]; mn=min(allc,key=lambda r:r['ratio'])
    ok(not low,f'contrast: {len(allc)} text nodes, min {mn["ratio"]:.2f}:1 ("{mn["text"][:30]}"), failures {low[:3]}')
    ctx.close(); b.close()
    ext=[]
    for l in sorted(links):
        if l.startswith(ORIGIN):
            c=fetch(l.split('#')[0])[0]; ok(c==200,f'internal link {l} -> {c}')
        else: ext.append(l)
    for l in ext:
        if l.startswith('http'): c=fetch(l)[0]; ok(c==200,f'external link {l} -> {c}')
    json.dump(ext,open(f'{EV}/{TAG}external-links.json','w'))
    ok(not external,f'no request left the site origin during tests: {sorted(set(external))}')
print(f"\nSUMMARY: {len(R['pass'])} pass, {len(R['fail'])} fail")
sys.exit(1 if R['fail'] else 0)
