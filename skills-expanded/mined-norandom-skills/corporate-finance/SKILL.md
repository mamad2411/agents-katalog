---
name: corporate-finance
version: 1.3.1
description: >
  Build, analyze, advise on, or review corporate financial models: three-statement
  models, budgets, cash forecasts, DCF/WACC valuations, EBITDA, and ratios. Use
  for auditable spreadsheet models and financial-statement interpretation, with
  formula traces and Python verification. Excludes bookkeeping, tax filing,
  audit opinions, and personal budgeting.
---

# Corporate finance and financial modeling

This skill starts with the finance action: build, analyze, advise, or reflect. From there it pulls two things: the explanation for the metric or method, and the spreadsheet structure that produces it. The point is simple: do the finance work in the right order, with the math visible.

It uses personal notes about Bojan Radojicic / bojanfin.com corporate-finance material, including handbooks, the 50-sheet model map, and worked XLSX templates, plus personal notes about MBA financial-modeling material on traceability and formula discipline. It is not original source text or an excerpt from those materials. Per-note source credits appear in the relevant bundled reference notes.

> Intent (action) -> explanation layer (concept) + template layer (spreadsheet) -> auditable artifact

---

## Prime directive: stay in the intent

Every request resolves to one of four action intents. Identify the intent first, then stay inside that workflow until the task is complete. Do not drift from build to advice, or from analysis to valuation, unless the user asks or the current workflow reaches a REFLECT gate.

For finance work, the math is part of the deliverable. Do not state a number unless you can show source, formula, substitution, units, result, and validation check. After the initial pass, independently recalculate every material result with Python against the initial results. If Python and the initial result disagree, stop and resolve the mismatch before delivery: check source values, units, scale, signs, period alignment, formula logic, and rounding. If the trace or Python check cannot be shown, label the value as an assumption/open item or do not state it.

Then pull the matching explanation and template:

| Intent | You want to | Primary output |
|--------|--------------|----------------|
| MODEL / BUILD | produce a spreadsheet | an XLSX / Claude-for-Excel workbook |
| ANALYZE / DIAGNOSE | read existing numbers | findings + ratios + commentary |
| ADVISE / CONSULT | improve a process or choose a method | a recommendation with trade-offs |
| REFLECT | check a model's integrity | a critique + fix list |

The ontology that maps finance topics to these intents is `references/intent-map.md`. The auditability protocol is `references/auditability-and-math-rigor.md`. Read both whenever the request contains numbers, formulas, model outputs, or an existing workbook.

---

## When to use / when not

Use it to build or fix a financial model, draft a budget, value a company, forecast cash, or interpret a set of statements or ratios.

Skip it for bookkeeping/journal entries, statutory tax filing, audit opinions, or personal-finance budgeting. Those are nearby tasks, but this skill does not cover them.

---

## How to use this skill

1. Classify the intent and lock the workflow (`references/intent-map.md`). MODEL, ANALYZE, ADVISE, or REFLECT? If the user says "build/make/forecast" it is MODEL; "why/how is/interpret" is ANALYZE; "should I/what's better" is ADVISE; "check/is this right" is REFLECT. Stay in that flow until its output and checks are complete.
2. Gather the context packet. You need entity, periods, granularity, currency, evidence status, and whichever inputs the chosen artifact consumes. Ask only for inputs that change the output.
3. Pull the explanation layer. Read the topic reference: `references/ebitda.md`, `references/ratios-and-analysis.md`, `references/three-statement-model.md`, `references/cash-flow-working-capital.md`, `references/valuation-dcf-wacc.md`, or `references/budgeting.md`. This gives the reason for the metric and how to read it.
4. Pull the audit layer (`references/auditability-and-math-rigor.md`). Every material number needs this trace: source -> formula -> inputs/cells -> substitution -> step-by-step calculation -> result -> units -> check -> Python recalculation -> mismatch status.
5. Pull the template layer. For MODEL intent, open the matching asset spec in `assets/` and follow `references/spreadsheet-conventions.md`: color coding, assumption sheet, evidence sheet, validation checks, no hardcoded values.
6. Produce the initial artifact. Build the workbook, run the analysis, or write the advice. For MODEL, follow the 20-step build order in `references/modeling-best-practices.md` and split long formulas into helper rows or sheets. Treat this as the initial pass, not the final answer.
7. Verify with Python before delivery. Recalculate the initial pass's material outputs in Python using the same source inputs. Compare Python results to the initial results. If any mismatch appears, investigate source values, signs, units, scale, period alignment, formula logic, and rounding; then correct the initial artifact or document the resolved exception. Do not present mismatched numbers as facts.
8. Reflect before delivery (`references/intent-map.md` REFLECT section). Run the consistency and sanity checks. Flag EBITDA/Non-GAAP, terminal-value, false-precision, source, formula-trace, or Python-verification risks. Hand off to `reflect` for a deeper assumption critique if the stakes are high.

---

## Capability map

- A. EBITDA & KPIs: definition, 4 KPIs, applications, improvement levers, controversies: `references/ebitda.md`.
- B. Ratios & statement analysis: liquidity/profitability/efficiency/leverage ratios, common-size (vertical) and trend (horizontal) analysis, breakeven, the 6-step ratio workflow, diagnostic reading: `references/ratios-and-analysis.md`.
- C. The 3-statement model: the 50-sheet model map, schedule-driven IS/BS/CF, linking logic, granularity: `references/three-statement-model.md`.
- D. Cash flow & working capital: direct vs indirect, 13-week forecast, NWC, cash conversion cycle, cash levers: `references/cash-flow-working-capital.md`.
- E. Valuation: DCF, FCFF, WACC build-up, terminal value, method selection, 40+ value drivers, common mistakes: `references/valuation-dcf-wacc.md`.
- F. Budgeting & planning: ZBB / incremental / rolling / beyond budgeting, cost-driver matrix, budget vs forecast vs plan: `references/budgeting.md`.
- G. Build craft: 20-step order, best practices, spreadsheet conventions: `references/modeling-best-practices.md`, `references/spreadsheet-conventions.md`.
- H. Auditability & math rigor: workflow lock, formula trace, evidence ledger, precision discipline: `references/auditability-and-math-rigor.md`.

---

## The context packet

Carry these fields across every phase. Use stable IDs when referring back to them.

| Packet field | Role |
|--------------|------|
| `E entity` | company / business unit being modeled |
| `P periods` | horizon + granularity (monthly Jan–Dec+FY, or yearly Y1–Y12) |
| `C currency` | reporting currency + units (000s / millions) |
| `H history` | historical financials feeding baselines (blue cells) |
| `A assumptions` | drivers the user controls (yellow cells) |
| `S sources` | source files, source cells, or evidence status for each input |
| `M math trace` | formula, input cells, substitution, result, units, validation for each material output |
| `O output` | the artifact for this intent (workbook / findings / advice / critique) |

---

## Decision points

- Which valuation method? Projectable cash flows + stable growth -> DCF. Public peers exist / startup with no cash flow -> Comparable Companies (EV/EBITDA). M&A with control premium -> Precedent Transactions. Pre-revenue / distressed / asset-heavy -> Net Book Value + Replacement Cost. (`references/valuation-dcf-wacc.md`.)
- Which budgeting method? Cut legacy cost / reallocate to strategy -> ZBB. Stable, predictable firm -> Incremental. Dynamic environment / constant horizon -> Rolling. Volatile industry, fixed targets harmful -> Beyond Budgeting. (`references/budgeting.md`.)
- Direct or indirect cash flow? Short-term liquidity (weekly/13-week) -> Direct. Monthly/annual statement tied to the model -> Indirect. (`references/cash-flow-working-capital.md`.)
- EBITDA looks great but net margin lags? The problem is below the operating line: interest (financing policy) and corporate income tax (tax policy). (`references/ratios-and-analysis.md`.)
- Can the result be stated? Only if the source and formula trace are clear. Otherwise state it as an assumption, range, or open item, never as an unexplained fact. (`references/auditability-and-math-rigor.md`.)

---

## Cross-skill handoffs

| Sibling skill | Direction | Phase | What flows |
|---------------|-----------|-------|------------|
| `reflect` | out | REFLECT (6) | model assumptions → deep critique before a high-stakes decision |
| `premortem` | out | REFLECT (6) | a finished valuation/budget → "how could this be wrong" failure modes |
| `game-theory-negotiation` | out | ADVISE | a valuation range / earnout → negotiation numbers (BATNA, ZOPA) |
| `intana-viz` | out | ANALYZE | diagnostic findings → structured-analytic visual (ACH, driver tree) |
| `strategic-foresight-viz` | both | ADVISE | scenario assumptions ↔ futures framing for the forecast |
| `cobesy` | out | ADVISE | finance findings → adoption/rollout plan for the org |
| `drawio` | out | MODEL/ANALYZE | model architecture or value-driver tree → diagram |
| `humanizer` (external) | out | any | the written narrative → de-AI'd prose ([github.com/blader/humanizer](https://github.com/blader/humanizer)) |

---

## Files

References (explanation + template specs):

- `references/intent-map.md`: the intent ontology; maps every topic to MODEL/ANALYZE/ADVISE/REFLECT with the layers to pull.
- `references/ebitda.md`: EBITDA definition, 4 KPIs, applications, improvement levers, adjusted EBITDA, controversies.
- `references/ratios-and-analysis.md`: full ratio formula set, common-size & trend analysis, breakeven, 6-step workflow, diagnostic reading.
- `references/three-statement-model.md`: the 50-sheet model map, schedule-driven IS/BS/CF, linking logic, granularity.
- `references/cash-flow-working-capital.md`: direct/indirect CF, 13-week forecast, NWC, cash conversion cycle, cash levers.
- `references/valuation-dcf-wacc.md`: DCF process, FCFF, WACC build-up, terminal value, method selection, value drivers, mistakes.
- `references/budgeting.md`: budgeting methods, cost-driver matrix, budget vs forecast vs plan.
- `references/modeling-best-practices.md`: 20-step build order and Bojan best-practice / do-and-don't list.
- `references/spreadsheet-conventions.md`: color coding, assumption sheet, validation checks, abbreviations, Claude-for-Excel notes.
- `references/auditability-and-math-rigor.md`: workflow lock, evidence ledger, formula trace protocol, false-precision rules, and model audit gates.

Assets (fill-in XLSX build specs):

- `assets/three-statement-model.md`: IS + BS + CF workbook spec with schedules and linking.
- `assets/budget-model.md`: driver-based annual budget spec (12 periods + FY).
- `assets/ratio-dashboard.md`: KPI / ratio dashboard spec with benchmark columns.
- `assets/thirteen-week-cashflow.md`: direct-method weekly cash forecast spec.
- `assets/dcf-wacc.md`: DCF + WACC build-up workbook spec with sensitivity table.
- `assets/ebitda-kpis.md`: EBITDA bridge + 4-KPI block spec.
