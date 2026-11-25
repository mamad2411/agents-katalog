# Skill: weighted-gdp-calculation — RL1C Public Contract Pin

## Tiny pin ledger
| Pin | Value |
| --- | --- |
| Artifact path | `/root/gdp.xlsx` |
| Required schema | Preserve existing workbook and sheets `Task` / `Data`; edit only family yellow cells; lookup formulas must reference `Data!`; result, stats, and weighted cells must be rounded to 1 decimal; weighted row must use `SUMPRODUCT` |
| Public acceptance check | `/tests/test.sh` recalculates with `ssconvert -S` and checks both workbook formulas and evaluated `Task`-sheet CSV values |

## Fast route
1. Read `/tests/test.sh`.
2. Read `/tests/test_outputs.py` only if it exists. If it is missing, continue from the prompt, workbook, and `test.sh` without stalling.
3. Inspect only small workbook regions needed to detect the variant and the labeled stats/weighted rows. Do not dump whole sheets or run long verbose scripts.
4. Write all family formulas into the existing workbook in one pass and save.
5. Reopen only the produced artifact and verify the pinned contract before finalizing. If available, mirror the public check with `ssconvert -S /root/gdp.xlsx /root/sheet.csv`.

## Variant map
- Net exports as % of GDP
  - Source rows: `Data!21:40`
  - Lookup blocks: `H12:L17`, `H19:L24`, `H26:L31`
  - Country result block: `H35:L40`
  - Country formula: `ROUND((Exports-Imports)/GDP*100,1)`
  - Weighted mean weights: GDP block
- Trade Balance Coefficient
  - Source rows: `Data!21:33`
  - Lookup blocks: `H12:M17`, `H19:M24`
  - Country result block: `H28:M33`
  - Country formula: `ROUND((Exports-Imports)/(Exports+Imports)*100,1)`
  - Weighted mean weights: `Exports + Imports`

## Stable lookup contract
- Series code key: `Task` column `D`
- Year key: `Task` row `10`
- Source series codes: `Data` column `B`
- Source year headers: `Data` row `4`
- Use only the year-value matrix in `INDEX`, not the whole data table

Write the top-left formula for each lookup block, then fill across and down:

- 5-year net-exports blocks:
  - `=INDEX(Data!$H$21:$L$40,MATCH($D12,Data!$B$21:$B$40,0),MATCH(H$10,Data!$H$4:$L$4,0))`
- 6-year trade-balance blocks:
  - `=INDEX(Data!$H$21:$M$33,MATCH($D12,Data!$B$21:$B$33,0),MATCH(H$10,Data!$H$4:$M$4,0))`

## Derived formulas
Country-result anchors:
- Net exports top-left:
  - `=ROUND((H12-H19)/H26*100,1)`
- Trade balance top-left:
  - `=ROUND((H12-H19)/(H12+H19)*100,1)`

Fill across years and down all six countries with same-row references only.

## Statistics
Find the six labeled summary rows directly below the country-result block and fill each year column from that year’s 6-country result range only:

- Min: `=ROUND(MIN(col_range),1)`
- Max: `=ROUND(MAX(col_range),1)`
- Median: `=ROUND(MEDIAN(col_range),1)`
- Simple mean: `=ROUND(AVERAGE(col_range),1)`
- 25th percentile: `=ROUND(PERCENTILE.INC(col_range,0.25),1)`
- 75th percentile: `=ROUND(PERCENTILE.INC(col_range,0.75),1)`

Use the actual labeled target rows from the sheet; do not guess from memory if the labels are shifted.

## Weighted mean
Use one year-column at a time:

- Net exports:
  - `=ROUND(SUMPRODUCT(H35:H40,H26:H31)/SUM(H26:H31),1)`
- Trade balance:
  - Prefer the `ssconvert`-safe split form:
  - `=ROUND((SUMPRODUCT(H28:H33,H12:H17)+SUMPRODUCT(H28:H33,H19:H24))/(SUM(H12:H17)+SUM(H19:H24)),1)`

Fill across all year columns.

## Anti-failure patches
- Do not rely on cached values from `openpyxl`; formulas must survive `ssconvert`.
- Do not replace the workbook, add sheets, or add macros.
- Keep inspection tiny; repeated failures came from oversized reads and long scripts.
- Do not finalize from an inspector or helper tool. The last meaningful action must leave `/root/gdp.xlsx` saved and complete.

## Final pinned verification
Reopen `/root/gdp.xlsx` and confirm:
- `Task` and `Data` still exist.
- A representative lookup cell contains `Data!` and `MATCH(`.
- A representative result/stat cell contains `ROUND(`.
- The weighted cell contains `SUMPRODUCT(`.
- If mirrored with `ssconvert`, the `Task` CSV shows numeric values in result, stats, and weighted cells.

Only then finalize.
