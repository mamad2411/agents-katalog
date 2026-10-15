---
name: syncfusion-winforms-spreadsheet-editor
description: Use this skill for Windows Forms Application needing Excel-like UI using the Syncfusion Spreadsheet Component. Trigger for creating, viewing, editing Excel (.xlsx, .xls) files; using formulas, filtering, sorting, or cell formatting. Also trigger when users reference spreadsheet files ("open xlsx", "load Excel file", "add Syncfusion spreadsheet"). Do NOT trigger for standalone file processing without UI components.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion Windows Forms Spreadsheet Editor

## Overview
Create Excel-like viewer/editor UI in Windows Forms using Syncfusion Spreadsheet control. This skill generates C# Windows Forms code for interactive spreadsheet functionality.

## Key Capabilities
- **Create & Edit:** Workbooks (.xlsx, .xls, .xlsm), worksheets, cell editing, formatting, styles
- **Advanced Features:** 400+ formulas, named ranges, data validation, dropdown lists, cell locking, worksheet protection
- **UI Components:** SpreadsheetRibbon (File, Home, Insert, Formulas tabs), interactive editing
- **Visual Elements:** Charts (Column, Line, Pie, Bar, Area, Scatter, etc.), sparklines (Line, Column, Win/Loss)
- **Navigation:** Hyperlinks (web URLs, email, files, workbook navigation)


## Quick Start Examples

### Example 1
**User:** "Show me how to create a spreadsheet with data and formulas"

**Result:** C# code generated to create workbook, set cell values, and add formulas

### Example 2
**User:** "Add data validation and rules in the spreadsheet control"

**Result:** C# code generated for spreadsheet control validation and custom rules

---
## Generate C# Code for the User's Project *(default)*

**Trigger keywords:** "how to", "add spreadsheet", "code sample", "show me", "example", "snippet", "integrate", "component", "create sample", "code", "sample code", "generate code", "implement", "add to project", "configure spreadsheet"

### STEP 1 — Analyze User Request
  1. Read the user’s request and extract the feature keywords.
  2. If relevant reference/*.md files exist, use them as the only source of truth for generating code.
  3. If no matching reference file exists, generate code using the samples in references/getting-started.md.

### STEP 2 — Consent & Destination Gate (MUST ASK BEFORE ANY FILE ACTIONS)
  Before generating or writing anything, ask the user:

  ```
  I'm ready to generate your Syncfusion Windows Forms Spreadsheet sample.

  Where should I place it?
  1) Create a new Form file in the skill's "output" folder (recommended for quick tryout)
  2) Add or modify an existing file in your project (please provide the full file path; choose append or replace)
  3) Say "Just show me the code" to get the snippet here without modifying any files.
  ```

  ### Rules
  - Do NOT proceed until the user selects an option or says "Just show me the code."
  - If the user refuses file modifications:
    - Only show the C# code in chat
    - No file creation or changes
  - **For Option 2 only:** Before generating code, check if the project has the prerequisites from `references/getting-started.md` (Prerequisites and Setup Requirements section). If missing, ask user consent and add them.


### STEP 3 — Generate Code (Strict Reference-Only Rules)
  - ALWAYS use the sample code structure from the "Minimal code" section in getting-started.md as the base template for spreadsheet creation.
  - Use APIs exactly as shown in references/*.md (e.g., getting-started.md, formulas.md).
  - Never invent APIs or guess behavior.
  - If the feature is not documented in any reference file, inform the user that it is unavailable.

### STEP 4 — Apply Changes (Only After Consent)

  ### Option A — Create New File in Skill’s Folder
  - Create a folder named `output/` at the skill root (if it does not already exist).
  - Default filename: `SpreadsheetSample.cs`
  - If the file already exists, ask:
    "A file named 'SpreadsheetSample.cs' already exists. Overwrite, append, or use a different name?"
  - Wait for the user’s decision before writing anything.
  - Write the generated C# content.


  ### Option B — Modify a File in the User’s Project
  1. Ask:
    "Which file should I modify? Provide the COMPLETE file path (e.g., D:\Project\Form1.cs)"
  2. Wait for explicit confirmation.
  3. If the user only replies with “2” (option number) and no path → ask again.
  4. Never guess or infer file paths.
  5. Once confirmed, apply the requested change (overwrite or append).


  ### Option C — Show the Code Only
  - Display the generated C# code in chat.
  - Do NOT create or modify any files.

---

## Out-of-Scope Requests
When a user asks a question that does **NOT** match the skill domain (i.e., not related to Windows Forms Spreadsheet, Excel processing, or Syncfusion spreadsheet control), respond with:

**"Unable to process the input. Please provide the input in a different way."**

**Do NOT attempt to:**
- Generate code outside the spreadsheet/Excel domain
- Provide general Windows Forms guidance unrelated to spreadsheet functionality
- Process requests for other Syncfusion controls or unrelated frameworks
- Assist with non-spreadsheet features

**ONLY activate this skill and its workflows when the user's request matches trigger keywords:** "spreadsheet", "Excel", "form", "UI", "code", "Ribbon", "WinForms" (in context of spreadsheet/Excel).

---
## Code References (in `references/` folder)

All templates and feature snippets live in references/*.md. Each file is a focused snippet the agent combines when generating samples.

Flow: Always start with references/getting-started.md (Prerequisites and Setup Requirements section), then merge matched feature snippets. If no feature keywords match, return only the basic sample.

| File | Contents |
|---|---|
| **getting-started.md** | Setup, assemblies (required/optional), instantiate Spreadsheet/SpreadsheetRibbon, create/open/save workbooks, display charts/sparklines, register renderers |
| **formulas.md** | SetCellValue, named ranges (add/edit/delete), 409 formula functions (Database, Date/Time, Engineering, Financial, Information, Logical, Lookup, Math, Statistical, Text, Web) |
| **editing.md** | Enable/disable editing, BeginEdit/EndEdit/ValidateAndEndEdit, cell locking (Locked property), properties, methods, events (CurrentCellBeginEdit, CurrentCellValueChanged, etc.) |
| **data-management.md** | Import from DataTable/DataView/Business Objects/Arrays, export to DataTable (ImportDataTable, ExportDataTable, ExcelExportDataTableOptions), refresh display (InvalidateCells) |
| **data-validation.md** | Number/date/time/text length validation, list validation (dropdowns), custom formula validation, IDataValidation interface, comparison operators, error messages |
| **hyperlinks.md** | Create hyperlinks (URL, email, file, workbook cell references), add/edit/remove, ExcelHyperLinkType enum, IHyperLink interface properties |
| **clipboard-operations.md** | Cut/Copy/Paste, Paste Special (ExcelPasteType, ExcelPasteOptions), Fill Series (Down/Right/Up/Left) |
| **conditional-formatting.md** | Highlight cell rules (value, formula, text, time period), Data Bars, Color Scales, Icon Sets, IConditionalFormat interface |
| **conversion.md** | Convert to Image (Bitmap/Metafile), PDF (ExcelToPdfConverter, settings), HTML (SaveAsHtml), required assemblies |
| **formatting.md** | Cell background, font, borders, alignment (horizontal/vertical/orientation/indent), wrap text, number formats, built-in styles, format as table, clear formatting |
| **freeze-panes.md** | FreezeRows, FreezeColumns, FreezePanes, UnfreezePanes, XlsIO SetFreezePanes/RemoveFreezePanes |
| **localization.md** | CurrentUICulture setup, resource files (.resx), culture-specific localization, modify default strings |
| **merge-cells.md** | Merge/unmerge cells, CoveredCellInfo, IRange.Merge/UnMerge methods, InvalidateCell |
| **overview.md** | Feature overview (Ribbon, editing, formulas, data validation, conditional formatting, charts, sparklines, protection, conversion, supported file types) |
| **outline.md** | Group/ungroup rows and columns, collapse/expand groups, outline settings (summary row/column location), clear outlines, OutlineLocation enum |
| **protection.md** | Worksheet protection (Protect/Unprotect, ExcelSheetProtection options), workbook protection, lock/unlock cells, check protection status |
| **rows-columns-operations.md** | Insert/delete rows and columns, set row height/column width, hide/show rows and columns, adjust row/column dimensions |
| **worksheet.md** | Add/remove/rename worksheets, navigate between worksheets, access worksheets, move/copy worksheets, show/hide worksheets, worksheet events |
| **filtering-and-sorting.md** | AutoFilter enable/disable, filter data (number, text, date, custom), sort data (ascending/descending, custom sort), clear filters/sorting |
| **find-and-replace.md** | Find cells (FindAll, FindNext), replace functionality, find options (case-sensitive, whole word), search by criteria, navigate results |
| **selection.md** | Select ranges (single cell, multiple cells, entire row/column), get active cell, select named ranges, selection change events, clear selection |
| **shapes.md** | Import charts, sparklines, pictures, textboxes, add/resize/reposition shapes, access selected shapes, select/clear shape selection, GraphicChartCellRenderer, SparklineCellRenderer |

---

## Rules

1. **Use Only Reference Snippets**
   - Generate code **exclusively from** the Markdown files under `references/
   - **Do not invent/guess/include** any properties, events, API methods, component names, or parameters not present in `references/*.md`

2. **NO FILE MODIFICATIONS WITHOUT PERMISSION**
  - Never create or modify files/folders in user workspace without explicit user selection and confirmation.
  - Cannot create buttons, forms, dialogs, MessageBox or any UI elements beyond the Spreadsheet without user permission.

3. **Unsupported Feature Handling**
   - If the user requests a feature with no corresponding snippet in `references/*.md`, respond with:
     `That feature is not currently supported by the Syncfusion Windows Forms Spreadsheet component.`
   - Suggest the closest supported features **only if** they have snippets
   - **Explicitly list** unsupported items and **do not synthesize code** for them

4. **Validation Before Write**
   - Re-validate before writing that **all code blocks** originate from `references/*.md` files
   - If validation fails, stop and inform the user
