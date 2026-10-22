# Copy diff: branching-v1 vs main (54ca006)

Every user-visible text change. Zinsser must re-gate each item marked **NEW** or **CHANGED**. Anything not listed here is unchanged from Zinsser's approved wording on main. Site copy is English only. The raw text diff is in `evidence/copy-branching.udiff`, and the full new copy is in `evidence/landing-copy.txt`.

## 1. Landing page (outside the form)
| # | Where | Old (main) | New (branching-v1) | Why |
|---|---|---|---|---|
| 1 | Meta description | …compared with three competitors you choose. The report comes by email. | …compared with **up to three** competitors you choose. The report comes by email. | Competitors are now optional, 1–3 |
| 2 | Hero lead | Tell us about your business and three competitors. We compare your Google Business Profile and website with theirs for the searches you care about, and email you a written report. | Tell us about your business and **up to three** competitors. We compare your Google Business Profile**, if you have one,** and your website with theirs for the searches you care about, and email you a written report. | Branches B and C have no profile |
| 3 | Covers, bullet 1 | Your Google Business Profile: categories, attributes, services, description, photos and posts, set against what your competitors do. | …set against what your competitors do. **If you don't have a profile yet, the report starts with how to set one up.** | Spec: for B, "Create your Google Business Profile" is the top quick win |
| 4 | Covers, bullet 2 | Your reviews: how many you have, … | Your **Google** reviews**, if you have a profile**: how many you have, … | Spec: prompt 13 runs only for A |
| 5 | Covers, bullet 3 | …and which **local** topics your competitors cover that you don't. | …and which topics your competitors cover that you don't. | C is not local |
| 6 | Covers, bullet 4 | Your business details: whether your name, address and phone number match across the web. | …match across the web. **For online-only businesses, we check your profiles on directories, social sites and marketplaces instead.** | Spec: prompt 15 is adapted for C |
| 7 | How it works, step 2 | We look at public information: your profile, your website, and the three competitors you name. | We look at public information: your profile **if you have one**, your website, and the competitors you name. | Optional profile, optional competitors |

These stay as they were on purpose, so please confirm them:
- The title "Query Polish: a free local search audit" and the H1 "A free audit of how your business shows up in local search". Both are now arguably inaccurate for branch C (online only), but changing the positioning is Warren's call, so I've flagged it rather than changed it.
- "It takes about ten minutes. Only the fields marked with a star are required." Still true (fewer required fields, so if anything it's quicker).

## 2. Form: new question 1 (all **NEW**)
- Legend: **How do your customers find you?** * (required)
- Helper: **Not sure? If you can be found on Google Maps, pick A.**
- **A. I'm a local business with a Google Maps listing** (customers visit me, or I visit them in my area)
- **B. I'm a local business but I don't have a Google Maps listing yet**
- **C. I'm online only** (no shop or service area, e.g. e-commerce, SaaS, newsletter, online courses)
(Verbatim from intake-branching-v1.md, with the letters A/B/C added because the helper text refers to "A".)

## 3. Form: changed or new labels and hints
| # | Field | Old | New | Status |
|---|---|---|---|---|
| 8 | Business name hint | Exactly as it appears on your Google Business Profile. | Exactly as it appears on your Google Business Profile**, if you have one.** | CHANGED |
| 9 | Full address (A) | required *, in "Your business" | optional, under the new legend "**Your Google Maps listing**" | CHANGED (moved) |
| 10 | Your Google Business Profile link | required *, in "Your business" | under "Your Google Maps listing", required for A only | moved |
| 11 | Legend (B) | – | **Where you work** | NEW |
| 12 | Field (B) | – | **Business address or service area** * · hint: **Your street address if customers visit you, or the area you cover if you visit them.** | NEW |
| 13 | Phone hint | As shown on your profile. | As shown on your profile **or website**. | CHANGED |
| 14 | Industry, Website, Main service | each required * | each optional (A/B section) | CHANGED |
| 15 | Main city * + Other cities you serve (Up to 5, one per line.) | two fields | one field: **Cities you serve** · hint: **Up to 5, one per line. Put your main city first.** | CHANGED |
| 16 | Legend (C) | – | **Your online business** | NEW |
| 17 | Fields (C) | – | **Website address** * · **What you sell** (hint: **Your main products or services, in a sentence or two.**) · **Main country** (hint: **Where most of your customers are.**) · **Main language** (hint: **The language your customers search in.**) | NEW |
| 18 | Competitors legend | Three competitors | **Competitors** (optional) | CHANGED |
| 19 | Competitors hint | The three businesses that most often show up above you in search. We need each one's Google Business Profile link and website. | **Up to three businesses that most often show up above you in search. Each one you name gives us more to compare. Leave blank and we'll pick likely competitors from public search.** | CHANGED (Warren's requested hint) |
| 20 | Competitor N: Google Business Profile link / Website domain | both required *, link listed first | both optional, domain first; the link appears only for answer A | CHANGED |
| 21 | Keywords legend | Keywords | Keywords **(all optional)** | CHANGED |
| 22 | Keywords hint | The searches you most want to show up for, such as "plumber in Uppsala". Three are required, five are better. | The searches you most want to show up for, such as "plumber in Uppsala". **Up to five.** | CHANGED |
| 23 | Keyword 1–3 | required * | (optional) | CHANGED |
| 24 | Report language | – | **Report language**: **English** (selected by default) / **Swedish** | NEW |

Field order also changed (no wording change): "Your best customer" moved into "Your business", and in "Current numbers", "Monthly website visits" now comes after "Google Maps top 3".

## 4. Without JavaScript only (**NEW**, hidden when JS is on)
- At the top of each branch section: **Fill in this part if you picked A above.** / **…B above.** / **…A or B above.** / **…C above.**
- Next to each branch-required field, instead of the star: **(required for this answer)**

## 5. Privacy page
| # | Old | New |
|---|---|---|
| 25 | What we collect. What you type into the audit form: details about your business, your services and market, the searches you want to show up for, three competitors, any numbers you choose to share, and your email address. … | What we collect. What you type into the audit form: **how your customers find you,** details about your business, your services and market, the searches you want to show up for, **up to three** competitors, any numbers you choose to share, your email address **and the language you want the report in**. … |

## 6. Unchanged
- The "What the audit covers" closing line, the note, the Privacy section, the button text, error and status messages, the consent text, the thanks page, the 404 page, the footer and the rest of the privacy page are all unchanged.
