---
name: cohort-analysis
description: "Creates cohort analysis frameworks for understanding retention, revenue, and behavior patterns over time. Use when measuring how user groups perform across their lifecycle."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Cohort Analysis

## When to Use This Skill

Use this skill when you need to:
- Understand customer retention trends by signup month
- Compare revenue performance across acquisition cohorts
- Identify which customer groups behave differently over time
- Build a repeatable cohort analysis framework for ongoing use

**DO NOT** use this skill for one-time snapshot metrics, individual customer analysis, or real-time monitoring. This is for longitudinal group-based analysis.

---

## Core Principle

AVERAGES LIE — COHORT ANALYSIS REVEALS WHETHER YOUR BUSINESS IS ACTUALLY IMPROVING BY COMPARING HOW DIFFERENT GROUPS BEHAVE OVER THE SAME LIFECYCLE STAGE.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Analysis goal** | "What are you trying to understand? (retention, revenue, engagement, churn)" | Customer retention |
| **Cohort definition** | "How should cohorts be grouped? (signup month, acquisition channel, plan tier)" | Signup month |
| **Time granularity** | "Weekly, monthly, or quarterly cohorts?" | Monthly |
| **Observation window** | "How many periods to track each cohort?" | 6 months |
| **Data source** | "Where is your customer data? (Stripe, CRM, database, spreadsheet)" | Spreadsheet or Stripe |
| **Metric** | "What metric per cohort? (active users, revenue, orders, logins)" | Active users (retention) |

**GATE: Confirm brief before proceeding.**

---

## Phase 2: Design

### Cohort Table Structure

Build a triangular matrix:
- **Rows** = cohorts (e.g., Jan signups, Feb signups)
- **Columns** = lifecycle periods (Month 0, Month 1, Month 2...)
- **Cells** = metric value or percentage

### Analysis Framework

1. **Retention curve** — how each cohort declines over time (or does not)
2. **Cohort comparison** — are newer cohorts retaining better than older ones?
3. **Inflection points** — where does the biggest drop-off happen?
4. **Stabilization** — at what period do cohorts flatten out?
5. **Segment overlays** — do specific segments (channel, plan, geography) retain differently?

**GATE: Present the analysis framework and confirm before building templates.**

---

## Phase 3: Build

### Deliverables

**1. Cohort Analysis Template**
- Spreadsheet or table structure ready for data entry
- Formulas for calculating retention percentages
- Conditional formatting rules (green = good retention, red = steep drop)
- Chart template for visualizing retention curves

**2. Interpretation Guide**
- How to read the cohort table (rows, columns, diagonal patterns)
- What "good" retention looks like for the business type
- Common patterns and what they mean:
  - Improving rows = product is getting better
  - Steep Month 1 drop = onboarding problem
  - Flat curves after Month 3 = healthy core retention

**3. Segmented Analysis Plan**
- Which segments to overlay (acquisition source, pricing tier, geography)
- How to split cohorts for sub-analysis
- Comparison template for segment vs. segment

**4. Action Recommendations Framework**
- If Month 1 retention is below X%, focus on onboarding
- If retention flattens at Y%, invest in expansion over acquisition
- If newer cohorts are worse, investigate product or market changes

---

## Phase 4: Polish

### Reporting Cadence

- Monthly: update the cohort table with latest period data
- Quarterly: full analysis with segment overlays and trend narrative
- Trigger: run ad hoc analysis when a major change is made (pricing, onboarding, product)

### Presentation Template

One-page summary with: cohort table, retention curve chart, top 3 insights, and recommended actions.

---

## Example 1: SaaS Monthly Retention Cohorts

Cohorts by signup month. Metric: % of users active in each subsequent month. Goal: identify if onboarding improvements in March improved Month 1 retention vs. January cohort.

## Example 2: E-commerce Revenue Cohorts

Cohorts by first purchase month. Metric: cumulative revenue per cohort. Goal: understand which acquisition channels produce higher lifetime value customers.

---

## Anti-Patterns

- **Using averages instead of cohorts** — "Average retention is 40%" hides whether things are getting better or worse. Always break by cohort.
- **Too many cohorts** — 52 weekly cohorts on one chart is unreadable. Start monthly, go weekly only for specific investigations.
- **Ignoring cohort size** — a cohort of 5 users with 80% retention is not meaningful. Note sample sizes.
- **Comparing different lifecycle stages** — Month 3 of a January cohort and Month 1 of a March cohort are not comparable. Align by period.
- **Analysis without action** — cohort data is diagnostic. Always end with "So what do we do about it?"

---

## Recovery

- **Not enough data:** Need at minimum 3 cohorts with 3 periods each. If data is thin, start tracking now and revisit in 3 months.
- **No customer-level data:** Use aggregate proxies (monthly active users vs. signups) for a rough cohort view. Plan to implement proper tracking.
- **Retention looks terrible:** Normalize expectations — B2C apps often see 20-30% Month 1 retention. Compare to industry benchmarks before panicking.
- **User cannot interpret the table:** Walk through one row in detail, explaining what each cell means for that specific cohort.
