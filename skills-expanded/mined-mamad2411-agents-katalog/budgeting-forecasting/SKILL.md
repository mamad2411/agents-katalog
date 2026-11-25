---
name: budgeting-forecasting
description: >
  Contains verified budget data model (budgetary positions, budget lines with planned/practical/theoretical
  amounts), five-state governance workflow, and 13-week cash flow projection templates that produce more
  precise answers than reasoning from general training alone. Time-proportional pacing computation,
  rolling forecast methodology, cash conversion cycle (DSO/DIO/DPO), working capital ratios, early
  payment discount analysis, line of credit sizing. Consult when creating an annual budget, building
  a rolling forecast, projecting cash flow, checking budget pacing, or asking "how much budget is left"
  or "what's our cash runway."
---

# Budgeting & Forecasting

Budget creation, rolling forecast methodology, and cash flow projection procedures for
C-corporation advisory clients. All budget structures assume US GAAP account hierarchies
and Form 1120 reporting alignment.

## Budget Data Model

Budgets have three structural layers: the header, budgetary positions, and budget lines.

### Budget Header

The envelope for a budget period. Contains:
- **Name** — descriptive label (e.g., "FY2026 Operating Budget")
- **Period** — `date_from` / `date_to` defining the budget window
- **Responsible** — the creating user
- **State** — governs editability and approval (see governance workflow below)
- **Budget lines** — the detail rows linking positions to amounts

### Budgetary Position

A category that groups GL accounts for budget allocation. Each position must link to at
least one GL account. Positions define what you are budgeting (e.g., "Marketing Expenses"
linking accounts 6600-6699, "Revenue" linking 4000-4199).

Design positions to match management reporting needs:
- One position per cost center or functional area
- Mirror the COA hierarchy groupings (invoke `accounting-foundation:chart-of-accounts` for numbering ranges)
- Keep positions broad enough to be stable year-over-year but specific enough for meaningful variance tracking

### Budget Lines

Each line ties a budgetary position to a planned amount for a date range, optionally
linked to an analytic account (department, project, cost center).

- **`planned_amount`** — the budgeted figure. Negative for expenses (matches analytic line sign conventions). Revenue budgets are positive.
- **`practical_amount`** — computed actual spend. Summed from analytic lines matching the position's GL accounts, the line's date range, and analytic account.
- **`theoretical_amount`** — time-proportional expected spend as of today (see pacing computation below).
- **`percentage`** — achievement ratio: `(practical / theoretical) * 100`. Tells you how much of the prorated budget has been realized.

Actuals flow exclusively through analytic lines, not journal entry lines. Budget
tracking requires that journal entries carry analytic distributions. If analytic lines are
missing, practical amount reads zero regardless of actual GL postings.

## Budget Governance Workflow

Budgets progress through a five-state lifecycle:

```
draft --> confirm --> validate --> done
  ^         |           |
  |         v           v
  +------ cancel <------+
```

- **Draft** — editable. Lines can be added, modified, deleted. This is the working state during budget creation and revision cycles.
- **Confirm** — submitted for approval. Lines frozen in UI. The budget preparer advances to this state when the draft is complete.
- **Validate** — approved by management. Confirms the budget as the official baseline for variance reporting. Only advance here after stakeholder sign-off.
- **Done** — period closed. Terminal state after the budget period ends and final variance analysis is complete.
- **Cancel** — withdrawn. Can be reset to draft to restart the cycle.

Budget lines are only editable when state is `draft`. Plan revision cycles before
advancing to `confirm`. Once validated, mid-period changes require a new budget or a
forecast revision rather than editing the approved baseline.

## Time-Proportional Pacing Computation

The theoretical amount answers: "Based on time elapsed, how much of the planned amount
should have been spent/earned by now?"

**Logic branches:**

1. **Today is before `date_from`** (budget period not started) — theoretical = 0.0
2. **Today is between `date_from` and `date_to`** (in progress) — prorate:
   `theoretical = (elapsed_seconds / total_seconds) * planned_amount`
3. **Today is at or past `date_to`** (period complete) — theoretical = full `planned_amount`
4. **`paid_date` override** — if set and `date_to <= paid_date`, theoretical = 0.0; otherwise full `planned_amount`. This handles one-time expenditures with known payment dates.

The computation uses datetime precision (not date), enabling sub-day granularity. A
364-day budget with -364 planned yields -1.0/day, -1.5 at 36 hours elapsed, -308.5
at day 308 noon.

**Achievement interpretation:**
- 100% = spending exactly on pace with time
- Below 100% = underspend relative to time elapsed (for expenses, this is favorable)
- Above 100% = overspend relative to time elapsed (for expenses, this is unfavorable)
- Reverse interpretation for revenue lines (above 100% = favorable)

## Annual Budget Creation Procedure

### Step 1: Gather Historical Actuals

Pull prior-year financial data as the starting baseline. Invoke
`accounting-foundation:financial-statements` for GAAP-basis historical P&L and balance
sheet. Invoke `qbo-integration:qbo-reporting` for Profit and Loss by Month and
Balance Sheet reports from the accounting system.

Key historical data points:
- 12-month P&L by account (revenue lines, COGS, each operating expense category)
- Balance sheet current assets and current liabilities (for working capital forecast)
- Year-over-year growth rates by revenue stream
- Expense-to-revenue ratios by category

### Step 2: Define Budgetary Positions

Create positions that align with management reporting structure:
- Revenue positions by stream (product lines, service types)
- COGS positions by cost driver (materials, labor, overhead)
- OpEx positions by functional area (sales, marketing, G&A, R&D)
- Capital expenditure positions if tracking CapEx in the budget

Each position must reference the corresponding GL account range from the chart of
accounts. Verify account mappings against the active COA.

### Step 3: Build Budget Lines

For each position, create lines with planned amounts:
- **Revenue** — Apply growth assumptions to historical baseline. Document the driver (market growth, pricing, new customers, mix shift).
- **COGS** — Model as percentage of revenue or per-unit cost, depending on business type. Separate variable from fixed components.
- **Operating expenses** — Start with prior-year actuals, adjust for known changes (headcount plan, rent escalation, contract renewals), then apply inflation/deflation assumptions.
- **Set date ranges** — Typically align with fiscal year. For seasonal businesses, consider monthly or quarterly lines to capture timing patterns.

Negative amounts for expenses. Positive for revenue. Verify sign conventions match
analytic line behavior.

### Step 4: Validate and Approve

- Reconcile total budgeted expenses + planned net income to revenue
- Confirm budget balances across all positions
- Advance through governance workflow: draft -> confirm -> validate

## Rolling Forecast Methodology

Rolling forecasts continuously extend the planning horizon, unlike static annual budgets
that end at fiscal year-end. The goal is to always maintain visibility N periods forward.

### Structure

- **Horizon** — typically 12 or 18 months rolling
- **Granularity** — monthly for the next 3-6 months, quarterly beyond that
- **Cadence** — update monthly. Each cycle drops the completed month and adds a new month at the far end.

### Update Procedure

1. Close the current month actuals (invoke `accounting-foundation:financial-statements`)
2. Replace the completed month's forecast with actuals
3. Re-forecast the remaining months based on updated run rates and known changes
4. Extend the horizon by adding a new period at the far end
5. Document key assumption changes (what changed from last month's forecast and why)

### Drivers to Re-Evaluate Each Cycle

- Revenue pipeline changes (deals won/lost, timing shifts)
- Headcount actuals vs. plan (hires, departures, timing)
- Vendor contract changes (rate adjustments, new agreements)
- One-time items (litigation, capital projects, restructuring)
- Macro factors (interest rates, FX, commodity prices)

Rolling forecasts feed into `financial-planning:variance-analysis` as the comparison
baseline for management reporting. They also provide forward-looking inputs to
`financial-planning:financial-modeling` for integrated scenario analysis.

## Cash Flow Projections

### 13-Week Cash Flow Model

The standard short-term liquidity forecasting tool. Projects week-by-week cash position
to identify shortfalls and inform borrowing/investment decisions.

**Structure:**
- **Opening cash balance** — actual bank balance at start of week 1
- **Cash inflows** — collections on AR (by aging bucket), other receipts, credit line draws
- **Cash outflows** — AP payments (by due date), payroll, rent, debt service, tax payments, CapEx
- **Net cash flow** — inflows minus outflows per week
- **Closing cash balance** — opening + net = closing, which becomes next week's opening

**AR collection assumptions:** Use historical collection patterns from AR aging analysis.
Example: 60% collected in current period, 25% in 30 days, 10% in 60 days, 3% in 90 days,
2% write-off. Adjust based on customer mix and recent trends.

**AP payment timing:** Schedule payments at the latest date that captures early payment
discounts when economically beneficial (see working capital decision logic below),
otherwise at term.

### Annual Cash Flow Forecast

Longer-horizon projection that bridges net income to cash:
`Operating Cash Flow = Net Income + Depreciation/Amortization - Change in AR - Change in Inventory + Change in AP`

Working capital line items dominate the bridge for most operating businesses. A profitable
company can be cash-negative if working capital grows faster than earnings (e.g., revenue
growth outpaces collections).

## Working Capital in Forecasts

Working capital changes are the primary driver of operating cash flow variance from net
income. Every budget and forecast should model working capital dynamics explicitly.

### Cash Conversion Cycle (CCC)

`CCC = DSO + DIO - DPO`

- **DSO** (Days Sales Outstanding) = AR / (Revenue / 365) — collection speed
- **DIO** (Days Inventory Outstanding) = Inventory / (COGS / 365) — inventory turnover. N/A for pure service firms.
- **DPO** (Days Payable Outstanding) = AP / (COGS / 365) — payment timing

**Industry benchmarks for CCC:**
- Professional services: 30-45 days (DSO-driven, no inventory)
- Manufacturing: 60-90 days (heavy inventory and trade receivables)
- Retail (cash/prepaid sales): Can be negative with supplier terms
- Construction: 80-120+ days (long project cycles, retention)
- SaaS/subscription: Near zero or negative with annual prepayment

### Liquidity Ratios

- **Current Ratio** = Current Assets / Current Liabilities. Target 1.5-2.0. Below 1.0 signals liquidity stress. Above 3.0 may indicate idle capital.
- **Quick Ratio** = (Cash + Short-Term Investments + AR) / Current Liabilities. Target 1.0+. Excludes inventory and prepaids.
- **Cash Ratio** = (Cash + Equivalents) / Current Liabilities. Most conservative; useful for stress testing.

### Working Capital Decision Logic

**Early payment discount analysis:**
- Standard offer: 2/10 Net 30 (2% discount if paid within 10 days)
- Annualized cost of not taking: (2% / 98%) x (365 / 20) = ~36.7%
- Decision rule: if cost of capital < annualized discount rate, take the discount. At a revolver cost of 8%, the 36.7% annualized return makes the discount nearly always optimal.

**AP term negotiation:**
- Moving Net 30 to Net 45 frees 15 days of cash — model the dollar impact as: (Annual COGS / 365) x days gained
- Preserve vendor relationships; do not stretch beyond agreed terms

**Line of credit sizing:**
- Minimum facility = peak CCC (days) x average daily operating expenses
- Size for peak month, not average
- Target average utilization below 50-60% of commitment
- Revolving credit for seasonal swings; term debt for permanent working capital increases

**Covenant awareness:**
Many loan agreements specify minimum current ratio or minimum working capital. Always
check covenant thresholds before recommending working capital changes. Maintain 15-20%
headroom above covenant minimums.

### Data Extraction for Working Capital

Invoke `qbo-integration:qbo-reporting` for the reports needed from the accounting system:
1. Balance Sheet (Standard) — current assets and current liabilities as of analysis date
2. AR Aging Summary — DSO calculation and aging bucket analysis
3. AP Aging Summary — DPO calculation and payment timing
4. Profit and Loss (Standard) — revenue and COGS for ratio denominators
5. P&L by Month — trend analysis for rolling CCC calculations

**Accounting system limitations to account for:**
- Most accounting systems do not compute CCC/DSO/DIO/DPO natively — extract balances and calculate externally
- AR/AP aging may not match balance sheet if mis-dated transactions or unapplied payments exist — reconcile before calculating ratios
- Inventory tracking in general-purpose accounting systems is limited; complex inventory businesses may have separate systems with different values
- Deferred revenue classification varies by accounting system setup; confirm it is in current liabilities

## Forecast Integration Checklist

Before finalizing any budget or forecast, verify:
- [ ] Revenue assumptions documented with drivers (growth rate, volume, pricing)
- [ ] Expense ratios tested against historical actuals and industry benchmarks
- [ ] Working capital modeled explicitly (AR, AP, inventory changes)
- [ ] Cash flow projection reconciles to P&L via working capital bridge
- [ ] Seasonal patterns captured (monthly or quarterly granularity where relevant)
- [ ] Debt service and covenant compliance confirmed
- [ ] Sign conventions correct (expenses negative, revenue positive)
- [ ] Analytic distributions in place so actuals flow to budget tracking
- [ ] Governance state appropriate (draft for working, validate for approved baseline)

## Supporting References

Read these for deeper detail on specific topics. The SKILL.md above synthesizes the
operational content; the references provide the full source material.

- **`references/budget-data-model.md`** — Complete data model specification for budgets, budgetary positions, and budget lines. Includes field-level definitions, SQL computation logic for practical amounts, state machine transitions, security/access rules, and UI structure. Read when you need exact field names, computation formulas, access control details, or integration point specifics (e.g., how analytic lines connect to budget actuals).

- **`references/guide-fpa.md`** — FP&A expert resource guide with curated source bibliography. Covers core FP&A frameworks (FPAC competency model, FP&A Board maturity model), financial modeling sources (Damodaran, CFI), scenario/sensitivity analysis methods, cash forecasting methodology (AFP, ACT 13-week model), budgeting approaches (zero-based, beyond budgeting), and Excel/SQL/Python tooling. Read when you need authoritative source references, methodology citations, or tool recommendations for an FP&A engagement.

- **`references/working-capital-optimization.md`** — Complete working capital advisory procedures. Covers CCC formula and component metrics with industry benchmarks, liquidity ratios (current, quick, cash), AR optimization tactics (aging analysis, early payment discounts, credit policies), AP management strategies, inventory optimization (ABC analysis, EOQ, safety stock, JIT), line of credit sizing, debt covenant interaction, and the report extraction workflow. Read when doing a working capital assessment, advising on cash management, or building the working capital section of a forecast.

## Cross-Plugin References

**Data sources:**
- Invoke `accounting-foundation:financial-statements` for historical actuals (P&L, balance sheet) used as budget baseline and forecast inputs
- Invoke `qbo-integration:qbo-reporting` for financial reports (P&L by month, balance sheet, AR/AP aging) used in budget creation and working capital analysis

**Downstream consumers:**
- Feeds into `financial-planning:variance-analysis` — the approved budget serves as the comparison baseline for budget-vs-actual analysis
- Referenced by `financial-planning:financial-modeling` — budget assumptions and forecast outputs provide inputs to integrated three-statement models and scenario analysis

**Foundation dependency:**
- Invoke `accounting-foundation:chart-of-accounts` for GL account numbering ranges and hierarchy when designing budgetary positions
