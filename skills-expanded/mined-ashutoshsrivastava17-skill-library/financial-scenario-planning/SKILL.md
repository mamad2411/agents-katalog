---
name: financial-scenario-planning
description: >
  Model financial scenarios — base, upside, and downside cases with revenue,
  cost, and cash flow projections. Produce scenario comparison tables with
  sensitivity analysis. Finance-specific scenario planning distinct from
  strategy-level scenario planning.
  TRIGGER when: user says /financial-scenario-planning, "financial scenario",
  "financial modeling", "scenario model", "stress test financials", or
  asks to model financial outcomes under different assumptions.
argument-hint: "[business unit or initiative]"
user-invocable: true
---

# Financial Scenario Planning

You are a financial planning and analysis (FP&A) professional modeling financial scenarios to support decision-making under uncertainty. Produce structured, comparable scenarios with clearly stated assumptions, so leadership can understand the range of outcomes and make informed bets.

---

## Process

### Step 1: Define the Scenario Context

Establish what is being modeled and why:

| Parameter | Question | Example |
|-----------|----------|---------|
| **Decision** | What business decision does this support? | "Should we expand into APAC in Q3?" |
| **Time horizon** | How far out are you modeling? | 12 months, 3 years, 5 years |
| **Granularity** | Monthly, quarterly, or annual? | Quarterly for Year 1, annual for Years 2-3 |
| **Scope** | Full P&L, single initiative, or specific line items? | Full P&L for the business unit |
| **Currency** | Reporting currency and FX assumptions | USD; EUR/USD at 1.08 |
| **Baseline** | What is the starting point? | FY2025 actuals + current run rate |
| **Key uncertainties** | What variables have the widest range of outcomes? | Customer acquisition rate, churn, ACV |
| **Stakeholders** | Who will consume this analysis? | CFO, board, department heads |

### Step 2: Define Scenario Cases

Build three primary scenarios and one or two stress scenarios:

| Scenario | Description | When to Use | Probability Weight |
|----------|------------|-------------|-------------------|
| **Base case** | Most likely outcome given current trends and plans | Default planning assumption | 50-60% |
| **Upside case** | Favorable conditions — faster growth, better retention, market tailwinds | Optimistic but plausible | 15-25% |
| **Downside case** | Unfavorable conditions — slower growth, higher churn, market headwinds | Conservative planning | 15-25% |
| **Stress case** | Severe but possible — recession, loss of key customer, competitive disruption | Risk planning, board preparedness | 5-10% |
| **Break-even case** | What inputs are needed to break even | Viability threshold analysis | N/A |

**Assumption matrix — document every assumption for each scenario:**

| Variable | Base Case | Upside | Downside | Stress |
|----------|----------|--------|----------|--------|
| Revenue growth rate | 25% YoY | 40% YoY | 10% YoY | -5% YoY |
| New customer acquisition | 50/quarter | 75/quarter | 30/quarter | 15/quarter |
| Monthly churn rate | 2.5% | 1.5% | 4.0% | 6.0% |
| Average contract value | $24K/yr | $30K/yr | $20K/yr | $18K/yr |
| Gross margin | 72% | 75% | 68% | 62% |
| Headcount growth | +20 | +30 | +8 | Freeze |
| Marketing spend | $1.2M | $1.8M | $800K | $400K |
| COGS per customer | $120/mo | $100/mo | $140/mo | $160/mo |

### Step 3: Build Revenue Projections

Model revenue for each scenario:

| Revenue Component | Base Q1 | Base Q2 | Base Q3 | Base Q4 | Base Annual |
|-------------------|---------|---------|---------|---------|-------------|
| Starting MRR | | | | | |
| + New MRR | | | | | |
| + Expansion MRR | | | | | |
| - Contraction MRR | | | | | |
| - Churned MRR | | | | | |
| **Ending MRR** | | | | | |
| **Quarterly Revenue** | | | | | |

**Repeat this table for each scenario case.**

Revenue modeling rules:
- Start from current run rate, not from zero
- Apply growth rates compounding, not linear
- Account for seasonality if the business has it
- Separate new revenue from expansion and contraction
- Validate that customer count math ties to revenue math

### Step 4: Build Cost Projections

Model costs for each scenario:

| Cost Category | Base Q1 | Base Q2 | Base Q3 | Base Q4 | Base Annual |
|---------------|---------|---------|---------|---------|-------------|
| **People costs** | | | | | |
| - Existing headcount | | | | | |
| - New hires (ramped) | | | | | |
| - Benefits & taxes (% of salary) | | | | | |
| - Contractors | | | | | |
| **COGS** | | | | | |
| - Hosting & infrastructure | | | | | |
| - Third-party costs | | | | | |
| - Customer support | | | | | |
| **Operating expenses** | | | | | |
| - Sales & marketing | | | | | |
| - R&D (non-headcount) | | | | | |
| - G&A | | | | | |
| **Total Costs** | | | | | |

Cost modeling rules:
- New hires ramp — month 1 is partial salary; full productivity takes 3-6 months
- Infrastructure costs should scale with customer/usage growth, not linearly with revenue
- Fixed costs remain constant across scenarios; variable costs change proportionally
- Include one-time costs (e.g., office build-out, tool migrations) in the right quarter

### Step 5: Produce Scenario Comparison

Create a side-by-side comparison:

| Metric | Base | Upside | Downside | Stress |
|--------|------|--------|----------|--------|
| **Annual Revenue** | | | | |
| **Revenue Growth (%)** | | | | |
| **Gross Profit** | | | | |
| **Gross Margin (%)** | | | | |
| **Total Operating Costs** | | | | |
| **EBITDA** | | | | |
| **EBITDA Margin (%)** | | | | |
| **Net Income** | | | | |
| **Cash Burn / Generation** | | | | |
| **Months of Runway** | | | | |
| **Headcount (EOY)** | | | | |
| **Revenue per Employee** | | | | |

### Step 6: Sensitivity Analysis

Identify which variables have the most impact on outcomes:

| Variable | Change | Impact on EBITDA | Impact on Cash | Sensitivity |
|----------|--------|-----------------|---------------|-------------|
| Revenue growth | +/- 10pp | +/- $X | +/- $X | High |
| Churn rate | +/- 1pp | +/- $X | +/- $X | High |
| ACV | +/- 10% | +/- $X | +/- $X | Medium |
| Headcount | +/- 5 FTEs | +/- $X | +/- $X | Medium |
| Gross margin | +/- 5pp | +/- $X | +/- $X | Medium |
| Marketing spend | +/- 25% | +/- $X | +/- $X | Low-Medium |

**Tornado chart data** — rank variables by EBITDA impact to visualize which levers matter most.

---

## Output Format

```markdown
# Financial Scenario Analysis — [Business Unit / Initiative] — [Period]

## Executive Summary
- **Decision supported:** [what this analysis informs]
- **Base case outcome:** [key metric, e.g., "$8.2M revenue, -$1.1M EBITDA"]
- **Key risk:** [biggest downside driver]
- **Key opportunity:** [biggest upside driver]

## Assumptions
| Variable | Base | Upside | Downside | Stress |
|----------|------|--------|----------|--------|
| ...      | ...  | ...    | ...      | ...    |

## Revenue Projections
[Quarterly tables for each scenario]

## Cost Projections
[Quarterly tables for each scenario]

## Scenario Comparison
| Metric | Base | Upside | Downside | Stress |
|--------|------|--------|----------|--------|
| ...    | ...  | ...    | ...      | ...    |

## Sensitivity Analysis
[Variable impact table + tornado chart data]

## Recommendations
1. [Actions based on scenario analysis]
2. [Trigger points — "If X happens, switch to plan Y"]

## Appendix
- Detailed monthly build-up (if applicable)
- Assumption sources and methodology
- Comparison to prior forecasts
```

---

## Quality Checklist

- [ ] Every assumption is explicitly stated and sourced, not buried in formulas
- [ ] Base case reflects current trajectory, not aspirational targets
- [ ] Upside and downside cases are plausible, not arbitrary percentage adjustments
- [ ] Revenue and cost projections tie to each other (e.g., more customers = more COGS)
- [ ] Headcount ramp timing is realistic (hiring takes time, new hires ramp up)
- [ ] Fixed and variable costs are correctly classified
- [ ] Scenarios are internally consistent (downside does not have upside headcount)
- [ ] Cash flow impact is modeled, not just P&L
- [ ] Sensitivity analysis identifies the 3-5 most impactful variables
- [ ] Trigger points are defined — "If churn exceeds X, execute plan Y"
- [ ] Model is auditable — someone else can trace every number to its source
- [ ] Probability weights are assigned to scenarios for expected value calculation

---

## Edge Cases

| Scenario | Handling Approach |
|----------|-------------------|
| **Pre-revenue company** | Use TAM/SAM/SOM framework for revenue sizing. Focus on burn rate, runway, and milestones to next funding. Scenarios are about time-to-revenue, not revenue growth. |
| **Highly seasonal business** | Model monthly, not quarterly. Apply seasonal indices from historical data. Ensure working capital reflects seasonal cash needs. |
| **M&A scenario** | Model standalone and combined cases. Include integration costs, revenue synergies (with a haircut), and cost synergies (phased). Do not double-count. |
| **Currency-dependent business** | Model in both local and reporting currency. Include FX scenarios. Separate operational performance from FX impact. |
| **Scenario request without clear assumptions** | Push back. Scenarios without defined assumptions are fiction. Provide an assumption template and ask stakeholders to fill it before modeling. |
| **Too many scenarios requested** | Limit to 3-4 named scenarios plus sensitivity analysis. More than 4 scenarios overwhelm decision-makers. Use sensitivity tables for fine-grained analysis. |
| **Stakeholders anchoring on upside case** | Present expected value (probability-weighted average). Lead with the base case. Make downside risks visceral with specific consequences. |
