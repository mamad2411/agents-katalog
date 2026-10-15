---
name: playbook-case-study-page
description: Finds a prospect company's own case-study or customer-stories page and pulls one named customer off it, so email 1 can open with "saw your work with Intercom". Triggers on "case study", "customer stories", "who are their clients", "saw your work with X", "name-drop one of their customers", "logos on their site". Outputs case_study_line, a short clause that finishes the sentence "Saw ...".
---

# Playbook: Case-Study Page Name-Drop

> All rules here are best practice, not law. Override any of them when the campaign calls for it; note the best practice once and move on.

**Use when:** the campaign wants a first line that proves you looked at the prospect's site, and the
prospect publishes customer stories — B2B software, agencies, consultancies, MSPs, staffing,
manufacturers with named clients.

**Do not use when:** you want a tech detail (`playbook-tech-on-website`), their pricing model
(`playbook-pricing-page`), or an ad they are running (`playbook-ad-library`).

**One-line output:** `case_study_line = "your work with Intercom on outbound pipeline"`, rendering as
`Saw your work with Intercom on outbound pipeline.`

## 1. Trigger and scope

Does this company publicly brag about a named customer, and if so which one, in words you can put in
an email today?

**The path list is ten, not four.** `/customers`, `/case-studies`, `/customer-stories`,
`/success-stories`, `/case-study`, `/clients`, `/our-work`, `/portfolio`, `/testimonials`, `/stories`.

This matters: in the live test one hit came from **`/testimonials`, the ninth path.** Any
implementation that probes only the first four loses that row to a paid fallback.

It does not judge whether the customer is impressive, does not read individual case-study PDFs, and
does not look for customers not published on the prospect's own site. If the client list is private,
the correct output is an abstain.

**Two things make this signal safe:**

1. **The model never writes the sentence.** It only picks the customer and quotes the page. A script
   assembles the clause.
2. **Every claim must appear verbatim in the page text you fetched**, so a hallucinated logo cannot
   reach an inbox.

## 2. Output contract

### Inputs required per row

| Field | Type | Required? |
|---|---|---|
| `domain` (bare, lowercase, no `www`, no scheme, no path) | string | yes |
| `company_name` | string | no, used for logging and page-owner context |

### Output fields

| Field | Type | Example | Null? |
|---|---|---|---|
| `case_study_line` | string, ≤16 words | `your work with Notion on global spend management` | no, use `""` |
| `client_name` | string | `Notion` | no, use `""` |
| `case_study_url` | string | `https://ramp.com/customers` | no, use `""` |
| `evidence_quote` | string | `Notion unified global spend management across 10+ countries` | no, use `""` |
| `confidence` | `high` / `low` | `high` | no |
| `ship_ready` | boolean | `true` | no, defaults `false` |
| `verified` | boolean | `true` | no, defaults `false` |
| `reject_reason` | string | `non-customer-context` | `""` when accepted |

**Only `ship_ready = true` rows get pushed.** `verified = true` with `ship_ready = false` means the
line is real but held for review.

### Coverage expectation

6/7 rows usable (86%). Broken down: 5 produced a real line (4 ship-ready, 1 held at low confidence),
1 correctly abstained, 1 **wrongly** abstained on a carousel-layout page.

⚠️ **Plan on the ship-ready number, not the usable number: 4/7 (57%) shipped without an operator
touching them.**

Expect lower coverage on SMB and trade segments, where most companies publish testimonials with no
company named. **Treat 50 to 60% as the planning number for a mixed B2B list, and 80%+ only for
software and agency segments.**

### Copy-fit rules

- Slots into `Saw {{case_study_line}}.`
- The value always begins with the lowercase words `your work with `, then the customer's name in
  **the customer's own capitalization**, then optionally ` on ` plus a 2 to 5 word topic.
- No trailing period, no leading capital, no em dashes.
- **The prospect's own company name never appears inside the value.** The reader knows who they are.
- **The value is assembled by a script, not written by the model**, so these rules hold by
  construction rather than by asking a model nicely.

### Downstream gate

If empty: drop the clause with spintax and keep the row. **Never render `Saw .`** — put the clause in
its own optional sentence so the paragraph still reads when blank.

### ⚠️ `confidence = low` does NOT auto-ship

Low-confidence rows are **held**, and strict-quote mode is the default. **The coverage cost is
accepted on purpose.**

A `low` row is **a bare logo with no story attached** — which is exactly the shape an investor logo,
a press logo, a partner logo, and a CMS placeholder logo all take. The verbatim gates in §6 **cannot
tell those apart from a customer logo.**

So every `low` row ships `ship_ready = false` and waits for an operator eyeball. To ship them, read a
20-row sample, confirm they are customers, then enable it deliberately. **A `low` row never carries a
topic clause even when it does ship.**

## 3. Source chain (cost-tagged)

| # | Source | Cost | Call | Result |
|---|---|---|---|---|
| 1 | **Direct path guess on the prospect's own origin** | FREE | `HEAD` over all **ten** paths, browser UA, follow redirects, `GET` with `Range: bytes=0-4095` when HEAD is refused | **6/7 found the page here** |
| 2 | Homepage anchor scan | FREE | parse `<a href>` and anchor text for `case stud`, `customer stor`, `success stor`, `our work`, `clients`, probe the first same-origin match | ⚠️ **untested, 0 hits.** It ran on exactly one domain and returned nothing. It is design intent, not a measured result |
| 3 | Page fetch and text flatten | FREE | strip script and style, **keep `<img alt>` as `[logo: X]`**, collapse whitespace, cap at 18,000 chars | mechanical |
| 4 | Model customer picker | CHEAP ($0.18/1k) | §6 prompt, minimal reasoning effort, JSON mode | 5/6 fetched pages yielded a verified customer |
| 5 | SERP `site:{domain} case study` | CHEAP | one simple query, never OR chains | untested |
| 6 | Rendering proxy | METERED | only when step 3 returned under 200 characters | untested. **Cap it to rows that actually failed, never list-wide** |
| 7 | An entity-search API | METERED | last resort | untested |

**Steps 1 to 4 are the tested path and the only ones with a verdict.**

### Before you escalate, check the list size

Case-study finding is a **research** task, and for research a strong reasoning subagent generally
beats a vendor browsing agent or a database when volume is modest and quality matters. In practice:

- **Steps 1 to 4 stay first regardless of size.** Ten free HEAD requests found the page on 6 of 7
  rows. **Nothing outranks free and measured, and a subagent is a worse tool than a HEAD request for
  a question a HEAD request answers.**
- **The leftover rows are where it bites.** On a modest tail — the handful that fell through on a
  list of a few hundred — hand those rows to subagents, one per company. A subagent follows the trail
  when the obvious path 404s, reads the actual page, and abstains honestly; a one-shot vendor agent
  pads.
- **Steps 5 to 7 are the SCALE answer**, for when the tail is thousands of rows running unattended.
- **Verification does not relax.** A subagent's customer name faces the same verbatim gates. If the
  name is not in the fetched page text, it does not ship. **"The agent said so" is not evidence.**

### Rejected alternatives

- **A metered web agent as the finder.** It costs credits per row to do what ten free HEAD requests
  already do at 6/7. Keep it for the leftover rows only.
- **LinkedIn scrapers.** Customer stories live on the company website, not on LinkedIn.
- **Third-party review sites.** Their customer lists are **not the prospect's own claim**, so the
  opener stops being "I read your site" and becomes "I read a directory" — exactly the tell you are
  avoiding.
- **Asking the model to write the finished sentence.** Measured: it lowercased proper nouns, **copied
  a percentage out of the few-shot example onto a different company**, and produced ungrammatical
  clauses.

## 4. Verification

**VERDICT: PASS 6/7 (86% usable, 4/7 ship-ready) | claims 5/5 (100% correct)** | ten-path HEAD sweep
→ model picker at minimal reasoning → deterministic line assembly | p50 2.4s/row | ~$0.18/1k.

**Claim-bearing playbook: 70% usable AND 90% claim correctness.** The single failure was a **wrong
abstain** on a carousel layout — a coverage miss, which costs volume and nothing else. **Naming an
investor or a press logo as a customer is the failure the 90% exists to stop**, and it is why strict
quoting and the low-confidence hold are both defaults rather than options.

Page discovery alone scored **7/7** (6 found, 1 correct negative).

### What this verdict does NOT cover

- **The Clay recipe.** Never run end to end.
- **The homepage anchor scan.** 0 of 6 discoveries.
- **Chain steps 5 to 7.** Never executed.
- **The non-customer logo class.** No row in the sample had an investor wall, a press strip, an
  integrations grid, or a CMS placeholder as its most prominent entity. The placeholder and context
  gates were **unit-tested against a real page dump and a synthetic investor wall** — a code check,
  not a live campaign result.
- ⚠️ **"Verification" that re-runs the same check is not verification.** A second pass that re-fetches
  the same URL with the same UA and runs the same substring check is a **reproduction, not a second
  source.** It can only confirm the string is on the page — which the code gate already guarantees —
  so it **structurally cannot detect the partner, press, or placeholder-logo error class.**

**Read the 6/7 as "6/7 rows produced a line whose name is verifiably printed on the prospect's own
page", not as "6/7 rows named a confirmed customer."**

## 5. Clay implementation

- **`clay-table.md`** — the column build, including the domain-normalization trap that produces a
  100% miss rate with no obvious cause.
- **`clay-workflow.md`** — the CLI-buildable version.

## 6. Locked prompt

Model: `gpt-4o-mini` **inside** Clay, a nano-class reasoning model **outside**. Reason, measured:
nano spends its completion budget on hidden reasoning unless minimal effort is passed, and **Clay's
integration does not expose that parameter.** Without it, this exact prompt returned
`finish_reason=length` with **empty content on 6 of 6 rows.** So nano wins outside Clay on price
(~$0.18/1k vs ~$0.50/1k) and mini wins inside Clay on the only thing that matters there: **returning
content at all.**

Params outside Clay: `max_completion_tokens=1200`, `reasoning_effort="minimal"`, JSON response
format, no `temperature`, flex tier for overnight batches.

```text
You read a company's own case-study, customer-stories, or testimonials web page and pull out ONE named customer they publicly brag about.

You do NOT write the sentence. A script builds the sentence from your fields. Your only job is to pick the right customer and prove it is on the page.

Return JSON only, with exactly these keys:
{"client_name": "...", "evidence_quote": "...", "detail_phrase": "...", "confidence": "high|low"}

What each key means:
- client_name: the name of ONE customer company named on the page, spelled and capitalized exactly as the page spells it. Never the page owner. Never a partner directory, a press outlet, a review site, or a person's name. Pick the customer with the clearest story on the page.
- evidence_quote: 4 to 20 words copied character for character from the page text. It MUST contain client_name. It is what proves the customer is really named there.
- detail_phrase: 2 to 5 plain words naming the TOPIC of the work, and every word of it must appear inside evidence_quote. It is a noun phrase like "global spend management" or "first response time". It is never the customer's name, never a sentence fragment like "time back" or "hours saved", and never ends in a small word like back, up, out, on, of, to, with. If evidence_quote holds no clean topic, return "" here. An empty detail_phrase is a good answer, not a failure.
- confidence: "high" when the page clearly presents that company as a customer, "low" when it is only a logo with no story.

Rules:
- Never invent a customer, a number, or a result. If the page names no customer company, return "" for client_name and "" for the other fields.
- A page of unnamed praise ("Great service. - Dave R.") names no customer company. Return "".
- The examples below show SHAPE ONLY. Never copy a customer name, a number, a percentage, or a phrase out of the examples into your answer.
- detail_phrase never contains the page owner's own name, never contains a number the page does not state, and never sounds like bad news for the customer.
- 5th-grade reading level. No em dashes anywhere in the output.
- Ignore navigation text, cookie banners, menu items, and blog titles. Those are not customer stories.

Examples:
Input: page owner = zendesk.com, page text = "Customer stories. How Uber cut first response time by 30%. Read the Shopify story. [logo: Slack]"
Output: {"client_name": "Uber", "evidence_quote": "How Uber cut first response time by 30%", "detail_phrase": "first response time", "confidence": "high"}
Input: page owner = someagency.com, page text = "Our work. [logo: Peloton] [logo: Casper] [logo: Warby Parker]"
Output: {"client_name": "Peloton", "evidence_quote": "[logo: Peloton]", "detail_phrase": "", "confidence": "low"}
Input: page owner = acmeplumbing.com, page text = "Testimonials. Great service, fast and friendly. - Dave R. Highly recommend! - Sarah T."
Output: {"client_name": "", "evidence_quote": "", "detail_phrase": "", "confidence": "low"}

PER-ROW DATA (appended last)
Page owner company: <company name>
Page owner domain: <domain>
Page URL: <case study url>
Page text:
<page text>
```

Note the "SHAPE ONLY" rule. It is there because **the model copied a percentage out of a few-shot
example onto an unrelated company** during testing.

### The clause is assembled by code

```
line = "your work with " + client_name
if every content word of detail_phrase appears inside evidence_quote
   and detail_phrase is not the client name
   and detail_phrase does not end in a dangling word (back, up, out, on, of, to, in)
   and detail_phrase contains no finite verb (is, are, helps, helped, ...)
then line = line + " on " + detail_phrase
if line is longer than 16 words, drop the detail
```

### Verifier pass: five code checks, not a second model call

1. `client_name` appears **verbatim** in the fetched page text.
2. `evidence_quote` appears **verbatim in full** in the fetched page text.
3. `evidence_quote` **contains** `client_name`.
4. `client_name` is not a CMS placeholder or generic noun (`Startup`, `University`, `Company`,
   `Partner`, `Client`, ...).
5. `client_name` does not appear **only** inside investor, press, partner, or integration wording —
   check a ~600-character window before each mention, cancelled by customer wording in the same
   window.

Any failure means abstain, **after one retry** (the model occasionally quotes an adjacent block, or
picks a placeholder logo when a real customer sits next to it). Checks 1 to 3 caught a fabricated
detail during the live test.

### ⚠️ Honest limits, read this before trusting a line

**Checks 1 to 3 prove the string is ON the page. They do not prove the entity is a CUSTOMER.**

An investor wall, a press strip, an integrations grid and a placeholder logo all live on the same page
and **all pass a substring check.** This is not hypothetical: a real captured page served
`[logo: Startup]`, `[logo: University]`, `[logo: Anthropic]`, `[logo: Google]`. Before checks 4 and 5
existed, a model returning `client_name = "University"` with `evidence_quote = "[logo: University]"`
passed all three checks and shipped as **`Saw your work with University.`**

Checks 4 and 5 are **reject-only heuristics**, so a false positive costs one abstained row and never
a bad line. **They are not a proof of customerhood, and no live-test row exercised an investor or
press wall.** That residual risk is exactly why low-confidence rows are held.

**Truncation guard:** `finish_reason=length` means retry, never abstain. It is the single most likely
failure on this prompt.

## 7. Edge cases and failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Every domain returns "no page found" from a script that works by hand | A default runtime User-Agent is being 403'd or challenged | **Send a browser User-Agent on every request** |
| A page "exists" at `/customers` on a company that obviously has none | **Soft 404**: the origin 302s unknown paths to `/` and returns 200 | Reject any candidate whose final path is `/`, and reject final paths that no longer match the case-study pattern |
| `/customers` lands on a support login or help center | Consumer sites use "customers" to mean account holders | The path pattern check plus the ignore-navigation instruction. Rows that slip through show up as `low` with no detail |
| Model returns empty content with `finish_reason=length` | Reasoning burned the completion budget | Minimal reasoning effort, cap 1200, treat `length` as a **retry**. Inside Clay, where the parameter is unavailable, use a mini-class model |
| The line names a customer not on the page at all | Hallucination | The verbatim gates catch this |
| **The line names an entity that IS on the page but is not a customer** — an investor (`Saw your work with Sequoia.`), a press logo, an integration partner, or a CMS placeholder (`Saw your work with University.`) | Investor walls, press strips, partner grids and unfilled CMS slots sit on the same page as the customer logos. **The verbatim gates cannot catch this** | **Partially mitigated, not solved.** Checks 4 and 5 are heuristics and neither was exercised live. `low` rows are the exposed class and are held. **Before enabling low-confidence shipping for a client, read 20 rows of that client's output yourself** |
| The line carries a result belonging to a different customer | Numbers next to the wrong logo, or the model copying a number out of the few-shot example | The detail is dropped unless **every** content word appears inside the evidence quote **for that same customer** |
| The line reads `your work with Air Tutors on Air Tutors` | The model returned the customer name as the topic | A code check rejects a detail equal to the client name |
| The line reads `your work with Google on time back` | The detail is a sentence fragment | Reject details ending in a dangling word or containing a finite verb |
| A real case-study page yields nothing (wrong abstain) | **Carousel or logo-wall layouts put names and quotes in separate DOM blocks**, so no short quote contains both | A known limitation, and **strict quoting stays the default.** This is a coverage miss, which costs volume only. Lenient quoting widens exactly the non-customer class above, so it stays off until that class has been live-tested |
| Page text comes back under 200 characters | JS-rendered marketing page | Escalate **that row only** to a rendering proxy. Never list-wide |
| Two runs on the same company return different customers | **Expected.** Any named customer is a valid answer | Not instability. If you need determinism, cache the first accepted value per domain |

### Hard rules

- **Every HTTP request sends a browser User-Agent**, or CDN-fronted prospect sites read as *missing*
  rather than as *blocked*.
- **Politeness is per origin, not global.** These are your targets' web servers, not a vendor API you
  pay for. Keep per-origin concurrency at 2, never above about 4; a global cap is a blast-radius
  control on your own egress and can be higher.
- **Throughput is fetch-bound**, roughly `rows × page-seconds / global-concurrency`. **Raising model
  concurrency alone does nothing.**
