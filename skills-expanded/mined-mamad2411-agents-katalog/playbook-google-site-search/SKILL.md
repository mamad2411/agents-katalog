---
name: playbook-google-site-search
description: Checks whether a company's own website mentions a specific keyword, using one simple Google site: query per keyword through a SERP API, and turns the hit into a copy-ready line. Triggers on "does their site mention X", "site: search", "find companies whose website says X", "filter this list by a keyword on their site", "check if they talk about X", "google search enrichment". Outputs site_keyword_hit plus a one-clause personalization line with an evidence URL.
---

# Playbook: Google `site:` Keyword Filter

> All rules here are best practice, not law. Override any of them when the campaign calls for it; note the best practice once and move on.

**Use when:** a campaign needs to know whether each company's own website talks about a specific
thing — a certification, a technology, a service line, a location, a program name — and no structured
API sells that field.

**Do not use when:** you need to *find* companies you do not have yet; when the thing you want is a
**page** rather than a phrase (`playbook-pricing-page`, `playbook-case-study-page`); or when a real
filterable field already exists (funding stage, headcount, technology installed) — filter at the
source and skip this entirely.

**One-line output:** `site_keyword_line = "you hold SOC 2 Type II certification"`, rendering as
`Noticed you hold SOC 2 Type II certification.`

## 1. Trigger and scope

You have a list of domains. Someone asks "which of these mention X on their website?"

**It does two jobs at once, and you should know which one you are buying.** As a **filter** it tells
you which rows to keep — that half is reliable. As a **personalization signal** it gives you an
evidence URL and a line — that half needs the confidence gate in §2, **because a page can contain
your keyword for reasons that have nothing to do with the company.**

**It does not prove a company lacks something.** The index is incomplete and its results are **not
even stable between two identical calls a minute apart** (measured). An empty result means "not
found in the index today", never "this company does not do X".

### The rule that defines this playbook: one keyword, one query

`site:acme.com "chess"`. **Never** `site:acme.com ("chess" OR "checkers" OR "board games")`.

Measured:

| Query | Precision |
|---|---|
| `site:n8n.io "SOC 2"` | **10/10 results contained the phrase** |
| the same domain with a 7-term OR chain | **4/10** |
| `site:uschess.org "Brooklyn"` | 8/10 on target |
| the same with an OR chain | **2/10**, and it drifted to a chess house in New Orleans |

The chain also **destroys attribution**: one response for seven keywords means you cannot tell which
one matched.

## 2. Output contract

### Inputs required per row

| Field | Type | Required? |
|---|---|---|
| `domain` (bare, lowercase, no scheme, no `www`) | string | yes |
| `keyword` | string, the exact phrase | yes |
| `company_name` | string | no, improves readability |

**The keyword is a campaign-level constant, not a per-row value.** One campaign, one keyword. Three
keywords means three columns and three queries per row, each with its own answerable yes or no.

### Output fields

| Field | Type | Example | Null? |
|---|---|---|---|
| `site_keyword_hit` | `"yes"` or `""` | `yes` | yes |
| `site_keyword_line` | string | `you hold SOC 2 Type II certification` | yes |
| `site_keyword_url` | URL | `https://linear.app/security` | yes |
| `site_keyword_status` | `has` / `planned` / `discusses` / `none` | `has` | no |
| `confidence` | `high` / `low` | `high` | no |
| `campaign_usable` | boolean | `true` | no |
| `site_keyword_sentence` | the **whole pre-rendered sentence** with its period and one trailing space | `Noticed you hold SOC 2 Type II certification. ` | yes |

**`campaign_usable` is the gate, and it is deliberately stricter than `site_keyword_hit`.** True only
when `status == "has"` AND `confidence == "high"`.

### ⚠️ `site_keyword_line` is emitted ONLY when `campaign_usable` is true

It is `""` otherwise — **including on rows where `site_keyword_hit == "yes"`.** This is not a
downstream convention an operator is trusted to remember. It must be computed that way, and
`campaign_usable` must be computed **first**.

**Why this is written this hard.** In the graded test the judge returned, for one domain:

```json
{"mentions": true, "status": "discusses", "confidence": "low",
 "line": "you passed your SOC 2 audit on the first try"}
```

The evidence URL was a **prompt-template marketing page on that company's own site** — the sentence
had been scraped out of an *example cold email printed inside their own content*. **That company had
passed no such audit.** `site_keyword_hit` was `yes`, so any pipeline that ships the line whenever
there is a hit **sends a fabricated compliance claim about the prospect's own company, to that
company.**

A row that is a hit but not usable is still a perfectly good **filter** answer. Keep the hit flag for
segmentation. Just never let it drive copy.

### Coverage expectation

9/10 rows usable (90%) in the graded test: six genuine hits, four abstains (three correct).

**Read that carefully before making the variable mandatory.** On a real list roughly **half to two
thirds of rows will abstain**, because most companies do not mention most keywords. **The 90% is the
accuracy of the answer, not the fill rate.**

**And the 90% is retrieval accuracy, not copy quality.** Among rows that **cleared** the gate,
roughly **1 in 6 carried a grammar or brand-casing defect** a human would have to fix by hand.
Measured: one row shipped `campaign_usable=true` with "you have SOC 2 Type 2 attestation" — missing
an article. Another shipped "linear undergoes regular SOC 2 audits" with the brand lowercased,
because **the model itself wrote it lowercase, and a sanitizer's brand guard only prevents the
sanitizer from lowercasing — it does not re-capitalize what arrived lowercase.**

**Neither defect is caught by anything downstream.** That is why §7 makes a 20-sample human grammar
read a required pre-launch step.

### Downstream gate: the half to two thirds that abstain

⚠️ **Spintax cannot do this job.** It picks a variant **at random** and cannot branch on whether a
variable is empty. `{Noticed {{site_keyword_line}}.|Quick one for you.}` still renders `Noticed .`
half the time on abstain rows.

**Mechanism A (default): pre-render the whole sentence, ship a blank on abstain.**

That is what `site_keyword_sentence` is for. It contains the **entire** sentence including its period
and one trailing space, or `""`. Put it in the body by itself, with nothing around it:

```
Hi {{first_name}},

{{site_keyword_sentence}}{{value_prop_line}}
```

On a usable row: `Noticed linear undergoes regular SOC 2 audits. Most teams we work with...`
On an abstain row: `Most teams we work with...` — **no gap, no stray period, no leading space.**
Nothing is left to an operator's memory, because the emptiness is baked into the value.

**Mechanism B: segment the list.** Filter on `campaign_usable == true` at upload and never let an
abstain row into the campaign. Then the variable is mandatory and Mechanism A is unnecessary.
Cleaner copy, smaller list.

**At a 50-66% abstain rate, Mechanism B is usually the right call** — running the covered rows as
their own campaign beats papering over two thirds of the list with blanks.

## 3. Source chain (cost-tagged)

| # | Source | Cost | Call | Result |
|---|---|---|---|---|
| 1 | SERP API + **literal-phrase filter** + model judge | CHEAP | `site:{domain} "{keyword}"`, limit 10, then the §6 judge | **measured 90% usable, 6/10 rows were hits** |
| 2 | A semantic entity-search API | METERED | for a single high-value row only | untested |
| 3 | Direct fetch of guessed paths (`/security`, `/trust`) through a rendering proxy | METERED | grep the literal phrase | untested. Only when you specifically suspect the page exists but is not indexed |

**No cache. Recompute — it is cheap.** At roughly $0.59 per 1,000 rows blended, a repeat check on a
domain another campaign already ran is worth less than a tenth of a cent. If a list has real internal
overlap, dedup on `(domain, keyword)` before the run.

### Cost, and a correction worth internalizing

| Leg | Unit | Per 1,000 rows |
|---|---|---|
| SERP call | ~$0.0005 per request | **$0.50** |
| Model judge | 1,335 in + 53 out per row | **$0.09** |
| **Blended** | | **$0.59** |

An earlier draft put this at $0.09/1k **by counting only the model leg**, on the assumption that the
SERP plan was flat-rate with no per-call charge. **That assumption was wrong.** Still cheap, but
budget against $0.59, not $0.09. When a cost line looks suspiciously low, check whether someone
counted only the leg they could see.

### Rejected alternatives

- **OR-chain queries.** See §1. Precision fell from 100% to 40%, and 80% to 20%, on two different
  cases.
- **Raw keyword matching without the judge.** One domain returned 7 on-domain results all literally
  containing the phrase, and **every one was a marketing or prompt-template page**, not a claim about
  the company. A naive filter marks that company a match.
- **Google's official Custom Search JSON API.** 100 free queries per day then metered, with a
  10k/day hard ceiling. Useless at list scale.
- **A browsing agent per row.** It works, but it is credits per row for something one search plus one
  cheap model call does for a tenth of a cent. Keep browsing agents for jobs that need a browser.
- **Bare `site:domain` with no keyword.** Returns whatever the engine feels like ranking and answers
  no question.

## 4. Verification

**VERDICT: PASS 9/10 (90%)** | SERP `site:` query → literal-phrase filter → model judge at minimal
reasoning effort | p50 1.7s/row | ~$0.59/1k blended.

Tested on 10 real B2B software domains with the keyword `SOC 2`, including 2 true negatives and 3
hard rows. Zero errors, zero rate limits across ~54 calls at concurrency 2. **The one failing row was
a copy-grammar failure, not a retrieval failure.**

**A post-review fix worth knowing about.** A verifier pass found the shipped script set
`site_keyword_line` on **every hit**, not only on gate-passing rows — so the fabricated compliance
claim in §2 **would have reached the sequencer despite the documented gate.** The gate was documented
correctly and implemented wrongly. That is the failure mode to watch for in your own build: a rule
that lives only in prose.

⚠️ This verdict covers the script path. **It does not cover the Clay implementation.**

## 5. Clay implementation

### Step 0, before you build anything: verify the search by hand

**Run the exact query for 3 to 5 real domains from your actual list and read the results with your
own eyes before you build a single column.** This is not optional.

A query that looks obviously right can return a completely different company:
`site:patagonia.com "SOC 2"` returned **10 results, zero of which contained the phrase** — all
matching a company whose name contains "Soc Trang". Ten minutes here saves a rebuilt table.

You are checking four things. Any one failing means fix the keyword before you scale:

1. Are the results actually **on** the domain you asked for?
2. Does the snippet **literally** contain your keyword, or did the engine fuzzy-match?
3. When the keyword is there, is it **the company talking about itself** — or a blog roundup, a
   customer logo wall, a job post, a forum thread?
4. Does the domain you expected to **miss** actually come back empty? **If everything hits, your
   keyword is too generic to filter on.**

Then:

- **`clay-table.md`** — the 11-column build, including a dependency cycle that will otherwise stop
  your table from building at all.
- **`clay-workflow.md`** — the CLI-buildable version.

## 6. Locked prompt

Model: a nano-class reasoning model — at 1,335 input plus 53 output tokens per row it is cheaper than
a mini-class model here (~$0.088/1k vs ~$0.23/1k), **so nano wins inside Clay too**, which is the
opposite of most playbooks in this library.

Params: `max_completion_tokens=1200`, **`reasoning_effort="minimal"`**, JSON response format, no
`temperature`.

**Minimal reasoning effort is load-bearing, not a tuning preference.** Without it, the model burned
past 1,800 completion tokens on reasoning and returned `finish_reason=length` with **empty content on
2 of 10 rows**. With it: measured **0 reasoning tokens**, and judge latency fell from **17.6s to
1.1s**.

```text
You judge whether a company's own website really talks about a given keyword, and you write one short line of outreach copy about it.

You will be given: a company domain, a keyword, and up to 5 Google results returned by the query site:<domain> "<keyword>".

Return JSON only, exactly these keys:
{"mentions": true|false, "status": "has"|"planned"|"discusses"|"none", "evidence_url": "", "line": "", "confidence": "high"|"low"}

How to decide "mentions":
- true only when a result is a page the COMPANY published about ITSELF and the keyword describes that company, its product, its service, its customers, or its own credential.
- false when the keyword only appears because the page is a directory listing, an integration or partner page about a DIFFERENT company, a user forum post, a job board scrape, a customer logo wall, a press roundup, or a generic blog post not about this company.
- false when no result is from the company's own domain or a subdomain of it.
- false when the only match is an unrelated word that happens to contain the keyword letters.

How to set "status":
- "has" when the page shows the company already does or holds the thing.
- "planned" when the page shows it is on a roadmap, in progress, requested, or coming soon.
- "discusses" when the company writes about the topic but the page does not show it holds or plans the thing itself.
- "none" when mentions is false.

Rules for "line":
- It must complete this sentence with correct grammar: "Noticed <line>."
- NEVER start the line with "Noticed", "noticed", "I noticed", "that", or "you have". The word "Noticed" is added automatically in front of your line. Starting with it produces "Noticed Noticed ..." which is broken copy.
- Write what you noticed about THEM, as a fact about the company. Never describe the web page itself. Do not write "is mentioned on", "the page says", "listed on your site", "in your security documents".
- Start with a lowercase letter UNLESS the first word is a proper noun, a brand name, or an acronym. Keep acronyms and brand names in their correct capitalization everywhere (SOC 2, HIPAA, HubSpot, ISO 9001).
- No trailing period. No em dashes. No quotes inside it.
- 5th-grade reading level. Under 90 characters.
- State only what the snippet proves. Never invent a fact, a date, or a number. If status is "planned", say it is planned.
- If mentions is false, return "" for line and "" for evidence_url.

Rules for "confidence":
- "high" when the snippet itself contains the keyword and the page is clearly the company's own page.
- "low" when you inferred it, or the page could belong to someone else.

Examples:
Input: domain=linear.app keyword=SOC 2 results=[{"title":"Security","url":"https://linear.app/security","snippet":"Linear undergoes regular Service Organization Controls audits (SOC 2 Type II)."}]
Output: {"mentions": true, "status": "has", "evidence_url": "https://linear.app/security", "line": "you run SOC 2 Type II audits", "confidence": "high"}
Input: domain=smallco.io keyword=SOC 2 results=[{"title":"Roadmap","url":"https://feedback.smallco.io/roadmap","snippet":"SOC 2 security certification - planned"}]
Output: {"mentions": true, "status": "planned", "evidence_url": "https://feedback.smallco.io/roadmap", "line": "SOC 2 is still sitting on your public roadmap", "confidence": "high"}
Input: domain=midco.com keyword=SOC 2 results=[{"title":"Trust","url":"https://trust.midco.com/","snippet":"We are in the middle of our SOC 2 Type 2 audit window."}]
Output: {"mentions": true, "status": "planned", "evidence_url": "https://trust.midco.com/", "line": "you are partway through your SOC 2 Type 2 audit", "confidence": "high"}
Input: domain=acme.com keyword=chess results=[{"title":"Best chess apps 2026","url":"https://acme.com/blog/roundup","snippet":"We ranked 20 chess apps."}]
Output: {"mentions": false, "status": "none", "evidence_url": "", "line": "", "confidence": "low"}
Input: domain=acme.com keyword=SOC 2 results=[]
Output: {"mentions": false, "status": "none", "evidence_url": "", "line": "", "confidence": "high"}

PER-ROW DATA FOLLOWS.
```

The static prefix measures about **1,030 tokens — just over the 1,024-token caching minimum**, so at
volume it caches at roughly a 90% discount. **Interpolating row data into it kills that discount.**

Per-row data goes last, as the user message:

```text
domain=<domain>
keyword=<keyword>
results=[{"title":"...","url":"...","snippet":"..."}]
```

**Verifier pass: not needed.** The judge never sees the open web, only snippets returned for this
exact domain, and the prompt forbids stating anything the snippet does not prove. The hallucination
surface is a claim drifting from its snippet, which the deterministic guards catch more cheaply: the
literal-phrase filter proves the keyword is in the text, and the evidence URL lets a human check in
one click.

⚠️ **The one thing to watch is a stale snippet** — a search cache can be months old. **If your keyword
is time-sensitive** (a funding round, a launch date, a "coming soon"), this is the wrong playbook.

**Truncation guard:** `finish_reason=length` means retry, never abstain. After 3 failed attempts,
record the row as an **ERROR** and exclude it — never as an abstain.

## 7. Edge cases and failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Results returned but none contain the keyword | **Search engines do not strictly honor quoted phrases on `site:` queries.** One query returned 10 results matching an unrelated company whose name shared the letters | A deterministic literal-phrase filter over title plus snippet **before** the model runs. **Never trust the raw hit count** |
| The line quotes a stale claim that contradicts the company's current page | `site:` includes subdomains, and `community.` / `forum.` subdomains are **users talking, not the company.** A stale forum answer outranked the company's own current security page | Drop `community. forum. forums. discuss. answers. feedback. ideas. status. help.` hosts before judging |
| Every row on a domain "matches" but the claims are nonsense | The keyword appears in blog roundups, prompt templates, integration directories, customer logo walls | The `status` + `confidence` gate. Only `has` + `high` reaches copy |
| Copy renders `Noticed Noticed you hold SOC 2.` | The model prepends the sentence frame. **Happened on 3 of 10 rows despite an explicit prompt rule** | A deterministic sanitizer strips a leading "Noticed"/"I noticed"/"that". **A regex, not a prompt rule** |
| Copy renders `Noticed .` | The model returned `mentions: true` with `status: "none"` and an empty line | A row is a hit only when `mentions === true` **AND** `status !== "none"` **AND** the sanitized line is non-empty |
| Copy renders `Noticed .` on **half the list** | The body used `Noticed {{site_keyword_line}}.` and the variable is correctly blank on every abstain row | Use the pre-rendered sentence field alone, or segment on `campaign_usable`. **Spintax cannot branch on emptiness** |
| A junk row for the domain "domain" | A CSV header row processed as data — burning a real search call | Skip a first line whose first field is literally `domain` |
| Brand name lowercased | The sanitizer applied lowercase-first blindly | Skip lowercasing when the first word is an all-caps acronym, carries an internal capital, or matches the domain root. ⚠️ **This does not fix a name the model itself wrote lowercase** |
| The same query returns 7 results, then 0, then 7 | **Search results are genuinely non-deterministic between calls.** Observed on three domains | **Retry once before recording a hard negative.** Never treat one empty response as proof of absence |
| Empty content, `finish_reason=length` | Reasoning overrun | Minimal reasoning effort plus retry. Exhausted retries is an **ERROR row, never an abstain** |
| The HTTP column 400s or 431s | Raw quotes and colons in the URL, or oversized headers | **Percent-encode the whole query string.** Set `automapInputs: false` on workflow nodes |
| The evidence URL does not contain the quoted phrase | The judge quoted one result and cited another | If the URL is load-bearing, verify the phrase is on that specific page |
| Fetching the evidence page returns nothing | Trust centers and feedback boards are JS-rendered | Verify against a first-party page on the main domain, or use a real browser |

### Required pre-launch step: the 20-sample grammar read

**Before any campaign using this variable goes live, a human reads 20 rendered samples.** Not
optional, and not a spot check you skip when the batch "looks fine".

**The gate catches false claims. Nothing in this playbook catches bad grammar, and bad grammar is
measurably common** — roughly **1 in 6 rows that clear the gate.**

1. Pull 20 random rows where `campaign_usable == true`.
2. Render each into the **actual frame**: `Noticed {{site_keyword_line}}.`
3. **Read all 20 out loud.** Mark any that need an edit of any size.
4. Grep the **rendered output** for em dashes, double periods, a leading "Noticed Noticed", and a
   stray "Noticed ." with nothing between.
5. **If more than 1 of 20 needs an edit, do not launch.** Fix the prompt, re-run, read a fresh 20. If
   a single brand name keeps arriving lowercased, add it to the sanitizer's proper-noun guard rather
   than hand-editing rows.

Note step 4 lints **rendered output**, not raw field values. A field that looks fine in a table can
render broken in a frame.

### Hard rules

- **One keyword, one query. Never an OR chain.** This is the defining rule of this playbook.
- **Manually verify your searches before scaling.** Step 0 of §5.
- **The hit count is never the filter, an error is never an abstain, and the line is blank unless
  `campaign_usable` is true.** A 429, a 5xx, an empty judge cell or an exhausted retry is an **ERROR
  row**: re-run it. A hit is a filter answer, not permission to ship copy.
- **Check your SERP provider's response shape.** A "light" endpoint often returns a flat array while
  the full endpoint nests results one level deeper — **and parsing one like the other silently
  returns zero rows** rather than erroring.
