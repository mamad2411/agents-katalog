---
name: follow-lib-tanstack-table
description: Use TanStack Table end to end — columns, row models, sorting/filtering/pagination, selection, grouping, server-side, virtualization
argument-hint: "[framework] [feature]"
related:
  - follow-lib-tanstack-ecosystem
  - run-test
  - run-typecheck
  - resolve-errors
---

## Goal

Use TanStack Table (v9) fully — headless datagrid: columns, row models, sorting, filtering, pagination, row selection, grouping/expanding, column features, server-side data, virtualization

## Scope

Works with data tables of any size — headless = the library manages state/logic, **you render the UI entirely yourself**; many rows → `follow-virtual`

- part of TanStack ecosystem — selection/dispatch lives in `/follow-lib-tanstack-ecosystem`

## Execute

### 1. Install

> Goal: install the table package

```bash
bun add @tanstack/react-table   # solid/vue/svelte/angular variants available
```

### 2. Columns

> Goal: type-safe column definitions

```tsx
const columnHelper = createColumnHelper<Todo>()

const columns = [
  columnHelper.accessor('title', { header: 'Title' }),
  columnHelper.accessor('done', {
    header: 'Status',
    cell: (info) => (info.getValue() ? 'Done' : 'Pending'),
    filterFn: 'equals',
  }),
  columnHelper.display({ id: 'actions', cell: (props) => <RowActions row={props.row} /> }),
]
```

- `accessor` (data key), `display` (UI-only), `group` (column groups) — pick the right type
- Column meta: `columnDef.meta` for custom data (align, width, css class)

### 3. Row Models And State

> Goal: features enabled by row models

```tsx
const table = useReactTable({
  data, columns,
  getCoreRowModel: getCoreRowModel(),
  getSortedRowModel: getSortedRowModel(),
  getFilteredRowModel: getFilteredRowModel(),
  getPaginationRowModel: getPaginationRowModel(),
  getExpandedRowModel: getExpandedRowModel(),
  state: { sorting, columnFilters, globalFilter, rowSelection, expanded, columnVisibility },
  onSortingChange: setSorting,              // controlled state for every feature
  onRowSelectionChange: setRowSelection,
  enableRowSelection: true,
})
```

- Every feature state can be controlled or uncontrolled — controlled when it must sync with the URL/external
- `initialState` for defaults; `autoResetPageIndex` when data changes

### 4. Feature Patterns

> Goal: the features actually used

1. **Sorting**: `column.getToggleSortingHandler()` + `getIsSorted()`; multi-sort `enableMultiSort`
2. **Filtering**: global (`setGlobalFilter`) + per-column (`column.setFilterValue`) + `filterFns` custom
3. **Pagination**: `nextPage`/`previousPage`/`setPageIndex`/`setPageSize`
4. **Selection**: `row.getToggleSelectedHandler()` + `table.getSelectedRowModel()` bulk actions
5. **Grouping/expanding**: `getGroupedRowModel` + `row.getIsExpanded()`/`toggleExpanded`
6. **Column features**: `column.toggleVisibility()`, pinning `column.pin('left')`, resizing `enableColumnResizing`
7. **Server-side**: `manualPagination`/`manualSorting`/`manualFiltering` + `pageCount` — the table doesn't process, fetch via `follow-query`

### 5. Render And Verify

> Goal: render real data and prove the headless logic works before finishing

```tsx
{table.getHeaderGroups().map((hg) => hg.headers.map((h) =>
  flexRender(h.column.columnDef.header, h.getContext())))}
{table.getRowModel().rows.map((row) => row.getVisibleCells().map((cell) =>
  flexRender(cell.column.columnDef.cell, cell.getContext())))}
```

1. `/run-typecheck` + `/run-test`; actually test sort/filter/paginate/select
2. >1000 rows → `useVirtualizer` over rows (`follow-virtual`)
3. If it fails → `/resolve-errors` max 3 rounds

## Rules

- `data`/`columns` must be `useMemo`'d — a new reference = recompute every render
- Use `flexRender` only for header/cell content
- Server-side mode = `manual*` flags + fetch yourself — don't pass all the data and then enable manual
- Controlled state when syncing the URL (`follow-router` search params)
- Headless — a11y (sort buttons, aria-sort, row selection semantics) is the app's responsibility

## Expected Outcome

- Table has every feature whose row model is enabled
- Type-safe columns + correct controlled/uncontrolled state
- Server-side/virtualization wiring is correct when data is large
