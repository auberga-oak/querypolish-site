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
A,B,C='local_listing','local_no_listing','online_only'
COMMON_REQ={'business_type','Business name','email','Consent'}
BR_REQ={A:{'Google Business Profile URL'},B:{'Address or service area'},C:{'Website (online)'}}
A_ONLY={'Google Business Profile URL','Address','Neighbourhoods','Competitor 1 GBP URL','Competitor 2 GBP URL','Competitor 3 GBP URL',
 'Review service keyword','Review city keyword','Google reviews total','Star rating','New reviews per month','Monthly profile views','Map pack status'}
B_ONLY={'Address or service area'}
AB={'Phone','Industry','Website','Main service','Other services','Cities served','Average job value'}
C_ONLY={'Website (online)','What you sell','Main country','Main language'}
OWN={A:A_ONLY|AB,B:B_ONLY|AB,C:C_ONLY}
FOREIGN={k:(A_ONLY|B_ONLY|AB|C_ONLY)-OWN[k] for k in OWN}
LETTER={A:'A',B:'B',C:'C'}
COMMON_FILL={'Business name':'Test Plumbing AB','email':'warren.ekenberg@agentmail.to'}
VAL={'Google Business Profile URL':'https://maps.app.goo.gl/test0','Address':'Testgatan 1, 111 22 Stockholm','Neighbourhoods':'Södermalm',
 'Competitor 1 GBP URL':'https://maps.app.goo.gl/test1','Competitor 2 GBP URL':'https://maps.app.goo.gl/test2','Competitor 3 GBP URL':'https://maps.app.goo.gl/test3',
 'Review service keyword':'plumbing','Review city keyword':'Stockholm','Google reviews total':'12','Star rating':'4.5','New reviews per month':'2','Monthly profile views':'300','Map pack status':'top 3 for plumber',
 'Address or service area':'Greater Stockholm','Phone':'+46 8 000 000','Industry':'Plumber','Website':'https://example.com','Main service':'Emergency plumbing',
 'Other services':'Drains','Cities served':'Stockholm','Average job value':'4,000 SEK',
 'Website (online)':'https://shop.example.com','What you sell':'Online courses','Main country':'Sweden','Main language':'Swedish',
 'Competitor 1 domain':'example.org','Keyword 1':'plumber stockholm'}
def pick(p,br): p.check(f'input[name=business_type][value={br}]')
def fill_own(p,br):
    for k in sorted(OWN[br]): p.fill(f'[name="{k}"]',VAL[k])
def state(p):
    return p.evaluate("""()=>[...document.querySelectorAll('#intake [name]')].filter(e=>e.type!=='hidden').map(e=>({n:e.name,req:e.required,dis:e.disabled,vis:!!(e.offsetWidth||e.offsetHeight||e.getClientRects().length)}))""")
def invalid(p): return set(p.evaluate('[...document.querySelectorAll("#intake input:invalid,#intake select:invalid,#intake textarea:invalid")].map(e=>e.name)'))
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
                if path=='/' and dpr==1:
                    for br in (A,B,C):
                        pick(p,br); p.screenshot(path=f'{EV}/home-{LETTER[br]}-{w}.png',full_page=True)
                        sw2=p.evaluate('document.documentElement.scrollWidth'); ok(sw2<=w,f'branch {LETTER[br]} @{w}px: no horizontal overflow ({sw2})')
                    p.goto(BASE+path)
                sw=p.evaluate('document.documentElement.scrollWidth')
                ok(sw<=w, f'{path} @{w}px dpr{dpr}: no horizontal overflow (scrollWidth={sw})')
                if path!='/no-such-page/': ok(st==200,f'{path} status {st}')
                else: ok(st==404,f'404 page status {st}')
            ok(not errs, f'@{w}px dpr{dpr}: no console errors/warnings on any page (expected document 404 on /no-such-page/ excluded) {errs}')
            ctx.close()
    # 2. structure checks (JS on, no branch picked)
    ctx=b.new_context(viewport={'width':1280,'height':800}); ctx.route('**/*',guard); p=ctx.new_page(); p.goto(BASE+'/')
    names=p.eval_on_selector_all('#intake [name]','els=>els.map(e=>({n:e.name,t:e.type,r:e.required,branch:(e.closest("[data-branch]")||{}).dataset?.branch||null}))')
    json.dump(names,open(f'{EV}/form-fields.json','w'),indent=1)
    ok(p.evaluate('document.querySelector("#intake [name]:not([type=hidden]):not(.hp *)")?.name')=='business_type' or
       p.evaluate('[...document.querySelectorAll("#intake input,#intake select,#intake textarea")].find(e=>e.type!=="hidden"&&!e.closest(".hp")).name')=='business_type','Q1 business_type is the first field')
    ok(sorted(p.eval_on_selector_all('input[name=business_type]','e=>e.map(x=>x.value)'))==sorted([A,B,C]) and p.eval_on_selector('input[name=business_type]','e=>e.required'),'Q1 radios: local_listing/local_no_listing/online_only, required')
    ok('Not sure? If you can be found on Google Maps, pick A.' in p.inner_text('#q1'),'Q1 helper text present')
    ok(not any(n['t']=='password' or re.search(r'pass|login|user ?name',n['n'],re.I) for n in names),'no password/login fields')
    ok(p.locator('footer').inner_text().count('Finansium AB')>=1,'footer names Finansium AB')
    ok(p.eval_on_selector('#consent','e=>e.required&&e.type=="checkbox"'),'consent checkbox required')
    ok(p.eval_on_selector('[name=email]','e=>e.required&&e.type=="email"'),'email required, type=email')
    ok(p.eval_on_selector('#lang-en','e=>e.checked') and not p.eval_on_selector('#lang-sv','e=>e.checked'),'report language defaults to English')
    ok(sorted(p.eval_on_selector_all('input[name=report_language]','e=>e.map(x=>x.value)'))==['English','Swedish'],'report language options English/Swedish')
    st0=state(p); vis_branch=[x['n'] for x in st0 if x['n'] in (A_ONLY|B_ONLY|AB|C_ONLY) and (x['vis'] or not x['dis'])]
    ok(not vis_branch,f'no branch picked: all branch fields hidden+disabled {vis_branch}')
    posts=[]
    def backend(route):
        posts.append(route.request.post_data); route.abort()
    p.route('https://api.web3forms.com/**',backend)
    p.click('#submit'); p.wait_for_timeout(400)
    inv=invalid(p)
    ok(len(posts)==0 and inv==COMMON_REQ, f'empty submit blocked, invalid={sorted(inv)}, 0 requests')
    ok('required fields' in p.inner_text('#status'), 'status message shown on invalid: '+p.inner_text('#status'))
    ok(p.evaluate('document.activeElement.name')=='business_type','focus moved to first invalid field (Q1)')
    gbp=[f'Competitor {i} GBP URL' for i in (1,2,3)]
    ok(all(p.locator(f'[name="{n}"]').count()==1 for n in gbp),'3 competitor GBP URL fields exist in the DOM')
    # 3. per-branch: required set, visibility, competitor GBP, stale values, payload
    order=[(None,A),(A,B),(B,C),(C,A)]
    for prev,br in order:
        L=LETTER[br]
        p.goto(BASE+'/'); posts.clear()
        if prev:  # fill the previous branch fully, then switch: its values must not leak
            pick(p,prev); fill_own(p,prev)
        pick(p,br)
        st=state(p); byn={x['n']:x for x in st}
        reqset={x['n'] for x in st if x['req'] and not x['dis']}
        ok(reqset==COMMON_REQ|BR_REQ[br],f'{L}: required = {sorted(reqset)}')
        ok(all(byn[n]['vis'] and not byn[n]['dis'] for n in OWN[br]),f'{L}: own branch fields visible + enabled')
        bad=[n for n in FOREIGN[br] if byn[n]['vis'] or not byn[n]['dis'] or byn[n]['req']]
        ok(not bad,f'{L}: other-branch fields hidden, disabled, not required {bad}')
        on=[n for n in gbp if not byn[n]['dis'] and byn[n]['vis']]
        ok(on==(gbp if br==A else []),f'{L}: competitor GBP URL fields enabled+visible only in A (enabled here: {len(on)})')
        ok(not any(byn[f'Competitor {i} domain']['req'] for i in (1,2,3)) and all(byn[f'Competitor {i} domain']['vis'] for i in (1,2,3)),f'{L}: competitor domains shown, optional')
        ok(p.eval_on_selector('#lang-en','e=>e.checked'),f'{L}: report language still English by default')
        p.click('#submit'); p.wait_for_timeout(300)
        inv=invalid(p); ok(len(posts)==0 and inv==(COMMON_REQ-{'business_type'})|BR_REQ[br],f'{L}: submit with only Q1 blocked, invalid={sorted(inv)}')
        for k,v in COMMON_FILL.items(): p.fill(f'[name="{k}"]',v)
        p.check('#consent'); p.click('#submit'); p.wait_for_timeout(300)
        ok(len(posts)==0 and invalid(p)==BR_REQ[br],f'{L}: missing branch-required field blocks submit')
        for k in BR_REQ[br]: p.fill(f'[name="{k}"]',VAL[k])
        p.fill('[name="Competitor 1 domain"]',VAL['Competitor 1 domain']); p.fill('[name="Keyword 1"]',VAL['Keyword 1'])
        if br==C: p.check('#lang-sv')
        p.click('#submit'); p.wait_for_timeout(800)
        ok(len(posts)==1,f'{L}: valid submit fires exactly 1 backend request (aborted){" after switching from "+LETTER[prev] if prev else ""}')
        body=json.loads(posts[0]) if posts else {}
        json.dump(body,open(f'{EV}/payload-{L}{"-from-"+LETTER[prev] if prev else ""}.json','w'),indent=1,ensure_ascii=False)
        ok(body.get('business_type')==br,f'{L}: business_type = {body.get("business_type")}')
        leaked=sorted(set(body)&FOREIGN[br]); ok(not leaked,f'{L}: no other-branch fields in payload {leaked}')
        ok(all(body.get(k)==VAL[k] for k in BR_REQ[br]) and all(body.get(k)==v for k,v in COMMON_FILL.items()) and body.get('Consent')=='Yes',f'{L}: payload carries common + branch-required values + consent')
        ok(body.get('report_language')==('Swedish' if br==C else 'English'),f'{L}: report_language = {body.get("report_language")}')
        ok(body.get('access_key')=='c9f5ef0c-dc1b-4ead-8727-fabec3abdc98' and 'botcheck' not in body,f'{L}: payload has Web3Forms key, honeypot unchecked')
        st=p.inner_text('#status'); ok('not sent' in st and p.url.endswith('/'),f'{L}: aborted request -> error shown, stays on page')
        if prev is None: p.screenshot(path=f'{EV}/submit-aborted-1280.png')
    # invalid email still blocks (branch A)
    p.goto(BASE+'/'); posts.clear(); pick(p,A)
    for k,v in COMMON_FILL.items(): p.fill(f'[name="{k}"]',v)
    p.fill('[name="Google Business Profile URL"]',VAL['Google Business Profile URL']); p.check('#consent'); p.fill('[name=email]','not-an-email'); p.click('#submit'); p.wait_for_timeout(300)
    ok(len(posts)==0,'invalid email blocks submit')
    # 5. mocked success (fulfilled locally, nothing leaves the box)
    p.fill('[name=email]',COMMON_FILL['email'])
    p.unroute('https://api.web3forms.com/**'); posts2=[]
    def mock(route):
        posts2.append(route.request.post_data); route.fulfill(status=200,content_type='application/json',body='{"success":true,"message":"mock"}')
    p.route('https://api.web3forms.com/**',mock)
    p.click('#submit'); p.wait_for_url(BASE+'/thanks/',timeout=5000)
    ok(p.url==BASE+'/thanks/' and len(posts2)==1,'mocked success -> /thanks/')
    ok("We'll email the report" in p.inner_text('main'),'thanks page says we will email the report')
    ctx.close()
    # 6. JS off: everything shown, only common fields required, native POST
    for w in (360,390,1280):
        ctx=b.new_context(java_script_enabled=False,viewport={'width':w,'height':800}); nat=[]
        def mk(nat):
          def g2(route):
            u=route.request.url
            if u.startswith(BASE): return route.continue_()
            nat.append((u,route.request.method,route.request.post_data)); route.abort()
          return g2
        ctx.route('**/*',mk(nat)); p=ctx.new_page(); p.goto(BASE+'/')
        p.screenshot(path=f'{EV}/home-nojs-{w}.png',full_page=True)
        sw=p.evaluate('document.documentElement.scrollWidth'); ok(sw<=w,f'JS off @{w}px: no horizontal overflow ({sw})')
        if w!=390: ctx.close(); continue
        st=state(p)
        ok(all(x['vis'] and not x['dis'] for x in st if x['n'] not in ('botcheck',)),'JS off: every section visible and enabled')
        reqset={x['n'] for x in st if x['req']}; ok(reqset==COMMON_REQ,f'JS off: only common fields required {sorted(reqset)}')
        ok(p.locator('.nojs-only').first.is_visible() and not p.locator('.req-js').first.is_visible(),'JS off: "fill in this part if you picked…" notes shown, branch stars hidden')
        ok(p.eval_on_selector('#lang-en','e=>e.checked'),'JS off: report language defaults to English')
        p.click('#submit'); p.wait_for_timeout(500)
        ok(len(nat)==0,'JS off: empty submit blocked by native validation')
        pick(p,C)
        for k,v in COMMON_FILL.items(): p.fill(f'[name="{k}"]',v)
        p.check('#consent')
        try:
            with p.expect_request('https://api.web3forms.com/**',timeout=4000): p.click('#submit')
        except Exception: pass
        p.wait_for_timeout(500)
        from urllib.parse import parse_qs
        q=parse_qs(nat[0][2] or '',keep_blank_values=True) if nat else {}
        json.dump(q,open(f'{EV}/payload-nojs.json','w'),indent=1,ensure_ascii=False)
        ok(len(nat)==1 and nat[0][1]=='POST' and q.get('redirect')==['https://querypolish.com/thanks/'],'JS off: native POST to Web3Forms with redirect to /thanks/ (aborted)')
        ok(q.get('business_type')==[C] and q.get('report_language')==['English'],'JS off: business_type=online_only, report_language=English in POST')
        ok(all(q.get(k)==[''] for k in FOREIGN[C]),'JS off (documented): other-branch fields are sent, but empty')
        ctx.close()
    # 7. contrast
    ctx=b.new_context(viewport={'width':1280,'height':800}); ctx.route('**/*',guard); p=ctx.new_page()
    js=open('/workspace/querypolish/tests/contrast.js').read(); allc=[]
    for path in PAGES[:3]:
        p.goto(BASE+path); res=p.evaluate(js); allc+= [dict(r,page=path) for r in res]
    for br in (A,B,C):
        p.goto(BASE+'/'); pick(p,br); allc+=[dict(r,page='/ '+LETTER[br]) for r in p.evaluate(js)]
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
