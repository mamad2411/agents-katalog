---
name: syncfusion-winforms-splitcontainer
description: Implement Syncfusion SplitContainerAdv control for creating resizable panel layouts separated by a splitter in Windows Forms applications. Use this when building split-view interfaces, multi-pane layouts, or resizable container controls. Covers panel orientation and sizing, splitter appearance customization, container styling, splitter movement events, horizontal/vertical layouts, panel collapsing, and nested containers.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing SplitContainerAdv in Windows Forms

SplitContainerAdv is a container control that enables developers to create resizable dual-panel layouts with a movable splitter bar. It's used when you need flexible panel division in forms.

## When to Use This Skill

Use this skill when you need to:
- Create a resizable split-panel layout in a Windows Forms application
- Add controls to separate panels within a container
- Allow users to resize panels by dragging the splitter
- Configure horizontal or vertical panel orientation
- Customize splitter appearance and behavior
- Collapse or expand panels dynamically
- Handle panel resize events

## Component Overview

**SplitContainerAdv** provides:
- Two resizable panels (Panel1 and Panel2) separated by a splitter
- Support for horizontal and vertical orientation
- Panel collapsing/expanding capabilities
- Rich customization of splitter appearance
- Event handling for splitter movements
- Nested container support (SplitContainerAdv within SplitContainerAdv)
- Visual styling options

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Assembly dependencies and NuGet setup
- Creating a new Windows Forms project
- Adding SplitContainerAdv via designer
- Adding SplitContainerAdv programmatically
- Adding child controls to panels
- Setting splitter orientation

### Panel Configuration
📄 **Read:** [references/panel-configuration.md](references/panel-configuration.md)
- Panel orientation (horizontal vs vertical)
- Fixed and resizable panels
- Minimum panel size constraints
- Collapsing and expanding panels at runtime
- Panel-specific properties and behavior

### Splitter Customization
📄 **Read:** [references/splitter-customization.md](references/splitter-customization.md)
- Splitter distance and positioning
- Fixed splitter configuration
- Splitter width and increment settings
- Thumbnail arrow and grip appearance
- Hover state customization
- Runtime appearance changes

### Appearance and Styling
📄 **Read:** [references/appearance-styling.md](references/appearance-styling.md)
- Background color configuration
- Foreground properties (fonts, colors)
- Border styling options
- Panel-specific appearance overrides
- Gradient and brush customization

### Events and Interactions
📄 **Read:** [references/events-handling.md](references/events-handling.md)
- SplitterMoved event handling
- SplitterMoving event handling
- Common event patterns
- Event args and data access
- Preventing splitter movement

## Quick Start Example

Basic implementation of SplitContainerAdv:

```csharp
// Create and configure SplitContainerAdv
SplitContainerAdv splitContainer = new SplitContainerAdv();
splitContainer.Dock = DockStyle.Fill;
splitContainer.Orientation = Orientation.Horizontal;
splitContainer.SplitterDistance = 150;

// Add controls to panels
Label label1 = new Label { Text = "Panel 1", Dock = DockStyle.Fill };
Label label2 = new Label { Text = "Panel 2", Dock = DockStyle.Fill };

splitContainer.Panel1.Controls.Add(label1);
splitContainer.Panel2.Controls.Add(label2);

// Add to form
this.Controls.Add(splitContainer);
```

```vb
' Create and configure SplitContainerAdv
Dim splitContainer As New SplitContainerAdv()
splitContainer.Dock = DockStyle.Fill
splitContainer.Orientation = Orientation.Horizontal
splitContainer.SplitterDistance = 150

' Add controls to panels
Dim label1 As New Label With {.Text = "Panel 1", .Dock = DockStyle.Fill}
Dim label2 As New Label With {.Text = "Panel 2", .Dock = DockStyle.Fill}

splitContainer.Panel1.Controls.Add(label1)
splitContainer.Panel2.Controls.Add(label2)

' Add to form
Me.Controls.Add(splitContainer)
```

## Common Patterns

### Pattern 1: Fixed Left Panel, Resizable Right Panel
```csharp
splitContainer.Orientation = Orientation.Vertical;
splitContainer.FixedPanel = FixedPanel.Panel1;
splitContainer.Panel1MinSize = 200;
splitContainer.SplitterDistance = 200;
```

### Pattern 2: Collapsible Panels
```csharp
splitContainer.PanelToBeCollapsed = CollapsedPanel.Panel2;
splitContainer.TogglePanelOn = TogglePanelOn.DoubleClick;
```

### Pattern 3: Vertical Layout with Equal Sizing
```csharp
splitContainer.Orientation = Orientation.Vertical;
splitContainer.SplitterDistance = splitContainer.Height / 2;
splitContainer.Panel1MinSize = 50;
splitContainer.Panel2MinSize = 50;
```

## Key Properties

| Property | Type | Purpose |
|----------|------|---------|
| `Orientation` | Orientation | Sets horizontal or vertical split (Default: Horizontal) |
| `SplitterDistance` | int | Distance from edge to splitter bar in pixels |
| `FixedPanel` | FixedPanel | Which panel remains fixed during resizing (Panel1, Panel2, or None) |
| `Panel1Collapsed` | bool | Whether Panel1 is hidden |
| `Panel2Collapsed` | bool | Whether Panel2 is hidden |
| `IsSplitterFixed` | bool | Whether splitter can be moved |
| `SplitterWidth` | int | Width of the splitter bar in pixels |
| `Panel1MinSize` | int | Minimum size for Panel1 (default: 25) |
| `Panel2MinSize` | int | Minimum size for Panel2 (default: 25) |
| `ExpandFill` | BrushInfo | Color of expand arrow fill |
| `HotGripDark` | BrushInfo | Grip color on hover |

## Quick Tips

- **Default Orientation:** Use `Orientation.Horizontal` for left-right split, `Orientation.Vertical` for top-bottom
- **Minimum Sizing:** Set `Panel1MinSize` and `Panel2MinSize` to prevent panels from collapsing too small
- **Fixed Panels:** Use `FixedPanel` to prevent resizing one side, useful for toolbars or sidebars
- **Panel Collapse:** Double-click the splitter to collapse when `TogglePanelOn = TogglePanelOn.DoubleClick`
- **Nested Containers:** Add a SplitContainerAdv to a panel of another SplitContainerAdv for complex layouts
- **Docking:** Use `Dock = DockStyle.Fill` to make the control fill its parent container
