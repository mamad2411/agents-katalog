---
name: xlsx-ops
description: "Use this skill any time a spreadsheet file is the primary input or output. Key triggers: 'budget', 'tracker', 'spreadsheet', 'Excel', '.xlsx', 'expense tracker', 'schedule', 'grade tracker', or requests to create any tabular financial or planning document. Target users are busy college and working women — budgets, shift trackers, grade calculators, expense logs, job application trackers. Also trigger for reading, editing, or cleaning existing .xlsx/.csv files. Do NOT trigger for Word documents, PDFs, or presentations."
---

# XLSX — Budgets, Trackers, and Spreadsheets

## Primary Use Cases (Creane Users)

| Request | Sheet Type | Notes |
|---------|------------|-------|
| "make me a budget for the month" | Monthly budget | Income vs. expenses, savings goal |
| "track my grades" | Grade calculator | Weighted average, what-if scenarios |
| "expense tracker for the week" | Expense log | Categories, running totals |
| "job application tracker" | App tracker | Company, role, status, follow-up date |
| "shift schedule tracker" | Work schedule | Hours, pay calculator |
| "savings goal tracker" | Goal planner | Target date, progress bar |

## Quality Standards

Every spreadsheet must:
- Have **zero formula errors** (#REF!, #DIV/0!, #VALUE!, #N/A, #NAME?)
- Use **formulas, not hardcoded calculated values** — the sheet must stay dynamic
- Have a **clean header row** (bold, colored background, frozen)
- Use **consistent number formatting** (currency as `$#,##0.00`, percentages as `0.0%`)
- Be **immediately usable** — user fills in their numbers, formulas do the rest

---

## CRITICAL: Formulas, Not Hardcoded Values

Always write Excel formulas into cells. Never calculate in Python and paste the result.

```python
# WRONG — hardcoded, sheet becomes static
sheet['B10'] = 1500  # user can't change assumptions

# CORRECT — formula, sheet stays dynamic
sheet['B10'] = '=SUM(B3:B9)'
sheet['C10'] = '=B10/B2'   # percentage of income
```

---

## Creating Spreadsheets — openpyxl (Primary)

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
```

### Monthly Budget Template

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = Workbook()
ws = wb.active
ws.title = "Monthly Budget"

# ---- Styles ----
HEADER_FILL   = PatternFill("solid", fgColor="1F497D")  # dark blue
SECTION_FILL  = PatternFill("solid", fgColor="D5E8F0")  # light blue
TOTAL_FILL    = PatternFill("solid", fgColor="E2EFDA")  # light green
WHITE_FONT    = Font(name="Calibri", bold=True, color="FFFFFF", size=11)
BOLD_FONT     = Font(name="Calibri", bold=True, size=11)
BODY_FONT     = Font(name="Calibri", size=11)
CURRENCY_FMT  = '$#,##0.00'
THIN_BORDER   = Border(
    bottom=Side(style="thin", color="CCCCCC"),
    left=Side(style="thin", color="CCCCCC"),
    right=Side(style="thin", color="CCCCCC"),
)

def header_row(ws, row, labels, col_widths=None):
    for col, label in enumerate(labels, 1):
        c = ws.cell(row=row, column=col, value=label)
        c.font = WHITE_FONT
        c.fill = HEADER_FILL
        c.alignment = Alignment(horizontal="center")
    if col_widths:
        for i, w in enumerate(col_widths, 1):
            ws.column_dimensions[get_column_letter(i)].width = w

def section_label(ws, row, text, cols=3):
    c = ws.cell(row=row, column=1, value=text)
    c.font = BOLD_FONT
    c.fill = SECTION_FILL
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=cols)

# ---- Title ----
ws.merge_cells("A1:C1")
title = ws["A1"]
title.value = "Monthly Budget"
title.font = Font(name="Calibri", bold=True, size=16)
title.alignment = Alignment(horizontal="center")

ws.merge_cells("A2:C2")
ws["A2"].value = "=TEXT(TODAY(),\"MMMM YYYY\")"
ws["A2"].alignment = Alignment(horizontal="center")

# ---- Header ----
header_row(ws, 4, ["Category", "Budgeted", "Actual"], col_widths=[30, 16, 16])

# ---- Income section ----
section_label(ws, 5, "INCOME", cols=3)
income_items = ["Job / Paycheck", "Financial Aid", "Side Hustle", "Other Income"]
income_start = 6
for i, item in enumerate(income_items):
    r = income_start + i
    ws.cell(r, 1, item).font = BODY_FONT
    ws.cell(r, 2).number_format = CURRENCY_FMT
    ws.cell(r, 3).number_format = CURRENCY_FMT

income_end = income_start + len(income_items) - 1
total_income_row = income_end + 1
ws.cell(total_income_row, 1, "Total Income").font = BOLD_FONT
ws.cell(total_income_row, 2, f"=SUM(B{income_start}:B{income_end})").number_format = CURRENCY_FMT
ws.cell(total_income_row, 3, f"=SUM(C{income_start}:C{income_end})").number_format = CURRENCY_FMT
ws.cell(total_income_row, 2).fill = TOTAL_FILL
ws.cell(total_income_row, 3).fill = TOTAL_FILL

# ---- Expenses section ----
exp_label_row = total_income_row + 2
section_label(ws, exp_label_row, "EXPENSES", cols=3)
expense_items = ["Rent / Housing", "Food & Groceries", "Transportation", "Phone Bill",
                 "Subscriptions", "School Supplies", "Personal Care", "Entertainment", "Savings Goal"]
exp_start = exp_label_row + 1
for i, item in enumerate(expense_items):
    r = exp_start + i
    ws.cell(r, 1, item).font = BODY_FONT
    ws.cell(r, 2).number_format = CURRENCY_FMT
    ws.cell(r, 3).number_format = CURRENCY_FMT

exp_end = exp_start + len(expense_items) - 1
total_exp_row = exp_end + 1
ws.cell(total_exp_row, 1, "Total Expenses").font = BOLD_FONT
ws.cell(total_exp_row, 2, f"=SUM(B{exp_start}:B{exp_end})").number_format = CURRENCY_FMT
ws.cell(total_exp_row, 3, f"=SUM(C{exp_start}:C{exp_end})").number_format = CURRENCY_FMT
ws.cell(total_exp_row, 2).fill = TOTAL_FILL
ws.cell(total_exp_row, 3).fill = TOTAL_FILL

# ---- Summary ----
summary_row = total_exp_row + 2
ws.cell(summary_row, 1, "Left Over / Deficit").font = BOLD_FONT
ws.cell(summary_row, 2, f"=B{total_income_row}-B{total_exp_row}").number_format = CURRENCY_FMT
ws.cell(summary_row, 3, f"=C{total_income_row}-C{total_exp_row}").number_format = CURRENCY_FMT

# Freeze header
ws.freeze_panes = "A5"

wb.save("monthly_budget.xlsx")
```

### Job Application Tracker

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
from datetime import date

wb = Workbook()
ws = wb.active
ws.title = "Job Applications"

headers = ["Company", "Role", "Date Applied", "Status", "Follow-Up Date", "Notes", "Link"]
col_widths = [25, 30, 14, 18, 16, 35, 40]
STATUS_COLORS = {
    "Applied":    "FFF3CD",  # yellow
    "Interview":  "D1ECF1",  # teal
    "Offer":      "D4EDDA",  # green
    "Rejected":   "F8D7DA",  # red
    "Withdrawn":  "E2E3E5",  # grey
}

HEADER_FILL = PatternFill("solid", fgColor="1F497D")
for col, (hdr, width) in enumerate(zip(headers, col_widths), 1):
    c = ws.cell(1, col, hdr)
    c.font = Font(bold=True, color="FFFFFF", name="Calibri")
    c.fill = HEADER_FILL
    c.alignment = Alignment(horizontal="center")
    ws.column_dimensions[get_column_letter(col)].width = width

# Sample row
ws.cell(2, 1, "Cleveland Clinic")
ws.cell(2, 2, "Nursing Assistant")
ws.cell(2, 3, date.today()).number_format = "MMM DD, YYYY"
ws.cell(2, 4, "Applied")
ws.cell(2, 5, "").number_format = "MMM DD, YYYY"
ws.cell(2, 6, "Applied via LinkedIn")

ws.freeze_panes = "A2"
wb.save("job_tracker.xlsx")
```

### Grade Calculator

```python
wb = Workbook()
ws = wb.active
ws.title = "Grade Calculator"

headers = ["Assignment", "Category", "Weight (%)", "Your Score", "Max Score", "Weighted Grade"]
for col, hdr in enumerate(headers, 1):
    c = ws.cell(1, col, hdr)
    c.font = Font(bold=True, color="FFFFFF", name="Calibri")
    c.fill = PatternFill("solid", fgColor="1F497D")

ws.column_dimensions['A'].width = 30
ws.column_dimensions['B'].width = 20

# Assignments (rows 2-11 for 10 assignments)
for row in range(2, 12):
    ws.cell(row, 3).number_format = "0.0%"  # weight
    ws.cell(row, 4).number_format = "0.00"  # your score
    ws.cell(row, 5).number_format = "0.00"  # max score
    # Weighted grade formula: (score/max) * weight
    ws.cell(row, 6, f"=(D{row}/E{row})*C{row}").number_format = "0.0%"

# Final grade
ws.cell(13, 1, "FINAL GRADE").font = Font(bold=True, name="Calibri")
ws.cell(13, 6, "=SUM(F2:F12)").number_format = "0.0%"
ws.cell(13, 6).font = Font(bold=True, size=14, name="Calibri")

ws.freeze_panes = "A2"
wb.save("grade_calculator.xlsx")
```

## Reading and Analyzing Existing Files

```python
import pandas as pd
from openpyxl import load_workbook

# Quick data read
df = pd.read_excel('file.xlsx')
all_sheets = pd.read_excel('file.xlsx', sheet_name=None)  # dict of DataFrames

# Editing without losing formulas
wb = load_workbook('existing.xlsx')  # don't use data_only=True if you need to save formulas
ws = wb.active
ws['A2'] = "New Value"
wb.save('updated.xlsx')

# Reading calculated values (WARNING: saving after this replaces formulas)
wb = load_workbook('existing.xlsx', data_only=True)
```

## openpyxl Formula Verification Checklist

- Verify cell references are correct (Excel is 1-indexed; DataFrame row 5 = Excel row 6)
- Check that SUM ranges are right — off-by-one errors are common
- Test with edge cases (empty cells, zeros, negatives)
- Check cross-sheet references use `SheetName!A1` format
- Column 64 = BL, not BK — double-check when using column numbers directly

## Number Formatting Reference

| Data Type | Format String |
|-----------|--------------|
| Currency | `$#,##0.00` |
| Currency (no cents) | `$#,##0` |
| Percentage | `0.0%` |
| Date | `MMM DD, YYYY` |
| Negative as parens | `$#,##0.00;($#,##0.00)` |
| Zero as dash | `$#,##0.00;($#,##0.00);-` |

## QA Checklist

- [ ] Zero formula errors in all cells
- [ ] All totals use SUM formulas, not hardcoded values
- [ ] Header row is bold, colored, and frozen
- [ ] Number formats match data type (currency, %, dates)
- [ ] File opens correctly in Excel and Google Sheets
- [ ] User only needs to fill in their numbers — no formula knowledge required

## Dependencies

```bash
pip install openpyxl pandas
```
