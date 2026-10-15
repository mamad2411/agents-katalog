---
name: syncfusion-flutter-excel
description: Create and manipulate Excel workbooks using Syncfusion Flutter XlsIO library. Supports two modes — generate Dart code for the user's Flutter project or provide code snippets. Use when the user mentions Excel creation, worksheets, cells, formatting, filtering, hyperlinks, or Syncfusion Flutter XlsIO.
metadata:
  author: Syncfusion Inc
  version: "33.1.44"
---

# Excel Document Processing Using Syncfusion Flutter XlsIO Library

## Overview

Create, edit, and save Excel workbooks (.xlsx) using the Syncfusion Flutter XlsIO library.
This skill supports generating Dart code snippets for Flutter projects targeting mobile, web, and desktop platforms.

## Key Capabilities

- **Create & Edit:** Workbooks, worksheets, cells, rows, columns, cell formatting, styles, formulas, named ranges, charts, images, hyperlinks, data validation, conditional formatting
- **Data Management:** Import data (lists, typed data, hyperlinks, images), export data, advanced filtering (text, custom, date, dynamic, color filters), freeze panes, show/hide rows/columns
- **Advanced Features:** RTL layout for international support, CSV export, template-based operations, data validation rules (text, list, number, date, decimal, custom)
- **Charts & Visualization:** Create and configure all chart types (pie, bar, column, line, stacked, 3D, specialized), customize elements (title, legends, labels, positioning)
- **Security:** Password protection, worksheet/workbook encryption, cell protection with unlock options
- **Page Setup:** Margins, page breaks, print areas, page orientation, headers/footers

## Prerequisites

- **Flutter SDK** installed
- Add dependencies to `pubspec.yaml`:
  ```yaml
  dependencies:
    syncfusion_flutter_xlsio: ^xx.x.xx
    syncfusion_officechart: ^xx.x.xx
  ```
- Run: `flutter pub get`
- Import in Dart code:
  ```dart
  import 'package:syncfusion_flutter_xlsio/xlsio.dart';
  import 'package:syncfusion_officechart/officechart.dart';
  ```

## Quick Start Example

### Generate Dart Code
**User:** "Show me how to create an Excel workbook with multiple sheets"
**Result:** Dart code snippet displayed (no files created)

---

### Mode: Generate Dart Code for the User's Flutter Project

**Trigger keywords:** "show me how", "how to", "how can I", "how do I", "provide code", "provide an example", "give an example", "demonstrate", "code snippet", "sample code", "example", "sample", "give me", "show me", "main.dart", "example code", "generate code for", "codesnippet".

**Workflow:**

#### Step 1 — Detect the Platform and Suggest the Correct Package
- Inspect the workspace project files (`pubspec.yaml`, `main.dart`, etc.) to identify the Flutter platform target (mobile, web, desktop).
- Tell the user to add `syncfusion_flutter_xlsio` to their `pubspec.yaml` **before** generating any code.

#### Step 2 — Generate Code from Reference Files Only
Do NOT invent, guess, or suggest any API, class, method, or property not explicitly present in the reference files.
- Read the relevant `references/*.md` file(s) for the requested feature
- Build Dart code **strictly** from the APIs and snippets found in those files
- Use the correct save/launch pattern for the target platform:
  - **Mobile** → `getApplicationSupportDirectory()` + `OpenFile.open()`
  - **Desktop** → `getApplicationSupportDirectory()` + `OpenFile.open()`
  - **Web** → base64 + JavaScript download or `web` package approach
- Do **not** create or run any standalone Dart script

---

## Code References

All snippets are in the `references/` folder:

| File | Contents |
|---|---|
| [references/workbook.md](references/workbook.md) | Create, save/dispose, async operations, RTL layout, CSV export |
| [references/worksheet.md](references/worksheet.md) | Create, access, tab color, sizing, freeze panes, page setup |
| [references/cell-data.md](references/cell-data.md) | Add text, numbers, dates, and other data types to cells; create hyperlinks |
| [references/hyperlinks.md](references/hyperlinks.md) | Add URL and mailto hyperlinks |
| [references/named-ranges.md](references/named-ranges.md) | Create and use named ranges in formulas |
| [references/data-filtering.md](references/data-filtering.md) | Text, custom, date, dynamic, and color filters |
| [references/cell-formatting.md](references/cell-formatting.md) | Create styles, apply globally, merge/unmerge cells, built-in styles |
| [references/number-formats.md](references/number-formats.md) | Number, currency, percentage, date, time, accounting, scientific, fraction, text formats |
| [references/rows-columns-manipulation.md](references/rows-columns-manipulation.md) | Insert, delete, auto-fit, show/hide rows and columns; set width/height; number formats |
| [references/formulas.md](references/formulas.md) | Enable calculations, apply formulas, access values, nested functions, and 25+ functions (general, logical, text, time, lookup, statistical, math) |
| [references/charts-basics.md](references/charts-basics.md) | Create charts, customize elements (title, legends, labels, positioning) |
| [references/charts-types.md](references/charts-types.md) | All chart types (pie, bar, column, line, stacked, markers, 3D, specialized) |
| [references/images.md](references/images.md) | Insert, resize, flip, and rotate images (JPEG, PNG) in worksheets |
| [references/security.md](references/security.md) | Protect workbooks and worksheets with passwords, unlock cells for editing |
| [references/conditional-formatting-basics.md](references/conditional-formatting-basics.md) | Cell value, text, date, unique/duplicate, top/bottom, above/below average formatting |
| [references/conditional-formatting-advanced.md](references/conditional-formatting-advanced.md) | Color scales, icon sets, data bars, custom icons with visual analytics |
| [references/data-import.md](references/data-import.md) | Import lists, typed data, hyperlinks, and images into worksheets |
| [references/data-validation.md](references/data-validation.md) | Text, time, list, number, decimal, date, and custom formula validation rules |
| [references/tables.md](references/tables.md) | Create, style, and manage Excel tables with built-in themes |
| [references/culture.md](references/culture.md) | Culture/locale settings for dates, times, numbers, and currency formatting |
| [references/page-setup.md](references/page-setup.md) | Page setup and print settings (orientation, margins, page breaks, print area) |

---

## Rules

- Do NOT create or run temp scripts — this skill only generates code for user projects (Mode 1)
- Generate code **strictly** from reference files — never invent APIs or methods
- Always include proper imports: `import 'package:syncfusion_flutter_xlsio/xlsio.dart';` and `import 'package:syncfusion_officechart/officechart.dart';`
- For mobile/desktop apps: Use `getApplicationSupportDirectory()` + `OpenFile.open()` for file saving
- For web apps: Use base64 + JavaScript download or `web` package approach
- Always call `workbook.dispose()` after saving to release memory
- Save workbooks synchronously using `saveSync()` or asynchronously using `save()`
- Remind users to add `syncfusion_flutter_xlsio` and `syncfusion_officechart` to `pubspec.yaml` before using generated code
