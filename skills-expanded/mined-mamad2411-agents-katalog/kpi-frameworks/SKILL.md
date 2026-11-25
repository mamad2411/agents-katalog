---
name: kpi-frameworks
description: KPI hierarchy definition, north star metrics, OKR trees, and leading vs. lagging indicator frameworks. Use when defining success metrics for a product, building a measurement plan, or evaluating whether current metrics actually reflect business health.
---

# KPI Frameworks

Metrics that don't connect to business outcomes are decoration. This skill covers how to build a coherent metric hierarchy — from north star down to feature-level indicators — so that every measurement tells you something actionable.

## When to Use This Skill

- Defining success metrics for a new product or feature
- Auditing whether existing metrics reflect what actually matters
- Building an OKR tree for a planning cycle
- Distinguishing leading from lagging indicators for a feature
- Designing the measurement plan for a product evaluation

## Core Concepts

### 1. North Star Metric

The north star metric is the single number that best captures the core value your product delivers to users. It should:
- Reflect genuine user value, not proxy activity
- Correlate with long-term business health
- Be something the product team can influence directly

| Product Type | Example North Star |
|-------------|-------------------|
| Marketplace | GMV (Gross Merchandise Value) |
| SaaS | Weekly Active Users (WAUs) or NRR |
| Content platform | Time in product (engaged minutes) |
| Communication tool | Messages sent per active user |
| Payments product | Transaction volume |

**North Star ≠ Revenue.** Revenue is a lagging outcome; the north star explains why revenue happens.

### 2. Leading vs. Lagging Indicators

| Type | Definition | Example | Lag Time |
|------|-----------|---------|----------|
| **Leading** | Predicts future outcomes; actionable early | Onboarding completion rate | Days to weeks |
| **Lagging** | Confirms outcomes after they've occurred | Monthly revenue, annual churn | Weeks to months |

For product evaluation, leading indicators let you course-correct before lagging indicators confirm a problem. Track both but act on leading indicators.

### 3. Guardrail Metrics

Guardrail metrics are things that must NOT get worse when you optimize for your primary metric. Every feature evaluation needs them.

```
Optimizing for: Checkout conversion rate
Guardrails:
  - Cart abandonment rate must not increase > 2pp
  - Support ticket volume must not increase > 10%
  - Average order value must not decrease > 5%
```

## Metric Hierarchy

```
North Star Metric
├── Revenue Metrics (lagging)
│   ├── MRR / ARR
│   ├── ARPU
│   └── LTV
├── Retention Metrics
│   ├── D7 / D30 / D90 retention
│   ├── Monthly churn rate
│   └── Net Revenue Retention (NRR)
├── Engagement Metrics (leading)
│   ├── DAU / WAU / MAU
│   ├── Session depth
│   └── Core action completion rate
└── Acquisition Metrics
    ├── New user activations
    ├── Activation rate (registered → activated)
    └── CAC by channel
```

## OKR Tree Format

OKRs (Objectives and Key Results) translate strategic intent into measurable quarterly commitments.

```markdown
## Objective: [What we're trying to achieve — qualitative]

### KR1: [Measurable outcome 1]
Current baseline: [X]
Target: [Y]
Owner: [Team / Person]

### KR2: [Measurable outcome 2]
Current baseline: [X]
Target: [Y]
Owner: [Team / Person]

### KR3: [Measurable outcome 3]
Current baseline: [X]
Target: [Y]
Owner: [Team / Person]
```

### OKR Quality Checklist

- [ ] Objective is inspiring and direction-setting, not a task
- [ ] Each KR is a measurable outcome, not a deliverable ("ship X" is not a KR)
- [ ] Each KR has a current baseline documented
- [ ] Targets are ambitious but achievable (70–80% confidence)
- [ ] KRs together would constitute evidence that the Objective was achieved
- [ ] No KR is a leading indicator that could be gamed without achieving the Objective

## Feature-Level Measurement Plan

For each feature, define:

```markdown
## Measurement Plan: [Feature Name]

**Measurement window:** [How long after launch before evaluating?]
**Minimum viable data:** [What volume of data is needed for meaningful conclusions?]

### Primary Success Metric
- Metric: [Name]
- Baseline: [Current value]
- Target: [Success threshold]
- Instrument: [How it's tracked — event name, query, dashboard]

### Leading Indicators (visible within 1-2 weeks)
| Metric | Baseline | Target | Instrument |
|--------|---------|--------|------------|
| [Metric] | [Current] | [Target] | [Tracking method] |

### Lagging Indicators (confirm success, 4-8 weeks)
| Metric | Baseline | Target | Instrument |
|--------|---------|--------|------------|
| [Metric] | [Current] | [Target] | [Tracking method] |

### Guardrail Metrics (must not degrade)
| Metric | Baseline | Threshold | Instrument |
|--------|---------|-----------|------------|
| [Metric] | [Current] | Must stay > [value] | [Tracking method] |
```

## Statistical Significance for Feature Evaluation

When evaluating whether a metric moved meaningfully:

| Sample Size | Minimum Detectable Effect | Confidence Level |
|-------------|--------------------------|-----------------|
| < 100 events | ≥ 20% relative change | Low — directional only |
| 100–500 events | ≥ 10% relative change | Moderate |
| 500–2,000 events | ≥ 5% relative change | Good |
| 2,000+ events | ≥ 2% relative change | High |

**Rule:** Don't declare success or failure until you have sufficient data. "We launched 3 days ago and conversion went up 2%" is noise, not signal.

### A/B Test Significance

For A/B tests, use a minimum:
- 95% confidence level (p < 0.05) for shipping decisions
- 80% confidence level for directional learning only
- Run tests for at least 2 full weeks to account for weekly variation

## Common Metric Mistakes

| Mistake | Effect | Fix |
|---------|--------|-----|
| Optimizing for activity metrics (page views, clicks) | Looks good; may not reflect value | Replace with outcome metrics |
| No baseline documented | Can't evaluate if the metric moved | Always record baseline before launch |
| Measuring too early | Noise looks like signal | Wait for minimum viable data volume |
| No guardrail metrics | Win on primary while breaking something else | Define guardrails before launch |
| Single metric evaluation | Optimization for one metric degrades others | Multi-metric evaluation with guardrails |

## Best Practices

1. **Define metrics before building, not after** — post-hoc metric selection finds the metric that makes the feature look good
2. **Instrument before launch** — if tracking isn't in place on day 1, early data is lost
3. **Distinguish "did it move" from "did we cause it"** — correlation vs. causation matters; control for concurrent changes
4. **Publish baselines** — metrics without baselines can be selectively interpreted
5. **Review metrics quarterly** — a metric that made sense 18 months ago may be measuring the wrong thing now
