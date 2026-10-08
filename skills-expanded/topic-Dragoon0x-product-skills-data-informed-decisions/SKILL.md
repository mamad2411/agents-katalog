---
name: data-informed-decisions
description: "Use data to inform product decisions without becoming a slave to metrics. Covers when data helps, when it misleads, and how to combine quantitative and qualitative signals. Use when metrics tell confusing stories, when the team over-indexes on data, or when decisions lack any data backing."
---

# Data-Informed Decisions

Use data to make better decisions, not to avoid making them.

## How to use

- `/data-informed-decisions` Apply data-informed decision constraints to this conversation.
- `/data-informed-decisions <situation>` Evaluate data for the described product decision.

## Constraints

### Data Role
- Data should INFORM decisions, not MAKE them. The PM still owns the judgment call.
- MUST combine quantitative data (what users do) with qualitative data (why they do it)
- SHOULD use data to narrow options, then use judgment for the final call
- NEVER let a dashboard substitute for product thinking
- MUST know what question the data answers before looking at the data

### When Data Helps
- Measuring what happened after a change (A/B tests, before/after comparisons)
- Identifying patterns in behavior (usage frequency, feature adoption, funnel conversion)
- Sizing opportunities (how many users are affected, how often)
- Validating or invalidating hypotheses with actual behavior
- SHOULD start with a hypothesis, then check data — not the other way around

### When Data Misleads
- Small sample sizes: MUST know when the data isn't statistically significant
- Survivor bias: the users you can measure are the ones who stayed. The ones who left are invisible.
- Correlation ≠ causation: users who use Feature X retain better, but Feature X might not cause retention
- Metric gaming: optimizing a metric while the underlying experience gets worse
- MUST check if the metric captures what you think it captures. Proxy metrics can be dangerous.

### Balancing Qual and Quant
- Quantitative tells you what is happening and how much
- Qualitative tells you why it's happening and what it means
- MUST use both. Data without context leads to wrong conclusions.
- SHOULD lead with qualitative when exploring new territory, quantitative when optimizing known territory
- NEVER dismiss user testimony because it doesn't match the numbers — investigate the gap

### Data Humility
- MUST acknowledge when the data is inconclusive
- SHOULD distinguish between "the data shows X" and "we believe X based on limited data"
- MUST be honest about data quality, gaps, and instrumentation issues
- NEVER cherry-pick data to support a predetermined conclusion
- SHOULD present conflicting data points rather than hiding them

### Anti-Patterns
- Data Worship: refusing to make decisions without perfect data
- The Vanity Dashboard: tracking metrics that look good but don't correlate with business health
- Post-Hoc Rationalization: making a gut decision then finding data to justify it
- Metric Tunnel Vision: optimizing one number while everything else degrades
- Ignoring Data: making decisions purely on intuition when relevant data exists
