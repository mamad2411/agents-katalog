---
name: syncfusion-angular-grid
description: Implements Syncfusion Angular Grid component for feature-rich data tables and grids. Use this when working with data display, sorting, filtering, grouping, aggregates, editing, or exporting. This skill covers grid configuration, CRUD operations, virtual scrolling or infinite scrolling,  hierarchy grids, state persistence, and advanced data management features for data-intensive applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Grids"
---

# Syncfusion Angular Grid

A comprehensive guide to implementing powerful, feature-rich data grids using Syncfusion's Angular Grid component. This skill covers all aspects of grid functionality from basic data binding to advanced features like virtual scrolling, hierarchical data, state management, and multi-format exports.

## Table of Contents

- [When to Use This Skill](#when-to-use-this-skill)
- [TreeGrid vs. Grid: Decision Guide](#treegrid-vs-grid-decision-guide)
- [Critical API Rules & Requirements](#critical-api-rules--requirements)
- [Feature Navigation Guide](#feature-navigation-guide)
- [Quick Start Example](#quick-start-example)
- [Common Patterns](#common-patterns)
- [Key Props & Configuration](#key-props--configuration)
- [Common Use Cases](#common-use-cases)

## When to Use This Skill

Use this skill when you need to:
- **Display tabular data** — Load and render structured data in a table format
- **Enable data operations** — Sort, filter, search, and paginate large datasets
- **Implement editing** — Add, update, and delete records with validation
- **Customize columns** — Configure column properties, templates, and layouts
- **Export data** — Generate Excel, PDF, or print-friendly reports
- **Handle advanced scenarios** — Hierarchical data, virtual scrolling, state persistence
- **Apply styling** — Theme grids, customize appearance, and style-specific elements
- **Optimize performance** — Implement infinite scrolling, virtual scrolling for large datasets

## TreeGrid vs. Grid: Decision Guide
 
| Requirement | Use TreeGrid | Use Grid |
|-------------|--------------|----------|
| **Data Structure** | Hierarchical/Tree/Nested | Flat/Tabular |
| **Parent-Child Relationships** | ✅ Native support | ❌ No (use Detail Template) |
| **Expand/Collapse Rows** | ✅ Built-in | ❌ No |
| **Nested Aggregates** | ✅ Includes children | ✅ Flat only |
| **Indent/Outdent Operations** | ✅ Yes | ❌ No |
| **Column Grouping** | ❌ No (use Grid) | ✅ Yes |
| **Performance (100K+ rows)** |  ✅Excellent | ✅ Excellent |
| **Use Cases** | Org charts, file systems, BoM | Orders, invoices, lists |

## Critical API Rules & Requirements

Grid's inbuilt API (137+ methods, 65+ events, 95+ properties) requires strict adherence to access patterns:

**⚠️ Detailed rules for proper API usage are located in the reference guides** — review the sections below based on your needs:

- 📄 **Method Access & Properties** → [references/programmatic-api.md](references/programmatic-api.md) — Learn @ViewChild requirement, method parameters, async handling, and refresh patterns
- 📄 **Event Handling** → [references/events-catalog.md](references/events-catalog.md) — Event signatures, timing, cancellation, and render event restrictions
- 📄 **Full API Reference:** [references/grid-properties-methods-events.md](references/grid-properties-methods-events.md) 
- 📄 **Module System** → [references/modules.md](references/modules.md) — Service injection requirements for feature methods
- 📄 **Selection** → [references/selection.md](references/selection.md) — Selection method prerequisites 
- 📄 **Backend Integration:** [references/adaptors.md](references/adaptors.md)

---

## Feature Navigation Guide

### Getting Started & Setup
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup
- Basic grid initialization
- CSS imports and themes
- Minimal working example

### Data Management
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Local and remote data binding
- Data source configuration
- API integration
- Real-time data updates

### Column Configuration
📄 **Read:** [references/columns.md](references/columns.md)
- Column properties and types
- Column templates
- Foreign key columns
- Column rendering options

**Related — Advanced Column Features:**  
📄 **Read:** [references/context-menu.md](references/context-menu.md) (context menu for columns)

### Row Management & Templates
📄 **Read:** [references/row.md](references/row.md)
- Row properties and events
- Row templates
- Detail row templates
- Row spanning

### Selection & Interaction
📄 **Read:** [references/selection.md](references/selection.md)
- Row, cell, and column selection
- Checkbox selection
- Selection events
- Multi-select patterns

### Data Operations
📄 **Read:** [references/filtering.md](references/filtering.md)
- Filter bar and filter menu
- Excel-like filtering
- Custom filters
- Programmatic filtering

📄 **Read:** [references/sorting.md](references/sorting.md)
- Single and multi-column sorting
- Custom sort order
- Sort events

📄 **Read:** [references/searching.md](references/searching.md)
- Global search functionality
- Search across columns
- Search algorithms

📄 **Read:** [references/paging.md](references/paging.md)
- Pagination setup
- Page size configuration
- Page change events

### Editing & Validation
📄 **Read:** [references/editing.md](references/editing.md)
- Edit types (inline, dialog, batch)
- Edit templates and custom editors
- Built-in validators (required, min, max, pattern)
- Validation rules and error messages
- Persisting changes to server

> ⚠️ **CRITICAL:** `[isPrimaryKey]="true"` is required on the key column — editing silently fails without it (no error thrown).

### Grouping & Aggregation
📄 **Read:** [references/grouping.md](references/grouping.md)
- Grouping columns
- Lazy-load grouping
- Caption templates

📄 **Read:** [references/aggregates.md](references/aggregates.md)
- Summary rows
- Custom aggregate functions
- Footer aggregates

### Export & Reporting
📄 **Read:** [references/excel-export.md](references/excel-export.md)
- Export to Excel formats
- Export options and customization
- Export events

📄 **Read:** [references/pdf-export.md](references/pdf-export.md)
- Export to PDF
- PDF templates and formatting
- Header and footer configuration

📄 **Read:** [references/print.md](references/print.md)
- Print functionality
- Print templates
- Print events

### Styling & UI Customization
📄 **Read:** [references/style-and-appearance.md](references/style-and-appearance.md)
- Theme selection
- CSS customization
- Style specific areas (header, rows, cells)
- Custom CSS classes

📄 **Read:** [references/toolbar.md](references/tool-bar.md)
- Toolbar items and configuration
- Custom toolbar buttons
- Toolbar events and click handlers

📄 **Read:** [references/clipboard.md](references/clipboard.md)
- Copy/paste functionality
- Clipboard events
- Clipboard selection management

### Advanced Column Features
📄 **Read:** [references/frozen.md](references/frozen.md)
- Freeze columns
- Multi-column freeze
- Freeze position configuration

> ⚠️ **Performance Warning:** `rowDataBound` and `queryCellInfo` fire on **every render/scroll** — NEVER make API calls inside them.
> ⚠️ **Conflict Risk:** Do NOT add both a column `[template]` AND a `rowDataBound` handler targeting the same field — produces duplicate, conflicting styling.

### Cell & Row Features
📄 **Read:** [references/cell.md](references/cell.md)
- Cell editing and selection
- Cell templates
- Cell spanning
- Cell-level events

### Context & Interaction
📄 **Read:** [references/context-menu.md](references/context-menu.md)
- Context menu items
- Custom context menu
- Context menu events
- Default menu configuration

### Advanced Features
📄 **Read:** [references/scrolling.md](references/scrolling.md)
- Virtual scrolling for 1K–100K+ records
- Infinite scrolling for continuous loading
- Sticky headers
- Scrolling performance optimization

> ⚠️ **CRITICAL:** `height` is required — scrolling is silently disabled without it (no error thrown).
> ⚠️ **INCOMPATIBLE:** Do NOT combine `enableVirtualization` or `enableInfiniteScrolling` with `allowPaging` — results are unpredictable.

| Rows | Mode | Key Config |
|---|---|---|
| < 1,000 | `allowPaging` | `Page` module |
| 1K – 100K | `enableVirtualization` + `height` | `VirtualScroll`, no paging |
| Continuous | `enableInfiniteScrolling` + `height` | `InfiniteScroll` |
| 100K+ grouped | `enableVirtualization` + `lazyLoadGrouping` | `VirtualScroll`, `Group` |

📄 **Read:** [references/hierarchy-grid.md](references/hierarchy-grid.md)
- Master-detail grids
- Child grid configuration
- Nested/hierarchical data
- Detail row templates
- Lazy-load child data

📄 **Read:** [references/state-management.md](references/state-management.md)
- Save grid state (columns, sorting, filters)
- Restore grid state
- State persistence options

📄 **Read:** [references/adaptive.md](references/adaptive.md)
- Responsive/mobile mode
- Adaptive layouts
- Touch interactions

📄 **Read:** [references/global-local.md](references/global-local.md)
- Keyboard shortcuts and navigation
- Global vs local settings
- Accessibility configurations

### Module System & Architecture
📄 **Read:** [references/modules.md](references/modules.md)
- Grid module architecture and 23+ feature services
- Service dependencies and relationships
- Module injection patterns in component decorators
- Bundle optimization via selective imports
- Performance impact of module inclusion

### Data Connectivity & Adaptors
📄 **Read:** [references/adaptors.md](references/adaptors.md)
- 7 adaptor types for backend integration
- UrlAdaptor, ODataV4Adaptor, WebApiAdaptor, GraphQLAdaptor
- Custom adaptors and RemoteSaveAdaptor
- Backend configuration examples (C#, Node.js)
- Request/response format specifications
- Error handling and adaptor comparison

### Performance Optimization
📄 **Read:** [references/performance.md](references/performance.md)
- Virtual scrolling for 10,000+ records
- Infinite scrolling and progressive loading
- Memory management and cleanup strategies
- Bundle size optimization
- Event debouncing and throttling
- Performance benchmarking and monitoring

### Accessibility & Compliance
📄 **Read:** [references/accessibility.md](references/accessibility.md)
- WCAG 2.2 and Section 508 compliance
- WAI-ARIA implementation and screen readers
- Keyboard navigation (Tab, arrows, Enter, Escape)
- Color contrast and focus management
- Accessibility testing tools (axe, NVDA, JAWS)
- Semantic HTML practices

### Data Validation
📄 **Read:** [references/validation.md](references/validation.md)
- Built-in validators (required, min, max, pattern)
- Custom validation functions
- Async validation with server checks
- Validation events and error display
- Server-side validation with ASP.NET
- Validation rules by column type

### Command Column & Row Actions
📄 **Read:** [references/command-column.md](references/command-column.md)
- Built-in commands (Edit, Delete, Save, Cancel)
- Custom command buttons
- Role-based and status-based commands
- Command click events
- Conditional command visibility
- CSS styling and icons

### Localization & Internationalization
📄 **Read:** [references/localization.md](references/localization.md)
- Multi-language support (60+ languages)
- Locale setup and culture configuration
- Number, date, and currency formatting
- RTL support (Arabic, Hebrew, Farsi)
- Custom localization and translation
- Language switcher implementation

### Responsive Design & Mobile
📄 **Read:** [references/responsive-design.md](references/responsive-design.md)
- Adaptive UI for mobile/tablet/desktop
- Responsive media queries and breakpoints
- Column visibility hiding rules
- Touch interactions (swipe, long-press)
- Mobile optimization strategies
- Device-specific styling patterns

### Programmatic Control

📄 **Read:** [references/programmatic-api.md](references/programmatic-api.md)
- The full programmatic method catalog
- Event prop reference
- Dynamic column control
- `setProperties()` examples, export hooks, and cross-feature

### Event Communication
 
📄 **Read:** [references/events-catalog.md](references/events-catalog.md)
- Wire `actionBegin` to **cancel** or **mutate before** an action (`args.cancel = true`, `args.data.field = value`)
- Wire `actionComplete` to **react after** (API call, toast, refresh, toolbar restore)
- Must wire `actionFailure` for error handling
- Use `args.requestType` to identify the action, see the requestType table in the events catalog


### Advanced Tutorials & Real-World Patterns
📄 **Read:** [references/advanced-tutorials.md](references/advanced-tutorials.md)
- Real-time data updates (WebSocket, SignalR)
- Master-detail with filtering
- Complex calculations and running totals
- Advanced filtering with complex predicates
- Custom themes and theme switching
- Performance monitoring techniques
- Unit and integration testing strategies

## Quick Start Example

```typescript
import { Component, OnInit } from '@angular/core';
import { GridComponent } from '@syncfusion/ej2-angular-grids';

interface Employee {
  EmployeeID: number;
  FirstName: string;
  LastName: string;
  Title: string;
  HireDate: Date;
  ReportsTo: number;
  Salary: number;
}

@Component({
  selector: 'app-grid',
  template: `
    <ejs-grid [dataSource]="data" [allowPaging]="true" 
              [pageSettings]="{ pageSize: 12 }"
              [allowSorting]="true" 
              [allowFiltering]="true">
      <e-columns>
        <e-column field="EmployeeID" headerText="ID" width="100"></e-column>
        <e-column field="FirstName" headerText="First Name" width="120"></e-column>
        <e-column field="LastName" headerText="Last Name" width="120"></e-column>
        <e-column field="Title" headerText="Title" width="150"></e-column>
        <e-column field="HireDate" headerText="Hire Date" type="date" 
                  format="yMd" width="130"></e-column>
        <e-column field="Salary" headerText="Salary" type="number" 
                  format="C2" width="120"></e-column>
      </e-columns>
    </ejs-grid>
  `
})
export class GridComponent implements OnInit {
  data: Employee[] = [];

  ngOnInit() {
    this.loadEmployeeData();
  }

  loadEmployeeData() {
    // Load your data here
    this.data = [
      { EmployeeID: 1, FirstName: 'Nancy', LastName: 'Davolio', Title: 'Sales Representative', 
        HireDate: new Date(1992, 4, 1), ReportsTo: 2, Salary: 60000 },
      { EmployeeID: 2, FirstName: 'Andrew', LastName: 'Fuller', Title: 'Vice President Sales', 
        HireDate: new Date(1992, 8, 14), ReportsTo: null, Salary: 97000 },
      // ... more data
    ];
  }
}
```

## Common Patterns

### Pattern 1: Data Grid with Sorting, Filtering, and Paging
Combine sorting, filtering, and paging for a complete data exploration experience:

```typescript
<ejs-grid [dataSource]="data" 
          [allowSorting]="true" 
          [allowFiltering]="true" 
          [allowPaging]="true"
          [pageSettings]="{ pageSize: 20 }">
  <e-columns>
    <e-column field="EmployeeID" headerText="ID" width="100"></e-column>
    <e-column field="FirstName" headerText="First Name" width="120"></e-column>
    <!-- more columns -->
  </e-columns>
</ejs-grid>
```

### Pattern 2: Inline Editing with Validation
Enable inline editing with form validation:

```typescript
<ejs-grid [dataSource]="data" 
          [editSettings]="{ allowEditing: true, allowAdding: true, mode: 'Normal' }"
          [toolbar]="['Add', 'Edit', 'Delete', 'Update', 'Cancel']">
  <e-columns>
    <e-column field="EmployeeID" headerText="ID" [isPrimaryKey]="true" 
              width="100"></e-column>
    <e-column field="FirstName" headerText="First Name" 
              [validationRules]="{ required: true }" width="120"></e-column>
    <!-- more columns -->
  </e-columns>
</ejs-grid>
```

### Pattern 3: Exporting to PDF and Excel
Enable both PDF and Excel exports with toolbar:

```typescript
<ejs-grid [dataSource]="data" 
          [toolbar]="['PdfExport', 'ExcelExport']"
          [allowPdfExport]='true'
          [allowExcelExport]='true'
          (toolbarClick)='toolbarClick($event)'>
  <e-columns>
    <!-- your columns -->
  </e-columns>
</ejs-grid>
```

### Pattern 4: Virtual Scrolling for Large Datasets
Optimize performance with virtual scrolling:

```typescript
<ejs-grid [dataSource]="largeDataset" 
          [enableVirtualization]="true"
          [pageSettings]="{ pageSize: 50 }">
  <e-columns>
    <!-- your columns -->
  </e-columns>
</ejs-grid>
```

## Key Props & Configuration

| Property | Type | Purpose | Common Values |
|----------|------|---------|----------------|
| `dataSource` | Array/DataManager | Grid data | Employee[], RemoteDataBinding |
| `allowSorting` | boolean | Enable sorting | true, false |
| `allowFiltering` | boolean | Enable filtering | true, false |
| `allowPaging` | boolean | Enable pagination | true, false |
| `allowGrouping` | boolean | Enable grouping | true, false |
| `editSettings` | object | Edit configuration | { mode: 'Inline' } |
| `pageSettings` | object | Paging options | { pageSize: 12 } |
| `enableVirtualization` | boolean | Virtual scrolling | true, false |
| `allowExcelExport` | boolean | Excel export | true, false |
| `allowPdfExport` | boolean | PDF export | true, false |
| `toolbar` | array | Toolbar items | ['Add', 'Edit', 'Delete'] |
| `columns` | array | Column definitions | [{ field, headerText }] |
| `height` | string/number | Grid height | '400px', 'auto' |

## Common Use Cases

**Scenario 1: Employee Directory**
Implement a searchable, sortable, filterable employee list with details on demand.  
→ Combine: getting-started + data-binding + columns + selection + hierarchy-grid

**Scenario 2: Data Entry Form**
Build a grid for adding and editing records with validation.  
→ Combine: editing + validation + toolbar + filtering

**Scenario 3: Sales Report Dashboard**
Create a highly customized grid with grouping, aggregates, and PDF export.  
→ Combine: grouping + aggregates + pdf-export + style-and-appearance

**Scenario 4: Real-time Data Monitor**
Display streaming data with virtual scrolling and state persistence.  
→ Combine: scrolling + state-management + data-binding + adaptive

**Scenario 5: Multi-level Organization Chart**
Show hierarchical org structure with detail rows for each level.  
→ Combine: hierarchy-grid + row templates + cell styling
