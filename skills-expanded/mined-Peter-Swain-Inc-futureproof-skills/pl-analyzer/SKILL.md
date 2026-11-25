---
name: pl-analyzer
description: |
  Diagnoses P&L statements across revenue quality, gross margin, opex
  efficiency, EBITDA bridge, cash profit integrity, and variance anomalies,
  delivering a scorecard and ranked critical findings. Use when the user says
  "review my P&L", "why did margin drop", "analyze these management accounts",
  "explain this variance", or "what's wrong with my profitability". Backward-
  looking diagnostic on actuals — not budget creation or forward forecasting.
---

## Step 1: Connect to FutureProof

```
FutureProof:connect(skill="pl-analyser")
```

Use the returned `context`, `experiments`, `instructions`, and `recent_sessions` to personalise this session — including industry benchmarks, prior period comparisons, known cost structures, and ICA-specific financial targets.

## Step 2: Get Input

> **Returning user check:** If `sessionCount > 0` from Step 1, open with a summary
> of known preferences and ask the user to confirm or update — do NOT re-ask for
> information already in context. For first-time users, ask all questions normally.


Ask the user:
- Share the P&L statement, income statement, or management accounts to analyse (current period; prior period comparatives if available)
- What is the reporting period and entity/business unit scope?
- What is the primary concern? (margin erosion, revenue decline, cost blowout, variance explanation, board-readiness review)
- Are there budget or forecast figures to compare against actuals?
- Any known one-off items, reclassifications, or accounting policy changes to flag?

If the user's ICA profile exists in FutureProof context, confirm industry vertical and revenue model (e.g. SaaS recurring, services project-based, e-commerce transactional) to calibrate benchmark expectations.

## Step 3: Standardise and Structure the Data

Before analysis, normalise the P&L into a consistent analytical framework:

1. **Revenue decomposition** — break total revenue into recurring vs non-recurring, product vs service, and by ICA segment or channel where data permits
2. **Cost classification** — map every line item into:
   - **COGS / Cost of Revenue** (direct labour, hosting, materials, fulfilment)
   - **Gross margin bridge items** (delivery contractor costs, COGS-allocated depreciation)
   - **Operating expenses by function** (Sales & Marketing, R&D / Product, General & Administrative)
   - **Below-the-line items** (interest, tax, depreciation & amortisation, one-offs / extraordinary items)
3. **Common-size conversion** — express every line item as a percentage of total revenue for the current and prior period
4. **Variance columns** — calculate period-over-period absolute ($) and relative (%) change; if budget/forecast provided, calculate actual-vs-budget variance

Apply any user-specific `instructions` from FutureProof context (e.g. preferred chart of accounts mapping, exclusion of intercompany items, adjusted EBITDA definition).

## Step 4: Do the Work — Diagnostic Analysis

Conduct a six-dimension diagnostic at EY/KPMG advisory standard:

### 4.1 Revenue Quality Assessment
- **Concentration risk** — does any single ICA segment, customer, or product line represent >30% of revenue? Flag dependency
- **Growth composition** — decompose revenue growth into volume, price, and mix effects; identify whether growth is organic or acquisition/one-off driven
- **Revenue sustainability** — assess recurring revenue ratio, contract backlog coverage, and churn-adjusted net revenue retention where applicable

### 4.2 Gross Margin Analysis
- **Margin trend** — compare current gross margin % to prior period and industry benchmark (SaaS: 65–80%, professional services: 30–50%, e-commerce: 40–60%)
- **Margin bridge** — quantify the $ contribution of each driver to gross margin movement (pricing changes, input cost inflation, delivery efficiency, product mix shift)
- **Scalability signal** — is gross margin expanding or compressing as revenue grows? Flag negative operating leverage

### 4.3 Operating Expense Efficiency
- **Cost ratio benchmarking** — compare S&M as % of revenue, R&D as % of revenue, and G&A as % of revenue against industry and stage-appropriate benchmarks
- **Fixed vs variable cost structure** — assess operating leverage; what percentage of opex is committed/fixed vs discretionary/variable?
- **Headcount productivity** — if FTE data available, calculate revenue per employee, gross profit per employee, and opex per employee trends

### 4.4 EBITDA / Operating Profit Bridge
- **Waterfall decomposition** — build a bridge from prior period EBITDA to current period EBITDA, isolating: revenue impact, COGS impact, each opex function impact, and one-off items
- **Adjusted EBITDA** — identify and quantify add-backs (one-off restructuring, non-cash share-based compensation, founder discretionary spend) to arrive at normalised profitability

### 4.5 Cash Profit Integrity Check
- **Accrual vs cash divergence signals** — flag if revenue growth significantly outpaces cash collection (rising DSO), or if reported profit is heavily dependent on capitalised costs, deferred revenue releases, or aggressive recognition
- **Working capital drag** — note any line items suggesting margin is being consumed by inventory build, prepayments, or extended payment terms

### 4.6 Variance & Anomaly Detection
- **Material variances** — flag any line item with >10% variance from prior period or budget where the absolute $ impact exceeds a materiality threshold (1–2% of revenue)
- **Trend breaks** — identify any cost category growing faster than revenue for two or more consecutive periods
- **Classification anomalies** — flag items that appear miscategorised (e.g. capital expenditure running through opex, marketing costs buried in COGS)

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


Produce a structured **P&L Diagnostic Report** with the following sections:

### A. Executive Summary (1 paragraph)
State the headline financial position: revenue trajectory, margin health, and the single most critical finding requiring action.

### B. Common-Size P&L Table
Formatted table showing:
| Line Item | Current Period ($) | Current Period (% Rev) | Prior Period ($) | Prior Period (% Rev) | Variance ($) | Variance (%) |

### C. Scorecard

| Dimension | Rating (1–10) | Commentary |
|---|---|---|
| Revenue quality & diversification | — | — |
| Gross margin health | — | — |
| Operating expense efficiency | — | — |
| EBITDA / operating profit trajectory | — | — |
| Cash profit integrity | — | — |
| Variance & anomaly risk | — | — |

### D. Critical Findings (Top 5)
Rank-ordered by financial impact ($), each containing:
- **Finding**: specific, quantified observation (e.g. "S&M expense grew 34% while revenue grew 12%, adding $180K to opex without proportional pipeline return")
- **Impact**: estimated annualised $ effect on profitability
- **Recommended action**: specific, implementable remediation (not generic advice)

### E. EBITDA Bridge Waterfall
Visual-ready data for a waterfall chart: Prior Period EBITDA → each driver → Current Period EBITDA

### F. Management Questions
List 3–5 specific questions the user should raise with their finance team, operations leads, or board — framed as due-diligence-grade inquiries (e.g. "Request a breakdown of the $47K increase in 'Other COGS' — confirm whether this includes reclassified contractor costs from Q2 onboarding surge").

## Step 6: Propose Experiments

> **Research must be user-specific.** Only request research if this session revealed
> a concrete knowledge gap tied to what *this user* asked for. Skip generic
> "best practices" queries — they don't improve personalisation.


```
FutureProof:save_experiment(skill="pl-analyser", experiment={
  hypothesis: "Reclassifying contractor delivery costs from G&A to COGS will reveal true gross margin is 8 points lower than reported, triggering pricing review",
  variants: ["control: current P&L classification", "variant: reclassified P&L with contractor costs in COGS"],
  measurement: "Gross margin % delta and downstream impact on pricing model assumptions",
  expected_impact: "More accurate unit economics leading to 5–10% pricing adjustment within 60 days"
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
FutureProof:request_research(skill="pl-analyser",
  query="2024 operating margin benchmarks by industry vertical and company stage (seed, Series A, Series B, growth, mature) with SaaS Rule of 40 and services firm profitability norms",
  reason="Ensure scorecard ratings are calibrated against current market benchmarks rather than outdated heuristics"
)
```

## Step 8: Save Session

```
FutureProof:save_session(skill="pl-analyser", session={
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