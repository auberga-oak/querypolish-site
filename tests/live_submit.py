"""ONE real submission through the live page (headless Chrome). Run 1: 22 Oct 2026 16:46 CEST. Run 2: 23 Oct 2026 after copy-ai-v1 deploy. Do not re-run without a new go-ahead.
Note: the first run lost the response body because the page navigated to thanks/ first; this version reads it inside a response handler."""
import json, datetime, zoneinfo, os, sys
EMAIL=os.environ.get('QP_LIVE_EMAIL') or sys.exit('set QP_LIVE_EMAIL to the team inbox (not committed)')
from playwright.sync_api import sync_playwright
BASE='https://auberga-oak.github.io/querypolish-site/'; EV='/workspace/querypolish/evidence'; TZ=zoneinfo.ZoneInfo('Europe/Stockholm')
SITE=os.environ.get('QP_LIVE_SITE','https://querypolish.com'); NOTE=os.environ.get('QP_LIVE_NOTE','TEST submission by Kent Beck, please ignore.'); OUT=os.environ.get('QP_LIVE_OUT','live-submit-result')
rec={'attempt':int(os.environ.get('QP_LIVE_ATTEMPT','1')),'website':SITE,'notes':NOTE}
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    ctx=b.new_context(viewport={'width':1280,'height':900}); p=ctx.new_page()
    resp={}; cons=[]
    # Do not read the body inside an event handler: in the sync API that blocks the dispatcher (attempt 1 on 23 Oct timed out this way).
    p.on('response',lambda r: ('api.web3forms.com/submit' in r.url) and resp.update(status=r.status,status_text=r.status_text))
    p.on('console',lambda m: cons.append(m.type+': '+m.text))
    reqs=[]; p.on('request',lambda r: 'web3forms' in r.url and reqs.append({'url':r.url,'method':r.method}))
    p.goto(BASE); p.fill('[name=Website]',SITE); p.fill('[name=email]',EMAIL)
    p.fill('[name=Notes]',NOTE); p.check('#consent')
    rec['submit_time_stockholm']=datetime.datetime.now(TZ).isoformat(timespec='seconds')
    p.click('#submit')
    p.wait_for_timeout(500)
    try: p.wait_for_url(BASE+'thanks/',timeout=20000)
    except Exception: pass
    rec['final_url']=p.url; rec['landed_on_thanks']=p.url==BASE+'thanks/'; rec['status_text']=p.inner_text('#status') if p.locator('#status').count() else ''
    rec['response']=resp; rec['web3forms_requests']=reqs; rec['console']=cons
    p.screenshot(path=f'{EV}/{OUT}.png',full_page=True)
    b.close()
json.dump(rec,open(f'{EV}/{OUT}.json','w'),indent=1,ensure_ascii=False); print(json.dumps(rec,indent=1,ensure_ascii=False).replace(EMAIL,'[team inbox]'))
