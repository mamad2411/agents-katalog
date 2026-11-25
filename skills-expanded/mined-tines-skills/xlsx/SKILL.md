---
name: xlsx
description: Create, edit, analyze, and read Excel spreadsheets (.xlsx, .xlsm, .csv) with XlsxWriter, openpyxl, and pandas. Use whenever the user wants a spreadsheet as output — a report, tracker, export, budget, or financial model — or uploads one to analyze, clean, reformat, or extend, even if they only say “sheet”, “Excel”, or “table”.
license: Apache-2.0
compatibility: Tines 3B
---

# Excel spreadsheets

Work with spreadsheets in Python through `execute`, adding packages to a `requirements.txt` in `files`: `XlsxWriter==3.2.9` to create workbooks, `openpyxl==3.1.5` to read and edit them, and `pandas` for analysis. In a workflow step, add them to the step’s `requirements.txt` instead.

User uploads arrive under `/3b/uploads/<id>/<file>`, which every execution can read. Write output to a persistent volume, such as `volumes: ["documents"]` and `/storage/documents/budget.xlsx`, then call `showStorageFile` so the user can preview it with sheet tabs and download it. Never overwrite the user’s upload: save edits as a new file, and call `showStorageFile` again after each change.

## Reading

Look before you parse. Real workbooks have title rows above the header, merged cells, hidden sheets, notes below the data, and several tables on one sheet.

```python
from openpyxl import load_workbook

wb = load_workbook("/3b/uploads/abc/vendors.xlsx", data_only=True)
for ws in wb.worksheets:
    print(f"--- {ws.title} ({ws.sheet_state}) {ws.dimensions}, merged: {list(ws.merged_cells.ranges)[:5]}")
    for row in ws.iter_rows(max_row=8, values_only=True):
        print(row)
```

`data_only=True` returns the results Excel last saved for formula cells, and `data_only=False` returns the formulas themselves. Once you know where the header row is, load the data with pandas for analysis: `pd.read_excel(path, sheet_name="Vendors", header=2)`. Dates can arrive as Excel serial numbers and IDs as floats, so check `dtypes` before computing anything.

## Formulas need saved results

An xlsx file stores each formula next to its last result. Excel, Google Sheets, and Numbers recalculate when they open a file, but the 3B preview, pandas, and `data_only=True` only read the saved result. A formula saved without one shows as blank there, and a chart over those cells draws nothing.

So write every formula with its result. Compute the value in Python from the same data, and pass it to XlsxWriter’s `write_formula` as `value=`, naming the argument because the positional slot before it is the cell format. Without it, XlsxWriter saves 0, and the preview shows zeros until someone opens the file in a spreadsheet app. Use formulas wherever a person may change inputs, such as totals, lookups, and model outputs, so the workbook stays live, and write plain values for figures nobody will edit.

## Creating

Create new workbooks with XlsxWriter:

```python
import datetime
import xlsxwriter

vendors = [
    ("Okta", "Identity", 42000, datetime.date(2026, 11, 15)),
    ("CrowdStrike", "Endpoint", 88000, datetime.date(2027, 3, 31)),
    ("1Password", "Identity", 18500, datetime.date(2026, 10, 31)),
]
last = len(vendors) + 1

wb = xlsxwriter.Workbook("/storage/documents/vendors.xlsx")
money = wb.add_format({"num_format": '"$"#,##0'})
total_money = wb.add_format({"num_format": '"$"#,##0', "bold": True})
bold = wb.add_format({"bold": True})

ws = wb.add_worksheet("Vendors")
ws.add_table(0, 0, last - 1, 3, {
    "name": "Vendors",
    "style": "Table Style Medium 2",
    "columns": [
        {"header": "Vendor"},
        {"header": "Category"},
        {"header": "Annual cost", "format": money},
        {"header": "Renewal", "format": wb.add_format({"num_format": "yyyy-mm-dd"})},
    ],
    "data": [list(vendor) for vendor in vendors],
})
ws.set_column("A:B", 18)
ws.set_column("C:D", 14)
ws.freeze_panes(1, 0)
ws.write(last, 0, "Total", bold)
ws.write_formula(last, 2, f"=SUM(C2:C{last})", total_money, value=sum(v[2] for v in vendors))

summary = wb.add_worksheet("Summary")
categories = sorted({v[1] for v in vendors})
summary.write_row(0, 0, ["Category", "Annual cost"], bold)
for row, category in enumerate(categories, start=1):
    summary.write(row, 0, category)
    summary.write_formula(
        row, 1, f"=SUMIF(Vendors!$B$2:$B${last},A{row + 1},Vendors!$C$2:$C${last})",
        money, value=sum(v[2] for v in vendors if v[1] == category),
    )
summary.set_column("A:B", 16)

chart = wb.add_chart({"type": "bar"})
chart.add_series({
    "name": "Annual cost",
    "categories": ["Summary", 1, 0, len(categories), 0],
    "values": ["Summary", 1, 1, len(categories), 1],
})
chart.set_title({"name": "Annual cost by category"})
chart.set_legend({"none": True})
summary.insert_chart("D2", chart)

wb.close()
```

- Rows and columns are zero-based in XlsxWriter calls, but formulas use Excel’s A1 references, so row index `r` is Excel row `r + 1`. Off-by-one references are the most common bug here.
- Put each table on its own sheet, starting at A1, with one header row. Downstream tools and pandas handle that shape best.
- Apply number formats instead of writing preformatted strings: `'"$"#,##0.00'` for currency, `"0.0%"` for percentages (stored as 0.125, not 12.5), and `"yyyy-mm-dd"` for dates (write `datetime` objects).
- Set column widths, freeze the header row, and add a table or `autofilter` so the sheet is usable the moment it opens.
- In a model, keep inputs on their own sheet or in a clearly marked block, give assumptions a label and unit, and reference cells rather than hard-coding numbers inside formulas.
- For newer functions such as `XLOOKUP` and `FILTER`, open the workbook with `xlsxwriter.Workbook(path, {"use_future_functions": True})`, or Excel shows `#NAME?`.
- Sheet names have at most 31 characters and can’t contain `[ ] : * ? / \`.

For large datasets, write CSV, or write the data through `with pd.ExcelWriter(path, engine="xlsxwriter") as writer:` and `df.to_excel(writer, sheet_name="Data", index=False)`, then format the sheet through `writer.sheets["Data"]`. Excel caps a sheet at 1,048,576 rows.

## Editing an existing workbook

XlsxWriter only creates files, so edit with openpyxl. Load with `load_workbook(path)`, keeping the default `data_only=False`, so formulas survive. Loading with `data_only=True` and saving replaces every formula with its last value.

openpyxl discards every saved formula result when it writes a file, so after an edit, all formula cells show blank in the 3B preview until someone opens and saves the workbook in a spreadsheet app. Tell the user about that. When the user mainly needs to view the result in 3B and the workbook is only values and formulas, read it with openpyxl and rebuild it with XlsxWriter instead. A rebuild keeps only what you copy across, so styles, conditional formatting, charts, images, and data validation are lost unless you recreate them: tell the user what it drops.

openpyxl also doesn’t round-trip everything: shapes, form controls, slicers, and some chart formatting are lost on save. Keep macros in an `.xlsm` with `load_workbook(path, keep_vba=True)` and save it under the `.xlsm` extension. Check what the workbook contains before editing, warn the user when something will be lost, and save under a new name.

openpyxl writes formulas exactly as given, so prefix newer functions yourself or Excel shows `#NAME?`. Most take `_xlfn.`, such as `=_xlfn.XLOOKUP(...)`, but worksheet-only array functions take `_xlfn._xlws.`, such as `=_xlfn._xlws.FILTER(...)` and `=_xlfn._xlws.SORT(...)`.

When inserting rows or columns, remember that openpyxl doesn’t rewrite formulas, defined names, or chart ranges that point at the shifted cells. Append below the data, or update those references yourself.

## Check the result

Reopen the saved file with `load_workbook(path, data_only=True)` and print each sheet’s dimensions, header row, and a few data rows. Any formula cell that reads as `None` or an unexpected 0 is missing its result. Then call `showStorageFile` so the user can see the sheets, and summarize what each sheet holds and which cells are formulas.
