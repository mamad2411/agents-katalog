---
name: metrics-measurement
description: "Design and maintain a metrics framework that tells you whether your product is healthy. Covers metric selection, hierarchy, and the difference between tracking and understanding. Use when metrics feel arbitrary, the team tracks too many things, or nobody agrees on what success looks like."
---

# Metrics & Measurement

Track the numbers that tell you whether the product is actually working.

## How to use

- `/metrics-measurement` Apply metrics measurement constraints to this conversation.
- `/metrics-measurement <product>` Design a metrics framework for the described product.

## Constraints

### Metric Hierarchy
Structure metrics in layers:
- North star: the one metric that captures your product's core value delivery
- Health metrics (3-5): the vital signs of product health — retention, activation, engagement, revenue
- Feature metrics: per-feature adoption, usage, and satisfaction
- MUST have a clear north star. If you track 20 metrics equally, you track none.
- Each metric SHOULD connect to the one above it in the hierarchy

### Metric Selection
- MUST choose metrics that are actionable — the team can influence them through their work
- MUST choose metrics that are understandable — everyone on the team can explain what they mean
- SHOULD prefer leading indicators over lagging ones (activation rate predicts revenue better than revenue itself)
- NEVER pick a metric just because it's easy to measure. Measure what matters, not what's convenient.
- MUST include at least one counter-metric to prevent gaming (e.g., if optimizing signup rate, also track 7-day retention)

### Instrumentation
- MUST define how each metric is calculated before tracking it. Ambiguous definitions create bad decisions.
- SHOULD document: data source, calculation method, known limitations, update frequency
- MUST ensure data accuracy. Bad data leads to confidently wrong decisions.
- SHOULD automate dashboards. Metrics that require manual calculation don't get checked.
- NEVER ship a feature without instrumenting the metrics that tell you if it worked

### Review Cadence
- North star: review weekly with leadership
- Health metrics: review weekly with the product team
- Feature metrics: review post-launch and monthly thereafter
- MUST set alerts for significant changes — don't wait for the weekly review to discover a cliff
- SHOULD do monthly deep dives on metric trends, not just snapshot checks

### Anti-Patterns
- Vanity Metrics: total users, downloads, page views — numbers that go up but don't correlate with value
- The Dashboard Nobody Checks: building dashboards and never looking at them
- Too Many Metrics: tracking 50 things and losing sight of what matters
- Metric Fixation: optimizing a number while ignoring the experience behind it
- The Misleading Aggregate: one number hiding completely different segment behaviors
