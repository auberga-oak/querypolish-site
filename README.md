# Query Polish: PRODUCTION status

Owner: Finansium AB. Engineering: Kent Beck. Updated 31 Oct 2026, Stockholm time (CET).

## Live (production)
- **Go-live approved by Henrik on 31 Oct 2026, 17:03 Stockholm time** ("Go live: Kent takes the site out of test mode and adds the domain").
- **URL:** https://querypolish.com/ (also `/privacy/` and `/thanks/`). GitHub Pages from `main` `/docs`, custom domain set by `docs/CNAME` (`querypolish.com`) and the Pages API. `www.querypolish.com` should redirect to the apex. The old https://auberga-oak.github.io/querypolish-site/ URL redirects to the domain once it is attached.
- Commit 2329a32: test banner and `noindex, nofollow` removed from every page. `thanks/` keeps `<meta name="robots" content="noindex">` because it is a post-submit page. `robots.txt` allows crawling and points to `https://querypolish.com/sitemap.xml`. `sitemap.xml` lists `/` and `/privacy/`, and leaves `/thanks/` out. The home page has canonical and og:url `https://querypolish.com/`, and privacy has canonical `https://querypolish.com/privacy/`. `404.html` now uses root-absolute paths (`/assets/...`), and the other pages use relative paths, which work at the root.
- The form is open for real requests. Its no-JS redirect is `https://querypolish.com/thanks/`.
- DNS at Spaceship follows `DNS-spaceship.md` (untracked). MX/email forwarding is not touched by this repo.
- **Still waiting on Henrik's own browser submission**: the live form check has to come from a normal browser, because Web3Forms blocks the box's IP (403 on the CORS preflight, 23 Oct). The tests mock the backend and send nothing.

## Form
- Required: **Website** (url) and **email**, plus the **Consent** checkbox. Optional: "Anything else you'd like us to know" (`Notes`). Report language is English by default, with Swedish as the other option. No branching, no detail fields.
- Backend: Web3Forms, key `c9f5ef0c-dc1b-4ead-8727-fabec3abdc98` (public by design). Redirect for no-JS posts: https://querypolish.com/thanks/

## Where submissions land
- **The team's AgentMail inbox and the Web3Forms dashboard.** Mail comes from `Query Polish intake form <notify@web3forms.com>` with the subject "New Query Polish audit request". The dashboard keeps 30 days of history on the free plan.

## Live end-to-end test (1 real submission, 1 attempt)
- Submitted at about **16:46:38–39 CEST, 22 Oct 2026**, through the live page in headless Chrome. Website https://querypolish.com, email [team inbox], notes "TEST submission by Kent Beck, please ignore.", consent ticked.
- Result: the page navigated to `thanks/`. form.js only does that on an OK response with `success` not false. The script failed to save the response body and the screenshot because the navigation came first (fixed in `tests/live_submit.py`, which must not be re-run without a go-ahead; it reads the inbox address from `QP_LIVE_EMAIL`, which isn't committed).
- **The email arrived at 16:46:39 CEST** in [team inbox] (thread `09de4a82-f5b1-43bb-8b0b-bf67942cf558`): Website, Notes, email, report_language=English, Consent=Yes. I only read it; nothing was sent, replied to or forwarded.
- Record: `evidence/live-submit-result.json`.

## Tests
- **Production (31 Oct, 2329a32):** `cd tests && QP_EXPECT=copy-ai QP_PORT=28782 python3 run_tests.py` now serves `docs/` at the root, like querypolish.com. Result: **200 pass, 0 fail** (`evidence/test-output.txt`). The live run against https://querypolish.com is recorded below once DNS and HTTPS are ready. The production checks cover: no banner, no noindex (except thanks/), robots allows crawling plus the Sitemap line, sitemap.xml, CNAME, canonical/og:url, 404 at root and at depth, the redirect URL, and that the form is open. The backend is aborted or mocked.
- Older (test deploy, subpath):
- `cd tests && QP_PORT=28765 python3 run_tests.py` serves `docs/` locally under `/querypolish-site/`. Result: **126 pass, 0 fail** (`evidence/test-output.txt`).
- `QP_BASE=https://auberga-oak.github.io/querypolish-site python3 run_tests.py` runs the same checks against the live site. Result: **126 pass, 0 fail** (`evidence/live-test-output.txt`).
- Both runs intercept the backend request (abort or a local mock), so the test runs send nothing. The test email defaults to `test@example.com` (override with `QP_TEST_EMAIL`).
- Coverage: the 3 required fields, banner and noindex on every page, the aborted submit and its payload, JS off, 360/390/1280 px (plus @2x), console errors, contrast (min 4.61:1), links and anchors, no root-absolute paths outside the subpath, robots/sitemap/CNAME.

## Evidence
- Local renders: `evidence/{home,thanks,privacy,404}-{360,390,1280}.png`, `home-*@2x.png`, `home-nojs-*.png`, `submit-aborted-1280.png`
- Live renders: `evidence/live-*.png` (the same set), `live-payload-aborted.json`, `live-payload-nojs.json`, `live-contrast-lowest.json`
- Copy diff for Zinsser: `evidence/copy-diff-simple.md`. Older: `copy-diff-branching.md`.

## Commits
- v1: 1f98085, 9e4445e, cc6789b, 27b5f95, c6d2f7c, 54ca006
- branching-v1: ffe565b, 8383563, 348cdde, b56f60e, ea93552
- simple-test: 6dd43a7. Merged into main as **debc9be** (first deploy).
- The README and live evidence are committed on top of debc9be (see `git log`).
- fcf600d: README and live evidence. 4a10f26: receiving inbox address removed from tracked files; Zinsser edit "Your Google Business Profile, if we can find one: categories,". 94e96c0: README + live evidence.
- **23 Oct 2026: copy-ai-v1 (2318b48) deployed** (Henrik approved 06:29). Merged into main as **40b4617** (merge commit; the branches had diverged, so no fast-forward). Pages build for 40b4617 finished 06:31 CEST. Tests: local 179/179, live 179/179 (`evidence/test-output.txt`, `evidence/live-test-output.txt`). Screenshots: `evidence/live-ai-home-390.png`, `evidence/live-ai-home-1280.png`.
- **23 Oct, fca471b:** review line made general: "A Finansium SEO expert reads every report before it is sent." (was "Henrik reads…"; Henrik asked 06:48). README in the following commit.
- **23 Oct live test submission FAILED (2 attempts, about 06:32 and 06:33:53 CEST).** Web3Forms answered the browser's CORS preflight with 403 and no Access-Control-Allow-Origin header, and a plain OPTIONS probe from the box got 403 "This method is not allowed. Use our API in client side…". It looks as if Web3Forms is treating this box's IP as a server. Nothing reached the team inbox. This needs checking from a normal browser before the form can be trusted. `evidence/live-submit-2-result.json/.png`.
- fcf600d: README and live evidence. 4a10f26: receiving inbox address removed from tracked files; Zinsser edit "Your Google Business Profile, if we can find one: categories," (live, verified 22 Oct 16:58 CEST; live render checks 126/126).
- Branch `copy-ai-v1` (7fcb045, local only, NOT pushed or deployed): AI-answer copy draft, see `evidence/copy-diff-ai.md` on that branch.

## Known issues and flags
- The public repo history includes `tests/v1-evidence/` (scraped third-party pages from earlier Luck Habits research) and `backups/`. They were removed from the tree in 6dd43a7 but are still in history, and older commits show the receiving inbox address. It was removed from all current files on main on 22 Oct. Rewriting history needs a force push, so I haven't done it.
- The box can't reach plain HTTP (port 80), so I didn't verify the HTTP to HTTPS redirect from here. HTTPS returns 200.
