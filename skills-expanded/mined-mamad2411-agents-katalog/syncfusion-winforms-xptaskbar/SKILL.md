---
name: syncfusion-winforms-xptaskbar
description: How to create and configure Syncfusion XPTaskBar controls in Windows Forms applications. Use this skill whenever the user needs to implement expandable task panels, create Windows XP-style task menus, build collapsible navigation panels, configure multi-box task bars, or customize task bar behavior with animations and events. Covers basic setup, box/item management, layout modes, events, customization, and spacing configuration.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing XPTaskBar in Windows Forms

## Table of Contents
- [When to Use This Skill](#when-to-use-this-skill)
- [Component Overview](#component-overview)
- [Quick Start Example](#quick-start-example)
- [Documentation Navigation Guide](#documentation-navigation-guide)
- [Common Patterns](#common-patterns)
- [Key Configuration Properties](#key-configuration-properties)

## When to Use This Skill

Use XPTaskBar when you need to:

- **Create expandable task panels** - Display command items or features in collapsible grouped boxes
- **Build Windows XP-style menus** - Recreate the classic task sidebar UI pattern
- **Organize navigation hierarchically** - Group related commands into categorized boxes
- **Implement interactive task lists** - Allow users to expand/collapse task categories with animations
- **Add custom animations and events** - Control expand/collapse behavior and respond to user interactions

## Component Overview

**XPTaskBar** is a Windows Forms control that displays command items organized within collapsible boxes, mimicking the Windows XP task sidebar. The component hierarchy includes:

- **XPTaskBar** - Main container control that can hold multiple boxes
- **XPTaskBarBox** - Collapsible section with header and items area
- **XPTaskBarItem** - Individual command items displayed within a box

### Key Features

- **Hierarchical layout** - Organize items into categorized boxes
- **Collapse/expand animation** - Smooth transitions with configurable animation speed
- **Multiple layout modes** - Vertical (default) or horizontal orientation
- **State persistence** - Remember expanded/collapsed state across sessions
- **Rich customization** - Control colors, fonts, images, and spacing
- **Event-driven** - Handle clicks, animations, and state changes
- **Child control support** - Host panels and other controls within boxes

## Quick Start Example

```csharp
using Syncfusion.Windows.Forms.Tools;

// Create XPTaskBar control
XPTaskBar xpTaskBar1 = new XPTaskBar();
xpTaskBar1.Dock = DockStyle.Fill;
this.Controls.Add(xpTaskBar1);

// Create first task box
XPTaskBarBox box1 = new XPTaskBarBox();
box1.Text = "File Operations";
xpTaskBar1.Controls.Add(box1);

// Add items to the box
box1.Items.AddRange(new XPTaskBarItem[] {
    new XPTaskBarItem("New Document", System.Drawing.Color.Empty, -1, "NewDoc"),
    new XPTaskBarItem("Open File", System.Drawing.Color.Empty, -1, "OpenFile"),
    new XPTaskBarItem("Save", System.Drawing.Color.Empty, -1, "Save")
});

// Handle item clicks
box1.ItemClick += (sender, e) => {
    switch (e.XPTaskBarItem.Tag as string) {
        case "NewDoc":
            // Handle new document
            break;
        case "OpenFile":
            // Handle file open
            break;
    }
};

// Create second task box
XPTaskBarBox box2 = new XPTaskBarBox();
box2.Text = "Editing Tools";
xpTaskBar1.Controls.Add(box2);

box2.Items.AddRange(new XPTaskBarItem[] {
    new XPTaskBarItem("Cut", System.Drawing.Color.Empty, -1, "Cut"),
    new XPTaskBarItem("Copy", System.Drawing.Color.Empty, -1, "Copy"),
    new XPTaskBarItem("Paste", System.Drawing.Color.Empty, -1, "Paste")
});
```

## Documentation Navigation Guide

Read the reference documentation in the order that matches your implementation needs:

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Assembly and package dependencies
- Adding control via designer or code
- Basic XPTaskBar, box, and item setup
- Assembly references required

### Building the Structure
📄 **Read:** [references/box-structure.md](references/box-structure.md)
- XPTaskBar box hierarchy and anatomy
- Header customization (text, font, alignment, direction)
- Collapse/expand button configuration
- Integrating child panels and controls

📄 **Read:** [references/items-and-content.md](references/items-and-content.md)
- Creating and managing XPTaskBarItems
- Working with Items collection
- Item properties and configuration
- Hosting nested controls with PreferredChildPanelHeight

### Layout and Orientation
📄 **Read:** [references/layout-orientation.md](references/layout-orientation.md)
- Vertical layout mode (default)
- Horizontal layout mode and column width
- Switching orientations dynamically
- Responsive layout behavior

### Behavior and Interactivity
📄 **Read:** [references/behavior-and-events.md](references/behavior-and-events.md)
- Animation configuration and timing
- Collapse/expand event handling
- ItemClick event with Tag-based routing
- State preservation (AutoPersistStates)
- Drag-and-drop support
- Event examples and patterns

### Appearance and Customization
📄 **Read:** [references/appearance-customization.md](references/appearance-customization.md)
- Header color and forecolor customization
- Font styling for headers
- Brush customization via ProvideHeaderBackgroundBrush and ProvideItemsBackgroundBrush events
- Adding images to headers and items
- Tooltip configuration and display
- Custom background drawing techniques

### Spacing and Scrolling
📄 **Read:** [references/padding-spacing-scrolling.md](references/padding-spacing-scrolling.md)
- XPTaskBar interior padding (DockPadding, HorizontalPadding, VerticalPadding)
- Box header padding (PADX, PADY)
- Auto-scroll behavior
- Scroll margin and minimum size configuration

## Common Patterns

### Pattern 1: Multi-Box Task Menu
Create a sidebar with multiple collapsible task categories:

```csharp
var taskBar = new XPTaskBar { VerticalLayout = true };

// Create boxes for different task categories
foreach (var category in new[] { "File", "Edit", "View", "Help" }) {
    var box = new XPTaskBarBox { Text = category };
    taskBar.Controls.Add(box);
    // Add items to box
}
```

### Pattern 2: Item Click Routing
Use the Tag property to implement event routing:

```csharp
box.ItemClick += (sender, e) => {
    var command = e.XPTaskBarItem.Tag as string;
    ExecuteCommand(command);
};
```

### Pattern 3: Stateful Persistence
Remember user preferences across sessions:

```csharp
xpTaskBar1.AutoPersistStates = true;
```

### Pattern 4: Animated State Changes
Control animation behavior during expand/collapse:

```csharp
box.AnimationDelay = 50;           // Milliseconds between frames
box.AnimationPositionsCount = 15;  // Number of animation steps
box.UseAdditionalAnimation = true; // Animate when adding/removing items
```

## Key Configuration Properties

### XPTaskBar Level

| Property | Type | Purpose |
|----------|------|---------|
| `VerticalLayout` | bool | Set true for vertical mode (default), false for horizontal |
| `ColWidthOnHorizontalAlignment` | int | Column width in horizontal layout mode |
| `HorizontalPadding` | int | Interior horizontal spacing |
| `VerticalPadding` | int | Interior vertical spacing |
| `AutoScroll` | bool | Enable automatic scrollbars when needed |
| `AutoPersistStates` | bool | Persist expanded/collapsed state between sessions |
| `AllowDrop` | bool | Enable drag-and-drop support |
| `MinimumSize` | Size | Minimum control dimensions |

### XPTaskBarBox Level

| Property | Type | Purpose |
|----------|------|---------|
| `Text` | string | Box header display text |
| `Collapsed` | bool | Set true to collapse, false to expand |
| `ShowCollapseButton` | bool | Show/hide collapse button |
| `ToggleByButton` | bool | Allow button to toggle state |
| `HeaderBackColor` | Color | Header background color |
| `HeaderForeColor` | Color | Header text color |
| `HeaderFont` | Font | Header text font |
| `HeaderTextAlign` | StringAlignment | Header text alignment |
| `AnimationDelay` | int | Delay in ms between animation frames |
| `AnimationPositionsCount` | int | Number of animation steps |
| `PreferredChildPanelHeight` | int | Height reserved for child controls |
| `ShowToolTip` | bool | Enable tooltips for items |
| `PADX` | int | Horizontal header padding |
| `PADY` | int | Vertical header padding |

### XPTaskBarItem Level

| Property | Type | Purpose |
|----------|------|---------|
| `Text` | string | Item display text |
| `ImageIndex` | int | Index in parent box's ImageList |
| `ToolTipText` | string | Tooltip text on hover |
| `Tag` | object | Custom data for event routing |

---

**Next Step:** Start with [references/getting-started.md](references/getting-started.md) to set up your first XPTaskBar control.
