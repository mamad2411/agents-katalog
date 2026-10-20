---
name: kendo-ui-data-binding
description: Use when implementing or reviewing Kendo UI DataSource configuration, MVVM ViewModel patterns, remote transport, paging, filtering, sorting, grouping, and real-time data binding.
---

# Kendo UI Data Binding

## Specialization

Implement and review expert-level Kendo UI data binding covering DataSource configuration, remote transport design, MVVM ViewModel patterns, schema mapping, hierarchical DataSource, real-time SignalR transport, and observable array/object patterns — grounded in official Kendo UI DataSource documentation.

## Trigger Conditions

- Configuring a `kendo.data.DataSource` for remote or local data.
- Designing transport `read`, `create`, `update`, `destroy` endpoints and their request/response contracts.
- Mapping server response schema to Kendo UI field contracts.
- Implementing paging, sorting, filtering, and grouping — server-side or client-side.
- Using `kendo.observable()` and `kendo.bind()` for MVVM patterns.
- Wiring multiple widgets to a shared DataSource with synchronized selection.
- Implementing hierarchical DataSource for TreeView or hierarchical Grid.
- Integrating SignalR for real-time data push into a widget.
- Debugging DataSource request/response cycle failures.

## Scope Boundaries

In scope:

- `kendo.data.DataSource` configuration: transport, schema, sort, filter, group, aggregate, page size.
- Transport request/response lifecycle: `read`, `create`, `update`, `destroy`, `submit` (batch).
- Schema field mapping: `model.id`, `model.fields`, `parse`, `data`, `total`, `errors`.
- MVVM: `kendo.observable()`, `kendo.bind()`, `data-bind` attribute contracts.
- ObservableArray and ObservableObject methods: `push`, `splice`, `get`, `set`, `bind`.
- Hierarchical DataSource for nested data structures.
- SignalR transport integration.
- Error handling: transport error callbacks, DataSource `error` event, validation error surfacing.

Out of scope:

- Widget-specific configuration options (see `kendo-ui-core`).
- SASS theming (see `kendo-ui-theming`).
- Server-side endpoint implementation.
- Security audit of transport URLs or response handling (see `kendo-ui-security`).

## Inputs

- DataSource type: local array, remote JSON, OData v3/v4, SignalR, custom transport.
- Endpoint URL contract and response envelope structure.
- Paging, sorting, filtering, grouping mode: server-side or client-side.
- Kendo UI version in use.
- Existing DataSource configuration to review (if applicable).

## Required Outputs

- Correct DataSource configuration with schema, transport, and model definition.
- Request parameterization contract for each transport operation.
- Schema parse function if server envelope is non-standard.
- Error handling strategy: transport errors, validation errors, and UI feedback path.
- MVVM ViewModel with explicit `get`/`set` contract for two-way binding.
- Batch vs. individual operation recommendation with rationale.
- Security note for any URL or response data that flows into widget templates (route to `kendo-ui-security`).

## Core Patterns

### Remote DataSource

```javascript
var dataSource = new kendo.data.DataSource({
    transport: {
        read: {
            url: "/api/products",
            dataType: "json"
        },
        update: {
            url: function(data) { return "/api/products/" + data.id; },
            method: "PUT",
            dataType: "json"
        },
        destroy: {
            url: function(data) { return "/api/products/" + data.id; },
            method: "DELETE"
        },
        create: {
            url: "/api/products",
            method: "POST",
            dataType: "json"
        },
        parameterMap: function(data, type) {
            if (type === "read") {
                return kendo.stringify(data);
            }
            return data;
        }
    },
    schema: {
        model: {
            id: "id",
            fields: {
                id:    { type: "number", editable: false },
                name:  { type: "string", validation: { required: true } },
                price: { type: "number", validation: { required: true, min: 0 } }
            }
        },
        data: "data",
        total: "total",
        errors: "errors"
    },
    pageSize: 20,
    serverPaging: true,
    serverSorting: true,
    serverFiltering: true,
    error: function(e) {
        // Surface transport errors; never swallow silently
        console.error("DataSource error:", e.errors || e.status);
    }
});
```

### MVVM ViewModel

```javascript
var viewModel = kendo.observable({
    products: new kendo.data.DataSource({ /* ... */ }),
    selectedProduct: null,
    selectProduct: function(e) {
        this.set("selectedProduct", e.data);
    }
});

kendo.bind($("#view"), viewModel);
```

### OData Transport

```javascript
var dataSource = new kendo.data.DataSource({
    type: "odata-v4",
    transport: {
        read: { url: "/odata/Products" }
    },
    schema: {
        model: { id: "Id" }
    },
    serverPaging: true,
    serverSorting: true,
    serverFiltering: true
});
```

## Error Handling Requirements

- Always define a DataSource `error` event handler. Silent failures create invisible data loss.
- Surface validation errors from `schema.errors` in the widget UI, not only in the console.
- For CRUD grids, call `dataSource.cancelChanges()` in the error handler to prevent stale edits.

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Remote read-only DataSource wired to one widget | Data loads and renders correctly |
| L2 Practical | Full CRUD DataSource with schema and error handling | Create, read, update, delete cycle tested end-to-end |
| L3 Composition | Shared DataSource across multiple widgets with MVVM ViewModel | ViewModel observable state drives all bound widgets |
| L4 Expert | SignalR real-time transport or hierarchical DataSource with cross-level selection | Real-time updates or nested data hierarchy verified end-to-end |
