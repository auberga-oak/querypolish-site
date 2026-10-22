# Query Polish (querypolish.com): v1 status

Owner: Finansium AB. Built by Kent Beck (engineering). **Status: built and tested locally, NOT deployed.**
Last updated: 22 Oct 2026, Stockholm time (CEST).

## What is done
- Static site in `docs/` (ready for GitHub Pages "deploy from branch: main /docs", so tests/evidence are not served publicly).
  - `docs/index.html` landing + intake form, `docs/thanks/` confirmation, `docs/privacy/` privacy note, `docs/404.html`
  - `docs/assets/style.css`, `docs/assets/form.js` (fetch JSON submit, falls back to native POST with JS off)
  - `docs/CNAME` = `querypolish.com`, `.nojekyll`, `robots.txt`, `sitemap.xml`, `favicon.svg`
- Tests: `tests/run_tests.py` (+ `tests/contrast.js`). Run: `cd tests && QP_PORT=28765 python3 run_tests.py`. Result 22 Oct: **78 pass, 0 fail** (`evidence/test-output.txt`).
  - Every request that leaves 127.0.0.1 is aborted. The backend request is intercepted: aborted in one test, answered with a local mock `{"success":true}` in another. Nothing was ever sent to Web3Forms.
- Evidence in `evidence/`: screenshots at 360/390/1280 (+@2x for 390/1280), intercepted payload, form field list, lowest contrast pairs, landing copy for review (`evidence/landing-copy.txt`).

## Not done (needs a decision or approval)
1. Zinsser review of the copy (`evidence/landing-copy.txt`). Not live until signed off.
2. Backend: Web3Forms recommended, access key not created yet. `docs/index.html` holds placeholder `WEB3FORMS_ACCESS_KEY`.
3. GitHub repo: not created. Proposed `auberga-oak/querypolish-site`, public, Pages from `main` `/docs`.
4. DNS at Spaceship: not changed (records below).
5. Real end-to-end test submission (contact email warren.ekenberg@agentmail.to): not done.
6. Policy points for Henrik to confirm: contact address in privacy/thanks (henrik.ekenberg@finansium.se, same as Luck Habits), 12-month retention, "Stockholm, Sweden" in footer, no turnaround time promised.

## Form field mapping (source: /workspace/seo-prompts/sarvesh-top-20-grok-seo-prompts.md, "Parameters to fill in before running")
| Parameter | Form field (name) | Required |
|---|---|---|
| Business name exactly as on Google profile | Business name | yes |
| Owner's name | Owner name | no |
| Full address incl. suite/unit | Address | yes |
| Phone number | Phone | no |
| Website domain + website URL | Website (URL; domain derived from it) | yes |
| GBP URL | Google Business Profile URL | yes |
| Industry / business type | Industry | yes |
| Year founded / years in business | Year founded | no |
| Team size (solo/small/large) | Team size (select) | no |
| Main service | Main service | yes |
| Other services, up to 5 | Other services (one per line) | no |
| Main city | Main city | yes |
| Service-area cities, up to 5 | Service area cities | no |
| Neighbourhoods/areas, 3 | Neighbourhoods | no |
| Target customer | Target customer | no |
| Average job value | Average job value | no |
| 3–5 target keywords | Keyword 1–3 (required), Keyword 4–5 | 1–3 yes |
| Keywords ranked for now / should rank for | Keywords you rank for now / Keywords you should rank for | no |
| Service + city keyword for reviews | Review service keyword / Review city keyword | no |
| Competitor GBP URLs (3) | Competitor N GBP URL | yes |
| Competitor domains (3) | Competitor N domain | yes |
| Competitor name, why they beat you | Competitor N name / Competitor N why they beat you | no |
| Reviews total, rating, new per month | Google reviews total / Star rating / New reviews per month | no |
| GBP monthly views, monthly site visits | Monthly profile views / Monthly website visits | no |
| Map pack status | Map pack status | no |
| Biggest SEO problem | Biggest SEO problem | no |
| SEO already tried | SEO already tried | no |
| "Access the prompts assume" (Chrome, Search Console, Semrush, Ahrefs, GA4) | **Deliberately not asked.** No passwords or logins. | – |
| (added) contact email | email | yes |
| (added) consent | Consent (checkbox) | yes |

## Backend recommendation: Web3Forms (free plan)
- Free: 250 submissions/month, 30-day dashboard history, 1 recipient, hCaptcha/honeypot, custom redirect. Autoresponder is Pro-only, so none is sent. https://web3forms.com/pricing
- Setup: enter the receiving email on web3forms.com ("Create Access Key"); the key arrives by email at that inbox. https://docs.web3forms.com/getting-started/installation
- Key in public HTML: yes, by design ("Don't worry this can be public", same doc). It only lets someone send to our inbox.
- Submissions land: as email in the inbox the key was made for (proposed: a team AgentMail inbox the team can read), plus the Web3Forms dashboard.
- Alternatives: Formspree free (50/month, 30-day archive, account + email verification, form ID public; Google Sheets plugin is paid) https://formspree.io/plans · Google Apps Script web app writing to a Sheet (no third party; needs a Google account in a browser to create, deploy "Execute as me", access "Anyone"; web app URL is public) https://developers.google.com/apps-script/guides/web , quotas https://developers.google.com/apps-script/guides/services/quotas

## Deploy path
- `gh auth status`: logged in as `auberga-oak` (User), scopes gist, read:org, repo. git uses `gh auth git-credential` as the credential helper for github.com. `git ls-remote` on luck-ledger-site works. luckhabits.com Pages config: legacy build, main `/`, HTTPS enforced.
- `auberga-oak/querypolish-site` does not exist yet.

## DNS (checked 22 Oct 2026 via dns.google and cloudflare-dns.com DoH; `dig` is not installed on the box)
Current: NS launch1/launch2.spaceship.net; A 54.149.79.189, 34.216.117.25 (Spaceship parking, TTL 300); no AAAA, MX, TXT; www = NXDOMAIN. HTTP and HTTPS to the apex timed out (15 s).

Needed at Spaceship (after the repo has querypolish.com set as its custom domain; remove the two parking A records first):
| Type | Host | Value |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| AAAA | @ | 2606:50c0:8000::153 |
| AAAA | @ | 2606:50c0:8001::153 |
| AAAA | @ | 2606:50c0:8002::153 |
| AAAA | @ | 2606:50c0:8003::153 |
| CNAME | www | auberga-oak.github.io |
| TXT | _github-pages-challenge-auberga-oak | (value shown by GitHub, Profile Settings > Pages > Add a domain) |
No wildcard records. Source: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site and https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages

## Commits
- Local only (no remote): `1f98085` Query Polish v1: static intake site, tests, evidence. The README edit adding this hash is committed on top of it.
- Live: none yet.
## Submission location
- Not set up yet (proposed: Web3Forms -> team AgentMail inbox).

## Status 22 Oct 2026 13:27 (Stockholm)
- Copy approved by Zinsser; edits applied in cc6789b (78 pass, 0 fail).
- Repo created (empty, public): https://github.com/auberga-oak/querypolish-site. Push held for Henrik's placeholder confirmation.
- GitHub Pages domain verification pending: TXT `_github-pages-challenge-auberga-oak.querypolish.com` = `0b9c128da44537407369e446f0534a` (sent to Warren for Spaceship).
- Backend: Web3Forms free, receiving inbox warren.ekenberg@agentmail.to (key step: Warren).

## Branch `branching-v1` (22 Oct 2026, Stockholm time): first question that branches the form
Spec: `intake-branching-v1.md`, plus Warren's resolutions (22 Oct): competitors are optional (1–3) and the Google Business Profile links appear only for A; report language is English or Swedish, with English selected by default. **Not merged, not pushed. main is untouched at 54ca006.**
- Code commit: `ffe565b`. The README is updated in the commit after it.
- Tests: `cd tests && QP_PORT=28765 python3 run_tests.py`. Result: **156 pass, 0 fail** (`evidence/test-output.txt`). Nothing left the box; the backend request was aborted or answered with a local mock.
- Form source: `tools/build_form.py` regenerates the `<form>` body in `docs/index.html`. `tools/extract_copy.py` dumps all visible text.
- Copy diff for Zinsser: `evidence/copy-diff-branching.md` (raw: `evidence/copy-branching.udiff`).

### How the form behaves
- Q1 `business_type` (radio, required) is the first field. Its values are `local_listing`, `local_no_listing` and `online_only`.
- Sections tagged `data-branch` show only for their answer. With JS on, the controls in hidden sections are **disabled**, so they aren't validated or submitted, and stale values from a branch the user switched away from are dropped (tested A→B, B→C, C→A). Fields marked `data-breq` become required only while their section is visible.
- Required in every branch: business_type, Business name, email, Consent. Report language (`report_language`) defaults to English.
- Required for one branch only: A `Google Business Profile URL`; B `Address or service area`; C `Website (online)`.
- **No-JS fallback (chosen):** every section is shown and enabled, and only the common fields are required. Each branch section carries a "Fill in this part if you picked X above." note, and the branch-required fields say "(required if this is your answer above)" but aren't enforced. The native POST then includes the other branches' fields as **empty** values (tested). The team should read `business_type` first.

### Which fields stay where
| Field(s) | A | B | C | Reason |
|---|---|---|---|---|
| Business name (req), Owner's name, Year founded, Team size, Your best customer | ✓ | ✓ | ✓ | Prompt 0 context for everyone |
| Google Business Profile link (req), Full address | ✓ | | | GBP prompts 1–8, 13, 18, 19 |
| Business address or service area (req) | | ✓ | | Spec |
| Phone, Industry, Website, Main service, Other services, Cities you serve, Average job value | ✓ | ✓ | | Local services and market (spec: main service, cities, website) |
| Neighbourhoods | ✓ | | | Used only by GBP prompts 5–8 |
| Website (req), What you sell, Main country, Main language | | | ✓ | Spec |
| Competitor 1–3: name, website domain, why they beat you (all optional) | ✓ | ✓ | ✓ | Warren |
| Competitor 1–3 Google Business Profile link (optional) | ✓ | | | Warren |
| Keywords 1–5, searches you rank for / should rank for (all optional) | ✓ | ✓ | ✓ | Prompts 9, 16 and 17 run in every branch |
| Review service/city words | ✓ | | | Prompt 4, reviews on the profile |
| Google reviews, rating, new reviews per month, profile views, Maps top 3 | ✓ | | | Only meaningful with a listing |
| Monthly website visits, biggest search problem, what you've tried | ✓ | ✓ | ✓ | Prompt 0 |
| Email (req), Report language (English default), Consent (req) | ✓ | ✓ | ✓ | Spec |

### Conflicts with Warren's original brief (for the record)
1. The brief required 3 competitors, each a GBP URL plus a domain. **Resolved by Warren (22 Oct):** competitors are optional, and the GBP link is asked only in A.
2. The brief required the GBP link, full address, website, keywords 1–3, main service, main city and industry for everyone. These are now branch-specific or optional, following the spec. Main city is merged into "Cities you serve".
3. The brief's product framing is a "local-SEO audit"; branch C is online only. The title and H1 still say "local search". Left unchanged, for Warren and Zinsser to decide.
4. "Name" in the spec's "All: name, email" is read as **Business name (required)**. Owner's name stays optional.
5. The spec says "(optional, we'll find them if blank)" for A's competitors. The site makes **no** promise to find them. The hint is Warren's "the more you name, the better the audit". Add the promise only if the team commits to it.
6. The report can be in Swedish, but the site copy stays English, and the confirmation and thanks pages are English.
