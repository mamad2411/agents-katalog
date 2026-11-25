---
name: business-case-modeling
description: Builds business cases and ROI models — NPV, IRR, payback period, and break-even analysis for new initiatives, product launches, market expansions, and capital allocation decisions. Use when the user mentions "business case," "ROI," "NPV," "should we invest in," "payback period," "build vs buy," or asks about "is this partnership worth it" or "compare these two growth initiatives."
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [cfo, finance, business-case, roi, capital-allocation, investment-decision]
related_skills: [revenue-forecasting, budget-creation-management, unit-economics-analysis, scenario-planning, strategic-initiative-modeling, headcount-and-comp-planning]
inputs_required: [initiative-description-and-hypothesis, cost-estimates-one-time-and-recurring, revenue-or-savings-projections, timeline-and-risk-factors]
deliverables: [one-page-business-case-summary, detailed-cost-benefit-model, npv-irr-payback-breakeven, risk-matrix-with-mitigations]
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Business Case Modeling

Build rigorous business cases for major investment decisions — new products, market expansions, hiring teams, tool migrations, office moves. Model the full cost, the expected return, and the risks. Goal: every significant dollar of spend has a documented case for why it's worth it.

## Purpose

Startups make dozens of investment decisions each year — should we hire a sales team in Europe? Build a new product? Attend this conference series? Without a structured business case, decisions are driven by whoever argues most loudly or has the CEO's ear. This skill brings rigor and consistency to capital allocation by modeling costs, benefits, risks, and alternatives for every major spend decision.

## When to Use

- "Should we hire a sales team in Europe?"
- "Build a business case for this new product"
- "What's the ROI of attending this conference series?"
- "Model the payback on this tool migration"
- "Is this partnership worth the investment?"
- "Compare these two growth initiatives"

## Inputs Required

1. **Initiative description** — what you're doing, why, and the hypothesis.
2. **Cost estimates** — one-time costs (setup, migration, equipment) and recurring costs (headcount, tools, ongoing spend).
3. **Revenue or savings projections** — what value does this create? New revenue, cost savings, or efficiency gains.
4. **Timeline** — when costs hit and when benefits start.
5. **Risk factors** — what could go wrong, and how likely is it?

## Quick Reference

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| NPV | Present value of future cash flows minus initial investment | > $0 = invest |
| IRR | Discount rate that makes NPV = 0 | > cost of capital = value-creating |
| Payback period | Time to recover initial investment | < 3 years for startups |
| Break-even | Point where cumulative benefits equal cumulative costs | Lower is safer |
| Discount rate | Risk-adjusted cost of capital | 15% standard for startup projects |

## Procedure

### 1. Executive Summary (Write This Last, Present First)

> *"We're evaluating opening a 3-person sales presence in London to target European enterprise customers. Estimated cost: $450k in year 1 (3 headcount + travel + tools). Expected return: $300k ARR in year 1 (ramping), $800k in year 2, $1.5M+ in year 3. Payback: ~18 months. Recommendation: Proceed, with a 6-month go/no-go checkpoint."*

### 2. Full Cost Model

| Cost Category | Year 1 | Year 2 | Year 3 |
|---|---|---|---|
| **People** | | | |
| Salaries (3 FTE) | $330,000 | $350,000 | $375,000 |
| Benefits & Taxes (~25%) | $82,500 | $87,500 | $93,750 |
| Recruiting fees | $45,000 | $0 | $15,000 |
| **Non-People** | | | |
| Office / coworking | $24,000 | $30,000 | $36,000 |
| Travel | $18,000 | $24,000 | $30,000 |
| Tools & Software | $9,000 | $12,000 | $15,000 |
| Legal / entity setup | $15,000 | $3,000 | $3,000 |
| **Total Cost** | **$523,500** | **$506,500** | **$567,750** |

### 3. Benefits Model

| Revenue Source | Year 1 | Year 2 | Year 3 |
|---|---|---|---|
| New EU logos (conservative: 6 in Y1, 15 in Y2, 30 in Y3) | $180,000 | $600,000 | $1,500,000 |
| Expansion from existing EU customers | $30,000 | $120,000 | $300,000 |
| **Total Revenue** | **$210,000** | **$720,000** | **$1,800,000** |
| Less COGS (20% of revenue) | ($42,000) | ($144,000) | ($360,000) |
| **Net Contribution** | **$168,000** | **$576,000** | **$1,440,000** |

### 4. Financial Metrics

```
Cumulative net cash flow:
  Year 1:  $168,000 - $523,500 = -$355,500
  Year 2: -$355,500 + ($576,000 - $506,500) = -$286,000
  Year 3: -$286,000 + ($1,440,000 - $567,750) = +$586,250  ← Payback achieved

NPV (discount rate = 15%):
  Year 0:  -$523,500
  Year 1:  +$69,500 / 1.15 = +$60,435
  Year 2:  +$872,250 / 1.15^2 = +$659,546
  Total NPV = +$196,481  ← Positive = invest

IRR: ~32%
Payback period: ~2.4 years
```

### 5. Sensitivity / Risk Analysis

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| Can't hire fast enough (EU talent market tight) | 30% | Delay revenue by 3-6 months | Pre-identify candidates, use local recruiter |
| Currency risk (EUR weakens vs USD) | 20% | Revenue worth less in USD terms | Price in EUR, build in 10% FX buffer |
| Sales cycle longer than expected (cultural differences) | 25% | Lower year 1 revenue | 6-month checkpoint — if no pipeline, adjust |
| Compliance / regulatory surprise (GDPR, local employment law) | 10% | Legal costs, delays | Local counsel engaged from day 1 |

### 6. Compare Alternatives

Is there a cheaper/faster/better way? Always model at least:
- **Do nothing** — what happens if you don't invest?
- **Minimal version** — what's the smallest viable test?
- **The proposed investment** — the full plan

### 7. Recommendation

- **Go**: if NPV > 0 and payback < 3 years and aligns with strategy.
- **No go**: if NPV < 0 or payback > 3 years or unaligned with strategy.
- **Conditional go**: go, but with a hard checkpoint at [date / milestone].

## Output Format

- One-page business case summary (exec-friendly)
- Detailed cost-benefit model
- NPV, IRR, payback, break-even
- Risk matrix with mitigations
- Comparison to alternatives

## Done Criteria

The skill is complete when:
1. The full cost of the initiative (people + non-people, one-time + recurring) is modeled.
2. Benefits are projected with conservative, base, and aggressive scenarios.
3. NPV, IRR, and payback period are calculated.
4. Key risks are identified with probability, impact, and mitigation plans.
5. At least one alternative (e.g., do nothing, minimal version) is modeled and compared.
6. A clear go/no-go/conditional-go recommendation is provided.

## Pitfalls

1. **"Approve everything with positive NPV"** — startup capital is rationed, not abundant. Two positive-NPV projects competing for the same three engineers or the same $500k of cash require a capital allocation decision, not just a yes/no on each. Always force-rank, never approve in isolation.
2. **Using static discount rates for all projects** — a core product expansion with proven unit economics deserves a lower discount rate (10-12%) than a speculative new market entry with no validation data (20-25%). Risk-adjust the rate, not the cash flows.
3. **Modeling revenue linearly from day one** — "we'll hire 3 reps and each will close $X per month starting month 1." In reality: month 1-3 is training, month 4-6 is pipe building, month 7+ is when deals start closing. Model ramp curves, not step functions.
4. **Ignoring second-order costs** — hiring 5 engineers to build a new product isn't just the salary cost; you also need a PM, a designer, additional AWS spend, onboarding/tooling costs, and management overhead. The fully-loaded cost is typically 1.5-2x the salary line.
5. **Presenting a single-point estimate with no range** — "this project will deliver $2M in year 1 revenue" is less useful than "this project is expected to deliver $1.2M–$2.8M in year 1 revenue, with a 60% probability of exceeding $1.8M." Ranges invite the right conversation; point estimates invite false precision.

### Heuristics

- **15% discount rate is standard for startup projects**: reflects higher risk than public market (8-10%).
- **If it takes > 3 years to pay back, it's probably not worth it**: the startup will look completely different by then.
- **Always model at least one alternative**: "what if we did nothing?" and "what if we did the minimal version?"
- **Costs are usually right (or low), benefits are usually high**: the optimism bias is real. Apply a 20% haircut to all benefit estimates.

### Edge Cases

- **Intangible benefits** (brand, learning, strategic positioning): hard to quantify. List them separately from the financials. Don't inflate the numbers to justify them.
- **Opportunity cost**: what ELSE could you do with this money and people? Sometimes the best investment is doing nothing and preserving cash.
- **Sunk cost review**: revisit business cases 12 months in. If a case assumed $500k benefit and delivered $100k, why? Learn from it.

## Verification

Can you look at the business case and answer "If everything goes wrong, how much do we lose?" and "What's the single assumption that, if wrong, kills the case?" If the business case doesn't make those two things obvious, it's not done.

## Example

1. > **User**: "Should we open a sales office in London? Build me a business case."
   > **Expected behavior**: You define the hypothesis, model headcount + operational costs bottom-up (get real salary benchmarks for London), project conservative pipeline and revenue ramp with realistic sales cycle times, calculate NPV/IRR/payback, identify key risks (currency, hiring, compliance), compare against the alternative of hiring a remote rep or using a partner channel, and deliver a clear go/no-go with checkpoint milestones.

2. > **User**: "Compare these two investments: hiring 2 enterprise AEs vs doubling our paid marketing budget."
   > **Expected behavior**: You build two separate business case models with aligned assumptions, calculate NPV and payback for each, present a side-by-side comparison table, and force-rank them. You factor in relevant constraints — do we have enough SDR support for the AEs? Is there enough search volume for the paid budget? The recommendation includes which to fund first if you can only fund one.

3. > **User**: "Revisit the London office business case — it's been 18 months. Did it work?"
   > **Expected behavior**: You compare actual costs and revenue against the original business case projections, calculate variance, identify which assumptions were right (costs) and which were wrong (revenue ramp was 40% slower), extract lessons learned, and produce a one-page post-mortem that feeds into how future business cases are built.

## Linked Skills

- Revenue projections → `revenue-forecasting`
- Cost structure → `budget-creation-management`
- Efficiency & payback logic → `unit-economics-analysis`
- Downside scenarios → `scenario-planning`
- Strategic initiatives → `strategic-initiative-modeling`
- Headcount implications → `headcount-and-comp-planning`
