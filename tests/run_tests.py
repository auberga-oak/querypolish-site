import json, re, sys, threading, http.server, socketserver, functools, os, urllib.request
from playwright.sync_api import sync_playwright
SITE='/workspace/querypolish/docs'; EV='/workspace/querypolish/evidence'; PORT=int(os.environ.get("QP_PORT","8791"))
BASE=f'http://127.0.0.1:{PORT}'
class H(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*a): pass
    def send_error(self, code, message=None, explain=None):
        if code==404:
            body=open(SITE+'/404.html','rb').read(); self.send_response(404); self.send_header('Content-Type','text/html'); self.end_headers(); self.wfile.write(body)
        else: super().send_error(code,message,explain)
socketserver.TCPServer.allow_reuse_address=True
srv=socketserver.TCPServer(('127.0.0.1',PORT),functools.partial(H,directory=SITE)); srv.allow_reuse_address=True
threading.Thread(target=srv.serve_forever,daemon=True).start()
R={'pass':[], 'fail':[]}
def ok(c,msg): (R['pass'] if c else R['fail']).append(msg); print(('PASS ' if c else 'FAIL ')+msg)
PAGES=['/','/thanks/','/privacy/','/no-such-page/']
external=[]  # every request leaving localhost
def guard(route):
    u=route.request.url
    if u.startswith(BASE): return route.continue_()
    external.append(u); return route.abort()
REQ={'First':'x'}
FILL={'Business name':'Test Plumbing AB','Address':'Testgatan 1, 111 22 Stockholm','Industry':'Plumber',
 'Website':'https://example.com','Google Business Profile URL':'https://maps.app.goo.gl/test0',
 'Main service':'Emergency plumbing','Main city':'Stockholm','Keyword 1':'plumber stockholm','Keyword 2':'emergency plumber','Keyword 3':'blocked drain stockholm',
 'Competitor 1 GBP URL':'https://maps.app.goo.gl/test1','Competitor 1 domain':'example.org',
 'Competitor 2 GBP URL':'https://maps.app.goo.gl/test2','Competitor 2 domain':'example.net',
 'Competitor 3 GBP URL':'https://maps.app.goo.gl/test3','Competitor 3 domain':'example.edu',
 'email':'warren.ekenberg@agentmail.to'}
def fill(p,skip=()):
    for k,v in FILL.items():
        if k in skip: continue
        p.fill(f'[name="{k}"]',v)
    if 'Consent' not in skip: p.check('#consent')
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    # 1. screenshots + console
    for w in (360,390,1280):
        for dpr in ((1,2) if w in (390,1280) else (1,)):
            ctx=b.new_context(viewport={'width':w,'height':800},device_scale_factor=dpr); ctx.route('**/*',guard)
            p=ctx.new_page(); errs=[]; cur=['']
            p.on('console',lambda m,errs=errs,cur=cur: m.type in('error','warning') and not (cur[0]=='/no-such-page/' and '404' in m.text) and errs.append(cur[0]+' '+m.type+': '+m.text))
            p.on('pageerror',lambda e,errs=errs: errs.append('pageerror: '+str(e)))
            for path in PAGES:
                cur[0]=path
                st=p.goto(BASE+path).status
                name=(path.strip('/').replace('no-such-page','404') or 'home')
                if dpr==1 or path=='/': p.screenshot(path=f'{EV}/{name}-{w}{"@2x" if dpr==2 else ""}.png',full_page=True)
                sw=p.evaluate('document.documentElement.scrollWidth')
                ok(sw<=w, f'{path} @{w}px dpr{dpr}: no horizontal overflow (scrollWidth={sw})')
                if path!='/no-such-page/': ok(st==200,f'{path} status {st}')
                else: ok(st==404,f'404 page status {st}')
            ok(not errs, f'@{w}px dpr{dpr}: no console errors/warnings on any page (expected document 404 on /no-such-page/ excluded) {errs}')
            ctx.close()
    # 2. structure checks
    ctx=b.new_context(viewport={'width':1280,'height':800}); ctx.route('**/*',guard); p=ctx.new_page(); p.goto(BASE+'/')
    names=p.eval_on_selector_all('#intake [name]','els=>els.map(e=>({n:e.name,t:e.type,r:e.required}))')
    json.dump(names,open(f'{EV}/form-fields.json','w'),indent=1)
    req=[n['n'] for n in names if n['r']]
    ok(set(req)==set(FILL)|{'Consent'}, f'required fields = {req}')
    ok(not any(n['t']=='password' or re.search(r'pass|login|user ?name',n['n'],re.I) for n in names),'no password/login fields')
    ok(p.locator('footer').inner_text().count('Finansium AB')>=1,'footer names Finansium AB')
    ok(p.eval_on_selector('#consent','e=>e.required&&e.type=="checkbox"'),'consent checkbox required')
    ok(p.eval_on_selector('[name=email]','e=>e.required&&e.type=="email"'),'email required, type=email')
    # 3. validation (JS on)
    posts=[]
    def backend(route):
        posts.append(route.request.post_data); route.abort()
    p.route('https://api.web3forms.com/**',backend)
    p.click('#submit'); p.wait_for_timeout(400)
    inv=p.evaluate('[...document.querySelectorAll("#intake input:invalid,#intake select:invalid,#intake textarea:invalid")].map(e=>e.name)')
    ok(len(posts)==0 and len(inv)==len(req), f'empty submit blocked, {len(inv)} invalid fields, 0 requests')
    ok('required fields' in p.inner_text('#status'), 'status message shown on invalid: '+p.inner_text('#status'))
    ok(p.evaluate('document.activeElement.name')=='Business name','focus moved to first invalid field')
    fill(p,skip=('Consent',)); p.click('#submit'); p.wait_for_timeout(300)
    ok(len(posts)==0 and p.evaluate('document.querySelector("#consent").matches(":invalid")'),'missing consent blocks submit')
    p.check('#consent'); p.fill('[name=email]','not-an-email'); p.click('#submit'); p.wait_for_timeout(300)
    ok(len(posts)==0,'invalid email blocks submit')
    p.fill('[name=email]',FILL['email']); p.fill('[name="Competitor 2 domain"]',''); p.click('#submit'); p.wait_for_timeout(300)
    ok(len(posts)==0,'missing competitor 2 domain blocks submit')
    p.fill('[name="Competitor 2 domain"]',FILL['Competitor 2 domain'])
    # 4. submit, backend aborted
    p.click('#submit'); p.wait_for_timeout(800)
    ok(len(posts)==1,'valid submit fires exactly 1 backend request (aborted)')
    body=json.loads(posts[0]) if posts else {}
    json.dump(body,open(f'{EV}/intercepted-payload-abort.json','w'),indent=1)
    ok(all(body.get(k)==v for k,v in FILL.items()) and body.get('Consent')=='Yes','payload carries every required value + consent')
    ok(body.get('access_key')=='WEB3FORMS_ACCESS_KEY' and 'botcheck' not in body, 'payload has placeholder key, honeypot unchecked')
    st=p.inner_text('#status'); ok('not sent' in st and p.url.endswith('/'), 'aborted request -> error shown, stays on page: '+st)
    p.screenshot(path=f'{EV}/submit-aborted-1280.png')
    # 5. mocked success (fulfilled locally, nothing leaves the box)
    p.unroute('https://api.web3forms.com/**'); posts2=[]
    def mock(route):
        posts2.append(route.request.post_data); route.fulfill(status=200,content_type='application/json',body='{"success":true,"message":"mock"}')
    p.route('https://api.web3forms.com/**',mock)
    p.click('#submit'); p.wait_for_url(BASE+'/thanks/',timeout=5000)
    ok(p.url==BASE+'/thanks/' and len(posts2)==1,'mocked success -> /thanks/')
    ok("We'll email the report" in p.inner_text('main'),'thanks page says we will email the report')
    ctx.close()
    # 6. JS off: native validation + native POST
    ctx=b.new_context(java_script_enabled=False,viewport={'width':390,'height':800}); nat=[]
    def g2(route):
        u=route.request.url
        if u.startswith(BASE): return route.continue_()
        nat.append((u,route.request.method,route.request.post_data)); route.abort()
    ctx.route('**/*',g2); p=ctx.new_page(); p.goto(BASE+'/')
    p.click('#submit'); p.wait_for_timeout(500)
    ok(len(nat)==0,'JS off: empty submit blocked by native validation')
    fill(p); 
    try:
        with p.expect_request('https://api.web3forms.com/**',timeout=4000): p.click('#submit')
    except Exception as e: pass
    p.wait_for_timeout(500)
    ok(len(nat)==1 and nat[0][1]=='POST' and 'redirect=https%3A%2F%2Fquerypolish.com%2Fthanks%2F' in (nat[0][2] or ''),'JS off: native POST to Web3Forms with redirect to /thanks/ (aborted)')
    ctx.close()
    # 7. contrast
    ctx=b.new_context(viewport={'width':1280,'height':800}); ctx.route('**/*',guard); p=ctx.new_page()
    js=open('/workspace/querypolish/tests/contrast.js').read(); allc=[]
    for path in PAGES[:3]:
        p.goto(BASE+path); res=p.evaluate(js); allc+= [dict(r,page=path) for r in res]
    json.dump(sorted(allc,key=lambda r:r['ratio'])[:15],open(f'{EV}/contrast-lowest.json','w'),indent=1)
    low=[r for r in allc if r['ratio']<(3 if r['large'] else 4.5)]
    mn=min(allc,key=lambda r:r['ratio'])
    ok(not low,f'contrast: {len(allc)} text nodes, min {mn["ratio"]:.2f}:1 ("{mn["text"][:30]}" {mn["fg"]} on {mn["bg"]}), failures {low[:3]}')
    # 8. links
    links=set()
    for path in PAGES:
        p.goto(BASE+path)
        if path!='/no-such-page/': links|=set(p.eval_on_selector_all('a[href]','as=>as.map(a=>a.href)'))
        for frag in p.eval_on_selector_all('a[href^="#"]','as=>as.map(a=>a.getAttribute("href").slice(1))'):
            ok(frag=='' or p.locator('#'+frag).count()==1, f'{path}: anchor #{frag} exists')
    ctx.close(); b.close()
    ext=[]
    for l in sorted(links):
        if l.startswith(BASE):
            u=l.split('#')[0]
            try: c=urllib.request.urlopen(u).status
            except Exception as e: c=getattr(e,'code',str(e))
            ok(c==200,f'internal link {l} -> {c}')
        else: ext.append(l)
    json.dump(ext,open(f'{EV}/external-links.json','w'))
    ok(set(external)<= set(), f'no request left the box during page loads: {sorted(set(external))}')
print(f"\nSUMMARY: {len(R['pass'])} pass, {len(R['fail'])} fail")
srv.shutdown(); sys.exit(1 if R['fail'] else 0)
