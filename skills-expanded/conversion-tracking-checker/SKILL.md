---
name: conversion-tracking-checker
description: 'Decide whether Google Ads conversion data is trustworthy enough for optimization by checking goals, action settings, duplicates, and campaign use. Use before changing bids, budgets, or performance targets.'
---

# Conversion Tracking Checker

## Doctrine

Bidding can only optimize toward the goals it is given. An active action can still be the wrong business outcome, a page view can drown out a demo, and two actions can count the same event. Google Ads evidence can reveal those risks, but it cannot prove what happened inside GA4, GTM, a website, or a CRM without separate data.

## When to use

- Before a bid-strategy, target, budget, or scaling recommendation.
- When Google Ads conversions disagree with sales, CRM, or another source.
- Use a connected Google Ads MCP, or paste conversion-action, campaign-goal, recent performance, and downstream outcome exports.

## Run it

```
Run a READ-ONLY Google Ads conversion check. Use live account data if connected; otherwise use what I paste. Change nothing.

1. Build an action inventory with: name, category, origin, status, primary or secondary, account-default inclusion, campaign goal mapping, counting rule, value rule, recent conversions, and available diagnostics.
2. Map which campaigns are bidding on which actions. Do not assume account-default goals apply everywhere without checking.
3. Flag likely bidding-quality problems, including shallow actions marked primary, inactive goals, missing values for value-based bidding, and actions that may count the same business event.
4. Treat possible duplication as a risk, not a fact. Compare action definitions, timestamps, identifiers, attribution windows, and the source of truth before deciding two actions duplicate each other.
5. Reconcile Google Ads totals with supplied CRM or sales outcomes only when date ranges, timezone, attribution, and conversion delay are aligned.
6. Give a trust grade: ready, caution, or not ready. Explain what decisions are safe now and which must wait.
7. List exact verification steps for the website tag, imported action, offline conversion, or CRM, but state when those systems are outside the available evidence.

Do not change goals, primary status, counting, values, tags, attribution, bids, or budgets. End with "No changes were made."
```

## Guardrails

- "Active" in Google Ads does not prove the website tag, GA4 event, or CRM pipeline is correct end to end.
- An imported Google Analytics action is evidence about the Google Ads action only. Do not claim access to the underlying GA4 property unless it was supplied separately.
- Similar totals do not prove actions duplicate each other, and different totals do not prove one is broken.
- A page view or other shallow action marked primary is a serious bidding risk, but changing it still requires verification and approval.
- Hold bid, budget, and scaling changes when the primary optimization signal is contaminated or unresolved.

## Good output looks like

A clear conversion-action inventory, a campaign goal map, an honest trust grade, and the shortest path to knowing which business outcome Google should optimize toward.
