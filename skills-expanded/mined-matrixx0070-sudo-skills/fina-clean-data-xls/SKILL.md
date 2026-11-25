---
name: fina-clean-data-xls
version: 1.0.0
description: Turns a messy raw financial export into a tidy, type-correct, unit-normalized, reconciled spreadsheet table ready to feed a model, with a repeatable cleaning log.
author: matrixx0070
tags: [finance, data-cleaning, excel, spreadsheet, etl, normalization, reconciliation]
capabilities: []
---

# Clean Financial Data in a Spreadsheet

## When to use
Use this when you have a raw financial extract (a downloaded trial balance, a pasted 10-K table, a bank or ERP export, a broker CSV) that is not yet trustworthy: numbers stored as text, mixed date formats, merged cells, footnote markers, blended units, and totals that do not tie. You clean and reconcile it into one tidy table before any modeling touches it.

**Not for:** building the model layout or formulas on the clean data (use fina-xlsx-author), constructing linked statements (use fina-3-statement-model), or checking someone else's finished workbook (use fina-audit-xls).

## Method
1. **Snapshot the source first.** Copy the raw extract onto a tab named `raw` and never edit it. All cleaning happens on a separate `clean` tab so you can always diff against the original and re-run the process. Record the source name, retrieval date, and reported units/currency in a header block.
2. **Profile every column before touching it.** For each column check: is it text or number, what date formats appear, are there trailing spaces, currency symbols, thousands separators, parentheses-negatives, or footnote markers. Decision point: if more than about 20 percent of a column is malformed or the same defect repeats predictably, build a Power Query transform instead of cell-level fixes so the cleaning is repeatable on the next export.
3. **Fix data types.** Strip formatting artifacts, then coerce to true numbers and true dates. Use `TRIM`, `CLEAN`, `SUBSTITUTE` to remove spaces, currency symbols, and thousands separators; `VALUE` to convert text-numbers; `DATEVALUE` (or Text-to-Columns / Power Query typed columns) to convert text-dates. Convert `(1,234)` accounting negatives to `-1234`.
4. **Handle blanks and nulls deliberately.** Distinguish a true zero from a missing value from a suppressed value. Decision point: leave a genuine unknown as empty (never fill with 0, which corrupts sums and averages) but replace a reported dash or "n/a" that means zero with an explicit 0, and log which rule you applied per column.
5. **Normalize units and periods.** Bring every monetary column to one unit (for example actual dollars, not a mix of thousands and millions) and one currency. Standardize period labels to one convention (for example `2024-Q1` or fiscal-year-end dates) so periods sort and join correctly.
6. **Dedupe records.** Define the natural key (for example account + period, or transaction id) and remove exact and near-duplicate rows, keeping the authoritative one. Keep a count of rows removed.
7. **Reconcile to the source.** Sum the cleaned column and tie it back to the reported total or control figure. If it does not tie to the cent (or to a stated rounding tolerance), stop and find the break before proceeding.
8. **Restructure into tidy data.** One record per row, one variable per column, a single header row, no merged cells, no blank spacer rows or columns, no repeated group headers embedded in the data.
9. **Write the cleaning log.** Record every transformation applied so the whole process is auditable and repeatable on the next refresh.

## Example
Raw pull from an ERP trial balance, `raw` tab:

| Account         | Q1 2024 |
|-----------------|---------|
| Revenue         | "1,234 " |
| COGS            | (500)   |
| Other  income¹  | –       |

Problems: the amount column is text (quotes, trailing space, thousands comma), COGS is a parentheses-negative, "Other income" carries a footnote marker and trailing spaces, and the dash is ambiguous. On the `clean` tab you apply `=VALUE(SUBSTITUTE(TRIM(A2),",",""))` to strip the comma and coerce, convert `(500)` to `-500`, `TRIM` and strip the `¹` marker from the label, and resolve the dash to `0` because the source footnote says "nil". Result:

| account       | period  | amount_usd |
|---------------|---------|-----------|
| Revenue       | 2024-Q1 | 1234      |
| COGS          | 2024-Q1 | -500      |
| Other income  | 2024-Q1 | 0         |

Reconciliation: sum of `amount_usd` = 734, which ties to the reported net of 734. Logged.

## Pitfalls
- **Silent text-numbers.** A number stored as text left-aligns and drops out of `SUM`, so a total looks right but understates. Coerce every numeric column with `VALUE` and confirm the count of numeric cells equals the row count.
- **Locale date flips.** `03/04/2024` is March 4 or April 3 depending on locale; guessing corrupts every time-series. Confirm the source locale and convert explicitly with `DATEVALUE` or typed Power Query columns.
- **Filling blanks with zero.** Replacing a true unknown with 0 poisons averages, growth rates, and reconciliations. Only substitute 0 where the source explicitly means nil.
- **Merged cells.** Merged headers and merged label cells break sorting, filtering, lookups, and pivots. Unmerge and repeat the value into every row.
- **Footnote markers glued to labels.** A trailing `¹` or `*` makes "Revenue*" and "Revenue" two different keys and breaks joins. Strip markers with `SUBSTITUTE`/`CLEAN` before keying.
- **Mixed units in one column.** Summing thousands and actual dollars together yields nonsense. Normalize units before any aggregation and reconcile after.
- **Editing the raw tab.** Once you overwrite the source you cannot re-run or prove the cleaning. Always work on a copy.

## Output format
```
Workbook: <source>_clean.xlsx
  Tab: raw            immutable copy of the source, header block (source, date, units, currency)
  Tab: clean          tidy table, one record per row, typed columns, normalized units/periods
  Tab: cleaning_log   ordered list of transformations + reconciliation result

clean tab columns (tidy):
  key... | period | metric | value_<unit> | flags

cleaning_log row shape:
  step | column | defect | transform_applied | rows_affected | tie_out
```

## Reference

### Common defects and detection
| Defect | How it looks | How to detect |
|--------|--------------|---------------|
| Text-stored number | left-aligned, ignored by SUM | `=ISNUMBER(cell)` false; `COUNT` < row count |
| Parentheses-negative | `(1,234)` as text | leading `(` present |
| Mixed date formats | `3/4/24` next to `2024-03-04` | `ISNUMBER` false on some dates |
| Trailing/leading spaces | `"Revenue "` | `=LEN(cell)<>LEN(TRIM(cell))` |
| Merged cells | one value spanning rows | Find & Select > merged cells |
| Footnote markers | `Revenue¹`, `Total*` | non-alphanumeric trailing chars |
| Currency/thousands glyphs | `$1,234`, `1 234` | non-digit chars inside numeric field |
| Ambiguous blank | `–`, `n/a`, empty | inspect source legend |

### Cleaning functions and tools
| Need | Function / step |
|------|-----------------|
| Remove leading/trailing/inner spaces | `TRIM` |
| Remove non-printable characters | `CLEAN` |
| Strip a glyph (comma, `$`, marker) | `SUBSTITUTE(text, "x", "")` |
| Text number to number | `VALUE` |
| Text date to date | `DATEVALUE` |
| Split one column into many | Text-to-Columns |
| Repeatable, refreshable pipeline | Power Query (Trim, Clean, Replace Values, Change Type, Remove Duplicates, Fill Down) |
| Repeat merged value down | Fill Down (Power Query) or unmerge + paste |
| Combine fixes | `=VALUE(SUBSTITUTE(TRIM(CLEAN(A2)),",",""))` |

### Unit and period normalization rules
- Pick one monetary unit for the whole table (actual currency units is safest) and divide/multiply columns to match; record the unit in the header and column name (`value_usd`).
- Convert foreign currency at a stated, dated rate; keep the rate and date in the log, never inline a magic number.
- Standardize periods to one sortable convention (`YYYY-Qn` or fiscal-year-end date); map "FY24", "2024A", "Q1'24" to it.
- Label actual vs. estimate/forecast explicitly so downstream models never mix them.

### Reconciliation checks
- Column total ties to the source-reported total within a stated rounding tolerance.
- Row count after dedupe = expected record count; log rows removed.
- Cross-foot: subtotals sum to the grand total.
- For statements, confirm the accounting identity where applicable (assets = liabilities + equity) before handing off to fina-3-statement-model.

### Tidy-data rules
- One record per row; one variable per column; one value per cell.
- Exactly one header row; unique, marker-free, machine-friendly column names.
- No merged cells, no blank spacer rows/columns, no embedded group headers or subtotals inside the data range.
- Keep raw, clean, and log on separate tabs so the process is auditable and re-runnable.
