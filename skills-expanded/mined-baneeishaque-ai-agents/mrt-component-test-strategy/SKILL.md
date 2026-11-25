---
name: mrt-component-test-strategy
description: Test Material React Table components with Jest+RTL under CRA's resetMocks — mock MRT, capture useMaterialReactTable options, isolate component deps, and avoid common pitfalls.
category: Testing & Debugging
---

# MRT Component Test Strategy

Unit-test Material React Table (MRT) components with Jest + React Testing
Library, specifically under CRA 5's `resetMocks: true` default.

## When to use

Use this skill when writing or debugging Jest+RTL tests for components that
use `useMaterialReactTable()` and `<MaterialReactTable>` from the
`material-react-table` library. This includes:

- Creating a new test file for an MRT-based table component.
- Debugging failing MRT tests where the table does not render or
  `mockTableOptions` is empty.
- Adding config verification tests (checking `enable*` props, manual
  pagination, etc.).
- Writing tests that verify toolbar actions, column rendering, or
  hierarchical row data.

## Composition Rationale

This skill is a composer: it does NOT re-implement the CRA `resetMocks: true`
survival patterns. It delegates those to the base
[`cra-reset-mocks-test-strategy`](../cra-reset-mocks-test-strategy/SKILL.md)
skill and adds only MRT-specific knowledge.

*Composition mechanism by base section:*

1. **Base §2.1 (Plain Arrow Functions)** — applied to all static hook mocks
   used alongside MRT (e.g., `useTablePersistence`, `useFilterLogic`,
   `useExportActions`).
2. **Base §2.2 (Wrapper Functions)** — applied to `useQuery` and
   `useMutation` which need per-test control for loading/error/data states.
3. **Base §2.3 (Component Mocks)** — applied to `MaterialReactTable` itself
   and to any sub-components like `FileSelectionModal`,
   `TableFilterComponent`.
4. **Base §2.4 (Table Methods)** — applied to the mock table instance
   returned by `useMaterialReactTable`, where all methods must be plain
   arrow functions.

**MRT-specific value-add over the base alone:** The exact structure of the
`material-react-table` mock (options capture, row rendering with Cell
support, locale mock), the `mockTableOptions` assertion pattern, and
common MRT pitfalls (renderToolbarCustomActions needing a table stub,
column rendering for Cell accessors) are all MRT-specific and do not belong
in the generic base skill.

***

## Environment & Dependencies

- **Node.js 18+ / react-scripts 5.x**: Same as base skill.
- **@testing-library/react**: Required for rendering. Verify with
  `npx react-scripts test --version`.
- **material-react-table**: The library under test. Verify with
  `npm ls material-react-table`.
- **Python 3.12+**: Required for boilerplate generation script. Verify with
  `python3 --version`.

***

## 1. MRT Mock Structure

### 1.1 Core mock template

The full MRT mock must be placed at the module level, before imports:

```typescript
jest.mock("material-react-table/locales/en", () => ({ MRT_Localization_EN: {} }));

jest.mock("material-react-table", () => {
  const React = require("react");
  return {
    useMaterialReactTable: (options: any) => {
      mockTableOptions = options;
      return {
        ...options,
        columns: options.columns?.map((col: any) => ({
          ...col,
          getIsVisible: () => true,
          getSize: () => col.size || 150,
        })) || [],
        getAllColumns: () => (options.columns || []).map((col: any) => ({
          ...col,
          getIsVisible: () => true,
          getSize: () => col.size || 150,
        })),
        getState: () => ({
          isFullScreen: false,
          isSaving: false,
          showAlertBanner: false,
          showProgressBars: false,
          ...options.state,
        }),
        getRowModel: () => ({ rows: [] }),
        getIsSomeRowsSelected: () => false,
        getIsAllRowsSelected: () => false,
        getSelectedRowModel: () => ({ rows: [] }),
        resetRowSelection: () => {},
        resetColumnFilters: () => {},
        resetSorting: () => {},
        resetColumnVisibility: () => {},
        resetColumnOrder: () => {},
        resetColumnSizing: () => {},
        resetExpanded: () => {},
        resetGrouping: () => {},
        setRowSelection: () => {},
        setEditingRow: () => {},
        toggleAllRowsSelected: () => {},
      };
    },
    MaterialReactTable: ({ table }: any) => {
      return React.createElement("div", { "data-testid": "mrt-table" },
        table?.data?.map((row: any, i: number) =>
          React.createElement("div", {
            key: i,
            "data-testid": `mrt-row-${i}`,
            "data-exec-id": row.exec_id || "",
          },
            table?.columns?.map((col: any, j: number) => {
              const cellCtx = {
                cell: { getValue: () => row[col.accessorKey] },
                row: { original: row },
              };
              if (col.Cell) {
                return React.createElement("div", {
                  key: j,
                  "data-testid": `cell-${i}-${col.accessorKey || j}`,
                }, React.createElement(col.Cell, cellCtx));
              }
              return React.createElement("span", {
                key: j,
                "data-testid": `cell-${i}-${col.accessorKey || j}`,
              }, row[col.accessorKey] ?? "");
            })
          )
        )
      );
    },
  };
});
```

### 1.2 Options capture variable

Declare a module-level variable before the mock:

```typescript
var mockTableOptions: Record<string, any> = {};
```

Reset it in `beforeEach`:

```typescript
beforeEach(() => {
  mockTableOptions = {};
});
```

All config assertions read from this variable.

### 1.3 Key constraints (why not jest.fn())

| Element | Why plain fn | Consequence of jest.fn() |
| --------- | ------------- | ------------------------- |
| `MaterialReactTable` component | Must render React elements every render | Returns `undefined` → no `mrt-table` in DOM |
| `resetRowSelection`, etc. | Called by component internals | Silent failures, but component may crash on chained calls |
| `getState`, `getRowModel` | Called by MRT internals for state | Returns `undefined` → component crashes on property access |

All of these must be plain arrow functions per the base skill's §2.3 and §2.4.

***

## 2. MRT-specific Assertion Patterns

### 2.1 Config verification

Assert on `mockTableOptions` properties directly:

```typescript
expect(mockTableOptions.enableColumnFilters).toBe(true);
expect(mockTableOptions.enableDensityToggle).toBe(true);
expect(mockTableOptions.enableFullScreenToggle).toBe(true);
expect(mockTableOptions.enableColumnResizing).toBe(true);
expect(mockTableOptions.enableStickyHeader).toBe(true);
expect(mockTableOptions.enableColumnOrdering).toBe(true);
expect(mockTableOptions.enableGrouping).toBe(true);
expect(mockTableOptions.manualSorting).toBe(true);
expect(mockTableOptions.manualPagination).toBe(true);
```

### 2.2 Toolbar action handler wiring

```typescript
expect(mockTableOptions.onShowColumnFiltersChange).toBeDefined();
expect(mockTableOptions.onDensityChange).toBeDefined();
expect(mockTableOptions.onPaginationChange).toBeDefined();
expect(mockTableOptions.enableFullScreenToggle).toBe(true);
```

### 2.3 Error and empty state config

```typescript
expect(mockTableOptions.muiToolbarAlertBannerProps.color).toBe("error");
expect(mockTableOptions.muiToolbarAlertBannerProps.children).toBe("Error loading data");
expect(mockTableOptions.localization?.noRecordsToDisplay).toBe(" No Data found");
```

### 2.4 Row rendering verification

The mock renders rows as `<div data-testid="mrt-row-{i}">`. Assert on
data attributes:

```typescript
const row0 = screen.getByTestId("mrt-row-0");
expect(row0).toHaveAttribute("data-exec-id", "EXEC001");
```

***

## 3. Associated Component Mocks

MRT table components typically import several supporting modules that must
be mocked to avoid uncontrolled dependencies:

### 3.1 FileUpload/FileSelectionModal

Uses `useNavigate()` from `react-router-dom`. Mock as a no-op div:

```typescript
jest.mock("../FileUpload/FileSelectionModal", () => {
  const r = require("react");
  const FakeComponent = (props: any) =>
    r.createElement("div", { "data-testid": "file-selection-modal" });
  FakeComponent.displayName = "FileSelectionModal";
  return { __esModule: true, default: FakeComponent };
});
```

### 3.2 TableFilterComponent

Typically a named/default export. Mock with a testid:

```typescript
jest.mock("../Filters/TableFilterComponent", () => {
  const r = require("react");
  return {
    __esModule: true,
    default: () => r.createElement("div", { "data-testid": "table-filter-component" }),
  };
});
```

### 3.3 QueryClientProvider wrapper

The component is usually wrapped in `QueryClientProvider` by its export.
The `App` export (often co-exported alongside the table) provides this
wrapper and should be the render target, not the raw table component.

***

## 4. Boilerplate Generator

The [scripts/generate-mrt-test-boilerplate.py](scripts/generate-mrt-test-boilerplate.py)
script generates the MRT mock boilerplate and supporting test structure:

```bash
# Generate boilerplate for a new test
python3 scripts/generate-mrt-test-boilerplate.py --output src/Component.early.test/Component.early.test.tsx

# Generate only the MRT mock section
python3 scripts/generate-mrt-test-boilerplate.py --section mock --stdout
```

The script produces: MRT mock, locale mock, options capture variable,
`renderApp` helper pattern, and common assertion helpers.

***

## 5. Verification

Run the test suite and confirm:

1. `mrt-table` data-testid is present in the rendered DOM.
2. `mockTableOptions` is populated after render (config tests pass).
3. Row testids (`mrt-row-0`, `mrt-row-1`, etc.) exist for provided data.
4. All toolbar action buttons are findable by role/name queries.
5. No `jest.fn() is not a function` or `useQuery is not a function` errors.

```bash
npx react-scripts test --watchAll=false --testPathPattern="<test-name>"
```

Expected:

```text
Test Suites: 1 passed, 1 total
Tests:       N passed, N total
```

***

## Composition by Higher-Level Skills

(None yet — this is a domain-specific composer, not a base skill.)

## Related Skills

- [`cra-reset-mocks-test-strategy`](../cra-reset-mocks-test-strategy/SKILL.md) — Base skill for surviving CRA
`resetMocks: true` in `jest.mock` factories. This composer depends on it.
- [`mrt-configuration-debug`](../mrt-configuration-debug/SKILL.md) — Complementary skill for runtime MRT config
debugging with playwright-cli (post-deployment verification).
- [`table-persistence-implementation`](../table-persistence-implementation/SKILL.md) — Companion skill for the
`useTablePersistence` hook often used alongside MRT.
- [`skill-factory`](../skill-factory/SKILL.md) — Protocol used to create this skill.
