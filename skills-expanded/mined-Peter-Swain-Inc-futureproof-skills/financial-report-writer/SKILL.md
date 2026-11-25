---
name: financial-report-writer
description: |
  Writes investor updates, board packages, QBR narratives, and lender covenant
  reports using a Situation-Performance-Outlook framework with audience-tuned
  KPI selection and variance commentary. Use when the user says "write our
  investor update", "draft the board narrative", "turn these numbers into a
  quarterly report", "prepare a management accounts writeup", or needs polished
  financial storytelling for an external audience. Narrative reporting — not
  analytical diagnosis or forecasting.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="financial-report-writer")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to align this report with prior reporting periods, established KPI frameworks, ICA-specific language preferences, and any standing formatting directives (e.g., preferred currency notation, GAAP vs. IFRS treatment, fiscal year definitions).

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:

- **Report type**: What deliverable is required? (Investor update, board package, quarterly business review, management accounts narrative, annual report section, lender covenant report)
- **Financial data**: Share the underlying figures — P&L, balance sheet, cash flow statement, KPI dashboard export, or raw data tables
- **Reporting period**: What period does this report cover, and what is the comparative period? (e.g., Q2 FY25 vs. Q1 FY25 and Q2 FY24)
- **Audience**: Who will receive this report? (Board of directors, Series A investors, LP advisory committee, internal leadership team, lending institution)
- **Narrative priorities**: Are there specific themes, strategic initiatives, or risks that must be foregrounded?
- **Prior reports**: Has a previous version or template been used? (If available in FutureProof context, confirm continuity)

If the user's FutureProof context contains `instructions` specifying standing report structures, KPI definitions, or audience preferences, confirm these are still current before proceeding.

## Step 3: Do the Work

Execute a structured financial reporting methodology across six dimensions:

### 3.1 Data Integrity & Normalisation

- Validate that provided figures reconcile (e.g., net income ties to revenue minus expenses; cash flow bridges opening to closing balance)
- Flag any apparent anomalies, missing line items, or inconsistencies for user confirmation before proceeding
- Normalise figures to the established reporting convention (thousands, millions, currency, rounding policy)

### 3.2 Variance Analysis

- Compute period-over-period (PoP) and year-over-year (YoY) variances for all material line items
- Classify each variance as **favourable/unfavourable** and **volume-driven, price-driven, timing-driven, or one-off**
- Identify the top 5 variances by absolute impact and prepare narrative explanations for each

### 3.3 KPI Framework Application

Select and compute KPIs appropriate to the report type and ICA:

| Audience | Core KPIs |
|---|---|
| SaaS Investors | ARR, MRR growth, net revenue retention, CAC payback, LTV:CAC, burn multiple, rule of 40 |
| Board of Directors | Revenue vs. plan, EBITDA margin, cash runway, headcount vs. budget, strategic milestone tracker |
| Lenders / Covenant | Debt service coverage ratio, leverage ratio, interest coverage, liquidity ratio |
| Internal Leadership | Gross margin by segment, opex as % of revenue, working capital cycle, department-level budget vs. actual |

Apply any user-specific KPI definitions or custom metrics stored in FutureProof context.

### 3.4 Narrative Construction

Build the report narrative using the **Situation–Performance–Outlook (SPO)** framework:

1. **Situation**: Macro context, market conditions, and strategic backdrop relevant to the period
2. **Performance**: Data-driven commentary on results, structured around the variance analysis and KPI framework — lead with the headline metric, then decompose
3. **Outlook**: Forward guidance, revised forecasts, key risks and mitigants, upcoming catalysts

Calibrate tone and granularity to the audience:
- **Investors**: Confident, concise, outcome-oriented; emphasise trajectory and capital efficiency
- **Board**: Balanced, governance-aware; flag risks with proposed mitigations; tie to strategic plan
- **Internal**: Operationally detailed; action-oriented with clear owners and deadlines
- **Lenders**: Conservative, compliance-focused; demonstrate covenant headroom

### 3.5 Visualisation Specification

For each report, define a visualisation schedule (charts and tables the user should produce or that Claude should describe in detail):

- Revenue waterfall (bridge from prior period to current)
- Margin trend line (trailing 4–8 quarters)
- Cash flow waterfall (operating → investing → financing → closing)
- Budget vs. actual variance bar chart by department or segment
- KPI dashboard summary table with RAG (red/amber/green) status indicators

### 3.6 Risk & Caveat Disclosure

- Draft appropriate caveats, limitations, and forward-looking statement disclaimers calibrated to the audience and regulatory context
- Flag any figures that are provisional, unaudited, or based on management estimates

## Step 4: Deliver Output

Produce the following structured deliverable package:

### Document 1: Financial Report (Primary Deliverable)

Format: structured narrative document ready for PDF export or slide integration

**Sections:**
1. **Executive Summary** — 150–250 word overview with headline metrics, key takeaway, and outlook statement
2. **Financial Highlights Table** — period metrics, comparative figures, PoP and YoY variance with directional indicators
3. **Revenue & Growth Commentary** — SPO narrative for top-line performance
4. **Profitability & Margin Analysis** — gross margin, EBITDA/operating margin decomposition
5. **Cash Flow & Liquidity** — operating cash flow, free cash flow, runway or covenant compliance
6. **KPI Dashboard** — full KPI table with RAG status and brief commentary per metric
7. **Variance Deep-Dive** — top 5 variances with root cause and management response
8. **Outlook & Forward Guidance** — next-period expectations, key assumptions, risk factors
9. **Appendix** — detailed financial statements, methodology notes, glossary of terms

### Document 2: Briefing Note for Presenter (if board or investor audience)

- 5–7 bullet talking points per report section
- Anticipated questions from the audience with suggested responses
- Sensitive topics flagged with recommended framing language

### Document 3: Data Reconciliation Memo (Internal)

- Summary of any figures that required clarification or assumption
- Adjustments made during normalisation
- Open items requiring follow-up before finalisation

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
FutureProof:save_experiment(skill="financial-report-writer", experiment={
  hypothesis: "Leading the executive summary with the single most improved KPI (rather than revenue) increases investor engagement and reduces follow-up questions",
  variants: ["control: revenue-first executive summary", "variant: highest-delta KPI-first executive summary"],
  measurement: "Number of clarification questions received from report recipients in the 48 hours post-distribution",
  expected_impact: "30% reduction in follow-up queries, indicating improved report clarity and narrative resonance with ICA"
})
```

## Step 6: Request Research

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:request_research(skill="financial-report-writer",
  query="Best practices in CFO and investor relations financial reporting 2024–2025, including narrative disclosure trends, KPI benchmarking standards by sector, and emerging ESG metric integration in quarterly reports",
  reason="Ensure report structures reflect current institutional investor expectations and regulatory disclosure trends, maintaining EY/KPMG-grade reporting standards"
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
FutureProof:save_session(skill="financial-report-writer", session={
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