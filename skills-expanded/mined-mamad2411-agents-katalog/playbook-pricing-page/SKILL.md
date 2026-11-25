---
name: playbook-pricing-page
description: Decides whether a company publishes public self-serve pricing and extracts its plan tiers, price points and feature axis. Triggers on "do they have a pricing page", "is their pricing public", "filter out enterprise quote-only companies", "what do they charge", "find their plans", "self-serve vs sales-led". Outputs a structured pricing record per domain. The copy-ready pricing clause is OFF by default and runs only when a campaign brief asks for it.
---

# Playbook: Pricing Page

> All rules here are best practice, not law. Override any of them when the campaign calls for it; note the best practice once and move on.

**Use when:** the campaign needs to separate self-serve companies from sales-led ones, or needs a
real price point to anchor an offer against.

**Do not use when:** you want technology installed on the site (`playbook-tech-on-website`).

**One-line output:** `pricing_public = true` with
`plans = [{"name":"Basic","price":"$10","period":"month"}, ...]` and `lowest_paid_price = "$10"`.

## 1. Trigger and scope

Does this business publish real prices on its own website, and if so what are the tiers?

**It is used for filtering first and copy second.** The most common job is splitting a list into
product-led companies (public price list, card checkout, low ACV) and sales-led companies (every
tier says Contact Sales) — because those two groups need completely different offers and completely
different copy.

### Bones only by default. No pricing line unless the campaign asks.

The deliverable is the structured record: `pricing_public`, `pricing_model`, `plans`,
`lowest_paid_price`, `has_free_tier`, `enterprise_quote_only`, `feature_diff_axis`.

The one-clause string `pricing_line` is an **opt-in extra, it is the weakest part of the output**,
and it should be stripped at the output boundary unless explicitly requested. **A price in a
stranger's inbox is a claim you have to be right about, and most campaigns using this playbook only
ever wanted the filter.**

It does **not** cover: what a prospect actually pays after negotiation, private rate cards,
marketplace listings, or ecommerce SKU prices.

**If every tier says Contact Sales, the correct answer is `pricing_public: false` — a real and
useful signal, not a failure.**

## 2. Output contract

### Inputs required per row

| Field | Type | Required? |
|---|---|---|
| `domain` (bare, lowercase, no scheme, no `www`) | string | yes |
| `company_name` | string | no, improves the copy line only |

### Output fields

| Field | Type | Example | Null? |
|---|---|---|---|
| `pricing_public` | boolean | `true` | no, defaults false |
| `pricing_url` | string | `https://www.notion.com/pricing` | yes, `""` |
| `pricing_model` | `per_seat` / `usage` / `flat` / `credits` / `quote_only` / `unknown` | `per_seat` | no |
| `plans` | array of `{name, price, period}`, max 6 | see above | yes, `[]` |
| `lowest_paid_price` | string | `$10` | yes, `""` |
| `has_free_tier` | boolean | `true` | no |
| `enterprise_quote_only` | boolean | `true` | no |
| `feature_diff_axis` | ≤6 words | `seats and automation limits` | yes, `""` |
| `confidence` | `high` / `low` | `high` | no |
| `pricing_line` | **OPT-IN, off by default** | `your Basic plan is $10 per user per month` | absent on a default run |

### ⚠️ `quote_only` and `unknown` are not the same thing

- **`quote_only`** — the page exists and every tier says contact sales. **A confident finding you
  can filter on.**
- **`unknown`** — you could not read the page at all. **A failed fetch, not a finding. The row must
  not be filtered out on your say-so.**

Collapsing these two is how a campaign silently deletes real prospects because of a network error.

### Coverage expectation

**8/10 rows produced a usable filtering record.** The existence check alone was **10/10**. That is
the number to plan on, because the filtering record is the whole default deliverable.

The optional copy string was usable on 9/10 in the clean regrade but **6/10 once corrected on an
earlier run** — so treat it as a **70-to-90% field**: spintax-optional, never mandatory. That spread
is part of why it is off by default.

### Downstream gate

**Whether a pricing value removes a row is decided per campaign brief.** This playbook produces the
bones; the brief says what to do with them. Ask once, up front:

- **Filter** (`pricing_public: false` rows leave this campaign) — correct when the offer only makes
  sense for self-serve companies, or only for sales-led ones.
- **Route** (send those rows to a different campaign or offer) — correct when both halves of the
  list are sellable, which is the common case.

⚠️ **Either way, `pricing_model: "unknown"` never removes a row.** Only act on `confidence: "high"`
findings.

**If the brief is silent, route rather than delete**, and say so in the handoff. Deleting rows is a
client-facing, money-adjacent decision, and **it is cheap to reverse a routing choice and expensive
to reverse a deletion.**

## 3. Source chain (cost-tagged)

| # | Source | Cost | Call | Result |
|---|---|---|---|---|
| 1 | **URL-guess existence check** | FREE | `HEAD https://{domain}/pricing`, then `/pricing/`, `/plans`, `/pricing-plans`, `/price`, then the same on `www.`. Browser UA, follow redirects, and **accept only when the final status is 2xx AND the final resolved path still matches `/pricing\|plans\|price/`** | **10/10 correct.** 15/16 pages found on the first candidate — **but the candidate walk is not optional:** one company only resolves via `/pricing → /plans/`, and two needed all 7 |
| 2 | Plain GET of the found URL | FREE | same browser UA, strip script/style/svg/comments to visible text, then take the **price-dense window** (not the first N chars), capped at 14,000 characters | 15/16 pages readable |
| 3 | Rendering proxy | METERED | JS render with a wait | **0/1 rescued.** Only when step 2 produced under 800 characters of visible text OR fewer than 2 currency amounts. **Never otherwise** |
| 4 | SERP site search | CHEAP | `site:{domain} pricing`, take the first result on the company's own domain, loop back to step 2 | **mixed.** It located the real pricing URLs for two hard domains but returned docs/community/careers pages for two others. **A discovery aid, not a guarantee.** One simple query, no OR chains |
| 5 | Model extractor | CHEAP | `reasoning_effort: "low"`, `max_completion_tokens: 6000`, JSON response format | 6/8 readable pages fully correct |

If HEAD is refused, fall back to `GET` with `Range: bytes=0-4095` — and **accept any 2xx**, because
a compliant origin answers **206 Partial Content**, not 200. A script that accepts only 200 silently
records those domains as having no pricing page.

### When "pricing analysis" is bigger than this chain

This playbook answers a narrow, mechanical question at 8/10 for a fraction of a cent, **so do not
route the per-row extraction to an agent of any kind.**

But operators say "pricing analysis" for a second, genuinely different job: *work out how this
company actually charges and what that implies for our pitch* — packaging logic, where the value
metric sits, how it compares to a competitor, whether "contact sales" hides a floor. **That is a
research question**, and for it a strong reasoning subagent per account generally beats a vendor
browsing agent or a database lookup, when volume is modest and quality matters.

So: **this chain for the structured record on every row; a subagent per account for the analysis on
a modest set; a vendor agent only when you are buying scale.** Either way the output contract and
the claim gates still bind — a subagent's reading of a pricing page is a claim like any other and
needs the URL and the quoted text.

### Rejected alternatives

- **A metered AI browse per row.** It works, but it is credits per row for a job that a free HEAD
  plus a free GET plus a fraction of a cent of model does at 90%.
- **Entity-search APIs.** You already know the entity and the URL. Nothing to search for.
- **A scraping marketplace actor.** Expensive, and none beats a plain GET on a public marketing page.
- **Search caches and third-party pricing aggregators.** **Stale by construction, and a stale price
  in an email is worse than no price.**

## 4. Verification

**VERDICT: PASS 8/10 (80% usable) | claims 8/8 (100% correct)** | multi-candidate HEAD → plain GET +
price-dense window → model JSON extractor | ~$0.50/1k domains.

**This is a claim-bearing playbook: 70% usable AND 90% claim correctness.** `unknown` is a failed
fetch, not a finding, and a correct "this company does not publish pricing" is a **correct outcome
that leaves the denominator entirely.**

**Scope note:** when the record is used only to route or filter, it is internal work and the plain
70% bar applies. **The moment a campaign turns the copy line on, or quotes a price, the 90% bar
binds.**

### ⚠️ The earlier 9/10 is withdrawn, and you should know why

The first run was **contaminated**: three of the four few-shot examples in the prompt were
**verbatim the scraped text and the exact expected output of three of the ten graded rows** — and
the prompt had been rewritten *after* seeing first-pass failures on those same rows.

**30% of the test had its answers in the prompt.**

The 8/10 above is a clean regrade: invented example companies, and 10 domains that appear nowhere in
the prompt. **The clean number is lower, which is what you should expect whenever a contaminated
number gets re-measured.**

**Rule for anyone editing a prompt in this library: a few-shot example may never be text from a
domain that appears in the test set, and if you tune the prompt against failures on specific rows,
you must regrade on different rows.**

## 5. Clay implementation

- **`clay-table.md`** — the column build.
- **`clay-workflow.md`** — the CLI-buildable version.

### The pricing cache

This is one of very few playbooks that earns a cache, because **whether a company publishes
self-serve pricing is a property of the domain rather than of the campaign**, so one client's answer
is reusable by the next. A row costs a multi-candidate HEAD sweep, a full page GET against the
prospect's own server, and a long model grade (~3,850 prompt tokens).

Three conditions on any reused record, none optional:

1. **Store `last_checked` and the resolved `pricing_url` with the record.** A cached record with no
   date is not reusable, it is a rumour.
2. **Re-fetch before a price goes into copy.** The filter fields age reasonably; **a dollar figure
   does not.**
3. **This covers records you extracted from live pages.** It is not permission to read pricing from
   a search cache or an aggregator.

Two things that sink cache designs:

- **Ship the write-back in the same pass.** A cache with no writer can never hit.
- **Pick a window short enough to stay honest.** A stale "no public pricing" verdict on a company
  that has since launched self-serve is a confident wrong answer in a live email — worse than the
  fetch it saved. Do not reuse a long email-cache window without arguing for it.

## 6. Locked prompt

**The prompt still produces `pricing_line`, and that is deliberate.** The default run drops the field
**at the output boundary**, rather than editing the prompt to stop asking for it. Editing the static
prefix would invalidate the clean regrade this verdict rests on, cool the prompt cache, and force a
full re-test to save a handful of output tokens. **Keep the prompt byte-identical; drop the field in
code.**

Params: `max_completion_tokens=6000`, `reasoning_effort="low"`, JSON response format, no
`temperature`, flex tier for batch.

```text
You are a B2B pricing-page analyst. You will be given the visible text of one company's pricing page, scraped from their website.

Your job is to decide whether this company publishes real, self-serve pricing, and to extract the plan structure. This is used to FILTER a prospect list, so a wrong "yes" is worse than an honest "no".

Return JSON only, with exactly these keys:
{"pricing_public": true|false, "pricing_model": "per_seat"|"usage"|"flat"|"credits"|"quote_only"|"unknown", "plans": [{"name": "...", "price": "...", "period": "month"|"year"|"one_time"|"unknown"}], "lowest_paid_price": "...", "has_free_tier": true|false, "enterprise_quote_only": true|false, "feature_diff_axis": "...", "pricing_line": "...", "confidence": "high"|"low"}

Rules:
- pricing_public is true ONLY if at least one plan shows a real currency amount on the page. A page that says "Contact sales" or "Request a quote" for every plan is pricing_public false with pricing_model "quote_only".
- Never invent a number. If a price is not in the input text, leave it out. Do not estimate.
- plans lists at most 6 plans, in the order shown on the page. Free tiers count as a plan with price "$0".
- Attach each price to the plan name it sits directly under on the page. Never shift a price up or down to the neighbouring plan. If you cannot tell which plan a number belongs to, leave that plan's price as "" instead of guessing.
- When a plan lists several seat types (full seat, dev seat, collaborator seat), use the FULL seat price for that plan and ignore the cheaper seat types.
- Take a price only from the plan card it belongs to. Ignore numbers that appear in body copy, footnotes or FAQs, such as a minimum invoice spend, an annual contract minimum, or a savings claim. If a plan says "Contact us" or "Talk to sales", its price is "" even when a large number appears in a sentence nearby.
- When a page shows a struck-through list price next to a limited-time promotional price ("50% off for 3 months"), use the LIST price, not the promotional one. A promo expires and would date the email.
- If the ONLY price shown for a plan is an introductory or limited-time rate ("$13/mo for 12 months", "first year", "then, starts at"), report that price, set confidence to "low", and leave pricing_line empty. An intro rate quoted as if it were the list price is a wrong claim in the prospect's inbox.
- lowest_paid_price is the cheapest list price a customer can actually pay, excluding free tiers and excluding promotions. Empty string if none is shown.
- feature_diff_axis is the single thing that changes between tiers, in 6 words or fewer, for example "seats and automation limits" or "monthly lead credits".
- pricing_line must read grammatically inside this sentence: "Noticed <pricing_line>." Write ONLY the part that replaces <pricing_line>. Do not write the word "Noticed" yourself, do not repeat the sentence frame, start with a lowercase letter, and do not end with a period. Keep it at a 5th-grade reading level.
- pricing_line names something only this company would recognise, such as the plan name plus its price. "pricing starts at $0 for the free plan" is too generic to use, so prefer the cheapest PAID plan.
- Only state a billing period in pricing_line if the page states one. If the page prices per unit with no period, say the unit, not "per month".
- No em dashes anywhere in your output. Use a comma or split the sentence.
- If the input text is a cookie banner, a login wall, a navigation shell, or is otherwise too thin to judge, return pricing_public false, pricing_model "unknown", confidence "low", and "" for pricing_line. Do not guess from the company name.

Examples (these four pages are invented, from companies that do not exist, so that no
example can ever hand you the answer to a page you are actually being asked to read):
Input: Northwind Ledger Pricing Starter $0 Free for small teams 3 workspaces Standard $7 per user/month Team $23 per user/month Enterprise Talk to us
Output: {"pricing_public": true, "pricing_model": "per_seat", "plans": [{"name": "Starter", "price": "$0", "period": "month"}, {"name": "Standard", "price": "$7", "period": "month"}, {"name": "Team", "price": "$23", "period": "month"}, {"name": "Enterprise", "price": "", "period": "unknown"}], "lowest_paid_price": "$7", "has_free_tier": true, "enterprise_quote_only": true, "feature_diff_axis": "seats and workspace limits", "pricing_line": "your Standard plan runs $7 a user each month", "confidence": "high"}

Input: Halden Systems Pricing Every deployment is scoped with our team. Book a walkthrough Request a quote Talk to sales
Output: {"pricing_public": false, "pricing_model": "quote_only", "plans": [], "lowest_paid_price": "", "has_free_tier": false, "enterprise_quote_only": true, "feature_diff_axis": "", "pricing_line": "", "confidence": "high"}

Input: Crate Studio Plans Sketch Includes: unlimited boards Studio Monthly Annual Full seat $29 /mo Builder seat $14 /mo Viewer seat $4 /mo Atelier Billed annually Full seat $68 /mo Builder seat $31 /mo Enterprise Full seat $115 /mo
Output: {"pricing_public": true, "pricing_model": "per_seat", "plans": [{"name": "Sketch", "price": "$0", "period": "month"}, {"name": "Studio", "price": "$29", "period": "month"}, {"name": "Atelier", "price": "$68", "period": "month"}, {"name": "Enterprise", "price": "$115", "period": "month"}], "lowest_paid_price": "$29", "has_free_tier": true, "enterprise_quote_only": false, "feature_diff_axis": "seat type and board limits", "pricing_line": "your Studio plan is $29 a seat each month", "confidence": "high"}

Input: Ferrous Growth Run every campaign in one place 30% off for the first year* $62 $43.40 USD per workspace / month, when paying monthly $54 USD per workspace / month, when paying annually
Output: {"pricing_public": true, "pricing_model": "flat", "plans": [{"name": "Growth", "price": "$62", "period": "month"}], "lowest_paid_price": "$62", "has_free_tier": false, "enterprise_quote_only": false, "feature_diff_axis": "billing period", "pricing_line": "your Growth plan lists at $62 a workspace each month", "confidence": "high"}

PER-ROW DATA (appended last)
PAGE DATA
Domain: <domain>
Pricing URL: <pricing url>
Visible page text:
<text>
```

### Verifier pass: not needed for the price, and here is the better check

The model's input is the company's **own live page, fetched seconds earlier**, so there is no stale
training data to hallucinate from. The check that actually catches fabrication is a **string
search**:

> Assert that every price and every plan name the model reports appears **verbatim** in the input
> text.

That assertion is free, runs locally, and is what graded all 10 rows. **Implement it as a formula or
a code assertion, not a second model call.** A second model call *is* warranted if you ever feed this
playbook cached or aggregated pricing instead of a live fetch.

**Truncation guard:** `finish_reason=length` means retry, never abstain. Measured on this exact
prompt at a 3,000-token cap: **empty content on 3 of 8 rows.**

⚠️ **This prompt is not locked, and it is further from locked than it looks.** The clean regrade
exposed two new failure modes (a minimum-invoice figure captured as a plan price; an unstruck
12-month intro rate reported as list price). Each got a new rule above, and **neither rule has been
tested since it was added.**

## 7. Edge cases and failure modes

| Symptom | Cause | Fix |
|---|---|---|
| A quote-only company is reported as having public pricing | **`{domain}/pricing` returns HTTP 200 and redirects to a 404 page.** Measured on a real enterprise domain resolving 200 to `/404` | **Require the final resolved path to still match `/pricing\|plans\|price/`. Status 200 alone proves nothing.** A guard that fails in the wrong direction records every quote-only company as having public pricing — a false claim on every one |
| A page with real prices is reported `quote_only` with high confidence | The text was truncated from the front and the price table was past the cutoff. Measured: one page extracts to **354,059 chars and the first 14,000 contain zero prices** | Use a **price-dense sliding window**, never `text.slice(0, N)` |
| Rows come back empty with no error | `finish_reason: "length"`, budget spent on reasoning. **3 of 8 rows** at a 3,000-token cap | `reasoning_effort: "low"`, cap 6000, retry on `length`. Never record it as an abstain |
| You paid for a render and got the same empty JS shell | A JS page may only fill in after paint | Keep a wait as the default but **treat it as unproven.** An A/B on one real page: no wait = 43 currency tokens in 3.4s; `wait=8000` = **43 currency tokens** in 23.5s, and the extra characters were the cookie banner. If you are burning credits with nothing to show, A/B it on your own pages |
| A "Contact us" plan comes back with a big price attached | A number in body copy or a footnote sits near the plan table. Measured: a page publishing "available on the Standard or Teams plan for $5,000 and Enterprise plan for $15,000" had **$15,000 attached to an Enterprise tier the same page marks "Contact us"** | The prompt now forbids it. **That rule is untested** — spot-check any plan whose price is an order of magnitude above the rest |
| The email quotes an intro rate as the list price | A promo with **no struck-through comparison**, so a struck-through rule never fires. Measured: a page showing "$13.00/mo for 12 months ... Then, starts at" where the list price **never reaches the text layer at all** | Report the intro price, set `confidence: "low"`, leave the copy line empty. **Untested.** Treat `low` rows as filter-only |
| `plans[].price` contains period text (`"$20 per user / month"`) | The model folded the period into the price field. 2 of 4 plans on one domain | Cosmetic — `lowest_paid_price` stayed clean, so the filter is unaffected. Normalize with a regex before pushing to copy |
| `lowest_paid_price` names a number in no plan in the same record | Annual and monthly rates both appear; the model picked annual for one field and monthly for the other. **Both true, both on the page** | Not a fabrication, but **do not use both numbers in the same sentence** |
| A pricing page exists but the origin refuses HEAD | The GET fallback's `Range` request gets **206**, not 200 | Accept any 2xx |
| A CDN-fronted site looks like it has no pricing page | A default runtime User-Agent got 403'd | **Send a browser User-Agent on every request. Never validate this path with `curl` — `curl` is not the production path** |
| The copy line renders `Noticed noticed your Pro plan...` | The prompt stated the sentence frame and the model echoed the frame word | The prompt explicitly forbids writing "Noticed". Re-check after any edit |
| Plan names and prices off by one tier | Multi-seat-type cards confuse the alignment | The prompt pins price to the plan name it sits under. **Verify with the free string-search assertion** |
| `plans` lists product SKUs instead of tiers | Very large multi-product pricing pages have no single tier table | **Accept it.** `pricing_public` and `pricing_model` are still correct, which is what the filter uses. Do not put those `plans` into copy |
| Some page never yields prices no matter what | The plan data arrives in a later XHR, not in the HTML | Accept the miss, or capture the vendor's own pricing XHR once with a real browser and hit that endpoint directly |
| Transient connection resets | Normal network noise | Retry with backoff. **A network failure is never a verdict, in either direction.** A fetcher with no retries is worse than it looks: an empty body fails the richness gate and **spends a metered render credit on what was only a blip** |
| The prompt cache stops paying and the estimate drifts | **Any edit to the static prefix cools the cache**, and small parallel batches never warm it. Measured: 6 of 8 calls cached on one run, **0 of 8 after the prefix was edited** | Budget the **uncached** number. Re-read the cached-token count after every prompt edit instead of carrying the old figure forward |

### Hard rules

- **Bones by default, no pricing line.** Do not produce, push, or build a column for the copy clause
  unless the brief asks.
- **Every price and plan name must appear verbatim in the fetched page text. Assert it in code.** A
  price a prospect cannot find on their own site destroys the message — and writing "Base" where the
  page says "Basic" is the same failure. **Never grade a batch by eye; grep every reported name and
  price back out of the captured text.**
- **A true negative is only confirmed by a second, independently located page with real readable
  text.** A second source that comes back as a 26-character JS shell **confirms nothing in either
  direction.**
- **`unknown` never removes a row.**
- **Fetch politely: concurrency 2 per origin.** These are the websites of companies you want to sell
  to.
