---
name: strategic-finance-maturity
description: Diagnose where a company's finance function sits on Oana Labes' 5-layer maturity model — from Layer 1 (Trusted Financials) through Layer 5 (Value Creation) — and distinguish Strategic Finance behaviors (engineers the future) from FP&A behaviors (reports what happened). Use when auditing a finance function, identifying where the CFO or finance team is leaving strategic value on the table, building a finance transformation roadmap, or assessing a company pre-investment/pre-acquisition. Source: Oana Labes MBA, CPA / CEO Financial Intelligence Academy.
---

# Strategic Finance Maturity Model

Source: Oana Labes, MBA, CPA — CEO Financial Intelligence Academy (oanalabes.com)

> Strategic Finance engineers the future. FP&A reports what happened. Most finance functions never make it past Layer 2.

## The 5 layers — Strategic Finance vs. FP&A

### Layer 1 — TRUSTED FINANCIALS
*Connected Statements, Verified Data*

| Strategic Finance does | FP&A trap |
|---|---|
| P&L, balance sheet, cash flow connected | P&L as the only view |
| Single source of truth | Spreadsheet workarounds |
| Books close clean and on time | Late close cycles |
| Real-time integration | Manual reconciliations |
| Cash flow ties to earnings | Disconnected systems |
| Working capital changes explained | Numbers get restated |
| Why we beat or missed plan | "Why" left unanswered |
| Trend analysis quarterly | Static reports |
| Operating leverage tracked | Dashboard without insight |
| Assumption shifts modeled | — |
| Triggers identified upfront | — |

### Layer 2 — PERFORMANCE INSIGHT
*Drivers, Ratios, Trends*

| Strategic Finance does | FP&A trap |
|---|---|
| What's actually driving the numbers | Misses called out, never explained |
| Where margin comes from | Last quarter's numbers only |
| Few KPIs that matter | Disconnected KPIs |
| Capital plan integrated | Sensitivities skipped |
| Downside stress-tested | Forecast as target |
| Returns vs forecast measured | — |

### Layer 3 — FORWARD VISIBILITY
*Forecasts, Scenarios, Stress Tests*

| Strategic Finance does | FP&A trap |
|---|---|
| Rolling 18-month forecast | Annual budget only |
| Three scenarios always | Single-point forecast |
| Reallocation discipline | Optimistic by default |
| Capital plan documented | Budget seen as commitment |
| Marginal cost calculated | ROIC rarely measured |
| ROIC tracked by category | Sunk-cost loyalty |

### Layer 4 — CAPITAL ALLOCATION
*Deployment, Returns, Discipline*

| Strategic Finance does | FP&A trap |
|---|---|
| Hurdle rates enforced | Capex by gut feel |
| Investor-grade reporting | Approvals without analysis |
| Strategic decisions modeled | Strategy disconnected from numbers |
| Capital structure intentional | Capital structure inherited |
| EV growth measured quarterly | Cash flow as afterthought |

### Layer 5 — VALUE CREATION
*Strategy, Governance, EV Growth*

| Strategic Finance does | FP&A trap |
|---|---|
| Board-level finance ownership | Board sees P&L only |
| Real Free Cash Flow™ tracked | Reports never reach the board |
| Revenue growth treated as strategy | — |

---

## Copy-paste diagnostic prompt

```
You are a strategic finance advisor. Use Oana Labes' 5-layer finance maturity model to diagnose where this company's finance function currently operates and identify the highest-leverage upgrades.

COMPANY CONTEXT:
- Industry / stage: [FILL IN — e.g. Series B SaaS, €50M revenue, 200 employees]
- Current finance team: [FILL IN — e.g. 1 CFO + 2 FP&A analysts, no controller]
- Current tools: [FILL IN — e.g. QuickBooks, Excel, no BI tool]
- What the finance function currently produces: [FILL IN — e.g. monthly P&L, annual budget, quarterly board deck]
- Known finance pain points: [FILL IN]

Assess this company against each layer:

LAYER 1 — TRUSTED FINANCIALS
- Are the three statements (P&L, balance sheet, cash flow) connected and reconciled?
- Is there a single source of truth, or spreadsheet workarounds?
- Do books close on time? Is cash flow tied to earnings?

LAYER 2 — PERFORMANCE INSIGHT
- Does the team explain what's DRIVING the numbers, not just what they are?
- Are there a few KPIs that matter, or disconnected metrics?
- Is downside stress-tested? Is operating leverage tracked?

LAYER 3 — FORWARD VISIBILITY
- Is there a rolling forecast (beyond annual budget)?
- Are three scenarios (base/upside/downside) standard practice?
- Is there a documented capital plan?

LAYER 4 — CAPITAL ALLOCATION
- Are hurdle rates defined and enforced?
- Is ROIC tracked by category? Are marginal costs calculated?
- Is the capital structure intentional, or inherited?

LAYER 5 — VALUE CREATION
- Does finance have board-level ownership?
- Is real free cash flow tracked? Is revenue growth treated as a strategy question?

Produce:
1. Current layer rating (1–5) with specific evidence from the context
2. The 3 most critical gaps blocking progress to the next layer
3. The highest-leverage single action to upgrade from current layer to the next
4. A 90-day finance transformation sprint (3 milestones, each 30 days)
5. Which FP&A traps this company is currently stuck in
```

---

## Pre-investment / acquisition finance audit prompt

```
I am evaluating [COMPANY NAME] for [acquisition / investment / partnership]. Audit their finance function using Oana Labes' 5-layer strategic finance model.

Available information:
[PASTE FINANCIALS, BOARD DECK, OR DESCRIBE WHAT YOU HAVE ACCESS TO]

Questions to answer:
1. What layer does their finance function appear to operate at? What's the evidence?
2. Which Strategic Finance behaviors are present vs. absent?
3. What does the absence of Layer [X] behaviors imply about data quality, forecast reliability, and capital discipline?
4. What finance-function risks should I price into this deal?
5. What would it cost (time + headcount) to bring this company to Layer 4 within 18 months?
```

---

## CFO self-assessment prompt

```
I am the CFO / Head of Finance at [COMPANY]. Audit my own finance function honestly against Oana Labes' 5-layer model.

For each layer, tell me:
- What behaviors I should already have in place at my company size/stage
- Which ones I can confirm I have
- Which ones I'm missing or doing partially
- The one thing I should stop doing (FP&A trap) and one thing I should start (Strategic Finance behavior)

My context:
- Company stage and size: [FILL IN]
- My team: [FILL IN]
- Current outputs I produce: [FILL IN]
- What the board/CEO asks me for most: [FILL IN]
- What I spend most of my time on: [FILL IN]
```

---

## The Strategic Finance vs. FP&A distinction (one-liner)

| | Strategic Finance | FP&A |
|---|---|---|
| Orientation | Future | Past |
| Question answered | What should we do? | What happened? |
| Capital structure | Intentional | Inherited |
| Forecast | Rolling 18-month, 3 scenarios | Annual budget |
| ROIC | Tracked by category | Rarely measured |
| Board relationship | Finance owns strategy | Reports to the board |
| Value driver | EV growth | Variance to plan |

---

## Related skills

- **business-intelligence-report**: Package the output of a finance audit into a formal board-ready report
- **multi-agent-debate**: Stress-test a finance transformation plan before committing resources
- **business-decision-frameworks**: Apply RICE or OKR scoring to prioritize finance upgrade initiatives
- **the-leverage-stack-auditor**: Combine with this skill — leverage audit (operational) + finance maturity (financial) = full business health picture
