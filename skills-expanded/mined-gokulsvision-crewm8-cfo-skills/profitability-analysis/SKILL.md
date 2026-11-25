---
name: profitability-analysis
description: Analyze profitability by dimension — product line, customer segment, channel, geography, cohort — identifying profit drivers and margin improvement opportunities for strategic decision-making.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [cfo, finance, profitability, margin-analysis, segmentation, product-pnl]
related_skills: [unit-economics-analysis, pricing-strategy-advisory, cost-optimization, revenue-forecasting, business-case-modeling]
inputs_required: [revenue-data-by-customer-product-channel-geography, cost-data-with-allocation-keys, customer-data-with-segment-labels, headcount-data-by-team-and-function]
deliverables: [profitability-heatmap, segment-product-channel-pnl, profit-concentration-analysis, kill-fix-invest-framework, improvement-recommendations]
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Profitability Analysis

Analyze profitability across every dimension of the business — by product, customer segment, channel, geography, and cohort. Identify what's making money, what's losing money, and where to focus. Goal: the company invests in its profit engines and fixes or kills its loss-makers.

## Purpose

Most startups look at blended gross margin and assume everything is fine. Segment-level profitability analysis almost always reveals ugly truths: a product that's losing money, a customer segment that destroys value, a geography that drains cash. Without this analysis, companies unknowingly invest in their loss-makers and underinvest in their profit engines. This skill provides the multi-dimensional view needed to allocate capital, set strategy, and improve margins where it matters.

## When to Use

- "Which products / customers / segments are most profitable?"
- "Analyze profitability by [dimension]"
- "Where are we losing money?"
- "Profitability deep dive"
- "Should we keep selling to SMB / that segment / that geography?"
- "Channel profitability analysis"

## Inputs Required

1. **Revenue data** — revenue by customer, product, channel, geography.
2. **Cost data** — COGS and OpEx with allocation keys (headcount by team, infrastructure by product, S&M by channel).
3. **Customer data** — segment labels, ARPU, churn rates.
4. **Headcount data** — employees by team, by product, by function.

## Quick Reference

| Profitability Level | What It Includes | Use Case |
|---------------------|-----------------|----------|
| Gross Profit | Revenue − Direct COGS | Product-level margin health |
| Contribution Margin | Gross Profit − Direct S&M (segment-level) | Channel and segment efficiency |
| Fully Loaded | Contribution − Shared R&D & G&A allocation | True economic profit |

| 80/20 Rule of Profit | Typical Finding |
|----------------------|-----------------|
| 20% of customers generate | 80%+ of profit |
| The bottom 20% of customers | Often destroy value (unprofitable) |
| 1-2 products/channels | Often account for majority of total profit |

## Procedure

### 1. Choose the Dimension(s)

Based on the business question, select which dimensions to analyze.

### 2. Allocate Costs Using Reasonable Drivers

- Hosting costs → usage data (compute hours, storage GB, API calls).
- Support costs → ticket volume by customer / product.
- S&M costs → headcount by segment + channel spend attribution.
- R&D costs → headcount by product team.
- G&A → headcount allocation or revenue share.

### 3. Calculate Profitability at Each Level

#### By Customer Segment

| ($ in 000s, annualized) | Enterprise | Mid-Market | SMB | Total |
|---|---|---|---|---|
| Revenue | $2,400 | $1,800 | $600 | $4,800 |
| Direct COGS (hosting, support allocation by tickets) | ($288) | ($270) | ($150) | ($708) |
| **Gross Profit** | **$2,112** (88%) | **$1,530** (85%) | **$450** (75%) | **$4,092** (85%) |
| Sales & Marketing allocation (by team/segment) | ($720) | ($540) | ($240) | ($1,500) |
| **Contribution Margin** | **$1,392** (58%) | **$990** (55%) | **$210** (35%) | **$2,592** (54%) |
| Shared R&D allocation | ($480) | ($360) | ($120) | ($960) |
| Shared G&A allocation | ($360) | ($270) | ($90) | ($720) |
| **Segment Profit (fully loaded)** | **$552** (23%) | **$360** (20%) | **$0** (0%) | **$912** (19%) |

#### By Product / Product Line

| Product | ARR | Gross Margin | Team Cost | Contribution | % of Total Profit |
|---|---|---|---|---|---|
| Core Platform | $3,200 | 85% | ($960) | $1,760 | 68% |
| Analytics Add-on | $1,000 | 80% | ($400) | $400 | 16% |
| API / Developer | $400 | 70% | ($200) | $80 | 3% |
| Professional Services | $200 | 40% | ($160) | ($80) | −3% |
| *Professional Services is losing money — fix or kill.* | | | | | |

#### By Customer Acquisition Channel

| Channel | ARR Acquired (12mo) | CAC (total) | 12-Month GP | Net (GP - CAC) | Payback (mo) |
|---|---|---|---|---|---|
| Inbound / Organic | $600,000 | $60,000 | $480,000 | $420,000 | 1.5 |
| Outbound Sales | $800,000 | $400,000 | $640,000 | $240,000 | 7.5 |
| Paid Search | $200,000 | $150,000 | $160,000 | $10,000 | 11.3 |
| Events | $100,000 | $80,000 | $80,000 | $0 | 12.0 |
| Partners | $150,000 | $30,000 | $120,000 | $90,000 | 3.0 |
| *Events and paid search are marginal. Outbound is good but expensive.* | | | | | |

#### By Geography

| Region | Revenue | Headcount | Other Costs | Profit | Margin % |
|---|---|---|---|---|---|
| North America | $3,500 | ($1,200) | ($700) | $1,600 | 46% |
| Europe | $800 | ($400) | ($200) | $200 | 25% |
| APAC | $300 | ($250) | ($150) | ($100) | −33% |
| *APAC is losing money — under-scale. Either invest to grow or pare back.* | | | | | |

#### Cohort Profitability

Track profit by the customer's vintage:

| Cohort (by quarter acquired) | Q Acquired ARR | Current ARR | NRR | Cumulative GP | Total CAC | Net Cumulative |
|---|---|---|---|---|---|---|
| Q1 2025 | $50,000 | $80,000 | 160% | $320,000 | ($75,000) | $245,000 |
| Q2 2025 | $80,000 | $110,000 | 138% | $280,000 | ($120,000) | $160,000 |
| Q3 2025 | $120,000 | $140,000 | 117% | $200,000 | ($180,000) | $20,000 |
| Q4 2025 | $150,000 | $145,000 | 97% | $80,000 | ($225,000) | ($145,000) |
| *Q4 2025 cohort is shrinking! Diagnose churn immediately.* | | | | | | |

### 4. Identify the 20% Driving 80% of Profit

Analyze which customers, products, or channels generate the majority of profit and which are destroying value.

### 5. Recommend: Kill, Fix, or Invest

For each underperforming area:
- **Kill**: if unprofitable with no path to improvement and no strategic value.
- **Fix**: if there's a clear lever to improve (price increase, cost reduction, efficiency).
- **Invest**: if it's a profit engine that deserves more capital.

## Output Format

- Profitability heatmap (green = profit engine, red = loss-maker)
- Segment / product / channel P&L
- Profit concentration analysis ("3 customers = 45% of total profit")
- Kill / Fix / Invest framework applied to the portfolio
- 3-5 concrete recommendations with estimated financial impact

## Done Criteria

The skill is complete when:
1. Profitability is analyzed across at least 2-3 dimensions (segment, product, channel, geography, or cohort).
2. Costs are allocated using reasonable, transparent drivers.
3. The profit concentration is identified (the 20% driving 80% of profit and the tail destroying value).
4. A Kill/Fix/Invest framework is applied to each area.
5. 3-5 specific recommendations are provided with estimated financial impact.

## Pitfalls

1. **Using blended gross margin as the only profitability metric** — blended metrics hide which segments or products are profitable and which are destroying value. Always disaggregate.
2. **Over-engineering cost allocation** — perfect allocation doesn't exist. Use simple, transparent drivers (headcount, usage, ticket volume). Don't let perfect be the enemy of good.
3. **Ignoring the cost allocation debates** — every department head will argue their allocation is unfair. Use simple rules, communicate them clearly, and hold the line. Don't re-litigate allocation methodology every quarter.
4. **Confusing contribution margin with fully loaded profit** — contribution margin tells you if a segment covers its direct costs. Fully loaded tells you the true economics. Use both, but know which is which.
5. **Killing unprofitable segments without considering strategic value** — sometimes you invest in a channel or geography for strategic reasons (network effects, future growth, competitive positioning). Make those decisions knowingly, not accidentally.

### Heuristics

- **80/20 of profit**: typically 20% of customers/products/channels generate 80%+ of profit. The tail is usually unprofitable.
- **Fully loaded is the honest answer**, but **contribution margin is the decision metric**: if a segment covers its direct costs + contributes to shared costs, it might be worth keeping even if fully loaded looks bad.
- **Most startups don't know their real profitability**: they look at blended gross margin and assume everything is fine. Segment-level analysis usually reveals ugly truths.
- **Unprofitable segments aren't always wrong**: sometimes you invest in a channel or geography for strategic reasons. Just do it knowingly, not accidentally.

### Edge Cases

- **Early-stage companies** with few customers: the data is too noisy. Focus on unit economics per customer rather than segment averages.
- **Network effects businesses**: some customers create value even if individually unprofitable (they bring other customers). Don't kill value-creators.
- **Cost allocation debates**: every department head will argue their allocation is unfair. Use simple, transparent drivers. Don't over-engineer it.
- **Strategic investments**: losing money in a new geography for 2-3 years can be fine. Set a clear timeline and investment cap.

## Verification

Can you answer "Which customer segment generates the most profit per dollar of revenue?" and "Which product line is losing money and why?" and "If we had to cut 20% of costs, where would we cut without hurting our most profitable segments?" If not, the profitability analysis is incomplete.

## Example

> **User**: "Which customer segments are most and least profitable?"
> **Expected behavior**: You pull revenue, COGS, and OpEx data by segment (enterprise, mid-market, SMB), allocate costs using reasonable drivers (headcount for S&M, ticket volume for support, usage for hosting), calculate gross profit, contribution margin, and fully loaded profit for each segment, present a comparison table, and recommend: enterprise is the profit engine (invest more), SMB is break-even (fix with price increase or efficiency), and mid-market needs monitoring.

> **User**: "Our professional services product line is losing money. Should we kill it?"
> **Expected behavior**: You build a product P&L for professional services showing revenue ($200k ARR), gross margin (40%), and fully loaded costs (team cost of $160k, shared costs of $80k, total loss of $40k). You analyze whether it drives core product adoption (customer success data: PS customers have 20% lower churn on core product). You recommend: don't kill — it's a strategic loss leader. Instead, raise PS rates by 25% and reduce delivery cost by standardizing engagements, targeting breakeven within 6 months.

## Linked Skills

- Customer-level economics → `unit-economics-analysis`
- Pricing changes to fix margin → `pricing-strategy-advisory`
- Cost reduction → `cost-optimization`
- Revenue forecast impact → `revenue-forecasting`
- Business case for fixing/launching → `business-case-modeling`
