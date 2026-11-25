---
name: scenario-planning
description: Runs multi-scenario financial planning — best/base/worst case, sensitivity analysis, trigger events, and contingency planning for startup financial resilience. Use when the user mentions "scenario planning," "best case worst case," "sensitivity analysis," "what if revenue drops," "contingency plan," or asks about "how much runway each scenario gives us."
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [cfo, finance, scenario-planning, sensitivity-analysis, contingency-planning, risk-management]
related_skills: [revenue-forecasting, budget-creation-management, cash-forecasting, unit-economics-analysis, forecast-accuracy-tracking, risk-management]
inputs_required: [base-case-financial-model, key-driver-assumptions, cost-structure-fixed-vs-variable, external-factors]
deliverables: [three-scenario-pnl-and-cash-flow-models, sensitivity-tornado-chart, contingency-plans-at-3-levels]
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Scenario Planning

Build and compare multiple financial scenarios — best case, base case, and worst case. Run sensitivity analyses on key drivers, define trigger events that signal a scenario shift, and prepare contingency plans. Goal: the company is never surprised by the future because you've already modeled the possibilities.

## Purpose

Startups operate in extreme uncertainty — one key customer loss, a fundraising freeze, or an unexpected growth spike can change the trajectory overnight. This skill prepares the company for multiple futures by modeling scenarios, identifying what would trigger a shift, and pre-building contingency plans so decisions are made calmly in advance rather than frantically in a crisis.

## When to Use

- "Run scenario planning for next year"
- "Model best case / worst case / base case"
- "What if revenue drops 20%?"
- "Sensitivity analysis on growth rate"
- "When should we switch to our contingency plan?"
- "How much runway does each scenario give us?"

## Inputs Required

1. **Base case model** — the "most likely" forecast from `revenue-forecasting` and `budget-creation-management`.
2. **Key drivers** — revenue growth rate, churn rate, hiring velocity, gross margin, sales efficiency.
3. **External factors** — market conditions, competitive dynamics, regulatory changes.
4. **Cost structure** — fixed vs variable cost split, to understand what flexes and what doesn't.

## Quick Reference

| Scenario | Probability | Revenue vs Plan | Costs vs Plan | Focus |
|----------|-------------|-----------------|---------------|-------|
| Upside | 20% | +20-30% | +10-15% | Can we capture demand? |
| Base | 55% | Plan | Plan | Business as expected |
| Downside | 25% | −20-50% | −5-20% (flex only) | Can we survive? |

| Contingency Level | Reduction | Actions |
|-------------------|-----------|---------|
| Level 1: Trim | 5-10% | Pause hiring, cut events, renegotiate SaaS |
| Level 2: Reduce | 10-20% | Hiring freeze, marketing cuts, contractor reduction |
| Level 3: Survive | 20-30% | Layoffs, program cancellations, salary cuts |

## Procedure

### 1. Define the Three Core Scenarios

| Scenario | Probability | Revenue | Costs | When it Applies |
|---|---|---|---|---|
| **Base case** | 55% | Plan | Plan | Business as expected |
| **Upside case** | 20% | +20–30% vs plan | +10–15% (mostly variable) | Key deals close faster, product goes viral, market tailwind |
| **Downside case** | 25% | −20–50% vs plan | −5–20% (only variable/flex costs) | Recession, competitor launch, key customer loss, funding market freeze |

### 2. Identify Key Drivers to Vary

| Driver | Base Case | Upside | Downside | Impact |
|---|---|---|---|---|
| Revenue growth rate | 10% MoM | 12% MoM | 5% MoM | High |
| Gross margin | 80% | 82% | 75% | Medium |
| Sales rep ramp time | 6 months | 4 months | 9 months | High |
| New hire acceptance rate | 70% | 85% | 50% | Medium |
| Enterprise sales cycle | 90 days | 60 days | 150 days | High |
| Logo churn (monthly) | 2% | 1.5% | 4% | High |

### 3. Build the Scenario Models

For each scenario, produce:
- Revenue forecast (monthly, 24 months)
- OpEx forecast (monthly, by department)
- Cash flow forecast (weekly for 13 weeks, monthly after)
- Runway projection
- Key metrics dashboard

### 4. Run Sensitivity Analysis

For each key driver, calculate the impact on the most important numbers:

| Driver | Change | Impact on Year-End ARR | Impact on Cash at Year-End | Impact on Runway |
|---|---|---|---|---|
| Growth rate | ±1% MoM | ±$X | ±$Y | ±Z months |
| Churn rate | ±0.5% | ±$A | ±$B | ±C months |
| Gross margin | ±1% | ±$D | ±$E | ±F months |
| S&M spend | ±10% | ±$G | ±$H | ±I months |

Present as a tornado chart (the most impactful drivers at the top).

### 5. Define Contingency Triggers

Define specific, measurable triggers that would cause a shift to the downside scenario:

| Trigger | Threshold | Action |
|---|---|---|
| Revenue misses plan 2 months in a row | < 80% of plan | Freeze all non-essential hiring |
| Churn > 3% for 3 months | > 3% monthly | Emergency churn intervention taskforce |
| Cash runway drops below 9 months | < 9 months | Implement 20% cost reduction plan |
| Key customer churns | Top 3 customer leaves | 10% immediate OpEx cut |
| Fundraising market freezes | — | Cut burn to extend runway to 24+ months |

### 6. Pre-Build Contingency Plans at Three Levels

**Level 1: Trim (5-10% reduction)**
- Pause non-critical hiring
- Cut travel & events
- Renegotiate top 5 SaaS subscriptions
- No impact on core operations

**Level 2: Reduce (10-20% reduction)**
- Hiring freeze (except backfills for critical roles)
- Marketing spend cut 30%
- Contractor reduction
- Delay office expansion
- Start to feel it, but survivable

**Level 3: Survive (20-30% reduction)**
- Layoffs
- Major program cancellations
- Salary cuts
- Office closure / sublease
- Existential — only if the alternative is death

### 7. Compare & Recommend

Side-by-side comparison:

| Metric | Upside | Base | Downside (no cuts) | Downside (with L2 cuts) |
|---|---|---|---|---|
| Year-End ARR | $5.2M | $4.1M | $2.8M | $2.5M |
| Year-End Cash | $8.3M | $5.1M | $1.2M | $2.8M |
| Runway (months) | 36+ | 24 | 8 | 15 |
| Zero Cash Date | — | — | Mar 2027 | Aug 2027 |

## Output Format

- Three scenario P&L and cash flow models
- Sensitivity tornado chart
- Trigger dashboard: which triggers are currently "active"?
- Contingency plans at 3 levels
- Decision framework: which scenario are you in RIGHT NOW?

## Done Criteria

The skill is complete when:
1. Three scenarios (upside, base, downside) are modeled with distinct revenue and cost assumptions.
2. Sensitivity analysis is performed on at least 4 key drivers.
3. Trigger events are defined with specific, measurable thresholds and named owners.
4. Contingency plans are documented at all three levels (trim, reduce, survive).
5. A side-by-side comparison table shows runway and zero-cash dates for each scenario.

## Pitfalls

1. **Modeling risks independently** — treating a revenue shortfall, a fundraising freeze, and rising churn as isolated events when they're often correlated (e.g., a recession hits all three at once). Always stress at least one scenario where multiple levers break simultaneously.
2. **Over-focusing on the upside** — spending 80% of scenario-planning effort on the "what if everything goes right" case while the downside gets a cursory skim. The upside model should be your Saturday afternoon project; the downside model is your Monday morning priority.
3. **Vague triggers without owners** — "if things look bad, we'll cut costs." A trigger must specify: the metric, the threshold, the measurement period, the action, and **who owns the decision**. Every trigger needs a named owner.
4. **Modeling costs as fully flexible** — assuming you can cut OpEx by 30% overnight ignores notice periods, severance costs, contract break fees, and morale collapse. Build realistic ramp-down curves with cash costs for each level.
5. **Using scenario planning as a one-time exercise** — building beautiful three-scenario models for the board deck in November and never touching them again until next November. Scenarios are living documents. Review triggers monthly.

### Heuristics

- **"What's the worst that could happen, and can we survive it?":** the primary purpose of scenario planning. If the answer is no, reduce risk.
- **Downside scenarios are more important than upside ones**: the upside takes care of itself. Focus planning energy on the downside.
- **Triggers must be specific and measurable**: "if revenue looks weak" is useless. "If revenue is below 80% of plan for 2 consecutive months" is actionable.
- **Pre-negotiate the cuts**: the worst time to decide which 20% to cut is during the crisis. Decide now, execute if needed.

### Edge Cases

- **"Black swan" events** (pandemic, banking crisis): too rare to model precisely. Instead of modeling the event, model the effect: "What if revenue drops 50% overnight?" Test the plan against that.
- **Correlated risks**: a recession means lower revenue AND harder fundraising AND higher churn. Don't model them independently.
- **Good scenarios that require investment**: what if demand spikes? Do you have the cash and hiring capacity to capture it? That's a good problem to have, but still a problem.

## Verification

Can you answer "If revenue drops 30% next quarter, how much cash do we have and how long will it last?" without opening a spreadsheet? Can the CEO rattle off the three trigger thresholds that would activate contingency plans? If not, the scenario planning hasn't been internalized.

## Example

1. > **User**: "Run a full three-scenario analysis for next year — best, base, and worst case — and tell me how much runway we have in each."
   > **Expected behavior**: You load the base case revenue and cost models, create upside (+25% revenue, +12% costs) and downside (-35% revenue, -15% costs after flex) variants, produce monthly P&Ls and cash flow statements for each, calculate runway, and present a side-by-side comparison table with clear recommendation on which scenario you're closest to today.

2. > **User**: "What happens to our runway if we miss revenue by 20% for two quarters?"
   > **Expected behavior**: You apply a 20% haircut to the revenue forecast for the next two quarters, model which costs flex (variable marketing, hiring slowdown) vs stay fixed (existing headcount, office lease), recalculate the cash balance trajectory, and report the new zero-cash date with recommended contingency actions.

3. > **User**: "Define the triggers that should make us activate our contingency plan."
   > **Expected behavior**: You identify the 4-6 most critical leading indicators (revenue vs plan, churn rate, pipeline coverage, cash balance, fundraising timeline), set numerical thresholds for each, assign owners, and produce a trigger dashboard that can be reviewed at each monthly finance review.

## Linked Skills

- Base case revenue → `revenue-forecasting`
- Base case costs → `budget-creation-management`
- Cash impact of scenarios → `cash-forecasting`
- Unit economics under stress → `unit-economics-analysis`
- How good is the base case anyway? → `forecast-accuracy-tracking`
- Risk management broader → `risk-management`
