---
name: xlsx
description: "Create, read, or edit spreadsheet files (.xlsx, .xlsm, .csv, .tsv) as the primary deliverable. Triggers on any task where the OUTPUT is a spreadsheet file: building from scratch, modifying an existing file, cleaning messy tabular data, adding columns/formulas/formatting/charts/pivots/conditional formatting/data validation, or converting between tabular formats. Triggers on casual file references ('the xlsx in my downloads', 'that CSV from the auditor', 'mi hoja de control'). Common workflows: financial models, compliance/control inventories, vendor risk registers, asset inventories, KPI dashboards, audit workpapers, bilingual (ES/EN) trackers. DO NOT trigger when the deliverable is: a Word doc (use docx), HTML report or web dashboard (use data:build-dashboard), publication-quality chart for a deck or report (use data:create-viz), warehouse SQL (use data:sql-queries), GAAP-formatted financial statements (use finance:financial-statements — it owns the structure; xlsx is just the substrate), Google Sheets API integration, or a standalone Python script. If a sibling skill is the better fit, defer and say so."
license: Proprietary. LICENSE.txt has complete terms
---

# xlsx — Spreadsheet Workhorse

## When to use vs. defer

| User asks for... | Use | Reason |
|---|---|---|
| "Build a vendor risk register / control inventory / asset inventory" | **xlsx** | Operational tracker, formulas + filters |
| "Clean up this messy CSV / fix this broken xlsx" | **xlsx** | File is the deliverable |
| "Add a pivot / conditional format / chart to file.xlsx" | **xlsx** | In-spreadsheet feature |
| "Generate Q3 P&L / Balance Sheet / Cash Flow" | **finance:financial-statements** | GAAP structure owns the logic; that skill calls xlsx as substrate |
| "Write the SQL to pull this from Snowflake/BQ" | **data:sql-queries** | Query authoring, not spreadsheet manipulation |
| "Make a publication-quality chart for the board deck" | **data:create-viz** | Matplotlib/plotly output, not in-Excel chart |
| "Build an interactive HTML dashboard" | **data:build-dashboard** | Web artifact, not xlsx |
| "Profile this dataset / find anomalies / outliers" | **data:explore-data** or **data:statistical-analysis** | Analysis, not spreadsheet authoring |

If the user says "spreadsheet" but the real ask is one of the deferrals above, route there and say so explicitly: "This is closer to finance:financial-statements — invoking that."

### Edge cases

| Situation | Decision |
|---|---|
| "Chart in xlsx, but I'll paste it into a deck" | **xlsx** for the file; if quality matters more than editability, also offer data:create-viz |
| "Spreadsheet of revenue by month" — could be P&L | If user wants raw data table → **xlsx**. If they want formatted statement with subtotals/GAAP order → **finance:financial-statements** |
| "Export query results to Excel" | **data:sql-queries** writes the query; **xlsx** receives the result if any post-processing is needed |
| "Make my CSV pretty" | **xlsx** (convert to .xlsx with formatting) |
| ".xlsm with macros" | **xlsx** — preserve the file with `keep_vba=True` in `load_workbook`; do not strip macros silently |
| "Google Sheet I exported" | **xlsx** — but warn that some Sheets-specific functions (`QUERY`, `IMPORTRANGE`, `ARRAYFORMULA`) won't survive |

---

## Hard requirements (every output)

1. **Zero formula errors** — no `#REF!`, `#DIV/0!`, `#VALUE!`, `#N/A`, `#NAME?`. Verify with `scripts/recalc.py`.
2. **Formulas, never hardcoded calculations** — if Python could compute it, an Excel formula MUST. Sums, percentages, ratios, growth rates: all live in cells.
3. **Preserve precision** — never round in Python before writing; let Excel format the display.
4. **Preserve dates as dates** — write `datetime` objects, not strings; format with `cell.number_format`.
5. **Preserve existing template conventions** — when editing, match the file's existing fonts/colors/structure. Existing patterns override these guidelines.
6. **Audit trail (SOX-relevant)** — for any financial/control workpaper: include a `Metadata` sheet with `Author`, `Date`, `Source`, `Version`, `SignedOff` cells. Cite hardcoded inputs with source comments.
7. **Recalculate before delivery** — `python scripts/recalc.py output.xlsx` and check the JSON; fix any reported errors.

---

## Capability Map

| Capability | Library | Pattern |
|---|---|---|
| Read tabular data | pandas | `pd.read_excel(path, sheet_name=None, dtype={'id': str}, parse_dates=['date'])` |
| Bulk write data | pandas | `df.to_excel(path, index=False, sheet_name='Data')` |
| Formulas + formatting | openpyxl | See "Formulas" + "Formatting" below |
| Multi-sheet workbook | openpyxl | `wb.create_sheet(name)`; cross-ref `=Sheet1!A1` |
| Charts (in-Excel) | openpyxl.chart | `BarChart`, `LineChart`, `PieChart`; add reference + categories |
| Pivot tables | openpyxl | Limited native; use formula-driven pivots (SUMIFS/COUNTIFS over a `Data` sheet) — see "Pivots" below |
| Conditional formatting | openpyxl.formatting.rule | `ColorScaleRule`, `CellIsRule`, `FormulaRule` — see "Conditional formatting" |
| Data validation | openpyxl.worksheet.datavalidation | Dropdowns, date ranges, integer bounds — see "Validation" |
| Filters + sorting | openpyxl | `sheet.auto_filter.ref = sheet.dimensions` |
| Freeze panes | openpyxl | `sheet.freeze_panes = 'A2'` (header row) or `'B2'` (header + first column) |
| Named ranges | openpyxl | `wb.defined_names['rate'] = DefinedName('rate', attr_text='Inputs!$B$2')` |

---

## Formulas (the core rule)

```python
# WRONG — hardcoded result
sheet['B10'] = df['Sales'].sum()

# RIGHT — let Excel compute
sheet['B10'] = '=SUM(B2:B9)'
```

Applies to totals, percentages, ratios, differences, weighted averages, growth, IRR, NPV — everything. Only inputs are hardcoded; everything else is a formula.

**Cross-sheet references**: `='Vendor Risk'!$D$5` (quote sheet names with spaces; absolute refs for assumption cells).

**Common safe patterns**:
- Sum: `=SUM(B2:B100)`
- Conditional sum: `=SUMIFS(Data!C:C, Data!A:A, "Critical")`
- Lookup: `=XLOOKUP(A2, Vendors!A:A, Vendors!E:E, "Not found")`
- Risk score: `=IFERROR(Likelihood*Impact, 0)` with named ranges
- Period-over-period: `=IFERROR((C5-B5)/B5, 0)` with `0` fallback to avoid `#DIV/0!`

---

## Formatting standards

### Fonts
Calibri 11 default unless the file already uses something else. Headers bold, 12pt. Never change a file's existing font when editing.

### Number formats
| Type | Format string |
|---|---|
| Currency (USD) | `"$#,##0;($#,##0);-"` (parens for negatives, dash for zero) |
| Percentage (1dp) | `"0.0%;(0.0%);-"` |
| Multiple | `"0.0\\x"` (e.g., 8.5x) |
| Date | `"yyyy-mm-dd"` (ISO; sortable; bilingual-safe) |
| Year as text | `"0"` then write as int 2024 (not "2,024") |
| Bilingual currency | Headers carry the unit: `Ingresos / Revenue ($mm)` |

### Color coding (financial models)
- **Blue (`0000FF`)**: hardcoded inputs / scenario knobs
- **Black (`000000`)**: formulas
- **Green (`008000`)**: links to other sheets in same workbook
- **Red (`FF0000`)**: external workbook links
- **Yellow fill (`FFFF00`)**: assumptions needing review

### RAG / risk palette (compliance + risk trackers)
- **Red (`E06666`)**: Critical / Open / High risk / Non-compliant
- **Amber (`F6B26B`)**: Medium / In progress / Partially compliant
- **Green (`93C47D`)**: Low / Closed / Compliant
- **Gray (`CCCCCC`)**: N/A or not assessed

Apply via conditional formatting (below), not manual fills, so updates re-color automatically.

---

## Conditional formatting (recipes)

```python
from openpyxl.formatting.rule import ColorScaleRule, CellIsRule, FormulaRule
from openpyxl.styles import PatternFill, Font

# Heatmap on risk scores (1-25)
sheet.conditional_formatting.add(
    'F2:F100',
    ColorScaleRule(start_type='num', start_value=1,  start_color='93C47D',
                   mid_type='num',   mid_value=12,   mid_color='F6B26B',
                   end_type='num',   end_value=25,   end_color='E06666')
)

# RAG by status text
red  = PatternFill('solid', start_color='E06666')
amber= PatternFill('solid', start_color='F6B26B')
green= PatternFill('solid', start_color='93C47D')
sheet.conditional_formatting.add('D2:D100', CellIsRule(operator='equal', formula=['"Open"'],         fill=red))
sheet.conditional_formatting.add('D2:D100', CellIsRule(operator='equal', formula=['"In Progress"'], fill=amber))
sheet.conditional_formatting.add('D2:D100', CellIsRule(operator='equal', formula=['"Closed"'],     fill=green))

# Highlight overdue rows (date col B, today comparison)
sheet.conditional_formatting.add(
    'A2:Z100',
    FormulaRule(formula=['AND($B2<TODAY(), $D2<>"Closed")'], fill=red)
)
```

---

## Data validation (dropdowns, bounds)

```python
from openpyxl.worksheet.datavalidation import DataValidation

# Status dropdown — bilingual safe
dv = DataValidation(type='list', formula1='"Open,In Progress,Closed,N/A"', allow_blank=True)
sheet.add_data_validation(dv)
dv.add('D2:D1000')

# Risk score 1-5 integer only
dv2 = DataValidation(type='whole', operator='between', formula1=1, formula2=5, errorTitle='Bad score', error='Use 1-5')
sheet.add_data_validation(dv2); dv2.add('E2:F1000')

# Reference list from another sheet (cleaner for long lists)
dv3 = DataValidation(type='list', formula1='=Lists!$A$2:$A$50')
sheet.add_data_validation(dv3); dv3.add('B2:B1000')
```

---

## Charts (in-Excel)

```python
from openpyxl.chart import BarChart, LineChart, PieChart, Reference
from openpyxl.chart.label import DataLabelList

# Bar: KPI by category
chart = BarChart()
chart.type = 'col'; chart.style = 11
chart.title = 'Open Findings by Severity'
chart.y_axis.title = 'Count'; chart.x_axis.title = 'Severity'
data  = Reference(sheet, min_col=2, min_row=1, max_col=2, max_row=5)  # headers in row 1
cats  = Reference(sheet, min_col=1, min_row=2, max_row=5)
chart.add_data(data, titles_from_data=True)
chart.set_categories(cats)
chart.dataLabels = DataLabelList(showVal=True)
sheet.add_chart(chart, 'D2')

# Line: MRR trend
line = LineChart(); line.title = 'MRR Trend'
line.y_axis.title = 'MRR ($)'; line.x_axis.title = 'Month'
line.add_data(Reference(sheet, min_col=2, min_row=1, max_row=13), titles_from_data=True)
line.set_categories(Reference(sheet, min_col=1, min_row=2, max_row=13))
sheet.add_chart(line, 'E2')
```

For board-quality output that needs custom typography or annotations: defer to **data:create-viz**.

---

## Named ranges + freeze panes + filters

```python
from openpyxl.workbook.defined_name import DefinedName

# Named range for an assumption (cleaner formulas)
wb.defined_names['tax_rate'] = DefinedName('tax_rate', attr_text="Inputs!$B$2")
sheet['C5'] = '=B5*(1-tax_rate)'

# Freeze the header row + first column
sheet.freeze_panes = 'B2'

# Auto-filter on the data range
sheet.auto_filter.ref = sheet.dimensions  # entire used range
```

---

## Pivots (formula-driven, since openpyxl pivots are fragile)

For control inventories / vendor lists / asset registers, build a `Summary` sheet that uses `SUMIFS`/`COUNTIFS`/`UNIQUE` against the `Data` sheet. This survives round-trips through Excel/Numbers/Google Sheets better than openpyxl's native pivot writer.

```python
# Summary sheet pattern
sheet['A1'] = 'Status'; sheet['B1'] = 'Count'; sheet['C1'] = 'Critical Count'
sheet['A2'] = 'Open'
sheet['B2'] = '=COUNTIF(Data!D:D, A2)'
sheet['C2'] = '=COUNTIFS(Data!D:D, A2, Data!E:E, "Critical")'
```

If the user explicitly needs a real PivotTable object, say so and offer to build the formula-driven version OR open the file in Excel and create the pivot manually with documented steps.

---

## Domain templates

### Vendor risk register
Sheets: `Vendors`, `Risk Scoring`, `Summary`, `Metadata`.

`Vendors` columns: `Vendor | Service | Data Sensitivity (1-5) | Likelihood (1-5) | Impact (1-5) | Risk Score | RAG | Owner | Last Review | Next Review | SOC2 | DPA Signed | Notes`

Risk score formula: `=D2*E2` (impact × likelihood, conditional formatted as heatmap).
RAG: `=IF(F2>=15,"High",IF(F2>=8,"Medium","Low"))`.
Validation: dropdowns on Data Sensitivity / Likelihood / Impact (1-5), SOC2 (Yes/No/Unknown).

### Control inventory (SOC2 / ISO27001)
Sheets: `Controls`, `Tests`, `Evidence`, `Summary`, `Metadata`.

`Controls` columns: `Control ID | Framework | Control Family | Description | Owner | Status | Last Tested | Next Test Due | Evidence Link | Exception?`

Conditional format: overdue tests turn red via `FormulaRule` on `Next Test Due < TODAY()`.

### Asset inventory
Sheets: `Assets`, `Summary`, `Metadata`.

`Assets`: `Asset ID | Type | Owner | Location | Criticality | Data Class | Lifecycle Stage | Acquired | Last Audit | Notes`

Filter on `Type`/`Criticality`; `Summary` sheet uses `COUNTIFS` to roll up.

---

## Bilingual (ES/EN) headers

For PR / mixed audiences, use bilingual headers in one row:

```
Vendor / Proveedor | Service / Servicio | Risk Score / Puntaje de Riesgo
```

Keep formulas referencing column letters (not header text) so language toggle never breaks math. For dropdown values, prefer language-neutral codes (Open/Closed) or include both: `Abierto / Open`.

---

## Workflows

### Create new
1. Choose tool (pandas for bulk data; openpyxl for formulas/format).
2. Build sheets in order: `Inputs/Assumptions` → `Data` → `Calculations` → `Summary` → `Metadata`.
3. Apply formatting + validation + conditional formatting.
4. `wb.save(path)`.
5. `python scripts/recalc.py path` → verify zero errors.
6. Open in headless LibreOffice once to sanity-check (optional but recommended for >3 sheets).

### Edit existing — INSPECT FIRST

**Mandatory first step before any edit**: load and inspect.

```python
from openpyxl import load_workbook
wb = load_workbook(path)  # NOT data_only=True — destroys formulas on save
for name in wb.sheetnames:
    s = wb[name]
    print(f'\n=== {name} ({s.max_row}r x {s.max_column}c) ===')
    for row in s.iter_rows(min_row=1, max_row=min(5, s.max_row), values_only=False):
        print([(c.coordinate, c.value, c.number_format) for c in row])
print('Merged ranges:', {n: list(wb[n].merged_cells.ranges) for n in wb.sheetnames})
print('Defined names:', list(wb.defined_names))
```

Then:
1. Identify existing fonts, fills, header style, number formats — match them.
2. Check for merged cells in your edit range (they break inserts/deletes — unmerge, edit, re-merge).
3. Check for tables (`ListObject`) and named ranges that auto-extend.
4. Modify; save; `python scripts/recalc.py path`; fix any new errors.
5. If you inserted/deleted rows, scan formulas in dependent sheets for `#REF!`.

### Round-trip safety (Excel ↔ Numbers ↔ Google Sheets)

Most users open xlsx in mixed clients. Avoid:
- `LET`, `LAMBDA`, `XLOOKUP` with wildcards (newer Excel only — Numbers chokes)
- `_xlfn.` dynamic-array functions when targeting older Excel/Numbers
- Conditional formatting using `INDIRECT` (renders inconsistently in Sheets)
- Custom number formats with non-ASCII (Numbers may strip)

Prefer: `IF`/`SUMIFS`/`COUNTIFS`/`VLOOKUP` (universally portable), ISO date format `yyyy-mm-dd`, ASCII-only number formats.

### Read / analyze
- Quick: `pd.read_excel(path, sheet_name=None)` → dict of DataFrames.
- Preserve formulas while reading: `load_workbook(path)` then `cell.value` returns the formula string; `load_workbook(path, data_only=True)` returns last-cached value (read-only — never save).

---

## Recalc + verify

```bash
python scripts/recalc.py output.xlsx
```

Returns JSON. If `status == "errors_found"`, the `error_summary` lists `#REF!`/`#DIV/0!`/etc. with cell locations. Fix and re-run until `status == "success"`.

Common fixes:
- `#DIV/0!` → wrap denominators: `=IFERROR(A2/B2, 0)`
- `#REF!` → a row/col was deleted; re-point the formula
- `#NAME?` → typo in function name or missing named range
- `#VALUE!` → text where number expected; check `cell.data_type`

---

## Code style

Python: minimal, no narration comments. In-cell comments: yes, for complex formulas, key assumptions, and source citations on hardcoded inputs.

Source-citation format (in cell comment or column to the right):
`Source: [System], [Date], [Reference], [URL if any]`

Examples:
- `Source: AWS Console, 2026-04-15, EC2 inventory export`
- `Source: Vendor SOC2 report, 2026-Q1, Section 3.2`
- `Source: 10-K, FY2024, p.45 Revenue Note, [SEC EDGAR URL]`
