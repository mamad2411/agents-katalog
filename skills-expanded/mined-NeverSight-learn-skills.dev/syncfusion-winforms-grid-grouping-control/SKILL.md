---
name: syncfusion-winforms-grid-grouping-control
description: Implements Syncfusion Windows Forms GridGroupingControl for advanced data management with grouping, sorting, filtering, and hierarchical display. Use this when working with multi-level grouping, master-detail grids, nested table relationships, or data summaries with aggregates. The skill covers group-by operations, Excel-like filtering, dynamic record filters, hierarchical data structures, and enterprise-level grid capabilities.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Grid Grouping Controls

Comprehensive guide for implementing Syncfusion® Windows Forms GridGroupingControl - an enterprise-level grid component with built-in support for hierarchical grouping, filtering, multi-column sorting, summaries, and complex data relationships.

## When to Use This Skill

Use this skill when you need to:

- **Implement GridGroupingControl** in Windows Forms applications
- **Display hierarchical or grouped data** with automatic grouping by one or more columns
- **Create master-detail relationships** with nested tables and child relations
- **Apply advanced filtering** (Excel-like, dynamic, or programmatic filters)
- **Add data summaries** (group summaries, caption summaries, table summaries)
- **Sort data** by single or multiple columns with custom sorting logic
- **Handle large datasets** with virtualization and performance optimization
- **Export grouped data** to Excel, PDF, CSV, HTML, or Word
- **Customize grid appearance** with conditional formatting and styling
- **Bind to various data sources** (DataTable, XML, collections, dynamic objects)

This skill is essential for applications requiring sophisticated data grouping, drill-down capabilities, and comprehensive data management features.

## Component Overview

**GridGroupingControl** is a powerful data grid component that extends standard grid functionality with:

- **Hierarchical Grouping:** Organize data into nested groups based on field values
- **Group Drop Area:** Interactive area for drag-and-drop grouping by column headers
- **Multi-Level Sorting:** Sort by multiple columns with custom sort logic
- **Advanced Filtering:** Excel-like filters, dynamic filters, and programmatic record filters
- **Summaries:** Column summaries, group summaries, and caption summaries with aggregates
- **Master-Detail Support:** Display nested tables with parent-child relationships
- **Data Virtualization:** Handle millions of records with instant scrolling
- **Rich Editing:** In-place editing with validation and custom editors
- **Flexible Styling:** Conditional formatting, themes, and cell-level customization

The control is designed for business applications requiring enterprise-level data management capabilities.

## Documentation and Navigation Guide

### Getting Started

📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and assembly deployment
- Creating GridGroupingControl through Designer and Code
- Basic data source binding
- Populating data and first grid example
- Essential properties and initial configuration

### Data Binding and Sources

📄 **Read:** [references/data-binding.md](references/data-binding.md)
- ADO.NET data binding (DataTable, DataSet, DataView)
- XML data binding with ReadXml/WriteXml
- Custom collections (IList, IBindingList, ITypedList)
- Strongly typed collections and generic collections
- Dynamic object binding for .NET 4.0+
- Unbound mode with custom columns
- Collection interfaces and change notifications

**When to read:** Setting up data sources, binding to databases, working with custom objects, or implementing unbound scenarios.

### Grouping Features

📄 **Read:** [references/grouping.md](references/grouping.md)
- Adding data groups (Designer and programmatic)
- GroupDropArea configuration and customization
- Multi-column grouping and nested groups
- Custom grouping with IComparer and IGroupByColumnCategorizer
- GroupBy options (headers, footers, preview rows)
- GroupCaptionSection and caption text tokens
- Working with groups (expand/collapse, iterate, access)
- Grouping events and customization

**When to read:** Implementing grouping functionality, customizing group appearance, working with nested groups, or handling group-related events.

### Sorting Operations

📄 **Read:** [references/sorting.md](references/sorting.md)
- Programmatic sorting with SortedColumns collection
- Multi-column sorting with precedence
- Sort icon placement and customization
- Removing and clearing sorting
- Sorting grouped columns
- Sort by summary values
- Sort by display member (foreign key relations)
- Custom sorting with IComparer
- Sorting events (Changing/Changed)

**When to read:** Implementing sorting features, customizing sort behavior, sorting by computed values, or handling sort events.

### Filtering and Search

📄 **Read:** [references/filtering.md](references/filtering.md)
- Setting up filter bar for user filtering
- Record filters (programmatic filtering)
- Filter by expression with operators
- Dynamic filter with GridDynamicFilter
- Excel-like filter (Optimized and Office2007)
- Filter by color, number, date, and null values
- Filter by display member vs value member
- Stacked header filtering
- Getting filtered records and filter strings
- Filtering events

**When to read:** Implementing filtering capabilities, Excel-like filtering UI, programmatic data filtering, or filter customization.

### Summaries and Aggregates

📄 **Read:** [references/summaries.md](references/summaries.md)
- Summary types (Column, Group, Table, Caption)
- Adding summaries with SummaryDescriptor
- Built-in aggregate functions (Sum, Average, Count, Min, Max)
- Custom summaries with ISummaryAggregate
- Sort by summary values
- Summary appearance and formatting
- Summary in group captions
- Summary events

**When to read:** Adding aggregate calculations, displaying group totals, implementing custom aggregates, or showing summaries in captions.

### Relations and Hierarchy

📄 **Read:** [references/relations-and-hierarchy.md](references/relations-and-hierarchy.md)
- Master-detail relationships setup
- Nested tables configuration
- Relations descriptor and child table descriptor
- Hierarchy display and navigation
- Expand/collapse nested tables
- Working with child tables programmatically
- Foreign key reference relations

**When to read:** Implementing master-detail grids, displaying nested data, configuring parent-child relationships, or working with hierarchical data.

### Editing Capabilities

📄 **Read:** [references/editing.md](references/editing.md)
- Enabling/disabling editing
- Cell editing modes and activation
- Current cell behavior
- Data validation
- Editing events (StartEditing, EditingComplete)
- Custom editors and cell types
- AddNew record functionality

**When to read:** Configuring edit behavior, implementing validation, customizing editors, or handling edit events.

### Selection Features

📄 **Read:** [references/selections.md](references/selections.md)
- Selection modes (None, One, Multiple, MultiSimple, MultiExtended)
- Record selection vs cell selection
- Programmatic selection
- Getting selected records
- Selection events
- Selection appearance

**When to read:** Implementing selection functionality, programmatic record selection, or customizing selection behavior.

### Column Management

📄 **Read:** [references/column-management.md](references/column-management.md)
- Adding/removing columns programmatically
- Column properties (Width, HeaderText, MappingName)
- Column width and auto-sizing
- Column visibility and VisibleColumns collection
- Column reordering and drag-drop
- Frozen columns
- Unbound columns

**When to read:** Managing column visibility, configuring column properties, implementing frozen columns, or adding unbound columns.

### Appearance and Styling

📄 **Read:** [references/appearance-and-formatting.md](references/appearance-and-formatting.md)
- Cell styles and GridStyleInfo
- Conditional formatting
- Themes and visual styles
- Row and column appearance
- QueryCellStyleInfo event for dynamic styling
- Appearance properties for different cell types
- BackColor, ForeColor, Font customization

**When to read:** Customizing grid appearance, applying conditional formatting, implementing themes, or styling specific cells.

### Cell Types and Customization

📄 **Read:** [references/cell-types.md](references/cell-types.md)
- Built-in cell types (TextBox, ComboBox, CheckBox, Image)
- ComboBox cells with DataSource
- CheckBox cells for boolean data
- Image cells for displaying graphics
- Custom cell types and renderers
- Cell type configuration

**When to read:** Implementing dropdown lists, checkboxes, image cells, or creating custom cell renderers.

### Grid Layout

📄 **Read:** [references/grid-layout.md](references/grid-layout.md)
- Row and column sizing (auto-size, fit)
- Stacked headers for grouped column headers
- Covered ranges (merged cells)
- Grid borders and lines
- Layout customization and spacing

**When to read:** Configuring row heights, implementing stacked headers, merging cells, or customizing grid layout.

### Navigation and Scrolling

📄 **Read:** [references/navigation-and-scrolling.md](references/navigation-and-scrolling.md)
- Navigation bar configuration
- Scrolling options and behavior
- Keyboard navigation
- Current cell navigation
- ScrollControlIntoView methods

**When to read:** Configuring navigation behavior, customizing keyboard shortcuts, or implementing programmatic navigation.

### Clipboard Operations

📄 **Read:** [references/clipboard-operations.md](references/clipboard-operations.md)
- Copy/paste operations
- Clipboard formats (Text, CSV, HTML)
- Cut operations
- Clipboard customization
- CopyPaste events

**When to read:** Implementing copy/paste functionality, customizing clipboard formats, or handling clipboard events.

### Exporting Data

📄 **Read:** [references/exporting.md](references/exporting.md)
- Excel export with ExcelExportingOptions
- PDF export with PdfExportingOptions
- CSV export
- HTML export
- Word export
- Export options and customization

**When to read:** Implementing data export features, customizing export formats, or configuring export options.

### Printing

📄 **Read:** [references/printing.md](references/printing.md)
- Print configuration and setup
- Print preview
- Print settings (margins, orientation, scaling)
- Custom print layouts
- PrintDocument integration

**When to read:** Implementing print functionality, customizing print layouts, or configuring print settings.

### Performance Optimization

📄 **Read:** [references/performance.md](references/performance.md)
- Virtualization for large datasets
- Handling millions of records
- Performance optimization tips
- Best practices for data binding
- Memory management

**When to read:** Optimizing grid performance, handling large datasets, or troubleshooting performance issues.

### Events Reference

📄 **Read:** [references/events.md](references/events.md)
- Data-related events (QueryValue, SaveValue)
- UI interaction events (CellClick, CellDoubleClick)
- Grouping events (GroupExpanding, GroupExpanded)
- Sorting events (SortedColumns.Changing/Changed)
- Filtering events (RecordFilters.Changing/Changed)
- Editing events (CurrentCellStartEditing, EditingComplete)
- Complete event reference with examples

**When to read:** Handling grid events, implementing event-driven logic, or responding to user interactions.

### Advanced Features

📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Expression fields for calculated columns
- Data validation rules
- Find and replace functionality
- Serialization (Binary, SOAP, XML)
- Touch support for tablets
- Zooming capabilities

**When to read:** Implementing calculated columns, validation rules, find/replace, serialization, or touch support.

### Troubleshooting

📄 **Read:** [references/troubleshooting.md](references/troubleshooting.md)
- Common issues and solutions
- Performance troubleshooting
- Data binding issues
- UI rendering problems
- Best practices and guidelines

**When to read:** Debugging issues, resolving errors, or optimizing implementation.

## Quick Start Example

Here's a minimal example to get started with GridGroupingControl:

```csharp
using Syncfusion.Windows.Forms.Grid.Grouping;
using System.Data;

// Create the control
GridGroupingControl gridGroupingControl1 = new GridGroupingControl();
gridGroupingControl1.Dock = DockStyle.Fill;
this.Controls.Add(gridGroupingControl1);

// Create sample data
DataTable dataTable = new DataTable("Employees");
dataTable.Columns.Add("ID", typeof(int));
dataTable.Columns.Add("Name", typeof(string));
dataTable.Columns.Add("Department", typeof(string));
dataTable.Columns.Add("Salary", typeof(decimal));

dataTable.Rows.Add(1, "John Smith", "Sales", 50000);
dataTable.Rows.Add(2, "Sarah Jones", "Marketing", 55000);
dataTable.Rows.Add(3, "Mike Wilson", "Sales", 52000);
dataTable.Rows.Add(4, "Lisa Brown", "Marketing", 58000);
dataTable.Rows.Add(5, "Tom Davis", "IT", 65000);

// Bind data source
gridGroupingControl1.DataSource = dataTable;

// Enable grouping with GroupDropArea
gridGroupingControl1.ShowGroupDropArea = true;

// Add a group by Department
gridGroupingControl1.TableDescriptor.GroupedColumns.Add("Department");

// Add a summary to show total salary per group
GridSummaryColumnDescriptor summaryColumn = new GridSummaryColumnDescriptor();
summaryColumn.MappingName = "Salary";
summaryColumn.SummaryType = SummaryType.DoubleAggregate;
summaryColumn.Format = "{Sum:C}";
summaryColumn.Name = "TotalSalary";

GridSummaryRowDescriptor summaryRow = new GridSummaryRowDescriptor();
summaryRow.SummaryColumns.Add(summaryColumn);
gridGroupingControl1.TableDescriptor.SummaryRows.Add(summaryRow);

// Enable sorting
gridGroupingControl1.TableOptions.AllowSortColumns = true;
```

This creates a grouped grid with department grouping and salary summaries.

## Common Patterns

### Master-Detail Pattern with Nested Tables

```csharp
// Assuming Orders and OrderDetails are related tables in a DataSet
DataSet dataSet = GetOrdersDataSet(); // Your data source

// Bind to parent table
gridGroupingControl1.DataSource = dataSet;
gridGroupingControl1.DataMember = "Orders";

// Nested tables are automatically detected from DataSet relations
// Customize child table appearance
GridRelationDescriptor relation = gridGroupingControl1.TableDescriptor.Relations[0];
relation.ChildTableDescriptor.Appearance.AlternateRecordFieldCell.BackColor = Color.LightBlue;
```

### Dynamic Filtering Pattern

```csharp
using Syncfusion.GridHelperClasses;

// Wire dynamic filter
GridDynamicFilter dynamicFilter = new GridDynamicFilter();
dynamicFilter.WireGrid(gridGroupingControl1);

// Enable filter bar
gridGroupingControl1.TopLevelGroupOptions.ShowFilterBar = true;

// Enable filtering for specific columns
foreach (GridColumnDescriptor column in gridGroupingControl1.TableDescriptor.Columns)
{
    column.AllowFilter = true;
}
```

### Excel-Like Filtering Pattern

```csharp
using Syncfusion.GridHelperClasses;

// Create and wire Excel filter
GridExcelFilter excelFilter = new GridExcelFilter();
excelFilter.AllowSearch = true; // Enable search in filter dropdown
excelFilter.AllowResize = true; // Allow resizing filter popup
excelFilter.EnableNumberFilter = true; // Enable number filters
excelFilter.EnableDateFilter = true; // Enable date filters
excelFilter.AllowFilterByColor = true; // Enable filter by cell color

excelFilter.WireGrid(gridGroupingControl1);
```

### Programmatic Grouping Pattern

```csharp
// Multi-level grouping
gridGroupingControl1.TableDescriptor.GroupedColumns.Add("Country");
gridGroupingControl1.TableDescriptor.GroupedColumns.Add("City");

// Customize group options
gridGroupingControl1.TopLevelGroupOptions.ShowCaption = true;
gridGroupingControl1.TopLevelGroupOptions.ShowGroupHeader = true;
gridGroupingControl1.TopLevelGroupOptions.ShowGroupFooter = true;

// Customize caption text with tokens
gridGroupingControl1.ChildGroupOptions.CaptionText = 
    "{CategoryName}: {Category} ({RecordCount} items)";
```

### Conditional Formatting Pattern

```csharp
// Apply conditional formatting based on cell value
gridGroupingControl1.QueryCellStyleInfo += (sender, e) =>
{
    if (e.TableCellIdentity.TableCellType == GridTableCellType.RecordFieldCell)
    {
        if (e.TableCellIdentity.Column.Name == "Salary")
        {
            decimal salary = Convert.ToDecimal(e.Style.CellValue);
            if (salary > 60000)
            {
                e.Style.BackColor = Color.LightGreen;
                e.Style.Font.Bold = true;
            }
            else if (salary < 40000)
            {
                e.Style.BackColor = Color.LightCoral;
            }
        }
    }
};
```

### Summary Pattern

```csharp
// Add multiple summaries for a group
GridSummaryRowDescriptor summaryRow = new GridSummaryRowDescriptor();
summaryRow.ShowSummaryInRow = false; // Show in separate columns

// Count summary
GridSummaryColumnDescriptor countColumn = new GridSummaryColumnDescriptor(
    "Count", SummaryType.Count, "ID", "{Count}");
summaryRow.SummaryColumns.Add(countColumn);

// Average summary
GridSummaryColumnDescriptor avgColumn = new GridSummaryColumnDescriptor(
    "Average", SummaryType.DoubleAggregate, "Salary", "Avg: {Average:C}");
summaryRow.SummaryColumns.Add(avgColumn);

// Total summary
GridSummaryColumnDescriptor sumColumn = new GridSummaryColumnDescriptor(
    "Total", SummaryType.DoubleAggregate, "Salary", "Total: {Sum:C}");
summaryRow.SummaryColumns.Add(sumColumn);

gridGroupingControl1.TableDescriptor.SummaryRows.Add(summaryRow);
```

## Key Properties

### Core Properties

| Property | Type | Description |
|----------|------|-------------|
| `DataSource` | object | Gets or sets the data source for the grid |
| `DataMember` | string | Gets or sets the data member within the data source |
| `ShowGroupDropArea` | bool | Shows or hides the group drop area for drag-drop grouping |
| `TableDescriptor` | GridTableDescriptor | Provides access to table configuration and columns |
| `TableOptions` | GridTableOptionsStyleInfo | Configures table-level options |
| `TopLevelGroupOptions` | GridGroupOptionsStyleInfo | Configures options for top-level groups |
| `ChildGroupOptions` | GridGroupOptionsStyleInfo | Configures options for child groups |

### Collection Properties

| Property | Type | Description |
|----------|------|-------------|
| `TableDescriptor.GroupedColumns` | SortColumnDescriptorCollection | Columns by which data is grouped |
| `TableDescriptor.SortedColumns` | SortColumnDescriptorCollection | Columns by which data is sorted |
| `TableDescriptor.RecordFilters` | RecordFilterDescriptorCollection | Programmatic record filters |
| `TableDescriptor.SummaryRows` | GridSummaryRowDescriptorCollection | Summary row definitions |
| `TableDescriptor.Columns` | GridColumnDescriptorCollection | Column descriptors |
| `TableDescriptor.Relations` | GridRelationDescriptorCollection | Child table relations |

## Key Events

### Data Events

- `QueryValue` - Raised when grid needs to retrieve unbound cell values
- `SaveValue` - Raised when grid needs to save unbound cell values
- `SourceListListChanged` - Raised when bound data source changes

### UI Events

- `QueryCellStyleInfo` - Raised to customize cell appearance dynamically
- `TableControlCellClick` - Raised when a cell is clicked
- `TableControlCellDoubleClick` - Raised when a cell is double-clicked
- `TableControlCurrentCellActivated` - Raised when a cell becomes current

### Grouping Events

- `GroupExpanding` / `GroupExpanded` - Raised when groups expand
- `GroupCollapsing` / `GroupCollapsed` - Raised when groups collapse
- `GroupedColumns.Changing` / `Changed` - Raised when grouping changes

### Sorting Events

- `SortedColumns.Changing` / `Changed` - Raised when sorting changes
- `TableControlQueryAllowSortColumn` - Raised to control column sorting

### Filtering Events

- `RecordFilters.Changing` / `Changed` - Raised when filters change
- `GridExcelFilter.RecordFiltersItemChanging` / `Changed` - Excel filter events

### Editing Events

- `TableControlCurrentCellStartEditing` - Raised when cell editing begins
- `TableControlCurrentCellEditingComplete` - Raised when cell editing completes
- `TableControlCurrentCellValidating` - Raised to validate cell values

## Common Use Cases

### Business Intelligence Dashboards
Display complex data with multi-level grouping, drill-down capabilities, and aggregate summaries for business analytics and reporting.

### Data Management Applications
Build CRUD applications with master-detail forms, inline editing, validation, and advanced filtering for data management.

### Hierarchical Data Visualization
Display organizational structures, product categories, or any hierarchical data with nested groups and expandable sections.

### Reporting Applications
Generate rich reports with grouping, summaries, conditional formatting, and export to multiple formats (Excel, PDF, Word).

### Data Analysis Tools
Implement interactive data exploration with dynamic grouping, sorting, filtering, and summary calculations.

## Architecture Notes

### Engine Architecture
GridGroupingControl uses a unique engine-based architecture that separates data management (Engine) from display (TableControl). This enables:
- Multiple views of the same data
- Efficient data virtualization
- Flexible grouping and sorting
- Independent nested table handling

### Display Elements
The grid organizes content into display elements:
- **Records** - Individual data rows
- **Groups** - Collections of records with matching category values
- **CaptionRows** - Group header rows
- **SummaryRows** - Aggregate summary rows
- **FilterBarCell** - Filter input cells

### Table Hierarchy
- **GridTable** - Top-level table instance
- **GridNestedTable** - Child table in master-detail relationship
- **TopLevelGroup** - Root group containing all records
- **Groups** - Nested group collections

## Best Practices

1. **Data Binding:** Use strongly-typed collections implementing IBindingList for automatic change notifications
2. **Performance:** Enable virtualization for large datasets (handled automatically)
3. **Grouping:** Limit initial grouping levels to 2-3 for better user experience
4. **Filtering:** Use GridExcelFilter for user-friendly filtering experience
5. **Summaries:** Place summaries strategically in captions or footers based on use case
6. **Styling:** Use QueryCellStyleInfo for dynamic styling instead of setting styles for all cells
7. **Events:** Minimize work in frequently-fired events like QueryCellStyleInfo
8. **Memory:** Dispose of GridGroupingControl properly when form closes

## Related Components

- **GridControl** - Standard non-grouping grid for simpler scenarios
- **GridDataBoundGrid** - Lightweight data-bound grid
- **DataGrid** - Standard .NET DataGrid control

Use GridGroupingControl when you need grouping, summaries, and hierarchical features. Use simpler grids for basic data display.

## Documentation Links

- **Official Documentation:** https://help.syncfusion.com/windowsforms/gridgrouping/overview
- **API Reference:** https://help.syncfusion.com/cr/windowsforms/Syncfusion.Windows.Forms.Grid.Grouping.html
- **Knowledge Base:** https://support.syncfusion.com/kb/windowsforms/gridgrouping

---

**Next Steps:** For detailed implementation guidance, navigate to the specific reference files above based on your requirements. Start with [getting-started.md](references/getting-started.md) for initial setup.