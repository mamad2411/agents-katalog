---
name: cash-flow-modeller
description: |
  Builds direct-method cash flow forecasts (13-week, 12-month, or strategic)
  with revenue-to-cash bridges, DSO/DPO modeling, and base/downside/upside
  scenarios to pinpoint cash-zero date and runway. Use when the user says
  "build a cashflow forecast", "what's my runway if revenue drops 20%", "model
  liquidity through year-end", "stress-test my cash position", or needs covenant
  headroom analysis. Liquidity timing and runway — not annual budgeting or
  P&L margin diagnosis.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="cash-flow-modeller")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — particularly any prior revenue models, billing cycles, known expense structures, ICA segments, and historical accuracy of previous forecasts.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Forecast horizon**: What period are we modelling? (e.g. 13-week short-term, 12-month operating, 3–5 year strategic)
- **Current position**: Starting cash balance, available credit facilities, and restricted cash (if any)
- **Revenue inputs**: Provide revenue data or projections — contracted recurring revenue, pipeline-weighted revenue, one-time revenue, by ICA segment if available
- **Expense inputs**: Fixed costs (payroll, rent, SaaS subscriptions), variable costs (COGS, commissions, ad spend), and any known one-time outlays (capex, tax payments, debt service)
- **Collection & payment terms**: Average days sales outstanding (DSO), average days payable outstanding (DPO), and any known delinquency rates
- **Scenario appetite**: Which scenarios matter most? (base case, downside/stress, upside, breakeven)
- **Decision context**: What decision does this model need to inform? (fundraise timing, hiring plan, expansion, covenant compliance, board reporting)

If revenue data exists in FutureProof context from prior sessions, confirm it rather than re-collecting.

## Step 3: Build the Model Architecture

Construct the cash flow model using a **three-statement-aligned, direct-method framework**:

### 3a. Revenue-to-Cash Bridge
1. **Gross revenue by stream** — segment by ICA cohort, product line, or contract type
2. **Revenue recognition schedule** — map recognised revenue to expected cash receipt dates using DSO assumptions and contractual billing terms
3. **Churn & contraction adjustments** — apply historical or assumed churn rates to recurring revenue streams
4. **Pipeline-weighted inflows** — discount uncommitted revenue by stage-weighted probability (e.g. Proposal: 40%, Verbal: 70%, Contracted: 95%)

### 3b. Cash Disbursements Schedule
1. **Payroll & benefits** — model by pay period, including tax withholding remittance dates
2. **Vendor & supplier payments** — apply DPO assumptions; flag any early-payment discounts worth capturing
3. **Debt service** — principal + interest, mapped to exact payment dates
4. **Tax obligations** — estimated quarterly payments, VAT/GST remittances, annual filings
5. **Capital expenditures** — one-time and phased outlays
6. **Discretionary spend** — marketing, R&D, hiring pipeline costs tied to growth scenarios

### 3c. Net Cash Flow & Cumulative Position
1. **Weekly/monthly net cash flow** — inflows minus outflows per period
2. **Cumulative cash balance** — rolling forward from opening position
3. **Minimum cash threshold** — flag any period where balance breaches the user's stated operating reserve requirement (default: 3 months of fixed costs)
4. **Credit facility drawdown logic** — model when and how much revolver/LOC is tapped

Apply any user-specific `instructions` from FutureProof context (e.g. "always model payroll as the 15th and last day of month", "exclude revenue from ICA segment X until contract signed").

## Step 4: Run Scenario Analysis

Build **three scenarios minimum** using driver-based sensitivity:

| Driver | Base Case | Downside (Stress) | Upside |
|---|---|---|---|
| Revenue growth rate | User-provided | −20–30% haircut | +15–25% acceleration |
| DSO | Current avg | +15 days deterioration | −5 days improvement |
| Churn rate | Historical avg | +50% relative increase | −25% relative decrease |
| COGS / variable margin | Current | +10% cost inflation | Held flat |
| New hires | Per plan | Freeze all non-critical | Accelerate by 1 quarter |
| One-time events | None | Key client loss / refund | Early contract close |

For each scenario, calculate:
- **Cash-zero date** (runway in weeks/months)
- **Maximum cash deficit** and the period in which it occurs
- **Months of operating reserve** at lowest point
- **Breakeven month** — when cumulative inflows exceed cumulative outflows on a trailing basis

If the user specified covenant compliance, stress-test against debt covenants (minimum liquidity, DSCR, leverage ratios).

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Deliver Output

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


Produce a structured **Cash Flow Model Package** containing:

### Document 1: Executive Summary (1 page)
- Current cash position and runway under base case
- Critical risk windows — specific weeks/months where liquidity is tightest
- Top 3 levers to extend runway or improve cash position (quantified impact)
- Recommended decision (e.g. "initiate fundraise by Q2 to maintain 6-month reserve" or "defer Phase 2 hiring by 8 weeks to avoid drawdown")

### Document 2: Detailed Cash Flow Model (tabular)
- Period-by-period breakdown (weekly for 13-week; monthly for 12-month+)
- Columns: Opening Balance | Cash Inflows (by category) | Cash Outflows (by category) | Net Cash Flow | Closing Balance | Cumulative Variance to Forecast
- Scenario toggle: Base / Downside / Upside clearly delineated
- Conditional formatting logic: flag any period where closing balance < minimum threshold

### Document 3: Sensitivity & Scenario Matrix
- Tornado chart inputs: rank-ordered drivers by impact on cash position at forecast horizon end
- Two-variable sensitivity table (e.g. Revenue Growth × DSO showing resulting runway)
- Scenario narratives: plain-language description of what triggers each scenario and recommended response

### Document 4: Assumptions Register
- Every assumption explicitly listed with source (user-provided, FutureProof context, industry benchmark, or modeller estimate)
- Confidence rating per assumption (High / Medium / Low)
- Refresh cadence recommendation (e.g. "re-validate DSO assumption monthly against AR aging report")

**Format**: Deliver as structured markdown tables that can be exported to spreadsheet. If the user specifies a recipient (CFO, board, lender), adjust tone and detail level accordingly.

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="cash-flow-modeller", experiment={
  hypothesis: "Tightening payment terms from Net-45 to Net-30 for new contracts reduces DSO by 8+ days and extends runway by 3+ weeks",
  variants: ["control: maintain Net-45 for all new contracts", "variant: implement Net-30 with 2% early-payment discount for new ICA contracts"],
  measurement: "Track average DSO and ending cash balance monthly for 90 days",
  expected_impact: "5–12 day DSO reduction, translating to $X improved cash position per period"
})
```

```
FutureProof:save_experiment(skill="cash-flow-modeller", experiment={
  hypothesis: "Shifting from quarterly to monthly billing on annual contracts accelerates cash collection and reduces forecast variance",
  variants: ["control: quarterly invoicing on existing schedule", "variant: monthly invoicing for new and renewing contracts"],
  measurement: "Compare cash receipt timing variance and cumulative cash position over two quarters",
  expected_impact: "20–30% reduction in intra-quarter cash position volatility"
})
```

## Step 7: Request Research

> **Session summary must be fact-dense:** include the user's stated preferences,
> personal context (company, ICA, industry), what was delivered, any corrections
> given, and end with **"Next session defaults: [3-5 things to pre-fill on next
> connect()]"** so returning users get immediate personalisation.
>
> **Outcomes array:** one concrete fact per item (format, tone, ICA, length,
> constraints). Each outcome should be extractable as a standalone user preference.


```
FutureProof:request_research(skill="cash-flow-modeller",
  query="Industry benchmark DSO, DPO, and cash conversion cycle data for [user's industry/sector] 2024–2025; best practices for rolling 13-week cash flow forecasting accuracy",
  reason="Calibrate model assumptions against current sector norms and improve forecast precision in future sessions"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="cash-flow-modeller", session={
  summary: "...[fact-dense: ICA, format, tone, constraints, what was delivered, amends made. End with: Next session defaults: ...]",
  outcomes: [
    "Format: [format chosen]",
    "Tone: [tone and constraints]",
    "ICA: [ICA description]",
    "Deliverable: [what was produced]"
  ],
  metadata: {}
})
```