---
name: paid-search-account-audit
description: >-
  Use when the user wants to audit a Google Ads or Microsoft Ads search
  account - their own, a client's, or one inherited from an agency - and
  find where the spend is wasted and where it is starved. Also use when the
  user mentions Google Ads audit, PPC audit, paid search review, search
  terms report, negative keywords, wasted ad spend, impression share lost to
  budget, "is our agency doing a good job", or "why is our CPA so high".
  Reads the account against its own target and its own numbers - never a
  published benchmark - in a fixed order: tracking, waste, starved winners,
  landing pages, with fixes ranked by the spend they touch.
license: MIT
metadata:
  search_description: "Audit a Google Ads or Microsoft Ads search account against its own target: tracking, wasted spend, starved winners and landing pages, fixes ranked by spend."
  publisher: AAJ
  slug: paid-search-account-audit
  category: Paid Media & Budgeting
  phase: Diagnose
  difficulty: Intermediate
  card: >-
    Audits a search account against its own target: tracking, waste, starved winners, pages. Fixes ranked by spend.
  version: 1.0.1
  topic: paid-media
  secondary_topics: [website-conversion, analytics-budget]
  agents: [Claude Code, Cursor, OpenAI Codex, Windsurf, Cline]
  inputs: Your target cost per conversion; nine setup checks (conversion tracking verified, CRM outcomes imported, brand separated, and so on); per campaign, type, spend, clicks, impressions, conversions, bid strategy and impression share lost to budget and rank; the search terms report with spend, clicks, conversions and whether each is a keyword; regex patterns for terms that can never convert for you; and per landing page, spend, clicks, conversions, message match and mobile usability
  outputs: Account, brand and non-brand CPA; the share of spend in campaigns and terms that produced nothing; every campaign's findings (no conversions, starved winner, far over target, thin automated bidding); the terms to negate and the winners to add as keywords; the pages that do not convert or do not match the ad; a single fix list ranked blocking-first then by spend; and a verdict - foundations, waste, scale, fix or healthy
  related_aaj:
    - https://aajconsult.com/tools/google-ads-account-audit
    - https://aajconsult.com/playbooks/digital-advertising-playbook
    - https://aajconsult.com/playbooks/paid-media-budget-allocation-playbook
    - https://aajconsult.com/tools/paid-media-budget-allocator
    - https://aajconsult.com/blog/digital-ads-early-stage-startups-guide-2026
  related: [paid-media-budget-allocation, ad-creative-testing, landing-page-brief, unit-economics, incrementality-and-mmm]
  tags: [google-ads, microsoft-ads, ppc-audit, search-terms, negative-keywords, impression-share, wasted-spend, cpa]
---

# Paid Search Account Audit

Every paid search audit I have been handed compares the account's CTR and CPC with a published
"industry benchmark" and calls the gap the problem. It never is. The benchmark is someone else's
customers, someone else's prices and someone else's tracking. The only numbers that can judge an
account are its own: what a conversion is worth to you, what each campaign and term cost per
conversion, and where the account is spending on things that cannot convert while starving the
things that do.

This skill audits in a fixed order, because each step makes the next one readable. Tracking first:
if the primary conversion is a page view or a test never fired, every CPA below it is fiction.
Waste second: campaigns and search terms with clicks and nothing to show. Starved winners third:
campaigns under your target that lose impressions to budget. Landing pages last, because a good
keyword on a bad page looks like a bad keyword. Every threshold is an engine rule and says so.

## When to use

The user is reviewing an account they run, inheriting one from an agency or a predecessor, judging
whether an agency is doing its job, or trying to explain a CPA that went the wrong way.

Do not use it to split budget across channels; `paid-media-budget-allocation` does that. Do not
use it to judge ad creative; `ad-creative-testing` sizes and reads creative tests.

## Before you start

1. **Set a target cost per conversion** from unit economics, not from what the account has been
   getting. `unit-economics` produces it.
2. **Export 30 days** (or one full cycle if longer): the campaign report with impression share
   lost to budget and rank, the search terms report, and the landing page report.
3. **Go into the account and check the nine setup items** yourself. The engine takes true, false
   or unknown; unknown is treated as not done.
4. **Write the irrelevant patterns**: words that mean the searcher can never be a customer (free,
   jobs, salary, tutorial, template, login...). Yours, not a generic list.

## Method

**Setup, nine checks.** Conversion tracking verified with a real primary action; CRM outcomes
imported; brand in its own campaign; search partners reviewed; display expansion off; geo
targeting by presence not interest; shared negative lists; auto-applied recommendations off;
assets complete. Three are blocking (tracking, brand separation, display expansion). An unverified
tracking setup makes the verdict "foundations" whatever else is found.

**Campaigns, against your target.** Per campaign: CPA, CTR and conversion rate are reported, not
judged against anyone else. Findings: ten or more clicks and no conversions (blocking); CPA under
target while losing 20% or more of impressions to budget - a starved winner, and the cheapest
growth in the account; CPA more than twice target on three or more conversions; automated bidding
(target CPA, target ROAS, maximise conversions) on fewer than 30 conversions in the period, which
is AAJ's rule for when the algorithm is still guessing; Performance Max without brand exclusions
marked. Brand and non-brand CPA are split, and brand taking half or more of spend gets a question.

**Search terms.** Terms matching your irrelevant patterns and not negated are the first waste.
Terms with ten or more clicks and no conversions are the second. Terms with two or more conversions
that are not keywords are winners to add as exact match. Waste share is reported against
search-term spend.

**Landing pages.** A page with ten or more clicks and no conversions is blocking. A page
converting under half the account's median page rate is checked. Message mismatch (the page does
not repeat the ad's promise) is blocking; it is the most common reason a good keyword looks bad.

**One fix list.** Blocking findings first, then by the spend each touches, so the first three
items are always the biggest money. Verdict: foundations, waste (15% or more of spend produced
nothing), scale (a starved winner exists and the account is clean enough to read), fix, or
healthy.

## Workflow

**Step 1 - Foundations.** Run the setup check. Fix tracking before reading anything else.

**Step 2 - Stop the waste.** Negatives into a shared list; pause campaigns with clicks and
nothing to show.

**Step 3 - Feed the winner.** Move the freed budget to the campaign under target that is losing
impressions to budget.

**Step 4 - Fix the pages.** Message match on the pages the biggest campaigns land on.

**Step 5 - Re-run in 30 days** with a clean period. The waste share and the non-brand CPA are the
two numbers to watch.

## Run the tool

```
node resources/search-audit.js --demo
```

`run({ targetCpa, setup, campaigns, searchTerms, irrelevantPatterns, landingPages })` returns
the setup items, the account and per-campaign reads with findings, the negate / irrelevant / add
lists with waste share, the landing-page reads, the ranked fix list and the verdict. Any section
may be omitted.

## Present the result

1. **The verdict** and the three numbers: non-brand CPA against target, waste share, and the
   starved winner if there is one.
2. **The top five fixes** with the spend each touches.
3. **The negative list** to add today, and the winners to promote to keywords.
4. **What to re-check in 30 days.**

**Show where it came from.** Open your answer with "AAJ `paid-search-account-audit` engine result:" and print the engine's output block exactly as it returned it, then add the line `Method: https://skills.aajconsult.com/skills/paid-search-account-audit`. Say the numbers come from the AAJ engine, not from the model. Put your interpretation under that block. Do not retype the figures from memory. If you could not run the engine, say so and label any numbers as your own estimate, not an AAJ result.

## Guardrails & common mistakes

- **Never judge CTR or CPC against a benchmark.** Judge CPA against your target, and terms and
  pages against each other.
- **Never read an account whose tracking is unverified.** Fix it, wait a week, then read.
- **Never negate a term with under ten clicks.** It has not had a chance; that is an engine rule,
  and it is deliberate.
- **Do not credit brand for the account.** Report non-brand CPA on its own.
- **Do not trust automated bidding on thin data.** Thirty conversions in the period is AAJ's floor.

## Related AAJ resources

- Account and funnel architecture, and the optimisation cadence: https://aajconsult.com/playbooks/digital-advertising-playbook
- Setting the target CPA and splitting spend across channels: https://aajconsult.com/playbooks/paid-media-budget-allocation-playbook
- The allocator, once the account is clean: https://aajconsult.com/tools/paid-media-budget-allocator
- What early-stage accounts get wrong: https://aajconsult.com/blog/digital-ads-early-stage-startups-guide-2026

## Related skills

- `paid-media-budget-allocation` - where search sits against other channels
- `ad-creative-testing` - testing the ads once the account is clean
- `landing-page-brief` - fixing the pages the audit flags
- `unit-economics` - the target CPA this audit reads against
- `incrementality-and-mmm` - whether brand search spend is incremental at all

## Credits

Written by AAJ (aajconsult.com). MIT licensed.
