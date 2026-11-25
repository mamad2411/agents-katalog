---
name: unit-economics-analysis
description: Analyzes startup unit economics — CAC, LTV, payback period, contribution margin by segment, cohort profitability, and efficiency metrics. Use when the user mentions "CAC," "LTV / CAC ratio," "payback period," "unit economics," "customer profitability," or asks about "which customer segments are most profitable" or "are we making money on each customer."
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [cfo, finance, unit-economics, cac-ltv, cohort-analysis, profitability]
related_skills: [revenue-forecasting, budget-creation-management, scenario-planning, profitability-analysis, pricing-strategy-advisory, business-case-modeling]
inputs_required: [revenue-by-customer-by-month, cogs-by-customer-or-segment, sand-spend-by-channel-and-segment, customer-acquisition-data-by-segment]
deliverables: [segment-unit-economics-dashboard, channel-efficiency-comparison, cohort-profitability-timeline, improvement-roadmap]
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Unit Economics Analysis

Analyze the fundamental economics of the business — what it costs to acquire a customer, what that customer is worth, and how long it takes to earn back the acquisition cost. Break down by segment, channel, and cohort. Goal: understand which customers are profit-generating engines and which are destroying value.

## Purpose

Blended metrics hide the truth. A 4x blended LTV/CAC ratio might look healthy, but if it's 10x for enterprise and 0.8x for SMB, the company has a ticking time bomb in one segment. This skill provides the segment-level and cohort-level analysis needed to make capital allocation decisions — where to invest more, what to fix, and what to stop doing.

## When to Use

- "What's our CAC?"
- "Calculate LTV / CAC ratio"
- "Analyze payback period by segment"
- "Which customer segments are most profitable?"
- "Unit economics deep dive"
- "Are we making money on each customer?"

## Inputs Required

1. **Revenue by customer by month** — for ARPU and churn calculations.
2. **COGS by customer or segment** — for gross margin.
3. **S&M spend by channel and segment** — for CAC.
4. **Customer acquisition data** — new logos by segment, source.

## Quick Reference

| Metric | Formula | Target |
|--------|---------|--------|
| CAC | Total S&M spend / New customers acquired | Varies by segment |
| LTV | (ARPU × Gross Margin %) / Monthly Churn Rate | > 3× CAC |
| LTV / CAC | LTV / CAC | > 3x healthy, < 1x existential |
| CAC Payback | CAC / (ARPU × Gross Margin %) | < 12 months good |
| NRR | (Starting ARR + Expansion − Churn − Contraction) / Starting ARR | > 100% good, > 120% excellent |

## Procedure

### 1. Calculate Segment-Level Metrics

For each meaningful segment (industry, size, channel, geography):

#### CAC (Customer Acquisition Cost)

```
Blended CAC = Total S&M spend in period / New customers acquired in period

Fully loaded CAC = (S&M salaries + marketing spend + tools + overhead allocation) / New customers

Paid CAC = Marketing + ads spend only / New customers from paid channels
```

**Segment CAC**: always calculate by segment. A blended CAC hides the real story.

| Segment | New Customers (Q) | S&M Spend (Q) | Blended CAC |
|---|---|---|---|
| Enterprise | 12 | $480,000 | $40,000 |
| Mid-Market | 25 | $375,000 | $15,000 |
| SMB | 80 | $160,000 | $2,000 |
| **Total** | **117** | **$1,015,000** | **$8,675** |

#### LTV (Customer Lifetime Value)

```
LTV = (ARPU × Gross Margin %) / Monthly Churn Rate

Alternative: LTV = ARPU × Gross Margin × Average Customer Lifetime (months)
```

**ARPU** = Average Revenue Per User/Customer per month.
**Gross margin** = (Revenue - COGS) / Revenue. For SaaS, typically 70-85%.
**Monthly churn** = % of customers who cancel per month.

| Segment | ARPU | Gross Margin | Monthly Churn | Avg Lifetime (mo) | LTV |
|---|---|---|---|---|---|
| Enterprise | $5,000 | 82% | 0.8% | 125 | $512,500 |
| Mid-Market | $1,200 | 80% | 1.5% | 67 | $64,320 |
| SMB | $150 | 78% | 4.0% | 25 | $2,925 |

#### LTV / CAC Ratio

```
LTV / CAC = Lifetime Value / Customer Acquisition Cost
```

| Ratio | Meaning |
|---|---|
| > 5x | Excellent — invest more in growth |
| 3-5x | Healthy — sustainable |
| 1-3x | Marginal — need to improve CAC or LTV |
| < 1x | Losing money on every customer — existential |

#### CAC Payback Period

```
CAC Payback (months) = CAC / (ARPU × Gross Margin %)
```

The number of months it takes a customer's gross profit to cover the cost of acquiring them.

| Segment | CAC | Monthly GP per Customer | Payback (months) |
|---|---|---|---|
| Enterprise | $40,000 | $4,100 | 9.8 |
| Mid-Market | $15,000 | $960 | 15.6 |
| SMB | $2,000 | $117 | 17.1 |

- **< 12 months**: good
- **12-18 months**: acceptable (but watch cash)
- **> 18 months**: cash flow problem — you're funding customer acquisition

### 2. Channel / Source Analysis

Same metrics, but by how the customer was acquired:

| Channel | New Customers | Spend | CAC | ARPU | LTV | LTV/CAC | Payback |
|---|---|---|---|---|---|---|---|
| Inbound / organic | | | | | | | |
| Paid search | | | | | | | |
| Outbound sales | | | | | | | |
| Partners | | | | | | | |
| Events | | | | | | | |

### 3. Cohort Profitability

Track a cohort's cumulative gross profit vs its acquisition cost over time:

| Month | Cohort Size | Cumulative Revenue | Cumulative COGS | Cumulative GP | Cumulative CAC | Net (GP - CAC) |
|---|---|---|---|---|---|---|
| 0 | 25 | $0 | $0 | $0 | $375,000 | −$375,000 |
| 3 | 23 | $82,800 | $16,560 | $66,240 | $375,000 | −$308,760 |
| 6 | 21 | $158,760 | $31,752 | $127,008 | $375,000 | −$247,992 |
| 12 | 20 | $300,000 | $60,000 | $240,000 | $375,000 | −$135,000 |
| 18 | 18 | $388,800 | $77,760 | $311,040 | $375,000 | −$63,960 |
| 24 | 17 | $448,800 | $89,760 | $359,040 | $375,000 | −$15,960 |
| 30 | 15 | $472,500 | $94,500 | $378,000 | $375,000 | **+$3,000** ← Breakeven |

### 4. Identify Improvement Levers

For each underperforming segment, identify the lever:

| Segment | Problem | Lever | Potential Impact |
|---|---|---|---|
| Mid-Market | CAC payback 15.6 months | Improve sales efficiency (ramp time, win rate) | Reduce payback to 10-12 months |
| SMB | LTV too low at $2,925 | Price increase, expansion revenue playbook | Increase LTV to $5,000+ |

## Output Format

- Segment unit economics dashboard
- Channel efficiency comparison
- Cohort profitability timeline
- Improvement roadmap (which levers to pull, ranked by impact)
- Benchmark comparison (how does the company compare to SaaS industry averages?)

## Done Criteria

The skill is complete when:
1. CAC, LTV, LTV/CAC, and payback period are calculated for each meaningful segment.
2. Channel-level efficiency is compared with clear rankings.
3. A cohort profitability timeline shows when each cohort breaks even or doesn't.
4. Specific improvement levers are identified for underperforming segments.
5. Results are benchmarked against SaaS industry standards.

## Pitfalls

1. **Using blended LTV/CAC without segment breakdown** — a 4x blended LTV/CAC that's 6x for enterprise and 0.8x for SMB is a business with a ticking time bomb in one segment. Blended metrics conceal capital allocation mistakes.
2. **Calculating CAC without sales ramp costs** — the fully-loaded cost of an enterprise sales rep includes base salary during their 6-month ramp period where they produce near-zero pipeline. Ignoring ramp costs understates true CAC by 30-50%.
3. **Treating LTV as static based on current churn** — if churn has been creeping up from 1.5% to 2.5% over the last 6 months, using the trailing 12-month average masks the trend. Always forward-project churn based on the most recent cohorts.
4. **Confusing revenue churn with logo churn** — a company losing 2% of logos but only 0.5% of revenue (because small customers churn) looks healthy on revenue churn alone. But logo churn is a leading indicator; today's logo churn becomes tomorrow's revenue churn when a big customer leaves.
5. **Benchmarking against bad public data** — comparing your SMB CAC payback of 17 months against a "SaaS benchmark" of 8 months without knowing whether that benchmark includes enterprise-only companies is misleading. Source your benchmarks carefully and match by segment and stage.

### Heuristics

- **LTV is a prediction, not a fact**: churn rates change, ARPU changes. Use conservative assumptions (higher churn, lower ARPU) for planning.
- **Most startups underestimate CAC and overestimate LTV**: be the honest voice in the room.
- **Blended metrics lie**: segment-level analysis is where the truth lives.
- **CAC payback < 12 months is a good rule of thumb**: above that, you're financing customer growth, which burns cash.
- **Paid CAC should be a fraction of blended CAC**: if it's not, your organic/word-of-mouth growth isn't working.

### Edge Cases

- **Pre-product-market-fit**: unit economics don't matter. Focus on PMF. Once you have it, THEN measure.
- **Marketplace businesses**: two-sided CAC (acquire both buyers and sellers). Both sides matter.
- **Freemium models**: CAC to paid conversion is the key metric, not CAC to signup. Track the entire funnel.
- **Very high NRR (>130%)**: the LTV formula breaks because churn is near zero and expansion is massive. Use a cohort model instead.
- **Enterprise with very long sales cycles (6-12 months)**: you're spending CAC for months before revenue starts. This creates a significant cash trough.

## Verification

Can you answer "Which customer segment is most profitable and why?" and "Which acquisition channel gives us the best return on every dollar spent?" Are the CAC, LTV, and payback numbers updated within the last quarter? If not, the unit economics view is stale.

## Example

1. > **User**: "Calculate our unit economics by segment — show me CAC, LTV, LTV/CAC, and payback period for enterprise, mid-market, and SMB."
   > **Expected behavior**: You pull revenue, COGS, churn, and S&M spend data by segment, calculate the four core metrics for each, present them in a comparison table, and highlight which segments are healthy vs needing intervention with specific improvement lever recommendations.

2. > **User**: "How profitable is the January 2024 mid-market cohort after 18 months?"
   > **Expected behavior**: You isolate that cohort, track cumulative gross profit against initial acquisition costs month by month, calculate when/if breakeven occurs, and compare against earlier cohorts to detect whether unit economics are improving or deteriorating over time.

3. > **User**: "What's our most efficient customer acquisition channel?"
   > **Expected behavior**: You calculate CAC, LTV, LTV/CAC, and payback by channel (inbound, paid, outbound, partners), rank them by efficiency, and flag any channels where CAC is rising or LTV is declining — recommending where to reallocate S&M budget.

## Linked Skills

- Revenue forecast inputs → `revenue-forecasting`
- Cost structure inputs → `budget-creation-management`
- Scenarios where churn or CAC spikes → `scenario-planning`
- Segment profitability → `profitability-analysis`
- Pricing changes → `pricing-strategy-advisory`
- ROI of acquisition channels → `business-case-modeling`
