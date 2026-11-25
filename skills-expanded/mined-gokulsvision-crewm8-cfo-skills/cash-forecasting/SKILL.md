---
name: cash-forecasting
description: Builds and maintains a 13-week rolling cash forecast — models inflows, outflows, scenario analysis, and forecast-vs-actual accuracy tracking. Use when the user mentions cash forecast, 13-week forecast, liquidity projection, cash runway, or asks about modeling cash under different scenarios or when cash runs out.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [cfo, finance, cash, treasury, cash-forecast, scenario-planning]
related_skills:
  - cash-monitoring
  - accounts-receivable-management
  - accounts-payable-management
  - revenue-forecasting
  - budget-creation-management
  - working-capital-optimization
inputs_required:
  - current-cash-position-from-cash-monitoring
  - revenue-forecast-from-revenue-forecasting-or-manual
  - budget-expense-forecast-from-budget-creation-management
  - ap-AR-and-payroll-schedules
  - tax-payment-and-debt-service-calendars
deliverables:
  - 13-week-cash-forecast-table-markdown-or-csv
  - scenario-comparison-base-bear-upside
  - zero-cash-date-and-runway-projection
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Cash Forecasting

Build and maintain a 13-week rolling cash flow forecast — the most important financial model for an early-stage startup. Model every expected inflow and outflow week by week, run scenarios, and track accuracy.

## Purpose

A cash forecast is the bridge between today's cash position and tomorrow's financial reality. Without it, startups fly blind — running out of cash is the #1 cause of startup failure. This skill produces the 13-week rolling forecast that tells leadership exactly when cash will run out under multiple scenarios, so they can act before it's too late.

## When to Use

- "Build a 13-week cash forecast"
- "Update the cash forecast"
- "Model our cash runway under different scenarios"
- "How long until we run out of money at current burn?"
- "What happens to cash if revenue drops 20%?"

## Inputs Required

1. **Current cash position** — get from `cash-monitoring` skill.
2. **Revenue forecast** — get from `revenue-forecasting` skill or provide manually.
3. **Budget / expense forecast** — get from `budget-creation-management` or provide manually.
4. **AP schedule** — upcoming vendor payments from `accounts-payable-management`.
5. **AR schedule** — expected customer payments from `accounts-receivable-management`.
6. **Payroll calendar** — pay dates, amounts from `payroll-processing`.
7. **Tax payment calendar** — from `tax-compliance-management`.
8. **Debt service schedule** — if any loans/credit facilities.

## Quick Reference

| Concept | Formula | Purpose |
|---------|---------|---------|
| Net cash flow (week N) | Total inflows - Total outflows | Weekly cash change |
| Ending cash (week N) | Ending cash (N-1) + Net cash flow (N) | Running cash balance |
| Zero cash date | Earliest week ending cash goes negative | Single most important fundraising trigger |
| Months of runway | Ending cash / avg monthly net burn | Time until cash exhaustion |
| Cash low point | Lowest ending cash in 13 weeks | Minimum liquidity planning |

## Procedure

### 1. Weekly Inflow Modeling

For each of the next 13 weeks:

| Category | Source |
|---|---|
| Customer receipts | AR aging + revenue forecast. Use historical collection timing per customer segment. |
| Stripe/payment processor transfers | Typically 2–7 day lag from customer payment. |
| Interest income | Current yield on cash balances. |
| Tax refunds / credits | If applicable. |
| Other inflows | Grants, one-time payments, etc. |

- **Conservative assumption**: assume new revenue collects in 30–45 days, not net-30 terms.
- **Enterprise assumption**: 45–60 day collection. Be pessimistic.

### 2. Weekly Outflow Modeling

For each of the next 13 weeks:

| Category | Timing |
|---|---|
| Payroll | Exact pay dates. Salaried is predictable. |
| Contractor payments | Due dates from AP. |
| Rent/office | 1st of the month. |
| Software subscriptions | Recurring — map to billing dates. |
| Professional services | Invoice dates + net-30. |
| Taxes | Quarterly estimated dates (Apr 15, Jun 15, Sep 15, Jan 15). |
| Sales commissions | End of month following deal close. |
| Other variable | Travel, events, recruiting, equipment — use budget ÷ 52 weeks. |

### 3. Net Cash Flow Per Week

```
Net cash flow (week N) = Total inflows (week N) − Total outflows (week N)
Ending cash (week N)   = Ending cash (week N-1) + Net cash flow (week N)
```

### 4. Build the Forecast Table

| Week Starting | Inflows | Outflows | Net | Ending Cash | Notes |
|---|---|---|---|---|---|
| 2026-04-27 | $45,000 | $68,000 | −$23,000 | $2,824,000 | Payroll week + AWS bill |
| 2026-05-04 | $32,000 | $22,000 | +$10,000 | $2,834,000 | |
| ... | ... | ... | ... | ... | |
| 2026-07-20 | ... | ... | ... | $2,740,000 | End of 13 weeks |

### 5. Scenario Analysis

Run at least 3 scenarios:

**Base case**: most likely. 80% confidence.
**Bear case**: revenue drops 20%, collections slow by 15 days, costs unchanged.
**Upside case**: revenue beats by 15%, new logo acceleration.

Present all three ending cash positions and the date each would hit zero (if any).

### 6. Key Metrics

- **Zero cash date**: the earliest week ending cash goes negative. This is the single most important number.
- **Months of runway**: ending cash ÷ average monthly net burn.
- **Cash low point**: the lowest ending cash balance during the 13 weeks.
- **Largest outflow week**: plan liquidity around it.

## Output Format

- 13-week cash forecast table (Markdown or CSV)
- Summary dashboard: starting cash, ending cash, net change, zero-cash date
- Scenario comparison table
- Weekly burn rate trend
- Top 3 risks to the forecast with mitigations

## Done Criteria

The skill is complete when:
1. Weekly inflows and outflows are modeled for all 13 weeks
2. Net cash flow and ending cash are calculated for each week
3. At least three scenarios (base, bear, upside) are modeled and compared
4. Zero-cash date and months of runway are computed for each scenario
5. Cash low point and largest outflow week are identified
6. Top 3 risks to the forecast with mitigations are documented

## Pitfalls

- **Setting and forgetting the forecast**: a 13-week forecast built once and never updated becomes dangerous fiction within 2–3 weeks. Cash timing assumptions (collection dates, payment dates) shift constantly and the forecast must reflect reality, not a static plan.
- **Forecasting revenue at the monthly level**: weekly granularity is mandatory for cash forecasting. A $100k month with all invoices due on the 30th has a very different cash profile than the same $100k spread across four weekly payments. Monthly aggregation hides intra-month liquidity crunches.
- **Ignoring payment processor settlement lags**: modeling customer payments as "received" on the day the customer pays via Stripe ignores the 2–7 day settlement delay. This can cause a forecast to show cash available 1–2 weeks before it actually hits the bank account.
- **Modeling only base case**: presenting a single forecast line without downside scenarios gives stakeholders a false sense of certainty. Every cash forecast must include at minimum a base, bear, and upside case with explicit assumptions for each.
- **Treating all outflows as evenly distributed**: spreading annual software costs evenly across 52 weeks or assuming all vendor payments fall neatly on the 30th of the month fails to capture real cash lumpiness — payroll weeks, quarterly tax dates, and annual renewal spikes must be modeled at their actual dates.

## Verification

Can you answer "when does the company run out of cash in the base case?" from this forecast? Can you answer "what's the impact on zero-cash date if revenue drops 20%?" Are the assumptions behind each scenario explicitly documented? If not, the forecast is incomplete.

## Example

**User prompt**: "Build a 13-week cash forecast starting from our current position."
**What should happen**: Pull the current cash position from `cash-monitoring`, gather AP/AR schedules, revenue forecast, and expense budget from linked skills, model weekly inflows and outflows for the next 13 weeks, produce the forecast table with key metrics (ending cash, zero-cash date, runway), and generate base/bear/upside scenarios.

**User prompt**: "What happens to our cash if we lose our 3 largest customers next quarter?"
**What should happen**: Take the existing 13-week forecast, remove the revenue from the 3 largest customers, model the downstream impact on cash position week-by-week, recalculate the zero-cash date and runway, and present the scenario comparison showing the delta from the base case with specific risk mitigations.

**User prompt**: "Update the cash forecast for the new hires starting next month."
**What should happen**: Incorporate the new hire payroll costs into the outflow model with the appropriate start-date lag (typically week 3–4 for first paycheck), recalculate the 13-week forecast, highlight the impact on cash low point and ending cash, and flag whether the runway threshold crosses any severity boundaries.

## Linked Skills

- Get current cash → `cash-monitoring`
- Model inflows from customers → `accounts-receivable-management`
- Model outflows to vendors → `accounts-payable-management`
- Revenue assumptions → `revenue-forecasting`
- Expense assumptions → `budget-creation-management`
- Payment timing optimization → `working-capital-optimization`
