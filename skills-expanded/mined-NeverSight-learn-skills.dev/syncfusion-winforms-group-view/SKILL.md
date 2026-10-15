---
name: syncfusion-winforms-group-view
description: Guide for implementing Syncfusion GroupView control in Windows Forms applications. Use when creating list controls with images, Visual Studio toolbox-style interfaces, or navigation item lists. Covers GroupViewItem collections, drag-drop item lists, highlighted selections, toolbox-style interfaces, and GroupBar client controls for OutlookBar-style interfaces.

metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing GroupView Control

The GroupView control is a list-type control for Windows Forms that displays items with text and images. It provides rich customization options for appearance, behavior, and interactive features, making it ideal for creating VS.NET toolbox-style interfaces, OutlookBar clones, and navigation panels.

## When to Use This Skill

Use this skill when you need to:
- Display a list of items with text and images in Windows Forms
- Create VS.NET toolbox-style interfaces
- Clone Microsoft OutlookBar or Visual Studio toolbox window
- Implement drag-and-drop item lists
- Build navigation panels with highlighted selections
- Add GroupView as a client control to GroupBar
- Configure item appearance, colors, and offsets
- Handle item selection, highlighting, and renaming events
- Create interactive item lists with tooltips and context menus

## Component Overview

**GroupView Control** displays a collection of GroupViewItems, each supporting:
- Text labels with formatting and highlighting
- Small and large images from ImageList
- Interactive states (selected, highlighted, selecting)
- Drag-and-drop reordering
- In-place renaming
- ToolTips and context menus
- Custom colors and offsets for various states
- Horizontal and vertical orientation

**Key Capabilities:**
- Flat or 3D appearance
- ButtonView for pressed state visualization
- FlowView for image-focused layouts
- Integrated scrolling for large item sets
- Event notifications for selection, highlighting, renaming, and reordering

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Assembly deployment (Syncfusion.Shared.Base)
- Adding GroupView via designer
- Adding GroupView via code
- Adding items to GroupViewItems collection
- Setting up ImageList for small and large images
- Configuring selected item

### Control Configuration
📄 **Read:** [references/control-settings.md](references/control-settings.md)
- Appearance settings (FlatLook, BorderStyle)
- Drag-and-drop behavior
- Spacing between items and borders
- Integrated scrolling
- Orientation and FlowView modes

### Item Customization
📄 **Read:** [references/item-customization.md](references/item-customization.md)
- Text highlighting, offset, and formatting
- Color settings for items and text (highlight, selection states)
- Image highlighting, offset, and spacing
- In-place renaming functionality

### Interactive Features
📄 **Read:** [references/interactive-features.md](references/interactive-features.md)
- ButtonView and ClipSelectionBounds
- ToolTips configuration
- Context menu implementation
- Selection behavior

### Events
📄 **Read:** [references/events.md](references/events.md)
- GroupViewItemSelected event
- GroupViewItemHighlighted event
- GroupViewItemRenamed event
- GroupViewItemsReordered event
- GroupViewItemDoubleClick event
- ShowContextMenu event

### GroupBar Integration
📄 **Read:** [references/groupbar-integration.md](references/groupbar-integration.md)
- Adding GroupView to GroupBar
- Creating VS.NET toolbox interface
- Client control attachment

## Quick Start

### Basic GroupView Setup

```csharp
using Syncfusion.Windows.Forms.Tools;

public class MyForm : Form
{
    private GroupView groupView1;
    private ImageList imageList1;
    
    public MyForm()
    {
        InitializeComponent();
        
        // Create GroupView
        this.groupView1 = new GroupView();
        this.groupView1.Location = new Point(10, 10);
        this.groupView1.Size = new Size(200, 300);
        this.groupView1.FlatLook = true;
        
        // Setup ImageList
        this.imageList1 = new ImageList();
        this.imageList1.Images.Add(Image.FromFile("icon1.png"));
        this.imageList1.Images.Add(Image.FromFile("icon2.png"));
        this.imageList1.Images.Add(Image.FromFile("icon3.png"));
        
        // Assign ImageList
        this.groupView1.SmallImageList = this.imageList1;
        this.groupView1.SmallImageView = true;
        
        // Add items
        this.groupView1.GroupViewItems.AddRange(new GroupViewItem[] {
            new GroupViewItem("My Computer", 0, true, null, "Item0"),
            new GroupViewItem("Network", 1, true, null, "Item1"),
            new GroupViewItem("Recycle Bin", 2, true, null, "Item2")
        });
        
        // Handle selection event
        this.groupView1.GroupViewItemSelected += GroupView1_ItemSelected;
        
        // Add to form
        this.Controls.Add(this.groupView1);
    }
    
    private void GroupView1_ItemSelected(object sender, EventArgs e)
    {
        int selectedIndex = this.groupView1.SelectedItem;
        string selectedText = this.groupView1.GroupViewItems[selectedIndex].Text;
        MessageBox.Show($"Selected: {selectedText}");
    }
}
```

### VS.NET Toolbox-Style Interface

```csharp
// Create toolbox-style GroupView
this.groupView1.FlatLook = true;
this.groupView1.FlowView = true;
this.groupView1.ShowFlowViewItemText = true;
this.groupView1.IntegratedScrolling = true;
this.groupView1.SmallImageView = true;
this.groupView1.AllowDragDrop = true;

// Configure highlighting
this.groupView1.HighlightText = true;
this.groupView1.HighlightImage = true;
this.groupView1.HighlightItemColor = Color.LightBlue;
this.groupView1.HighlightTextColor = Color.DarkBlue;
```

## Common Patterns

### Pattern 1: Adding Items Dynamically

```csharp
// Add single item
GroupViewItem newItem = new GroupViewItem(
    text: "New Item",
    imageIndex: 3,
    visible: true,
    toolTipText: null,
    name: "NewItem1"
);
this.groupView1.GroupViewItems.Add(newItem);

// Add multiple items
this.groupView1.GroupViewItems.AddRange(new GroupViewItem[] {
    new GroupViewItem("Item 1", 0, true, null, "Item1"),
    new GroupViewItem("Item 2", 1, true, null, "Item2"),
    new GroupViewItem("Item 3", 2, true, null, "Item3")
});
```

### Pattern 2: Configuring Highlighting and Selection

```csharp
// Enable highlighting
this.groupView1.HighlightText = true;
this.groupView1.HighlightImage = true;

// Set highlight colors
this.groupView1.HighlightItemColor = Color.LightGray;
this.groupView1.HighlightTextColor = Color.Black;

// Set selection colors
this.groupView1.SelectedItemColor = Color.Navy;
this.groupView1.SelectedTextColor = Color.White;
this.groupView1.SelectedHighlightItemColor = Color.Blue;
this.groupView1.SelectedHighlightTextColor = Color.Yellow;
```

### Pattern 3: Drag-and-Drop Configuration

```csharp
// Enable drag-and-drop
this.groupView1.AllowDragDrop = true;
this.groupView1.AllowDragAnyObject = true;

// Handle reorder event
this.groupView1.GroupViewItemsReordered += (sender, e) => {
    // Items have been reordered
    UpdateItemPositions();
};
```

### Pattern 4: In-Place Renaming

```csharp
// Enable in-place renaming for specific item
int itemIndexToRename = 2;
this.groupView1.InplaceRenameItem(itemIndexToRename);

// Handle rename event
this.groupView1.GroupViewItemRenamed += (sender, e) => {
    GroupItemRenamedEventArgs args = (GroupItemRenamedEventArgs)e;
    MessageBox.Show($"Renamed from '{args.OldLabel}' to '{args.NewLabel}'");
};
```

### Pattern 5: Context Menu Implementation

```csharp
// Handle ShowContextMenu event
this.groupView1.ShowContextMenu += GroupView1_ShowContextMenu;

private void GroupView1_ShowContextMenu(object sender, EventArgs e)
{
    ContextMenuStrip menu = new ContextMenuStrip();
    
    // Add menu items
    menu.Items.Add("Add New Item", null, AddNewItem_Click);
    menu.Items.Add("Remove Item", null, RemoveItem_Click);
    menu.Items.Add(new ToolStripSeparator());
    menu.Items.Add("Properties", null, Properties_Click);
    
    // Check if mouse is over an item
    if (this.groupView1.ContextMenuItem != -1)
    {
        menu.Items[1].Enabled = true; // Enable Remove
    }
    else
    {
        menu.Items[1].Enabled = false; // Disable Remove
    }
    
    // Show context menu
    menu.Show(this.groupView1, this.groupView1.PointToClient(Cursor.Position));
}
```

## Key Properties

### Core Properties
- **GroupViewItems** - Collection of items displayed in the control
- **SelectedItem** - Index of currently selected item
- **HighlightedItem** - Index of currently highlighted item
- **ContextMenuItem** - Index of item under mouse for context menu

### Appearance Properties
- **FlatLook** - Removes 3D edge from items
- **BorderStyle** - Border style for the control
- **SmallImageView** - Display items with small images
- **FlowView** - Display items in flow layout mode

### Behavior Properties
- **AllowDragDrop** - Enable drag-and-drop functionality
- **IntegratedScrolling** - Enable scrolling for overflow
- **Orientation** - Horizontal or Vertical item arrangement
- **ButtonView** - Display selected item in pressed state

### Image Properties
- **SmallImageList** - ImageList for small icons (16x16)
- **LargeImageList** - ImageList for large icons (32x32)
- **HighlightImage** - Enable image highlighting on hover
- **ImageSpacing** - Spacing between image edge and item edge

### Text Properties
- **HighlightText** - Enable text highlighting on hover
- **TextWrap** - Wrap long text
- **TextUnderline** - Underline item text
- **TextSpacing** - Spacing between text and other elements

### Color Properties
- **HighlightItemColor** - Color when mouse hovers over item
- **HighlightTextColor** - Text color when mouse hovers
- **SelectedItemColor** - Background color of selected item
- **SelectedTextColor** - Text color of selected item

## Common Use Cases

### Use Case 1: Navigation Panel
Display application sections with icons and text, allowing users to navigate by clicking items.

### Use Case 2: Tool Palette
Create a VS.NET toolbox-style palette where users can select tools or components from categorized lists.

### Use Case 3: File Browser
Build a file/folder browser with icons representing different file types and support for drag-and-drop operations.

### Use Case 4: Settings Menu
Display hierarchical settings categories with icons, enabling quick access to configuration options.

### Use Case 5: Dashboard Widgets
Present dashboard widget options that users can select and drag onto a canvas.

## Troubleshooting

**Issue:** Images not displaying
- Verify ImageList is assigned to SmallImageList or LargeImageList
- Ensure SmallImageView is set to true for small images
- Check that GroupViewItem.ImageIndex matches valid index in ImageList

**Issue:** Events not firing
- Verify event handlers are properly subscribed
- Check that control is added to form's Controls collection
- Ensure items exist in GroupViewItems collection

**Issue:** Drag-and-drop not working
- Set AllowDragDrop to true
- Consider AllowDragAnyObject for external objects
- Verify form allows drop operations if dragging from external source

**Issue:** Selection not visible
- Configure SelectedItemColor and SelectedTextColor
- Set ButtonView to true for pressed state visualization
- Check ClipSelectionBounds property for selection borders
