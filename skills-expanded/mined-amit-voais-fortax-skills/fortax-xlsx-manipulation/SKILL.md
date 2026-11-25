---
name: fortax-xlsx-manipulation
description: Build or edit an Excel workbook with Python (openpyxl) the way a CA's working paper should be - live formulas instead of pasted values, an assumptions block, Indian number formats (1,00,000 and Rs), check cells that must show 0, a Source column, conditional formatting, dropdowns, charts, frozen headers - and verify it recalculates without errors before handing it over. For computations, schedules, reconciliations, MIS, lead schedules and any workbook the other Fortax skills produce. Typical asks - "Excel bana do formulas ke saath", "is sheet me total aur check lagao", "lakh format me dikhao", "dropdown daalo", "chart add karo", "is workbook ko clean karo".
license: Apache-2.0
metadata:
  author: Fortax
  version: "1.0.0"
  homepage: https://github.com/amit-voais/fortax-skills
  credits: "openpyxl techniques and examples adapted from claude-office-skills/skills, https://github.com/claude-office-skills/skills (MIT)"
---

# Excel workbooks with live formulas

Create and edit .xlsx files with **openpyxl** (`pip install openpyxl`). Write the Python, run it, then
verify the result. The workbook is the working paper: a reviewer must be able to click any figure and see
where it comes from.

## Rules for a Fortax workbook

1. **Formulas, not values.** Every total, difference, tax, percentage and check is an Excel formula
   (`=SUM(D2:D40)`), never a number computed in Python and pasted. Inputs are the only typed numbers.
2. **Assumptions block.** Rates, thresholds, dates and other inputs sit in one labelled block (a sheet
   `Inputs` or the top rows), each with its source ("s.40A(3), Income-tax Act 1961 — confirm", "kb,
   captured 2026-08-01"). Formulas refer to those cells (or named ranges), never to a rate typed inside a
   formula.
3. **Inputs look different:** blue font for typed inputs, black for formulas (the usual convention);
   say so in a legend.
4. **Check cells.** Each sheet that must tie has a check row that must be 0 or TRUE (debits - credits,
   total assets - total liabilities, reconciliation difference), with conditional formatting that turns
   red when it is not.
5. **Source column** on every data row: file, sheet/page, row or voucher number.
6. **Indian formats:** amounts with lakh grouping, dates dd-mm-yyyy, and the period and entity in the
   sheet title.
7. **Do not destroy the client's file.** Edit a copy (`<name>_working.xlsx`), never overwrite the
   original; keep their sheets, formats and formulas.
8. **Verify before handing over** (below). A workbook with `#REF!` or a non-zero check is not done.
9. No client names in examples; made-up names (Sharma Traders).

## Fundamentals

```python
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.chart import BarChart, Reference

wb = Workbook()          # new workbook
ws = wb.active

wb = load_workbook("existing.xlsx")   # open existing (formulas kept as formulas)
ws = wb["Sheet1"]
```

Structure:
```
Workbook
  worksheets (sheets / tabs)
    cells (data), rows / columns (formatting), merged cells, charts
  defined_names (named ranges)
  styles
```

### Cells

```python
ws["A1"] = "Header"
ws["B1"] = 42
ws.cell(row=1, column=3, value="Data")
ws.append(["Row", "Data", "Here"])          # next empty row

value = ws["A1"].value
for row in ws.iter_rows(min_row=2, max_row=10, min_col=1, max_col=3):
    for cell in row:
        print(cell.coordinate, cell.value)
```

Note: `ws["A1:C1"] = [...]` does not assign a range; write cell by cell or use `append`.

### Formulas and named ranges

```python
ws["D1"] = "=SUM(A1:C1)"
ws["D2"] = "=AVERAGE(A2:C2)"
ws["E1"] = '=IF(D1>100,"High","Low")'

from openpyxl.workbook.defined_name import DefinedName
wb.defined_names["GST_RATE"] = DefinedName("GST_RATE", attr_text="Inputs!$B$3")  # openpyxl 3.1+
ws["F2"] = "=E2*GST_RATE"
```

Use English function names and commas as separators. openpyxl does not calculate formulas — the values
appear when Excel / LibreOffice opens and recalculates the file (see Verify).

### Formatting

```python
ws["A1"].font = Font(name="Arial", size=12, bold=True, color="FFFFFF")
ws["A1"].fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
thin = Side(style="thin")
ws["A1"].border = Border(left=thin, right=thin, top=thin, bottom=thin)
ws["A1"].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
ws["B2"].font = Font(color="0000FF")      # typed input
```

### Number formats (Indian)

```python
LAKH = '[>=10000000]##\\,##\\,##\\,##0.00;[>=100000]##\\,##\\,##0.00;##,##0.00'
ws["B2"].number_format = LAKH                 # 1,23,45,678.00 — positive numbers
ws["B3"].number_format = '"Rs "#,##0.00'      # simple rupee format (international grouping)
ws["C2"].number_format = "0.00%"
ws["D2"].number_format = "DD-MM-YYYY"
ws["E2"].number_format = '#,##0.00 "units"'
```

The lakh format uses conditional sections, so it cannot also carry a negative section; for columns
that go negative, show negatives in a separate Dr/Cr column or use `#,##0.00;(#,##0.00)`. Do not use the
`$` formats from generic examples.

### Conditional formatting

```python
from openpyxl.formatting.rule import ColorScaleRule, CellIsRule, FormulaRule
red = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")

ws.conditional_formatting.add("H50", CellIsRule(operator="notEqual", formula=["0"], fill=red))  # check cell
ws.conditional_formatting.add("F2:F200", FormulaRule(formula=["ABS(F2)>Inputs!$B$5"], fill=red))  # over threshold
ws.conditional_formatting.add("G2:G200", ColorScaleRule(start_type="min", start_color="F8696B",
                                                       end_type="max", end_color="63BE7B"))
```

### Data validation (dropdowns, ranges)

```python
from openpyxl.worksheet.datavalidation import DataValidation
dv = DataValidation(type="list", formula1='"Timing,Adjustment,Investigate"', allow_blank=True)
dv.error, dv.errorTitle = "Pick from the list", "Invalid category"
ws.add_data_validation(dv)
dv.add("J2:J500")

dv_rate = DataValidation(type="decimal", operator="between", formula1="0", formula2="0.28")
ws.add_data_validation(dv_rate)
dv_rate.add("Inputs!B3")
```

### Charts

```python
from openpyxl.chart import BarChart, LineChart, PieChart, Reference
data = Reference(ws, min_col=2, min_row=1, max_col=3, max_row=13)
cats = Reference(ws, min_col=1, min_row=2, max_row=13)

bar = BarChart(); bar.type = "col"; bar.title = "Sales by month"
bar.add_data(data, titles_from_data=True); bar.set_categories(cats)
ws.add_chart(bar, "E2")

line = LineChart(); line.title = "Trend"
line.add_data(data, titles_from_data=True); line.set_categories(cats)
ws.add_chart(line, "E20")

pie = PieChart(); pie.add_data(Reference(ws, min_col=2, min_row=1, max_row=5), titles_from_data=True)
pie.set_categories(Reference(ws, min_col=1, min_row=2, max_row=5)); ws.add_chart(pie, "M2")
```

Waterfall / bridge charts: openpyxl has no native waterfall; use a stacked column chart with an
invisible base series (see `fortax-variance-analysis`).

### Sheets, rows and columns

```python
ws2 = wb.create_sheet("Data")
ws0 = wb.create_sheet("Summary", 0)      # at position 0
ws.title = "Lead Schedule"
del wb["Sheet2"]
copy = wb.copy_worksheet(wb["Template"])

ws.column_dimensions["A"].width = 32
ws.row_dimensions[1].height = 30
ws.column_dimensions["C"].hidden = True
ws.freeze_panes = "B2"                   # freeze row 1 and column A
ws.auto_filter.ref = "A1:K500"
```

## Verify before handing over

openpyxl writes formulas but not their results, so check the workbook the way the CA will see it:

1. **Recalculate** with LibreOffice if installed:
   `soffice --headless --convert-to xlsx --outdir /tmp/recalc <file>.xlsx`
   (on macOS the binary may be `/Applications/LibreOffice.app/Contents/MacOS/soffice`). If LibreOffice is
   not available, tell the CA the file must be opened once in Excel to calculate, and do the checks below
   on the formulas you wrote.
2. **Read the recalculated values:** `load_workbook(path, data_only=True)`; scan every cell for
   `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`, `#N/A`.
3. **Check cells** all 0 / TRUE.
4. **Spot-check** two or three totals against the source file with a script (not by eye).
5. Say in your reply: which checks ran, and that the values were recalculated (or not).

## Good practice

1. Start from the client's or firm's template when there is one.
2. Batch writes; avoid cell-by-cell loops over very large ranges when `append` will do.
3. Named ranges for inputs used in many formulas.
4. Data validation on columns people will type into.
5. For large files, write in stages and save.
6. Keep sheet order: Inputs, Summary, working sheets, Data, Checks.

Longer patterns (CSV import, report template, monthly tracker, dashboard) are in
[references/examples.md](references/examples.md).

## Limitations

- Cannot run VBA macros (a `.xlsm` loaded with `keep_vba=True` keeps them but does not run them).
- Pivot tables are not really supported — build a formula summary (`SUMIFS`) instead.
- Limited sparklines; no external data connections; some chart types unavailable.
- Old binary `.xls` files: convert first (LibreOffice `--convert-to xlsx`) or read with pandas + xlrd.
- `load_workbook(data_only=True)` then `save` replaces formulas with values — never save a file opened
  that way.

## Resources

- openpyxl documentation: https://openpyxl.readthedocs.io/
- Styles: https://openpyxl.readthedocs.io/en/stable/styles.html

## Credit

Techniques and examples adapted from claude-office-skills/skills (MIT; notice in
`LICENSE-THIRD-PARTY-claude-office-skills.txt`). Changed by Fortax: working-paper rules (formulas,
assumptions block, checks, sources), Indian formats, verification step, CA examples.
