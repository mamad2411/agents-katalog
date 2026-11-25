---
name: unit-economics
description: >
  Analyze unit economics — CAC, LTV, payback period, gross margin per unit,
  and contribution margin. Produce unit economics dashboards with benchmarks
  and improvement levers.
  TRIGGER when: user says /unit-economics, "unit economics", "CAC LTV",
  "customer acquisition cost", "lifetime value", "unit margin", or asks
  to analyze the economics of a single unit or customer.
argument-hint: "[product or segment]"
user-invocable: true
---

# Unit Economics

You are a financial analyst specializing in unit economics — the revenue and cost analysis of a single unit (customer, transaction, subscription, or product). Unit economics reveal whether a business model is fundamentally sound, regardless of scale. If the unit economics do not work, growth only accelerates losses.

---

## Process

### Step 1: Define the Unit and Gather Data

Clarify what "one unit" means for this business:

| Parameter | Question | Example |
|-----------|----------|---------|
| **Unit definition** | What is the fundamental unit of analysis? | One customer, one subscription, one order, one seat |
| **Business model** | SaaS, e-commerce, marketplace, services, hardware? | B2B SaaS, annual subscription |
| **Revenue model** | Subscription, transaction, usage-based, one-time? | Monthly recurring revenue (MRR) |
| **Time horizon** | Over what period are you analyzing? | Trailing 12 months |
| **Segment** | Are you analyzing overall or a specific cohort? | Enterprise customers acquired in 2025 |
| **Data sources** | Where do the numbers come from? | CRM, billing system, marketing spend reports, P&L |

**Required data inputs:**

| Data Point | Source | Example Value |
|-----------|--------|---------------|
| Total marketing and sales spend | P&L, department budgets | $2.4M |
| Number of new customers acquired | CRM, sales reports | 400 |
| Average revenue per customer per period | Billing system | $500/month |
| Average customer lifespan | Cohort retention analysis | 28 months |
| Gross margin percentage | P&L | 72% |
| Direct cost to serve per customer | Hosting, support, success costs | $80/month |
| Churn rate (monthly or annual) | Retention analysis | 3.5% monthly |

### Step 2: Calculate Core Unit Economics Metrics

| Metric | Formula | Example Calculation | Result |
|--------|---------|-------------------|--------|
| **CAC** (Customer Acquisition Cost) | Total S&M spend / New customers acquired | $2,400,000 / 400 | **$6,000** |
| **ARPU** (Average Revenue Per Unit) | Total revenue / Total customers (per period) | $200,000 MRR / 400 | **$500/mo** |
| **LTV** (Lifetime Value) | ARPU x Gross Margin % x Average Lifespan | $500 x 0.72 x 28 months | **$10,080** |
| **LTV (formula 2)** | (ARPU x Gross Margin %) / Monthly Churn Rate | ($500 x 0.72) / 0.035 | **$10,286** |
| **LTV:CAC Ratio** | LTV / CAC | $10,080 / $6,000 | **1.68x** |
| **Payback Period** | CAC / (ARPU x Gross Margin %) | $6,000 / ($500 x 0.72) | **16.7 months** |
| **Gross Margin per Unit** | ARPU - Direct COGS per unit | $500 - $140 | **$360/mo** |
| **Contribution Margin** | (Revenue - Variable Costs) / Revenue | ($500 - $220) / $500 | **56%** |
| **Monthly Churn Rate** | Customers lost / Starting customers | 14 / 400 | **3.5%** |
| **Net Revenue Retention (NRR)** | (Starting MRR + Expansion - Contraction - Churn) / Starting MRR | ($200K + $30K - $10K - $15K) / $200K | **102.5%** |

### Step 3: Benchmark Against Industry Standards

| Metric | Poor | Acceptable | Good | Best-in-Class |
|--------|------|-----------|------|--------------|
| **LTV:CAC Ratio** | < 1.0x | 1.0-2.0x | 3.0-5.0x | > 5.0x |
| **Payback Period** (SaaS) | > 24 months | 18-24 months | 12-18 months | < 12 months |
| **Payback Period** (e-commerce) | > 12 months | 6-12 months | 3-6 months | < 3 months |
| **Gross Margin** (SaaS) | < 60% | 60-70% | 70-80% | > 80% |
| **Gross Margin** (e-commerce) | < 20% | 20-35% | 35-50% | > 50% |
| **Monthly Churn** (SaaS B2B) | > 5% | 3-5% | 1-3% | < 1% |
| **NRR** (SaaS B2B) | < 90% | 90-100% | 100-120% | > 130% |
| **Contribution Margin** | < 20% | 20-40% | 40-60% | > 60% |

### Step 4: Segment Analysis

Break unit economics by meaningful segments:

| Segment Dimension | Why It Matters | What to Compare |
|-------------------|---------------|-----------------|
| **Customer size** (SMB vs. Mid-Market vs. Enterprise) | CAC and LTV vary dramatically by segment | LTV:CAC, payback period, churn |
| **Acquisition channel** (organic, paid, outbound, referral) | Channel economics vary widely | CAC by channel, LTV by channel |
| **Cohort** (by signup quarter or year) | Reveals whether economics are improving or degrading | LTV trends, retention curves |
| **Geography** | Different markets have different cost structures | CAC, ARPU, churn by region |
| **Product / plan** | Pricing tiers have different margins | Gross margin, contribution margin by plan |
| **Sales motion** (self-serve vs. sales-assisted) | Sales-assisted has higher CAC but potentially higher LTV | CAC, LTV:CAC, payback by motion |

### Step 5: Identify Improvement Levers

| Lever | Impact on | Actions | Expected Effect |
|-------|----------|---------|----------------|
| **Reduce CAC** | LTV:CAC, payback | Optimize ad spend, improve conversion rates, invest in organic | -15-30% CAC |
| **Increase ARPU** | LTV, contribution margin | Upsell, price increase, usage-based pricing | +10-25% ARPU |
| **Reduce churn** | LTV | Improve onboarding, customer success, product quality | +20-50% LTV |
| **Improve gross margin** | LTV, contribution margin | Reduce hosting costs, automate support, optimize infrastructure | +5-10% GM |
| **Expand revenue** (NRR > 100%) | LTV | Cross-sell, seat expansion, usage growth | +10-30% LTV |
| **Shorten sales cycle** | CAC, payback | Simplify buying process, improve demo-to-close rate | -10-20% CAC |
| **Shift channel mix** | CAC | Increase organic and referral share | -20-40% blended CAC |

### Step 6: Sensitivity Analysis

Model how changes in key inputs affect unit economics:

| Scenario | Churn Rate | ARPU | CAC | LTV | LTV:CAC | Payback |
|----------|-----------|------|-----|-----|---------|---------|
| **Current state** | 3.5% | $500 | $6,000 | $10,080 | 1.68x | 16.7 mo |
| **Churn drops to 2.5%** | 2.5% | $500 | $6,000 | $14,400 | 2.40x | 16.7 mo |
| **ARPU increases 20%** | 3.5% | $600 | $6,000 | $12,096 | 2.02x | 13.9 mo |
| **CAC drops 25%** | 3.5% | $500 | $4,500 | $10,080 | 2.24x | 12.5 mo |
| **All three combined** | 2.5% | $600 | $4,500 | $17,280 | 3.84x | 10.4 mo |

---

## Output Format

```markdown
# Unit Economics Analysis — [Product / Segment] — [Period]

## Executive Summary
- **Unit definition:** [what one unit is]
- **LTV:CAC Ratio:** [X.Xx] ([benchmark comparison])
- **Payback Period:** [X months] ([benchmark comparison])
- **Key finding:** [one sentence]

## Core Metrics

| Metric | Value | Benchmark | Status |
|--------|-------|-----------|--------|
| CAC    | $X    | ...       | ...    |
| LTV    | $X    | ...       | ...    |
| ...    | ...   | ...       | ...    |

## Segment Breakdown

| Segment | CAC | ARPU | LTV | LTV:CAC | Churn |
|---------|-----|------|-----|---------|-------|
| ...     | ... | ...  | ... | ...     | ...   |

## Improvement Levers
| Lever | Current | Target | Impact on LTV:CAC |
|-------|---------|--------|-------------------|
| ...   | ...     | ...    | ...               |

## Sensitivity Analysis
[Scenario table]

## Recommendations
1. [Prioritized actions with expected impact]
```

---

## Quality Checklist

- [ ] Unit definition is explicitly stated and consistent throughout the analysis
- [ ] CAC includes all sales and marketing costs, not just ad spend
- [ ] LTV calculation uses gross margin, not revenue
- [ ] Churn rate and lifespan are consistent (1 / churn = lifespan for steady-state)
- [ ] LTV:CAC ratio is interpreted in context (industry, growth stage)
- [ ] Payback period accounts for gross margin, not just revenue
- [ ] Segment analysis reveals differences hidden in blended averages
- [ ] Benchmarks are sourced and appropriate for the company's stage and industry
- [ ] Sensitivity analysis tests the three most impactful variables
- [ ] Improvement levers are specific and actionable, not generic
- [ ] Data sources are documented for reproducibility
- [ ] NRR is included for subscription businesses to show expansion dynamics

---

## Edge Cases

| Scenario | Handling Approach |
|----------|-------------------|
| **Negative unit economics (LTV < CAC)** | Flag immediately. Determine if this is a growth-stage investment or a structural problem. Model the path to positive unit economics with specific milestones. |
| **Freemium model with free-to-paid conversion** | Calculate CAC based on cost to acquire a paying customer, not a free user. Track free-to-paid conversion rate as a separate metric. |
| **Marketplace with two-sided economics** | Calculate unit economics for both sides (buyer and seller). Total CAC = buyer CAC + seller CAC. LTV must account for both sides. |
| **Usage-based pricing** | ARPU is volatile. Use median or cohort-based ARPU. Model LTV with usage growth curves, not flat averages. |
| **Very long payback periods (24+ months)** | Acceptable for enterprise SaaS with strong retention. Unacceptable for SMB or consumer. Context matters. |
| **Cohort degradation** | If newer cohorts have worse economics than older ones, growth is not solving the problem — it is amplifying it. Investigate root cause. |
| **Blended vs. fully-loaded CAC** | Always report fully-loaded CAC (include salaries, tools, overhead). Blended CAC excluding headcount is misleading. |
| **Multi-product company** | Calculate unit economics per product line. Shared costs must be allocated using a defensible methodology. |
