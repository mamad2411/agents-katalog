---
name: playbook-ad-library
description: Produces a line about what a company is currently advertising on Facebook and Instagram, from the Meta Ad Library. Triggers on "are they running ads", "what are they advertising", "meta ad library", "facebook ads", "pull their ad copy", "who is spending on paid social". Outputs ad_library_line, a lowercase clause that completes "Noticed <line>."
---

# Playbook: Meta Ad Library

> All rules here are best practice, not law. Override any of them when the campaign calls for it; note the best practice once and move on.

**Use when:** the angle depends on the prospect spending money on paid social right now — creative
agencies, UGC shops, CRO and landing-page services, media buyers, attribution and analytics tools,
or anyone selling to ecommerce brands that already advertise.

**Do not use when:** you only need to know a company exists or sells online (`playbook-tech-on-website`),
or you want LinkedIn organic activity (`playbook-linkedin-engagement`). Facebook and Instagram only —
not Google Ads, not TikTok, not LinkedIn ads.

**One-line output:** `ad_library_line = "you are using ai to run outbound campaigns with one command"`

## 1. Trigger and scope

One question per row: **is this company running ads on Meta right now, and what is the ad actually
about.**

**The hard part is not the ad library. It is the input.** The Meta Ad Library is keyed to a
Facebook **Page**; your lists are keyed to a **company domain**. Nothing maps one to the other for
free. So most of this playbook is a discovery chain that turns a domain into a *verified* Facebook
Page URL, plus the gates that stop that chain from returning the wrong company's page. Ungated, it
confidently returned **a golfer's page for `ridge.com`** and **a pottery studio for `clay.com`**.

Two things it deliberately does not do:

- **It never reports a raw ad count to a prospect.** Meta's `totalCount` counts collated
  duplicates and overstates reality — one brand showed 950 for what was really about three
  creatives.
- **It never guesses.** When a page cannot be verified, the row abstains with an empty string
  rather than shipping a plausible-looking wrong page.

## 2. Output contract

### Inputs required per row

| Field | Type | Source | Required? |
|---|---|---|---|
| `domain` (bare, lowercase, no `www`, no scheme) | string | your list | yes |
| `company_name` (cleaned) | string | your list, cleaned by `playbook-company-name-cleaning` | yes — step 2 searches on it |
| `fb_page_url` | string | this playbook produces it; pass it in to skip to step 4 | no |

### Output fields

| Field | Type | Example | Max | Null? |
|---|---|---|---|---|
| `ad_library_line` | string | `you are using ai to run outbound campaigns with one command` | 20 words / ~120 chars | no, use `""` |
| `ad_theme` | string | `ai outbound automation` | 4 words | no, use `""` |
| `active_ad_count` | integer | `33` | n/a | no, use `0` |
| `fb_page_url` | string | `https://www.facebook.com/smartleadai` | 120 chars | no, use `""` |
| `evidence_ad_id` | string | `26618345894517042` | 32 chars | no, use `""` |
| `ad_confidence` | enum | `high` or `low` | n/a | no |

⚠️ **Name mapping.** The model returns the JSON key `confidence`; the output field is
`ad_confidence`. The rename happens in the parse step, **not in the prompt** — the prompt is
evidence-locked and its key names must not drift.

**Abstain value:** `""` for every string, `0` for the count. Never "null", never "N/A", never a
guessed page.

### Coverage expectation

6/8 rows usable (75%) on the graded re-run: **8/8** on page discovery, **6/6** on the ad fetch with
zero vendor errors, **5/6** on the line writer.

**Read the split, not the headline.** Of the 5 pages that actually carried ads, 3 produced a
shippable line, 1 was blanked by the spam-word gate, and 1 correctly abstained. A prompt that
abstained on everything would still score 3/8 on this rubric and be worthless, so **track the
positive-line rate on ad-bearing pages separately.**

Expect roughly **half** of a cold list to end with an empty line, mostly because no Facebook page
can be verified. Treat the variable as **spintax-optional, never mandatory.**

### Copy-fit rules

- Slots into: `Noticed {{ad_library_line}}.`
- First character lowercase, no trailing punctuation.
- **Never begins with "noticed", "saw", or "seeing"**, or the sentence stutters.
- No quotation marks, no raw ad counts, no em or en dashes.
- 5th-grade reading level, 16 words target, 20 words hard cap.
- The word "angle" is banned. Name the offer or the product instead.

### Downstream gate

If empty: drop the clause through spintax and **keep the row**. "Not currently advertising" is
usually a targeting question for the strategist, not a disqualification. The exception: if the
campaign's whole premise is "you are running ads", decide up front whether empty rows route to a
different campaign variant.

## 3. Source chain (cost-tagged)

| # | Source | Cost | Call | Hit rate | Stop rule |
|---|---|---|---|---|---|
| 0 | **Cache** (45 days, keyed on bare domain) | FREE | lookup before anything else | depends on list overlap | **ALWAYS first.** Every paid step is gated on a cache miss |
| 1 | Company website HTML | FREE | `GET https://{domain}/`, then `/contact`, `/about`, browser UA, follow redirects. Un-escape `\/` to `/`, then regex for a `facebook.com/<slug>` link | **38%** measured | always run, it costs nothing |
| 2 | SERP search | CHEAP | `site:facebook.com "{Company Name}"`, limit 10, then **three gates** | 40% of step-1 misses | only if step 1 found nothing |
| 3 | JS-rendering proxy | METERED | render the homepage, same regex as step 1 | 1/1 measured | **only** if step 1 returned HTTP 403 or 429 AND step 2 found nothing. Never for a plain "no link on the page" miss |
| 4 | **Apify Meta Ad Library** | METERED ($4.20/1k pages) | actor `apify/facebook-ads-scraper`, input `{"startUrls":[{"url":"<fb_page_url>"}],"onlyTotal":true,"activeStatus":"active"}` | 6/6 pages, 0 errors | only on a cache miss **and** a verified page |
| 5 | Model line writer | CHEAP ($0.149/1k rows measured) | 3 drafts, deterministic gates, then a truth judge. 3 to 4 calls per row | 6/6 | every row where step 4 returned a non-template ad |
| 6 | Keyword-search rescue | **EXPENSIVE** ($33.60/1k rows; **cap 100**) | ad-library keyword URL, `resultsLimit: 8`. **Bills per AD, not per page** | very low precision | only on explicit request, batches under 100 |

### The cache, because the scraper bills per page every single time

Without a cache, the same DTC brand on three client lists is billed three times, and a re-run of
the same campaign is billed again. Two things are mandatory before any paid step:

1. **Dedup the input on normalized bare domain** (lowercase, strip scheme, `www.`, path).
2. **Check a 45-day cache.**

Suggested shape:

```sql
CREATE TABLE ad_library_cache (
  domain            text PRIMARY KEY,
  fb_page_url       text,
  page_source       text,          -- website_html | serp | proxy | abstain
  active_ad_count   integer,
  ad_library_line   text,
  ad_theme          text,
  evidence_ad_id    text,
  ad_confidence     text,
  last_checked      timestamptz NOT NULL DEFAULT now()
);
```

**Cache the abstains too.** A domain with no discoverable Facebook page will not grow one this
month, and re-running discovery burns a search and possibly a proxy call every time. The ad payload
is the part that goes stale, hence 45 days rather than forever.

Most playbooks in this library have **no** cache — recompute is cheaper than storage. This one
earns it because the scraper is the most expensive tier in the stack. Do not carry a cache step
into a new playbook by analogy.

### Three gates that make step 2 safe

All three are load-bearing.

1. **Root-page gate.** Accept a result only when the Facebook URL has **exactly one path segment**.
   `facebook.com/hexclad/` passes. `facebook.com/JohnDaly/videos/...` is rejected — that is
   somebody else's page talking about the brand.
2. **Title-match gate.** The result title, normalized to lowercase alphanumerics, must contain the
   normalized company name.
3. **Brand-label gate.** The page **slug** must start with the domain's second-level label, or be a
   prefix of it. `ridge` for ridge.com passes; `smartleadai` for smartlead.ai passes;
   `KettleandFireBoneBroth` for kettleandfire.com passes; **`theclayplant` for clay.com does not.**

Gates 1 and 2 took false positives from 2 of 5 rows to 0 of 5. **They were not enough.** A query
for `Clay` returned `facebook.com/theclayplant` — a pottery business, root URL, title "The Clay
Plant" which *contains* "clay" — and it got billed. A patch that also accepted a title-first-segment
match then let `facebook.com/adrianesmithbrowncreative` through, because its title began with the
word Clay. **The gate now looks only at the slug: the title is whatever the page owner typed, the
slug is the page identity. Never re-add a title escape hatch.**

Recall cost, stated plainly: a brand whose slug shares nothing with its domain (`shophexclad` for
hexclad.com) now abstains. **That is the right trade.** A wrong page costs the same as a right one
and produces a confidently wrong sentence in a stranger's inbox.

### Rejected alternatives

- **Meta's own Graph API `ads_archive`.** Outside the EU it only returns political and issue ads, so
  it returns nothing for commercial brands, and it needs a verified Business app plus ID
  verification.
- **Scraping `facebook.com/ads/library/` directly.** The page is a React app whose data comes from
  an authenticated GraphQL call, so the HTML contains no ads. That is exactly what the actor solves.
- **Company-enrichment vendors as a page source.** They resolve LinkedIn well and Facebook poorly;
  most company objects do not expose a Facebook page at all.

## 4. Verification

**VERDICT: PASS 6/8 (75%)** | chain = website HTML → SERP `site:facebook.com` behind three gates →
Apify `facebook-ads-scraper` with `onlyTotal:true` → model line writer, best of 3 behind a
deterministic gate stack plus a truth judge | p50 1.1s discovery, ~8s per page batched, 2.6s per row
on the writer | **~$3.30/1k METERED** ($3.15 scraper at the 75% discovery rate, $0.149 model).

**History, because you will find the older verdict.** The first run scored **FAIL 5/8 (63%)**. Its
layer scores located the failure precisely: the data layer was 6/6 pages with zero vendor errors and
the line writer was 4/6. **That is a prompt problem, so the fix was a prompt loop, not a new source.**
The source chain is unchanged and no fallback source was opened.

What the re-run changed: prompt v2 moved to a system block with 13 few-shot examples as faux prior
turns, and added the rules the failures demanded (never name the prospect's own brand, one product
not a list, abstain on brand films). Five deterministic guards were added around it, and the writer
now samples 3 drafts and keeps the first that passes every gate.

**Stability was the specific complaint** ("the line writer is not stable run to run"). The final
configuration was replayed 3 times over the same payload: **15 of 15 row-rounds usable.** Wording
varies; shippability does not.

**Still failing: `anthropic.com`.** It advertises under a page named `Claude` with landing pages on
`claude.com`, so neither the website scrape nor a domain-match gate can connect it to the corporate
domain. Documented, not papered over. **Loosening the gates to catch it reintroduces the golfer and
the pottery studio.**

⚠️ **This verdict does not cover running the chain inside Clay, which has never been tried.** Every
Clay-specific claim in `clay-table.md` is an inference, not an observation.

Re-test if the actor changes its `onlyTotal` billing shape or input schema, if page discovery drops
below 50% on a real list, or if anyone edits the §6 prompt.

## 5. Clay implementation

- **`clay-table.md`** — the 19-column build.
- **`clay-workflow.md`** — the CLI-buildable version.

⚠️ Both unbuilt. The verified path is the script chain.

## 6. Locked prompt

Model: a small reasoning model outside Clay; **`gpt-4o-mini` inside Clay** (Clay's AI column does
not expose reasoning effort).

Params outside Clay: `reasoning_effort="minimal"`, `max_completion_tokens=2000`,
`response_format={"type":"json_object"}`, no `temperature`, flex tier for batch.

Measured: without minimal reasoning effort this prompt returned `finish_reason:"length"` with empty
content on **6 of 6 calls**. With the static prefix first, the prompt cache hit **86%** of prompt
tokens (43,264 of 50,065) — that is what keeps a 4-call-per-row design at $0.149 per 1,000 rows.

### System block (static prefix, part 1)

```text
You write one short merge field that gets dropped into the middle of a cold email sentence.

The sentence it goes into is exactly this, and you are writing only the AD_LIBRARY_LINE part:
"Noticed AD_LIBRARY_LINE."

You are given one company's currently running Facebook and Instagram ads: the page name, how many ads are running, and the text of a few of those ads.

Rules:
1. Write at a 5th-grade reading level. Use short, common words. If a shorter word means the same thing, use the shorter word.
2. Your text has to fit the sentence around it. Read the whole sentence back with your text in place before you answer. Start with a lowercase letter. Never start with the word noticed, saw, or seeing. Do not start with a comma or the word and. Do not end with a period. 16 words or fewer.
3. Never use an em dash or an en dash. Use a comma, or split the idea, or use and, so, or because.
4. Never state a fact that is not in the ad text you were given. Do not guess what the company sells, do not round numbers, and do not describe what the company probably does.
5. If the ads do not support a specific, true line, return an empty string for ad_library_line and low for confidence. Never write N/A, unknown, none, not available, a dash, or a placeholder in brackets. An empty answer is always better than a wrong one.
6. Output only the JSON object described below. No preamble, no reasoning, no markdown fence.

Output shape, exactly these keys:
{"ad_library_line": "...", "ad_theme": "...", "evidence_ad_id": "...", "confidence": "high|low"}

Task rules:
7. Never write the company's own name, or any word of it, inside ad_library_line. They already know who they are, and naming them back reads like a robot. Write what the ads sell, not who is selling it. This holds even when the ad text repeats the brand name in every sentence.
8. Name ONE thing, never a list. Pick the single offer, product, promise, or promotion the ads push hardest. When several ads repeat one idea, use that idea. When the ads push different products, use the product in the first ad and write only that one. A line that names two or more products reads like a catalog and is worse than no line. Never join two products with the word and. When in doubt, write about the ad listed FIRST.
9. Return an empty ad_library_line when the ads are brand films, jokes, or slogans with no product, no offer and no landing page, when the only ad text is a template token like a double-brace placeholder, or when the ads say nothing a stranger could repeat back.
10. VOLUME_PHRASE is given to you. When it is allowed you may write the words a lot of ads. When it is banned, write nothing at all about how many ads are running. Never write a raw ad count in either case.
11. Never use the words angle or angles. Never use quotation marks, trademark or registered symbols, star characters, emoji, or a web address.
12. Some ads are written in Spanish, German, French or another language. Always write the line in English.
13. Write about what the ads sell, never about the advertising itself. Banned phrases: a line about, a campaign about, in multiple regions, in several languages, across regions, various markets.
14. Write every word out. No apostrophes and no contractions: write you are, not you're, and write everyone, not everyone's.
15. ad_theme is two to four lowercase words naming the repeated idea across the ads, or an empty string if unclear. evidence_ad_id is the id of the single ad you used, or an empty string when you returned an empty line.
```

### Examples (static prefix, part 2)

**13 few-shot pairs as faux prior conversation turns — `user` then `assistant` — not a bulleted
list inside the system message.** This is the single change that did the most work: a controlled
probe measured roughly **2 of 6** clean outputs with no examples against **6 of 6** with 12 example
pairs.

They cover, in order: a clean product ad; the brand-name trap (the ad body repeats the brand, the
answer never does); a Spanish ad answered in English; a claim-led DTC ad; a B2B SaaS row with volume
banned at 33 ads; an apparel collection; a brand film that must abstain; zero ads; template-token-only
ads; a discount promo; a limited release; a multi-product page that collapses to one product; and a
thin but real service offer.

**Every example company is invented. No graded row is ever also an example**, or the harness is
measuring memorization.

### Per-row message (last)

```text
COMPANY: {{Facebook Page Name}} | ACTIVE_ADS: {{Active Ad Count}} | VOLUME_PHRASE: {{Volume Phrase}} | ADS: [{{Ad Samples}}]
```

`VOLUME_PHRASE` is computed **in code**, and it is a required input, not pseudocode. The model wrote
"a lot of ads" for a page with 33 active ads, twice, when the rule lived in the prompt. **Any rule
with a number in it belongs in code.** Compute it as `activeAds >= 50 ? "allowed" : "banned"`. The
lint gate is the backstop: a volume claim while the phrase is banned blanks the line.

### The guard stack (this is not optional)

The prompt alone scored 4/6. The prompt **plus these guards** scored 6/6, and 15 of 15 on the
stability replay.

| Guard | What it does | The line that caused it |
|---|---|---|
| brand-token lint | blanks any line containing the first word of the page name, the squashed page name, or the domain label (4+ chars only, so "AI" and "Co" cannot blank a good line) | `you are promoting ridge wallets and a metal powerbank` |
| list-shape lint | rejects 2+ commas or 2+ uses of "and" | `for wallet, powerbank, rings, and edc wallet` |
| repeated-word lint | rejects any 5+ letter word used twice | `a single command outbound with outbound tools` |
| symbol / meta lint | rejects quotes, curly apostrophes, trademark and star symbols, emoji, URLs, "do not name a product", "in multiple regions" | `you are not showing a real product or offer in the ads` |
| **ungrounded-words check** | zero-cost, deterministic. Every content word of 4+ chars, de-pluralized and stemmed to 4, must appear in the ad text (the landing URL counts) | `gym wear and shoes` on a page whose ads never said shoes |
| banned-word lint | blanks any line carrying a spam-trigger word. A generated merge field is prospect-visible copy, bound by the same spam list as hand-written copy | `you are pushing nonstick cookware that is free from forever chemicals` |
| **truth judge** | mandatory, **100% of lines, never a sample**. One extra model call with its own few-shot examples. ~$0.02 per 10,000 rows | catches invented meaning that survives word-level grounding |
| best of 3 | 3 drafts issued together, first passing draft wins | one draft was shippable about 2 runs in 3 |
| targeted retry | on total failure, the least-broken draft goes back with the specific rule it broke | a blind retry reproduces the same mistake |
| **no nudge on 3 blanks** | 3 independent blanks are taken at face value | pushing past them produced `you are pushing oat milk drinks but do not name a product or offer` |
| prefer English ads | foreign-language ads dropped when any English ad exists, so grounding stays valid | `gym wear and trainers` derived from a Spanish ad |

**The truth judge IS the verifier pass, and it is required.** An earlier version of this playbook
argued a verifier was unnecessary because every claim is copied out of ad text the same call is
looking at. That was **wrong twice in one graded run**, both times by adding a product the ads never
mentioned. Structural QC cannot catch semantic error.

**Truncation guard:** `finish_reason=length` means retry, never abstain. A naive identical retry does
**not** recover — the model deterministically spends the same budget on reasoning. The retry must set
minimal reasoning effort and raise the token cap.

## 7. Edge cases and failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Discovery returns another company's page (a golfer for `ridge.com`) | The top SERP result for `site:facebook.com "<brand>"` is often a post on somebody else's page mentioning the brand | Root-page gate: exactly one path segment. Then the title gate |
| Homepage returns 200 but no Facebook link, on an obviously social-active brand | Modern frameworks embed footer links inside JSON as `https:\/\/facebook.com\/ridge` | **Replace `\/` with `/` before the regex.** This one is easy to miss and costs you 38% of your free hits |
| Homepage returns 403 | Bot protection | The **only** case that justifies the rendering proxy |
| Ad body is `{{product.brand}}` and title is `{{product.name}}` | Dynamic catalog ad — Meta fills the product in at serve time, so the library stores the template | Filter any ad whose body **and** title are both template tokens **before the prompt sees them** |
| `totalCount` says 950 but every ad body is the same three sentences | It is a collation count including near-duplicate creatives, placements and locales | Never quote the number. Only "a lot of ads", only above 50 |
| Ads come back in Spanish, German or French | Non-US brand or a global page | The prompt answers in English regardless; drop foreign ads when any English ad exists |
| Every ad has an empty `linkUrl` | Brand-awareness video ads with no CTA, common for CPG | You lose the landing-domain verification signal. Fall back to matching the page name, and set confidence low |
| The company advertises but the chain abstains | The brand runs ads under a product-brand page with a different name and landing domain | Known limitation, no cheap fix. **Do not paper over it by loosening the gates** |
| Discovery returns a company sharing one word of the name | The title gate is a **substring** test, so any one-word or generic company name walks through | The brand-label gate, on the slug only |
| The whole batch dies with `ECONNRESET` **after** the paid call went out | One unhandled transient socket error. **Money spent, nothing returned — the worst possible failure shape** | Retry the paid call 4x with exponential backoff, retry model calls on 429/5xx, and wrap each row so one bad row cannot abort the batch. An errored row is a **retry candidate, never an abstain** |
| The line names a product the ads never mentioned | The model pattern-matched the category instead of reading the ads. Format lint cannot see this, and the judge alone missed it twice | Run the free ungrounded-words check **first**, then the judge. Both, in that order — the free check is also the more reliable one on this failure |
| The line is a laundry list | Several products in the payload and nothing told the model to pick one | Prompt rule 8 **plus** the list lint **plus** the multi-product few-shot. All three; the rule alone did not hold |
| The line names the prospect's own brand back at them | The ad copy repeats the brand in every sentence and the model copies it | Prompt rule 7 plus the brand-token lint. **This was 3 of 4 lines before the fix** |
| A rich-ad row returns an empty line once in ~4 runs | Single-draft variance; an empty string is a legal abstain, so a blank was accepted silently | Best of 3 drafts. **Do not** solve it by nudging the model after a blank |
| Every line on a non-English page is blank | The grounding check is an English lexical test, and a correct translation is word-for-word ungrounded | Drop foreign ads when English exists; otherwise mark the row multilingual and let the judge arbitrate, which usually abstains. That is the safe direction |
| The scraper bills far more than expected | `onlyTotal` was omitted, so billing switched from **1 item per page** to **1 item per ad** | Always send `"onlyTotal": true`, and read the charged-event count back after every run |
| Model writes "Noticed noticed you are..." | The line started with "noticed" | The lint blanks it. Never ship a line that fails lint |

### Hard rules

- **Every paid call sits behind `verified page AND cache miss`.** A wrong page costs the same as a
  right one.
- **Always send `"onlyTotal": true`,** and read the charged-event count back after every batch to
  confirm it equals the page count. Never leave a paid batch running unattended. Keep a per-run row
  cap as a blast-radius control against a runaway loop.
- **Dedup on bare domain and check the cache before every paid call**, abstains included.
- **Truth-check 100% of lines, never a sample.** A vendor error is a retry, never "this company has
  no ads".
- **Never quote a raw ad count.** Only "a lot of ads", only above 50, via the code-computed volume
  phrase.
