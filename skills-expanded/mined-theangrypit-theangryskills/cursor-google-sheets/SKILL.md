---
name: cursor-google-sheets
description: Build and edit Google Sheets with the google-sheets tools - values, formatting, charts, conditional formatting, structure, validation, named and protected ranges. Use when creating a spreadsheet or dashboard, formatting cells, adding or fixing charts, or reorganizing tabs and rows.
---

## Runtime selection

Before runtime-dependent work, read [execution selection](references/runtime/selection.md). In a verified T3 host follow [the T3 contract](references/runtime/t3.md) and its method reference; the inline section below is the native Codex branch, not literal T3 dispatch. Outside T3, native Codex follows that inline branch unchanged. If the host is ambiguous or a required capability is unavailable, report the gap; a permission refusal never authorizes switching branches.

## Native Codex branch

## Codex capability boundary

This is source guidance, not an installed connector or a runtime proof. Resolve tools against the current host and read their actual schemas before using them. Preserve the named product and requested outcome. If a required operation is unavailable, report its exact name and leave that step incomplete. Do not invent tool names, connect accounts, install helpers, spend money, or broaden access from this document alone. Current operator authorization and native permissions govern every action.

Use the official Codex Google plugin and its owning skill when available. The tool names and schema details below describe the upstream connector; they are not promises about the Codex plugin. Map each operation only after inspecting the exposed schema. If the official plugin lacks the operation, name the gap; do not fall back to GOG or another credential route without explicit authorization. Never widen sharing or make a private image public to satisfy an image URL requirement. For visual work, apply available design guidance and inspect exported output.

# Google Sheets authoring

## Two coordinate systems, on purpose

- VALUE tools (`read_range`, `write_range`, `append_rows`, `clear_range`)
  address a TAB TITLE plus A1 cells: `{sheet: "Data", cells: "A1:B4"}`.
- STRUCTURE/FORMAT tools (`format_cells`, `set_borders`, `merge_cells`,
  `add_chart`, `add_conditional_formatting`, `insert_rows_or_columns`,
  `delete_rows_or_columns`, `freeze_rows_or_columns`, `sort_range`,
  `set_data_validation`, `set_basic_filter`, `add_banding`,
  `set_column_width`, `rename_sheet_tab`, `delete_sheet_tab`) address the
  numeric `sheetId`.

`get_spreadsheet` returns both (each tab's title AND sheetId) with no cell
data - call it first and keep the mapping. A new tab's sheetId is in
`add_sheet_tab`'s reply (`replies[0].addSheet.properties.sheetId`).

## Sequencing a styled sheet: values first, then format, chart last

1. `create_spreadsheet` (optionally with named tabs; it cannot target a
   folder - move it after with google-drive `google_drive_move_or_rename`).
2. `write_range` the data with `parseInput: true` when values include
   numbers, dates, or formulas (default false stores everything as literal
   text - a top source of "chart is empty" bugs).
3. Format like a real dashboard, not a bare grid:
   - `format_cells` bold header with a fill color and white text; number
     patterns on value columns (`$#,##0`, `0.0%`).
   - `freeze_rows_or_columns` the header row.
   - `set_basic_filter` over the table range - filter dropdowns are what
     make it read as a data table.
   - `set_borders` (outer heavier than inner) or `add_banding` for
     alternating row colors; `set_column_width` so nothing clips.
   - `add_conditional_formatting` for thresholds worth seeing at a glance.
4. `add_chart` LAST, after the data exists.

## Charts

- In `add_chart`, the FIRST range is the domain (x axis / pie labels) and
  later ranges are the series, one column each; anchoring a chart to the
  wrong or reversed ranges is the most common chart bug. All ranges live on
  the same tab as the chart. `headerCount: 1` uses the first cells as
  series labels - include the header row in each range when you set it.
- Place the chart over empty cells beside or below the table, not on top of
  the data it plots.
- A wrong chart is fixed in place, not worked around: `get_spreadsheet`
  lists every tab's charts (chartId, title), `update_chart` replaces a
  chart's spec keeping its position, `delete_chart` removes one. Never add
  a second chart to paper over a bad first one.

## Named and protected ranges

- `add_named_range` makes formulas self-documenting (`=SUM(Budget)` instead
  of `=SUM(B2:B13)`); write the formula with `parseInput: true`. Names
  cannot look like cell references.
- `protect_range` guards headers and formula cells (`warningOnly: true` by
  default warns editors; `false` locks them). Protect AFTER the last write
  to that range, or your own writes fight the protection.
- `get_spreadsheet` lists both, with the ids `delete_named_range` and
  `unprotect_range` need.

## Pitfalls

- No revision guard anywhere: last write wins. Read before writing when a
  collaborator may be editing.
- `merge_cells` keeps only the top-left value; write the text after merging.
- `sort_range` rewrites cell positions; sort before adding formulas that
  reference the range, and exclude the header row from the sorted range.
- `insert_rows_or_columns` / `delete_rows_or_columns` positions are 1-based
  (A=1); deletes are immediate and not undoable through the API.
- `find_replace_sheet` is literal (never regex here) and can search inside
  formulas with `searchFormulas: true`.
- Whole-tab reads can blow the byte cap; bound `cells` (e.g. "1:2000") on
  tabs you have not sized and follow `nextCells` when truncated.

## Verify your work

`read_range` for values (FORMATTED_VALUE shows what the user sees;
UNFORMATTED_VALUE the raw numbers - use it to confirm numbers are numbers,
not text). `get_spreadsheet` for structure: tabs, charts, named ranges,
protections. google-drive `google_drive_export_file` (pdf renders every tab
including charts and formatting) when the visual result matters.
