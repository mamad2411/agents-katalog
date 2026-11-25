---
name: mkt-performance-report
version: 1.0.0
description: Turn marketing metrics into a clear performance report with trends, interpreted wins and misses, and prioritized optimizations.
author: matrixx0070
tags: [marketing, analytics, reporting, metrics, optimization]
capabilities: []
---

## When to use

Use this when you have campaign or channel data for a period and need to explain what happened, why it matters, and what to do next — not just dump numbers.

**Not for:** planning a campaign before it runs (use mkt-campaign-plan) or forecasting with no historical data. If key metrics are missing, note the gap; do not invent figures.

## Method

1. Establish scope. Confirm the reporting period, the comparison baseline (prior period, target, or year-over-year), and the objectives the work served.
2. Assemble metrics that map to those objectives: reach, engagement, traffic, leads, conversion rate, cost per result, revenue/ROI. Decision point: if a metric is missing, flag it explicitly rather than estimating.
3. Compute trends. For each metric show current vs. baseline as absolute and percent change, and mark direction.
4. Interpret, do not just report. For each notable move, give the most likely driver and your confidence level.
5. Separate wins from misses, each tied back to an objective.
6. Recommend optimizations. Convert each miss and each unexploited win into a specific next action, ranked by expected impact vs. effort.
7. Flag anything that looks like a data-quality issue.

## Example

Period: Q2 vs. Q1. Leads +38% (420 → 580) driven by the LinkedIn webinar series (high confidence — traffic source data confirms). But CAC +22% because paid search spend rose with flat conversion (medium confidence). Win: webinars — double down, add a Q3 cadence. Miss: paid search — pause the two worst ad groups, reallocate to webinar promotion. Data caveat: attribution window changed mid-quarter.

## Pitfalls

- Reporting numbers with no interpretation — the "so what" is the whole job.
- Claiming causation from correlation; state confidence and the likely driver.
- Cherry-picking wins and hiding misses; both tie to objectives.
- Recommendations that are not actionable ("improve conversions") instead of specific next steps.

## Output format

```
Executive summary: <3-4 sentences on the period's story>

Scorecard:
| Goal | Target | Actual | Status |

Metrics:
| Metric | This period | Baseline | Change | Trend |

Wins: <what worked + why>
Misses: <what underperformed + likely cause>
Optimizations: <prioritized actions with impact/effort>
Data caveats: <...>
```
