---
name: saas-metrics-dashboard
description: "Sets up SaaS metrics dashboards tracking MRR, churn, LTV, CAC, expansion revenue, and cohort retention. Use when building or improving subscription business analytics."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# SaaS Metrics Dashboard

## When to Use This Skill

Use this skill when you need to:
- Define and track core SaaS metrics for a subscription business
- Design a metrics dashboard layout with KPIs and visualizations
- Set up cohort retention analysis and revenue tracking
- Create a reporting cadence for stakeholders or personal review

**DO NOT** use this skill for financial forecasting models, investor reporting decks, or marketing analytics dashboards. This is for core SaaS business health metrics.

---

## Core Principle

TRACK THE METRICS THAT DRIVE DECISIONS — A DASHBOARD WITH 50 METRICS IS A DASHBOARD NOBODY USES. FOCUS ON THE 8-12 NUMBERS THAT TELL YOU IF YOUR BUSINESS IS HEALTHY.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Product and pricing** | "What is your SaaS product and what are the plan prices?" | No default — must be provided |
| **Current MRR** | "What is your current monthly recurring revenue?" | Unknown — establish tracking |
| **Billing model** | "Monthly, annual, or both? Any usage-based component?" | Monthly subscriptions |
| **Data sources** | "Where does your billing data live? Stripe, Paddle, custom?" | Stripe |
| **Team size** | "Who reviews this dashboard? Just you, or a team?" | Solo founder |
| **Current tracking** | "What metrics do you currently track, if any?" | Revenue only |

**GATE: Confirm the brief before defining the metrics framework.**

---

## Phase 2: Define Metrics

### Tier 1: Must-Track (Daily/Weekly Review)

| Metric | Formula | Why It Matters |
|--------|---------|---------------|
| **MRR** | Sum of all active subscription revenue | Core health indicator |
| **MRR Growth Rate** | (MRR this month - MRR last month) / MRR last month | Velocity of growth |
| **Churn Rate** | Customers lost / Customers at start of period | Retention health |
| **Net Revenue Retention** | (MRR start + expansion - contraction - churn) / MRR start | Growth without new sales |

### Tier 2: Strategic (Monthly Review)

| Metric | Formula | Why It Matters |
|--------|---------|---------------|
| **LTV** | ARPU / Monthly churn rate | Customer lifetime value |
| **CAC** | Total acquisition spend / New customers acquired | Cost to acquire |
| **LTV:CAC Ratio** | LTV / CAC | Unit economics health (target 3:1+) |
| **Expansion MRR** | Revenue from upgrades and add-ons | Growth from existing customers |
| **ARPU** | MRR / Active customers | Average revenue per user |

### Tier 3: Deep Dives (Quarterly)

| Metric | Formula | Why It Matters |
|--------|---------|---------------|
| **Cohort Retention** | % of cohort still active at month N | True retention over time |
| **Revenue Churn vs. Logo Churn** | Revenue lost vs. customers lost | Reveals whether big or small accounts leave |
| **Payback Period** | CAC / (ARPU x Gross Margin) | Months to recoup acquisition cost |

**GATE: Confirm which metrics to include before designing the layout.**

---

## Phase 3: Design the Dashboard

### Layout Recommendations

**Top row (KPI cards):** MRR, MRR Growth Rate, Active Customers, Churn Rate
**Second row (charts):** MRR trend (line chart, 12 months), Revenue breakdown (stacked bar: new, expansion, contraction, churn)
**Third row:** Cohort retention table (heatmap), LTV:CAC trend
**Bottom row:** Recent activity feed (new signups, churns, upgrades)

### Dashboard Specifications

For each metric, document:
- Metric name and definition
- Data source and calculation method
- Visualization type (number, chart, table)
- Update frequency (real-time, daily, monthly)
- Alert threshold (e.g., churn exceeds 5%)

### Tool Recommendations

| Tool | Best For | Price Range |
|------|----------|-------------|
| **Stripe Dashboard** | Basic MRR and churn | Free with Stripe |
| **Baremetrics/ChartMogul** | Full SaaS metrics | $50-250/month |
| **Google Sheets** | Custom calculations | Free |
| **Notion** | Manual tracking for early stage | Free-$10/month |

---

## Phase 4: Polish

### 1. Reporting Cadence

```
## Review Schedule

- **Daily:** MRR, new signups, churns (glance at KPI cards)
- **Weekly:** MRR growth rate, trial conversions, support ticket volume
- **Monthly:** Full dashboard review, cohort analysis, LTV:CAC check
- **Quarterly:** Deep dive on retention cohorts, CAC trends, pricing evaluation trigger
```

### 2. Alert System

Define automated alerts:
- MRR drops more than 5% month-over-month
- Churn rate exceeds target threshold
- LTV:CAC ratio drops below 3:1
- No new signups for 3+ consecutive days
- Large account cancels or downgrades

### 3. Quality Checklist

```
## Dashboard Checklist

- [ ] MRR is tracked and updated daily
- [ ] Churn rate is calculated correctly (logo and revenue)
- [ ] LTV and CAC are defined with clear formulas
- [ ] Net revenue retention is tracked monthly
- [ ] Cohort retention table is set up (minimum 6-month view)
- [ ] Dashboard loads quickly and is not cluttered
- [ ] Alerts are configured for critical thresholds
- [ ] Review cadence is documented and followed
- [ ] All metrics have clear definitions (no ambiguity)
- [ ] Data source is reliable and automated (not manual entry)
```

---

## Example

**Product:** Project management SaaS, $19/$49/$99 plans
**MRR:** $12,400
**Customers:** 340 active

**KPI Card Layout:**
```
| MRR: $12,400 (+8.2%) | Active: 340 (+12) | Churn: 3.2% | ARPU: $36.47 |
```

**Alert example:**
"Alert: Monthly churn rate hit 4.1% (target: under 3.5%). Three accounts on the $99 plan canceled this week. Review cancellation reasons in exit surveys."

---

## Anti-Patterns

- **Vanity metrics on the dashboard** — total signups (all-time) tells you nothing. Track active customers and MRR.
- **Manual data entry** — if metrics require manual updates, they will go stale. Automate the data pipeline.
- **Too many metrics** — 8-12 core metrics maximum. Everything else is a report, not a dashboard.
- **No definitions** — if two people calculate churn differently, the metric is useless. Document every formula.
- **Ignoring cohorts** — aggregate churn hides whether retention is improving over time. Cohort analysis reveals the truth.

---

## Recovery

- **No billing data access:** Start with a manual Google Sheet tracker. Log MRR, new customers, and churns weekly until you can automate.
- **Too early for meaningful metrics:** Track MRR and customer count. Add churn and LTV once you have 3+ months of data.
- **Multiple pricing models:** Break metrics down by plan tier. Blended averages hide tier-specific problems.
- **Metrics look bad:** That is the point. A dashboard that only shows good numbers is not doing its job. Identify the worst metric and focus improvement there.
