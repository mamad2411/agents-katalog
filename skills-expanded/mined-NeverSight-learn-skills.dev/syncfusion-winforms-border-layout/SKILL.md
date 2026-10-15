---
name: syncfusion-winforms-border-layout
description: "Implement Syncfusion Windows Forms BorderLayout to arrange child controls along borders (North, South, East, West) and center. Use this when working with BorderLayout, positioning controls in border regions, using docking alternatives, or configuring container layout and control spacing in Windows Forms applications."
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion Windows Forms BorderLayout

BorderLayout is a Windows Forms layout manager that allows you to arrange and layout child controls along the borders (North, South, East, West) to the center, similar to .NET framework's built-in docking support. Unlike automatic layout managers, BorderLayout gives you explicit control over positioning.

## When to Use This Skill

- **Layout with border regions**: When you need to arrange controls along borders and a center area
- **Top/bottom headers/footers**: When you want a fixed header (North) and footer (South) with content in between
- **Left/right sidebars**: When you need a sidebar panel on the left or right with main content in the center
- **Spacing control**: When you need precise spacing between controls using HGap and VGap
- **Designer or code-based layouts**: Whether building UI in designer or programmatically in C#/VB.NET
- **Alternative to docking**: When you want a more structured approach than Windows Forms docking

## Component Overview

**Key Features:**
- **5-position layout**: North, South, East, West, Center positions for child controls
- **Spacing configuration**: Customize horizontal (HGap) and vertical (VGap) gaps between controls
- **Designer support**: Add BorderLayout and child controls via Visual Studio designer
- **Code-based creation**: Programmatically create and configure BorderLayout in C# or VB.NET
- **Container control**: Set any control (typically a Form) as the container for BorderLayout

## Documentation Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Assembly and NuGet package setup
- Creating BorderLayout in designer
- Creating BorderLayout via code (C# and VB.NET)
- Adding child controls
- Container setup

### Positioning Controls
📄 **Read:** [references/positioning-controls.md](references/positioning-controls.md)
- Setting control positions (North, South, East, West, Center)
- SetPosition() method usage
- BorderPosition enumeration
- Multiple controls at the same position
- Code examples for each position
- Common position configurations

### Spacing Configuration
📄 **Read:** [references/spacing-configuration.md](references/spacing-configuration.md)
- HGap property (horizontal spacing)
- VGap property (vertical spacing)
- Setting spacing in designer
- Setting spacing in code (C# and VB.NET)
- Responsive spacing patterns

### Layout Patterns
📄 **Read:** [references/layout-patterns.md](references/layout-patterns.md)
- Common layouts (header/footer, sidebars, multi-panel)
- Best practices and patterns
- Responsive considerations
- When to use BorderLayout vs other approaches
- Complete working examples

## Quick Start

Here's a minimal BorderLayout setup:

```csharp
using Syncfusion.Windows.Forms.Tools;

// In your form
BorderLayout borderLayout1 = new BorderLayout();
this.borderLayout1.ContainerControl = this;

// Add controls
ButtonAdv topButton = new ButtonAdv() { Text = "Header", Dock = DockStyle.Top };
ButtonAdv leftButton = new ButtonAdv() { Text = "Sidebar", Dock = DockStyle.Left };
ButtonAdv centerButton = new ButtonAdv() { Text = "Content", Dock = DockStyle.Fill };

this.Controls.Add(topButton);
this.Controls.Add(leftButton);
this.Controls.Add(centerButton);

// Set positions
borderLayout1.SetPosition(topButton, BorderPosition.North);
borderLayout1.SetPosition(leftButton, BorderPosition.West);
borderLayout1.SetPosition(centerButton, BorderPosition.Center);

// Configure spacing
borderLayout1.HGap = 10;
borderLayout1.VGap = 10;
```

**VB.NET Equivalent:**
```vb
Imports Syncfusion.Windows.Forms.Tools

' In your form
Dim borderLayout1 As BorderLayout = New BorderLayout()
Me.borderLayout1.ContainerControl = Me

' Add controls
Dim topButton As ButtonAdv = New ButtonAdv() With {.Text = "Header", .Dock = DockStyle.Top}
Dim leftButton As ButtonAdv = New ButtonAdv() With {.Text = "Sidebar", .Dock = DockStyle.Left}
Dim centerButton As ButtonAdv = New ButtonAdv() With {.Text = "Content", .Dock = DockStyle.Fill}

Me.Controls.Add(topButton)
Me.Controls.Add(leftButton)
Me.Controls.Add(centerButton)

' Set positions
borderLayout1.SetPosition(topButton, BorderPosition.North)
borderLayout1.SetPosition(leftButton, BorderPosition.West)
borderLayout1.SetPosition(centerButton, BorderPosition.Center)

' Configure spacing
borderLayout1.HGap = 10
borderLayout1.VGap = 10
```

## Common Patterns

### Pattern 1: Header + Content + Footer
The most common layout with fixed header, scrollable content area, and fixed footer.

```csharp
// Create panels for header, content, footer
Panel headerPanel = new Panel() { Height = 50 };
Panel contentPanel = new Panel();
Panel footerPanel = new Panel() { Height = 40 };

// Add to form
this.Controls.Add(headerPanel);
this.Controls.Add(contentPanel);
this.Controls.Add(footerPanel);

// Position with BorderLayout
borderLayout1.SetPosition(headerPanel, BorderPosition.North);
borderLayout1.SetPosition(footerPanel, BorderPosition.South);
borderLayout1.SetPosition(contentPanel, BorderPosition.Center);
```

### Pattern 2: Sidebar + Content
Left sidebar with main content area.

```csharp
// Create sidebar and content panels
Panel sidebarPanel = new Panel() { Width = 200 };
Panel contentPanel = new Panel();

this.Controls.Add(sidebarPanel);
this.Controls.Add(contentPanel);

// Position
borderLayout1.SetPosition(sidebarPanel, BorderPosition.West);
borderLayout1.SetPosition(contentPanel, BorderPosition.Center);
```

### Pattern 3: Multi-Edge Layout
Controls on multiple edges with center content.

```csharp
Panel top = new Panel() { Height = 40 };
Panel bottom = new Panel() { Height = 40 };
Panel left = new Panel() { Width = 150 };
Panel right = new Panel() { Width = 150 };
Panel center = new Panel();

this.Controls.Add(top);
this.Controls.Add(bottom);
this.Controls.Add(left);
this.Controls.Add(right);
this.Controls.Add(center);

borderLayout1.SetPosition(top, BorderPosition.North);
borderLayout1.SetPosition(bottom, BorderPosition.South);
borderLayout1.SetPosition(left, BorderPosition.West);
borderLayout1.SetPosition(right, BorderPosition.East);
borderLayout1.SetPosition(center, BorderPosition.Center);
```

## Key Properties

| Property | Type | Description |
|----------|------|-------------|
| `ContainerControl` | Control | The control that acts as the container for BorderLayout |
| `HGap` | int | Horizontal spacing between controls |
| `VGap` | int | Vertical spacing between controls |

## Key Methods

| Method | Parameters | Description |
|--------|-----------|-------------|
| `SetPosition()` | Control, BorderPosition | Sets the border position for a child control |

## Supported Positions (BorderPosition enum)

- `North` - Top of the layout
- `South` - Bottom of the layout
- `East` - Right side of the layout
- `West` - Left side of the layout
- `Center` - Center area (fills remaining space)
