# U11-CLEAN Skill: weighted workbook GDP/trade calculation

## Output contract
- Artifact: the edited visible `gdp.xlsx` workbook at the provided path.
- Type/schema: preserve the existing workbook and sheets; fill only the task-requested yellow cells on the existing sheets.
- Count/unit: complete all required lookup ranges, per-country metric cells, summary-stat cells, and the weighted-mean cell. Percentage outputs must be scaled by 100 and rounded to 1 decimal so they display like `12.3`, not `0.123`.
- Invariants: no new sheets, no macros/VBA, no format/style changes.

## Route
1. Read the visible instruction and inspect the workbook with `excel_inspect_workbook`. Use `excel_read_range` to map:
   - the target yellow ranges,
   - the year header row,
   - the series-code column,
   - the source rows on `Data`,
   - the visible labels for summary outputs and weighted mean.
2. Make a small internal ledger with one row per required slot/block:
   - each lookup-filled yellow block,
   - each derived metric block,
   - each summary-stat target,
   - the weighted-mean target,
   - the formatting/no-new-sheet invariants.
3. Reserve the artifact early by treating the provided `gdp.xlsx` as the only source of truth and writing the first valid formulas as soon as the block mapping is clear.
4. Fill lookup blocks with workbook formulas via `excel_write_formulas`, using a two-condition lookup driven by:
   - series code from the task sheet, and
   - year from the header row.
   Use an allowed lookup pattern such as `INDEX/MATCH`, `XLOOKUP/MATCH`, or the prompt-permitted equivalent. Confirm one anchor cell first, then copy the pattern across/down.
5. Infer the calculation path from the visible prompt:
   - If the task asks for net exports relative to GDP, compute per-country values from exports, imports, and GDP, then compute the GCC weighted mean with `SUMPRODUCT` using GDP weights.
   - If the task asks for Trade Balance Coefficient, compute `(Exports - Imports) / (Exports + Imports)`, then compute the GCC weighted mean with `SUMPRODUCT` using total-trade weights.
   In both routes, keep the visible task-sheet blocks as the evidence chain for downstream formulas.
6. Fill the descriptive statistics by matching the visible labels to standard Excel formulas on the per-country metric range for each year/column: min, max, median, simple mean, 25th percentile, 75th percentile.
7. Recalculate with `excel_recalculate`. If `weighted_gdp_calculate` clearly matches the visible contract, it may be used as an accelerator, but still validate placement and formulas afterward.

## Ledger
For every filled slot, keep one visible justification:
- source anchor from `Data`,
- deterministic formula from already-filled task cells,
- or a concrete workbook write/recalc operation.

If any slot is still ambiguous, keep it conservative only briefly and resolve it from visible sheet labels/ranges before copying formulas broadly.

## Public readback and spot-check
Before finalizing, do one visible readback pass:
- Use `excel_formula_dump` on representative cells from:
  - the first lookup block,
  - another copied lookup cell,
  - one derived metric cell,
  - one summary cell,
  - the weighted-mean cell.
- Use `excel_read_range` to confirm recalculated numeric outputs appear in the expected targets.
- If available, use `excel_style_check` to confirm styles stayed intact.
- Spot-check the most fragile item:
  - one lookup cell must reflect the intended series-code/year logic, and
  - the weighted-mean formula must use the correct weight base with only one percentage scaling.

## Last-write rule
Near the step cap, make the workbook itself final: perform the last needed `excel_write_formulas` or `excel_recalculate` so the on-disk `gdp.xlsx` is the most complete, schema-valid artifact.

## RL1C Public Contract Pin Delta
Before any long tool action, pin the prompt-visible artifact path, required schema or fields, and one public acceptance check in a tiny ledger. After writing the artifact, reread only the produced artifact and verify the pinned public contract before finalizing.
