---
name: cash-flow-forecast
description: "Projects monthly cash flow for 3-12 months from revenue and expense inputs with scenario modeling and runway calculations. Use when a user needs to plan spending, evaluate whether they can afford a hire or investment, or wants to understand when they'll run out of (or accumulate) cash."
---

# Cash Flow Forecast

## When to Use This Skill

- Planning a major business expense (hire, equipment, marketing spend)
- Evaluating whether revenue supports current burn rate
- Preparing financial projections for a loan or investor
- Seasonal business planning (anticipating slow months)
- Answering "how long can I sustain this?" or "when do I break even?"

**DISCLAIMER: This tool provides estimates for planning purposes. It is not financial advice. Consult a qualified accountant or financial advisor for formal financial planning.**

## Core Principle

**CASH FLOW IS NOT PROFIT. A profitable business can run out of cash. This forecast tracks when money actually enters and leaves your bank account.**

## Workflow

### Step 1: Gather Financial Inputs

Ask the user:

1. Current cash on hand (bank balance)
2. Monthly revenue sources and amounts (be specific: retainer clients, product sales, subscriptions)
3. Monthly fixed expenses (rent, software, subscriptions, salaries)
4. Monthly variable expenses (ads, materials, contractors)
5. Any upcoming one-time expenses or revenue (equipment purchase, tax payment, contract signing)
6. Forecast period (default: 6 months)

**Minimum needed: questions 1, 2, and 3.**

### Step 2: Build the Forecast Table

Create a month-by-month table:

| | Month 1 | Month 2 | Month 3 | Month 4 | Month 5 | Month 6 |
|---|---------|---------|---------|---------|---------|---------|
| **Starting Cash** | | | | | | |
| Revenue Line 1 | | | | | | |
| Revenue Line 2 | | | | | | |
| **Total Revenue** | | | | | | |
| Fixed Expense 1 | | | | | | |
| Fixed Expense 2 | | | | | | |
| Variable Expenses | | | | | | |
| One-Time Expenses | | | | | | |
| **Total Expenses** | | | | | | |
| **Net Cash Flow** | | | | | | |
| **Ending Cash** | | | | | | |

### Step 3: Calculate Key Metrics

- **Monthly Burn Rate:** Average total expenses per month
- **Revenue Coverage Ratio:** Total revenue / total expenses (above 1.0 = cash positive)
- **Cash Runway:** Starting cash / (monthly expenses - monthly revenue) = months until $0
- **Break-Even Month:** First month where cumulative cash flow turns positive
- **Lowest Cash Point:** The month with the lowest ending cash balance (danger zone)

### Step 4: Scenario Modeling

Build three scenarios:

| Scenario | Revenue Assumption | Expense Assumption |
|----------|-------------------|-------------------|
| Conservative | 80% of projected revenue | 110% of projected expenses |
| Base Case | 100% of projected | 100% of projected |
| Optimistic | 120% of projected revenue | 95% of projected expenses |

Highlight the **conservative scenario** as the planning baseline.

### Step 5: Recommendations

Based on the forecast, provide:
- Cash danger zones (months where ending cash drops below 1 month of expenses)
- Specific recommendations (cut expenses, accelerate revenue, build reserve)
- Decision support for the user's original question

## Examples

### Example 1: Freelance Designer Considering a Full-Time Hire

**Inputs:**
- Cash on hand: $28,000
- Revenue: 3 retainer clients × $3,500/mo = $10,500/mo + sporadic project work ~$2,000/mo
- Fixed expenses: $4,200/mo (rent $1,500, software $400, insurance $300, utilities $200, accounting $150, misc $1,650)
- Proposed hire: $4,500/mo (salary + taxes + benefits)
- Forecast: 6 months

**Forecast (Base Case):**

| | Jan | Feb | Mar | Apr | May | Jun |
|---|-----|-----|-----|-----|-----|-----|
| Starting Cash | $28,000 | $29,800 | $31,600 | $33,400 | $35,200 | $37,000 |
| Retainer Revenue | $10,500 | $10,500 | $10,500 | $10,500 | $10,500 | $10,500 |
| Project Revenue | $2,000 | $2,000 | $2,000 | $2,000 | $2,000 | $2,000 |
| **Total Revenue** | **$12,500** | **$12,500** | **$12,500** | **$12,500** | **$12,500** | **$12,500** |
| Current Expenses | -$4,200 | -$4,200 | -$4,200 | -$4,200 | -$4,200 | -$4,200 |
| New Hire | -$4,500 | -$4,500 | -$4,500 | -$4,500 | -$4,500 | -$4,500 |
| Contractor (replaced) | $0 | $0 | $0 | $0 | $0 | $0 |
| **Total Expenses** | **-$8,700** | **-$8,700** | **-$8,700** | **-$8,700** | **-$8,700** | **-$8,700** |
| **Net Cash Flow** | **$3,800** | **$3,800** | **$3,800** | **$3,800** | **$3,800** | **$3,800** |
| **Ending Cash** | **$31,800** | **$35,600** | **$39,400** | **$43,200** | **$47,000** | **$50,800** |

**Conservative Scenario** (lose 1 retainer client in month 3):

| | Jan | Feb | Mar | Apr | May | Jun |
|---|-----|-----|-----|-----|-----|-----|
| Ending Cash | $31,800 | $35,600 | $35,900 | $31,200 | $26,500 | $21,800 |

**Key Metrics:**
- Burn rate with hire: $8,700/mo
- Revenue coverage: 1.44x (base) / 1.03x (conservative)
- Cash runway (conservative, from month 3): 10.2 months
- Lowest cash point: $21,800 (month 6, conservative)

**Recommendation:** The hire is financially viable. Even in the conservative scenario (losing a client), you maintain $21,800+ cash through month 6 — that's 2.5 months of runway. Proceed with the hire, but set a trigger: if cash drops below $15,000, freeze non-essential spending.

### Example 2: E-commerce Store Seasonal Planning

**Inputs:**
- Cash on hand: $12,000
- Revenue: $8,000/mo average, but seasonal (Nov-Dec: $18,000, Jan-Feb: $4,000)
- Fixed expenses: $3,800/mo
- Variable (COGS): 40% of revenue
- Q4 inventory buy: $8,000 in September

**Key Finding:** Cash drops to $1,400 in October (after inventory buy, before holiday sales). Recommendation: secure a $5,000 line of credit before September or pre-sell holiday bundles in August.

## Recovery & Fallbacks

- **User doesn't know exact numbers:** Use ranges. "Revenue is probably $8K-$12K/mo" → model at $8K (conservative).
- **Revenue is highly variable:** Use the lowest 3-month average as the baseline, not the overall average.
- **User has no financial records:** Start with bank statements. Total deposits = revenue, total debits = expenses. It's rough but usable.
- **Forecast shows negative runway:** Don't panic the user. Present options: cut specific expenses, accelerate a revenue initiative, or bridge with savings/credit.

## Constraints

- **ALWAYS include the financial disclaimer**
- **NEVER present forecasts as guarantees** — they are estimates based on assumptions
- Always show assumptions beneath every projection
- Use conservative scenario as the planning baseline
- Flag any month where ending cash drops below 1 month of expenses
- Round to whole dollars — false precision ($10,437.83) implies accuracy that doesn't exist
