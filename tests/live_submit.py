"""ONE real submission through the live page (headless Chrome). ALREADY RUN 22 Oct 2026 16:46 CEST; do not re-run without a new go-ahead.
Note: the first run lost the response body because the page navigated to thanks/ first; this version reads it inside a response handler."""
import json, datetime, zoneinfo, os, sys
EMAIL=os.environ.get('QP_LIVE_EMAIL') or sys.exit('set QP_LIVE_EMAIL to the team inbox (not committed)')
from playwright.sync_api import sync_playwright
BASE='https://auberga-oak.github.io/querypolish-site/'; EV='/workspace/querypolish/evidence'; TZ=zoneinfo.ZoneInfo('Europe/Stockholm')
rec={'attempt':1}
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
    ctx=b.new_context(viewport={'width':1280,'height':900}); p=ctx.new_page()
    resp={}; p.on('response',lambda r: ('api.web3forms.com/submit' in r.url) and resp.update(status=r.status,body=r.text()))
    reqs=[]; p.on('request',lambda r: 'web3forms' in r.url and reqs.append({'url':r.url,'method':r.method}))
    p.goto(BASE); p.fill('[name=Website]','https://querypolish.com'); p.fill('[name=email]',EMAIL)
    p.fill('[name=Notes]','TEST submission by Kent Beck, please ignore.'); p.check('#consent')
    with p.expect_response(lambda r:'api.web3forms.com/submit' in r.url and r.request.method=='POST',timeout=30000) as ri:
        rec['submit_time_stockholm']=datetime.datetime.now(TZ).isoformat(timespec='seconds')
        p.click('#submit')
    p.wait_for_timeout(500); rec['response']=resp
    try: p.wait_for_url(BASE+'thanks/',timeout=20000)
    except Exception: pass
    rec['final_url']=p.url; rec['landed_on_thanks']=p.url==BASE+'thanks/'; rec['status_text']=p.inner_text('#status') if p.locator('#status').count() else ''
    rec['web3forms_requests']=reqs
    p.screenshot(path=f'{EV}/live-submit-result.png',full_page=True)
    b.close()
json.dump(rec,open(f'{EV}/live-submit-result.json','w'),indent=1,ensure_ascii=False); print(json.dumps(rec,indent=1,ensure_ascii=False))
