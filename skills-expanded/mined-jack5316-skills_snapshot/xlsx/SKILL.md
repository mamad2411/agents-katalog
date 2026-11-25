---
name: xlsx
description: "Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path — even casually (like \"the xlsx in my downloads\") — and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved."
license: Proprietary. LICENSE.txt has complete terms
---

# XLSX Skill

Work with Excel files (.xlsx, .xlsm) and tabular data (.csv, .tsv).

## Dependencies

```bash
pip install openpyxl pandas xlsxwriter
# Also: LibreOffice (for formula recalculation)
```

## Choosing the Right Tool

| Task | Tool |
|------|------|
| Data analysis, filtering, aggregation | pandas |
| Formulas, formatting, charts | openpyxl |
| Complex chart formatting | xlsxwriter |
| Formula recalculation | scripts/recalc.py |

## Reading Data (pandas)

```python
import pandas as pd

# Read Excel
df = pd.read_excel("data.xlsx", sheet_name="Sheet1")

# Read CSV
df = pd.read_csv("data.csv")

# Read specific range
df = pd.read_excel("data.xlsx", skiprows=2, nrows=100)

print(df.head())
print(df.dtypes)
```

## Writing Data (pandas)

```python
import pandas as pd

df = pd.DataFrame({
    "Name": ["Alice", "Bob", "Charlie"],
    "Revenue": [10000, 15000, 8000],
    "Costs": [6000, 9000, 5000],
})

# Calculate profit margin (use formula, not hardcoded)
df["Profit"] = df["Revenue"] - df["Costs"]
df["Margin"] = df["Profit"] / df["Revenue"]

df.to_excel("output.xlsx", index=False)
```

## Formatting and Formulas (openpyxl)

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = Workbook()
ws = wb.active
ws.title = "Report"

# Headers
headers = ["Month", "Revenue", "Costs", "Profit", "Margin"]
for col, header in enumerate(headers, 1):
    cell = ws.cell(row=1, column=col, value=header)
    cell.font = Font(bold=True, color="FFFFFF")
    cell.fill = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")

# Data with FORMULAS (not hardcoded values!)
data = [
    ["Jan", 10000, 6000],
    ["Feb", 15000, 9000],
    ["Mar", 8000, 5000],
]

for row_idx, (month, rev, cost) in enumerate(data, 2):
    ws.cell(row=row_idx, column=1, value=month)
    ws.cell(row=row_idx, column=2, value=rev)
    ws.cell(row=row_idx, column=3, value=cost)
    # Use Excel formulas for calculated columns
    ws.cell(row=row_idx, column=4, value=f"=B{row_idx}-C{row_idx}")
    ws.cell(row=row_idx, column=5, value=f"=D{row_idx}/B{row_idx}")

# Format margin as percentage
for row in range(2, len(data) + 2):
    ws.cell(row=row, column=5).number_format = '0.0%'

wb.save("output.xlsx")
```

## Professional Standards

### Color Coding (Financial Models)
| Color | Meaning |
|-------|---------|
| **Blue text** | Hardcoded inputs / user-changeable values |
| **Black text** | Formulas and calculations |
| **Green text** | Internal worksheet links |
| **Red text** | External file links |
| **Yellow background** | Key assumptions |

### Critical Rules
1. **Always use Excel formulas** for calculated values — never hardcode results
2. **Zero formula errors** — no #REF!, #DIV/0!, #VALUE! errors allowed
3. **Consistent professional fonts** throughout (Calibri, Arial)
4. **Preserve template conventions** when editing existing files

## Formula Recalculation (MANDATORY)

After creating or editing, always run:

```bash
python scripts/recalc.py output.xlsx
```

This uses LibreOffice to recalculate all formulas and verify they evaluate correctly. Fix any errors before delivery.

## Charts (openpyxl)

```python
from openpyxl.chart import BarChart, Reference

chart = BarChart()
chart.type = "col"
chart.title = "Monthly Revenue"
chart.y_axis.title = "Amount ($)"
chart.x_axis.title = "Month"

# Data reference
data_ref = Reference(ws, min_col=2, min_row=1, max_row=4)  # Revenue column
chart.add_data(data_ref, titles_from_data=True)

# Category labels
cats = Reference(ws, min_col=1, min_row=2, max_row=4)
chart.set_categories(cats)

ws.add_chart(chart, "G2")
```

## Large Dataset Performance

```python
# Use openpyxl's optimized write mode for large datasets
from openpyxl import Workbook

wb = Workbook(write_only=True)
ws = wb.create_sheet()

for row in large_dataset:
    ws.append(row)

wb.save("large_output.xlsx")
```
