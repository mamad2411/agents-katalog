---
name: syncfusion-dotnet-excel
description: Create, edit, and convert Excel workbooks (.xlsx/.xls) using Syncfusion XlsIO. Supports two modes — generate C# code for the user's project, or execute a temporary CSX script. Use when the user mentions Excel, xlsx, workbook, template markers, Syncfusion XlsIO, or PDF conversion.
metadata:
  author: Syncfusion Inc
  version: "33.1.44"
---

# Excel (XLSX / XLS) Document Processing

## Overview

Create, edit, and convert Excel (.xlsx, .xls) files using the Syncfusion Excel Library.
This skill supports two operational modes — generating C# code for the user's project or executing tasks directly through a CSX script.

## Key Capabilities

- **Create & Edit:** Workbooks, worksheets, cells, rows, columns, cell formatting, styles, formulas, names ranges, charts, shapes, images, hyperlinks, comments, data validation, conditional formatting
- **Advanced Features:** Template markers and mail merge, data binding (DataTable, collections, objects), pivot tables, pivot charts, slicers, auto-fill, fill series, what-if analysis scenarios, custom XML, drawing objects (text boxes, checkboxes, shapes), VBA macros
- **Data Management:** Import data (CSV, DataTable, collections, nested objects, XML, HTML tables), export data (ranges, tables, named ranges), find/replace with regex, advanced filtering (top10, custom, color, icon filters), freeze panes, show/hide rows/columns/sheets
- **Conversion:** Excel to PDF, Excel to JSON, Excel to CSV (import/export)
- **Security:** Password encryption/decryption, document protection, permission settings
- **Page Setup:** Margins, headers/footers, print areas

## Prerequisites

- .NET SDK 8+ and `dotnet-script`: `dotnet tool install -g dotnet-script`
- Syncfusion License: https://www.syncfusion.com/products/communitylicense

## Quick Start Examples

### Example 1: Generate Code (Mode 1)
**User:** "Show me how to create an Excel workbook with a table"
**Result:** C# code snippet displayed (no files created)

### Example 2: Execute Task (Mode 2)
**User:** "Create an Excel spreadsheet with sales data at output/report.xlsx"
**Result:** Physical file created at specified path

## Two Modes — Choose Based on User Intent

Before choosing a mode, infer what the user wants to accomplish:

### Mode 1: Generate C# Code for the User's Project *(default)*

Use this mode when the user wants to view, write, review, refactor, or modify C# code related to Excel processing.
 
**Trigger keywords:** "code", "snippet", "how to write", "Program.cs", "show me", "sample", "example code", "generate code for", "NuGet", "add to project", "integrate", "implementation", "usage example", "API example", "learn", "teach", "how do I", "I want to", "I need to", "help me implement", "library", "package", "ASP.NET", "Blazor", "WPF", "WinForms", "MAUI", "console app", "sort", "sorting", "sorted", "chart to image", "export chart", "chart as image", "hyperlink", "link", "links", "find replace", "replace", "filter", "filtering", "pivot", "template", "marker", "formula", "function".
 
**Workflow:**
 
#### Step 1 — Detect the Application Type and Suggest the Correct NuGet Package(s)

- Inspect the workspace project files (`.csproj`, `web.config`, `App.config`, `Startup.cs`, `Program.cs`, etc.) and use the detection signals table in `references/nuget-packages.md` to identify the application type.

- Look up the correct package(s) from `references/nuget-packages.md` based on the detected app type and tell the user to install them **before** generating any code.

#### Step 2 — Generate Code from Reference Files Only

Do NOT invent, guess, or suggest any API, method, property, class, or namespace not explicitly present in the reference files.

- Read the relevant `references/*.md` file(s) for the requested feature
- Build C# code **strictly** from the APIs and snippets found in those files
- Select the correct snippet variant based on the app type detected in Step 1:
  - **Windows-specific apps** (WinForms, WPF, .NET Framework Console, ASP.NET MVC4/5, UWP) → use Windows-specific snippets
  - **Cross-platform apps** (ASP.NET Core, .NET Core/.NET 5+ Console, Blazor, MAUI, Xamarin) → use cross-platform / `.Net.Core` snippets
 - Do **not** create or run any `.csx` script
   
---

### Mode 2: Execute via CSX Script *(does not touch project files)*

Use this mode only when the user explicitly requests execution, file generation, or a fully produced output (such as a completed XLSX file).

**Trigger keywords:** "create a workbook", "create an Excel file", "generate a spreadsheet", "make a spreadsheet", "generate a file", "open", "edit", "modify", "change" an `.xlsx` file, "without modifying my project", "run a csx script", "just create it", "build me", "export to excel", "save as", "output", "result", "export", "convert", "transform", "file path", or when the user provides a file path (e.g., `output/report.xlsx`, `~/Documents/sales.xlsx`, `/tmp/data.xlsx`).

**Workflow:**

#### Step 1 — Create Temp CSX Script

- Start with `references/template.csx` as the base
- Create at: `{skill-root}/syncfusion-dotnet-excel/scripts/temp-{timestamp}.csx` (e.g., `skill-root` = `.codestudio/skills`)
- Use Unix timestamp for unique filename; never create in workspace root

#### Step 2 — Build Script from Reference Files

- Do NOT invent APIs/methods not in reference files
- Read relevant `references/*.md` file(s) and extract code snippets
- Replace all placeholders: file paths, sheet names, cell values, data, field names, etc.

#### Step 3 — Execute Script

- Run: `dotnet script {skill-root}/syncfusion-dotnet-excel/scripts/temp-{timestamp}.csx`
- Verify successful execution and capture any errors

#### Step 4 — Clean Up and Report
- Delete the temp `.csx` file after execution
- Report SUCCESS/ERROR with output file path(s) and any error messages with fixes

---

## Code References

All templates and snippets are in the `references/` folder:

| File | Contents |
|---|---|
| **nuget-packages.md** | NuGet package mappings by application type (Mode 1) |
| **template.csx** | Base CSX script structure and license registration |
| **document-structure.md** | Create/save/close workbook, add/rename/delete/move sheets |
| **template-markers.md** | Template marker binding: variables, DataTable, lists, DataSet |
| **cell-formatting.md** | Cell formatting, number formats, styles, autofit |
| **cell-values.md** | Cell values and operations: set/read text, numbers, formulas, dates, booleans, detect type |
| **cell-access-manipulation.md** | Access cells relatively, discontinuous ranges, migrant range, precedent/dependent cells, clear content |
| **formulas-advanced.md** | Cross-sheet references, array formulas, external references, named ranges, calculated columns, calculation modes, formula auditing |
| **charts.md** | Create and configure charts |
| **excel-csv.md** | Import/export CSV |
| **excel-to-json.md** | Convert worksheets or ranges to JSON |
| **excel-to-pdf.md** | Convert workbook to PDF using renderer |
| **export-data.md** | Exporting tables, ranges and named ranges |
| **import-data.md** | Import CSV, DataTable, and other data sources into sheets |
| **import-data-advanced.md** | Import HTML tables, XML, arrays, collections, nested collections, DataColumn, DataView, grid controls |
| **data-validation.md** | Add and manage data validation rules and dropdowns |
| **comments.md** | Add, edit, and remove cell comments/notes |
| **conditional-formatting.md** | Apply conditional formatting rules and color scales |
| **freeze-panes.md** | Freeze rows, columns, split panes, and unfreeze worksheet sections |
| **show-hide.md** | Show/hide rows, columns, sheets, grid lines, headers, tabs, and zoom level |
| **row-column-insert-delete.md** | Insert, delete, and move rows and columns with formatting options |
| **row-column-sizing.md** | Resize, autofit, group, and subtotal rows and columns |
| **auto-fill.md** | Auto fill series, patterns, and trends in cell ranges |
| **fill-series.md** | Fill series with linear, growth, datetime, and auto fill options |
| **find-all-replace.md** | Find all by type (text, numbers, formulas, values, comments), replace with options, entire workbook |
| **filtering-advanced.md** | Top10 filters, custom conditions, combination (text/datetime), dynamic, color, icon filters, advanced filters |
| **page-setup.md** | Page setup, margins, headers/footers, print areas |
| **pictures.md** | Insert, position, resize, align pictures and images, external links, SVG images |
| **pivot-table.md** | Create and configure pivot tables |
| **pivot-table-advanced.md** | Advanced pivot operations: cell formatting, layouts, sorting/filtering, grouping, calculated fields |
| **pivot-chart.md** | Create and configure pivot charts from pivot table data |
| **table-listobject.md** | Create and manage Excel tables (ListObjects) |
| **what-if-analysis.md** | Create and manage scenarios with what-if analysis for testing input values |
| **slicer.md** | Create and manage table slicers for UI-based filtering |
| **security.md** | Password protection, encryption, and permission settings |
| **drawing-objects.md** | Create and manage drawing objects including text boxes, checkboxes, shapes, and comments |
| **macros.md** | Create, edit, and manage VBA macros in Excel workbooks |
| **custom-xml.md** | Add and read custom XML parts to store arbitrary XML data in workbooks |
| **worksheet-move-copy.md** | Move and copy worksheets, rows, columns, and cell ranges |

---

## Rules

- Output files go in `./output/` directory
- Temp `.csx` scripts must be created inside `{skill-root}/syncfusion-dotnet-excel/scripts/` — never in the workspace root or customer `scripts/` folder
- Use license key from `SyncfusionLicense.txt` at workspace root or env var `SYNCFUSION_LICENSE_KEY`
- Never use Python libraries (e.g., openpyxl, pandas)
- Never leave temp `.csx` files after execution