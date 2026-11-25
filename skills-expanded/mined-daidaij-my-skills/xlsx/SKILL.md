---
name: xlsx
description: "Use this skill any time a spreadsheet file is the primary input or output. This means any task where the user wants to: open, read, edit, or fix an existing .xlsx, .xlsm, .csv, or .tsv file (e.g., adding columns, computing formulas, formatting, charting, cleaning messy data); create a new spreadsheet from scratch or from other data sources; or convert between tabular file formats. Trigger especially when the user references a spreadsheet file by name or path — even casually (like \"the xlsx in my downloads\") — and wants something done to it or produced from it. Also trigger for cleaning or restructuring messy tabular data files (malformed rows, misplaced headers, junk data) into proper spreadsheets. The deliverable must be a spreadsheet file. Do NOT trigger when the primary deliverable is a Word document, HTML report, standalone Python script, database pipeline, or Google Sheets API integration, even if tabular data is involved."
license: Proprietary. LICENSE.txt has complete terms
---

# Requirements for Outputs

## All Excel files

### Professional Font
- Use a consistent, professional font (e.g., Arial, Times New Roman) for all deliverables unless otherwise instructed by the user

### Zero Formula Errors
- Every Excel model MUST be delivered with ZERO formula errors (#REF!, #DIV/0!, #VALUE!, #N/A, #NAME?)

### Preserve Existing Templates (when updating templates)
- Study and EXACTLY match existing format, style, and conventions when modifying files
- Never impose standardized formatting on files with established patterns
- Existing template conventions ALWAYS override these guidelines

## Financial models

### Color Coding Standards
Unless otherwise stated by the user or existing template

#### Industry-Standard Color Conventions
- **Blue text (RGB: 0,0,255)**: Hardcoded inputs, and numbers users will change for scenarios
- **Black text (RGB: 0,0,0)**: ALL formulas and calculations
- **Green text (RGB: 0,128,0)**: Links pulling from other worksheets within same workbook
- **Red text (RGB: 255,0,0)**: External links to other files
- **Yellow background (RGB: 255,255,0)**: Key assumptions needing attention or cells that need to be updated

### Number Formatting Standards

#### Required Format Rules
- **Years**: Format as text strings (e.g., "2024" not "2,024")
- **Currency**: Use $#,##0 format; ALWAYS specify units in headers ("Revenue ($mm)")
- **Zeros**: Use number formatting to make all zeros "-", including percentages (e.g., "$#,##0;($#,##0);-")
- **Percentages**: Default to 0.0% format (one decimal)
- **Multiples**: Format as 0.0x for valuation multiples (EV/EBITDA, P/E)
- **Negative numbers**: Use parentheses (123) not minus -123

### Formula Construction Rules

#### Assumptions Placement
- Place ALL assumptions (growth rates, margins, multiples, etc.) in separate assumption cells
- Use cell references instead of hardcoded values in formulas
- Example: Use =B5*(1+$B$6) instead of =B5*1.05

#### Formula Error Prevention
- Verify all cell references are correct
- Check for off-by-one errors in ranges
- Ensure consistent formulas across all projection periods
- Test with edge cases (zero values, negative numbers)
- Verify no unintended circular references

#### Documentation Requirements for Hardcodes
- Comment or in cells beside (if end of table). Format: "Source: [System/Document], [Date], [Specific Reference], [URL if applicable]"
- Examples:
  - "Source: Company 10-K, FY2024, Page 45, Revenue Note, [SEC EDGAR URL]"
  - "Source: Company 10-Q, Q2 2025, Exhibit 99.1, [SEC EDGAR URL]"
  - "Source: Bloomberg Terminal, 8/15/2025, AAPL US Equity"
  - "Source: FactSet, 8/20/2025, Consensus Estimates Screen"

# XLSX creation, editing, and analysis

## Overview

A user may ask you to create, edit, or analyze the contents of an .xlsx file. You have different tools and workflows available for different tasks.

## Important Requirements

**LibreOffice Required for Formula Recalculation**: You can assume LibreOffice is installed for recalculating formula values using the `scripts/recalc.py` script. The script automatically configures LibreOffice on first run, including in sandboxed environments where Unix sockets are restricted (handled by `scripts/office/soffice.py`)

## Reading and analyzing data

### Data analysis with pandas
For data analysis, visualization, and basic operations, use **pandas** which provides powerful data manipulation capabilities:

```python
import pandas as pd

# Read Excel
df = pd.read_excel('file.xlsx')  # Default: first sheet
all_sheets = pd.read_excel('file.xlsx', sheet_name=None)  # All sheets as dict

# Analyze
df.head()      # Preview data
df.info()      # Column info
df.describe()  # Statistics

# Write Excel
df.to_excel('output.xlsx', index=False)
```

## Excel File Workflows

## CRITICAL: Use Formulas, Not Hardcoded Values

**Always use Excel formulas instead of calculating values in Python and hardcoding them.** This ensures the spreadsheet remains dynamic and updateable.

### ❌ WRONG - Hardcoding Calculated Values
```python
# Bad: Calculating in Python and hardcoding result
total = df['Sales'].sum()
sheet['B10'] = total  # Hardcodes 5000

# Bad: Computing growth rate in Python
growth = (df.iloc[-1]['Revenue'] - df.iloc[0]['Revenue']) / df.iloc[0]['Revenue']
sheet['C5'] = growth  # Hardcodes 0.15

# Bad: Python calculation for average
avg = sum(values) / len(values)
sheet['D20'] = avg  # Hardcodes 42.5
```

### ✅ CORRECT - Using Excel Formulas
```python
# Good: Let Excel calculate the sum
sheet['B10'] = '=SUM(B2:B9)'

# Good: Growth rate as Excel formula
sheet['C5'] = '=(C4-C2)/C2'

# Good: Average using Excel function
sheet['D20'] = '=AVERAGE(D2:D19)'
```

This applies to ALL calculations - totals, percentages, ratios, differences, etc. The spreadsheet should be able to recalculate when source data changes.

## Common Workflow
1. **Choose tool**: pandas for data, openpyxl for formulas/formatting
2. **Create/Load**: Create new workbook or load existing file
3. **Modify**: Add/edit data, formulas, and formatting
4. **Save**: Write to file
5. **Recalculate formulas (MANDATORY IF USING FORMULAS)**: Use the scripts/recalc.py script
   ```bash
   python scripts/recalc.py output.xlsx
   ```
6. **Verify and fix any errors**: 
   - The script returns JSON with error details
   - If `status` is `errors_found`, check `error_summary` for specific error types and locations
   - Fix the identified errors and recalculate again
   - Common errors to fix:
     - `#REF!`: Invalid cell references
     - `#DIV/0!`: Division by zero
     - `#VALUE!`: Wrong data type in formula
     - `#NAME?`: Unrecognized formula name

### Creating new Excel files

```python
# Using openpyxl for formulas and formatting
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
sheet = wb.active

# Add data
sheet['A1'] = 'Hello'
sheet['B1'] = 'World'
sheet.append(['Row', 'of', 'data'])

# Add formula
sheet['B2'] = '=SUM(A1:A10)'

# Formatting
sheet['A1'].font = Font(bold=True, color='FF0000')
sheet['A1'].fill = PatternFill('solid', start_color='FFFF00')
sheet['A1'].alignment = Alignment(horizontal='center')

# Column width
sheet.column_dimensions['A'].width = 20

wb.save('output.xlsx')
```

### Editing existing Excel files

```python
# Using openpyxl to preserve formulas and formatting
from openpyxl import load_workbook

# Load existing file
wb = load_workbook('existing.xlsx')
sheet = wb.active  # or wb['SheetName'] for specific sheet

# Working with multiple sheets
for sheet_name in wb.sheetnames:
    sheet = wb[sheet_name]
    print(f"Sheet: {sheet_name}")

# Modify cells
sheet['A1'] = 'New Value'
sheet.insert_rows(2)  # Insert row at position 2
sheet.delete_cols(3)  # Delete column 3

# Add new sheet
new_sheet = wb.create_sheet('NewSheet')
new_sheet['A1'] = 'Data'

wb.save('modified.xlsx')
```

## Recalculating formulas

Excel files created or modified by openpyxl contain formulas as strings but not calculated values. Use the provided `scripts/recalc.py` script to recalculate formulas:

```bash
python scripts/recalc.py <excel_file> [timeout_seconds]
```

Example:
```bash
python scripts/recalc.py output.xlsx 30
```

The script:
- Automatically sets up LibreOffice macro on first run
- Recalculates all formulas in all sheets
- Scans ALL cells for Excel errors (#REF!, #DIV/0!, etc.)
- Returns JSON with detailed error locations and counts
- Works on both Linux and macOS

## Formula Verification Checklist

Quick checks to ensure formulas work correctly:

### Essential Verification
- [ ] **Test 2-3 sample references**: Verify they pull correct values before building full model
- [ ] **Column mapping**: Confirm Excel columns match (e.g., column 64 = BL, not BK)
- [ ] **Row offset**: Remember Excel rows are 1-indexed (DataFrame row 5 = Excel row 6)

### Common Pitfalls
- [ ] **NaN handling**: Check for null values with `pd.notna()`
- [ ] **Far-right columns**: FY data often in columns 50+ 
- [ ] **Multiple matches**: Search all occurrences, not just first
- [ ] **Division by zero**: Check denominators before using `/` in formulas (#DIV/0!)
- [ ] **Wrong references**: Verify all cell references point to intended cells (#REF!)
- [ ] **Cross-sheet references**: Use correct format (Sheet1!A1) for linking sheets

### Formula Testing Strategy
- [ ] **Start small**: Test formulas on 2-3 cells before applying broadly
- [ ] **Verify dependencies**: Check all cells referenced in formulas exist
- [ ] **Test edge cases**: Include zero, negative, and very large values

### Interpreting scripts/recalc.py Output
The script returns JSON with error details:
```json
{
  "status": "success",           // or "errors_found"
  "total_errors": 0,              // Total error count
  "total_formulas": 42,           // Number of formulas in file
  "error_summary": {              // Only present if errors found
    "#REF!": {
      "count": 2,
      "locations": ["Sheet1!B5", "Sheet1!C10"]
    }
  }
}
```

## Filling Data Into Complex Table Templates

Real-world spreadsheets often have complex layouts that don't map to simple row/column data. **Always inspect the template structure before writing any code.**

### Step 1: Inspect the Template Structure

```python
from openpyxl import load_workbook

wb = load_workbook('template.xlsx')
ws = wb.active

# 1. Find all merged cells
print("Merged ranges:", list(ws.merged_cells.ranges))

# 2. Dump a region to see the layout (adjust range as needed)
for row in ws.iter_rows(min_row=1, max_row=20, max_col=10, values_only=False):
    for cell in row:
        if cell.value is not None:
            print(f"  {cell.coordinate}: {cell.value!r} (merged={cell.coordinate in {str(c) for mc in ws.merged_cells.ranges for c in mc.cells}})")

# 3. Check which cells have borders/fills (data entry cells often differ)
from openpyxl.styles import PatternFill
for row in ws.iter_rows(min_row=1, max_row=20, max_col=10):
    for cell in row:
        fill = cell.fill
        if fill and fill.fgColor and fill.fgColor.rgb and fill.fgColor.rgb != '00000000':
            print(f"  {cell.coordinate}: fill={fill.fgColor.rgb}")
```

### Pattern A: Alternating Header/Data Rows

```
Row 1: [Category Header]  [Q1]    [Q2]    [Q3]    [Q4]
Row 2: [Revenue]           [   ]   [   ]   [   ]   [   ]   ← data entry
Row 3: [Expenses]          [   ]   [   ]   [   ]   [   ]   ← data entry
Row 4: [Category Header]  [Q1]    [Q2]    [Q3]    [Q4]
Row 5: [Headcount]         [   ]   [   ]   [   ]   [   ]   ← data entry
Row 6: [Churn Rate]        [   ]   [   ]   [   ]   [   ]   ← data entry
```

**Strategy:** Identify the pattern programmatically, then fill only the data rows.

```python
from openpyxl import load_workbook

wb = load_workbook('template.xlsx')
ws = wb.active

# Detect header rows vs data rows by checking if column A has bold text
header_rows = set()
data_rows = []
for row_idx in range(1, ws.max_row + 1):
    cell = ws.cell(row=row_idx, column=1)
    if cell.font and cell.font.bold:
        header_rows.add(row_idx)
    elif cell.value is not None:
        data_rows.append(row_idx)

# Fill data rows only
data_to_fill = {
    'Revenue': [100, 120, 130, 150],
    'Expenses': [80, 90, 85, 95],
    'Headcount': [10, 12, 12, 14],
    'Churn Rate': [0.05, 0.04, 0.03, 0.03],
}

for row_idx in data_rows:
    label = ws.cell(row=row_idx, column=1).value
    if label in data_to_fill:
        for col_offset, val in enumerate(data_to_fill[label]):
            ws.cell(row=row_idx, column=2 + col_offset).value = val

wb.save('filled.xlsx')
```

### Pattern B: Left Column Headers + Top Row Headers (Cross-Tab)

```
         [Jan]   [Feb]   [Mar]
[Sales]  [   ]   [   ]   [   ]
[Cost]   [   ]   [   ]   [   ]
[Profit] [   ]   [   ]   [   ]
```

**Strategy:** Find the intersection of row label and column label.

```python
from openpyxl import load_workbook

wb = load_workbook('template.xlsx')
ws = wb.active

# Find header row (the row with month names)
header_row = None
row_labels = {}  # row_idx -> label
for row_idx in range(1, ws.max_row + 1):
    for col_idx in range(1, ws.max_column + 1):
        val = ws.cell(row=row_idx, column=col_idx).value
        if val and str(val).strip() in ('Jan', 'Feb', 'Mar', 'Q1', 'Q2'):
            header_row = row_idx
            break
    if header_row:
        break

# Map column headers
col_map = {}  # header_text -> col_idx
for col_idx in range(1, ws.max_column + 1):
    val = ws.cell(row=header_row, column=col_idx).value
    if val:
        col_map[str(val).strip()] = col_idx

# Map row labels
for row_idx in range(header_row + 1, ws.max_row + 1):
    val = ws.cell(row=row_idx, column=1).value
    if val:
        row_labels[str(val).strip()] = row_idx

# Fill by label intersection
values = {
    ('Sales', 'Jan'): 1000,
    ('Sales', 'Feb'): 1200,
    ('Sales', 'Mar'): 1100,
    ('Cost', 'Jan'): 600,
    ('Cost', 'Feb'): 700,
    ('Cost', 'Mar'): 650,
}
for (row_label, col_label), val in values.items():
    r = row_labels.get(row_label)
    c = col_map.get(col_label)
    if r and c:
        ws.cell(row=r, column=c).value = val

wb.save('filled.xlsx')
```

### Pattern C: Multi-Level Row Headers (Grouped Rows)

```
[Region A]                          ← group header (merged A:B)
  [Product X]  [100]  [200]        ← data row
  [Product Y]  [150]  [250]        ← data row
[Region B]                          ← group header (merged A:B)
  [Product X]  [300]  [400]        ← data row
```

**Strategy:** Detect merged cells in column A to identify group boundaries, then fill non-merged, non-empty rows.

```python
from openpyxl import load_workbook

wb = load_workbook('template.xlsx')
ws = wb.active

merged_a = {r for mc in ws.merged_cells.ranges for r in mc.rows if mc.min_col == 1}

for row_idx in range(1, ws.max_row + 1):
    cell_a = ws.cell(row=row_idx, column=1)
    # Skip merged cells (group headers) and empty rows
    if row_idx in merged_a or cell_a.value is None:
        continue
    # This is a data row — fill it
    # cell_a.value is the product name, fill columns B, C, etc.
    ws.cell(row=row_idx, column=2).value = get_sales(cell_a.value)
    ws.cell(row=row_idx, column=3).value = get_target(cell_a.value)

wb.save('filled.xlsx')
```

### Pattern D: Multi-Level Column Headers

```
Row 1: [         ]  [Revenue      ]  [Expenses     ]
Row 2: [         ]  [Actual] [Plan]  [Actual] [Plan]
Row 3: [Q1 2025  ]  [   ]    [   ]   [   ]    [   ]
Row 4: [Q2 2025  ]  [   ]    [   ]   [   ]    [   ]
```

**Strategy:** Build a column map from the leaf header row (row 2), using combined parent+child labels.

```python
from openpyxl import load_workbook

wb = load_workbook('template.xlsx')
ws = wb.active

# Find the leaf header row (the one with the most non-empty cells)
header_rows = []
for r in range(1, 4):
    non_empty = sum(1 for c in range(1, ws.max_column + 1) if ws.cell(r, c).value)
    header_rows.append((r, non_empty))

leaf_row = max(header_rows, key=lambda x: x[1])[0]
parent_row = leaf_row - 1

# Build column map: "Revenue - Actual" -> col_idx
col_map = {}
current_parent = None
for col_idx in range(1, ws.max_column + 1):
    parent_val = ws.cell(row=parent_row, column=col_idx).value
    if parent_val:
        current_parent = str(parent_val).strip()
    child_val = ws.cell(row=leaf_row, column=col_idx).value
    if child_val:
        key = f"{current_parent} - {str(child_val).strip()}"
        col_map[key] = col_idx

# Fill data
data = {
    'Q1 2025': {'Revenue - Actual': 100, 'Revenue - Plan': 110, 'Expenses - Actual': 60, 'Expenses - Plan': 65},
    'Q2 2025': {'Revenue - Actual': 120, 'Revenue - Plan': 115, 'Expenses - Actual': 70, 'Expenses - Plan': 68},
}

for row_idx in range(leaf_row + 1, ws.max_row + 1):
    label = ws.cell(row=row_idx, column=1).value
    if label and str(label).strip() in data:
        for col_key, val in data[str(label).strip()].items():
            c = col_map.get(col_key)
            if c:
                ws.cell(row=row_idx, column=c).value = val

wb.save('filled.xlsx')
```

### General Rules for Complex Templates

1. **Always inspect first** — never assume the layout; read merged cells, headers, and formatting
2. **Don't unmerge cells** — use `ws.merged_cells.ranges` to detect them and skip accordingly
3. **Fill by label matching, not by hard-coded row/column numbers** — templates may have variable row counts
4. **Preserve formatting** — only write to `.value`, don't modify `.font`, `.fill`, `.alignment` unless needed
5. **Handle `None` cells in merged ranges** — only the top-left cell of a merged range has a value; the rest return `None`
6. **Test with a small region first** — verify 2-3 cells are correct before filling the entire template

## Best Practices

### Library Selection
- **pandas**: Best for data analysis, bulk operations, and simple data export
- **openpyxl**: Best for complex formatting, formulas, and Excel-specific features

### Working with openpyxl
- Cell indices are 1-based (row=1, column=1 refers to cell A1)
- Use `data_only=True` to read calculated values: `load_workbook('file.xlsx', data_only=True)`
- **Warning**: If opened with `data_only=True` and saved, formulas are replaced with values and permanently lost
- For large files: Use `read_only=True` for reading or `write_only=True` for writing
- Formulas are preserved but not evaluated - use scripts/recalc.py to update values

### Working with pandas
- Specify data types to avoid inference issues: `pd.read_excel('file.xlsx', dtype={'id': str})`
- For large files, read specific columns: `pd.read_excel('file.xlsx', usecols=['A', 'C', 'E'])`
- Handle dates properly: `pd.read_excel('file.xlsx', parse_dates=['date_column'])`

## Code Style Guidelines
**IMPORTANT**: When generating Python code for Excel operations:
- Write minimal, concise Python code without unnecessary comments
- Avoid verbose variable names and redundant operations
- Avoid unnecessary print statements

**For Excel files themselves**:
- Add comments to cells with complex formulas or important assumptions
- Document data sources for hardcoded values
- Include notes for key calculations and model sections