# Skill: weighted-gdp-calculation — L2A3

Use an acceptance-first workbook workflow. The scored artifact is the existing `/root/gdp.xlsx`. The verifier recalculates it with `ssconvert -S` and reads evaluated `Task`-sheet CSV values plus workbook formulas. `openpyxl` cached values are not enough.

## Artifact ledger

| Artifact | Minimum contract | Create owner | Check owner | Repair owner | Finalizer minimum restore |
| --- | --- | --- | --- | --- | --- |
| `/root/gdp.xlsx` | Preserve workbook, sheet order, and sheets `Task` / `Data`; write formulas only into family target cells; no replacement workbook, no new sheets/macros | Build | Build + Mirror | Repair | Reopen, rewrite all family formula cells for detected variant, save |
| `/root/sheet.csv.*` | Fresh `ssconvert -S` export exists and Task CSV shows evaluated numeric outputs where verifier reads them | Mirror | Mirror | Repair | If workbook is already correct, one last `ssconvert` run |

## Node: Contract

- Start with `read_tests` once if visible. If visible tests are partial or missing, do not hunt guessed test paths; use the family contract below and proceed.
- Preserve the existing workbook exactly except for family-owned yellow cells.
- Keep `Task` intact because CSV sheet selection uses workbook order/content fallback.
- Do not hard-code final numbers.
- Use `python` for workbook inspection/writes and `shell` for `ssconvert`. Do not spend steps on ad-hoc spreadsheet tools or repeated local test runs.

## Node: Scaffold

Use one `python` inspection pass on `/root/gdp.xlsx` to detect the variant and map the output rows.

Stable family keys:
- `Task` series-code column: `D`
- `Task` year header row: `10`
- `Data` series-code column: `B`
- `Data` year header row: `4`

Variant map:
- Net-exports-as-%-of-GDP:
  - source rows `Data!21:40`
  - lookup blocks `H12:L17`, `H19:L24`, `H26:L31`
  - result block `H35:L40`
- Trade-balance-coefficient:
  - source rows `Data!21:33`
  - lookup blocks `H12:M17`, `H19:M24`
  - result block `H28:M33`

Critical compute patch:
- Do not infer exports/imports/GDP from fixed `Data` subrows or manual reads.
- Always use a two-condition lookup by series code and year across the full family source span.

Map summary rows by scanning labels in columns `A:G` just below the result block:
- `min`
- `max`
- `median`
- `mean` or `average`
- `25`, `q1`, or `first quartile`
- `75`, `q3`, or `third quartile`
- `weighted`

## Node: Build

In that same `python` pass, write all family formulas with `openpyxl`, save once, then reopen with `data_only=False` and confirm representative cells contain formula strings.

### 1) Lookup blocks

Use only the `Data` year-value matrix in `INDEX`.

Net-exports template:
- top-left formula pattern: `=INDEX(Data!$H$21:$L$40,MATCH($D12,Data!$B$21:$B$40,0),MATCH(H$10,Data!$H$4:$L$4,0))`

Trade-balance template:
- top-left formula pattern: `=INDEX(Data!$H$21:$M$33,MATCH($D12,Data!$B$21:$B$33,0),MATCH(H$10,Data!$H$4:$M$4,0))`

Rules:
- write the formula into each block’s top-left cell and fill the whole block
- lock all `Data` ranges
- keep the `Task` row reference relative down rows
- keep the year reference relative across columns

### 2) Country result block

Net-exports:
- top-left result formula: `=ROUND((H12-H19)/H26*100,1)`

Trade-balance:
- top-left result formula: `=ROUND((H12-H19)/(H12+H19)*100,1)`

Rules:
- fill across all year columns and down all six country rows
- keep same-row references only
- keep `*100` inside the formula
- keep `ROUND(...,1)`

### 3) Summary statistics

For each mapped statistic row and each year column, use only that year’s six-country result range.

Write:
- min → `=ROUND(MIN(result_col_range),1)`
- max → `=ROUND(MAX(result_col_range),1)`
- median → `=ROUND(MEDIAN(result_col_range),1)`
- mean/average → `=ROUND(AVERAGE(result_col_range),1)`
- 25th percentile → `=ROUND(PERCENTILE.INC(result_col_range,0.25),1)`
- 75th percentile → `=ROUND(PERCENTILE.INC(result_col_range,0.75),1)`

### 4) Weighted mean

Net-exports weighted by GDP:
- `=ROUND(SUMPRODUCT(result_col,gdp_col)/SUM(gdp_col),1)`

Trade-balance weighted by total trade:
- `=ROUND((SUMPRODUCT(result_col,exports_col)+SUMPRODUCT(result_col,imports_col))/(SUM(exports_col)+SUM(imports_col)),1)`

Use the two-`SUMPRODUCT` trade formula; it is safer than inline array addition.

## Node: Mirror

Run one `shell` mirror:
- `ssconvert -S /root/gdp.xlsx /root/sheet.csv`

Do only a compact check after that:
- at least one `/root/sheet.csv.*` exists
- the Task CSV representative result/statistic/weighted cells are numeric

Do not use `openpyxl` to judge recalculated numeric outputs.

## Node: Repair

Only if representative formulas are missing or the CSV mirror is missing/non-numeric.

Repair suspects:
- wrong variant width
- wrong `Data` row span
- lookup not using series code + year
- missing `*100` or missing `ROUND(...,1)`
- wrong weighted weights
- statistic rows not mapped from labels

Repair rule:
- rewrite all family-owned cells in one `python` pass
- save
- rerun `ssconvert` once
- recheck only representative formula presence plus CSV numerics

## Node: Finalizer

- After the first successful mirror, finalize immediately.
- Do not spend late steps on browsing workbook ranges, repeated inspections, or local `run_tests`.
- If the runtime leaves one last action and formulas are already written, use that last action on the `ssconvert` mirror only if it is missing or stale; otherwise give the final answer immediately.

## Route

1. `read_tests` once if available.
2. One `python` pass to inspect workbook geometry, detect variant, map labels, write every formula, save, and verify representative formula strings.
3. One `shell` `ssconvert -S /root/gdp.xlsx /root/sheet.csv`.
4. If mirror is obviously bad, one `python` full rewrite and one final `shell` mirror.
5. Finalize.
