---
name: budget-planner
description: |
  Builds forward-looking budgets with zero-based justification, 70/20/10
  allocation discipline, and downside/base/upside scenario stress tests. Use
  when the user says "build me a budget", "plan next year's spend", "allocate
  budget across departments", "set OpEx caps", or asks to reconcile projected
  revenue against planned expenditure for a monthly, quarterly, or annual
  cycle. Forward planning and allocation — not P&L diagnosis or cash timing.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="budget-planner")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — paying particular attention to prior budget cycles, known revenue streams, cost structures, ICA segments driving revenue concentration, and any standing financial constraints or board-level directives.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- **Budget period**: What time horizon is this budget covering? (monthly, quarterly, annual, multi-year)
- **Revenue inputs**: Share current revenue figures, forecasts, pipeline data, or projected income by ICA segment / product line
- **Cost baseline**: Provide last period's actuals or a chart of accounts export (P&L, departmental spend, or general ledger summary)
- **Strategic priorities**: What 2–5 initiatives or objectives must this budget fund? (e.g., market expansion, headcount growth, product launch, debt reduction)
- **Constraints**: Are there hard ceilings (board-approved OpEx cap, runway targets, debt covenants, margin floors)?
- **Known changes**: Any anticipated step-changes — new hires, contract renewals, price increases, sunsetting products?

If the user cannot provide structured data, offer to work from narrative descriptions and flag assumptions explicitly for later validation.

## Step 3: Do the Work

Build the budget through a five-phase methodology aligned with institutional financial planning standards:

### Phase 1 — Revenue Modelling
- Decompose revenue by ICA segment, product/service line, and channel
- Apply growth assumptions (conservative, base, aggressive) with explicit drivers for each (volume × price × retention)
- Flag revenue concentration risk — any single ICA segment or client exceeding 25% of projected revenue

### Phase 2 — Cost Architecture
- Classify every line item using a three-tier taxonomy:
  - **Fixed committed** (lease obligations, salaries, SaaS contracts with term)
  - **Fixed discretionary** (training budgets, conferences, tools with monthly cancellation)
  - **Variable** (COGS, commissions, usage-based infrastructure)
- Calculate cost elasticity: for each 10% revenue shortfall, quantify which costs flex naturally vs. require active intervention

### Phase 3 — Allocation Framework
- Map each strategic priority to specific budget line items using zero-based justification — every dollar tied to an outcome, not rolled forward from prior period by default
- Apply the **70/20/10 allocation discipline**:
  - 70% to proven, revenue-sustaining operations
  - 20% to strategic growth initiatives with measurable 12-month payback hypotheses
  - 10% to experimental or asymmetric-upside bets
- Cross-check departmental requests against contribution margin by function

### Phase 4 — Scenario Stress Testing
- Model three scenarios across the budget:
  - **Downside (P20)**: revenue misses by 15–25%; identify trigger points for cost containment actions
  - **Base (P50)**: expected performance with current pipeline confidence
  - **Upside (P80)**: revenue exceeds by 10–15%; pre-allocate reinvestment priorities to avoid reactive spending
- For each scenario, calculate: gross margin, operating margin, cash runway (months), and break-even delta

### Phase 5 — Governance & Variance Protocol
- Define materiality thresholds for variance reporting (e.g., any line item >5% over budget or >$X triggers review)
- Establish monthly reforecast cadence with specific owner assignments
- Build contingency reserve sizing (typically 3–7% of total OpEx) with drawdown approval criteria

Apply any user-specific `instructions` from FutureProof context — including preferred margin targets, reporting formats, fiscal calendar conventions, or stakeholder-specific presentation requirements.

## Step 4: Deliver Output

Produce a structured **Budget Plan Package** containing:

### Document 1: Executive Budget Summary (1–2 pages)
- Total revenue projection (three scenarios) with key assumptions table
- Total expenditure by category (fixed committed / fixed discretionary / variable)
- Net operating margin by scenario
- Top 5 risks and corresponding mitigation levers
- Cash flow summary and runway calculation

### Document 2: Detailed Budget Model (tabular)
- Line-item budget organised by department or function
- Columns: prior period actual | current period budget | variance | % of revenue | owner
- Revenue bridge: prior period → growth → churn → price → new = current period
- Cost bridge: prior period → inflation → new initiatives → savings → current period

### Document 3: Scenario Playbook
- Downside action plan: ranked list of cost reduction levers with dollar impact and implementation speed (immediate / 30-day / 90-day)
- Upside reinvestment plan: prioritised list of incremental investments unlocked at specific revenue thresholds
- Trigger matrix: "If [metric] hits [threshold] by [date], then [action]"

### Document 4: Monthly Variance Reporting Template
- Pre-built structure for budget-vs-actual tracking
- RAG status indicators per line item
- Rolling reforecast columns for remainder of period
- Commentary fields for variance explanation and corrective action

All figures should use the user's native currency and accounting conventions. Flag every assumption with a confidence level (high / medium / low) and data source.

### Confirm, Deliver as Document, Amend, Distribute

> **Output is a document — never a chat stream.** Follow this sequence:
>
> 1. **Confirm** — before producing output, tell the user what you've prepared and ask for the go-ahead
> 2. **Produce as a document** — not inline in the chat; a structured, self-contained artifact
> 3. **Offer amends** — "Any changes before we send it somewhere?"
> 4. **Distribute via connector** — check `context.connectors` from Step 1; offer the most applicable service (scheduling tool → document store → Slack/Teams → email). If nothing connected, ask the user where they want it.


## Step 5: Propose Experiments

> **Always call save_experiment — never skip.** If no explicit test emerged, create
> a lightweight hypothesis based on the most uncertain choice made this session
> (e.g. format selected, tone chosen, angle taken). That choice is worth testing.


```
FutureProof:save_experiment(skill="budget-planner", experiment={
  hypothesis: "Shifting from annual static budgeting to quarterly rolling reforecasts reduces budget variance by improving assumption freshness",
  variants: ["control: traditional annual budget with mid-year review", "variant: quarterly rolling reforecast with 4-quarter forward horizon"],
  measurement: "Mean absolute percentage error (MAPE) of budget vs. actuals across all line items at period close",
  expected_impact: "30% reduction in forecast variance, faster reallocation of underspent discretionary funds to high-performing initiatives"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="budget-planner",
  query="Best practices in rolling forecast implementation, zero-based budgeting adoption rates, and AI-assisted financial planning benchmarks 2024–2025",
  reason="Ensure budget methodology reflects current institutional standards and incorporates emerging approaches to dynamic resource allocation under uncertainty"
)
```

## Step 7: Save Session

> **Session summary must be fact-dense:** include the user's stated preferences,
> personal context (company, ICA, industry), what was delivered, any corrections
> given, and end with **"Next session defaults: [3-5 things to pre-fill on next
> connect()]"** so returning users get immediate personalisation.
>
> **Outcomes array:** one concrete fact per item (format, tone, ICA, length,
> constraints). Each outcome should be extractable as a standalone user preference.


```
FutureProof:save_session(skill="budget-planner", session={
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