---
name: kendo-ui-performance
description: Use when diagnosing or improving Kendo UI performance covering Grid virtual scrolling, DataSource paging strategy, widget initialization cost, bundle size optimization, and memory leak prevention.
---

# Kendo UI Performance

## Specialization

Diagnose and remediate Kendo UI performance bottlenecks covering Grid virtual scrolling configuration, server-side paging vs. client-side paging trade-offs, widget initialization cost on large pages, DataSource request batching, DOM recycling via virtual scrolling, JavaScript heap memory management, and Kendo UI bundle size reduction — grounded in official Kendo UI performance guidance.

## Trigger Conditions

- Grid render time is slow with large datasets (> 500 rows).
- Page initialization is slow because many Kendo UI widgets initialize on DOM ready.
- Memory consumption grows over time (navigating between Kendo UI-heavy views).
- DataSource is making excessive server requests (unintentional re-reads on every sort/filter).
- Kendo UI bundle size exceeds the project performance budget.
- Chart renders with noticeable delay when data series are large.
- Scheduler becomes unresponsive with many events in a date range.
- A `kendo-ui-quality-gate` audit identifies a performance finding.

## Scope Boundaries

In scope:

- Grid: virtual scrolling, server paging, locked columns performance cost, column virtualization.
- DataSource: server-side vs. client-side paging/filtering/sorting decisions, batch request reduction.
- Widget initialization: deferred initialization, lazy initialization on tab/accordion reveal.
- Bundle size: Kendo UI custom build strategy, tree-shaking (for Angular/React variants), CDN loading.
- Memory management: `destroy()` obligation, event handler accumulation, DataSource disposal.
- Chart: data decimation for large series, deferred rendering.
- Scheduler: event rendering strategy for dense calendars.

Out of scope:

- Server-side query optimization (use `sql-server-query-tuning` or backend skills).
- Network latency reduction beyond DataSource request batching.
- Core Web Vitals measurement (use `web-ux-performance`).
- CSS rendering performance (use `tailwind-performance` or browser profiling).

## Inputs

- Kendo UI version in use.
- Widget(s) exhibiting performance issues.
- Dataset size: row count, column count, event count.
- Current paging strategy: client-side or server-side.
- Bundle size current measurement (gzip KB).
- Browser profiling data (if available).

## Required Outputs

- Paging strategy recommendation with server-side vs. client-side rationale.
- Virtual scrolling configuration (Grid) or deferred rendering (Chart, Scheduler) where applicable.
- Widget initialization deferral plan for pages with many widgets.
- Bundle size reduction strategy: custom build or CDN split.
- Memory leak prevention checklist: `destroy()` calls, DataSource disposal, event handler cleanup.
- Benchmark targets: Grid initial render < 200ms for virtualized 10K-row dataset at target page size.

## Core Patterns

### Grid Virtual Scrolling

```javascript
$("#grid").kendoGrid({
    dataSource: {
        transport: { read: { url: "/api/items", dataType: "json" } },
        schema: { data: "data", total: "total" },
        pageSize: 100,        // Virtual scrolling renders one page at a time
        serverPaging: true,
        serverSorting: true,
        serverFiltering: true
    },
    scrollable: {
        virtual: true         // Enable row virtualization
    },
    height: 600,
    // Avoid locked columns with virtual scrolling — significant performance penalty
    columns: [
        { field: "id", width: 80 },
        { field: "name", width: 200 },
        { field: "status", width: 120 }
    ]
});
```

### Deferred Widget Initialization (TabStrip)

```javascript
// Only initialize Grids inside tabs when the tab is activated
$("#tabstrip").kendoTabStrip({
    activate: function(e) {
        var tab = $(e.contentElement);
        if (!tab.data("kendoGrid")) {
            tab.find(".grid-placeholder").kendoGrid({ /* ... */ });
        }
    }
});
```

### DataSource Request Batching

```javascript
// Batch CRUD operations to reduce round trips
var dataSource = new kendo.data.DataSource({
    batch: true,          // Sends all pending changes in one request
    transport: {
        update: { url: "/api/items/batch", method: "POST" },
        create: { url: "/api/items/batch", method: "POST" },
        destroy: { url: "/api/items/batch", method: "POST" }
    }
});
```

### Memory-Safe Widget Lifecycle

```javascript
// Before navigating away from a Kendo UI-heavy view:
function teardownView() {
    // Destroy all widgets in reverse initialization order
    $("[data-role]").each(function() {
        var widget = kendo.widgetInstance($(this));
        if (widget) { widget.destroy(); }
    });
    // Dispose DataSource references
    dataSource = null;
}
```

### Custom Build (Kendo UI for jQuery)

```bash
# Use the Kendo UI custom download builder at:
# https://www.telerik.com/download/kendo-ui
# Select only the components used in the project.
# Typical reduction: 800 KB → 200-300 KB gzip depending on component selection.
```

## Performance Benchmarks

| Scenario | Target |
|---|---|
| Grid initial render (virtual, 10K rows, pageSize 100) | < 200ms |
| DataSource read request (server paging, single page) | < 300ms network (application dependent) |
| Widget initialization per page (20 widgets, DOM-ready) | < 500ms total |
| Memory per Grid instance (virtual, 100 visible rows) | < 10 MB heap delta |
| Kendo UI bundle (custom build, gzip) | ≤ 300 KB (component-dependent) |

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Enable server paging on one Grid | Server-paging DataSource active; client loads only current page |
| L2 Practical | Virtual scrolling + server-side paging, sorting, filtering | Grid renders 10K+ rows without scroll jank |
| L3 Hardening | Deferred init + memory-safe teardown + custom build | Page load budget met; no memory growth across navigation cycles |
| L4 Expert | Full performance evidence: benchmarks, heap profiles, bundle analysis | Evidence artifacts support promotion decision |
