---
name: kendo-ui-core
description: Use when implementing or reviewing Kendo UI components including Grid, Chart, Scheduler, TreeView, Editor, and core widget patterns with correct initialization, configuration, and lifecycle management.
---

# Kendo UI Core

## Specialization

Implement and review expert-level Kendo UI component usage covering widget initialization, configuration contracts, event binding, method invocation, DataSource wiring, and widget destruction — grounded in official Kendo UI API documentation.

## Trigger Conditions

- Initializing a Kendo UI widget via jQuery plugin (`.kendoGrid()`, `.kendoChart()`, etc.).
- Wiring a Kendo UI component to a remote or local DataSource.
- Invoking widget methods (`dataItem()`, `refresh()`, `setDataSource()`, `destroy()`).
- Binding widget events via `bind()` or the options hash.
- Composing complex widgets: Grid with locked columns, hierarchical Grid, Chart with multiple series.
- Reviewing widget initialization order dependencies or lifecycle teardown.
- Choosing between Kendo UI widget initialization approaches: jQuery plugin, `kendo.init()`, MVVM `data-role`.
- Implementing widget templates (row templates, column templates, header templates).

## Scope Boundaries

In scope:

- Widget initialization patterns: jQuery plugin, MVVM `kendo.init()`, and programmatic `kendo.bind()`.
- Configuration option contracts per widget (Grid, Chart, Scheduler, Editor, TreeView, PanelBar, TabStrip, Window, Dialog, DropDownList, ComboBox, AutoComplete, DatePicker, NumericTextBox, Slider, Upload, Splitter, Tooltip).
- Event binding and unbinding lifecycle.
- Widget method invocation and return contract.
- DataSource option wiring within widget configuration.
- Widget destruction and memory cleanup (`destroy()`, event unbinding).
- Template syntax: Kendo UI template (`#= #`, `#: #`, `# #`) and its escaping rules.
- Widget API versioning and deprecated option detection.

Out of scope:

- DataSource internals and remote transport configuration (see `kendo-ui-data-binding`).
- SASS theming and visual token customization (see `kendo-ui-theming`).
- Accessibility compliance review (see `kendo-ui-accessibility`).
- Form validation patterns (see `kendo-ui-forms`).
- Security audit of template content (see `kendo-ui-security`).
- Performance profiling of large datasets (see `kendo-ui-performance`).

## Inputs

- Target widget(s) and their configuration requirements.
- Kendo UI version in use and framework variant (jQuery assumed unless stated).
- Existing initialization code to review (if applicable).
- DataSource type: local array, remote JSON, OData, SignalR.
- Browser target matrix (if IE11 or legacy compatibility applies).

## Required Outputs

- Correct widget initialization pattern with documented option rationale.
- Event binding contract with explicit unbind obligation.
- Method invocation examples covering the target use cases.
- Widget destruction sequence with memory-safe teardown.
- Template usage with XSS-safe encoding confirmation (route to `kendo-ui-security` if unsafe patterns are found).
- DataSource wiring stub (full DataSource guidance deferred to `kendo-ui-data-binding`).
- Deprecated option or method flag with replacement guidance.

## Core Patterns

### Widget Initialization

```javascript
// jQuery plugin — preferred for single-widget initialization
$("#grid").kendoGrid({
    dataSource: { /* ... */ },
    columns: [{ field: "name", title: "Name" }],
    pageable: true,
    sortable: true
});

// Retrieve widget instance
var grid = $("#grid").data("kendoGrid");
```

### Event Binding

```javascript
// Via options hash (preferred — binds before widget renders)
$("#grid").kendoGrid({
    dataBound: function(e) { /* handler */ },
    change: function(e) { /* handler */ }
});

// Via .bind() — after initialization
var grid = $("#grid").data("kendoGrid");
grid.bind("dataBound", function(e) { /* handler */ });

// Unbind on teardown — mandatory to prevent handler accumulation
grid.unbind("dataBound");
```

### Template Safety

```javascript
// XSS-safe: encodes HTML entities
var template = kendo.template("<td>#: data.name #</td>");

// XSS-UNSAFE: renders raw HTML — only for trusted server content
var template = kendo.template("<td>#= data.html #</td>");
```

### Widget Destruction

```javascript
// Destroy widget and free event handlers and DOM references
var grid = $("#grid").data("kendoGrid");
if (grid) {
    grid.destroy();
    $("#grid").empty();
}
```

## Deprecated API Flags

| Deprecated | Replacement | Version Removed |
|---|---|---|
| `kendo.observable()` inline binding via `data-bind` in IE-only mode | Standard MVVM `kendo.bind()` | Check release notes |
| Widget `change` event on read-only widgets | Widget-specific event (e.g., `select`) | Varies by widget |

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Initialize one widget with minimal config | Widget renders with correct data |
| L2 Practical | Full widget config with events, methods, and teardown | All lifecycle phases covered |
| L3 Composition | Multi-widget interaction: detail Grid in master Grid, Chart linked to Grid selection | Cross-widget event wiring verified |
| L4 Expert | Custom widget authoring extending `kendo.ui.Widget` base class | Custom widget passes destroy, event, and option contract checks |
