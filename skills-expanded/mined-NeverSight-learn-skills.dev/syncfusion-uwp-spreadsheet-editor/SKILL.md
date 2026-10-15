---
name: syncfusion-uwp-spreadsheet-editor
description: Use this skill for UWP Application needing Excel-like UI using the Syncfusion Spreadsheet Component. Trigger for creating, viewing, editing Excel (.xlsx, .xls) files; using formulas, filtering, sorting, or cell formatting. Also trigger when users reference spreadsheet files ("open xlsx", "load Excel file", "add Syncfusion spreadsheet"). Do NOT trigger for standalone file processing without UI components.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion UWP Spreadsheet Editor

## Overview

Build Excel-like spreadsheet applications in UWP using Syncfusion SfSpreadsheet control with full support for workbook operations, formulas, charts, data validation, and ribbon customization.

## Key Capabilities

- **Workbook Operations:** Create/open/save Excel files (XLS, XLSX, XLSM, CSV), multiple worksheets, freeze panes, zoom, protection
- **Cell Operations:** Editing, formatting (fonts, colors, borders, alignment), merge cells, comments, hyperlinks, bookmarks
- **Data Features:** 400+ Excel-compatible formulas, named ranges, data validation, conditional formatting, fill series
- **Advanced Features:** Charts, sparklines, clipboard operations, undo/redo, grouping/outlines


## Quick Start Examples

### Example 1
**User:** "Show me how to create a spreadsheet with data and formulas"

**Result:** C# code generated to create workbook, set cell values, and add formulas

### Example 2
**User:** "Add data validation and rules in the spreadsheet control"

**Result:** C# code generated for spreadsheet control validation and custom rules

---

## Generate UWP Code — Workflow

**Trigger keywords:** "how to", "add spreadsheet", "code sample", "show me", "example", "snippet", "integrate", "component", "create sample", "code", "sample code", "generate code", "implement", "add to project", "configure spreadsheet"

### Step 1: Ask User for Delivery Option

Before showing code, ask:
```
"How would you like me to provide the solution?

Option 1: Create a new file in skill folder (.codestudio/skills/syncfusion-uwp-spreadsheet-editor/output/)
Option 2: Add code to an existing file in your project (you provide the file path)
Option 3: Just show the code (no files created/modified)

Please select Option 1, 2, or 3."
```

**⏸️ WAIT for explicit user selection before proceeding.**

### Step 2: Generate Code from Reference Files

- Read relevant `references/*.md` file(s) for requested feature
- Build C# and/or XAML code using ONLY snippets from reference files
- Do NOT show code yet, do NOT create files yet

### Step 3: Handle User Selection

**Option 1:** Show code → automatically save to `.codestudio/skills/syncfusion-uwp-spreadsheet-editor/output/` (skill folder only)
**Option 2:** Ask for file path → show code → wait for explicit YES confirmation → apply code → ask to build
**Option 3:** Show code with summary and required assemblies → done (no files created/modified)

  - **For Option 2 only:** Before generating code, check if the project has the prerequisites from `references/gettingstarted.md` (Prerequisites and Setup Requirements section). If missing, ask user consent and add them.

---

## Out-of-Scope Requests
When a user asks a question that does **NOT** match the skill domain (i.e., not related to UWP Spreadsheet, Excel processing, or Syncfusion spreadsheet control), respond with:

**"Unable to process the input. Please provide the input in a different way."**

**Do NOT attempt to:**
- Generate code outside the spreadsheet/Excel domain
- Provide general UWP guidance unrelated to spreadsheet functionality
- Process requests for other Syncfusion controls or unrelated frameworks
- Assist with non-spreadsheet features

**ONLY activate this skill and its workflows when the user's request matches trigger keywords:** "spreadsheet", "Excel", "UI", "code", "Ribbon", "UWP" (in context of spreadsheet/Excel).

---

## Code References

All templates and feature snippets live in `references/*.md`. Each file is a focused snippet the agent combines when generating samples.
 
Flow: Always start with `references/gettingstarted.md` (Prerequisites and Setup Requirements section), then merge matched feature snippets. If no feature keywords match, return only the basic sample.

| File | Contents |
|---|---|
| **gettingstarted.md** | NuGet packages check, XAML setup, namespaces, create/open/save workbook, basic spreadsheet code |
| **localization.md** | Supported languages, culture settings, localized UI strings, RTL support, number/date/currency formatting, dynamic language switching |
| **ribboncustomization.md** | Add custom ribbon tabs, add items to existing tabs, remove ribbon tabs and items, ribbon customization patterns |
| **worksheetmanagement.md** | Insert/delete/rename/hide/unhide sheets, protection (sheets and workbooks), gridlines, headings, zooming |
| **editing.md** | Enable/disable editing, edit cells programmatically, locking/unlocking cells, editing events, data validation (number, date, text, list, custom formula), hyperlinks |
| **selection.md** | Enable/disable selection, access current cell, get selected ranges, add/clear selections, move current cell, convert GridRangeInfo and IRange, selection events, keyboard navigation |
| **findandreplace.md** | Find All, Find Next, Find Conditional Formatting, Find Constants, Find Formulas, Find Data Validation, Replace All, Replace operations |
| **formulas.md** | Add formulas to cells, 409+ built-in functions (database, date/time, math, text, logical, lookup, statistical, financial, information), named ranges, formula calculation engine |
| **customformula.md** | Register custom formulas, add custom formulas to FormulaEngine, implement custom formula logic, use custom formulas in cells |
| **formatting.md** | Cell background color, font formatting, cell borders, cell alignment, text wrapping, merge/unmerge cells, number formatting, built-in styles, format as table, clear formatting |
| **rowsandcolumns.md** | Insert/delete rows and columns, row height and column width, hide/show rows and columns, freeze/unfreeze panes, auto-fit rows and columns |
| **conditionalformatting.md** | Highlight cell rules (values, formulas, text, time periods), data bars, color scales, icon sets, comparison operators, format types, time period types |
| **interactivefeatures.md** | Clipboard operations (cut, copy, paste, paste options in pogrammatically), undo/redo functionality, context menu customization, cell comments |
| **outline.md** | Group/ungroup rows and columns, expand/collapse groups, outline settings, clear all outlines |
| **shapes.md** | **⚠️ REQUIRED for graphic elements:** Charts (register `GraphicChartCellRenderer`), sparklines (register `SparklineCellRenderer`), pictures (add at runtime), text boxes, select shapes, clear shape selection |
| **workingwithsfspreadsheet.md** | Access workbook/worksheets, access SpreadsheetGrid, workbook load/unload events, set active sheet, access cells and ranges, set/clear cell values, refresh view, scrolling, formula bar visibility, workbook modification check, suppress alerts, suspend/resume formula calculation, popup management |

---
## Rules

1. **Use Only Reference Snippets**
   - Generate code **exclusively from** the Markdown files under `references/`
   - **Do not invent/guess/include** any properties, events, API methods, component names, or parameters not present in `references/*.md`

2. **NO FILE MODIFICATIONS WITHOUT PERMISSION**
   - Never create or modify files/folders in user workspace without explicit user selection and confirmation.
   - Cannot create StackPanel, buttons, textblocks, dialogs, MessageBox or any UI elements beyond the Spreadsheet without user permission.

3. **Unsupported Feature Handling**
   - If the user requests a feature with no corresponding snippet in `references/*.md`, respond with:
     `That feature is not currently supported by the Syncfusion UWP Spreadsheet component.`
   - Suggest the closest supported features **only if** they have snippets
   - **Explicitly list** unsupported items and **do not synthesize code** for them

4. **Validation Before Write**
   - Re-validate before writing that **all code blocks** originate from `references/*.md` files
   - If validation fails, stop and inform the user

---
