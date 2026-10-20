---
name: product-metrics
description: "When to activate: product metrics, north star metric, KPIs, retention metrics, engagement metrics, revenue metrics, metric tree, dashboard, DAU MAU"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: business
  domain: product
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---

# Product Metrics

## North Star Metric Framework

### What Makes a Good North Star
1. Captures value delivered to customers (not just revenue)
2. Predictive of long-term business success
3. Actionable — teams can influence it
4. Understandable — whole company can explain it
5. Measurable — available in near real-time

### North Star Examples by Business Model
| Business Model | North Star Metric |
|---------------|-------------------|
| B2B SaaS | Weekly active teams |
| Consumer social | DAU/MAU ratio |
| Marketplace | GMV (gross merchandise value) |
| Media/content | Total reading time per week |
| E-commerce | Orders per customer per year |
| Developer tools | Weekly active developers running builds |
| Collaboration | Files shared per user per week |
| Fintech | Transactions processed per active user |

## Metric Tree (Input Metrics)

```
North Star: Weekly Active Teams

├── Acquisition
│   ├── New signups / week
│   ├── Trial activation rate (signup → first value)
│   └── Traffic × Conversion rate

├── Activation
│   ├── Time to first key action (< 3 days target)
│   ├── Onboarding completion rate (target: 70%)
│   └── Setup step completion rates (funnel)

├── Engagement (core action frequency)
│   ├── DAU / WAU / MAU
│   ├── Sessions per user per week
│   ├── Features used per session
│   └── Core action depth (# items created, shared, etc.)

├── Retention
│   ├── Day 1 / Day 7 / Day 30 retention
│   ├── Monthly churn rate
│   └── L30 (users active in last 30 days)

└── Expansion
    ├── Seats added per account per month
    ├── Upgrade rate (free → paid)
    └── NRR (Net Revenue Retention)
```

## Retention Metrics

### Cohort Retention Curve
```
Cohort: Users who signed up in January

         Day 0  Day 1  Day 7  Day 14  Day 30  Day 90
Jan cohort: 100%  40%   25%    20%     18%     15%

"Flattening" = product-market fit signal
Continuous decline = no PMF
```

### Retention Formulas
```
Day N Retention = Users from cohort active on Day N / Cohort size

Rolling Retention = Users from cohort active on Day N or later / Cohort size

Churn Rate (monthly) = Customers lost in period / Customers at start of period

Retention Rate = 1 - Churn Rate

Quick Ratio = (New MRR + Expansion MRR) / (Contraction MRR + Churn MRR)
  > 4 = excellent growth
  2-4 = healthy
  < 2 = leaky bucket
```

### Retention Benchmarks by Stage
| Stage | Day 1 | Day 7 | Day 30 |
|-------|-------|-------|--------|
| Early PMF (B2C) | 25-35% | 12-20% | 8-15% |
| Strong PMF (B2C) | 35-50% | 20-35% | 15-25% |
| B2B SaaS monthly | — | — | 90-95% |

## Engagement Metrics

### DAU/MAU Ratio (Stickiness)
```
Stickiness = DAU / MAU

> 20% = good (Slack ~50%, Facebook ~65%)
10-20% = moderate
< 10% = low engagement / wrong use case

Use WAU/MAU for weekly-use products
```

### L-Ness Framework (Active Users)
```
L7 = users active in last 7 days
L14 = users active in last 14 days
L28 = users active in last 28 days

L7/L28 = stickiness equivalent
```

### Feature Adoption Metrics
```
Feature Adoption Rate = Users who used feature / Total active users

Feature Frequency = Avg times feature used per user per period

Feature Breadth = Avg # of features used per active user (depth of product)
```

## Revenue Metrics (SaaS)

### Core SaaS Metrics
```
MRR = Monthly Recurring Revenue (sum of all monthly subscriptions)
ARR = MRR × 12 (or sum of annual contracts)

New MRR = revenue from new customers this month
Expansion MRR = upgrades, upsells, additional seats
Contraction MRR = downgrades
Churned MRR = cancelled subscriptions

Net New MRR = New MRR + Expansion MRR - Contraction MRR - Churned MRR

NRR (Net Revenue Retention) = 
  (MRR from cohort at end of period) / (MRR from same cohort at start)
  > 120% = world-class (customers expand faster than they churn)
  > 100% = growth without new customers
  < 100% = leaky bucket

GRR (Gross Revenue Retention) = NRR without expansion
  Healthy: > 85% SMB, > 90% enterprise
```

### Unit Economics
```
CAC (Customer Acquisition Cost) = 
  Total Sales & Marketing spend / New customers acquired

LTV (Lifetime Value) = 
  ARPU × Gross Margin % / Churn Rate
  or: ARPU × Average customer lifespan in months

LTV:CAC Ratio:
  > 3:1 = healthy (< 3 years payback)
  < 1:1 = losing money per customer

CAC Payback Period = CAC / (ARPU × Gross Margin %)
  < 12 months = excellent
  12-18 months = good
  > 24 months = concerning

ARPU (Average Revenue Per User) = MRR / # active paying customers
ARPA (Average Revenue Per Account) = MRR / # accounts
```

## Acquisition Metrics
```
Traffic → Sign-up Conversion Rate (target: 2-5% for B2B SaaS)
Sign-up → Activation Rate (target: 40-60%)
Activation → Paid Conversion Rate (target: 15-25% for PLG)
Trial → Paid Conversion Rate (target: 25% for freemium, 15% trial)

Lead Velocity Rate (LVR) = 
  (Qualified leads this month - last month) / last month × 100
  Leading indicator of future revenue growth
```

## Dashboard Design Principles

### Metric Hierarchy
```
Executive Dashboard (weekly)
├── North Star (vs goal)
├── MRR/ARR (vs goal)
├── Churn Rate (vs target)
└── CAC Payback Period

Team Dashboard (daily)
├── DAU / WAU (vs 7-day avg)
├── Activation rate (rolling 7d)
├── Feature-specific metrics
└── Error rates / P0 issues

Experiment Dashboard (real-time)
├── Treatment vs control metric
├── Statistical significance
└── Guardrail metrics (not regressions)
```

### Anti-Patterns
- Vanity metrics: total sign-ups without activation context
- Lagging-only dashboards: MRR is lagging, track leading indicators
- Too many metrics: max 5-7 metrics per dashboard
- No targets: every metric needs a goal and time horizon
- Missing context: always show trend + vs period / vs goal

## Metric Governance
- [ ] Each metric has a single owner
- [ ] Metric definitions documented (exact SQL/event name)
- [ ] Calculation methodology agreed cross-functionally
- [ ] Refresh cadence defined (real-time, daily, weekly)
- [ ] Metric changes require changelog entry
- [ ] Discrepancies between tools investigated and resolved
