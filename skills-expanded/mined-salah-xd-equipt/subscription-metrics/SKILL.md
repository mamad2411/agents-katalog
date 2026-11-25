---
name: subscription-metrics
description: "Calculates and reports on subscription metrics including MRR, ARR, churn rate, LTV, and CAC. Use when tracking the health of a subscription-based business."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Subscription Metrics

## When to Use This Skill

Use this skill when you need to:
- Calculate core subscription business metrics (MRR, ARR, churn, LTV, CAC)
- Create a subscription metrics dashboard or report
- Analyze the health of a recurring revenue business
- Identify trends and areas for improvement in subscription performance

**DO NOT** use this skill for one-time purchase businesses, general financial reporting, or ad hoc revenue calculations. This is for recurring revenue business models.

---

## Core Principle

SUBSCRIPTION BUSINESSES LIVE AND DIE BY RETENTION — MRR GROWTH MEANS NOTHING IF CHURN IS EATING IT FROM BELOW.

---

## Phase 1: Data Collection

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Current MRR** | "What is your current monthly recurring revenue?" | No default — must be provided |
| **Total active subscribers** | "How many paying subscribers do you have?" | No default — must be provided |
| **New subscribers this month** | "How many new subscribers joined this month?" | No default — must be provided |
| **Churned subscribers this month** | "How many subscribers cancelled this month?" | No default — must be provided |
| **Expansion revenue** | "Any upgrades or add-on revenue this month?" | $0 |
| **Total marketing spend** | "What did you spend on acquisition this month?" | No default — estimate if unknown |
| **Pricing tiers** | "What are your subscription price points?" | Single tier |

**GATE: Do not proceed without MRR, subscriber count, new subscribers, and churned subscribers.**

---

## Phase 2: Core Metrics

### Metric Calculations

```
## Subscription Metrics Report: [Month/Year]

### Revenue Metrics
| Metric | Value | Formula |
|--------|-------|---------|
| MRR | $[X] | Sum of all active subscriptions |
| ARR | $[X] | MRR x 12 |
| New MRR | $[X] | New subscriber revenue this month |
| Expansion MRR | $[X] | Upgrade/add-on revenue |
| Churned MRR | $[X] | Lost revenue from cancellations |
| Net New MRR | $[X] | New + Expansion - Churned |
| MRR Growth Rate | [X]% | Net New MRR / Previous MRR |
| ARPU | $[X] | MRR / Active subscribers |

### Customer Metrics
| Metric | Value | Formula |
|--------|-------|---------|
| Active subscribers | [X] | Current paying customers |
| New subscribers | [X] | Acquired this month |
| Churned subscribers | [X] | Cancelled this month |
| Net subscriber growth | [X] | New - Churned |
| Logo churn rate | [X]% | Churned / Start-of-month subscribers |
| Revenue churn rate | [X]% | Churned MRR / Start-of-month MRR |
| Net revenue retention | [X]% | (MRR - Churned + Expansion) / Start MRR x 100 |

### Unit Economics
| Metric | Value | Formula |
|--------|-------|---------|
| CAC | $[X] | Marketing spend / New subscribers |
| LTV | $[X] | ARPU / Monthly churn rate |
| LTV:CAC ratio | [X]:1 | LTV / CAC |
| Payback period | [X] months | CAC / ARPU |
| Gross margin | [X]% | (MRR - COGS) / MRR |
```

---

## Phase 3: Health Assessment

### Benchmark Comparison

```
## Health Check

| Metric | Your Value | Healthy Benchmark | Status |
|--------|-----------|-------------------|--------|
| Monthly churn | [X]% | <5% (SMB), <2% (Enterprise) | [Good/Warning/Critical] |
| Net revenue retention | [X]% | >100% | [Good/Warning/Critical] |
| LTV:CAC | [X]:1 | >3:1 | [Good/Warning/Critical] |
| Payback period | [X] months | <12 months | [Good/Warning/Critical] |
| MRR growth rate | [X]% | >10% MoM (early stage) | [Good/Warning/Critical] |
| Gross margin | [X]% | >70% (SaaS) | [Good/Warning/Critical] |
```

### Trend Analysis

```
## 6-Month Trend

| Metric | M-5 | M-4 | M-3 | M-2 | M-1 | Current | Trend |
|--------|-----|-----|-----|-----|-----|---------|-------|
| MRR | | | | | | | ↑↓→ |
| Churn % | | | | | | | ↑↓→ |
| New MRR | | | | | | | ↑↓→ |
| LTV:CAC | | | | | | | ↑↓→ |
```

### Recommendations

Based on the health check, provide 3-5 specific actions:

```
## Priority Actions

1. **[Action]** — [Why this matters based on the data]
2. **[Action]** — [Why]
3. **[Action]** — [Why]
```

---

## Phase 4: Deliverable

```
## Report Delivery

metrics/
└── subscription-metrics-[YYYY-MM].md
```

Include: All calculated metrics, health assessment, trend data (if available), and prioritized recommendations.

---

## Example: SaaS with 200 Subscribers

**Data:** MRR $5,800, 200 subscribers, 15 new, 8 churned, $400 expansion, $2,100 marketing spend.

**Results:** ARPU $29, logo churn 4%, revenue churn 3.4%, NRR 104%, CAC $140, LTV $853, LTV:CAC 6.1:1, payback 4.8 months.

**Assessment:** Healthy LTV:CAC and payback period. Churn at 4% is acceptable for SMB but worth reducing. NRR above 100% means expansion revenue covers churn — strong signal. Priority: reduce churn from 4% to 3% which would increase LTV by 33%.

---

## Anti-Patterns

- **Calculating LTV with revenue churn instead of logo churn** — use the right churn type for the right metric. Revenue churn for revenue LTV.
- **Ignoring expansion revenue** — net revenue retention is a more meaningful metric than gross churn alone
- **Monthly metrics without trends** — one month of data is a snapshot, not insight. Track at least 3-6 months for trends.
- **Blending free and paid users** — only include paying subscribers in these calculations. Free users are a different funnel stage.
- **Using averages when cohorts differ** — if you have multiple pricing tiers, calculate metrics per tier. Blended averages hide problems.

---

## Recovery

- **No historical data:** Start tracking now. Create the first report as a baseline and commit to monthly updates.
- **Very early stage (< 50 subscribers):** Small sample sizes make percentages unreliable. Report raw numbers alongside percentages and note the sample size caveat.
- **Churn data unavailable:** Use net subscriber change as a proxy. Set up proper churn tracking immediately — this is your most important metric.
- **Freemium model:** Separate free and paid metrics completely. Track free-to-paid conversion rate as an additional KPI.
