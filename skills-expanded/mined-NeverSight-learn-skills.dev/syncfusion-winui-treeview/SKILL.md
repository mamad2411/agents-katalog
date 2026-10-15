---
name: syncfusion-winui-treeview
description: Comprehensive guide for implementing Syncfusion WinUI TreeView (SfTreeView) control in desktop applications. Use this skill when working with hierarchical data display, tree structures, or node-based navigation. Covers TreeView implementation for file explorers, organization charts, category browsers, and expandable/collapsible data visualization in WinUI applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing WinUI TreeView

Comprehensive guide for implementing the Syncfusion® WinUI TreeView (SfTreeView) control to display hierarchical data in Windows App SDK applications.

## When to Use This Skill

Use this skill when you need to:
- **Display hierarchical data** in a tree structure (files, folders, categories)
- **Implement file explorers** or folder browsers in WinUI applications
- **Create organization charts** or reporting structures
- **Build category navigation** with expandable/collapsible nodes
- **Enable node selection** with single or multiple selection modes
- **Support inline editing** of tree nodes
- **Implement drag-and-drop** for node reordering or moving
- **Load data on demand** for large hierarchies
- **Customize tree appearance** with templates and styling
- **Handle CRUD operations** on hierarchical data

The TreeView control excels at visualizing parent-child relationships and nested data structures.

## Component Overview

The **SfTreeView** is a data-oriented control that displays data in a hierarchical structure with expanding and collapsing nodes. It's commonly used to illustrate folder structures, organizational hierarchies, or nested relationships.

### Key Capabilities

- **Dual Data Modes:** Bound mode (data binding) and Unbound mode (manual nodes)
- **Flexible Selection:** Multiple selection modes including Extended with keyboard modifiers
- **Inline Editing:** Edit node content with custom templates
- **Drag-and-Drop:** Reorder or move nodes within the tree
- **Load on Demand:** Lazy load child nodes when parent expands
- **Checkboxes:** Built-in checkbox support for multi-selection
- **Context Menus:** Add flyout menus for node operations
- **Animations:** Smooth expand/collapse animations
- **MVVM Support:** Full command and data binding support
- **Customization:** Complete control over appearance with templates

### When to Choose TreeView

Choose TreeView when you need:
- **Hierarchical visualization** of parent-child data
- **Expandable/collapsible sections** for space-efficient display
- **Multiple levels of nesting** (2+ levels deep)
- **Tree navigation** patterns familiar to users

Consider alternatives for:
- **Flat lists** → Use ListView or DataGrid
- **Simple grouped data** → Use ListView with grouping
- **Network/graph relationships** → Use custom visualization

## Documentation and Navigation Guide

### Getting Started

📄 **Read:** [references/getting-started.md](references/getting-started.md)

Start here for initial setup and your first TreeView:
- Installing NuGet package (Syncfusion.TreeView.WinUI)
- Adding TreeView to XAML pages
- Basic TreeView implementation with unbound nodes
- Simple bound mode example with hierarchical data
- Namespace imports and control initialization
- Project configuration

### Data Management

📄 **Read:** [references/data-binding.md](references/data-binding.md)

Learn how to bind TreeView to your data models:
- Bound vs Unbound modes comparison
- Hierarchical data source binding with ItemsSource
- ChildPropertyName for self-relational binding
- HierarchyPropertyDescriptors for complex hierarchies
- ItemTemplate and ExpanderTemplate configuration
- ObservableCollection and INotifyPropertyChanged
- NodePopulationMode (OnDemand vs Instant)
- NotificationSubscriptionMode for change tracking

📄 **Read:** [references/drag-drop-crud.md](references/drag-drop-crud.md)

Master node manipulation and CRUD operations:
- Enabling drag-and-drop (AllowDragging, AllowDrop)
- Drag-drop events and customization
- Adding nodes programmatically
- Deleting nodes from hierarchy
- Updating node content
- Load on demand implementation
- Context menu operations

### User Interaction Features

📄 **Read:** [references/selection.md](references/selection.md)

Implement node selection functionality:
- SelectionMode options (None, Single, SingleDeselect, Multiple, Extended)
- UI selection with mouse and touch
- Programmatic selection (SelectedItem, SelectedItems)
- Selection events (SelectionChanging, SelectionChanged)
- Keyboard navigation for selection
- Multi-selection with Ctrl/Shift modifiers
- Selection customization and styling

📄 **Read:** [references/expand-collapse.md](references/expand-collapse.md)

Control node expansion and collapse:
- AutoExpandMode options
- Programmatic expand and collapse
- ExpandAction configuration (single/double tap)
- IsExpanded property usage
- Expand/collapse events
- Expand all and collapse all scenarios
- Maintaining expansion state

📄 **Read:** [references/editing.md](references/editing.md)

Enable inline editing of tree nodes:
- Enabling editing with AllowEditing
- EditTemplate and EditTemplateSelector
- Initiating edit mode (F2 key)
- Committing and canceling edits
- Edit events (ItemBeginEdit, ItemEndEdit)
- Validation during editing
- Bound vs unbound mode editing differences

📄 **Read:** [references/interactivity.md](references/interactivity.md)

Add interactive features to your TreeView:
- Checkbox support and configuration
- Context flyout menus
- Interactive events (ItemTapped, ItemDoubleTapped, ItemHolding)
- Keyboard shortcuts and navigation
- Touch gestures
- Scrolling behavior
- Animation settings (IsAnimationEnabled)

### Advanced Features

📄 **Read:** [references/mvvm-patterns.md](references/mvvm-patterns.md)

Implement MVVM architecture with TreeView:
- MVVM patterns for hierarchical data
- Commands in TreeView
- Data binding best practices
- ViewModel design for tree structures
- Handling ObservableCollections
- Event to command conversions
- Unit testing TreeView ViewModels

### Customization

📄 **Read:** [references/appearance-customization.md](references/appearance-customization.md)

Customize the visual appearance:
- ItemTemplate for node content
- ExpanderTemplate for expand/collapse icons
- Item height customization (ItemHeight, QueryNodeSize)
- TreeLines configuration
- Indentation and spacing
- Adding icons and images
- Styling selected/hover states
- Theme integration

## Quick Start Example

Here's a minimal TreeView showing a file structure:

**XAML:**
```xml
<Page xmlns:treeView="using:Syncfusion.UI.Xaml.TreeView">
    
    <Page.DataContext>
        <local:FileViewModel />
    </Page.DataContext>
    
    <treeView:SfTreeView x:Name="treeView"
                          Width="400"
                          Height="500"
                          ChildPropertyName="SubFiles"
                          ItemsSource="{Binding Files}">
        <treeView:SfTreeView.ItemTemplate>
            <DataTemplate>
                <StackPanel Orientation="Horizontal">
                    <TextBlock Text="📁" Margin="0,0,5,0" />
                    <TextBlock Text="{Binding FileName}" 
                               VerticalAlignment="Center" />
                </StackPanel>
            </DataTemplate>
        </treeView:SfTreeView.ItemTemplate>
    </treeView:SfTreeView>
    
</Page>
```

**ViewModel (C#):**
```csharp
public class FileViewModel : INotifyPropertyChanged
{
    public ObservableCollection<FileNode> Files { get; set; }
    
    public FileViewModel()
    {
        Files = new ObservableCollection<FileNode>
        {
            new FileNode 
            { 
                FileName = "Documents",
                SubFiles = new ObservableCollection<FileNode>
                {
                    new FileNode { FileName = "Resume.docx" },
                    new FileNode { FileName = "CoverLetter.pdf" }
                }
            },
            new FileNode 
            { 
                FileName = "Downloads",
                SubFiles = new ObservableCollection<FileNode>()
            }
        };
    }
    
    public event PropertyChangedEventHandler PropertyChanged;
}

public class FileNode : INotifyPropertyChanged
{
    private string _fileName;
    private ObservableCollection<FileNode> _subFiles;
    
    public string FileName
    {
        get => _fileName;
        set { _fileName = value; OnPropertyChanged(); }
    }
    
    public ObservableCollection<FileNode> SubFiles
    {
        get => _subFiles;
        set { _subFiles = value; OnPropertyChanged(); }
    }
    
    public event PropertyChangedEventHandler PropertyChanged;
    
    protected void OnPropertyChanged([CallerMemberName] string name = null)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
    }
}
```

## Common Patterns

### Pattern 1: File Explorer with Icons

```xml
<treeView:SfTreeView ItemsSource="{Binding Items}"
                      ChildPropertyName="Children">
    <treeView:SfTreeView.ItemTemplate>
        <DataTemplate>
            <StackPanel Orientation="Horizontal">
                <FontIcon Glyph="{Binding Icon}" 
                          FontSize="16" 
                          Margin="0,0,8,0" />
                <TextBlock Text="{Binding Name}" />
            </StackPanel>
        </DataTemplate>
    </treeView:SfTreeView.ItemTemplate>
</treeView:SfTreeView>
```

### Pattern 2: Multiple Selection with Checkboxes

```xml
<treeView:SfTreeView SelectionMode="Multiple"
                      CheckBoxMode="Recursive">
    <!-- When parent checked, all children auto-check -->
</treeView:SfTreeView>
```

### Pattern 3: Load on Demand

```xml
<treeView:SfTreeView LoadOnDemand="True"
                      LoadOnDemandCommand="{Binding LoadChildrenCommand}">
    <!-- Children load only when node expands -->
</treeView:SfTreeView>
```

### Pattern 4: Programmatic Selection

```csharp
// Single selection
treeView.SelectedItem = viewModel.RootNode.Children[0];

// Multiple selection
treeView.SelectedItems.Add(node1);
treeView.SelectedItems.Add(node2);

// Select all nodes
treeView.SelectAll();
```

### Pattern 5: Context Menu Operations

```xml
<treeView:SfTreeView ItemHolding="OnItemHolding">
    <!-- Show context menu on right-click/long-press -->
</treeView:SfTreeView>
```

```csharp
private void OnItemHolding(object sender, ItemHoldingEventArgs e)
{
    var flyout = new MenuFlyout();
    flyout.Items.Add(new MenuFlyoutItem { Text = "Rename" });
    flyout.Items.Add(new MenuFlyoutItem { Text = "Delete" });
    flyout.ShowAt(e.Element);
}
```

## Key Properties and Methods

### Essential Properties

| Property | Type | Description |
|----------|------|-------------|
| **ItemsSource** | object | Hierarchical data collection to bind |
| **ChildPropertyName** | string | Property name containing child items |
| **SelectionMode** | SelectionMode | Selection behavior (None, Single, Multiple, Extended) |
| **SelectedItem** | object | Currently selected item |
| **SelectedItems** | ObservableCollection | Collection of selected items |
| **AllowEditing** | bool | Enable inline editing |
| **AllowDragging** | bool | Enable drag-and-drop |
| **AutoExpandMode** | AutoExpandMode | Auto-expand behavior (None, AllNodes, RootNodes) |
| **IsAnimationEnabled** | bool | Enable expand/collapse animations |
| **CheckBoxMode** | CheckBoxMode | Checkbox behavior (None, Recursive) |
| **LoadOnDemand** | bool | Enable lazy loading of child nodes |

### Key Methods

| Method | Description |
|--------|-------------|
| **ExpandAll()** | Expands all nodes in the tree |
| **CollapseAll()** | Collapses all nodes |
| **ExpandNode(TreeViewNode)** | Expands specific node |
| **CollapseNode(TreeViewNode)** | Collapses specific node |
| **SelectAll()** | Selects all nodes |
| **ClearSelection()** | Clears all selections |
| **BringIntoView(TreeViewNode)** | Scrolls to make node visible |

### Important Events

| Event | Description |
|-------|-------------|
| **SelectionChanged** | Fired when selection changes |
| **ItemTapped** | Fired when node is tapped |
| **ItemDoubleTapped** | Fired when node is double-tapped |
| **NodeExpanding** | Fired before node expands |
| **NodeExpanded** | Fired after node expands |
| **NodeCollapsing** | Fired before node collapses |
| **NodeCollapsed** | Fired after node collapses |
| **ItemBeginEdit** | Fired when editing starts |
| **ItemEndEdit** | Fired when editing ends |

## Common Use Cases

### Use Case 1: File System Browser

Display computer folders and files with expand/collapse, file icons, and context menu operations (rename, delete, copy).

**When to use:** Document management, file pickers, asset browsers

**Key features needed:**
- Bound mode with hierarchical data
- Custom ItemTemplate with icons
- Context flyout menus
- Drag-and-drop for moving files

### Use Case 2: Organization Chart

Show company hierarchy with departments, teams, and employees with selection to view details.

**When to use:** HR applications, org visualization, reporting structures

**Key features needed:**
- Bound mode with employee data
- AutoExpandMode for initial display
- Single selection mode
- Custom templates for employee cards

### Use Case 3: Product Category Browser

E-commerce category navigation with expandable categories and subcategories.

**When to use:** E-commerce, content management, product catalogs

**Key features needed:**
- Load on demand for large catalogs
- Single selection
- Custom styling for categories
- Click events for navigation

### Use Case 4: Settings Panel

Hierarchical settings interface with grouped options and expandable sections.

**When to use:** Application settings, preferences UI, configuration panels

**Key features needed:**
- Unbound mode with manual nodes
- AutoExpandMode for convenience
- Custom ItemTemplate for settings controls
- Maintain expansion state

### Use Case 5: Project Explorer (IDE-like)

Display solution structure with projects, folders, and files similar to Visual Studio.

**When to use:** Developer tools, IDEs, code editors

**Key features needed:**
- Bound mode with solution model
- Inline editing for renaming
- Drag-drop for reorganizing
- Context menus for file operations
- Multiple selection for batch operations

## Performance Tips

- Use **OnDemand** NodePopulationMode for large hierarchies (1000+ nodes)
- Set **NotificationSubscriptionMode** to CollectionChanged only if needed
- Use **x:Bind** instead of Binding for better performance
- Minimize complexity in ItemTemplate
- Use **LoadOnDemand** for deep hierarchies with many children
- Consider virtualization for very large flat sections

## Troubleshooting Quick Reference

| Issue | Solution |
|-------|----------|
| Nodes not expanding | Check ChildPropertyName matches property name exactly |
| Selection not working | Set SelectionMode to Single or Multiple |
| Data not updating | Implement INotifyPropertyChanged on data models |
| Children not loading | Set NotificationSubscriptionMode to CollectionChanged |
| Poor performance | Enable OnDemand mode and LoadOnDemand |
| Editing not enabled | Set AllowEditing="True" and define EditTemplate |
| Drag-drop not working | Set both AllowDragging and AllowDrop to true |

## Related Components

- **ListView** - For flat lists without hierarchy
- **DataGrid** - For tabular data with hierarchy support (TreeGrid)
- **Expander** - For simple expand/collapse sections

---

**Next Steps:** Read the reference documentation linked above based on your specific needs. Start with `getting-started.md` if you're new to TreeView.
