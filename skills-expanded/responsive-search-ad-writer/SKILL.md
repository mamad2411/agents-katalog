---
name: responsive-search-ad-writer
description: 'Write a complete Google responsive search ad from real query intent and supported page claims, then validate every asset and character limit. Use when an ad group needs credible copy, sitelinks, and callouts.'
---

# Responsive Search Ad Writer

## Doctrine

A responsive search ad is a set of assets Google can combine in many orders. Every headline and description must work alone and beside the others. Start from the query and the page, use only claims the business can prove, and validate the copy before calling it ready.

## When to use

- When a focused Search ad group needs a new or replacement responsive search ad.
- Use a connected Google Ads MCP for read-only context, or paste the keywords, search terms, current ads, page copy, final URL, brand voice, and policy constraints.
- Supply real sitelink URLs and supported facts. Missing proof stays missing; it is never filled with a plausible claim.

## Run it

```
Draft a Google responsive search ad. Use live account data for read-only context if connected; otherwise use what I paste. Do not create or edit an ad.

1. Confirm the ad-group job, target queries and keywords, final URL, page facts, brand voice, legal requirements, current assets, and approved sitelink URLs.
2. Make a claim ledger before writing: supported facts, unsupported claims to avoid, and missing proof.
3. Output in this order:
   - ad-group and query map;
   - negative-keyword questions, not automatic negatives;
   - 4 or more sitelinks with supplied URLs, or clearly marked URL gaps;
   - 4 or more callouts;
   - final URL and 2 display paths;
   - 15 distinct headlines;
   - 4 distinct descriptions;
   - pinning plan, default unpinned unless a legal or message requirement must always show;
   - validation report and claim sources.
4. Enforce current RSA limits: every headline at most 30 characters, every description at most 90, and every path at most 15. Print the character count beside each asset.
5. Make assets useful in different combinations. Avoid repeating the same claim with tiny wording changes.
6. Map every factual claim to supplied page evidence. If a sitelink URL, price, trial condition, certification claim, timing claim, or feature is not supplied, do not invent it.
7. Check that the first 3 headlines can appear together, that any headline can pair with any description, and that no combination overclaims.

Return copy and a pass/fail validation report. If required inputs are missing, label the draft "not ready to publish" and list the gaps. End with "No ads were created or changed."
```

## Guardrails

- Google allows up to 15 headlines and 4 descriptions. This skill writes the full set for range, but does not pretend every asset will serve.
- Never add "no credit card", "guaranteed", setup-time, savings, security, certification, or performance claims without supplied proof.
- Do not invent sitelink destinations. A useful label with no verified URL is a gap, not a ready asset.
- Pinning reduces combination flexibility. Use it only when the user supplies a real requirement.
- Copy is a draft. Creating, editing, or enabling an ad requires a separate, explicit approval step.

## Good output looks like

One intent-matched RSA with validated counts, distinct assets, a visible claim ledger, honest URL gaps, and no unsupported promise hiding in the copy.
