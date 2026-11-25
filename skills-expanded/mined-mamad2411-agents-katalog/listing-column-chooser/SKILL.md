---
name: listing-column-chooser
description: >-
  Adds a Columns show/hide dropdown to Cimmple ERPV2 listing pages, with
  locked columns, localStorage persistence, and table headers/cells driven by
  visibleColumns. Use when the user asks for a column chooser, column picker,
  show/hide columns, Columns button, or to copy the Job Template Master
  column-chooser pattern onto another master/list page.
---

# Listing Column Chooser (ERPV2)

Clone the Job Template Master **Columns** button pattern. Do not invent a new
grid library — drive `<thead>` / `<tbody>` from a `COLUMNS` definition and a
`hiddenColumns` preference.

## Before coding — gather

1. Target list page (e.g. `ProcessMaster.tsx`, `CustomerMaster.tsx`)
2. Column list: `key`, `label`, optional `sortKey`, which are `locked`
3. Default-hidden keys (secondary columns off until the user enables them)
4. `localStorage` key — unique per page, e.g. `processMaster.hiddenColumns`
5. Whether Export (if present) should honor `visibleColumns` (prefer yes)

## Checklist

```
- [ ] ColumnDefinition + COLUMNS + DEFAULT_HIDDEN_COLUMNS + COLUMN_PREFERENCE_KEY
- [ ] State: hiddenColumns (hydrate from localStorage), showColumnChooser, ref
- [ ] Outside-click useEffect closes the menu
- [ ] toggleColumn persists to localStorage
- [ ] visibleColumns = COLUMNS filtered by locked || !hidden
- [ ] page-actions: Columns dropdown (before primary Add button)
- [ ] Table thead/tbody/empty colspan use visibleColumns
- [ ] renderCell / renderCellText switch on column.key
- [ ] SCSS: shared .column-chooser* in CustomerMaster.scss (or page SCSS once)
- [ ] Export (if any) uses visibleColumns for headers/rows
```

## Reference implementation

| Piece | File |
|-------|------|
| Full pattern | `Cimmple_UI/src/Modules/Masters/JobTemplateMaster.tsx` |
| Styles | `Cimmple_UI/src/Modules/Masters/JobTemplateMaster.scss` (`.column-chooser*`) |
| Shared page chrome | `Cimmple_UI/src/Modules/Masters/CustomerMaster.scss` (`.page-actions`, `.btn-secondary`) |

Code snippets: [reference.md](reference.md).

## Rules

1. **Locked columns** — at least one identity column (`code` / `name`) stays `locked: true` so the row is never blank. Locked checkboxes are checked + disabled.
2. **Preference key** — one key per page; never reuse across masters.
3. **Persist hidden keys**, not visible keys — default list is small; new columns appear visible until the user hides them.
4. **Outside click** — close on `mousedown` outside `columnChooserRef`; do not leave the menu open across navigation.
5. **Wire the table** — hard-coded `<th>` / `<td>` lists defeat the chooser. Map `visibleColumns` for header, cells, and empty `colSpan`.
6. **Styles** — if applying to a second page, move `.column-chooser*` into `CustomerMaster.scss` (already imported by most masters) instead of duplicating. Keep Job Template’s import of that shared file.
7. **Match existing chrome** — place the control in `.page-actions` with `btn-secondary`, label **Columns**, to the left of the primary Add button (Export, if any, stays further left).
8. **No new dependencies** — no AG Grid / react-table.

## Anti-patterns

- Storing full column config objects in `localStorage` (keys only)
- Hiding every column (always keep ≥1 locked)
- Closing the menu only on button toggle (must handle outside click)
- Changing API payloads based on visible columns (filter is UI-only; export may subset columns client-side)
