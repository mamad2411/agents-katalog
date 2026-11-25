---
name: syncfusion-aspnetcore-tree-grid
description: Implements Syncfusion ASP.NET Core TreeGrid for hierarchical data with sorting, filtering, editing, exporting, paging, virtual scrolling, and advanced features. Supports configuration, CRUD, aggregates, templates, state persistence, and performance optimization in ASP.NET Core applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "TreeGrid"
---

# Syncfusion ASP.NET Core TreeGrid

The TreeGrid component visualizes self-referential hierarchical data in a tabular format. It supports child/parent data binding (via `childMapping` or `idMapping`), expand/collapse of child rows, sorting, filtering, editing, paging, export, and virtualization.

## ⚠️ Security & Trust Boundary
 
- The TreeGrid skill does not perform any remote data access.
- All external API interaction is handled by a separate DataManager skill outside this skill’s trust boundary.

## When to Use This Skill

- Rendering hierarchical or parent-child structured data in ASP.NET Core (e.g. project tasks, org charts, bill of materials)
- Implementing CRUD operations on tree-structured data
- Sorting, filtering, or searching across hierarchical records
- Exporting tree data to Excel or PDF
- Handling large datasets with virtual scrolling or infinite scroll

> Refer to [**Properties & Configuration**](#properties--configuration), [**Events & Lifecycle**](#events--lifecycle), and [**Classes & Enums Reference**](#settings-classes--enums-reference) files for complete API lookup.

## Table of Contents
- [Data Structure Rules](#data-structure-rules)
- [Documentation and Navigation Guide](#documentation-and-navigation-guide)
- [Quick Start Example](#quick-start-example)
- [Common Patterns](#common-patterns)

## Data Structure Rules

### Rule 1: childMapping is MANDATORY for Hierarchical Data
**Severity**: 🔴 CRITICAL - Grid will not expand/collapse without this

**Requirement**:

**CSHTML View**:
```cshtml
<!-- ✅ REQUIRED - childMapping matches data property name exactly -->
<ejs-treegrid id="TreeGrid" dataSource="@ViewBag.data" childMapping="Children"
              treeColumnIndex="1" allowPaging="true">
    <e-treegrid-columns>
        <e-treegrid-column field="TaskId" headerText="Task ID" 
                           isPrimaryKey="true" textAlign="Right" width="95"></e-treegrid-column>
        <e-treegrid-column field="TaskName" headerText="Task Name" width="220"></e-treegrid-column>
        <e-treegrid-column field="Duration" headerText="Duration" textAlign="Right" width="100"></e-treegrid-column>
    </e-treegrid-columns>
</ejs-treegrid>

<!-- ❌ WRONG - No childMapping = No expansion possible -->
<ejs-treegrid id="TreeGrid2" dataSource="@ViewBag.data">
    <!-- Missing childMapping & treeColumnIndex - Won't expand! -->
</ejs-treegrid>
```

**Data Format C# Model**:
```csharp
public class TreeGridItem
{
    public int TaskId { get; set; }
    public string TaskName { get; set; }
    public int Duration { get; set; }
    public List<TreeGridItem> Children { get; set; }  // Must match childMapping="Children"
}

// Sample data
var data = new List<TreeGridItem>
{
    new TreeGridItem
    {
        TaskId = 1,
        TaskName = "Planning",
        Duration = 5,
        Children = new List<TreeGridItem>  // ✅ CORRECT - nested Children property
        {
            new TreeGridItem { TaskId = 2, TaskName = "Identify Site", Duration = 2 },
            new TreeGridItem { TaskId = 3, TaskName = "Perform Test",   Duration = 3 }
        }
    }
};
```

**Alternative: Flat Structure with Parent IDs**:
```cshtml
<!-- Use idMapping + parentIdMapping instead of childMapping -->
<ejs-treegrid id="TreeGrid" dataSource="@ViewBag.flatData" 
              idMapping="TaskId" parentIdMapping="ParentId" treeColumnIndex="1">
    ...
</ejs-treegrid>
```

```csharp
var flatData = new List<TreeGridItem>
{
    new TreeGridItem { TaskId = 1, TaskName = "Planning", ParentId = null },
    new TreeGridItem { TaskId = 2, TaskName = "Identify Site", ParentId = 1 },
    new TreeGridItem { TaskId = 3, TaskName = "Perform Test",   ParentId = 1 }
};
```

### Rule 2: Data Type Matching is MANDATORY
**Severity**: 🟠 IMPORTANT - Type mismatches cause rendering/sorting issues

**C# Model - Correct Types**:
```csharp
public class TreeGridItem
{
    public int TaskId { get; set; }              // ✅ int type
    public string TaskName { get; set; }         // ✅ string type
    public DateTime StartDate { get; set; }      // ✅ DateTime for date columns
    public decimal Price { get; set; }           // ✅ decimal for currency
}

var data = new List<TreeGridItem>
{
    new TreeGridItem
    {
        TaskId = 1,                              // int, not string "1"
        TaskName = "Planning",
        StartDate = new DateTime(2024, 3, 15),   // DateTime, not "03/15/2024"
        Price = 1500.50m                         // decimal, not string "1500.50"
    }
};
```

**CSHTML Column Definition - Match Data Types**:
```cshtml
<ejs-treegrid id="TreeGrid" dataSource="@ViewBag.data" childMapping="Children">
    <e-treegrid-columns>
        <!-- field "TaskId" is int, so type="number" -->
        <e-treegrid-column field="TaskId" headerText="Task ID" 
                           type="number" textAlign="Right" width="95"></e-treegrid-column>
        <!-- field "TaskName" is string, type="string" (default) -->
        <e-treegrid-column field="TaskName" headerText="Task Name" width="220"></e-treegrid-column>
        <!-- field "StartDate" is DateTime, so type="date" with format -->
        <e-treegrid-column field="StartDate" headerText="Start Date" 
                           type="date" format="yMd" textAlign="Right" width="115"></e-treegrid-column>
        <!-- field "Price" is decimal, type="number" with currency format -->
        <e-treegrid-column field="Price" headerText="Price" 
                           type="number" format="c2" textAlign="Right" width="100"></e-treegrid-column>
    </e-treegrid-columns>
</ejs-treegrid>
```

**❌ WRONG - Type Mismatch Issues**:
```csharp
// Bad model - mixing string where types should be specific
var badData = new List<TreeGridItem>
{
    new TreeGridItem
    {
        TaskId = "1",                // ❌ String instead of int
        StartDate = "02/03/2024"     // ❌ String instead of DateTime
    }
};
// Result: Sorting fails, formatting doesn't work, expand/collapse issues
```

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- NuGet installation (`Syncfusion.EJ2.AspNet.Core`)
- TagHelper registration in `_ViewImports.cshtml`
- CSS/script CDN setup in `_Layout.cshtml`
- Basic `<ejs-treegrid>` declaration
- Binding local data with `childMapping` / `treeColumnIndex`
- Defining columns with `<e-treegrid-columns>`
- Enabling paging, sorting, and filtering at startup
- Error handling with `actionFailure`

### Data Binding
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Local data with `childMapping` (nested list) and `idMapping`/`parentIdMapping` (flat list)
- Remote data via `DataManager` with OData/WebAPI adaptor
- Ajax/Fetch-based binding
- `expandStateMapping` — control initial expand/collapse state per row
- Handling null or missing parent references

### Columns
📄 **Read:** [references/columns.md](references/columns.md)
- Column `field`, `headerText`, `textAlign`, `width`, `type`, `format`
- `treeColumnIndex` — which column shows expand/collapse arrows
- Number/date formatting (N2, C2, yMd, custom)
- Lock columns, show/hide columns dynamically
- Checkbox column (`showCheckbox`, `autoCheckHierarchy`)
- `valueAccessor` for computed/expression columns
- Column menu (`showColumnMenu`)
- Column reorder, resize, auto-fit
- Column templates, column spanning, headers, complex data binding

### Sorting
📄 **Read:** [references/sorting.md](references/sorting.md)
- Enable with `allowSorting`
- Initial sort via `e-treegrid-sortsettings`
- Multi-column sort (CTRL + click)
- Disable sort per column (`allowSorting: false` on column)
- Sort events (`actionBegin`, `actionComplete`)
- Programmatic sort/clear via `sortColumn` / `clearSorting`

### Filtering
📄 **Read:** [references/filtering.md](references/filtering.md)
- Enable with `allowFiltering`
- Filter types: FilterBar (default), Menu, Excel-like
- Filter hierarchy modes: Parent, Child, Both, None
- Initial filter with predicate
- Filter operators (startswith, contains, equal, greaterthan, etc.)
- Disable filter per column

### Editing
📄 **Read:** [references/editing.md](references/editing.md)
- Enable with `e-treegrid-editSettings` and `isPrimaryKey`
- Edit modes: Cell, Row, Dialog, Batch
- Toolbar with Add/Edit/Delete/Update/Cancel
- `newRowPosition`: Top, Bottom, Above, Below, Child
- Delete confirmation dialog
- Default column values on add
- Disable editing per column
- Validation rules
- Persisting edited data to server

### Paging
📄 **Read:** [references/paging.md](references/paging.md)
- Enable with `allowPaging`
- `e-treegrid-pagesettings`: `pageSize`, `pageSizeMode` (All/Root)
- Page size dropdown, pager template
- Render pager at top via `dataBound` event

### Selection
📄 **Read:** [references/selection.md](references/selection.md)
- Row, Cell, Both selection modes
- Single vs Multiple type (`e-treegrid-selectionsettings`)
- Checkbox selection with `checkboxMode`
- Programmatic selection

### Aggregates
📄 **Read:** [references/aggregates.md](references/aggregates.md)
- Built-in types: Sum, Average, Min, Max, Count, Truecount, Falsecount
- Footer aggregate and child (parent row footer) aggregate
- `showChildSummary` to show child aggregate
- Custom aggregate function
- `footerTemplate` for custom display

### Row Customization
📄 **Read:** [references/row.md](references/row.md)
- `rowDataBound` for conditional styling
- Alternate row styling (`.e-altrow`)
- Row template, detail template
- Row drag-and-drop (`allowRowDragAndDrop`)
- Row height, row spanning

### Cell Customization
📄 **Read:** [references/cell.md](references/cell.md)
- `queryCellInfo` for per-cell customization
- Custom attributes on cells
- Auto text wrap (`allowTextWrap`)
- Clip mode (Clip, Ellipsis, EllipsisWithTooltip)
- Grid lines

### Export (Excel)
📄 **Read:** [references/excel-export.md](references/excel-export.md)
- Excel export (`allowExcelExport`, `excelExport()`)
- Persist collapsed state in export
- Custom aggregates in export
- Headers/footers, cell style customization
- Server-side export options

### PDF Export
📄 **Read:** [references/pdf-export.md](references/pdf-export.md)
- PDF export (`allowPdfExport`, `pdfExport()`)
- PDF export options and configurations
- Page orientation (Portrait, Landscape)
- Custom headers, footers, and styling
- Cell style customization for PDF
- Server-side PDF export

### Print
📄 **Read:** [references/print.md](references/print.md)
- Enable printing with `allowPrinting`
- Print via toolbar button or external button
- Print current page only (`printMode: 'CurrentPage'`)
- Show/hide columns during print
- Handling large datasets
- Page setup configuration

### Clipboard
📄 **Read:** [references/clipboard.md](references/clipboard.md)
- Copy to clipboard with Ctrl+C and Ctrl+Shift+H
- Copy with external buttons
- Copy hierarchy modes (Parent, Child, Both, None)
- AutoFill feature with drag-to-fill
- Paste functionality with Ctrl+V
- Type conversion limitations

### Scrolling
📄 **Read:** [references/scrolling.md](references/scrolling.md)
- Basic scrolling and responsive configurations
- Sticky header, row/column virtualization, and infinite scrolling
- Performance optimization for large datasets

### Adaptive Layout
📄 **Read:** [references/adaptive.md](references/adaptive.md)
- Responsive UI with `enableAdaptiveUI` for mobile and tablet devices
- Adaptive dialog mode for filtering and editing on small screens
- Expand/collapse behavior optimization for touch interaction
- Column chooser adaptation to mobile dialogs
- Vertical row rendering mode for enhanced mobile readability
- Best practices for responsive TreeGrid design

### Frozen Rows and Columns
📄 **Read:** [references/frozen.md](references/frozen.md)
- Freeze rows and columns using `frozenRows`, `frozenColumns`, or `isFrozen` property
- Freeze direction control with Left/Right positioning
- Limitations and compatibility considerations with other features

### Styling and Appearance
📄 **Read:** [references/styling-and-appearance.md](references/styling-and-appearance.md)
- Customize Tree Grid styling with CSS classes for all elements
- CSS override examples for headers, rows, cells, selection, and summary
- Custom theme options using Syncfusion Theme Studio

### Immutable Mode
📄 **Read:** [references/immutable.md](references/immutable.md)
- Enable with `enableImmutableMode="true"`
- Performance optimization for large datasets
- Primary key requirement for comparison
- Selective re-render of modified rows
- Performance benefits for batch operations
- Limitations and workarounds

### Toolbar
📄 **Read:** [references/toolbar.md](references/toolbar.md)
- Built-in toolbar items (Add, Edit, Delete, Update, Cancel, Search, ExcelExport, PdfExport, etc.)
- Custom toolbar items with text, icons, tooltips, and alignment
- Toolbar click handler with event arguments
- Built-in item ID patterns and identification
- Disabling toolbar items dynamically based on row selection
- Best practices for toolbar design and layout
- Edit mode integration with toolbar buttons

### Context Menu
📄 **Read:** [references/context-menu.md](references/context-menu.md)
- Default context menu items for data manipulation and column operations
- Custom context menu items with hierarchy-aware functionality
- Contextual visibility using target selectors (.e-content, .e-headercell)
- Context menu click handler with row and column information
- Enable/disable items dynamically based on row state (parent/child)
- Hierarchy-aware expand/collapse menus for TreeGrid
- Advanced scenarios: parent-only operations, conditional menu items
- Best practices for TreeGrid-specific context menu design

### Searching
📄 **Read:** [references/searching.md](references/searching.md)
- Enable full-text search across TreeGrid hierarchical data
- Add search toolbar item for real-time filtering as user types
- Configure search field scope (all columns or specific column subset)
- Search with operators (contains, startsWith, endsWith, equal, notEqual)
- Programmatic search triggering from external input controls
- Search in hierarchy with automatic parent row expansion on child matches
- Clear search and reset to show all rows
- Handle search events (actionBegin, actionComplete) for custom logic
- Best practices for searching large hierarchical datasets

### Loading Animation
📄 **Read:** [references/loading-animation.md](references/loading-animation.md)
- Loading indicator types: Spinner (default) and Shimmer animations
- When loading animation displays (initial render, sorting, filtering, paging, searching)
- Remote data binding with loading animation via DataManager
- Programmatic control of loading indicator (show/hide)
- Customizing loading behavior with action events
- Best practices for UX with loading states
- Mobile and slow network optimization

### Globalization & Localization
📄 **Read:** [references/global-local.md](references/global-local.md)
- Culture-specific number and date formatting via `locale` property
- Localization of UI strings (toolbar, dialogs, pager, filter, expand/collapse text)
- Right-to-left (RTL) layout support for Arabic, Hebrew, and other RTL languages
- CLDR data loading and culture configuration
- Format codes (C2, yMd, N2) for currency, date, and number columns
- Multi-locale support with dynamic language switching
- Best practices for global applications

### State Management
📄 **Read:** [references/state-management.md](references/state-management.md)
- Persist TreeGrid state across sessions with `enablePersistence`
- Save and restore sorting, filtering, paging, and column preferences
- Preserve expand/collapse state of parent rows on page reload
- LocalStorage-based automatic persistence and manual state retrieval
- Reset TreeGrid state to defaults programmatically
- Custom server-side state persistence for sensitive data
- Best practices for state management in hierarchical data

### Accessibility
📄 **Read:** [references/accessibility.md](references/accessibility.md)
- WCAG 2.1 compliance
- Keyboard navigation
- ARIA attributes
- Screen reader support

### Properties & Configuration
📄 **Read:** [references/properties-configuration.md](references/properties-configuration.md)
- Lookup 145+ TreeGrid properties organized by concern
- Data configuration (dataSource, childMapping, idMapping, parentIdMapping, expandStateMapping)
- UI layout (height, width, rowHeight, treeColumnIndex)
- Grid appearance (gridLines, enableAltRow, enableRtl, enableHover, clipMode)
- Feature toggles table (Paging, Sorting, Filtering, Editing, Selection, etc.)
- Performance tuning (virtualization, infinite scroll, immutable mode, persistence)
- Event callbacks and handlers
- Advanced configuration objects (EditSettings, PageSettings, FilterSettings, SelectionSettings, etc.)

### Events & Lifecycle
📄 **Read:** [references/events-methods.md](references/events-methods.md)
- Lifecycle events (created, load, dataBound, beforeDataBound, dataSourceChanged)
- Action events (actionBegin, actionComplete, actionFailure)
- Expand/collapse events (expanding, expanded, collapsing, collapsed)
- Edit events (beginEdit, cellEdit, cellSave, cellSaved, batchAdd, batchDelete, beforeBatchSave)
- Selection events (rowSelected, rowSelecting, rowDeselected, checkboxChange)
- Drag & drop events (rowDragStart, rowDrop, columnDragStart, columnDrop)
- Custom rendering events (queryCellInfo, rowDataBound, detailDataBound)
- Export events (beforeExcelExport, excelExportComplete, beforePdfExport, pdfQueryCellInfo)
- Complete event signatures and examples for each category

### Settings Classes & Enums Reference
📄 **Read:** [references/classes-enums-reference.md](references/classes-enums-reference.md)
- Enums: CopyHierarchyType, EditMode, FilterHierarchyMode, FilterType, PageSizeMode, RowPosition, WrapMode
- Settings classes: EditSettings, PageSettings, SortSettings, FilterSettings, SelectionSettings, RowDropSettings, InfiniteScrollSettings
- Column configuration: TreeGridColumn, StackedHeaderCell classes
- Builder pattern for fluent API and tag helper approach
- Complete property definitions for each settings class

## Quick Start Example

**Minimal TreeGrid with local data, columns, sorting, filtering, and paging:**

**`_ViewImports.cshtml`**
```cshtml
@addTagHelper *, Syncfusion.EJ2
```

**`_Layout.cshtml`** (inside `<head>`)
```cshtml
<!-- Syncfusion ASP.NET Core controls styles -->
<link rel="stylesheet" href="~/ej2/ej2version/fluent2.css" />
<!-- Syncfusion ASP.NET Core controls scripts -->
<script src="~/ej2/ej2version/dist/ej2.min.js"></script>
```

**`_Layout.cshtml`** (end of `<body>`)
```cshtml
<ejs-scripts></ejs-scripts>
```

**`Index.cshtml`**
```cshtml
@{
    var data = TreeGridItems.GetTreeData();
}

<ejs-treegrid id="TreeGrid" dataSource="@data" childMapping="Children"
              treeColumnIndex="1" allowSorting="true" allowFiltering="true" allowPaging="true">
    <e-treegrid-pagesettings pageSize="5"></e-treegrid-pagesettings>
    <e-treegrid-columns>
        <e-treegrid-column field="TaskId" headerText="Task ID" isPrimaryKey="true"
                           textAlign="Right" width="95"></e-treegrid-column>
        <e-treegrid-column field="TaskName" headerText="Task Name" width="220"></e-treegrid-column>
        <e-treegrid-column field="StartDate" headerText="Start Date"
                           textAlign="Right" format="yMd" type="date" width="115"></e-treegrid-column>
        <e-treegrid-column field="Duration" headerText="Duration"
                           textAlign="Right" width="100"></e-treegrid-column>
    </e-treegrid-columns>
</ejs-treegrid>
```

**`Index.cshtml.cs` (or Controller)**
```csharp
public class TreeGridItems
{
    public int TaskId { get; set; }
    public string TaskName { get; set; }
    public DateTime StartDate { get; set; }
    public int Duration { get; set; }
    public List<TreeGridItems> Children { get; set; }

    public static List<TreeGridItems> GetTreeData()
    {
        return new List<TreeGridItems>
        {
            new TreeGridItems
            {
                TaskId = 1, TaskName = "Planning",
                StartDate = new DateTime(2021, 6, 7), Duration = 5,
                Children = new List<TreeGridItems>
                {
                    new TreeGridItems { TaskId = 2, TaskName = "Plan timeline", StartDate = new DateTime(2021, 6, 7), Duration = 5 },
                    new TreeGridItems { TaskId = 3, TaskName = "Plan budget",   StartDate = new DateTime(2021, 6, 7), Duration = 5 }
                }
            }
        };
    }
}
```

## Common Patterns

### When to use `childMapping` vs `idMapping`
- **`childMapping`**: Data is nested (each parent has a `Children` list) → bind `childMapping="Children"`
- **`idMapping` + `parentIdMapping`**: Data is flat with parent ID references → bind `idMapping="TaskId" parentIdMapping="ParentId"`

### Enable Editing with Toolbar
```cshtml
<ejs-treegrid id="TreeGrid" dataSource="@data" childMapping="Children"
              treeColumnIndex="1" toolbar="@(new List<string>() {"Add","Edit","Delete","Update","Cancel"})">
    <e-treegrid-editsettings allowAdding="true" allowEditing="true"
                             allowDeleting="true" mode="Row"></e-treegrid-editsettings>
    <e-treegrid-columns>
        <e-treegrid-column field="TaskId" headerText="Task ID"
                           isPrimaryKey="true" width="90"></e-treegrid-column>
        <e-treegrid-column field="TaskName" headerText="Task Name" width="220"></e-treegrid-column>
    </e-treegrid-columns>
</ejs-treegrid>
```

> Always set `isPrimaryKey="true"` on one column — editing and delete operations require it.

### Key Error Avoidance
- Do NOT enable paging and virtualization simultaneously
- Do NOT set `isFrozen` and `frozenColumns` at the same time
- `showCheckbox` column must be defined only on the tree column
- `textAlign="Right"` is not applicable for the tree column
- Do NOT enable `idMapping` and `childMapping` simultaneously
