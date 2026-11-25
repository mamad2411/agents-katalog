---
name: unit-economics
description: "Calculates unit economics for products and services with contribution margin, payback period, and LTV:CAC ratios. Use when evaluating the profitability of each customer or unit."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Unit Economics

## When to Use This Skill

Use this skill when you need to:
- Calculate the profitability of each customer, sale, or transaction
- Determine LTV, CAC, contribution margin, and payback period
- Evaluate whether your business model is fundamentally viable
- Prepare unit economics for investor presentations or strategic decisions

**DO NOT** use this skill for aggregate financial projections (use financial-projection) or pricing strategy (use pricing-strategy). This is for per-unit profitability analysis.

---

## Core Principle

IF THE UNIT ECONOMICS DO NOT WORK FOR ONE CUSTOMER, THEY DO NOT WORK FOR A THOUSAND — SCALE AMPLIFIES UNIT ECONOMICS, IT DOES NOT FIX THEM.

---

## Phase 1: Inputs

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Business model** | "Subscription, one-time purchase, marketplace, or service?" | No default — must be provided |
| **Average revenue per customer** | "What does one customer pay? (per month, per purchase, per project)" | No default — must be provided |
| **Cost to acquire a customer (CAC)** | "What do you spend in marketing/sales to get one customer?" | No default — estimate if unknown |
| **Cost to serve a customer** | "What does it cost to deliver the product/service to one customer?" | No default — must be provided |
| **Customer lifespan** | "How long does a customer stay? (months for subscriptions, repeat rate for purchases)" | 12 months |
| **Gross margin** | "What percentage of revenue is left after direct costs?" | Will calculate |

**GATE: Do not proceed without revenue per customer and cost to serve.**

---

## Phase 2: Core Calculations

```
## Unit Economics: [Product/Business]

### Per-Customer Revenue
| Metric | Value | Notes |
|--------|-------|-------|
| Average revenue per transaction | $[X] | |
| Transactions per month | [X] | |
| Monthly revenue per customer | $[X] | |
| Average customer lifespan | [X] months | |
| **Lifetime Value (LTV)** | **$[X]** | Monthly rev x lifespan |

### Per-Customer Costs
| Cost Component | Per Transaction | Per Month | Lifetime |
|---------------|----------------|-----------|----------|
| COGS / delivery | $[X] | $[X] | $[X] |
| Support / service | $[X] | $[X] | $[X] |
| Platform / transaction fees | $[X] | $[X] | $[X] |
| **Total cost to serve** | **$[X]** | **$[X]** | **$[X]** |

### Contribution Margin
| Metric | Per Month | Per Lifetime |
|--------|-----------|-------------|
| Revenue | $[X] | $[X] |
| - Cost to serve | $[X] | $[X] |
| **= Contribution margin** | **$[X]** | **$[X]** |
| **Contribution margin %** | **[X]%** | **[X]%** |

### Acquisition Economics
| Metric | Value | Formula |
|--------|-------|---------|
| Customer Acquisition Cost (CAC) | $[X] | Total marketing / New customers |
| LTV | $[X] | As calculated above |
| **LTV:CAC ratio** | **[X]:1** | LTV / CAC |
| **Payback period** | **[X] months** | CAC / Monthly contribution margin |
| CAC as % of LTV | [X]% | CAC / LTV x 100 |
```

---

## Phase 3: Health Assessment

### Benchmark Analysis

```
## Unit Economics Health Check

| Metric | Your Value | Healthy Benchmark | Status |
|--------|-----------|-------------------|--------|
| LTV:CAC | [X]:1 | >3:1 | [Healthy/Warning/Critical] |
| Payback period | [X] months | <12 months | [Healthy/Warning/Critical] |
| Contribution margin | [X]% | >50% | [Healthy/Warning/Critical] |
| Gross margin | [X]% | >60% (SaaS), >40% (product) | [Healthy/Warning/Critical] |
| CAC as % of first-year revenue | [X]% | <33% | [Healthy/Warning/Critical] |

### Interpretation
- **LTV:CAC > 3:1:** Healthy — room to invest more in acquisition
- **LTV:CAC 1-3:1:** Caution — improve retention or reduce CAC
- **LTV:CAC < 1:1:** Critical — losing money on every customer
- **Payback > 18 months:** Need significant capital to fund growth
```

### Sensitivity Table

```
## Sensitivity: What Moves the Needle

### Impact of Improving Each Lever by 10%
| Lever | Current | +10% | LTV:CAC Impact |
|-------|---------|------|---------------|
| Price increase | $[X] | $[X] | [X]:1 → [X]:1 |
| Reduce churn (extend lifespan) | [X] mo | [X] mo | [X]:1 → [X]:1 |
| Reduce CAC | $[X] | $[X] | [X]:1 → [X]:1 |
| Reduce COGS | $[X] | $[X] | [X]:1 → [X]:1 |
```

---

## Phase 4: Recommendations

```
## Action Plan

### Priority Lever: [Highest-impact lever from sensitivity]
[Specific recommendations to improve this lever]

### Unit Economics Improvement Roadmap
1. **Quick win:** [Action with immediate impact]
2. **Medium-term:** [Action requiring 1-3 months]
3. **Long-term:** [Structural change for sustained improvement]

### Monitoring
Track these metrics monthly:
- [ ] LTV (recalculate quarterly as lifespan data improves)
- [ ] CAC (by channel if possible)
- [ ] Contribution margin (watch for cost creep)
- [ ] Payback period (should decrease over time)
```

---

## Example: SaaS ($49/month, 14-month avg lifespan)

**LTV:** $686. **CAC:** $180 (blended across channels). **Monthly COGS:** $8. **Contribution margin:** $41/month (84%). **LTV:CAC:** 3.8:1. **Payback:** 4.4 months.

**Assessment:** Healthy unit economics. Biggest lever is retention — extending average lifespan from 14 to 16 months increases LTV by $82 and LTV:CAC to 4.3:1.

---

## Anti-Patterns

- **Using gross LTV without subtracting cost to serve** — LTV should represent gross profit, not gross revenue. A $100/month customer with $80/month costs has a $20/month contribution.
- **Blending CAC across all channels** — calculate CAC per channel. Your Google Ads CAC and referral CAC are likely very different.
- **Ignoring expansion revenue** — upsells and cross-sells increase LTV. Include them if tracking is available.
- **Static calculations** — unit economics change as you scale. Recalculate quarterly.
- **Assuming constant churn** — early churn is usually higher than late churn. Cohort analysis gives more accurate lifespan estimates.

---

## Recovery

- **No CAC data:** Estimate based on total marketing spend divided by new customers. Commit to tracking by channel going forward.
- **No churn data (one-time purchases):** Use repeat purchase rate instead of churn. LTV = Average order value x Average lifetime purchases.
- **Negative unit economics:** Identify which lever (price, COGS, CAC, retention) is most fixable. Show the math for what needs to change to reach 3:1 LTV:CAC.
- **Very early stage (< 50 customers):** Acknowledge that the data is preliminary. Use current numbers as a hypothesis and plan to validate with 3-6 months of additional data.
