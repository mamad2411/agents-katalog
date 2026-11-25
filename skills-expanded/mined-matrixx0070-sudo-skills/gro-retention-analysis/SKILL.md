---
name: gro-retention-analysis
version: 1.0.0
description: Analyze retention and churn cohorts to find the flattening point and the single strongest retention lever.
author: matrixx0070
tags: [growth, retention, churn, cohorts, engagement]
capabilities: []
---

## When to use

Use this when you care whether users *keep coming back* — the truest signal of product-market fit. Reach for it when growth is up but revenue stalls (leaky bucket), before scaling acquisition spend, or when churn spikes and you need the cause.

**Not for:** first-session conversion (use gro-activation-optimize), one-time funnel drop-off (gro-funnel-analysis), or generic behavior-over-time slicing (gro-cohort-analysis is the mechanic; this is the retention interpretation on top of it).

## Method

1. Pick the retention definition that matches your product's natural frequency: daily for social/utility, weekly for SaaS, monthly for infrequent tools. Decision point: wrong cadence makes healthy products look dead — match usage rhythm.
2. Define "retained" as a meaningful action, not just a login (e.g. "created a doc"), and choose N-day (came back on exactly day N) vs unbounded (any action ≥ day N). Unbounded is usually kinder and more honest.
3. Build the retention curve by signup cohort. Read three things: Day-1 (onboarding), the *slope* of early decay, and whether the curve *flattens* to a horizontal asymptote.
4. Decision point: if the curve never flattens, you have no core retained user base — fix product value before spending on acquisition. If it flattens, the asymptote height is your ceiling; work to raise it.
5. Split retained vs churned users by early behavior. Find the action, frequency, or feature that retained users did in week 1 that churned users didn't — that's your candidate lever (correlation; validate causally).
6. Prescribe one intervention to push more new users into that behavior, and test it with gro-ab-test-design.

## Example

Weekly cohorts, "retained = sent a message." Curves decay to a flat 22% by week 4 — a real core exists. Splitting week-1 behavior: users who added ≥3 teammates retain at 55%; solo users at 8%. Lever: drive team invites during onboarding. Intervention: prompt to invite 3 teammates on first login; validate via A/B on 4-week retention.

## Pitfalls

- Using login as the retention event, inflating numbers and hiding real disengagement.
- Reading a curve that hasn't flattened as "fine" — early cohorts just haven't churned *yet*.
- Confusing correlation with causation: retained users invite teammates AND are already committed. Test before believing.
- Averaging all cohorts into one line, hiding that recent cohorts retain worse (a regression you'd miss).

## Output format

```
Retention def: <event> | Cadence: <daily/weekly/monthly> | Type: <N-day/unbounded>
Cohort curve:
  Period:   0     1     2     3     4     ...
  Retained: 100%  40%   30%   25%   23%   (flattens ~<X>%)
Day-1:            <%>   | Early slope: <steep/gentle> | Asymptote: <%>
Health:           <flattens = core exists | no flatten = no PMF>
Lever (correlated): <behavior> → <retained %> vs <churned %>
Intervention:     <one change to drive that behavior>
Validation:       A/B on <horizon>-retention via gro-ab-test-design
```
