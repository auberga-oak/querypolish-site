# Copy diff: simple test deploy (`simple-test`) vs branching-v1 at ea93552

Zinsser to re-gate the items marked **CHANGED** or **NEW**. Everything else keeps the wording approved at ea93552.

## Changed
| # | Where | Old | New |
|---|---|---|---|
| 1 | Meta description | …compared with up to three competitors you choose. The report comes by email. | …compared with **your closest competitors**. The report comes by email. |
| 2 | Hero lead | Tell us about your business and up to three competitors. We compare your Google Business Profile, if you have one, and your website with theirs for the searches you care about, and email you a written report. | **Tell us your website.** We compare your Google Business Profile, if you have one, and your website with **your closest competitors for the searches your customers use**, and email you a written report. |
| 3 | Covers, bullet 3 | …match the searches **you named**, … | …match the searches **your customers use**, … |
| 4 | How it works, step 1 | Fill in the form below. It takes about ten minutes. Only the fields marked with a star are required. | Fill in the form below. **You only need to give us your website and your email address.** |
| 5 | How it works, step 2 | …your website, and the competitors you name. | …your website, and **your closest competitors**. |
| 6 | Privacy, "What we collect" | What you type into the audit form: how your customers find you, details about your business, your services and market, the searches you want to show up for, up to three competitors, any numbers you choose to share, your email address and the language you want the report in. | What you type into the audit form: **your website address, your email address, the language you want the report in, and anything else you choose to tell us.** |
| 7 | Form: Website address | optional, only in the "Services and market" and "Your online business" sections | **required** (*), in "Your business" |

## New
- Banner on every page: **Test version. This site is being tested and isn't open for requests yet.**
- Form field: **Anything else you'd like us to know** (optional). I added one free-text field so a test, or a customer, can add context.

## Removed (no replacement wording)
- Q1 "How do your customers find you?" and its helper and the A/B/C options.
- The sections "Your Google Maps listing", "Where you work", "Services and market", "Your online business", "Competitors" (and its hint), "Keywords" and "Your current numbers", with all their labels and hints.
- From "Your business": Business name and its hint, Owner's name, Year founded, Team size, Your best customer.
- The JS-off notes ("Fill in this part if you picked …", "(required for this answer)").

## Unchanged (kept as approved)
- Title, H1, "What the audit covers" bullets 1, 2 and 4, and its closing line.
- How it works step 3, the note, and the Privacy section on the home page.
- "Fields marked * are required." (still true: Website, email and consent carry a star).
- Report language (English default / Swedish), the consent text, the button, and the status and error messages.
- The thanks page, the 404 page, the footer and the rest of the privacy page (contact henrik.ekenberg@finansium.se).

## Flags for Zinsser and Warren
- Bullets 1 and 4 still describe checking the profile and the name/address/phone. The form no longer asks for the profile link or the address, so the team has to find them from the website. Is that acceptable for a test?
- "Your closest competitors" / "searches your customers use" commits us to choosing both ourselves, which matches Zinsser's earlier hint ("we'll find likely competitors in public search results").
