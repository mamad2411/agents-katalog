---
name: syncfusion-winui-treegrid
description: Guide for implementing Syncfusion WinUI TreeGrid (SfTreeGrid) components for displaying hierarchical or self-relational data. Use this skill when working with tree-structured grids, parent-child data relationships, or expandable grid rows. Covers TreeGrid features for organizational charts, file system displays, and multi-level data representation in WinUI applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion WinUI TreeGrid

## When to Use This Skill

Use this skill when you need to:
- Display hierarchical or self-relational data in a tree-structured grid
- Create data grids with parent-child relationships
- Implement expandable/collapsible rows with nested data
- Build organizational charts or employee hierarchies in grid format
- Display file system structures with grid features
- Work with category hierarchies, bill of materials, or nested classifications
- Need advanced grid features (sorting, filtering, editing) on tree-structured data
- Visualize multi-level data with column-based representation

## Component Overview

The Syncfusion® WinUI TreeGrid (SfTreeGrid) is a data-oriented control that displays self-relational or hierarchical data in a tree structure with grid capabilities. It combines the tree view's expandable/collapsible navigation with the data grid's rich feature set.

**Control Name:** `SfTreeGrid`  
**Namespace:** `Syncfusion.UI.Xaml.TreeGrid`  
**NuGet Package:** `Syncfusion.Grid.WinUI`  
**Platform:** WinUI 3 (Windows App SDK)

### Key Capabilities

- **Data Binding:** Self-relational and nested collection support
- **Columns:** 8 built-in column types with auto-generation
- **Editing:** Built-in editors for all column types with validation
- **Sorting:** Single and multi-column sorting
- **Filtering:** Excel-inspired filter UI
- **Selection:** Row and cell selection modes
- **Node Features:** Checkboxes, load-on-demand, expand/collapse
- **Row Operations:** Drag-and-drop, merge cells
- **Data Operations:** Clipboard operations, Excel export
- **Styling:** Conditional styling, custom templates
- **Advanced:** Context menus, tooltips, MVVM support

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Creating WinUI TreeGrid application setup
- NuGet package installation (Syncfusion.Grid.WinUI)
- Namespace imports and basic initialization
- First TreeGrid with minimal XAML/C# code
- Quick render verification

### Data Binding
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Binding self-relational data (ParentPropertyName, ChildPropertyName)
- SelfRelationRootValue configuration for root nodes
- Binding nested collections (hierarchical objects)
- Creating data models and ViewModels
- ItemsSource binding patterns
- Tree structure formation examples

### Columns and Column Types
📄 **Read:** [references/columns.md](references/columns.md)
- 8 built-in column types (Text, Numeric, Date, Time, CheckBox, ComboBox, Hyperlink, Template)
- Auto-generating columns vs manual definition
- AutoGeneratingColumn event for customization
- Column type selection based on data types
- TreeGridColumn base class and properties

### Column Configuration
📄 **Read:** [references/column-configuration.md](references/column-configuration.md)
- Column sizing and width modes (Auto, Star, Fill)
- Header customization and formatting
- MappingName for data binding
- Column visibility and ordering
- Frozen columns for fixed display
- Cell and edit templates

### Editing and Validation
📄 **Read:** [references/editing.md](references/editing.md)
- Enabling editing (AllowEditing property)
- Column-level editing control
- Edit mode configuration
- CurrentCellBeginEdit and CurrentCellEndEdit events
- Data validation during editing
- Programmatic editing operations
- Custom editor templates

### Selection
📄 **Read:** [references/selection.md](references/selection.md)
- Selection modes (Single, Multiple, Extended, None)
- Row selection vs cell selection (SelectionUnit)
- SelectionChanging and SelectionChanged events
- Programmatic selection APIs
- SelectedItem, SelectedItems properties
- Keyboard navigation patterns

### Sorting and Filtering
📄 **Read:** [references/sorting-filtering.md](references/sorting-filtering.md)
- Single and multi-column sorting
- SortColumnDescriptions collection
- SortColumnChanging/Changed events
- Custom sorting logic
- Excel-inspired filter UI (AllowFiltering)
- FilterChanging/Changed events
- Programmatic filtering with predicates
- Filter customization

### Row Operations
📄 **Read:** [references/row-operations.md](references/row-operations.md)
- Row height customization
- Row drag-and-drop functionality
- Drag-drop events and validation
- Merge cells feature
- Cell merging configuration
- Conditional row styling
- Row validation rules

### Node Features
📄 **Read:** [references/node-features.md](references/node-features.md)
- Node checkboxes for selection
- Recursive checking behavior
- NodeCheckStateChanging/Changed events
- Load-on-demand (lazy loading child nodes)
- LoadOnDemandCommand
- HasChildNodes property
- Dynamic child population

### Data Operations
📄 **Read:** [references/data-operations.md](references/data-operations.md)
- Clipboard operations (copy/paste)
- CopyOption property configuration
- CopyGridCellContent event
- Export to Excel functionality
- ExcelExportingOptions
- Exporting selected items
- Export customization and formatting

### Styling and Customization
📄 **Read:** [references/styling-customization.md](references/styling-customization.md)
- Conditional styling based on data
- Cell and row styling
- QueryCellStyle and QueryRowStyle events
- GridLines customization
- GridLinesVisibility property
- UI customization and templates
- Theme integration

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Context flyout menus
- Custom context menu items
- Tooltips for cells and headers
- Custom tooltip templates
- MVVM pattern support
- Commands and data binding
- Helper methods and utilities
- Performance optimization techniques

## Quick Start Example

### Self-Relational Data

```xaml
<Window
    x:Class="TreeGridDemo.MainWindow"
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    xmlns:treeGrid="using:Syncfusion.UI.Xaml.TreeGrid">
    
    <Window.DataContext>
        <local:ViewModel/>
    </Window.DataContext>
    
    <Grid>
        <treeGrid:SfTreeGrid x:Name="treeGrid"
                            ItemsSource="{Binding Employees}"
                            ParentPropertyName="ID"
                            ChildPropertyName="ReportsTo"
                            SelfRelationRootValue="-1"
                            AutoExpandMode="RootNodesExpanded" />
    </Grid>
</Window>
```

```csharp
public class EmployeeInfo
{
    public int ID { get; set; }
    public string FirstName { get; set; }
    public string LastName { get; set; }
    public string Title { get; set; }
    public double Salary { get; set; }
    public int ReportsTo { get; set; }
}

public class ViewModel
{
    public ObservableCollection<EmployeeInfo> Employees { get; set; }
    
    public ViewModel()
    {
        Employees = new ObservableCollection<EmployeeInfo>
        {
            new EmployeeInfo { ID = 1, FirstName = "John", LastName = "Doe", 
                              Title = "CEO", Salary = 200000, ReportsTo = -1 },
            new EmployeeInfo { ID = 2, FirstName = "Jane", LastName = "Smith", 
                              Title = "Manager", Salary = 120000, ReportsTo = 1 },
            new EmployeeInfo { ID = 3, FirstName = "Bob", LastName = "Johnson", 
                              Title = "Developer", Salary = 80000, ReportsTo = 2 }
        };
    }
}
```

### Nested Collection Data

```csharp
public class PersonInfo
{
    public string FirstName { get; set; }
    public string LastName { get; set; }
    public double Salary { get; set; }
    public ObservableCollection<PersonInfo> Children { get; set; }
}
```

```xaml
<treeGrid:SfTreeGrid x:Name="treeGrid"
                    ItemsSource="{Binding PersonDetails}"
                    ChildPropertyName="Children" />
```

## Common Patterns

### Self-Relational Data Structure

Use when data objects reference each other via ID/ParentID:

```csharp
// Each employee has an ID and ReportsTo (parent ID)
ParentPropertyName = "ID"
ChildPropertyName = "ReportsTo"
SelfRelationRootValue = -1  // Root nodes have ReportsTo = -1
```

### Nested Collection Structure

Use when data objects contain child collections:

```csharp
// Each person has a Children property containing child objects
ChildPropertyName = "Children"
// No ParentPropertyName needed
```

### Column Auto-Generation Control

```xaml
<!-- Auto-generate columns from data properties -->
<treeGrid:SfTreeGrid AutoGenerateColumns="True" />

<!-- Define columns manually for full control -->
<treeGrid:SfTreeGrid AutoGenerateColumns="False">
    <treeGrid:SfTreeGrid.Columns>
        <treeGrid:TreeGridTextColumn MappingName="FirstName" HeaderText="First Name"/>
        <treeGrid:TreeGridNumericColumn MappingName="Salary" DisplayNumberFormat="C2"/>
    </treeGrid:SfTreeGrid.Columns>
</treeGrid:SfTreeGrid>
```

### MVVM Data Binding

```csharp
public class ViewModel : INotifyPropertyChanged
{
    private ObservableCollection<DataModel> _items;
    
    public ObservableCollection<DataModel> Items
    {
        get => _items;
        set
        {
            _items = value;
            OnPropertyChanged();
        }
    }
    
    public event PropertyChangedEventHandler PropertyChanged;
    
    protected void OnPropertyChanged([CallerMemberName] string name = null)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
    }
}
```

### Expand/Collapse Control

```csharp
// Auto-expand modes
AutoExpandMode = AutoExpandMode.AllNodesExpanded;  // All expanded
AutoExpandMode = AutoExpandMode.RootNodesExpanded; // Only root
AutoExpandMode = AutoExpandMode.None;              // All collapsed

// Programmatic control
treeGrid.ExpandNode(node);
treeGrid.CollapseNode(node);
treeGrid.ExpandAllNodes();
treeGrid.CollapseAllNodes();
```

## Key Properties

### Data Binding Properties

- **ItemsSource** - Data source (IEnumerable)
  - When: Always required for data binding
  - Why: Provides the data to display

- **ChildPropertyName** - Property containing child collection or parent reference
  - When: Required for all tree structures
  - Why: Defines the tree relationship

- **ParentPropertyName** - Property containing unique identifier (self-relational only)
  - When: Only for self-relational data
  - Why: Identifies parent nodes

- **SelfRelationRootValue** - Value indicating root nodes (self-relational only)
  - When: With self-relational data
  - Why: Identifies which nodes are roots (default: null)

### Display Properties

- **AutoGenerateColumns** - Auto-create columns from properties (default: true)
  - When: Set false for manual column control
  - Why: Automatic vs explicit column definition

- **AutoExpandMode** - Initial expand state
  - When: Control initial tree visibility
  - Why: User experience for data exploration

- **ColumnWidthMode** - How columns calculate width
  - When: Control column sizing behavior
  - Why: Auto, Star, or fixed widths

### Feature Properties

- **AllowEditing** - Enable cell editing (default: false)
  - When: Editable grid needed
  - Why: In-place data modification

- **AllowFiltering** - Enable filter UI (default: false)
  - When: Large datasets need filtering
  - Why: Excel-style data filtering

- **SelectionMode** - Row/cell selection type
  - When: Control selection behavior
  - Why: Single, Multiple, Extended, or None

- **SelectionUnit** - Select rows or cells
  - When: Define selection granularity
  - Why: Row vs cell-level selection

## Common Use Cases

### Organizational Hierarchy
Display company structure with employees reporting to managers:
```csharp
ParentPropertyName = "EmployeeID"
ChildPropertyName = "ManagerID"
```

### File System Browser
Show folders and files in tree structure:
```csharp
ChildPropertyName = "SubItems"  // Nested collection
```

### Category Management
Display product categories with subcategories:
```csharp
ChildPropertyName = "SubCategories"
```

### Bill of Materials (BOM)
Show product assemblies and components:
```csharp
ParentPropertyName = "PartID"
ChildPropertyName = "ParentPartID"
```

### Task/Project Management
Display tasks with subtasks:
```csharp
ChildPropertyName = "SubTasks"
```

### Geographic Hierarchies
Show countries > states > cities:
```csharp
ChildPropertyName = "Children"
```

## Troubleshooting

### Tree Structure Not Forming
- Verify ParentPropertyName and ChildPropertyName are set correctly
- Check SelfRelationRootValue matches your data's root indicator
- Ensure data relationships are properly defined

### Columns Not Appearing
- Set AutoGenerateColumns = True, or define columns manually
- Check MappingName matches property names exactly (case-sensitive)
- Verify data source is bound to ItemsSource

### Performance Issues with Large Datasets
- Enable load-on-demand for lazy loading
- Use on-demand mode to defer child node loading
- Consider data virtualization for very large trees

### Editing Not Working
- Set AllowEditing = True on TreeGrid
- Check column-level AllowEditing property
- Ensure data objects implement INotifyPropertyChanged

---

**Next Steps:** Read the getting-started guide, then explore feature-specific references based on your requirements.
