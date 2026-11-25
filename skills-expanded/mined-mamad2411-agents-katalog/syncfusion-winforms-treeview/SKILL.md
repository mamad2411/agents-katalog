---
name: syncfusion-winforms-treeview
description: Implements Syncfusion TreeViewAdv control for Windows Forms applications to display hierarchical tree structures, file explorers, organization charts, and nested data. Use this when working with hierarchical data, parent-child relationships, expandable nodes, file browser interfaces, or folder structures. The skill covers data binding, drag-and-drop, node customization, editing capabilities, and performance optimization for tree structures in WinForms.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing TreeViews in Windows Forms

## When to Use This Skill

Use this skill ALWAYS and immediately when:
- User needs to display hierarchical data in a tree structure
- Building file explorers, folder browsers, or directory navigation
- Implementing organization charts, category trees, or nested menus
- Need parent-child relationships with expandable/collapsible nodes
- Working with self-referencing data or data relations
- Need drag-and-drop reordering of tree nodes
- Implementing editable tree structures with insert/delete/rename operations
- Performance optimization needed for large tree datasets (1000+ nodes)
- User mentions: TreeView, hierarchical data, tree structure, expandable nodes, parent-child

## Component Overview

The **Syncfusion TreeViewAdv** control displays hierarchical data in a tree structure with advanced features beyond the standard Windows Forms TreeView. It provides comprehensive support for data binding, drag-and-drop, virtualization, editing, and extensive customization options.

### Key Features

- **Advanced Data Binding:** Self-referencing, data relations, object-relational binding
- **Drag-and-Drop:** Full drag-drop support with visual feedback and validation
- **Performance:** Virtualization for 20,000+ nodes with minimal delay
- **Node Customization:** Checkboxes, option buttons, images, custom styles
- **Editing Operations:** Dynamic insert, delete, rename with data source sync
- **Load on Demand:** Lazy loading of child nodes for better performance
- **Rich Appearance:** Themes, custom styles, borders, colors, fonts
- **Advanced Features:** Find/replace, history manager (undo/redo), XML persistence, printing
- **Multi-Selection:** CTRL+SHIFT key support for multiple node selection
- **Context Menus:** Associate menus with show/hide options

### Common Use Cases

- File/folder browser interfaces
- Organization hierarchy displays
- Category/subcategory navigation
- Project/task tree structures
- Settings/configuration trees
- XML/JSON data visualization
- Database table relationships
- Multi-level menu systems

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and NuGet package setup
- Adding control via Designer (Toolbox drag-drop)
- Adding control manually in C# and VB.NET
- Creating TreeViewAdv instances
- Adding nodes through NodeCollection Editor
- Adding nodes programmatically
- Basic node customization (lines, plus/minus signs)
- Assigning active nodes

### Data Binding
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Binding to self-referencing data (single table with parent-child)
- ParentMember, ChildMember, SelfRelationRootValue properties
- Binding to data relations (multiple related tables)
- Binding to object-relational data (custom objects)
- DataSource, DisplayMember, ValueMember configuration
- Synchronizing tree with data source changes

### Node Customization
📄 **Read:** [references/node-customization.md](references/node-customization.md)
- Root lines and connecting lines (ShowLines, ShowRootLines)
- Plus/Minus signs for parent nodes
- ShowPlusOnExpand for expanded state indicators
- CheckBoxes for node selection (ShowCheckBoxes)
- OptionButtons for radio-style selection
- Node-level vs control-level properties
- Images for expanded/collapsed states
- Left, right, and state image sources

### Appearance and Styling
📄 **Read:** [references/appearance-styling.md](references/appearance-styling.md)
- Border customization (BorderStyle, BorderSingle, BorderColor)
- 2D vs 3D borders (FixedSingle, Fixed3D)
- Border styles (Solid, Dashed, Dotted, Inset, Outset)
- Node appearance (font, colors, backgrounds)
- Global styles vs node-specific styles
- TreeNodeAdv customization properties
- Styles architecture overview
- Theme support and Office-like styling

### Drag and Drop
📄 **Read:** [references/drag-and-drop.md](references/drag-and-drop.md)
- Drag-drop functionality overview
- Drag-drop event handling (DragDrop, DragEnter, DragLeave, DragOver)
- ItemDrag event for initiating drag operations
- GiveFeedback and QueryContinueDrag events
- Custom drag feedback and validation
- Advanced drag-drop scenarios
- Inter-control drag-drop support

### Editing Operations
📄 **Read:** [references/editing-operations.md](references/editing-operations.md)
- Dynamic updates (insert, delete, rename)
- Synchronizing with data source
- GridGroupingControl integration
- Runtime node manipulation
- AcceptChanges pattern for data updates
- Reflecting changes bidirectionally

### Sorting
📄 **Read:** [references/sorting.md](references/sorting.md)
- Runtime sorting capabilities
- Sort methods and properties
- Custom sorting logic
- Sorting with data binding
- Performance considerations

### Load on Demand
📄 **Read:** [references/load-on-demand.md](references/load-on-demand.md)
- LoadOnDemand feature overview
- Lazy loading for performance
- BeforeExpand event handling
- Adding sub-nodes dynamically
- GetPath method for node paths
- AddSeparatorAtEnd property

### Performance Optimization
📄 **Read:** [references/performance-optimization.md](references/performance-optimization.md)
- EnableVirtualization for large datasets
- Virtualization benefits (20,000+ nodes)
- SuspendExpandRecalculate optimization
- RecalculateExpansion property
- Best practices for large trees
- Performance benchmarks

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Find and Replace functionality
- Search capabilities
- History Manager (undo/redo operations)
- Save and Load XML (persistence)
- Printing support and customization
- Context menus with show/hide options
- Multi-selection with CTRL+SHIFT keys

### ScrollBar Customization
📄 **Read:** [references/scrollbar-customization.md](references/scrollbar-customization.md)
- ScrollBar properties and configuration
- Automatic scrolling support
- Custom scrollbar appearance
- Scroll behavior configuration

## Quick Start Example

### Basic TreeView Setup

```csharp
using Syncfusion.Windows.Forms.Tools;

namespace WinFormsTreeApp
{
    public partial class Form1 : Form
    {
        private TreeViewAdv treeViewAdv1;
        
        public Form1()
        {
            InitializeComponent();
            InitializeTreeView();
        }
        
        private void InitializeTreeView()
        {
            // Create TreeViewAdv instance
            treeViewAdv1 = new TreeViewAdv();
            treeViewAdv1.Location = new System.Drawing.Point(20, 20);
            treeViewAdv1.Size = new System.Drawing.Size(300, 400);
            
            // Create nodes
            TreeNodeAdv parentNode1 = new TreeNodeAdv("Parent 1");
            TreeNodeAdv childNode1 = new TreeNodeAdv("Child 1");
            TreeNodeAdv childNode2 = new TreeNodeAdv("Child 2");
            
            // Build hierarchy
            parentNode1.Nodes.AddRange(new TreeNodeAdv[] { childNode1, childNode2 });
            
            TreeNodeAdv parentNode2 = new TreeNodeAdv("Parent 2");
            TreeNodeAdv childNode3 = new TreeNodeAdv("Child 3");
            parentNode2.Nodes.Add(childNode3);
            
            // Add root nodes
            treeViewAdv1.Nodes.AddRange(new TreeNodeAdv[] { parentNode1, parentNode2 });
            
            // Customize appearance
            treeViewAdv1.ShowLines = true;
            treeViewAdv1.ShowRootLines = true;
            treeViewAdv1.ShowPlusMinus = true;
            
            // Add to form
            this.Controls.Add(treeViewAdv1);
        }
    }
}
```

### Data Binding Example

```csharp
// Self-referencing data binding
DataTable dataTable = CreateHierarchicalData();

treeViewAdv1.DataSource = dataTable;
treeViewAdv1.DisplayMember = "Name";
treeViewAdv1.ValueMember = "ID";
treeViewAdv1.ParentMember = "ParentID";
treeViewAdv1.ChildMember = "ID";
treeViewAdv1.SelfRelationRootValue = DBNull.Value;
```

## Common Patterns

### Pattern 1: Programmatic Node Creation

**When:** Building tree structure dynamically from code

```csharp
// Create nodes with constructor
TreeNodeAdv node = new TreeNodeAdv("Node Text");

// Set properties
node.Text = "Updated Text";
node.ShowCheckBox = true;
node.Tag = customDataObject;

// Add children
node.Nodes.Add(new TreeNodeAdv("Child"));

// Add to tree
treeViewAdv1.Nodes.Add(node);
```

### Pattern 2: Self-Referencing Data Binding

**When:** Binding to single table with parent-child relationships

```csharp
// Setup data source
treeViewAdv1.DataSource = employeeTable;
treeViewAdv1.DisplayMember = "EmployeeName";
treeViewAdv1.ValueMember = "EmployeeID";
treeViewAdv1.ParentMember = "ManagerID";
treeViewAdv1.ChildMember = "EmployeeID";
treeViewAdv1.SelfRelationRootValue = DBNull.Value; // Root nodes have null parent
```

### Pattern 3: Load on Demand

**When:** Working with large datasets, need lazy loading

```csharp
// Enable load on demand
treeViewAdv1.LoadOnDemand = true;

// Handle BeforeExpand to load children
treeViewAdv1.BeforeExpand += (sender, e) => 
{
    TreeNodeAdv node = e.Node;
    
    // Check if children already loaded
    if (node.Nodes.Count == 0)
    {
        // Load children from data source
        var children = LoadChildNodesFromDatabase(node.Tag);
        
        foreach (var child in children)
        {
            TreeNodeAdv childNode = new TreeNodeAdv(child.Name);
            childNode.Tag = child;
            node.Nodes.Add(childNode);
        }
    }
};
```

### Pattern 4: Drag-Drop Node Reordering

**When:** Users need to reorder nodes via drag-drop

```csharp
// Enable drag-drop
treeViewAdv1.AllowDrop = true;

// Handle ItemDrag
treeViewAdv1.ItemDrag += (sender, e) => 
{
    if (e.Item is TreeNodeAdv node)
    {
        treeViewAdv1.DoDragDrop(node, DragDropEffects.Move);
    }
};

// Handle DragDrop
treeViewAdv1.DragDrop += (sender, e) => 
{
    TreeNodeAdv sourceNode = (TreeNodeAdv)e.Data.GetData(typeof(TreeNodeAdv));
    TreeNodeAdv targetNode = treeViewAdv1.GetNodeAtPoint(treeViewAdv1.PointToClient(new Point(e.X, e.Y)));
    
    if (targetNode != null && sourceNode != targetNode)
    {
        sourceNode.Remove();
        targetNode.Nodes.Add(sourceNode);
        targetNode.Expand();
    }
};
```

### Pattern 5: Performance Optimization for Large Trees

**When:** Working with 1000+ nodes, experiencing slow load times

```csharp
// Enable virtualization
treeViewAdv1.EnableVirtualization = true;

// Optimize expand/collapse
treeViewAdv1.SuspendExpandRecalculate = true;
treeViewAdv1.RecalculateExpansion = false;

// Suspend layout during bulk operations
treeViewAdv1.BeginUpdate();
try
{
    // Add thousands of nodes
    for (int i = 0; i < 10000; i++)
    {
        treeViewAdv1.Nodes.Add(new TreeNodeAdv($"Node {i}"));
    }
}
finally
{
    treeViewAdv1.EndUpdate();
}
```

## Key Properties

### Data Binding Properties
- `DataSource` - Data source object (DataTable, List, etc.)
- `DisplayMember` - Field for node text display
- `ValueMember` - Field for node value
- `ParentMember` - Parent ID field for self-referencing
- `ChildMember` - Child ID field for self-referencing
- `SelfRelationRootValue` - Value indicating root nodes

### Appearance Properties
- `ShowLines` - Display connecting lines between nodes
- `ShowRootLines` - Display lines between root nodes
- `ShowPlusMinus` - Display expand/collapse buttons
- `ShowCheckBoxes` - Display checkboxes on nodes
- `ShowOptionButtons` - Display option buttons (radio style)
- `BorderStyle` - Border style (None, FixedSingle, Fixed3D)

### Behavior Properties
- `LoadOnDemand` - Enable lazy loading of child nodes
- `AllowDrop` - Enable drag-drop operations
- `EnableVirtualization` - Enable virtualization for performance
- `SuspendExpandRecalculate` - Optimize expand/collapse performance
- `RecalculateExpansion` - Control dimension calculation on load

### Node Properties (TreeNodeAdv)
- `Text` - Node display text
- `Tag` - Custom data object
- `Checked` - Checkbox state
- `Expanded` - Expand/collapse state
- `ShowCheckBox` - Show checkbox for this node
- `ShowPlusMinus` - Show plus/minus for this node

## Key Events

### Selection Events
- `AfterSelect` - After node selection changes
- `BeforeSelect` - Before node selection changes
- `NodeSelected` - Node selected event

### Expand/Collapse Events
- `BeforeExpand` - Before node expands (use for load on demand)
- `AfterExpand` - After node expands
- `BeforeCollapse` - Before node collapses
- `AfterCollapse` - After node collapses

### Drag-Drop Events
- `ItemDrag` - Node drag initiated
- `DragDrop` - Item dropped on control
- `DragEnter` - Drag enters control bounds
- `DragOver` - Drag over control bounds

### Edit Events
- `BeforeEdit` - Before node edit starts
- `AfterEdit` - After node edit completes

## Common Use Cases

### Use Case 1: File Explorer

Build Windows Explorer-like interface with folders and files:
- Use load on demand for directory browsing
- Add folder/file icons via LeftImageList
- Handle double-click to open files
- Implement context menus for file operations

### Use Case 2: Organization Chart

Display company hierarchy with employees:
- Bind to employee table with self-referencing data
- Show employee photos as node images
- Add checkboxes for multi-select operations
- Implement drag-drop for reorganization

### Use Case 3: Settings Tree

Create hierarchical settings/preferences interface:
- Group settings by category in tree structure
- Use option buttons for single-choice settings
- Use checkboxes for boolean settings
- Save/load settings via XML persistence

### Use Case 4: Database Schema Visualizer

Display database tables and relationships:
- Load database schema into tree
- Show tables as parent nodes, columns as children
- Add icons to indicate data types
- Enable find/replace for schema search

### Use Case 5: XML/JSON Editor

Visual editor for hierarchical data formats:
- Parse XML/JSON into tree structure
- Enable inline editing of node values
- Implement undo/redo via History Manager
- Save changes back to XML/JSON format

## Troubleshooting

**Issue:** Nodes not appearing after data binding
- **Solution:** Verify DataSource is not null, check ParentMember/ChildMember match column names, ensure SelfRelationRootValue matches root node pattern

**Issue:** Performance slow with large datasets
- **Solution:** Enable EnableVirtualization, use LoadOnDemand for lazy loading, set SuspendExpandRecalculate = true

**Issue:** Drag-drop not working
- **Solution:** Set AllowDrop = true, implement ItemDrag and DragDrop event handlers, check DragDropEffects

**Issue:** Changes not reflecting in bound data source
- **Solution:** Call AcceptChanges() on DataTable after modifications, verify DataSource binding is active

**Issue:** Plus/minus signs not showing for parent nodes
- **Solution:** Verify ShowPlusMinus = true, check nodes have children, for LoadOnDemand ensure ShowPlusOnExpand is configured
