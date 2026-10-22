# Query Polish: TEST deploy status

Owner: Finansium AB. Engineering: Kent Beck. Updated 22 Oct 2026, 16:50 Stockholm time (CEST).

## Live (test only)
- **URL:** https://auberga-oak.github.io/querypolish-site/ (also `thanks/` and `privacy/`). GitHub Pages from `main` `/docs`, HTTPS enforced, **no custom domain** (no `docs/CNAME`).
- Repo: https://github.com/auberga-oak/querypolish-site (public). The first Pages build (debc9be) finished at 16:36:32 CEST.
- Every page shows a test banner ("Test version. This site is being tested and isn't open for requests yet.") and has `<meta name="robots" content="noindex, nofollow">`. `robots.txt` is `Disallow: /`, but it sits under the project subpath, so crawlers won't read it there; the meta noindex is what counts. There's no sitemap. All paths are relative except `404.html`, which needs absolute `/querypolish-site/` paths because Pages serves it at any depth.
- querypolish.com DNS is unchanged (still Spaceship parking).

## Form
- Required: **Website** (url) and **email**, plus the **Consent** checkbox. Optional: "Anything else you'd like us to know" (`Notes`). Report language is English by default, with Swedish as the other option. No branching, no detail fields.
- Backend: Web3Forms, key `c9f5ef0c-dc1b-4ead-8727-fabec3abdc98` (public by design). Redirect for no-JS posts: https://auberga-oak.github.io/querypolish-site/thanks/

## Where submissions land
- Email to **warren.ekenberg@agentmail.to** (from `Query Polish intake form <notify@web3forms.com>`, subject "New Query Polish audit request").
- The **Web3Forms dashboard** for that key (free plan: 30-day history).

## Live end-to-end test (1 real submission, 1 attempt)
- Submitted at about **16:46:38–39 CEST, 22 Oct 2026**, through the live page in headless Chrome. Website https://querypolish.com, email warren.ekenberg@agentmail.to, notes "TEST submission by Kent Beck, please ignore.", consent ticked.
- Result: the page navigated to `thanks/`. form.js only does that on an OK response with `success` not false. The script failed to save the response body and the screenshot because the navigation came first (fixed in `tests/live_submit.py`, which must not be re-run without a go-ahead).
- **The email arrived at 16:46:39 CEST** in warren.ekenberg@agentmail.to (thread `09de4a82-f5b1-43bb-8b0b-bf67942cf558`): Website, Notes, email, report_language=English, Consent=Yes. I only read it; nothing was sent, replied to or forwarded.
- Record: `evidence/live-submit-result.json`.

## Tests
- `cd tests && QP_PORT=28765 python3 run_tests.py` serves `docs/` locally under `/querypolish-site/`. Result: **126 pass, 0 fail** (`evidence/test-output.txt`).
- `QP_BASE=https://auberga-oak.github.io/querypolish-site python3 run_tests.py` runs the same checks against the live site. Result: **126 pass, 0 fail** (`evidence/live-test-output.txt`).
- Both runs intercept the backend request (abort or a local mock), so the test runs send nothing.
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

## Known issues and flags
- The public repo history includes `tests/v1-evidence/` (scraped third-party pages from earlier Luck Habits research) and `backups/`. They were removed from the tree in 6dd43a7 but are still in history, and the evidence JSON shows the receiving inbox address. Rewriting history needs a force push, so I haven't done it.
- The box can't reach plain HTTP (port 80), so I didn't verify the HTTP to HTTPS redirect from here. HTTPS returns 200.
