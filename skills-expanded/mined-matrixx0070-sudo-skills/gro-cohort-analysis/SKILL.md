---
name: gro-cohort-analysis
version: 1.0.0
description: Build and read a cohort table to see how grouped users behave over time and whether the product is improving.
author: matrixx0070
tags: [growth, cohorts, analytics, behavior, trends]
capabilities: []
---

## When to use

Use this when an aggregate metric hides what's really happening — a flat top-line can mask new cohorts getting worse while old ones prop it up. Reach for it to compare cohorts over time, isolate the effect of a launch, or answer "is the product getting better for users we acquire now?"

**Not for:** the specific retention-lever workflow (use gro-retention-analysis, which is a cohort analysis specialized to retention), single-step drop-off (gro-funnel-analysis), or proving causation of one change (gro-ab-test-design). This is the general mechanic; the others are lenses on it.

## Method

1. Choose the cohort key — usually signup period (acquisition cohort), but sometimes a behavioral cohort (users who did action X) or a source cohort. Decision point: acquisition cohorts answer "are we improving over time?"; behavioral cohorts answer "does behavior X matter?"
2. Choose the metric per cell: retention %, revenue, orders, or any per-user value. Pick the time grain (day/week/month) matching product frequency.
3. Build the matrix: rows = cohorts (by start period), columns = age (periods since start), cells = the metric. Every cell in a column is the *same age*, which is what makes cohorts comparable.
4. Read it three ways: down a *column* (are newer cohorts better or worse at the same age? — the product-health trend), across a *row* (how a single cohort evolves — decay or growth), and the *diagonal* (calendar effects like a launch or seasonality hitting all cohorts at once).
5. Decision point: if newer cohorts underperform older ones at equal age, something regressed (or you're acquiring worse users) — investigate acquisition source mix and recent product changes.
6. Normalize by cohort size (use rates, not raw counts) so a big cohort doesn't dominate, and isolate the driver before recommending action.

## Example

Monthly signup cohorts, cell = % still active. Reading down the month-3 column: Jan cohort 30%, Feb 28%, Mar 21%. Newer cohorts decay faster at the same age. The diagonal shows no shared calendar dip, so it's not seasonality. Cause: a Feb paid-ads push brought lower-intent users. Action: shift spend back to higher-retaining channels; confirm with the next cohort.

## Pitfalls

- Comparing cohorts at *different ages* (a 6-month-old vs a 1-month-old cohort) — always compare down a column.
- Using raw counts so the largest cohort dominates; use per-user rates.
- Reading only the diagonal (calendar) and missing the column trend (product health), or vice versa.
- Too-small cohorts producing noisy cells you over-interpret; bucket up until each cell is stable.

## Output format

```
Cohort key: <signup month/behavior/source> | Metric: <retention/revenue> | Grain: <week/month>
Cohort \ Age   0      1      2      3      ...
<Jan>         100%   45%    35%    30%
<Feb>         100%   43%    32%    28%
<Mar>         100%   40%    28%    21%
Column read (health):  <newer better/worse at same age>
Row read (lifecycle):  <decay/growth shape>
Diagonal (calendar):   <launch/seasonality effect or none>
Finding:               <what changed + likely driver>
Action:                <recommendation> | Confirm: next cohort / gro-ab-test-design
```
