---
name: syncfusion-winforms-multicolumn-treeview
description: Implements Syncfusion MultiColumnTreeView control for Windows Forms applications to display hierarchical data with additional columns. Use this when working with TreeNodeAdv, TreeColumnAdv, multi-column tree structures, or hierarchical data requiring multiple columns per node. The skill covers node collections, checkboxes, option buttons, XML data binding, load on demand features, and tree appearance customization.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing MultiColumn TreeView

The MultiColumnTreeView is an advanced treeview control for Windows Forms that displays hierarchical data with multiple columns. This control combines the tree structure visualization with additional data columns, making it ideal for file explorers, organizational charts, and data browsers where you need to show both hierarchy and related information.

## When to Use This Skill

Use this skill when you need to:
- **Display hierarchical data** with multiple columns of information
- **Build file explorers** or folder browsers with metadata columns
- **Create organizational charts** with employee details
- **Show product catalogs** with hierarchical categories and specifications
- **Implement data browsers** with parent-child relationships
- **Add interactive features** like checkboxes, option buttons, or inline editing
- **Load large datasets** on demand for better performance
- **Sort and filter** hierarchical data dynamically
- **Customize appearance** with styles, colors, and themes
- **Bind to XML data** for easy import/export

## Component Overview

The MultiColumnTreeView provides:

**Core Components:**
- **TreeNodeAdv** - Individual nodes with text, images, and subitems
- **TreeColumnAdv** - Column definitions with headers and styling
- **TreeNodeAdvSubItem** - Additional column data for each node

**Key Capabilities:**
- Multiple columns with customizable headers
- Hierarchical node structure with unlimited depth
- Interactive elements (checkboxes, option buttons)
- Multiple selection modes
- Sorting and filtering
- Load on demand for performance
- Flexible style architecture
- XML data binding
- Event-driven interactions

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and assembly deployment
- Adding MultiColumnTreeView via designer
- Adding MultiColumnTreeView via code
- Creating columns (TreeColumnAdv)
- Adding nodes and child nodes
- Adding subitems for additional columns
- First working example

### Nodes and Columns Management
📄 **Read:** [references/nodes-and-columns.md](references/nodes-and-columns.md)
- TreeNodeAdv properties and features
- TreeColumnAdv configuration
- Adding/removing nodes dynamically
- Building hierarchical structures
- SubItems and multi-column data
- Node collection operations
- Column sizing and auto-sizing

### Node Features
📄 **Read:** [references/node-features.md](references/node-features.md)
- CheckBoxes and InteractiveCheckBoxes
- OptionButtons (radio button selection)
- ToolTips and HelpText
- Plus/Minus expansion symbols
- Root lines and connecting lines
- Custom controls in nodes
- Primitives (LabelPrimitive, ImagePrimitive, CheckBoxPrimitive)
- Multiline node text

### Selection and Editing
📄 **Read:** [references/selection-and-editing.md](references/selection-and-editing.md)
- SelectionMode (Single, MultiSelectSameLevel, MultiSelectAll)
- SelectedNode and SelectedNodes properties
- ActiveNode management
- Mouse-based selection (drag selection)
- Keyboard search functionality
- Label editing (LabelEdit property)
- Node editing events

### Data Binding
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Loading data from XML files
- Saving tree structure to XML
- XML node mapping
- Data binding patterns
- Dynamic node population
- Export and import operations

### Sorting and Filtering
📄 **Read:** [references/sorting-and-filtering.md](references/sorting-and-filtering.md)
- Sort method and SortOrder
- SortType (Checkbox, Tag, Text)
- SortWithChildNode property
- CompareOptions for text comparison
- Filter levels (Root, All, Extended)
- Creating filter delegates
- RefreshFilter method
- Clearing filters

### Appearance Customization
📄 **Read:** [references/appearance.md](references/appearance.md)
- Border styles (2D and 3D borders)
- Color customization (background, foreground, lines)
- Header customization
- BaseStyles for nodes and columns
- Selected node appearance
- SubItem styling
- Visual styles (Office2016Colorful, White, Black, DarkGray)
- Image lists (LeftImage, RightImage, StateImage)

### Performance Optimization
📄 **Read:** [references/performance.md](references/performance.md)
- SuspendExpandRecalculate property
- BeginUpdate/EndUpdate pattern
- Load on demand implementation
- Large dataset handling
- Memory management tips
- Performance best practices

### Events
📄 **Read:** [references/events.md](references/events.md)
- Node selection events
- Expand/collapse events
- Editing events (BeforeEdit, AfterEdit)
- Mouse and keyboard events
- Custom event handling patterns
- Event subscription examples

## Quick Start Example

Here's a minimal example showing a MultiColumnTreeView with countries and capitals:

```csharp
using System;
using System.Windows.Forms;
using Syncfusion.Windows.Forms.Tools.MultiColumnTreeView;

public class MultiColumnTreeViewExample : Form
{
    private MultiColumnTreeView multiColumnTreeView1;
    
    public MultiColumnTreeViewExample()
    {
        InitializeForm();
        SetupMultiColumnTreeView();
        PopulateData();
    }
    
    private void InitializeForm()
    {
        this.Text = "MultiColumnTreeView Example";
        this.Size = new System.Drawing.Size(600, 400);
    }
    
    private void SetupMultiColumnTreeView()
    {
        // Create control
        multiColumnTreeView1 = new MultiColumnTreeView();
        multiColumnTreeView1.Dock = DockStyle.Fill;
        
        // Add columns
        TreeColumnAdv countryColumn = new TreeColumnAdv();
        countryColumn.Text = "Country";
        countryColumn.Width = 200;
        
        TreeColumnAdv capitalColumn = new TreeColumnAdv();
        capitalColumn.Text = "Capital";
        capitalColumn.Width = 150;
        
        multiColumnTreeView1.Columns.AddRange(
            new TreeColumnAdv[] { countryColumn, capitalColumn });
        
        // Add to form
        this.Controls.Add(multiColumnTreeView1);
    }
    
    private void PopulateData()
    {
        // Create parent nodes
        TreeNodeAdv asiaNode = new TreeNodeAdv();
        asiaNode.Text = "Asia";
        
        TreeNodeAdv europeNode = new TreeNodeAdv();
        europeNode.Text = "Europe";
        
        // Create child nodes with subitems
        TreeNodeAdv indiaNode = new TreeNodeAdv();
        indiaNode.Text = "India";
        TreeNodeAdvSubItem delhiSubItem = new TreeNodeAdvSubItem();
        delhiSubItem.Text = "New Delhi";
        indiaNode.SubItems.Add(delhiSubItem);
        
        TreeNodeAdv chinaNode = new TreeNodeAdv();
        chinaNode.Text = "China";
        TreeNodeAdvSubItem beijingSubItem = new TreeNodeAdvSubItem();
        beijingSubItem.Text = "Beijing";
        chinaNode.SubItems.Add(beijingSubItem);
        
        TreeNodeAdv ukNode = new TreeNodeAdv();
        ukNode.Text = "United Kingdom";
        TreeNodeAdvSubItem londonSubItem = new TreeNodeAdvSubItem();
        londonSubItem.Text = "London";
        ukNode.SubItems.Add(londonSubItem);
        
        // Build hierarchy
        asiaNode.Nodes.AddRange(new TreeNodeAdv[] { indiaNode, chinaNode });
        europeNode.Nodes.Add(ukNode);
        
        multiColumnTreeView1.Nodes.AddRange(
            new TreeNodeAdv[] { asiaNode, europeNode });
    }
    
    [STAThread]
    static void Main()
    {
        Application.EnableVisualStyles();
        Application.Run(new MultiColumnTreeViewExample());
    }
}
```

## Common Patterns

### Pattern 1: Adding Nodes with Multiple Columns

```csharp
// Create node for first column
TreeNodeAdv employeeNode = new TreeNodeAdv();
employeeNode.Text = "John Doe";

// Add subitems for additional columns
TreeNodeAdvSubItem departmentSubItem = new TreeNodeAdvSubItem();
departmentSubItem.Text = "Engineering";

TreeNodeAdvSubItem salarySubItem = new TreeNodeAdvSubItem();
salarySubItem.Text = "$85,000";

employeeNode.SubItems.Add(departmentSubItem);
employeeNode.SubItems.Add(salarySubItem);

multiColumnTreeView1.Nodes.Add(employeeNode);
```

### Pattern 2: Interactive Nodes with Checkboxes

```csharp
// Enable checkboxes for all nodes
multiColumnTreeView1.ShowCheckBoxes = true;
multiColumnTreeView1.InteractiveCheckBoxes = true;

// Or for individual nodes
TreeNodeAdv node = new TreeNodeAdv();
node.Text = "Select Me";
node.ShowCheckBox = true;
node.InteractiveCheckBox = true; // Parent reflects child states
```

### Pattern 3: Sorting Tree Data

```csharp
// Sort by text in ascending order
multiColumnTreeView1.Nodes.Sort(SortOrder.Ascending);

// Sort with child nodes
multiColumnTreeView1.Nodes[0].SortOrder = SortOrder.Descending;
```

### Pattern 4: Filtering Nodes

```csharp
// Define filter delegate
public bool FilterNodes(object o)
{
    var node = o as TreeNodeAdv;
    if (node.SubItems.Count > 0)
    {
        int value = int.Parse(node.SubItems[0].Text);
        return value > 50000; // Filter by criteria
    }
    return false;
}

// Apply filter
multiColumnTreeView1.FilterLevel = FilterLevel.Extended;
multiColumnTreeView1.Filter = FilterNodes;
multiColumnTreeView1.RefreshFilter();
```

### Pattern 5: Handling Selection Events

```csharp
// Subscribe to node selected event
multiColumnTreeView1.NodeSelected += (sender, e) =>
{
    if (multiColumnTreeView1.SelectedNode != null)
    {
        string nodeText = multiColumnTreeView1.SelectedNode.Text;
        MessageBox.Show($"Selected: {nodeText}");
    }
};
```

## Key Properties and Methods

### Essential Properties

**Control-Level:**
- `Columns` - Collection of TreeColumnAdv objects
- `Nodes` - Root-level TreeNodeAdv collection
- `SelectedNode` - Currently selected node (single selection)
- `SelectedNodes` - Collection of selected nodes (multi-selection)
- `ActiveNode` - Node with focus
- `SelectionMode` - Single, MultiSelectSameLevel, MultiSelectAll
- `ShowCheckBoxes` - Display checkboxes on all nodes
- `ShowOptionButtons` - Display option buttons on all nodes
- `ShowLines` - Show connecting lines between nodes
- `ShowRootLines` - Show lines between root nodes
- `ShowPlusMinus` - Show expand/collapse symbols
- `Style` - Visual theme (Office2016Colorful, White, Black, DarkGray)
- `FilterLevel` - Filter scope (Root, All, Extended)
- `Filter` - Filter delegate function

**Node Properties (TreeNodeAdv):**
- `Text` - Node text content
- `SubItems` - Collection of TreeNodeAdvSubItem objects
- `Nodes` - Child nodes collection
- `Checked` - Checkbox state
- `Optioned` - Option button state
- `Expanded` - Expand/collapse state
- `ShowCheckBox` - Show checkbox for this node
- `ShowOptionButton` - Show option button for this node
- `LeftImageIndices` - Left image indices
- `RightImageIndices` - Right image indices
- `HelpText` - Tooltip text

**Column Properties (TreeColumnAdv):**
- `Text` - Column header text
- `Width` - Column width in pixels
- `Background` - Header background brush
- `TextColor` - Header text color

### Essential Methods

**Control Methods:**
- `BeginUpdate()` - Suspend visual updates for performance
- `EndUpdate()` - Resume visual updates
- `ExpandAll()` - Expand all nodes
- `CollapseAll()` - Collapse all nodes
- `RefreshFilter()` - Reapply current filter
- `Sort()` - Sort nodes

**Node Methods:**
- `Expand()` - Expand node
- `Collapse()` - Collapse node
- `EnsureVisible()` - Scroll node into view

## Common Use Cases

### Use Case 1: File Explorer
Display file system hierarchy with file names, sizes, dates, and types across multiple columns. Use icons for file types and implement lazy loading for large directory structures.

### Use Case 2: Organizational Chart
Show company structure with employee names, titles, departments, and contact information. Use checkboxes for selection and option buttons for primary contact designation.

### Use Case 3: Product Catalog
Display product categories and subcategories with pricing, stock, and description columns. Implement filtering by price range or stock availability.

### Use Case 4: Project Task Manager
Show project tasks in hierarchical structure with task names, assignees, due dates, and status. Use checkboxes for task completion tracking.

### Use Case 5: Database Schema Viewer
Display database tables, views, and columns in tree format with data types, constraints, and descriptions in additional columns.

## Assembly Requirements

**Required Assemblies:**
- `Syncfusion.Grid.Base`
- `Syncfusion.Grid.Windows`
- `Syncfusion.Shared.Base`
- `Syncfusion.Shared.Windows`
- `Syncfusion.Tools.Base`
- `Syncfusion.Tools.Windows`

**Installation via NuGet:**
```powershell
Install-Package Syncfusion.Tools.Windows
```

## Best Practices

1. **Use BeginUpdate/EndUpdate** when adding many nodes to improve performance
2. **Enable load on demand** for large datasets to reduce initial load time
3. **Set SuspendExpandRecalculate** to true for faster node expansion with many nodes
4. **Use appropriate selection mode** based on user requirements
5. **Provide clear column headers** to make data relationships obvious
6. **Handle events** to respond to user interactions appropriately
7. **Apply consistent styling** through BaseStyles for professional appearance
8. **Test with large datasets** to ensure performance meets requirements
9. **Use XML binding** for easy data persistence
10. **Clear filters** when no longer needed to show all data

## Related Components

- **TreeView** - Single-column tree control
- **DataGrid** - Flat grid without hierarchy
- **ListView** - List with columns but no tree structure

## Troubleshooting Tips

- **Nodes not displaying:** Check if columns are added before nodes
- **SubItems not visible:** Ensure SubItems count matches column count - 1
- **Performance issues:** Use BeginUpdate/EndUpdate and SuspendExpandRecalculate
- **Checkboxes not working:** Verify ShowCheckBoxes or ShowCheckBox is true
- **Filter not applying:** Call RefreshFilter() after setting Filter delegate
- **Selection not working:** Check SelectionMode property setting