# Copy diff: `copy-ai-v1` (draft, NOT deployed) vs main fcf600d (live test site)

The copy borrows from Henrik's Swedish reference page ("Köparen frågar AI. Svaret nämner er inte."), translated into English and adapted to the free audit. The form, the test banner, noindex, the thanks page, the privacy page and the footer are unchanged. Zinsser to gate every line below. Screenshots: `evidence/ai-home-390.png`, `evidence/ai-home-1280.png`.

## Changed
| # | Where | Old | New |
|---|---|---|---|
| 1 | `<title>` | Query Polish: a free search audit for your business | Query Polish: does the AI answer mention you? A free audit |
| 2 | Meta description | A free audit of how your business shows up in Google search and Google Maps, compared with your closest competitors. The report comes by email. | Your customers ask ChatGPT, Perplexity, Google AI Overviews and Google. A free audit of whether the answers mention your business. The report comes by email. |
| 3 | H1 | A free audit of how your business shows up in search | Your customers ask AI. Does the answer mention you? |
| 4 | Hero lead | Tell us your website. We compare your Google Business Profile, if you have one, and your website with your closest competitors for the searches your customers use, and email you a written report. | People ask ChatGPT, Perplexity, Google AI Overviews and Google which business to choose. Our free audit shows whether the answers mention you, and what to change on your website and Google Business Profile so they can. A person reads every report before we send it. |
| 5 | How it works, step 2 | We look at public information: your profile if you have one, your website, and your closest competitors. | …your website, and your closest competitors. **We also put the questions your customers ask to ChatGPT, Perplexity, Google AI Overviews and Google.** |
| 6 | How it works, step 3 | We email the report to the address you give us. | **A person reads the report first. Then** we email it to the address you give us. |
| 7 | Note | We never ask for passwords or logins. The audit uses only what you tell us and what anyone can see on Google and on the web. | …and on the web. **We only ask for access to Google Search Console and Google Analytics if you say yes to more work after the report.** |
| 8 | Privacy section (home) | …You can ask us to delete it at any time. The privacy note has the details. | …The privacy note has the details. **This page stores nothing. We only receive what you send in the form.** |

## New
- **Example section** (from the reference page's ExampleCo, made local):
  - H2 "An example"
  - "ExampleCo is invented. This is what it looks like when the answers include the website."
  - Question: "Who can fix a blocked drain in Uppsala today?"
  - Google: "ExampleCo Plumbing: same-day drain repair in Uppsala" · example.com
  - ChatGPT: "ExampleCo can usually come the same day in central Uppsala." · example.com
  - Perplexity: "Sources: ExampleCo emergency plumbing" · example.com/emergency
  - Google AI Overviews: "ExampleCo offers same-day drain repair in Uppsala." · example.com/prices
- **What the audit covers, new intro and three steps** (Lästa / Hittade / Nämnda):
  - "An AI model can't mention a business it hasn't read. The same goes for Google. The audit looks at the website you already have and asks three questions."
  - "**Read.** Can Google, and the crawlers that AI tools send, see every page you already have?"
  - "**Found.** When a customer asks a question, does the right page come up? Two of your pages shouldn't compete for the same question."
  - "**Mentioned.** Do the answers name your business and link to your site? Where an answer is wrong, the fix belongs on your site, not in the chat."
  - "It also covers:" (this introduces the 4 existing bullets)

## Unchanged
- The test banner and the "Request the audit" links.
- The 4 "covers" bullets and "Each finding comes with…".
- How it works, step 1.
- The rest of the home Privacy section.
- The whole form (Website *, Anything else…, email *, Report language, consent, button, messages).
- The footer, the thanks page, the privacy page and the 404 page. The contact is still henrik.ekenberg@finansium.se.

## Deliberately NOT taken from the reference
- The 10 000 kr/month price and the daily-change subscription ("en ändring varje vardag", the Monday report).
- "Not for shops or restaurants": v1 audits local businesses too.
- contact@querypolish.com: the contact stays henrik.ekenberg@finansium.se.
- The mailto-only form: Web3Forms stays.

The tests check that all four are absent: no price or "kr" text, no `contact@` anywhere, no `mailto:` in the form, the form posts to Web3Forms, no "not for shops/restaurants", no daily-change wording.

## Flags for Warren and Zinsser
1. **Scope promise:** the copy now promises that the audit checks the AI answers (ChatGPT, Perplexity, Google AI Overviews, Google). The current audit prompts (Sarvesh 0–20) don't do that, so the audit procedure has to add it before this copy goes live.
2. **"A person reads every report before we send it":** this is a process commitment. Someone has to own it.
3. **"This page stores nothing":** true for the page itself (no cookies, no analytics), but Web3Forms stores the submissions (30-day dashboard). The privacy page already names Web3Forms. Check that the wording isn't read as "nothing is stored anywhere".
4. **Search Console / GA4 vs "We never ask for passwords or logins":** access is granted by adding us as a user, not with a password. Zinsser may want to say that explicitly.
5. **H1 as a question:** the reference states it flatly ("The answer doesn't mention you"). I used a question because the free audit doesn't know the answer yet.
