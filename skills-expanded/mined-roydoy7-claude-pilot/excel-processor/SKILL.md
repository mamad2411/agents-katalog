---
name: excel-processor
description: Create, edit, analyze, validate, and convert Excel workbooks for operational and presentation use. Use for XLSX/XLS/CSV data, registers and ledgers, Japanese business forms, applications, estimates and invoices, schedules, checklists, analysis, dashboards, template filling, print-ready sheets, and formatting-preserving workbook changes.
---

# Excel Processing

## Start with intent, not a fixed style

Classify the workbook before designing it:

- Decide whether it is for data exchange, repeated entry, operational tracking, calculation, analysis, management communication, or printing.
- Identify the audience, update frequency, screen/print use, collaboration needs, and template constraints.
- Preserve an existing organization-provided format unless the user requests redesign.

Read [workbook-modes.md](references/workbook-modes.md) to select the closest common mode. Combine modes when necessary.

For Japanese business use, read [japan-office-conventions.md](references/japan-office-conventions.md).

## Choose the tool path

### Inspect and read existing files

1. `mcp__xlsx__xlsx` with `inspect` — sheet mapping, usedRange vs dimensionRef, features/risks.
2. `capabilities` — confirm action is supported for the required operations.
3. `sample` — quick content overview for unknown files.
4. `read-range` — read a specific range with values, formulas, and types.
5. `read-sheet` — read a complete sheet using cursor pagination. Loop until `hasMore: false`. **Never claim a sheet is fully read after only a `sample`.**
6. `search` — locate specific values, formulas, or text across sheets.

### Modify existing files

1. `inspect` + `capabilities` — understand file structure and confirm actions are safe.
2. `read-range` on target cells — verify current values and formulas before patching.
3. `patch(dryRun: true, strict: true)` — confirm changedCells count and expectedValue matches.
4. `patch` — apply. Check `recalculationStatus` in the response.
5. `diff` — confirm only expected sheets/cells changed.
6. `validate` — verify package integrity.
7. If formulas changed and `recalculationStatus: "required"`, open in Excel/LibreOffice to recalculate.

**OOXML backend supports**: `set-cell`, `set-range`, `copy-formula-down`, `replace-values`, `clear-range`, `insert-rows`, `delete-rows`, `add/rename/delete-sheet`, `merge-cells`, `unmerge-cells`, `duplicate-sheet`, `reorder-sheet`, `set-sheet-visibility`, `set-pane`, `set-auto-filter`, `set-row-properties`, `set-column-properties`, `insert-columns`, `delete-columns`, `set-hyperlink`.

**UNSUPPORTED (requires Office COM or browser)**: `set-cell-style`, `set-data-validation`, `set-conditional-format`, `set-print-settings`, `set-comment`, `add-image`, `replace-image`, `delete-drawing`, `update-chart-data`. If Office COM is unavailable, report clearly and stop — do not attempt workarounds.

### Analyze only (no modification)

Use pandas for analysis, filtering, reshaping, joins, and large tabular data. **Do not use pandas to write back modified workbooks** — it cannot preserve macros, external links, conditional formatting, pivot tables, charts, and other non-data elements.

### Create new workbooks

Use ExcelJS for new styled `.xlsx` workbooks when TypeScript is the better fit.
Use openpyxl for new workbooks in Python contexts.
Convert legacy `.xls` to `.xlsx` with `mcp__convert__convert` before structured editing.

## Preserve workbook semantics

- Treat one record per row and one stable field per column as the default for machine-readable data.
- Preserve formulas, named ranges, tables, validations, conditional formatting, hidden sheets, print settings, and external links unless the task targets them.
- Write numbers and dates as typed values, not formatted strings. Apply display formats separately.
- Keep IDs, postal codes, account codes, and other leading-zero fields as text.
- Do not claim formula results were recalculated unless `recalculationStatus: "done"` is returned.
- Save to a new file by default.

## Apply fit-for-purpose design

Read [visual-and-print-quality.md](references/visual-and-print-quality.md) before creating or redesigning a user-facing workbook.

## Validate before delivery

Follow [validation-checklist.md](references/validation-checklist.md). At minimum:

1. Run `validate` on the output file.
2. Run `diff` to confirm only expected cell/sheet changes.
3. Check formula errors, broken links, accidental type conversion, and damaged print areas.
4. Recalculate with Excel/LibreOffice when formulas changed and `recalculationStatus: "required"`.
5. Visually inspect every user-facing sheet in its intended view, including print preview.
6. Confirm the source file remains unchanged and report any unsupported feature or fidelity risk.
