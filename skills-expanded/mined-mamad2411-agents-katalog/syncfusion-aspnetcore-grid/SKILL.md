---
name: syncfusion-aspnetcore-grid
description: Implements Syncfusion ASP.NET Core Grid component for feature-rich data tables and grids. Use this when working with data display, sorting, filtering, grouping, aggregates, editing, or exporting. This skill covers grid configuration, CRUD operations, virtual scrolling or infinite scrolling, hierarchy grids, state persistence, and advanced data management features for data-intensive applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Grid"
---

# Syncfusion ASP.NET Core Grid

The Syncfusion ASP.NET Core Grid is a comprehensive, feature-rich component for displaying and manipulating tabular data. It provides extensive functionality for data binding, paging, sorting, filtering, grouping, editing, exporting, scrolling modes, row/column customization, and advanced state management to handle datasets of any size and complexity efficiently.

## ⚠️ Security & Trust Boundary
 
- The Grid skill does not perform any remote data access.
- All external API interaction is handled by a separate DataManager skill outside this skill’s trust boundary.

## Table of Contents
- [When to Use This Skill](#when-to-use-this-skill)
- [Component Overview](#component-overview)
- [Feature/Skill Navigation Guide](#featureskill-navigation-guide)
- [Quick Start Example](#quick-start-example)

## When to Use This Skill

Use the Syncfusion ASP.NET Core Grid when you need to:

- **Display tabular data** with rows and columns in ASP.NET Core applications
- **Handle large datasets** efficiently with paging, virtual scrolling, or infinite scrolling
- **Enable sorting, filtering, and searching** for single or multiple columns
- **Edit data inline** with multiple edit modes (Inline, Batch, Dialog)
- **Export data** to Excel or PDF formats with customization
- **Group and aggregate data** with summaries and calculations
- **Customize rows and cells** with templates and styling
- **Manage complex column configurations** (frozen columns, spanning, reordering, resizing)
- **Optimize performance** when rendering thousands of records
- **Persist grid state** for user preferences and configuration
- **Provide responsive data views** for different screen sizes

## Component Overview

The Grid component provides:

- **Data Binding**: Support for local collections, remote data sources, and DataManager integration
- **Paging**: Server-side or client-side pagination with customizable page size and navigation
- **Sorting**: Single and multi-column sorting
- **Filtering**: Multiple filter modes (FilterBar, FilterMenu, Excel-like filter)
- **Searching**: Global search across columns
- **Grouping**: Group data by columns with aggregates
- **Selection**: Row, cell, and column selection with checkbox support
- **Editing**: Inline, Batch, and Dialog modes with validation and templates
- **Aggregates**: Sum, Average, Count, Min, Max with footer, group, and caption display
- **Exporting**: Excel and PDF export with templates and customization
- **Scrolling**: Standard, Virtual, and Infinite scrolling modes
- **Row Customization**: Templates, detail views, drag-drop, pinning, spanning
- **Column Customization**: Templates, resizing, reordering, freezing, spanning
- **Performance**: Optimized rendering for large datasets
- **Responsive Design**: Adaptive layouts for different screen sizes

## Mandatory Rules for Server-Side Grid Configuration

**CRITICAL**: Follow these rules when configuring ASP.NET Core Grid for optimal performance and correctness:

### Rule 1: DataManager Adaptor Configuration
Adaptors determine how the Grid communicates with your server backend. Each request type (read, create, update, delete) has specific URL mapping requirements.

| Adaptor | Backend | Use Case |
|---------|---------|----------|
| `UrlAdaptor` | Generic HTTP endpoint | Simple REST APIs with standard conventions |
| `ODataAdaptor` | OData v4 service | Microsoft ODATA, SAP services |
| `ODataV4Adaptor` | OData v4 (newer) | Modern ODATA endpoints |
| `WebApiAdaptor` | ASP.NET Web API | ASP.NET Core API controllers |
| `GridAdaptor` | Syncfusion GridAdaptor | Built-in Syncfusion backend conventions |

---

📄 **Full Adaptor Reference:** [references/adaptors.md](references/adaptors.md)

---

### Rule 2: EnablePersistence for State Management
To persist grid state (sorting, filtering, grouping, paging, column order), enable persistence:

```csharp
<ejs-grid id="Grid" allowPaging="true" enablePersistence="true">
    <!-- Grid configuration -->
</ejs-grid>
```

⚠️ **Rule**: `enablePersistence="true"` is required when using state management in grid.

### Rule 3: Primary Key Configuration for Editing
The `isPrimaryKey="true"` attribute is required on the key column — editing silently fails without it.

```csharp
<e-grid-column field="OrderID" headerText="Order ID" isPrimaryKey="true"></e-grid-column>
```

## Feature/Skill Navigation Guide

### Getting Started & Setup
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- NuGet package installation
- Tag helper registration
- CSS and script setup
- Basic grid initialization
- Data binding fundamentals

### Data Binding
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Local data binding (IEnumerable, List, DataTable)
- Remote data with DataManager (OData, WebAPI)
- Loading indicators
- Dynamic data refresh

### Column Configuration
📄 **Read:** [references/columns.md](references/columns.md)
- Column definition and properties
- Column types (string, number, date, boolean, checkbox)
- Column width and formatting
- Column templates and custom rendering
- Column features (spanning, reordering, resizing)
- Foreign key columns
- Stacked headers

### Data Aggregation
📄 **Read:** [references/aggregates.md](references/aggregates.md)
- Footer aggregates (Sum, Avg, Count, Min, Max)
- Group footer aggregates
- Group caption aggregates
- Custom aggregate functions
- Reactive aggregate updates

### Navigation & Pagination
📄 **Read:** [references/paging.md](references/paging.md)
- Enable and configure paging
- Page size configuration
- Navigation and page change
- External paging

### Sorting Data
📄 **Read:** [references/sorting.md](references/sorting.md)
- Enable sorting (single and multi-column)
- Initial sort configuration
- Custom sort comparers
- Sort events

### Filtering
**Start here:** 📄 Read [references/filter-setup.md](references/filter-setup.md) — Enable filtering, choose filter type (FilterBar, Menu, Excel, CheckBox)

**Choose your type:**
- 📄 Read [references/filter-types.md](references/filter-types.md) — All filter types: FilterBar (inline text), Menu (operators), Excel (checkboxes)
- 📄 Read [references/filter-operators.md](references/filter-operators.md) — All filter operators, syntax, wildcards, AND/OR logic

### Searching
📄 **Read:** [references/searching.md](references/searching.md)
- Grid search functionality
- Global search across columns
- Search configuration

### Grouping Data
📄 **Read:** [references/grouping.md](references/grouping.md)
- Enable grouping by columns
- Group by multiple columns
- Caption templates
- Group footer aggregates
- Lazy-load grouping

### Selection
📄 **Read:** [references/selection.md](references/selection.md)
- Row, cell, and column selection modes
- Checkbox selection
- Multiple selection handling
- Selection events

### Editing
📄 **Read:** [references/editing.md](references/editing.md)
- Enable editing (allowEditing, allowAdding, allowDeleting)
- Edit modes: Inline, Batch, Dialog
- Edit triggers (double-click, toolbar)
- Custom edit templates
- Validation rules
- Server-side data persistence

### Row Features
📄 **Read:** [references/row.md](references/row.md)
- Row templates
- Detail templates (expand/collapse)
- Row drag and drop
- Row pinning
- Row spanning

### Toolbar
📄 **Read:** [references/tool-bar.md](references/tool-bar.md)
- Built-in toolbar items
- Custom toolbar buttons
- Toolbar events

### Exporting to Excel
📄 **Read:** [references/excel-export.md](references/excel-export.md)
- Excel export setup
- Export options and customization
- Export with templates
- Server-side export

### Exporting to PDF
📄 **Read:** [references/pdf-export.md](references/pdf-export.md)
- PDF export setup
- Headers and footers
- Export options and customization
- Export with templates
- Server-side export

### Printing
📄 **Read:** [references/print.md](references/print.md)
- Print grid
- Print templates
- Print customization

### Styling & Appearance
📄 **Read:** [references/style-and-appearance.md](references/style-and-appearance.md)
- CSS customization
- Themes and dark mode
- Inline styling and classes
- Custom color schemes

### Freezing & Pinning
📄 **Read:** [references/frozen.md](references/frozen.md)
- Freeze columns
- Freeze rows
- Row pinning
- Frozen column behavior

### Scrolling Modes
📄 **Read:** [references/scrolling.md](references/scrolling.md)
- Standard scrolling
- Virtual scrolling (performance optimization)
- Infinite scrolling
- Scrollbar and height configuration

### Hierarchy & Nested Data
📄 **Read:** [references/hierarchy-grid.md](references/hierarchy-grid.md)
- Parent-child data structures
- Child grid configuration
- Expand and collapse behavior
- Detail row templates
- Lazy loading child data

### Context Menu
📄 **Read:** [references/context-menu.md](references/context-menu.md)
- Built-in context menu items
- Custom context menus
- Context menu events

### Cell Features
📄 **Read:** [references/cell.md](references/cell.md)
- Cell templates
- Cell customization via events
- Custom cell attributes
- Cell tooltips

### Clipboard Operations
📄 **Read:** [references/clipboard.md](references/clipboard.md)
- Copy and paste functionality
- Copy with headers
- Custom separators

### Configuration Management
📄 **Read:** [references/global-local.md](references/global-local.md)
- Global grid settings
- Local column configuration

### State Management
📄 **Read:** [references/state-management.md](references/state-management.md)
- Persist grid state
- Save and restore state
- Local storage

⚠️ **Rule**: `enablePersistence="true"` must be enabled when using state management in grid.

### Data Validation
📄 **Read:** [references/validation.md](references/validation.md)
- Built-in validation rules
- Custom validation logic
- Dynamic validation
- Server-side validation
- Error handling

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
📄 **Read:** [references/adaptive.md](references/adaptive.md)
- Enable adaptive UI for mobile
- Full-screen dialogs for filtering/editing
- Mobile-optimized layouts

📄 **Read:** [references/responsive-design.md](references/responsive-design.md)
- Responsive grid layouts
- Column visibility on mobile
- Touch-friendly interactions
- Mobile breakpoints

### API Reference & Properties
📄 **Read:** [references/properties-configuration.md](references/properties-configuration.md)
- All configurable properties organized by category
- Quick reference table for quick lookup
- When to use each property
- Configuration requirements

### Programmatic Control (Methods)
📄 **Read:** [references/programmatic-api.md](references/programmatic-api.md)
- Grid methods by category (data, row, column, sort, filter, group, page, edit, export)
- Method signatures and parameters
- Return values and usage patterns
- Server-side method invocation

### Event Communication (Events)
📄 **Read:** [references/events-catalog.md](references/events-catalog.md)
- All Grid events with timing and use cases
- ActionBegin event for canceling or mutating actions
- ActionComplete event for reactive operations
- ActionFailure event for error handling
- Using `args.requestType` to identify the action

### Data Connectivity & Adaptors
📄 **Read:** [references/adaptors.md](references/adaptors.md)
- 5+ adaptor types for backend integration
- UrlAdaptor, ODataV4Adaptor, WebApiAdaptor
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
- Performance benchmarking

### Accessibility & Compliance
📄 **Read:** [references/accessibility.md](references/accessibility.md)
- WCAG 2.2 and Section 508 compliance
- WAI-ARIA implementation and screen readers
- Keyboard navigation (Tab, arrows, Enter, Escape)
- Color contrast and focus management
- Accessibility testing tools
- Semantic HTML practices

## Quick Start Example

```cshtml
@* ~/Pages/_ViewImports.cshtml *@
@addTagHelper *, Syncfusion.EJ2
```

```cshtml
@* ~/Pages/Index.cshtml *@
<ejs-grid id="Grid" dataSource="@ViewBag.DataSource" allowPaging="true" allowSorting="true" allowFiltering="true">
    <e-grid-pagesettings pageSize="10"></e-grid-pagesettings>
    <e-grid-columns>
        <e-grid-column field="OrderID" headerText="Order ID" isPrimaryKey="true" width="120" textAlign="Right"></e-grid-column>
        <e-grid-column field="CustomerID" headerText="Customer ID" width="150"></e-grid-column>
        <e-grid-column field="ShipCity" headerText="Ship City" width="150"></e-grid-column>
        <e-grid-column field="OrderDate" headerText="Order Date" format="yMd" width="150"></e-grid-column>
        <e-grid-column field="Freight" headerText="Freight" format="C2" textAlign="Right" width="120"></e-grid-column>
    </e-grid-columns>
</ejs-grid>
```

```csharp
// Controller / PageModel
public IActionResult Index()
{
    ViewBag.DataSource = OrdersDetails.GetAllRecords();
    return View();
}
```
