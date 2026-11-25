---
name: fundraising-financials
description: Build the financial models and narratives for fundraising — 3-statement projections, SaaS metrics, use of funds, valuation analysis, and investor Q&A prep. Use when the user asks about building a fundraising model, creating pitch deck numbers, modeling use of funds, valuation targets, or preparing for investor Q&A.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [cfo, finance, fundraising, financial-model, investor-qa]
related_skills:
  - revenue-forecasting
  - budget-creation-management
  - unit-economics-analysis
  - scenario-planning
  - cap-table-management
  - data-room-management
  - fundraising-process-management
inputs_required:
  - historical-financials-PL-balance-sheet-cash-flow-monthly-2-3-years
  - current-SaaS-metrics-ARR-MRR-growth-churn-NRR
  - revenue-and-budget-forecasts-from-linked-skills
  - cap-table-and-target-raise-info-round-amount-use-of-funds
deliverables:
  - three-statement-financial-model-with-SaaS-metrics-dashboard
  - use-of-funds-breakdown-with-hiring-plan
  - valuation-range-dilution-analysis-and-investor-QA-prep
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Fundraising Financials

Build the complete financial package for a fundraise — from the 3-statement model to the pitch deck numbers to the investor Q&A prep. Goal: every number a VC asks for is already modeled, stress-tested, and has a narrative behind it.

## Purpose

Investors invest in stories backed by numbers. A sloppy financial model or a vague use-of-funds slide is the fastest way to lose credibility. This skill produces the full financial package — 3-statement projections, SaaS metrics dashboard, valuation and dilution analysis, use of funds breakdown, and prepared Q&A answers — so the team walks into every investor meeting with confidence.

## When to Use

- "Build our fundraising financial model"
- "Create numbers for the pitch deck"
- "Model our use of funds"
- "What valuation should we target?"
- "Prepare for investor Q&A"
- "Project our Series A metrics"

## Inputs Required

1. **Historical financials** — P&L, balance sheet, cash flow (monthly for 2-3 years if available).
2. **Current SaaS metrics** — ARR, MRR, growth rate, churn, logo count, expansion revenue.
3. **Revenue forecast** — from `revenue-forecasting` or build as part of this skill.
4. **Budget** — current and planned from `budget-creation-management`.
5. **Cap table** — from `cap-table-management` for dilution modeling.
6. **Target raise info** — amount, round (seed/A/B), target use of funds.

## Quick Reference

| Metric | What It Tells Investors | Target for Fundraising |
|---|---|---|
| Rule of 40 | Growth rate + profit margin | > 40% for healthy SaaS |
| Burn multiple | Net burn / net new ARR | < 1.5x for fundraising; < 1x is efficient |
| Magic number | Net new ARR (quarter) / S&M spend (prior quarter) | > 1.0 means profitable scaling |
| ARR per employee | Total ARR / headcount | $150k-200k+ at Series A |
| Forward revenue multiple | Pre-money valuation / forward ARR | Seed: story; Series A: 10-30x; B: 8-20x |

## Procedure

### 1. Three-Statement Model

Build a monthly projection covering 3 years (past 12 months actuals + 36 months projected):

**Income Statement:**
- Revenue (with growth rate, seasonality)
- COGS (as % of revenue, by department)
- Gross Profit & Margin
- OpEx by department (R&D, S&M, G&A)
- EBITDA
- Net Income

**Balance Sheet:**
- Cash (from cash flow statement)
- AR (tied to DSO assumption)
- Fixed assets (net of depreciation)
- AP & Accruals (tied to DPO assumption)
- Deferred Revenue (tied to billing model)
- Debt
- Equity (including new raise)

**Cash Flow Statement:**
- Operating cash flow
- Investing cash flow
- Financing cash flow (the raise!)
- Ending cash balance

All three must articulate. Revenue in P&L → AR change on BS → Operating CF. Every line has a driver.

### 2. SaaS Metrics Dashboard

Include the metrics VCs care about most:

| Metric | Current | Year 1 Target | Year 2 Target | Year 3 Target |
|---|---|---|---|---|
| ARR | $1.2M | $3.0M | $7.5M | $18M |
| ARR Growth Rate | 80% YoY | 150% | 150% | 140% |
| Net Revenue Retention | 110% | 115% | 120% | 120% |
| Gross Margin | 78% | 80% | 82% | 83% |
| CAC Payback (months) | 14 | 12 | 10 | 8 |
| LTV / CAC | 4.2x | 5.5x | 7x | 9x |
| Burn Multiple | 1.8x | 1.2x | 0.8x | 0.5x |
| Magic Number | 0.7 | 0.9 | 1.1 | 1.3 |

### 3. Use of Funds

Model where the money goes:

| Category | Allocation | % |
|---|---|---|
| Engineering & Product (hiring) | $4.5M | 38% |
| Sales & Marketing (hiring + spend) | $4.0M | 33% |
| G&A (ops, legal, finance) | $1.5M | 13% |
| Infrastructure & tools | $1.0M | 8% |
| Buffer / contingency | $1.0M | 8% |
| **Total** | **$12.0M** | **100%** |

Show the hiring plan: headcount today → 12-month target by department.

### 4. Valuation & Dilution Analysis

**Revenue multiple method:**
- Find comparable public & private company multiples.
- Apply a range (e.g., 10–20x forward ARR) to your forward ARR.
- Propose a valuation range: Low / Mid / High.

**Dilution:**
- Current fully diluted shares: X
- New shares issued: Y
- Option pool increase (if needed): Z
- Post-money dilution for existing shareholders: (Y + Z) / (X + Y + Z)

### 5. Pitch Deck Numbers (1–2 slides only)

- Revenue chart: historical + projected (3 years)
- Key metrics: ARR, growth rate, NRR, gross margin, burn multiple
- Unit economics: CAC, LTV, payback
- Milestones the raise will achieve

### 6. Investor Q&A Prep

Prepare answers for the hardest questions:

- "Your growth is decelerating — why, and how does this raise change that?"
- "Your CAC payback is > 12 months. What's your plan to improve it?"
- "You're at 75% gross margin — can you get to 80%+ and how?"
- "What's your biggest customer concentration risk?"
- "Your burn multiple is 2x — when does it come below 1x?"
- "Why this amount? Why now?"

## Output Format

- Three-statement model (Markdown table + summary)
- SaaS metrics dashboard
- Use of funds breakdown with hiring plan
- Valuation range and dilution analysis
- Pitch deck financial slide content
- Top 10 investor Q&A with prepared answers

## Done Criteria

The skill is complete when:
1. Three-statement model (P&L, balance sheet, cash flow) is built and articulated — all three statements tie together
2. SaaS metrics dashboard is populated with current, year-1, year-2, and year-3 targets
3. Use of funds is modeled with hiring plan by department
4. Valuation range is proposed with comparable company analysis
5. Dilution impact is modeled for existing shareholders
6. Top 10 investor Q&A questions have prepared answers

## Pitfalls

- **Building a model that doesn't articulate**: if revenue growth on the P&L doesn't flow through to AR changes on the balance sheet and operating CF on the cash flow statement, the model is broken. Every line must have a driver and every statement must tie.
- **Presenting only base case**: investors will ask "what if?" If you haven't modeled downside scenarios, you haven't done the work. Always include bear and upside cases.
- **Ignoring dilution in valuation discussions**: a high pre-money with big option pool increase may be a lower effective valuation. Always show the pro forma cap table.
- **Fudging the use of funds**: generic line items like "growth" without a hiring plan signal that the team hasn't thought through how they'll deploy capital.
- **Over-promising on metrics**: projecting 200% growth in year 3 when you're at 50% in year 1 destroys credibility. Sensible deceleration is expected.

## Verification

Can you answer "what is our projected ARR in year 3 and what drives it?" from the model? Does the balance sheet tie to the cash flow statement? Can an investor see exactly where their capital goes (use of funds)? Are prepared Q&A answers ready for the 5 hardest questions an investor might ask? If not, the financial package is incomplete.

## Example

**User prompt**: "Build our fundraising financial model."
**What should happen**: Build the three-statement model with monthly projections covering 3 years, populate the SaaS metrics dashboard with current and target metrics, produce the use of funds breakdown with hiring plan, run valuation and dilution analysis, and prepare pitch deck financial slide content and investor Q&A answers.

**User prompt**: "What valuation should we target for our Series A?"
**What should happen**: Analyze comparable public and private company revenue multiples, apply appropriate multiples to forward ARR projections, propose a low/mid/high valuation range, model dilution impact at each valuation, and recommend a target range with rationale.

## Linked Skills

- Revenue projections → `revenue-forecasting`
- Expense modeling → `budget-creation-management`
- Unit economics detail → `unit-economics-analysis`
- Scenario modeling → `scenario-planning`
- Dilution & cap table → `cap-table-management`
- Store in data room → `data-room-management`
- Fundraise timeline → `fundraising-process-management`
