---
name: site-contradictions
description: Find the places where a website contradicts itself, on any site and any CMS. Reads the site's pages, collects every checkable claim with its verbatim quote and URL (prices, plans and seats, trials, setup times, customer counts, integration counts, statistics, names and titles of people and customers, product capabilities, guarantees, legal and company facts), compares claims about the same thing across pages, and reports each contradiction with both quotes, how much it matters, and either a concrete fix or a question for whoever owns the fact. Written for the team that owns the site. Read-only. Use when asked to "find contradictions on <site>", "where does our site contradict itself", "are our prices and numbers the same everywhere", "check the site for inconsistent claims", "what would a buyer notice doesn't add up", or before a relaunch, a migration or a pricing change.
---

# Site contradictions

Find every place where a website says two different things about the same fact, and
hand the editor a short list to fix. A buyer who sees $499 on the homepage and $49 on
/pricing stops trusting both. So does an AI assistant that quotes the site.

**Core principle: a contradiction is two quotes, never an impression.** Each one needs
two verbatim quotes, each with the URL it came from, that cannot both be true at the same
time. Do not decide which one is right unless the site itself says so (see §4). That is
for the people who own the fact to decide (product, sales, legal, leadership), so it becomes a question. Nothing is written to the site or its CMS.

## 0. Setup

Input: the site's address. A list of URLs works too (one section, one product line).

Create the run directory `.site-contradictions/<site-slug>/` in the project root (slug =
bare domain without TLD, e.g. `acme`). All outputs land there. It is working material
about a company: add `/.site-contradictions/` to the project's `.gitignore` if it is
missing. If the directory exists from an earlier run, ask whether to refresh or stop.

## 1. Read the site

Build the page list, in this order, and stop adding when the list is complete:

1. `/llms.txt` and `/sitemap.xml`. A Nexity site lists every page in both, and serves
   each page as Markdown at its URL plus `.md` (or with `Accept: text/markdown`). Read
   the Markdown twin when there is one: it is the page's content without the chrome.
2. The main navigation and the footer, for pages a sitemap misses.
3. Read every commercial page: home, pricing, every product, feature, service and
   solution page, about, contact, FAQ, legal (terms, privacy: company name, address,
   registration), case studies, and listing pages that show numbers.
4. Read the blog, news and podcast pages too. They repeat numbers from the commercial
   pages and are where old values survive. On a large site (more than ~60 posts), read
   the 30 most recent and every post a commercial page links to. Say so in the report.

Fetching gotcha: on JS-rendered sites the fetch tool may return only the `<title>`. Fall
back to `curl -sL <url>` and strip the HTML. Skip a URL that does not respond promptly.
Log it under "Not fetched" and move on.

Log every page you read in `evidence.md` under `## Sources checked`: URL and how many
claims it yielded, including "no claims".

## 2. Collect the claims

For every page, write each checkable claim as a row in `evidence.md`:

```
| Fact | Source URL | Verbatim quote |
|---|---|---|
```

What counts as a checkable claim. Collect it even when it looks harmless; most
contradictions are in plain facts:

- **Money:** prices, plan names, what each plan includes, seats, discounts, trial terms.
- **Time:** setup time, time to first result, delivery times, SLAs, response times.
- **Counts:** customers, users, integrations, countries, team size, years in business.
- **Results:** statistics and outcomes ("43% higher win rate"), with the customer and the
  period when the page names them.
- **People and customers:** names, job titles, company names in quotes and case studies.
- **Product facts:** what a feature does, which plan has it, which tools it integrates
  with, platforms, security and compliance (SOC 2, GDPR, SSO, data residency).
- **Promises:** guarantees, refund terms, uptime, "no engineering needed".
- **Company and legal facts:** company name, address, registration, founding year.
- **Dates and versions:** "new", "launched in", version numbers, "updated".

Quote exactly, including the number's format ("$1,299/mo", "under 30 minutes"). One row
per claim per page: the same sentence on three pages is three rows. That repetition is
what makes the comparison possible.

## 3. Compare

Group the rows by subject: the same fact about the same thing, in the same unit and
scope ("price of the Starter plan, per month, billed monthly"). Then classify each group:

- **Contradiction:** two or more values that cannot all be true at once. Number them
  C1, C2… in order of severity, then of how many pages carry them.
- **Stale:** one value is current and another clearly older (a dated post, a "v1"
  page, an announcement superseded by the product page). It is a finding, not a
  contradiction, and its fix is usually to update or annotate the old page.
- **Tension:** values that are not strictly incompatible but collide when cited
  together (two customer counts with undefined denominators, a stat whose base is
  missing).
- **Consistent:** the same value on two or more pages. Count these; they show the
  sweep was real and what the site can safely repeat.

Before you call two values a contradiction, rule out the honest explanations: monthly vs
yearly billing, per seat vs per account, different plans or regions, a range and a point
inside it, rounding ("40+" and "40"), a date that makes one of them historic, and an
example or calculator value presented as illustrative. When one of these explains the
difference, it is not a contradiction. If the page does not make the scope clear, it is
tension, and the fix is to say the scope.

Arithmetic counts. A "43% improvement" from 38% to 54% is a 42% relative lift; a total
that does not equal its parts is a contradiction inside one page.

**Severity:**
- **high:** prices, plan contents, trials, guarantees, legal and company facts, security
  and compliance, and any number a buyer would quote back in a sales call.
- **medium:** product capabilities, integration and customer counts, setup and delivery
  times, named results.
- **low:** names, titles and dates that change no decision, internal inconsistencies of
  wording.

## 4. Fix or ask

For each contradiction decide one of two routes, and say which in the report:

- **Fix:** the site itself marks one value as current. The canonical page for that fact
  (/pricing for prices, the product page for capabilities, the legal page for company
  facts) states it, and the other value sits on a less authoritative or older page.
  Write the fix as a change for the editor: page, old text, new text.
- **Question:** nothing on the site says which value is right. Write one question for
  whoever owns the fact (product, sales, legal, leadership) that names both values and where they appear.

Never invent the right value. Never mark a page "wrong" because it is less polished.

## 5. Write the outputs

1. `contradictions.md`: the contradictions first (C1… each with a title ending in one
   full stop, severity, the values as quotes with their pages and evidence ids, and the
   fix or the question), then a table of the other findings
   `| claim | on record / note | status | evidence refs |` with status `stale`,
   `tension` or `consistent`, then the open questions grouped by subject and owner.
2. `contradictions.html` from `report-template.html` (same directory as this skill; do
   not restyle it, fill it):
   1. Copy the template to the run directory and replace every `{{...}}` token:
      `{{SITE_NAME}}`, `{{SITE_DOMAIN}}`, `{{RUN_DATE}}`, `{{PAGE_COUNT}}` (pages read),
      `{{FACT_COUNT}}` (evidence rows), `{{CONTRADICTION_COUNT}}`, `{{FINDING_COUNT}}`
      (rows in the other-findings table) and `{{QUESTION_COUNT}}`.
   2. Fill each `<!-- SLOT: ... -->` region using only the markup patterns its comment
      shows. `SLOT:BRIEF` holds the 3 to 5 contradictions an editor should fix first,
      one plain sentence each naming both values and where they appear, linked as
      `#c1`, `#c2`….
   3. Write cross-references as plain text, "question 5" and "C2": the page's script
      numbers the rows, links those references both ways, marks evidence by status,
      adds a way back from an evidence row and the Copy buttons. Do not add any of that
      by hand.
   4. Self-check: no `{{` or `SLOT:` left; every `href="#e..."` resolves to a row id;
      every brief item points to an existing contradiction; no doubled punctuation
      (`..`, `""`); the counts in the masthead match the rows.

If your agent can publish an artifact, publish `contradictions.html` (private until the
user shares it; say so). Otherwise give the file path and suggest opening it in a browser.

## 6. Deliver

In chat, five lines at most: how many pages were read, how many contradictions (by
severity), the top three in one line each, how many are fixes and how many are open
questions, and the path or link to the report. Do not paste the report into chat.

## Common mistakes

| Mistake | Instead |
|---|---|
| Flagging monthly vs yearly, per seat vs per account, or a range and a value inside it | Check the scope first; unclear scope is tension, not a contradiction |
| Picking the "right" value yourself | Fix only when the canonical page states it; otherwise ask whoever owns the fact |
| Paraphrasing a quote to make the conflict clearer | Quote exactly; the editor searches the page for that text |
| Reading only the commercial pages | Old values survive in the blog and in case studies; read them |
| Reporting tone, style or wording | Out of scope: only facts that can be checked |
