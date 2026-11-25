---
name: syncfusion-winui-datagrid
description: Guide for implementing Syncfusion WinUI DataGrid (SfDataGrid) for tabular data display in desktop applications. Use this skill when working with data grids, sorting, filtering, grouping, or CRUD operations. Covers data binding, column configuration, master-details views, Excel export, and performance optimization including data virtualization and custom templates.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing WinUI DataGrid (SfDataGrid)

Comprehensive guide for implementing the Syncfusion WinUI DataGrid control. SfDataGrid is a high-performance, feature-rich control for displaying and manipulating tabular data in WinUI 3 applications with support for sorting, filtering, grouping, editing, summaries, and more.

## When to Use This Skill

Use this skill when you need to:
- Display tabular data with 100 to 1,000,000+ rows in WinUI applications
- Implement sortable, filterable, and groupable data views
- Enable inline editing with validation for data entry scenarios
- Perform CRUD (Create, Read, Update, Delete) operations on datasets
- Export data to Excel format
- Display hierarchical data with master-details views
- Implement drag-and-drop row reordering
- Show data summaries and aggregations (sum, average, count, etc.)
- Handle real-time data updates with ObservableCollection
- Create data-centric enterprise Windows desktop applications

**Important Note:** In WinUI 3, DataContext is not directly inherited from Window. You must explicitly set DataContext on the Grid or Page element in XAML (e.g., `<Grid DataContext="{x:Bind ViewModel}">`) for data binding to work properly.

## DataGrid Overview

**SfDataGrid** (`Syncfusion.UI.Xaml.DataGrid.SfDataGrid`) is the primary grid control for WinUI 3, offering:

- **High Performance:** UI and data virtualization for millions of rows
- **Rich Data Operations:** Sorting, filtering, grouping with multi-level support
- **Editing:** Cell/row/batch editing modes with validation
- **Summaries:** Table, group, and caption summaries with custom aggregates
- **Selection:** Single/multiple row or cell selection
- **Styling:** Conditional formatting and custom templates
- **Export:** Excel export with styling
- **Advanced Features:** Unbound rows, master-details, frozen columns

**Required Packages:**
- **Main Package:** `Syncfusion.Grid.WinUI` (DataGrid control)
- **Export Package:** `Syncfusion.GridExport.WinUI` (Excel export functionality)
- **Excel Engine:** `Syncfusion.XlsIO.NET` (Required for export operations)

**Namespace:** `Syncfusion.UI.Xaml.DataGrid`

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Data binding fundamentals (IEnumerable, ObservableCollection, dynamic objects)
- ItemsSource configuration and INotifyCollectionChanged
- Complex property binding (nested objects)
- Basic XAML setup and first implementation
- Package installation and namespace registration

### Column Management
📄 **Read:** [references/columns.md](references/columns.md)
- Column types (GridTextColumn, GridNumericColumn, GridCheckBoxColumn, GridComboBoxColumn, etc.)
- Auto-generate vs manual column definition
- Column width modes (Auto, Star, None, Fill, AutoLastColumnFill)
- Column sizing, autosize, and resizing
- Show/hide columns and column visibility
- Column reordering and freeze columns

### Data Operations (Sorting, Filtering, Grouping)
📄 **Read:** [references/data-operations.md](references/data-operations.md)
- Sorting: Single and multi-column sorting, custom sorting, tri-state sorting
- Filtering: Programmatic filters, view predicates, column filters, filter row
- Grouping: Single and multi-level grouping, custom grouping, expand/collapse
- Group summaries and filter row configuration

### Editing and Data Validation
📄 **Read:** [references/editing-validation.md](references/editing-validation.md)
- Editing modes: Cell, row, and batch editing
- Edit triggers (single click, double click, F2 key)
- Data validation rules and error handling
- CRUD operations: Add, update, delete rows
- Commit and cancel changes
- CurrentCell navigation

### Selection
📄 **Read:** [references/selection.md](references/selection.md)
- Selection modes: Single, Multiple, Extended, None
- Selection units: Row and Cell
- SelectedItem, SelectedItems, SelectedIndex binding
- Programmatic selection and SelectionChanged events
- Select all rows, select ranges

### Summaries and Aggregations
📄 **Read:** [references/summaries.md](references/summaries.md)
- Table summaries (displayed in footer)
- Group summaries (per group)
- Caption summaries (in group headers)
- Built-in aggregates (Sum, Average, Count, Min, Max)
- Custom summary calculations
- Summary row positioning

### Conditional Styling
📄 **Read:** [references/conditional-styling.md](references/conditional-styling.md)
- Row styling based on data conditions
- Cell styling and custom templates
- Style selectors for dynamic styling
- Visual states and data templates
- Alternating row colors

### Advanced Row Features
📄 **Read:** [references/row-features.md](references/row-features.md)
- Row drag and drop for reordering
- Unbound rows (above and below data rows)
- Master-details view for hierarchical data
- Row height customization
- Details view templates and nested grids

### Data Virtualization
📄 **Read:** [references/virtualization.md](references/virtualization.md)
- Data virtualization for large datasets
- UI virtualization (enabled by default)
- Virtual mode configuration
- Performance optimization techniques
- Handling 100,000+ rows efficiently

### Export to Excel
📄 **Read:** [references/export.md](references/export.md)
- Export entire grid to Excel (.xlsx)
- Export options and customization
- Export selected rows only
- Export with styling and formatting
- Custom export logic

## Quick Start Example

### Basic Implementation

```xml
<!-- MainPage.xaml -->
<Page xmlns:dataGrid="using:Syncfusion.UI.Xaml.DataGrid">
    
    <Grid>
        <dataGrid:SfDataGrid x:Name="sfDataGrid"
                             ItemsSource="{Binding Orders}"
                             AutoGenerateColumns="True"
                             AllowSorting="True"
                             AllowFiltering="True"
                             AllowEditing="True"
                             SelectionMode="Single" />
    </Grid>
</Page>
```

```csharp
// MainPage.xaml.cs
using Microsoft.UI.Xaml.Controls;
using System.Collections.ObjectModel;

public sealed partial class MainPage : Page
{
    public ObservableCollection<Order> Orders { get; set; }
    
    public MainPage()
    {
        this.InitializeComponent();
        
        Orders = new ObservableCollection<Order>
        {
            new Order { OrderID = 1001, CustomerName = "Maria Anders", Country = "Germany", Total = 250.50M },
            new Order { OrderID = 1002, CustomerName = "Ana Trujillo", Country = "Mexico", Total = 180.00M },
            new Order { OrderID = 1003, CustomerName = "Antonio Moreno", Country = "Mexico", Total = 420.75M }
        };
        
        sfDataGrid.ItemsSource = Orders;
    }
}

// Order Model
public class Order
{
    public int OrderID { get; set; }
    public string CustomerName { get; set; }
    public string Country { get; set; }
    public decimal Total { get; set; }
}
```

## Common Patterns

### Pattern 1: Manual Column Definition

```xml
<dataGrid:SfDataGrid x:Name="sfDataGrid"
                     AutoGenerateColumns="False"
                     ItemsSource="{Binding Orders}">
    <dataGrid:SfDataGrid.Columns>
        <dataGrid:GridTextColumn MappingName="OrderID" 
                                 HeaderText="Order ID" 
                                 Width="120" />
        <dataGrid:GridTextColumn MappingName="CustomerName" 
                                 HeaderText="Customer" 
                                 Width="200" />
        <dataGrid:GridTextColumn MappingName="Country" 
                                 Width="150" />
        <dataGrid:GridNumericColumn MappingName="Total" 
                                    HeaderText="Total Amount"
                                    Width="150" />
    </dataGrid:SfDataGrid.Columns>
</dataGrid:SfDataGrid>
```

### Pattern 2: Enable Sorting and Filtering

```xml
<dataGrid:SfDataGrid x:Name="sfDataGrid"
                     ItemsSource="{Binding Orders}"
                     AllowSorting="True"
                     AllowFiltering="True"
                     FilterRowPosition="FixedTop"
                     AllowTriStateSorting="True" />
```

### Pattern 3: Enable Grouping

```xml
<dataGrid:SfDataGrid x:Name="sfDataGrid"
                     ItemsSource="{Binding Orders}"
                     AllowGrouping="True"
                     ShowGroupDropArea="True" />
```

```csharp
// Programmatic grouping
sfDataGrid.GroupColumnDescriptions.Add(new GroupColumnDescription { ColumnName = "Country" });
```

### Pattern 4: Enable Editing

```xml
<dataGrid:SfDataGrid x:Name="sfDataGrid"
                     ItemsSource="{Binding Orders}"
                     AllowEditing="True"
                     EditTrigger="OnDoubleTap"
                     NavigationMode="Cell" />
```

### Pattern 5: Add Summaries

```xml
<dataGrid:SfDataGrid x:Name="sfDataGrid"
                     ItemsSource="{Binding Orders}"
                     ShowRowHeader="True">
    <dataGrid:SfDataGrid.TableSummaryRows>
        <dataGrid:GridTableSummaryRow ShowSummaryInRow="False">
            <dataGrid:GridTableSummaryRow.SummaryColumns>
                <dataGrid:GridSummaryColumn Name="TotalSum"
                                            MappingName="Total"
                                            SummaryType="DoubleAggregate"
                                            Format="'Total: {Sum:C}'" />
                <dataGrid:GridSummaryColumn Name="OrderCount"
                                            MappingName="OrderID"
                                            SummaryType="CountAggregate"
                                            Format="'Count: {Count}'" />
            </dataGrid:GridTableSummaryRow.SummaryColumns>
        </dataGrid:GridTableSummaryRow>
    </dataGrid:SfDataGrid.TableSummaryRows>
</dataGrid:SfDataGrid>
```

## Key Properties

| Property | Type | Description |
|----------|------|-------------|
| `ItemsSource` | `object` | Data source for the grid (IEnumerable) |
| `AutoGenerateColumns` | `bool` | Auto-create columns from data source properties |
| `Columns` | `Columns` | Collection of manually defined columns |
| `AllowSorting` | `bool` | Enable/disable sorting (default: false) |
| `AllowFiltering` | `bool` | Enable/disable filtering (default: false) |
| `AllowGrouping` | `bool` | Enable/disable grouping (default: false) |
| `AllowEditing` | `bool` | Enable/disable editing (default: false) |
| `SelectionMode` | `GridSelectionMode` | Single, Multiple, Extended, None |
| `SelectionUnit` | `GridSelectionUnit` | Row or Cell |
| `NavigationMode` | `NavigationMode` | Cell or Row navigation |
| `ColumnWidthMode` | `ColumnWidthMode` | None, Star, Auto, SizeToCells, SizeToHeader, AutoLastColumnFill, AutoWithLastColumnFill |
| `ShowGroupDropArea` | `bool` | Show drag-and-drop area for grouping |
| `FilterRowPosition` | `FilterRowPosition` | FixedTop, Top, Bottom |

## Common Use Cases

### Enterprise Data Entry Application
- Enable editing, validation, and CRUD operations
- Use batch editing mode for efficiency
- Implement SelectedItems binding for bulk operations
- Add table summaries for data insights

### Data Analysis Dashboard
- Enable sorting, filtering, and grouping
- Add summaries at table and group levels
- Use conditional styling to highlight key data
- Implement export to Excel for reporting

### Master-Details Data Viewer
- Configure DetailsViewDefinition for nested data
- Use hierarchical data binding
- Enable expand/collapse for details
- Style master and details rows differently

### Large Dataset Browser (100K+ rows)
- Enable data virtualization
- Disable features not needed (grouping, summaries)
- Use frozen columns for important data
- Implement incremental loading

### Transaction Management System
- Enable row drag-and-drop for prioritization
- Use unbound rows for totals and summary info
- Implement real-time updates with ObservableCollection
- Add validation rules for data integrity

## Integration with MVVM

```csharp
// ViewModel
public class OrderViewModel : INotifyPropertyChanged
{
    private ObservableCollection<Order> orders;
    private Order selectedOrder;
    
    public ObservableCollection<Order> Orders
    {
        get => orders;
        set { orders = value; OnPropertyChanged(); }
    }
    
    public Order SelectedOrder
    {
        get => selectedOrder;
        set { selectedOrder = value; OnPropertyChanged(); }
    }
    
    public ICommand DeleteCommand { get; }
    public ICommand ExportCommand { get; }
}
```

```xml
<!-- View -->
<dataGrid:SfDataGrid ItemsSource="{Binding Orders}"
                     SelectedItem="{Binding SelectedOrder, Mode=TwoWay}" />
```

## Performance Tips

1. **Use ObservableCollection** for automatic UI updates instead of List<T>
2. **Set AutoGenerateColumns="False"** and define columns manually when possible
3. **Enable virtualization** (enabled by default, don't disable unless needed)
4. **Freeze essential columns** to improve horizontal scrolling performance
5. **Use ColumnWidthMode="None"** for static column widths when data size is known
6. **Limit grouping levels** to 2-3 for better performance
7. **Use filtering instead of grouping** for very large datasets (100K+)
8. **Dispose the grid** in Page.Unloaded event

## Troubleshooting

**Data not displaying:**
- Verify `ItemsSource` is bound correctly
- Check properties have public getters
- Ensure `DataContext` is set if using binding

**Editing not working:**
- Set `AllowEditing="True"`
- Set `NavigationMode="Cell"`
- Verify column has `AllowEditing="True"` (inherited from grid if not set)

**Poor performance with large datasets:**
- Verify virtualization is enabled (default)
- Reduce number of columns
- Use `ColumnWidthMode="None"` instead of Auto
- Consider data pagination for 500K+ rows

**Sorting/Filtering not working:**
- Set `AllowSorting="True"` and/or `AllowFiltering="True"`
- Verify data source implements IEnumerable
- Check if column has these disabled individually

## Related Components
- **TreeGrid:** For hierarchical tree data
- **PivotGrid:** For OLAP and pivot table scenarios
- **PropertyGrid:** For editing object properties
