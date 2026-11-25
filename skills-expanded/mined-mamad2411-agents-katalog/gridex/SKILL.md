---
name: gridex
description: "Guide for using Gridex — a comprehensive React data grid library built on TanStack Table v8. Use when the user asks about data grids, tables, spreadsheets in React, or needs help with Gridex columns, sorting, filtering, editing, server-side data, exporting, theming, or any Gridex API."
progressive_disclosure:
  entry_point:
    summary: "React data grid with all enterprise features — sorting, filtering, editing, virtualization, export, themes, i18n — built on TanStack Table v8"
    when_to_use: "When working with Gridex, React data grids, table components, column definitions, cell editing, server-side data, or data export."
    quick_start: "1. Review core concepts below. 2. Use createColumns for type-safe column definitions. 3. Consult references for advanced features."
  references:
    - column-system.md
    - editing-validation.md
    - server-side.md
    - export-import.md
    - theming-i18n.md
    - advanced-features.md
    - mantine-integration.md
---

# Gridex — React Data Grid

Gridex is a comprehensive React data grid library built on TanStack Table v8. It provides all enterprise-level features (sorting, filtering, editing, virtualization, export, themes, i18n) — fully customizable, zero paywalls.

## Installation

```bash
npm install gridex
# or
pnpm add gridex
```

**Peer dependencies:** `react >= 18.0.0`, `react-dom >= 18.0.0`

## Quick Start

```tsx
import { Gridex, createColumns } from "gridex";
import "gridex/dist/index.css";

type Person = { name: string; age: number; email: string };

const columns = createColumns<Person>((col) => [
  col.accessor("name", { header: "Name" }),
  col.accessor("age", { header: "Age", type: "number" }),
  col.accessor("email", { header: "Email" }),
]);

export default function App() {
  const [data] = useState<Person[]>([
    { name: "Alice", age: 30, email: "alice@example.com" },
    { name: "Bob", age: 25, email: "bob@example.com" },
  ]);
  return <Gridex data={data} columns={columns} />;
}
```

## Core Concepts

| Concept | Description |
|---------|-------------|
| **`<Gridex>`** | Main component — accepts `data`, `columns`, and feature config props |
| **`createColumns()`** | Type-safe column builder with `col.accessor()`, `col.display()`, `col.group()` |
| **Value Pipeline** | `valueGetter` → `valueFormatter` → `cell` (display); inverse for editing |
| **Controlled/Uncontrolled** | All state (sorting, filtering, pagination) supports both modes |
| **Slots** | 50+ replaceable UI components via `slots` prop |
| **`useGridex()`** | Context hook — access table, exportAPI, filterAPI, scrollAPI, gridAPI, eventEmitter |
| **CSS Variables** | 60+ custom properties for theming, dark mode via `[data-gridex-theme="dark"]` |

## Component API Overview

```tsx
<Gridex
  // Data
  data={data}                              // Client-side data array
  columns={columns}                        // Column definitions from createColumns()
  dataSource={{ fetchData, pageSize: 25 }} // OR server-side (replaces data)
  getRowId={(row) => row.id}               // Custom row identity

  // Sorting
  sorting={{
    defaultSort: [{ id: "name", desc: false }],
    multiSort: true,                       // Allow multi-column sort
    maxMultiSortColumns: 3,
  }}

  // Filtering
  filtering={{
    showFilterRow: true,                   // Column filter inputs
    globalFilter: true,                    // Global search bar
    filterDebounceMs: 300,
    advancedFilter: true,                  // Advanced filter dialog
    filterBuilder: true,                   // Filter builder UI
  }}

  // Pagination
  pagination={{
    pageSize: 10,
    pageSizeOptions: [10, 25, 50, 100],
    showPageSizeSelector: true,
  }}

  // Selection
  selection={{
    mode: "multiple",                      // "single" | "multiple" | false
    selectAllMode: "page",                 // "page" | "all"
    enableRangeSelection: true,            // Shift+click range
    enableCellRangeSelection: true,        // Multi-cell selection
    onSelectionChange: (rows) => {},
  }}

  // Columns
  columnConfig={{
    enableResizing: true,
    enableReordering: true,
    enablePinning: true,
    enableVisibility: true,
    enableStretching: true,                // Stretch columns to fill width
    stretchMode: "all",                    // "all" | "last" | "fit"
  }}

  // Virtualization
  virtualization={{
    height: 600,                           // Container height (required)
    rowHeight: 40,                         // Fixed row height (optional)
    overscan: 5,                           // Extra rows to render
  }}

  // Editing (see editing-validation.md reference)
  editing={{
    enabled: true,
    trigger: "doubleClick",                // "click" | "doubleClick" | "keypress"
    mode: "cell",                          // "cell" | "row" | "batch" | "form" | "popup"
    onAfterEdit: (params) => {},
  }}

  // Expansion / Master-Detail
  expansion={{
    enabled: true,
    renderDetail: (row) => <DetailPanel row={row} />,
    singleExpand: false,                   // Only one expanded at a time
  }}

  // Grouping
  grouping={{
    enabled: true,
    defaultGrouping: ["department"],
    aggregations: { salary: "sum", age: "avg" },
  }}

  // Tree Data
  treeData={{
    enabled: true,
    getSubRows: (row) => row.children,
    defaultExpanded: true,
  }}

  // Summary Row
  summary={{
    enabled: true,
    position: "bottom",                    // "top" | "bottom" | "both"
    aggregations: { amount: "sum", price: "avg" },
  }}

  // Appearance
  theme="dark"                             // "light" | "dark" | ThemePreset | CSSVariableMap
  themePreset="alpine"                     // "material" | "alpine" | "quartz" | "minimal" | "corporate" | "highContrast"
  density="comfortable"                    // "compact" | "comfortable" | "spacious"
  striped                                  // Alternating row colors
  rtl                                      // Right-to-left layout

  // i18n
  locale={ptBR}                            // Import from "gridex" (35 locales available)

  // Toolbar
  toolbar={{
    showAddRow: true,
    showDeleteSelected: true,
    createNewRow: () => ({ name: "", age: 0 }),
    onAddRow: (row) => {},
    onDelete: (rows) => {},
  }}

  // Sidebar
  sidebar={{
    panels: ["columns", "filters"],
    defaultPanel: "columns",
  }}

  // Status Bar
  statusBar={{
    panels: ["rowCount", "selectedCount", "aggregation"],
  }}

  // Context Menu
  enableContextMenu
  contextMenuItems={(row, column) => [
    { label: "Copy", action: () => {} },
    { label: "Delete", action: () => {}, variant: "danger" },
  ]}

  // Find & Replace
  enableFind                               // Ctrl+F find bar

  // Tooltips
  enableCellTooltips                       // Overflow tooltips
  tooltipConfig={{ delay: 500, position: "top" }}

  // Responsive
  responsive={{
    breakpoint: 768,
    mobileView: "card",                    // "card" | "list"
    renderCard: (row) => <Card row={row} />,
  }}

  // Conditional Formatting
  conditionalFormatting={[
    { column: "status", condition: (v) => v === "error", style: { color: "red" } },
  ]}

  // Overlay
  overlay={{ loading: isLoading, text: "Loading..." }}

  // Events
  onGridReady={(api) => {}}
  onCellClick={(data) => {}}
  onRowClick={(data) => {}}
  onSortChanged={(sorting) => {}}
  onFilterChanged={(filters) => {}}
  onSelectionChanged={(selection) => {}}

  // Slots (override any UI component)
  slots={{
    cell: CustomCell,
    headerCell: CustomHeader,
    row: CustomRow,
    pagination: CustomPagination,
    emptyState: CustomEmpty,
    loadingState: CustomLoading,
  }}
/>
```

## Column Types

Built-in column types that automatically configure formatting, filtering, sorting, and editing:

| Type | Description |
|------|-------------|
| `text` | Plain text (default) |
| `number` | Numeric with locale formatting |
| `date` | Date with configurable format |
| `dateTime` | Date + time |
| `time` | Time only |
| `boolean` | Checkbox display + toggle |
| `select` | Dropdown from options |
| `richSelect` | Searchable dropdown with custom rendering |
| `autocomplete` | Text input with suggestions |
| `password` | Masked input |
| `phone` | Phone number with mask |
| `duration` | Time duration (hm/colon/minutes) |
| `percentage` | Percentage with format options |
| `currency` | Currency formatting |
| `bigint` | Large integer formatting |
| `masked` | Custom input mask |

## Context API

Access grid internals from any child component:

```tsx
import { useGridex } from "gridex";

function MyToolbar() {
  const { table, exportAPI, filterAPI, scrollAPI, gridAPI, eventEmitter } = useGridex();

  return (
    <div>
      <button onClick={() => exportAPI?.downloadCSV()}>Export CSV</button>
      <button onClick={() => exportAPI?.downloadExcel()}>Export Excel</button>
      <button onClick={() => filterAPI?.clearFilters()}>Clear Filters</button>
      <button onClick={() => gridAPI?.scrollToRow(0, "start")}>Scroll to Top</button>
    </div>
  );
}
```

## Imperative Grid API

```tsx
const gridRef = useRef<GridexAPI>(null);

// Navigation
gridAPI.scrollToRow(rowIndex, "start" | "center" | "end");
gridAPI.scrollToColumn(columnId);

// Editing
gridAPI.startEdit(rowIndex, columnId);
gridAPI.stopEdit();

// Selection
gridAPI.selectRows([0, 1, 2]);
gridAPI.deselectAll();

// State
gridAPI.refresh();
gridAPI.resetState("all" | "sorting" | "filtering" | "pagination" | "selection");
gridAPI.autoSizeColumn(columnId);
gridAPI.autoSizeAllColumns();
```

## Event Emitter

```tsx
const { eventEmitter } = useGridex();

useEffect(() => {
  const unsub = eventEmitter?.on("cellClicked", (data) => {
    console.log("Cell clicked:", data.rowIndex, data.columnId);
  });
  return () => unsub?.();
}, [eventEmitter]);
```

**Available events:** `gridReady`, `dataLoaded`, `firstDataRendered`, `cellClicked`, `cellDoubleClicked`, `rowClicked`, `sortChanged`, `filterChanged`, `selectionChanged`, `stateChanged`, `scrollEnd`

## Mantine Integration

```bash
npm install gridex-mantine @mantine/core @mantine/dates
```

```tsx
import { MantineProvider } from "@mantine/core";
import { MantineGridex } from "gridex-mantine";

<MantineProvider>
  <MantineGridex data={data} columns={columns} />
</MantineProvider>
```

`MantineGridex` automatically replaces all 15 editors and 21 UI slot components with Mantine equivalents, maps 53 CSS variables to Mantine design tokens, provides a Tabler icon pack (22 icons), and detects dark mode from `MantineProvider`. See `mantine-integration.md` reference for full API, all slot components, editor mappings, theme utilities, convenience objects, and utility functions.

### Selective Mantine Integration

Use individual slot collections or editors without the full wrapper:

```tsx
import { Gridex } from "gridex";
import {
  mantineSlots,           // All 21 slot overrides
  mantineStructuralSlots, // Pagination, empty, loading, toolbar
  mantineInteractiveSlots,// Column filter, visibility, advanced filter
  mantineOverlaySlots,    // Popup edit, form panel, sidebar, detail, find, tooltip, comment
  mantineMenuSlots,       // Context menu, column menu, status bar, batch toolbar, filter builder
  mantineViewSlots,       // Card view, list view
  mantineIconPack,        // 22 Tabler icons
  mantineEditorMap,       // All 15 editor mappings
  useMantineGridexTheme,  // Theme hook
} from "gridex-mantine";

// Use only structural slots
<Gridex slots={mantineStructuralSlots} />

// Or mix and match
<Gridex slots={{ ...mantineStructuralSlots, ...mantineMenuSlots }} />
```

## Additional Exported Utilities

### Type Helpers

```tsx
import type { GridexColumnDef, GridexRowData, GridexCellValue } from "gridex";

// GridexColumnDef<TData> — Convenience alias for ColumnDef<TData, any>
// GridexRowData<TColumns> — Extracts row data type from column definitions
// GridexCellValue<TData, TKey> — Extracts cell value type from data + key
```

### Filter Builder

```tsx
import { FilterBuilder, createEmptyFilterBuilderModel, isFilterBuilderGroup } from "gridex";

// Create an empty filter builder model
const model = createEmptyFilterBuilderModel("columnId");

// Check if an item is a group (vs. condition)
if (isFilterBuilderGroup(item)) { /* nested group */ }

// Standalone filter builder component
<FilterBuilder
  columns={columns}
  model={model}
  onChange={(model) => setModel(model)}
  onApply={(model) => applyFilters(model)}
  showApplyButton
/>
```

### Config Provider (Shared Defaults)

```tsx
import { GridexConfigProvider, ptBR } from "gridex";
import type { GridexConfig } from "gridex";

// Define shared config once — all nested <Gridex> instances inherit it
<GridexConfigProvider
  config={{
    theme: "dark",
    density: "compact",
    locale: ptBR,
    striped: true,
    enableFind: true,
    showRowNumbers: true,
  }}
>
  <Gridex data={data1} columns={cols1} />
  <Gridex data={data2} columns={cols2} />
  {/* Per-instance override still works */}
  <Gridex data={data3} columns={cols3} theme="light" />
</GridexConfigProvider>
```

**Shareable `GridexConfig` props:** `theme`, `themePreset`, `density`, `striped`, `rtl`, `locale`, `iconPack`, `tooltipConfig`, `dragConfig`, `enableContextMenu`, `enableTouchOptimization`, `enableRowAnimation`, `enableFind`, `enableColumnHoverHighlight`, `showRowNumbers`, `layout`, `responsiveView`, `responsiveBreakpoint`, `loadingRowCount`

**Nesting:** Inner `GridexConfigProvider` merges with outer — inherits unset props, overrides set ones.

**Dynamic switching:** Pass a stateful config object; all grids update when state changes.

**SSR safe:** Uses only `useMemo` + `useContext` — no browser APIs.

### i18n Provider & Hook

```tsx
import { GridexI18nProvider, useTranslations, t } from "gridex";

// Set locale once for all nested grids (also works via GridexConfigProvider)
<GridexI18nProvider translations={ptBR}>
  <Gridex data={data1} columns={cols1} />
  <Gridex data={data2} columns={cols2} />
</GridexI18nProvider>

// Access translations in custom components
function MyCustomComponent() {
  const translations = useTranslations();
  return <span>{t(translations.pagination.showing, { from: 1, to: 10, total: 100 })}</span>;
}
```

### Long Press Hook (Mobile)

```tsx
import { useLongPress } from "gridex";

const handlers = useLongPress({
  onLongPress: (event) => showContextMenu(event),
  threshold: 500,  // ms (default: 500)
  enabled: true,
});

<div {...handlers}>Long press me</div>
```

### Formula Utilities

```tsx
import { evaluateFormula, isFormula, colLetterToIndex, indexToColLetter, parseCellRef } from "gridex";

isFormula("=SUM(A1:A5)"); // true
isFormula("hello");         // false
```

### Event Emitter Hook

```tsx
import { useEventEmitter } from "gridex";

const emitter = useEventEmitter();
emitter.on("cellClicked", (data) => { /* handle */ });
emitter.emit("customEvent", { payload: "data" });
```

## Monorepo Commands

```bash
pnpm build              # Build the library (tsup)
pnpm test               # Run all tests (vitest)
pnpm test:watch         # Watch mode tests
pnpm lint               # ESLint across workspaces
pnpm typecheck          # TypeScript check
pnpm format             # Prettier write
pnpm dev:docs           # Start Storybook (port 6006)
pnpm dev:playground     # Start playground (port 5173)
```

## Architecture Notes

- **Monorepo:** pnpm workspaces — `packages/gridex`, `packages/gridex-mantine`, `apps/docs`, `apps/playground`, `apps/landing`
- **Build:** tsup outputs ESM + CJS + `.d.ts`. CSS via CSS Modules.
- **Turbopack compatible** — CSS Modules use local `.darkTheme` class instead of root-level `:global()` selectors. No `--webpack` flag needed with Next.js Turbopack.
- **Storybook resolves from source** (not `dist/`) because tsup compiles CSS Modules to empty objects
- **Server-side `dataSource` bypasses intermediate hooks** to prevent infinite re-render loops
- **`useDataSource` uses serialized primitive deps** (`JSON.stringify`) to avoid object identity infinite loops
- **Pinned columns cannot be dragged** — sticky position + drag reorder creates confusing UX
- **i18n uses deep partial merge** — pass a `DeepPartial<GridexTranslations>` to override specific strings
- **gridex-mantine is fully localized** — all 21 slot components use `useTranslations()` from gridex's i18n system
