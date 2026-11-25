---
name: value-metrics
description: "Measure what matters, ignore what doesn't. Defines core metrics by product type, dashboards that surface real signals, and analytics events that tell the full story. Use when setting up analytics, building dashboards, or defining KPIs."
---

# Value Metrics

Measure what matters, ignore what doesn't.

## How to use

- `/value-metrics` Apply metrics constraints to this conversation.
- `/value-metrics <product-type>` Recommend metrics for the described product.

## Constraints

### North Star Metric
- MUST identify ONE metric that best represents the value users get
- This metric should go up when users are getting value and down when they're not
- Examples: messages sent (Slack), nights booked (Airbnb), deployments completed (Vercel)
- NEVER use revenue as the north star. Revenue is an output, not a driver.
- NEVER use DAU/MAU without defining what counts as a meaningful visit

### Metric Hierarchy
1. North Star: the one number everyone aligns on
2. Input metrics: 3-5 metrics that drive the north star
3. Health metrics: things that shouldn't drop (performance, error rate, support volume)
4. Guardrail metrics: things you watch to make sure growth isn't harming quality

### Analytics Events
- MUST track the full activation funnel (signup > onboarding step > core action > retained)
- MUST track where users drop off, not just where they convert
- SHOULD track time-to-value (how long from signup to first meaningful outcome)
- NEVER track more than you'll actually look at. Unused data is not an asset.

### Dashboard Rules
- MUST be scannable in under 10 seconds
- SHOULD show trends over time, not just current numbers
- MUST include comparison period (vs. last week, last month)
- NEVER show metrics without context (is 1,000 signups good or bad?)
- SHOULD alert on anomalies, not just thresholds

### Anti-Patterns
- Measuring what's easy to measure instead of what matters
- Vanity metrics (total signups, page views, social followers)
- Building dashboards nobody checks
- Changing metrics to make bad performance look good
- Measuring activity instead of value (logins are not engagement)
