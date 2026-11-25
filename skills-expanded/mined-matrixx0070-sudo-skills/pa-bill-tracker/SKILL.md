---
name: pa-bill-tracker
version: 1.0.0
description: Track recurring bills and subscriptions, flag upcoming renewals, price hikes, and cancel candidates.
author: matrixx0070
tags: [bills, subscriptions, finance, renewals, personal-assistant]
capabilities: []
---

## When to use

Use this when the owner wants visibility and control over recurring charges — subscriptions, utilities, memberships, insurance. Good for a "where is my money leaking" audit, catching a silent price increase, or spotting free-trials about to convert.

**Not for:** full budgeting/net-worth planning, investment advice, or paying/cancelling anything on your own. You track and recommend; the owner authorizes every payment and cancellation.

## Method

1. Build the ledger: for each recurring item capture name, amount, cadence (monthly/annual), next charge date, and category.
2. Normalize to a monthly-equivalent cost so annual and monthly items compare fairly.
3. Decision point — did any amount change since last known? Flag **PRICE HIKE** with old vs new and the percent jump.
4. Flag **RENEWAL SOON** for anything charging within the next 7-14 days, especially annual and trial-conversion items.
5. Score each for value: is the owner actually using it? Mark low-use items as **CANCEL CANDIDATE** with the annual savings.
6. Decision point — is a charge unrecognized? Flag as **REVIEW** (possible fraud/duplicate) and tell the owner to verify with the provider.
7. Present totals and flags. Confirm before cancelling any subscription or contacting a provider — both are hard stops.

## Example

Input: Netflix $15.49/mo, gym $40/mo (unused 3 mo), cloud storage $99/yr renewing in 5 days, streaming trial converting in 2 days.
Output: Monthly total $63. PRICE HIKE: Netflix $15.49 (was $13.99, +11%). RENEWAL SOON: cloud storage in 5d, trial in 2d. CANCEL CANDIDATE: gym — unused, saves $480/yr. Next: want me to prep cancellation steps for gym?

## Pitfalls

- Mixing cadences without normalizing — a $120/yr item looks cheaper than a $12/mo one until you convert.
- Missing trial-to-paid conversions; those are the costliest surprises. Flag them earliest.
- Treating a price change as noise. Even small hikes compound; always surface them.
- Cancelling or paying on your own. Confirm every money action and provider contact first.

## Output format

```
BILL TRACKER — [owner] — [as of date]

MONTHLY TOTAL: $[x]  (annualized: $[x])

RENEWAL SOON (<=14d)
- [name] — $[amt] — charges [date]
PRICE HIKES
- [name] — $[old] -> $[new] (+[%])
CANCEL CANDIDATES
- [name] — $[amt] — [reason] — saves $[annual]/yr
REVIEW (unrecognized)
- [name] — $[amt] — verify with provider

Next: reply with items to cancel; I prep steps, you authorize the action.
```
