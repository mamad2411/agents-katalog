---
name: product-analytics
description: Define product metrics, event instrumentation, dashboards, funnels, retention cohorts, sprint reviews, and cross-functional product reviews. Use when a user asks for a North Star metric, KPI tree, analytics plan, dashboard specification, funnel or cohort analysis, sprint review, QBR, or product health assessment.
---

# Product Analytics

Metrics support decisions; they do not replace qualitative understanding. Define each metric precisely and protect user data throughout collection and analysis.

## Route

- **Metric framework:** outcome, North Star where appropriate, input metrics, guardrails, and counter-metrics linked by a causal hypothesis.
- **Instrumentation:** event name, trigger, properties, identity, source, schema owner, validation, privacy classification, and retention.
- **Dashboard:** audience, decision, metric definitions, filters, freshness, alerts, annotations, and drill-downs.
- **Funnel or cohort:** eligibility, denominator, time window, conversion event, segmentation, censoring, and comparison method.
- **Sprint or product review:** goals, shipped work, outcomes, quality, learning, risks, decisions, and follow-ups.

Read [product-analytics-reference.md](references/product-analytics-reference.md) only for detailed templates and worked examples.

## Data rules

- Use an authoritative source and record query, owner, time zone, window, exclusions, and freshness.
- Minimize personal data; avoid sensitive segmentation without lawful purpose and appropriate review.
- Check missing events, duplicate events, bots, internal traffic, identity stitching, late arrivals, and definition drift.
- Show absolute values and denominators beside percentages.
- Distinguish correlation from causation and statistical uncertainty from business importance.
- Never fabricate a baseline, cohort, customer quote, or result.

## Workflow

1. Define the decision and user outcome.
2. Create a metric specification before designing visuals.
3. Validate instrumentation and data quality.
4. Analyze with relevant segments and counter-metrics.
5. Explain findings, alternative explanations, and limitations.
6. Record the decision, owner, follow-up, and measurement date.

Return definitions, evidence, analysis, visualization specification, data-quality findings, and next decisions rather than a decorative dashboard alone.
