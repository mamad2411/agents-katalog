---
name: revenue-forecasting
description: Builds revenue forecasts — cohort-based, pipeline-driven, or SaaS metric-driven models with top-down and bottom-up approaches, growth scenarios, and revenue composition analysis. Use when the user mentions "revenue forecast," "model revenue growth," "forecast ARR," "project pipeline revenue," "growth rate," or asks about "expansion revenue vs new logo revenue."
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [cfo, finance, revenue-forecasting, saas-metrics, cohort-analysis, growth-modeling]
related_skills: [budget-creation-management, unit-economics-analysis, scenario-planning, cash-forecasting, forecast-accuracy-tracking]
inputs_required: [historical-revenue-monthly, customer-acquisition-data, pipeline-data, churn-data-by-segment, expansion-data]
deliverables: [revenue-forecast-monthly-24-36-months, revenue-composition-waterfall, key-assumptions-register]
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Revenue Forecasting

Build robust revenue forecasts — the foundation of every other financial model. Use multiple methods (cohort, pipeline, SaaS metrics), project by segment, and model growth levers. Goal: a revenue forecast that the CEO trusts, the board believes, and the team can execute against.

## Purpose

Revenue is the single most important input to every financial model — budget, cash flow, headcount, and valuation all depend on it. This skill provides multiple validated methods to project revenue, reconcile them against each other, and produce a forecast that stakeholders can trust and act on.

## When to Use

- "Build our revenue forecast"
- "Model revenue growth for next year"
- "Forecast ARR by cohort"
- "Project enterprise pipeline revenue"
- "What growth rate is realistic?"
- "Model expansion revenue vs new logo revenue"

## Inputs Required

1. **Historical revenue** — monthly MRR/ARR, broken out by: new logos, expansion, churn/contraction. At least 12 months.
2. **Customer acquisition data** — new customers per month, by segment/channel.
3. **Pipeline data** — for enterprise sales: qualified pipeline by stage, historical win rates, average deal size, cycle time.
4. **Churn data** — logo churn and revenue churn by segment and cohort.
5. **Expansion data** — NRR trends, upsell rates, price increase schedule.

## Quick Reference

| Metric | Formula | What It Tells You |
|--------|---------|-------------------|
| Net New ARR | New Logo ARR + Expansion ARR − Churned ARR − Contraction ARR | Growth engine health |
| NRR (Net Revenue Retention) | (Starting ARR + Expansion − Churn − Contraction) / Starting ARR | Customer value expansion |
| Logo churn rate | Customers lost / Starting customers | Customer retention |
| Pipeline coverage | Weighted pipeline value / Quota | Sales capacity to hit target |
| Growth deceleration | Current growth rate vs size-adjusted benchmark | Realistic growth expectations |

## Procedure

### 1. Revenue Composition Analysis

Break down revenue growth:

```
Net New ARR = New Logo ARR + Expansion ARR - Churned ARR - Contraction ARR

Growth Rate = (Ending ARR - Starting ARR) / Starting ARR
```

| Component | Current Quarter | Next Q Estimate | Next Year Estimate |
|---|---|---|---|
| Starting ARR | $1,000,000 | $1,200,000 | $1,500,000 |
| + New Logo ARR | $300,000 | $350,000 | $600,000 |
| + Expansion ARR | $50,000 | $60,000 | $120,000 |
| - Churn/Contraction | ($150,000) | ($110,000) | ($80,000) |
| = Ending ARR | $1,200,000 | $1,500,000 | $2,140,000 |
| Growth Rate | — | 25% QoQ | ~43% YoY |

### 2. Choose Forecasting Methods (Use at Least 2 and Reconcile)

#### Method A: Cohort-Based (Bottom-Up)

Most accurate for SaaS. Model each monthly cohort:

```
For each month (M0, M1, M2...):
  New ARR acquired = f(marketing spend, sales capacity, growth rate assumption)
  Churned ARR from this cohort = cohort ARR × cohort churn rate
  Expansion ARR from this cohort = cohort ARR × expansion rate
  Net ARR from this cohort = Starting + New - Churn + Expansion
```

Cohort retention curves by segment:

| Month | Enterprise Retention | Mid-Market Retention | SMB Retention |
|---|---|---|---|
| 0 | 100% | 100% | 100% |
| 1 | 99% | 97% | 95% |
| 3 | 97% | 94% | 90% |
| 6 | 95% | 90% | 82% |
| 12 | 93% | 85% | 72% |

#### Method B: Top-Down (Market / Growth Rate)

```
Next Year ARR = Current ARR × (1 + growth rate)
```

Use when historical growth is steady. Adjust growth rate by:
- Market maturity (growth decelerates naturally)
- Law of large numbers (harder to grow 100% from $10M than from $1M)
- Planned investments (hiring sales team, new product launch)

#### Method C: Pipeline-Based (Enterprise)

```
Quarterly new ARR = (Pipeline created × Win rate) × Avg deal size

Stages:
  Pipeline created → Qualified → Proposal → Negotiation → Closed Won
```

| Stage | Conversion | Cumulative |
|---|---|---|
| Pipeline created → Qualified | 40% | 40% |
| Qualified → Proposal | 50% | 20% |
| Proposal → Negotiation | 60% | 12% |
| Negotiation → Closed Won | 70% | 8.4% |

Bottom-up: multiply each deal's value by its stage probability. Sum for the total risk-adjusted pipeline.

### 3. Build the Forecast

For each of the next 12-36 months:

1. Project new logos by segment (using historical trend + planned investment).
2. Apply cohort retention curves to existing customers.
3. Apply expansion/renewal uplift assumptions.
4. Sum to total revenue.

### 4. Growth Driver Sensitivity

Model the impact of changing key drivers:

| Driver | Change | ARR Impact (Year 1) |
|---|---|---|
| New logo acquisition rate | +20% | +$X |
| Logo churn rate | -1% | +$Y |
| NRR | +5% | +$Z |
| Sales cycle time | -15 days | Pulls revenue forward |

### 5. Sanity Checks

- Is growth rate consistent with market benchmarks? (Seed: 10-20% MoM, Series A: 8-15%, Series B+: 4-10%)
- Does NRR make sense? (>100% is good, >120% is exceptional, <100% is trouble)
- Are assumptions getting more conservative over time? (They should — forecasting gets harder the further out you go.)

## Output Format

- Revenue forecast (monthly for 24-36 months)
- Revenue composition waterfall (new, expansion, churn, contraction)
- Key assumptions register
- Growth rate trajectory chart data
- Top-line summary for the CEO: "ARR goes from $X to $Y in 12 months, driven by Z"

## Done Criteria

The skill is complete when:
1. At least two independent forecasting methods are built and reconciled against each other.
2. Revenue is broken out into new logos, expansion, churn, and contraction components.
3. NRR, logo churn, and growth rates are calculated and benchmarked.
4. Key assumptions are documented and sensitivity ranges are provided.
5. The forecast is presented with a clear narrative: what drives the number and what could change it.

## Pitfalls

1. **Forecasting constant growth rates** — a company growing 10% MoM at $500k ARR won't sustain that at $10M ARR. The law of large numbers applies. Model deceleration explicitly.
2. **Blending unlike revenue streams** — mixing high-margin SaaS with low-margin services, one-time implementation fees, or marketplace GMV into one top-line number obscures the real growth story. Always disaggregate by type.
3. **Over-indexing on pipeline coverage** — a 3x pipeline coverage ratio means nothing if the pipeline is stale, unqualified, or padded. Audit pipeline health, not just volume.
4. **Ignoring cohort decay** — assuming the January 2025 cohort retains at the same rate as the January 2024 cohort without checking whether product quality, support, or competitive dynamics have changed. Validate retention curves against recent cohorts.
5. **Single-method forecasting** — relying on only top-down or only bottom-up creates blind spots. Always reconcile at least two independent methods; disagreement between them is the most valuable signal.

### Heuristics

- **NRR > 120% = best-in-class**: means you could stop selling and still grow 20%.
- **Logo churn < 2%/month for SMB, < 1%/month for enterprise**: above that, you're leaking faster than you can fill.
- **Growth naturally decelerates**: a company growing 150% at $1M ARR will likely grow 80-100% at $3M, 50-70% at $10M. Don't forecast constant growth rates.
- **The most common forecasting error**: overestimating new logo acquisition and underestimating churn. Be pessimistic on both.

### Edge Cases

- **Usage-based pricing** (e.g., API, AI models): forecast based on usage growth and price per unit, not fixed subscriptions.
- **Marketplace / take rate models**: forecast GMV, then apply the take rate.
- **Professional services revenue**: less predictable, lower margin. Keep it separate from SaaS revenue. Investors discount it.
- **Channel / partner revenue**: slower ramp, less control. Use a separate, more conservative forecast.
- **New product launch**: zero revenue until proven. Keep it as a separate "new product" line item until it has 6+ months of traction.

## Verification

Can you answer "What will our ARR be in 12 months and what are the three biggest assumptions behind that number?" Can you explain the gap between the top-down and bottom-up forecasts? If the two methods disagree, do you know why? If not, the forecast isn't ready for decision-making.

## Example

1. > **User**: "Build a revenue forecast for the next 24 months using our cohort data."
   > **Expected behavior**: You load monthly acquisition and churn data by segment, project new logos using historical rates adjusted for planned S&M investment, apply cohort retention curves, layer on expansion revenue assumptions, and output a monthly ARR forecast with a composition waterfall.

2. > **User**: "What growth rate is realistic for us next year?"
   > **Expected behavior**: You run a top-down deceleration analysis (current growth rate, size-adjusted benchmarks), compare against bottom-up cohort projections, identify the gap, and present a range: "Based on your $3M ARR and market comps, 60-80% YoY is realistic. Your cohort model suggests 90%, which implies you need to validate your new logo acquisition assumptions."

3. > **User**: "Model what happens if our enterprise sales cycle goes from 60 days to 90 days."
   > **Expected behavior**: You take the pipeline-based forecast, extend cycle times by 50%, recalculate when deals close, and show the revenue timing impact — likely a ~15-20% reduction in year-1 recognized revenue with the same total contract value pushed into year 2.

## Linked Skills

- OpEx plan to support revenue → `budget-creation-management`
- CAC / LTV / efficiency detail → `unit-economics-analysis`
- Alternative scenarios → `scenario-planning`
- Cash flow from revenue → `cash-forecasting`
- Track how well we forecast → `forecast-accuracy-tracking`
