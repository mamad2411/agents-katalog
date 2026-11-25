---
name: web-tables-and-spreadsheets
description: Navigate, read, and edit grid cells, paginated tables, and spreadsheet web apps reliably.
version: 0.1.0
when:
  keywords: [spreadsheet, table, grid, cell, pagination, sort column, csv]
---
# Web tables and spreadsheets

Data grids and spreadsheet web apps often virtualize rows and turn cells into editors only after activation.

Reading tables:
1. Run `browser_snapshot` and read the column headers (`columnheader`) first so you align values with the right column.
2. Many grids render only visible rows. Use `browser_scroll` inside the grid container and re-snapshot after each scroll to collect off-screen rows.
3. For paginated tables, check the page indicator ("1-25 of 120") and click "Next" rather than assuming all rows are shown.

Editing cells:
1. Click the target cell (`browser_click`) or press `Enter` / `F2` after focusing it; some spreadsheets require a click followed by re-snapshotting to reveal the active input ref.
2. Fill the revealed editor input with `browser_fill`, then commit with `Enter` or `Tab` via `browser_press` (clicking away without committing can discard edits).
3. Run `browser_snapshot` to confirm the cell displays the updated value and no validation error banner appeared.

Safety:
- Confirm with the user before bulk-editing, overwriting formulas, or deleting rows.
