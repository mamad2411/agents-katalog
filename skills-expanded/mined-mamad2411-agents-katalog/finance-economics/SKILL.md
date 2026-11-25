---
name: finance-economics
description: |
  Finance and economics workflows: statement extraction, valuation math,
  time-series detrending/correlation, fraud indicators, and market/energy
  pricing tables. Use for DCF-like calculations, SEC/PDF financial extraction,
  GDP/econ series, and spreadsheet-based financial models — not for generic
  tabular ML or office formatting where the financial semantics don't matter.
---

# finance-economics

Load `safe-agent-scope` before any state-changing action; finance workflows do not waive sandbox, recipient, or injection rules.

## Why

Financial graders check **formulas, signs, units ($ vs $mm), and auditability**.
Pretty formatting without correct links/formulas fails. Prefer transparent
cell logic over opaque pasted values.

## Procedure

1. **Clarify the metric** — NPV, return, correlation, fraud score, price — and
   the exact output schema.
2. **Source hygiene** — when extracting from PDFs/tables, keep a traceable
   mapping from source → number.
3. **Model structure** — inputs (blue) vs formulas (black) when building sheets;
   no hardcoded rates inside long formulas.
4. **Signs & periods** — cash outflows negative if the convention says so;
   align fiscal periods before joining series.
5. **Checks** — balance identities, totals, and a quick sensitivity smoke.
6. **Export** — required file name/format; run `verify-task-output`.

## Heuristics

- Prefer vectorized pandas/numpy for econ series; plot only if asked
- For fraud/risk, report precision/recall-style metrics if evaluation implies detection quality
- Currency units in headers always

## Anti-patterns

- Hardcoding a "known" ticker price from parametric memory when a file is provided
- Breaking spreadsheet formulas into dead values
- Mixing nominal and real series without adjustment
