---
name: build-spreadsheet
description: Creates and edits XLSX workbooks with formulas, multi-sheet references, cell formatting, conditional formatting, pivot-style summaries, and native Excel charts.
when_to_use: When the user asks to build or modify an Excel/XLSX file — add columns with formulas (SUM/VLOOKUP), format cells, build multi-sheet workbooks with cross-sheet references, create native charts, or turn data into a structured financial-model-style workbook.
---

## When to Use

Use this skill to **produce a `.xlsx` artifact a human will open in Excel** — a financial model, budget, tracker, report, or dashboard. The deliverable is a live workbook: formulas recalculate, charts re-render, sheets cross-reference.

Reach for it when the request includes any of: "add a column that sums/looks-up", "format these cells", "highlight values over X", "build a summary sheet that pulls from the detail tabs", "make a chart", "turn this CSV into a real Excel model".

**Not this skill** — if the goal is to *analyze* data and report numbers back in chat (use pandas/data-wrangle). The line: data-wrangle answers a question, build-spreadsheet hands over a file.

Default engine: **openpyxl** (read + write + formatting + native charts in one library). Only switch to `xlsxwriter` for write-only generation of very large files (>50k rows) where speed matters — it is faster but **cannot read or edit existing files**.

## Steps

1. **Install + import.** `pip install openpyxl` if missing. Then:
   ```python
   from openpyxl import Workbook, load_workbook
   from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
   from openpyxl.formatting.rule import ColorScaleRule, CellIsRule, FormulaRule
   from openpyxl.chart import BarChart, LineChart, PieChart, ScatterChart, Reference, Series
   from openpyxl.utils import get_column_letter
   ```
   New file → `wb = Workbook()`. Editing an existing file → `wb = load_workbook("in.xlsx")` (add `data_only=False` to keep formulas as formulas, not last-cached values).

2. **Lay out sheets and headers.** `ws = wb.active; ws.title = "Detail"`; add more with `wb.create_sheet("Summary")`. Write headers, then write **typed** cell values — pass real `int`/`float`/`datetime`, not strings, or Excel treats numbers as text and SUM returns 0. Set `cell.number_format = "yyyy-mm-dd"` for dates.

3. **Write formulas as strings, never precompute.** Store the formula so Excel computes it:
   ```python
   ws["D2"] = "=B2*C2"
   ws["E2"] = "=SUM(D2:D100)"
   ws["F2"] = '=VLOOKUP(A2,Detail!$A$2:$C$100,3,FALSE)'
   ```
   A leading `=` is what makes it a formula. openpyxl does **not** evaluate it — the cell has no value until Excel/LibreOffice opens and recalcs the file.

4. **Cross-sheet refs and named ranges.** Reference another sheet with `SheetName!A1`; quote sheet names containing spaces: `'Q1 Detail'!A1`. For reusable ranges:
   ```python
   from openpyxl.workbook.defined_name import DefinedName
   wb.defined_names.add(DefinedName("tax_rate", attr_text="Assumptions!$B$1"))
   ws["C2"] = "=B2*tax_rate"
   ```

5. **Formatting.** Apply per cell (styles do **not** cascade from columns/rows):
   ```python
   ws["A1"].font = Font(bold=True, color="FFFFFF")
   ws["A1"].fill = PatternFill("solid", fgColor="305496")
   ws["B2"].number_format = '#,##0.00'          # or '$#,##0', '0.0%', '#,##0;[Red](#,##0)'
   ws.column_dimensions["A"].width = 22
   ws.freeze_panes = "A2"                        # lock header row
   ```

6. **Conditional formatting** is bound to a range and re-evaluates live in Excel:
   ```python
   ws.conditional_formatting.add("D2:D100",
       ColorScaleRule(start_type="min", start_color="F8696B",
                      end_type="max", end_color="63BE7B"))
   ws.conditional_formatting.add("E2:E100",
       CellIsRule(operator="greaterThan", formula=["1000"],
                  fill=PatternFill("solid", fgColor="FFC7CE")))
   ```

7. **Pivot-style summary** — don't try to write a real PivotTable (openpyxl support is fragile). Instead build a summary sheet of unique keys + `SUMIF`/`COUNTIF`/`AVERAGEIF` against the detail sheet, so totals stay live:
   ```python
   ws_sum["B2"] = '=SUMIF(Detail!$A:$A,A2,Detail!$D:$D)'
   ```

8. **Native charts** bound to `Reference` ranges (these recalc/redraw in Excel, unlike pasted images):
   ```python
   chart = BarChart(); chart.title = "Sales by Region"; chart.type = "col"
   data = Reference(ws, min_col=2, min_row=1, max_col=2, max_row=10)  # include header row
   cats = Reference(ws, min_col=1, min_row=2, max_row=10)
   chart.add_data(data, titles_from_data=True)
   chart.set_categories(cats)
   ws.add_chart(chart, "H2")   # anchor cell
   ```
   Swap `BarChart`→`LineChart`/`PieChart`/`ScatterChart` as needed. Scatter needs `Series(yvalues, xvalues)` explicitly.

9. **Save** with `wb.save("out.xlsx")`. Pick a clear, descriptive filename.

## Common Errors

- **Formula shows as text / SUM = 0.** Either the string lacks a leading `=`, or the summed cells hold strings not numbers. Write numeric values as real `int`/`float`. Also: a cell can hold a formula **or** a literal value, not both — openpyxl never fills in the computed result, so the file looks "empty" until opened and recalced.
- **Reading back gives `None` for formula cells.** `load_workbook(data_only=True)` returns the *last cached value Excel saved*. A file written purely by openpyxl was never opened by Excel, so there is no cache → `None`. Use `data_only=False` to read the formula string; open in Excel once and save if you need cached values.
- **Styles/charts vanish after editing an existing file.** `load_workbook` drops what it can't model — VBA macros (unless `keep_vba=True`), some chart types, and many embedded PivotTables/images are lost on re-save. Verify after round-trip; for macro files keep `.xlsm` + `keep_vba=True`.
- **Style applied to a whole column doesn't show.** openpyxl styles are per-cell; setting `column_dimensions[...].font` only affects *new* cells, not existing ones. Loop the actual cells.
- **A `Font`/`Fill`/`Border` object shared across cells** can raise `StyleProxy`/copy errors — create a fresh style object (or `copy()`) per cell instead of reusing one instance.
- **Sheet name with spaces in a formula not quoted** → `#REF!`. Wrap in single quotes: `'My Sheet'!A1`.
- **Huge files blow memory.** For tens of thousands of rows, write with `Workbook(write_only=True)` + `ws.append(row_list)` (no random cell access, no formatting mid-stream), or use `xlsxwriter`.
- **Color hex** is `RRGGBB` (or `AARRGGBB`), no `#`. `"#FF0000"` fails silently or errors.

## Verify

After saving, reopen and assert structure programmatically — never assume the write succeeded:

```python
chk = load_workbook("out.xlsx")
assert {"Detail", "Summary"} <= set(chk.sheetnames)
assert chk["Detail"]["D2"].value == "=B2*C2"          # formula stored as string
assert chk["Detail"]["D2"].data_type == "f"           # 'f' = formula
assert len(chk["Detail"]._charts) >= 1                 # chart survived save
```

Then do a real recalc check: open the file once in Excel or headless LibreOffice (`libreoffice --headless --convert-to xlsx out.xlsx`) and confirm formula cells show numbers, not `0`/`#REF!`/text. If totals are `0`, the inputs were strings — go back to step 2.
