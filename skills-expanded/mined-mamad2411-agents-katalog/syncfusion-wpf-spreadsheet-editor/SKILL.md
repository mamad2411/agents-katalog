---
name: syncfusion-wpf-spreadsheet-editor
description: Use this skill for WPF Application needing Excel-like UI using the Syncfusion Spreadsheet Component. Trigger for creating, viewing, editing Excel (.xlsx, .xls) files; using formulas, filtering, sorting, or cell formatting. Also trigger when users reference spreadsheet files ("open xlsx", "load Excel file", "add Syncfusion spreadsheet"). Do NOT trigger for standalone file processing without UI components.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion WPF Spreadsheet Editor

## Overview

Build Excel-like spreadsheet applications in WPF using Syncfusion SfSpreadsheet control with full support for workbook operations, formulas, charts, data validation, and ribbon customization.

## Key Capabilities

- **Workbook Operations:** Create/open/save Excel files (XLS, XLSX, XLSM, CSV), multiple worksheets, freeze panes, zoom, protection
- **Cell Operations:** Editing, formatting (fonts, colors, borders, alignment), merge cells, comments, hyperlinks, bookmarks
- **Data Features:** 400+ Excel-compatible formulas, named ranges, data validation, conditional formatting, fill series
- **Advanced Features:** Charts, sparklines, clipboard operations, undo/redo, grouping/outlines
- **Conversion:** Export to PDF, HTML, Image, CSV


## Quick Start Examples

### Example 1
**User:** "Show me how to create a spreadsheet with data and formulas"

**Result:** C# code generated to create workbook, set cell values, and add formulas

### Example 2
**User:** "Add data validation and rules in the spreadsheet control"

**Result:** C# code generated for spreadsheet control validation and custom rules

---

## Generate WPF Code — Workflow

**Trigger keywords:** "how to", "add spreadsheet", "code sample", "show me", "example", "snippet", "integrate", "component", "create sample", "code", "sample code", "generate code", "implement", "add to project", "configure spreadsheet"

### Step 1: Ask User for Delivery Option

Before showing code, ask:
```
"How would you like me to provide the solution?

Option 1: Create a new file in skill folder (.codestudio/skills/wpf-spreadsheet-editor/output/)
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

**Option 1:** Show code → automatically save to `.codestudio/skills/wpf-spreadsheet-editor/output/` (skill folder only)
**Option 2:** Ask for file path → show code → wait for explicit YES confirmation → apply code → ask to build
**Option 3:** Show code with summary and required assemblies → done (no files created/modified)

  - **For Option 2 only:** Before generating code, check if the project has the prerequisites from `references/getting-started.md` (Prerequisites and Setup Requirements section). If missing, ask user consent and add them.

---

## Out-of-Scope Requests
When a user asks a question that does **NOT** match the skill domain (i.e., not related to WPF Spreadsheet, Excel processing, or Syncfusion spreadsheet control), respond with:

**"Unable to process the input. Please provide the input in a different way."**

**Do NOT attempt to:**
- Generate code outside the spreadsheet/Excel domain
- Provide general WPF guidance unrelated to spreadsheet functionality
- Process requests for other Syncfusion controls or unrelated frameworks
- Assist with non-spreadsheet features

**ONLY activate this skill and its workflows when the user's request matches trigger keywords:** "spreadsheet", "Excel", "UI", "code", "Ribbon", "WPF" (in context of spreadsheet/Excel).

---

## Code References

All templates and feature snippets live in `references/*.md`. Each file is a focused snippet the agent combines when generating samples.
 
Flow: Always start with `references/getting-started.md` (Prerequisites and Setup Requirements section), then merge matched feature snippets. If no feature keywords match, return only the basic sample.

| File | Contents |
|---|---|
| **getting-started.md** | Assemblies, XAML setup, create/open/save workbook, import from datatable and export to datatable |
| **localization.md** | Localization and language support in spreadsheet |
| **ribbon.md** | Built-in ribbon overview and integration |
| **ribbon-customization.md** | Add/remove ribbon tabs and items, cancel ribbon commands |
| **worksheet-management.md** | Insert sheet/delete sheet/rename sheet/ hide sheets, gridlines, headings, zoom, events |
| **editing-and-selection.md** | Cell editing, cut/copy/paste, keyboard interaction |
| **selection.md** | Cell selection modes, select ranges, select rows/columns |
| **find-and-replace.md** | Find All, Find Next, Find Conditional Formatting, Find Constants, Find Formulas, Find Data Validation, Replace All, and Replace operations |
| **formulas.md** | 400+ Excel-compatible formulas, formula bar, multi-threaded calculation, name ranges | To add formulas into cell | To add or define named ranges, edit and remove named ranges | ExcelLikeComputation | Custom Formula|
| **name-manager.md** | Create, edit, and manage named ranges |
| **cell-comments.md** | Create, edit, and manage cell comments and notes | Cell Context menu | TabItem Context Menu | Customize the Cell Context Menu and TabItemContext Menu
| **cell-formatting.md** | set Text values , numbers values , dates values , borders, fonts, fill colors, alignment, font styles, wrap text, build in styles, format as table, clear formatting | sample data |
| **resizing-and-hiding.md** | Insert/Delete, Hide/unhide rows and columns, set row height and column width |
| **sorting-and-filtering.md** | Sorting and filtering data, apply filters, custom sort orders, filter by values and criteria |
| **conditional-formatting.md** | Data bars, icon sets, color scales, rule-based formatting |
| **data-validation.md** | Input restrictions, error alerts, list and cross-sheet validation |
| **freeze-panes.md** | Freeze rows and columns for easy navigation and scrolling |
| **clipboard-operations.md** | Cut, copy, paste with paste-special options |
| **charts-pictures-textboxes.md** | Import and display charts, images, and textboxes | Select Shapes | Access the Selected Shapes | Clear Selected Shapes | Import Chart Excel File |
| **outlines.md** | Group/ungroup rows and columns, expand/collapse outline levels |
| **sparklines.md** | Import line, column, and win/loss sparklines | Import Excel file with Sparklines |
| **merge-cells.md** | Merge and unmerge cells |
| **workbook-worksheet-protection.md** | Password-protect worksheets and workbook structure |
| **conversion.md** | Export to PDF, HTML, image, and CSV; printing spreadsheet |
| **fill-series.md** | Auto-fill cells with series values and patterns |
| **floating-cells.md** | Work with floating cells and textboxes |
| **hyperlinks-and-bookmarks.md** | Create and manage hyperlinks and bookmarks |
| **supported-file-types.md** | Supported file formats and import/export options |
| **undo-redo.md** | Undo and redo operations in spreadsheet |
| **zooming.md** | Zoom in/out and adjust view levels |

---
## Rules

1. **Use Only Reference Snippets**
   - Generate code **exclusively from** the Markdown files under `references/
   - **Do not invent/guess/include** any properties, events, API methods, component names, or parameters not present in `references/*.md`

2. **NO FILE MODIFICATIONS WITHOUT PERMISSION**
   - Never create or modify files/folders in user workspace without explicit user selection and confirmation.
   - Cannot create StackPanel, buttons, textblocks, dialogs, ,MessageBox or any UI elements beyond the Spreadsheet without user permission.

3. **Unsupported Feature Handling**
   - If the user requests a feature with no corresponding snippet in `references/*.md`, respond with:
     `That feature is not currently supported by the Syncfusion WPF Spreadsheet component.`
   - Suggest the closest supported features **only if** they have snippets
   - **Explicitly list** unsupported items and **do not synthesize code** for them

4. **Validation Before Write**
   - Re-validate before writing that **all code blocks** originate from `references/*.md` files
   - If validation fails, stop and inform the user
