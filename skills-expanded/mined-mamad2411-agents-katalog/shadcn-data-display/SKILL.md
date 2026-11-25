---
name: shadcn-data-display
description: Use when implementing data-heavy shadcn/ui surfaces — covering TanStack Table DataTable patterns, shadcn Charts (Recharts), Command palette, Combobox, and complex list/grid compositions with sorting, filtering, pagination, and accessibility.
---

# shadcn/ui Data Display

## Specialization

Provide expert-level guidance for implementing data-heavy UI surfaces using shadcn/ui — covering `DataTable` with TanStack Table v8, `Chart` components with Recharts, `Command` palette and `Combobox` for search and selection, and complex list and grid compositions with sorting, filtering, pagination, virtualization, and full accessibility.

This skill covers data display patterns. General component design and CVA variants are handled by `shadcn-component-design`. Form inputs and validation are handled by `shadcn-forms`. Quality gate review is handled by `shadcn-quality-gate`.

## Trigger Conditions

- Implementing a `DataTable` with sorting, filtering, column visibility, row selection, or pagination.
- Building a `Command` palette or `Combobox` with search, async loading, grouping, or custom rendering.
- Implementing shadcn `Chart` components (bar, line, area, pie, radar, radial) with Recharts.
- Building a data grid or list with virtualization requirements (> 500 rows).
- Composing complex multi-select, tag input, or search-driven selection patterns.
- Auditing an existing data table or chart for accessibility, performance, or pattern correctness.

## When Not to Use

- Simple static lists or display cards without interactivity (use `shadcn-component-design`).
- Form inputs including basic `Select` with static options (use `shadcn-forms`).
- Chart data sourcing, API design, or server-side aggregation logic.
- Quality gate sign-off for a completed implementation (use `shadcn-quality-gate`).

## Inputs

- Data shape and volume (row count, column count, update frequency).
- Required interactive features: sorting, filtering, pagination, row selection, column visibility.
- Chart type and data series structure.
- Framework in use and RSC constraints.
- Accessibility requirements (default: WCAG 2.2 AA).
- Virtualization requirements if applicable (row count threshold, scrollable container constraints).
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

| Output | Description |
|---|---|
| Column definition schema | TanStack Table `ColumnDef<TData>[]` with typed accessors, headers, and cell renderers |
| Table component | Fully typed `DataTable` using shadcn `Table` primitives with feature flags for sorting, filtering, and pagination |
| Filter implementation | Column filter or global filter wired to `useReactTable` state; debounced input |
| Pagination implementation | `PaginationState` managed in table; shadcn `Pagination` component wired to table API |
| Chart component | Recharts chart wrapped in shadcn `ChartContainer` with `ChartConfig`, tooltips, and legend |
| Command/Combobox implementation | `Command` or `Combobox` with correct open/close state, search, keyboard navigation, and selection model |
| Accessibility annotation | ARIA roles, keyboard navigation, and screen-reader labels for all interactive data components |
| Performance assessment | Virtualization decision, re-render strategy, and memoization plan for large datasets |
| Readiness summary | Open items, deferred features, and known edge cases |

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Render a basic sortable data table | Table renders, one column sorts, data displays correctly |
| L2 Practical Delivery | Full production DataTable with filtering, pagination, and selection | All interactive features working; accessibility annotation complete |
| L3 Advanced Patterns | Async data, virtualization, or complex chart compositions | Server-side sort/filter wired; virtualization active for large datasets; chart config complete |
| L4 Expert Standardization | Reusable cross-project DataTable and Chart patterns | Typed generic DataTable factory, Chart wrapper conventions, and pattern library documented |

## DataTable Pattern

### 1. Install TanStack Table

```bash
npm install @tanstack/react-table
npx shadcn add table
```

### 2. Define Column Definitions

```tsx
"use client"

import { ColumnDef } from "@tanstack/react-table"
import { ArrowUpDown, MoreHorizontal } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Checkbox } from "@/components/ui/checkbox"

export type Payment = {
  id: string
  amount: number
  status: "pending" | "processing" | "success" | "failed"
  email: string
}

export const columns: ColumnDef<Payment>[] = [
  {
    id: "select",
    header: ({ table }) => (
      <Checkbox
        checked={table.getIsAllPageRowsSelected()}
        onCheckedChange={(value) => table.toggleAllPageRowsSelected(!!value)}
        aria-label="Select all"
      />
    ),
    cell: ({ row }) => (
      <Checkbox
        checked={row.getIsSelected()}
        onCheckedChange={(value) => row.toggleSelected(!!value)}
        aria-label="Select row"
      />
    ),
    enableSorting: false,
    enableHiding: false,
  },
  {
    accessorKey: "status",
    header: "Status",
    cell: ({ row }) => <div className="capitalize">{row.getValue("status")}</div>,
  },
  {
    accessorKey: "email",
    header: ({ column }) => (
      <Button variant="ghost" onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}>
        Email <ArrowUpDown className="ml-2 h-4 w-4" />
      </Button>
    ),
  },
  {
    accessorKey: "amount",
    header: () => <div className="text-right">Amount</div>,
    cell: ({ row }) => {
      const amount = parseFloat(row.getValue("amount"))
      return <div className="text-right font-medium">{new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(amount)}</div>
    },
  },
]
```

### 3. DataTable Component

```tsx
"use client"

import {
  flexRender, getCoreRowModel, getFilteredRowModel,
  getPaginationRowModel, getSortedRowModel, useReactTable,
  type ColumnFiltersState, type SortingState, type VisibilityState,
} from "@tanstack/react-table"
import { useState } from "react"
import { Input } from "@/components/ui/input"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Button } from "@/components/ui/button"

interface DataTableProps<TData, TValue> {
  columns: ColumnDef<TData, TValue>[]
  data: TData[]
}

export function DataTable<TData, TValue>({ columns, data }: DataTableProps<TData, TValue>) {
  const [sorting, setSorting] = useState<SortingState>([])
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([])
  const [columnVisibility, setColumnVisibility] = useState<VisibilityState>({})
  const [rowSelection, setRowSelection] = useState({})

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    onColumnVisibilityChange: setColumnVisibility,
    onRowSelectionChange: setRowSelection,
    state: { sorting, columnFilters, columnVisibility, rowSelection },
  })

  return (
    <div className="space-y-4">
      <Input
        placeholder="Filter emails..."
        value={(table.getColumn("email")?.getFilterValue() as string) ?? ""}
        onChange={(e) => table.getColumn("email")?.setFilterValue(e.target.value)}
        className="max-w-sm"
      />
      <div className="rounded-md border">
        <Table>
          <TableHeader>
            {table.getHeaderGroups().map((headerGroup) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header) => (
                  <TableHead key={header.id}>
                    {header.isPlaceholder ? null : flexRender(header.column.columnDef.header, header.getContext())}
                  </TableHead>
                ))}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows?.length ? (
              table.getRowModel().rows.map((row) => (
                <TableRow key={row.id} data-state={row.getIsSelected() && "selected"}>
                  {row.getVisibleCells().map((cell) => (
                    <TableCell key={cell.id}>
                      {flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </TableCell>
                  ))}
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={columns.length} className="h-24 text-center">No results.</TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
      <div className="flex items-center justify-between">
        <div className="text-sm text-muted-foreground">
          {table.getFilteredSelectedRowModel().rows.length} of {table.getFilteredRowModel().rows.length} row(s) selected.
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" onClick={() => table.previousPage()} disabled={!table.getCanPreviousPage()}>Previous</Button>
          <Button variant="outline" size="sm" onClick={() => table.nextPage()} disabled={!table.getCanNextPage()}>Next</Button>
        </div>
      </div>
    </div>
  )
}
```

### Server-Side Sorting and Filtering

For large datasets, move sort/filter state to the server:

```tsx
const table = useReactTable({
  data,
  columns,
  manualSorting: true,       // server owns sort
  manualFiltering: true,     // server owns filter
  manualPagination: true,    // server owns page
  pageCount: totalPages,     // from server response
  onSortingChange: (updater) => {
    const newSorting = typeof updater === "function" ? updater(sorting) : updater
    setSorting(newSorting)
    router.push({ query: { sort: newSorting[0]?.id, dir: newSorting[0]?.desc ? "desc" : "asc" } })
  },
  // ...
})
```

## Command Palette Pattern

```tsx
npx shadcn add command
```

```tsx
"use client"

import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "@/components/ui/command"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { Button } from "@/components/ui/button"
import { ChevronsUpDown, Check } from "lucide-react"
import { cn } from "@/lib/utils"
import { useState } from "react"

// Combobox pattern (selection from Command)
export function Combobox({ options, value, onSelect }: ComboboxProps) {
  const [open, setOpen] = useState(false)

  return (
    <Popover open={open} onOpenChange={setOpen}>
      <PopoverTrigger asChild>
        <Button variant="outline" role="combobox" aria-expanded={open} className="w-[200px] justify-between">
          {value ? options.find((o) => o.value === value)?.label : "Select option..."}
          <ChevronsUpDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
        </Button>
      </PopoverTrigger>
      <PopoverContent className="w-[200px] p-0">
        <Command>
          <CommandInput placeholder="Search..." />
          <CommandList>
            <CommandEmpty>No results found.</CommandEmpty>
            <CommandGroup>
              {options.map((option) => (
                <CommandItem key={option.value} value={option.value} onSelect={(current) => { onSelect(current === value ? "" : current); setOpen(false) }}>
                  <Check className={cn("mr-2 h-4 w-4", value === option.value ? "opacity-100" : "opacity-0")} />
                  {option.label}
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  )
}
```

**Command accessibility rules:**
- `CommandInput` provides the accessible search label for the listbox.
- `CommandItem` must include visible text — icon-only items need an `aria-label`.
- Keyboard: `↑`/`↓` navigates items, `Enter` selects, `Escape` closes. Radix manages this automatically.

## Chart Pattern

```bash
npx shadcn add chart
```

```tsx
"use client"

import { Bar, BarChart, CartesianGrid, XAxis } from "recharts"
import { ChartConfig, ChartContainer, ChartTooltip, ChartTooltipContent } from "@/components/ui/chart"

const chartData = [
  { month: "January", desktop: 186, mobile: 80 },
  { month: "February", desktop: 305, mobile: 200 },
]

const chartConfig = {
  desktop: { label: "Desktop", color: "hsl(var(--chart-1))" },
  mobile: { label: "Mobile", color: "hsl(var(--chart-2))" },
} satisfies ChartConfig

export function BarChartComponent() {
  return (
    <ChartContainer config={chartConfig} className="min-h-[200px] w-full">
      <BarChart data={chartData}>
        <CartesianGrid vertical={false} />
        <XAxis dataKey="month" tickLine={false} tickMargin={10} axisLine={false} tickFormatter={(v) => v.slice(0, 3)} />
        <ChartTooltip content={<ChartTooltipContent />} />
        <Bar dataKey="desktop" fill="var(--color-desktop)" radius={4} />
        <Bar dataKey="mobile" fill="var(--color-mobile)" radius={4} />
      </BarChart>
    </ChartContainer>
  )
}
```

**Chart rules:**
- Always use `hsl(var(--chart-N))` token variables for chart colors — never raw hex.
- `ChartContainer` wraps Recharts with correct `ResponsiveContainer` sizing and token injection.
- `ChartTooltip` with `ChartTooltipContent` provides accessible, themed tooltips automatically.
- Charts are visual only by default — for accessibility, add a `aria-label` on `ChartContainer` and provide a data table alternative for screen reader users.

## Virtualization for Large Datasets

For tables exceeding ~500 rows, add `@tanstack/react-virtual`:

```bash
npm install @tanstack/react-virtual
```

```tsx
import { useVirtualizer } from "@tanstack/react-virtual"

const rowVirtualizer = useVirtualizer({
  count: table.getRowModel().rows.length,
  getScrollElement: () => parentRef.current,
  estimateSize: () => 45, // estimated row height in px
  overscan: 10,
})
```

Virtualization is required when:
- Row count exceeds 500 in a client-rendered table, or
- The table is inside a fixed-height scrollable container with dynamic data.

## Accessibility Requirements

| Component | Requirement |
|---|---|
| DataTable | `<table>` with `<thead>`, `<tbody>`; sortable headers are `<button>` inside `<th>`; `aria-sort` on sorted column |
| Row selection | Checkbox `aria-label` on each row; "Select all" checkbox on header |
| Pagination | Navigation buttons labeled; current page announced via `aria-live` region |
| Command/Combobox | `role="combobox"` on trigger; `aria-expanded`; `role="listbox"` on options list |
| Chart | `aria-label` on container; data table alternative available for screen readers |

## Pragmatic Stop Rule

Stop when the column definitions are typed, the table component handles all required interactive features, accessibility annotations are complete, and the performance assessment confirms whether virtualization is needed. Chart config must use `--chart-N` tokens. Open items must be in the readiness summary.
