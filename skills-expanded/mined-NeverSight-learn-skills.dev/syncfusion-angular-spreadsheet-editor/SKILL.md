---
name: syncfusion-angular-spreadsheet-editor
description: Use this skill for Angular apps needing Excel-like UI using the Syncfusion Spreadsheet Component. Trigger for creating, viewing, editing Excel (.xlsx, .xls, .xlsb) and CSV files; embedding spreadsheet editors; data binding from APIs/JSON; using formulas, charts, validation, filtering, or conditional formatting. Also trigger when users reference spreadsheet files ("open xlsx", "load Excel file", "add Syncfusion spreadsheet", "bind data to spreadsheet"). Do NOT trigger for standalone file processing without UI components.
compatibility: Angular supported version >= 12.x+, Node version >= 14.0.0+ (NPM Package Manager)
metadata:
  author: Syncfusion Inc
  version: "33.1.44"
---

# Syncfusion Angular Spreadsheet Editor

## Overview

This skill helps developers generate Angular code for integrating the Syncfusion Spreadsheet Editor into their applications. It provides ready-to-use code snippets, API guidance, and best practices for building Excel-like functionality in Angular projects.

## Key Capabilities

- **File Operations:** Import/export Excel files (`xlsx`, `xls`, `xlsb`), CSV files, and PDF export
- **Data Management:** Data binding, editing, sorting, filtering, and validation
- **Cell Operations:** Formatting (fonts, colors, borders, alignment), merge cells, wrap text
- **Formulas & Calculations:** Built-in Excel formulas, custom functions, named ranges
- **Collaboration:** Notes, comments, and threaded discussions
- **Advanced Features:** Charts, images, hyperlinks, conditional formatting, freeze panes, sheet protection, virtualization for large datasets

## Quick Start Examples

### Example 1: Generate Spreadsheet with Formatting
**User:** "*Create a Spreadsheet with data and apply cell styles*"

**Result:** An Angular component code snippet is generated that loads provided data into the Spreadsheet and applies basic cell formatting.

### Example 2: Generate Code for Loading a File
**User:** "*Create a Spreadsheet and load an Excel file initially*"

**Result:** An Angular component code snippet is generated that initializes the Spreadsheet and programmatically opens an Excel file on startup.

## Getting Started — Minimal Angular Code

Minimal Angular setup using **Standalone Component** (Angular 14+):

**app.ts**
```typescript
import { Component, ViewChild } from '@angular/core';
import { SpreadsheetAllModule, SpreadsheetComponent } from '@syncfusion/ej2-angular-spreadsheet';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [SpreadsheetAllModule],
  template: `
    <ejs-spreadsheet #spreadsheet (created)="created()">
      <e-sheets>
        <e-sheet>
          <e-rows>
            <e-row>
              <e-cells>
                <e-cell value="Hello, Spreadsheet!"></e-cell>
              </e-cells>
            </e-row>
          </e-rows>
        </e-sheet>
      </e-sheets>
    </ejs-spreadsheet>
  `
})
export class AppComponent {
  @ViewChild('spreadsheet') spreadsheet!: SpreadsheetComponent;

  created(): void {
    // All post-initialization code goes here
  }
}
```

Placeholders:
- `#spreadsheet` — Angular template reference variable for the component
- `<e-sheets>` — declarative sheet definitions with rows and cells
- `created()` — event handler called after the Spreadsheet is fully initialized

**Note:** Always import `SpreadsheetAllModule` in the `imports` array of the standalone component for all features to work correctly.

---

## Generate Angular Code for the User's Project

**Trigger keywords:** "angular spreadsheet", "spreadsheet editor", "syncfusion spreadsheet", "excel component", "load excel file", "open excel file", "import excel", "export excel file", "save excel", "export to pdf", "export to csv", "view excel", "configure spreadsheet", "create spreadsheet", "add spreadsheet", "spreadsheet data", "cell formatting", "apply formulas", "insert chart", "data binding", "spreadsheet validation", "freeze panes", "protect sheet"

**Workflow:**
1. Identify the requested Spreadsheet feature (data binding, formulas, charts, export, etc.).
2. Read the relevant `references/*.md` file(s) to understand the APIs and code patterns for the requested feature.
3. **STOP before generating code.** Check if the user has already chosen a delivery mode.
4. **If no delivery mode is chosen yet**, you MUST ask the user first using this concise multiple-choice question:

   **"How would you like to receive the generated Spreadsheet code?"**

   - **Option 1:** Replace the code in a specific project file (you'll need to provide the file path and confirm)
   - **Option 2:** Save the code in this skill's output folder at `{skill-root}/syncfusion-angular-spreadsheet-editor/output/app.ts` (and related files)
   - **Option 3:** Share the code directly in the chat window

5. **Only after the user selects a delivery mode**, proceed to generate Angular code using the APIs and snippets from `references/*.md`, substituting concrete placeholders from the user's project.
6. **Scope implementations within the `created` event handler** — All code implementations should be placed within the Spreadsheet's `created` event unless the user explicitly requests a different event handler (e.g., `beforeSave`, `cellSaving`, etc.).
7. **Do NOT make changes to workspace project files** unless the user explicitly chose Option 1 and provided the file path with permission.
8. Provide complete Angular snippets and concise integration steps after delivering the code.

*Refer to `## Rules` section for operational constraints (output directory, temporary files, allowed libraries, etc.)*

## Code References

All code snippets and examples are in the `references/` folder. Each file contains:
- **Minimal Angular Code** — a working, ready-to-use snippet
- **Placeholders** — values the user must customize
- **Notes** — Angular best practices and constraints

| File                          | Topic                                         |
|-------------------------------|-----------------------------------------------|
| initialization.md             | Basic Angular setup and options               |
| data-binding.md               | Local arrays, JSON, remote (DataManager)      |
| formulas.md                   | Formulas, aggregates, named ranges            |
| formatting.md                 | Cell formatting, borders, wrap text           |
| number-formatting.md          | Number formatting, decimals, currency, date   |
| conditional-formatting.md     | Rules, highlights based on conditions         |
| data-validation.md            | Validation rules, invalid highlights          |
| sorting-filtering.md          | Sorting, filtering                            |
| find-replace.md               | Find, replace                                 |
| import-export.md              | Save (XLSX/CSV/PDF), open, openFromJson       |
| charts.md                     | Insert, edit, delete charts                   |
| images.md                     | Insert, modify pictures                       |
| hyperlink.md                  | Add, remove hyperlinks                        |
| comments.md                   | Threaded comments, replies, resolve threads   |
| notes.md                      | Simple cell notes, sticky visibility, add/edit/delete |
| protection.md                 | Sheet protection, cell locking, permissions   |
| edit-cell.md                  | startEdit, endEdit, updateCell, edit modes    |
| freeze-panes.md               | Freeze rows/columns, split panes              |
| row-column.md                 | Insert, delete, resize rows/columns, hide     |
| merge-cells.md                | Merge, unmerge cells, spanning                |
| print.md                      | Page setup, headers/footers, scaling, margins |
| misc-operations.md            | Autofill, clear, sheet management, goTo       |
| clipboard.md                  | Copy, cut, paste with different paste types   |
| selection.md                  | Select cells/ranges, multi-select, getSelectedRange |
| scrolling-virtualization.md   | Virtual scrolling, large datasets, performance |
| wrap.md                       | Text wrapping, multi-line display, row height |
| defined-names.md              | Named ranges, define names, refersTo format   |
| custom-functions.md           | Custom calculation functions, addCustomFunction |
| ribbon-customization.md       | Ribbon tabs, toolbar items, file menu customization |
| context-menu.md               | Right-click context menu, contextMenuBeforeOpen |
| localization.md               | Multi-language, locale, RTL, number/date formats |
| events.md                     | Event handling, event properties, event patterns |
| autofill.md                   | Autofill patterns, fill types, series         |

## Key Rules for Code Generation (Angular-first)

1. **Angular-first snippets** — All examples and snippets must be written in Angular (TypeScript with inline template) and compile with the current `@syncfusion/ej2-angular-spreadsheet` npm package.

2. **No inline code in this manifest** — Refer to `references/*.md` for runnable snippets; keep this file as the concise policy and index.

3. **Default event scoping** — All implementations must be placed within the Spreadsheet's `created` event handler unless the user explicitly requests implementation in another event (e.g., `beforeSave`, `cellSaving`, etc.). This ensures all operations occur after the Spreadsheet component is fully initialized.

4. **Standalone component** — Always use `standalone: true` with `imports` array inside the component. Never generate `NgModule` or `app.module.ts` or `app.component.css` based code.

5. **Reference file requirements** — Each reference must include:
    - **Minimal Angular Code** (complete, runnable — standalone component with inline template)
    - **Placeholders** (clearly marked values to replace)
    - **Notes** (Angular integration steps and best practices)

6. **License handling** — Do not hardcode license keys; refer users to env variables or project config.

7. **Preserve data integrity** — Preserve existing formulas, references, and formatting when generating or editing sheets.

8. **No hallucinated APIs** — Use verified Syncfusion Spreadsheet Editor method names only.

9. **Read references first** — For any requested feature, always read the relevant `references/*.md` file(s) first before generating code.

10. **Build strictly from references** — Build Angular code strictly from the APIs, methods, properties, events, and snippets found in the reference files. Do NOT invent, guess, or suggest any API, method, property, or event not explicitly present in the reference files.

## Rules

- **Output files** must go in `{skill-root}/syncfusion-angular-spreadsheet-editor/output/` directory when user selects Option 2
- **Only use Syncfusion Spreadsheet APIs** — never recommend or use alternative spreadsheet libraries (e.g., handsontable, ag-grid, luckysheet)
- **No temporary files** — never create temporary scripts, intermediate files, or scaffolding outside the output directory
- **Angular-only code** — all generated code must be valid Angular (TypeScript + HTML template), never generate vanilla JavaScript, jQuery, or non-Angular patterns
