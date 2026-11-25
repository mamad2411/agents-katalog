---
name: pm-metrics-review
version: 1.0.0
description: Turn a dashboard or data export into a decision-grade metrics review — trend, decomposition, ranked insights, and owned next steps, not restated numbers.
author: matrixx0070
tags: [product, metrics, analytics, growth, insights, retention]
capabilities: []
---

# Metrics Review

## When to use
Use this when you have a dashboard, data export, or weekly number and need to know what actually changed, why it matters, and what to do, rather than reciting figures back to leadership.

**Not for:** building the instrumentation or data pipeline, running a controlled experiment analysis (that needs statistical rigor and a pre-registered hypothesis), or defining a north-star metric from scratch. If the data window or definitions are untrustworthy, fix that first.

## Method
1. Anchor on the goal. Identify the north-star metric tied to the outcome, and separate supporting metrics from guardrails.
2. Establish baseline and trend: compare vs prior period, same period last cycle, and target. Report direction, magnitude, and whether the move is outside normal noise. **Decision point:** if it is within noise, say so and stop, do not manufacture a story.
3. Decompose the movement by segment, cohort, surface, or funnel step. **Decision point:** if the top line is flat, still decompose, opposing sub-trends often cancel out.
4. Form a hypothesis per notable move, tying it to a known release, seasonality, or external event. Label as hypothesis unless you have a clean before/after.
5. Rank insights by impact x confidence; drop the interesting-but-not-actionable.
6. Recommend concrete steps: investigate, ship, or hold, each with an owner and expected effect.

## Example
Activation flat at 42% week-over-week. Decomposing by signup source: organic rose 38%→45% while paid fell 46%→39%, cancelling out. Hypothesis: last week's paid campaign drove low-intent traffic (ties to the Tuesday ad launch). Action: pause the underperforming ad set and re-check activation next week (owner: growth).

## Pitfalls
- Reporting a delta without a baseline, so nobody can tell if it is good or noise.
- Stating causation ("the redesign lifted retention") without a clean before/after or control.
- Drowning the headline in twenty secondary metrics; leadership needs the one thing that matters first.
- Ending with insights but no owned action, leaving the review as trivia.

## Output format
```
# Metrics Review: [product/area] — window [start–end]
Headline: the one thing leadership must know.

## Metric table
| Metric | Value | Δ vs prior | Δ vs target | Trend |
| --- | --- | --- | --- | --- |

## Key movements
- [movement] → likely driver [hypothesis if unproven]

## Watch list
- [metric trending toward trouble]

## Recommended actions
- [investigate/ship/hold] — owner — expected effect
Data caveats: [quality/completeness notes]
```
