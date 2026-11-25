---
name: budget-creation-management
description: Creates and manages operating budgets — annual plans, quarterly refreshes, and rolling forecasts at department-level granularity, with variance tracking and budget-vs-actual analysis. Use when the user mentions "create a budget," "annual plan," "OpEx run-rate," "departmental budget," "budget vs actuals," "re-forecast," or asks about "allocating budget to departments."
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [cfo, finance, budgeting, opex, variance-analysis, financial-planning]
related_skills: [revenue-forecasting, headcount-and-comp-planning, cash-forecasting, scenario-planning, forecast-accuracy-tracking]
inputs_required: [historical-actuals, headcount-plan, revenue-forecast, strategic-priorities, runway-target]
deliverables: [annual-budget, budget-vs-actual-tracker, variance-commentary, runway-projection]
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Budget Creation & Management

Build and maintain the company's operating budget — annual plans, quarterly refreshes, and rolling forecasts. Budget by department, track variances, and manage budget vs actuals. Goal: every dollar has an owner, a purpose, and a plan.

## Purpose

Every startup dollar is scarce and every expense needs justification. This skill ensures budgets are built from scratch (zero-based), aligned with strategic priorities, and managed actively through variance tracking and re-forecasting. It solves the problem of budget drift — where last year's spend becomes next year's baseline without questioning whether it's still the right allocation.

## When to Use

- "Create our annual budget"
- "Build a departmental budget"
- "What's our OpEx run-rate?"
- "Review budget vs actuals"
- "Re-forecast based on new information"
- "Allocate budget to departments"

## Inputs Required

1. **Historical actuals** — P&L by department (monthly, last 12–24 months).
2. **Headcount plan** — current and projected from `headcount-and-comp-planning`.
3. **Revenue forecast** — from `revenue-forecasting` (drives variable costs).
4. **Strategic priorities** — what the company is trying to achieve (drives spend allocation).
5. **Runway target** — months of cash to target (drives total spend envelope).

## Quick Reference

| Concept | Description | Key Ratio |
|---------|-------------|-----------|
| OpEx envelope | Total spend available after gross margin minus target burn | Revenue × Gross Margin % − Target Monthly Burn |
| Zero-based budgeting | Build each budget from scratch, not from last year's numbers | Don't use "last year + 20%" |
| Department benchmarks | Typical % of total OpEx by stage | R&D 30-60%, S&M 15-45%, G&A 10-25% |
| Variance threshold | Flag when actuals deviate from budget | > 10% or > $5,000 |
| Contingency | Holdback for unknowns | 10-20% of total budget |

## Procedure

### 1. Set the Top-Down Envelope

```
Revenue:                       $X (from revenue-forecasting)
Gross Margin:                  $Y (revenue × margin %)
Target Burn (monthly):         $Z (based on runway target)
Available OpEx:                $Y - $Z
```

The total OpEx must fit within the available envelope. If it doesn't, either: grow revenue faster, improve margins, cut burn, or raise more money.

### 2. Build Department Budgets (Zero-Based Approach)

Don't just add 20% to last year. Build from scratch:

For each department:
1. What are you trying to achieve? (OKRs, KPIs)
2. What resources do you need to achieve it?
3. What's the minimum viable budget? (must-do)
4. What would an extra 50% get you? (growth lever)
5. What would you cut if cash got tight? (triage list)

Work with the department head:
1. Review last quarter's actuals.
2. Map headcount to hiring plan.
3. Project non-headcount spend (use run-rate for recurring, specific for one-time).
4. Flag any step-function changes (new office, major conference, tool migration).

#### Department Budget Template

| Line Item | Jan | Feb | Mar | Q1 Total | Q2 | ... | FY Total |
|---|---|---|---|---|---|---|---|
| **Headcount** | | | | | | | |
| Salaries + Benefits | | | | | | | |
| Contractors | | | | | | | |
| Recruiting | | | | | | | |
| Travel & Entertainment | | | | | | | |
| **Non-Headcount** | | | | | | | |
| Software & Subscriptions | | | | | | | |
| Marketing Spend | | | | | | | |
| Events & Conferences | | | | | | | |
| Professional Services | | | | | | | |
| Office & Facilities | | | | | | | |
| Equipment | | | | | | | |
| Training & Development | | | | | | | |
| Other | | | | | | | |
| **Total Department Spend** | | | | | | | |

#### Department Benchmarks (% of Total OpEx)

Typical SaaS startup allocation:

| Department | Early (pre-PMF) | Growth (post-Series A) | Scale (Series B+) |
|---|---|---|---|
| R&D / Engineering | 40-60% | 35-45% | 30-40% |
| Sales & Marketing | 15-25% | 30-40% | 35-45% |
| G&A | 15-25% | 10-20% | 10-15% |

### 3. Consolidate & Stress Test

- Does the total budget produce the right runway?
- Are department allocations in line with benchmarks?
- Is headcount growth sustainable? (Can recruiting actually hire this fast?)
- Are there any "cliffs" (large one-time expenses in a single month)?

### 4. Budget Approval & Lock

Present the consolidated budget to the CEO/board. Once approved, lock it as the plan of record.

### 5. Ongoing Management

**Monthly:**
- Budget vs actual by department.
- Flag variances > 10% or > $5,000.
- Each department head explains material variances.

**Quarterly:**
- Re-forecast based on actuals and new information.
- Adjust the remaining months, don't re-litigate the past.

## Output Format

- Annual budget (monthly × department)
- Budget vs actual tracker
- Variance commentary by department
- Runway projection based on budget

## Done Criteria

The skill is complete when:
1. The top-down OpEx envelope is set and aligned with runway targets.
2. Each department budget is built zero-based with department head input.
3. The consolidated budget is stress-tested against hiring velocity and cash constraints.
4. Variance thresholds are defined and tracking mechanisms are in place.
5. The budget is approved and locked as the plan of record.

## Pitfalls

1. **"Last year + 20%" incremental budgeting** — copying the prior period and scaling by a flat percentage destroys accountability and misses structural shifts in the business. Always zero-base.
2. **Treating all costs as fixed** — modeling cloud hosting, payment processing, and variable marketing as fixed line items leads to gross margin surprises when revenue scales.
3. **Building budgets without department head input** — a budget imposed by finance that the VP of Sales never reviewed won't be owned, won't be accurate, and won't be respected.
4. **Ignoring hiring velocity constraints** — budgeting for 5 new hires per month when recruiting's actual throughput is 2 creates a phantom underspend. Cap hiring projections at realistic throughput.
5. **No contingency line** — every startup budget needs a 10-20% holdback for unknowns. A budget that allocates every dollar to the penny is a budget that will be broken by the first surprise.

### Heuristics

- **Build for the most likely case, have a contingency for the worst case**: 80% confidence budget + a 10-20% contingency line.
- **Hiring is almost always slower than planned**: a hiring plan that says "hire 3 engineers per month" will probably do 1.5. Model this.
- **Non-headcount expenses are stickier than you think**: cutting SaaS tools or travel budgets takes 2-3 months to show up. Plan accordingly.
- **Marketing spend is the most flexible lever**: it's easy to turn on/off. Model it as a variable, not fixed, line item.
- **Budget owners must buy in**: if the VP of Sales didn't help build the sales budget, they won't feel accountable to it.

### Edge Cases

- **Hypergrowth**: if growing > 10% MoM, monthly budgets can't keep up. Use rolling 3-month forecasts.
- **New departments**: when adding a function (e.g., first sales hire), don't just add salary — add tools, travel, events, onboarding costs.
- **Office moves / expansions**: often the largest single line item. Model as a project budget separate from the recurring OpEx.
- **Currency exposure**: if paying employees/vendors in multiple currencies, build in an FX buffer (3-5%).

## Verification

Can you answer "What's our total OpEx spend this quarter vs budget?" for each department? Can you explain every variance > 10%? Are the assumptions in the budget still valid given what you know today? If not, the budget is already stale.

## Example

1. > **User**: "Create our annual operating budget for next fiscal year, starting with the revenue forecast, then build departmental budgets zero-based."
   > **Expected behavior**: You load the revenue forecast, set the top-down OpEx envelope, then walk through each department (R&D, S&M, G&A) building from headcount outward. Outputs a monthly × department budget with benchmarks and a runway projection.

2. > **User**: "Review Q2 budget vs actuals and tell me why we're off."
   > **Expected behavior**: You compare budget vs actual line items by department, flag material variances (>10% or >$5k), surface commentary from each department head, and highlight patterns — e.g., hiring running at 60% of plan, marketing overspend from an unplanned conference.

3. > **User**: "Re-forecast the rest of the year based on what actually happened in Q1."
   > **Expected behavior**: You take Q1 actuals as the new baseline, adjust remaining months' projections (don't re-litigate Q1), update runway math, and flag any assumptions that need revising — e.g., slower hiring pace, higher AWS costs.

## Linked Skills

- Revenue projections → `revenue-forecasting`
- Headcount & comp assumptions → `headcount-and-comp-planning`
- Cash impact → `cash-forecasting`
- Scenario modeling → `scenario-planning`
- Track budget accuracy → `forecast-accuracy-tracking`
