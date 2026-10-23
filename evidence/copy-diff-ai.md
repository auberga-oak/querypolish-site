# Copy diff: `copy-ai-v1` (draft, NOT deployed) vs main `4a10f26` (live test site)

Revision 2. Applies Warren's rulings (no claim that we check AI answers; "Henrik reads every report before it is sent.") and Zinsser's lines (i) to (iv). Form, test banner, noindex, thanks page, 404 and footer are unchanged. Screenshots: `evidence/ai-home-390.png`, `evidence/ai-home-1280.png`.

Status key: **GATED** = wording supplied by Zinsser or Warren, used verbatim. **NEW, UNGATED** = my wording, Zinsser to gate. **CHANGED, UNGATED** = Zinsser's line with a change I had to make (reason given).

## Retention check (Zinsser line ii)
Zinsser's draft said Web3Forms "keeps it for 30 days". Web3Forms' own pricing page, https://web3forms.com/pricing (fetched 22 Oct 2026, 16:53 CEST), says otherwise:
- "Form Submission History: How far back the dashboard lists your submissions. Data is retained longer — see Data Retention Policy below." Free: **30 days**.
- "Data Retention Policy: How long submission data is kept before permanent deletion. Set per form from 7 days to 3 years". Free: **Up to 3 years**.

So 30 days is only how far back the dashboard *lists* submissions; it is not how long Web3Forms keeps them. I used "the period set for our form: between 7 days and 3 years on its free plan". **Action for someone with the Web3Forms login (not me):** read or set the retention for this form in the dashboard, then replace the range with the real figure (for example "30 days"). The email copy in our own inbox is kept separately and is not covered by this line.

## Cookies and analytics check (Zinsser line ii)
- The page loads one script, `assets/form.js` (same origin). No hCaptcha, no analytics, no fonts, no third-party request: the test suite routes every request and records anything leaving the site origin; result `[]`.
- `document.cookie` is empty and the browser context holds no cookies after loading every page (new test, all pages).
- Live GitHub Pages response headers carry no `Set-Cookie` (curl -I, 22 Oct 2026).
- So "This page uses no cookies or analytics." is true today. If hCaptcha or analytics is ever added, this line has to change. The tests will fail if that happens.

## Changed lines
| # | Where | Old (live main) | New (draft) | Status |
|---|---|---|---|---|
| 1 | `<title>` | Query Polish: a free search audit for your business | Query Polish: a free audit of how Google and AI tools read your site | NEW, UNGATED |
| 2 | Meta description | A free audit of how your business shows up in Google search and Google Maps, compared with your closest competitors. The report comes by email. | Your customers ask ChatGPT, Perplexity, Google AI Overviews and Google. A free audit of whether they can read and find your website. The report comes by email. | NEW, UNGATED |
| 3 | H1 | A free audit of how your business shows up in search | Your customers ask AI. Make sure it can read your site. | NEW, UNGATED |
| 4 | Hero lead | Tell us your website. We compare your Google Business Profile, if you have one, and your website with your closest competitors for the searches your customers use, and email you a written report. | People ask ChatGPT, Perplexity, Google AI Overviews and Google which business to choose. These tools answer from what they can read. Our free audit shows what to change on your website and Google Business Profile so Google, and the crawlers AI tools send, can read and find you. | NEW, UNGATED |
| 5 | How it works, step 3 | We email the report to the address you give us. | Henrik reads every report before it is sent. Then we email it to the address you give us. | First sentence GATED (Warren). "Then we email it to the address you give us." NEW, UNGATED |
| 6 | Note under How it works | We never ask for passwords or logins. The audit uses only what you tell us and what anyone can see on Google and on the web. | …and on the web. If you want more work after the report, we may ask you to add us as a user in Google Search Console and Google Analytics. You never share a password. | Added sentences GATED (Zinsser i) |
| 7 | Privacy section (home) | …The privacy note has the details. | …The privacy note has the details. This page uses no cookies or analytics. What you send in the form reaches us through Web3Forms, which keeps it for the period set for our form: between 7 days and 3 years on its free plan. | "This page uses no cookies or analytics. What you send in the form reaches us through Web3Forms, which keeps it for" GATED (Zinsser ii). Tail CHANGED, UNGATED: "30 days" replaced, see retention check |
| 8 | Privacy page, Who processes it | Web3Forms (web3forms.com) receives the form and forwards it to us by email, as our data processor. | …as our data processor. Web3Forms keeps it for the period set for our form: between 7 days and 3 years on its free plan. | NEW, UNGATED (made consistent with #7) |
| 9 | Privacy page, How long | We keep your answers and the report for 12 months after we send it, then delete them. You can ask us to delete them sooner. | You can ask us to delete your information at any time. | NEW, UNGATED. "12 months" removed as instructed. **Flag:** GDPR expects a stated period or the criteria for one; Henrik/Warren should pick our own retention period and add it here |

## New lines (none of these exist on live main)
| # | Where | New | Status |
|---|---|---|---|
| 10 | Example, H2 | An example | NEW, UNGATED |
| 11 | Example, label | ExampleCo is invented. This is the kind of change the report suggests, for one question a customer might ask. | NEW, UNGATED |
| 12 | Example, question | "Who can fix a blocked drain in Uppsala today?" | NEW, UNGATED |
| 13 | Example card "Read" | Before: the site blocked AI tools' crawlers. After: Google and AI crawlers can read every page. · example.com/robots.txt | NEW, UNGATED |
| 14 | Example card "Found" | Before: two pages competed for "drain repair". After: one page answers it. · example.com/emergency | NEW, UNGATED |
| 15 | Example card "Ready to mention" | Before: the area and opening hours were only in a picture. After: the page says in plain text "Same-day drain repair in Uppsala, 7 am to 10 pm." · example.com/emergency | NEW, UNGATED |
| 16 | What the audit covers, intro | Google and AI tools answer from what they can read. The audit looks at the website you already have and checks three things. | NEW, UNGATED |
| 17 | Step "Read." | Can Google, and the crawlers that AI tools send, see every page you already have? | NEW, UNGATED |
| 18 | Step "Found." | When a customer searches, does the right page come up on Google? Two of your pages shouldn't compete for the same search. | NEW, UNGATED |
| 19 | Step "Ready to mention." | Does each page say plainly, in text, who you are, what you do and where? We can't control what an AI tool says. We can make your site easy to read and quote. | NEW, UNGATED. Replaces "Mentioned" (Nämnda), which asked whether the answers name you, against Warren's ruling |
| 20 | "It also covers:" | It also covers: | NEW, UNGATED (lead-in before the existing list; the list itself is unchanged and includes Zinsser's "if we can find one" edit) |

## Removed from the first draft (revision 1, ba7a3fa) under the rulings
- Title "…does the AI answer mention you?…" and H1 "…Does the answer mention you?" (rhetorical questions, implied checking).
- "Our free audit shows whether the answers mention you…", "We also put the questions your customers ask to ChatGPT, Perplexity, Google AI Overviews and Google." and the "Mentioned" step (claims that we check AI answers).
- The four example cards labelled Google / ChatGPT / Perplexity / Google AI Overviews that showed answers (implied checking). Replaced by Read / Found / Ready to mention before/after cards.
- "A person reads every report before we send it." (hero) and "A person reads the report first." Now one mention only: "Henrik reads every report before it is sent." (step 3).
- "This page stores nothing. We only receive what you send in the form."

## Title and H1 options (no question marks)
Used: title 1 and H1 1. Alternatives for Zinsser:
- Title 1: Query Polish: a free audit of how Google and AI tools read your site
- Title 2: Query Polish: free audit. Make your site readable for Google and AI tools
- Title 3: Query Polish: a free audit for search and AI tools
- H1 1: Your customers ask AI. Make sure it can read your site.
- H1 2: AI tools answer from what they can read. A free audit of your site.
- H1 3: Make your site easy for Google and AI tools to read and find.

## Checks added to the tests
"12 months" and "stores nothing" absent; no "keeps it for 30 days"; no claim that we check AI answers (regex: "we … put/ask/check/test/run … ChatGPT/Perplexity/AI Overviews/AI tools", "answers mention/name/include", "whether the answers", "does the answer"); report review mentioned at most once per page and "Henrik reads every report before it is sent." exactly once on home; no "?" in title or any heading; only same-origin scripts; no cookies; Zinsser GSC/GA4 line, storage line and GBP edit present.

## Raw extracted-text diff (tools/extract_copy.py, main 4a10f26 vs copy-ai-v1)
```diff
@@ -2,2 +2,2 @@
-TITLE: Query Polish: a free search audit for your business
-META DESCRIPTION: A free audit of how your business shows up in Google search and Google Maps, compared with your closest competitors. The report comes by email.
+TITLE: Query Polish: a free audit of how Google and AI tools read your site
+META DESCRIPTION: Your customers ask ChatGPT, Perplexity, Google AI Overviews and Google. A free audit of whether they can read and find your website. The report comes by email.
@@ -7,2 +7,2 @@
-# A free audit of how your business shows up in search 
-Tell us your website. We compare your Google Business Profile, if you have one, and your website with your closest competitors for the searches your customers use, and email you a written report. 
+# Your customers ask AI. Make sure it can read your site. 
+People ask ChatGPT, Perplexity, Google AI Overviews and Google which business to choose. These tools answer from what they can read. Our free audit shows what to change on your website and Google Business Profile so Google, and the crawlers AI tools send, can read and find you. 
@@ -11 +11,22 @@
-## What the audit covers  
+## An example 
+ExampleCo is invented. This is the kind of change the report suggests, for one question a customer might ask. 
+"Who can fix a blocked drain in Uppsala today?" 
+
+Read
+Before: the site blocked AI tools' crawlers. After: Google and AI crawlers can read every page.
+example.com/robots.txt 
+
+Found
+Before: two pages competed for "drain repair". After: one page answers it.
+example.com/emergency 
+
+Ready to mention
+Before: the area and opening hours were only in a picture. After: the page says in plain text "Same-day drain repair in Uppsala, 7 am to 10 pm."
+example.com/emergency    
+
+## What the audit covers 
+Google and AI tools answer from what they can read. The audit looks at the website you already have and checks three things.  
+- Read. Can Google, and the crawlers that AI tools send, see every page you already have? 
+- Found. When a customer searches, does the right page come up on Google? Two of your pages shouldn't compete for the same search. 
+- Ready to mention. Does each page say plainly, in text, who you are, what you do and where? We can't control what an AI tool says. We can make your site easy to read and quote.  
+It also covers:  
@@ -21,2 +42,2 @@
-- We email the report to the address you give us.  
-We never ask for passwords or logins. The audit uses only what you tell us and what anyone can see on Google and on the web.   
+- Henrik reads every report before it is sent. Then we email it to the address you give us.  
+We never ask for passwords or logins. The audit uses only what you tell us and what anyone can see on Google and on the web. If you want more work after the report, we may ask you to add us as a user in Google Search Console and Google Analytics. You never share a password.   
@@ -25 +46 @@
-We use what you send only to prepare your audit and email it to you. We don't sell it, share it for marketing, or add you to a mailing list. You can ask us to delete it at any time. The privacy note has the details.   
+We use what you send only to prepare your audit and email it to you. We don't sell it, share it for marketing, or add you to a mailing list. You can ask us to delete it at any time. The privacy note has the details. This page uses no cookies or analytics. What you send in the form reaches us through Web3Forms, which keeps it for the period set for our form: between 7 days and 3 years on its free plan.   
@@ -75,2 +96,2 @@
-Who processes it. Web3Forms (web3forms.com) receives the form and forwards it to us by email, as our data processor. 
-How long. We keep your answers and the report for 12 months after we send it, then delete them. You can ask us to delete them sooner. 
+Who processes it. Web3Forms (web3forms.com) receives the form and forwards it to us by email, as our data processor. Web3Forms keeps it for the period set for our form: between 7 days and 3 years on its free plan. 
+How long. You can ask us to delete your information at any time. 
```
