---
name: search-term-miner
description: 'Sort paid search queries into keep, review, and exclude candidates using business fit and real performance evidence. Use to find waste without blindly blocking useful demand.'
---

# Search Term Miner

## Doctrine

The search terms report is where Google shows the demand it actually bought. A zero-conversion query can be clear waste, an under-tested query, or a legitimate offer that converts later. Classify by business fit first, then use spend, outcomes, conversion delay, and the account target to decide how confident the label should be.

## When to use

- During a weekly or monthly search-term review.
- Use a connected Google Ads MCP, or paste a search-term export with campaign, ad group, triggering keyword, match type, clicks, spend, conversions, and value.
- Bring the offer, valid customer intents, exclusions, target CPA or ROAS, and conversion delay when available.

## Run it

```
Run a READ-ONLY search-term review. Use live Google Ads data if connected; otherwise use the export I paste. Change nothing.

1. Confirm the business offer, valid acquisition intents, date range, currency, primary conversion, target, and conversion delay. Mark missing context.
2. Classify each useful term as:
   - keep: clearly fits the offer and has supporting evidence;
   - review: fit or performance is uncertain, or the sample is immature;
   - exclude candidate: clearly does not fit the business or has enough reliable evidence of waste.
3. For each term show campaign, ad group, triggering keyword, spend, clicks, conversions, CPA or ROAS when calculable, business-fit reason, confidence, and suggested negative scope for later review.
4. Rank exclude candidates by spend in this report. Protect real offers and known conversion paths, even when words such as "free", "template", or "how to" appear.
5. Show the total spend of exclude candidates inside the supplied report scope. Do not call it a percentage of the whole account unless total account spend was provided.
6. End with three lists: confirmed exclude candidates, needs review, and terms worth building around.

Do not add negatives. Hand confirmed candidates to the Negative Keyword Builder for match-type and collision checks. End with "No changes were made."
```

## Guardrails

- Zero conversions is not automatically waste. Consider business fit, spend relative to the target, conversion lag, and sample size.
- Do not create a universal spend cutoff. Use the advertiser's economics and evidence.
- Do not blacklist a word across the account when only a specific query is proven wrong.
- Search-term reports may omit low-activity queries. State that the review covers reported terms, not every search.
- Keep facts and classifications separate. A recommendation is not an account change.

## Good output looks like

A ranked, evidence-backed list of queries to keep, review, or send for negative-keyword drafting, with the report's coverage limits stated plainly.
