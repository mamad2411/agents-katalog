---
name: metric-interpretation
description: "Understand what product metrics actually mean in context. A 3% conversion rate can be amazing or terrible depending on product type, stage, and market. Provides contextual benchmarks and interpretation frameworks. Use when evaluating whether a metric is good or bad, reporting to stakeholders, or when a metric changes unexpectedly."
---

# Metric Interpretation

Understand what your numbers actually mean. Context is everything.

## How to use

- `/metric-interpretation` Apply metric interpretation constraints to this conversation.
- `/metric-interpretation <metric and value>` Interpret a specific metric in context.

## Constraints

### Three Context Layers
Every metric MUST have at least three layers before it's meaningful:
1. Product context: B2B vs. B2C, free vs. paid, daily-use vs. quarterly, stage (pre-PMF, growth, mature)
2. Funnel context: where in the journey (top = high volume low conversion, bottom = low volume high conversion)
3. Temporal context: trend direction, seasonality, what changed recently, rate of change not just absolute

### Interpretation Checklist
Before interpreting any metric:
- Is this the right metric? Are we measuring what matters, or what's easy?
- What's the denominator? 50% conversion on 10 users is noise, not signal.
- What's the trend? One data point is an anecdote.
- What changed? If it moved, something caused it. Find the cause.
- What's not measured? Every metric has blind spots.
- Who are we comparing against? Compare to your own history first, then your specific market.

### Benchmark Ranges (Context-Dependent)
- Visitor → signup: 1-3% broad traffic, 3-8% targeted, 8-15% high-intent
- Trial to paid: 2-5% opt-in upgrade, 10-25% time-limited, 25-40% credit card required
- Monthly churn (B2B SaaS): under 2% excellent, 2-5% acceptable SMB, 5%+ needs attention
- NRR: under 90% contracting, 100-120% healthy, 120%+ strong expansion
- DAU/MAU: under 10% infrequent use (can be fine), 20-30% weekly use, 50%+ daily habit
- MUST adjust benchmarks for product type. A tax tool with 5% DAU/MAU isn't broken.

### Presentation Rules
- Lead with the insight, not the number
- MUST show trend, not just current state
- MUST connect to business impact ("this retention improvement = $X in preserved revenue")
- SHOULD include confidence level: strong signal or noise?
- NEVER present a metric without context for what "good" looks like

### Anti-Patterns
- Survivorship bias: "retained users love us" — the unhappy ones left
- Averaging across segments that behave completely differently
- Ignoring base rates: 200% improvement from 0.1% to 0.3% isn't impressive
- Confusing correlation with causation: power users use everything, not just the feature you're measuring
- Snapshot without trend: 40% retention is great if it was 20% last quarter, terrible if it was 60%
- Vanity metrics: total registered users, downloads, page views tell you nothing about product health
