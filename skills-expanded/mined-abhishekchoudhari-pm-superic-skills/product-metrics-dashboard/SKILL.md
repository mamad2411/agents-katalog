---
name: product-metrics-dashboard
description: "Design a product metrics dashboard — select the right metrics, define the hierarchy from North Star to diagnostics, set alert thresholds, specify the data pipeline, and identify metric ownership. Use when building a new product dashboard, auditing an existing one, selecting the North Star metric, structuring metrics for a leadership review, or designing alert rules for product health."
---

# Product Metrics Dashboard Design

Design a metrics dashboard that drives decisions, not just reports numbers. The goal is a system where every metric has an owner, a threshold, and a clear connection to the North Star.

---

## Context

You are designing a product metrics dashboard for **$ARGUMENTS**.

If the user provides existing metrics or business context, incorporate them. Otherwise, ask for: product type, user base size, and primary business model.

---

## Part 1: Metrics Hierarchy

Every well-designed dashboard has three layers. Each layer explains the one above it.

### Layer 1: North Star Metric (1 metric)

The single metric that best represents the value your product delivers to users. It must:
- Reflect genuine user value (not proxy metrics like downloads or registrations)
- Correlate with long-term business health (revenue, retention, referral)
- Be actionable — the team can influence it directly

**North Star examples by product type:**

| Product type | North Star metric | Why |
|---|---|---|
| Social app | Weekly active users (WAU) or posts per week | Reflects network activity |
| E-commerce | Gross merchandise value (GMV) or orders per month | Revenue-correlated |
| SaaS | Seats in use per account or features activated | Reflects stickiness |
| Subscription service | Subscriber count or monthly hours consumed | Reflects engagement |
| Marketplace | Successful transactions per month | Both sides of market captured |
| Financial product | Monthly active transactors | Behavioral, not just registered |

**Anti-pattern North Stars to avoid:**
- Total registered users (includes inactive users, inflates with marketing)
- Total downloads (no engagement signal)
- Revenue alone at early stage (can grow while retention collapses)

### Layer 2: L2 Metrics (3-5 metrics)

L2 metrics explain why the North Star is moving up or down. Each L2 metric covers a pillar of the product.

**Standard L2 framework for a B2C product:**

| L2 Metric | What it measures | Connection to North Star |
|---|---|---|
| Acquisition rate | New activated users per week | North Star grows only if acquisition feeds it |
| D30 retention | % of users active 30 days after activation | North Star stays high if retained users compound |
| DAU/MAU ratio | Engagement frequency of active users | North Star reflects real engagement, not dormant accounts |
| ARPU | Revenue per monthly active user | North Star correlates with revenue |
| NPS or CSAT | User satisfaction leading indicator | North Star is sustainable only if users are satisfied |

### Layer 3: L3 Diagnostics (10-15 metrics)

L3 metrics diagnose which specific part of the product is driving an L2 change.

**Example L3 metrics under "D30 retention" L2:**
- D1 retention by acquisition channel
- Onboarding completion rate
- Core feature adoption rate (% of users who used the primary feature in first 7 days)
- Day 7 re-engagement rate after dormancy
- Notification opt-in rate (leading indicator of re-engagement surface availability)

---

## Part 2: Dashboard Types

Build the right dashboard for the right audience and cadence.

### Real-time ops dashboard

**Audience:** on-call engineering, operations team, fraud team
**Cadence:** live / 5-minute refresh
**Metrics:**
- Payment success rate (alert if <98%)
- API error rate (alert if >0.5%)
- App crash rate (alert if >0.1% of sessions)
- Fraud transaction rate (alert if >0.5% of transactions)
- P99 API latency (alert if >2 seconds)

**Tool:** Grafana, Datadog, or PagerDuty

### Weekly product dashboard

**Audience:** product team, growth team, weekly standup
**Cadence:** weekly, refreshed Monday morning
**Metrics:** North Star, DAU/MAU, D7 and D30 retention (latest cohort), weekly new activations, ARPU, funnel conversion by step
**Tool:** Amplitude, Mixpanel, or Metabase

### Monthly leadership dashboard

**Audience:** CEO, VP Product, VP Engineering, board
**Cadence:** monthly, shared first week of the month
**Metrics:** MAU, MoM MAU growth %, D30 retention (3-month trend), ARPU, NRR or revenue cohort LTV, NPS
**Tool:** Looker, Tableau, or a Google Sheet with embedded charts

---

## Part 3: Common B2C Product Dashboard — Benchmarks

A standard B2C product dashboard should include these metrics and their healthy ranges.

| Metric | Poor | Median | Strong | Alert threshold |
|---|---|---|---|---|
| MAU growth (MoM %) | <0% | 3-8% | >10% | Alert if negative for 2 consecutive months |
| DAU/MAU ratio | <10% | 15-25% | >30% | Alert if drops >20% WoW |
| D1 retention | <15% | 25-35% | >40% | Alert if latest cohort drops >5pp vs 4-week average |
| D30 retention | <5% | 10-15% | >20% | Alert if latest cohort drops >3pp vs 4-week average |
| Activation rate (signup to first value) | <20% | 35-50% | >60% | Alert if drops >5pp WoW |
| NPS | <10 | 30-50 | >60 | Alert if drops >10 points MoM |
| ARPU | Product-specific | Product-specific | Product-specific | Alert if drops >10% MoM |

---

## Part 4: Alert Threshold Design

Alerts should fire for actionable problems, not every routine fluctuation. Three threshold types:

### Absolute threshold
Fires when a metric drops below a fixed floor.
- Example: "Alert if payment success rate drops below 97%"
- Best for: SLAs, safety metrics, metrics with known minimum acceptable values

### Relative threshold
Fires when a metric drops more than X% compared to a prior period.
- Example: "Alert if DAU drops >15% vs same day last week"
- Best for: engagement metrics, conversion metrics with natural week-over-week variation

### Anomaly detection threshold
Fires when a metric deviates more than 2 standard deviations from its recent trend.
- Example: "Alert if today's DAU is more than 2 standard deviations below the 30-day rolling average"
- Best for: mature products with stable baselines; less useful for early-stage products with high natural variance

### Alert fatigue prevention

| Rule | Implementation |
|---|---|
| Every alert must have an owner | Assign each alert to a specific person, not a team |
| Every alert must have a runbook | Document what to check and what to do when it fires |
| Review alert thresholds quarterly | Thresholds become stale as product scales |
| Separate P0 (wake someone up) from P1 (check next business day) | Not all alerts are equally urgent |

---

## Part 5: Vanity Metrics to Avoid

Replace these with the metric in the "Use instead" column.

| Vanity metric | Problem | Use instead |
|---|---|---|
| Total registered users | Includes dormant and fake accounts | MAU (active in last 30 days) |
| Total downloads | No engagement signal | Activated users (completed onboarding) |
| Total messages sent | Bots and noise inflate the number | Unique senders or threads with a reply |
| Page views | Session and bounce patterns matter more | Session depth, scroll depth, or task completion rate |
| Total revenue | Hides churn and contraction | Net Revenue Retention (NRR) or ARPU |
| App store rating | Recency and sample bias issues | NPS from active users |
| Social media followers | Reach without engagement is worthless | Engagement rate (comments + shares / impressions) |

---

## Part 6: Tool Recommendations

| Use case | Primary tool | Backup option |
|---|---|---|
| User behavior and funnel analytics | Amplitude or Mixpanel | PostHog (open source) |
| SQL-based ad hoc analysis | BigQuery + Metabase | Redshift + Mode |
| Business intelligence / leadership dashboards | Looker or Tableau | Google Looker Studio (free) |
| Real-time ops and infrastructure | Grafana + Prometheus | Datadog |
| A/B testing and feature flags | LaunchDarkly or Statsig | Optimizely |
| Customer satisfaction | Delighted (NPS) or Qualtrics | Typeform |

---

## Part 7: Instrumentation-to-Dashboard Pipeline

Understanding the full pipeline prevents gaps between what happened and what the dashboard shows.

```
[User action in app]
       ↓
[Event fired: event_name, user_id, properties, timestamp]
       ↓
[Event ingested: Segment, Amplitude SDK, or custom pipeline]
       ↓
[Data warehouse: BigQuery / Snowflake / Redshift]
       ↓
[Transformation: dbt models or SQL views that clean and aggregate raw events]
       ↓
[BI layer: Looker / Metabase / Mode queries against transformed tables]
       ↓
[Dashboard: charts, alerts, and weekly digest emails]
```

**Common pipeline failures:**
- Events fire but are missing required properties (user_id is null = cannot attribute to user)
- dbt model runs before all events land in the warehouse (data lag causes today's numbers to be understated until next run)
- Schema changes in raw events break downstream dbt models without alerting anyone
- BI tool caches queries aggressively and shows stale data

**Recommendation:** build a data quality check at the warehouse layer — a daily query that counts events by type and alerts if counts drop >30% vs prior day.

---

## Part 8: Metric Ownership Model

Unowned metrics don't move. Assign an owner to every metric before publishing the dashboard.

| Metric level | Owner | Accountability |
|---|---|---|
| North Star | VP Product or Product Lead | Presents to leadership monthly; explains YoY and MoM movement |
| L2 metrics | Product Manager for each area | Reviews weekly; owns the roadmap to move the metric |
| L3 diagnostics | PM or analyst assigned to the feature | Monitors daily; escalates anomalies |
| Ops metrics (latency, error rate) | Engineering on-call | Responds to alerts within SLA |
| Revenue metrics | Finance or growth PM | Owns ARPU, NRR, LTV reporting |

---

## Part 9: Dashboard Design Output Format

When designing a dashboard for a user, produce this specification.

```
## Product Metrics Dashboard: [Product Name]

### North Star Metric
[Metric name] — [definition] — [current value or target]

### L2 Metrics
| Metric | Definition | Owner | Current value | Target | Alert threshold |
|---|---|---|---|---|---|
| | | | | | |

### L3 Diagnostics
[List by L2 metric — 3 diagnostic metrics per L2]

### Dashboard views to build
1. Real-time ops: [metrics list, tool, refresh rate]
2. Weekly product: [metrics list, tool, audience]
3. Monthly leadership: [metrics list, tool, audience]

### Alert rules
| Metric | Threshold type | Threshold value | Owner | Runbook location |
|---|---|---|---|---|
| | | | | |

### Data pipeline notes
[Any gaps in current instrumentation that need to be filled before this dashboard can go live]

### Vanity metrics to retire
[List current metrics in reports that should be replaced]
```

---

### Further Reading

- [Are You Tracking the Right Metrics?](https://www.productcompass.pm/p/are-you-tracking-the-right-metrics)
- [The Product Analytics Playbook](https://www.productcompass.pm/p/the-product-analytics-playbook-aarrr)
