---
name: syncfusion-winforms-flow-layout
description: Implementing FlowLayout in Windows Forms to automatically arrange child components horizontally or vertically. Use this when working with automatic control layouts, responsive form designs, or dynamic control arrangement. Covers spacing configuration, alignment modes, control constraints, and layout positioning.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion Windows Forms FlowLayout

Master the FlowLayout component to create flexible, automatic control layouts in Windows Forms applications. FlowLayout arranges child components horizontally or vertically based on available space, making it ideal for responsive form design.

## When to Use This Skill

Use this skill when you need to:
- **Arrange controls automatically** in horizontal or vertical flows
- **Manage spacing** between child controls with horizontal and vertical gaps
- **Configure alignment** for controls within layout rows or columns
- **Set up constraint-based layouts** for complex, resizable forms
- **Control layout direction** with reverse flow options
- **Enable auto-sizing** of containers based on content
- **Prevent specific controls** from participating in the layout
- **Create responsive designs** that adapt to container resizing

## Component Overview

The `FlowLayout` is a layout manager that automatically positions child controls in a single-direction flow pattern. Unlike absolute positioning, FlowLayout provides:

- **Automatic arrangement**: Controls flow horizontally or vertically with automatic wrapping
- **Flexible spacing**: Configure gaps between controls
- **Smart alignment**: Center, left/right, or constrained-based positioning
- **Responsive sizing**: Auto-height adjustment when controls overflow
- **Constraint system**: Fine-grained control over individual control placement

## Key Features

- **Layout Modes**: Horizontal (default) or vertical arrangement
- **Spacing Control**: Separate horizontal (HGap) and vertical (VGap) gaps
- **Auto-Resizing**: AutoHeight property adjusts container height automatically
- **Directional Control**: ReverseRows reverses the flow direction (RTL/BTL)
- **Alignment Options**: Center, Near, Far, or ChildConstraints-based alignment
- **Child Constraints**: Per-control HAlign, VAlign, NewLine, and proportional sizing
- **Layout Participation**: Selectively include/exclude controls from layout

## Documentation Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)

Learn assembly requirements, setup methods, and basic FlowLayout implementation:
- Assembly references and package requirements
- Designer-based and code-based setup approaches
- Setting ContainerControl property
- Adding child controls to the layout
- Selecting layout mode (Horizontal/Vertical)

**When to read:** Before implementing FlowLayout for the first time

---

### Layout Modes and Direction
📄 **Read:** [references/layout-modes.md](references/layout-modes.md)

Configure how controls flow and reverse the direction:
- LayoutMode property (Horizontal vs Vertical)
- ReverseRows property for right-to-left or bottom-to-top flow
- ParticipateInLayout method to include/exclude controls dynamically
- Switching between layout modes at runtime
- Use cases for each layout mode

**When to read:** When changing how controls are arranged or need directional control

---

### Spacing and Sizing
📄 **Read:** [references/spacing-and-sizing.md](references/spacing-and-sizing.md)

Manage gaps between controls and container auto-sizing:
- HGap property for horizontal spacing
- VGap property for vertical spacing
- AutoHeight for automatic container height adjustment
- Container behavior during overflow
- Responsive layout patterns

**When to read:** When adjusting control spacing or enabling responsive sizing

---

### Alignment Options
📄 **Read:** [references/alignment-options.md](references/alignment-options.md)

Configure control alignment and layout strategies:
- Simple alignment modes (Center, Near, Far)
- ChildConstraints-based alignment system
- When to use each alignment approach
- Switching between alignment types
- Edge cases and special scenarios

**When to read:** When centering controls, justifying rows, or using constraint-based layouts

---

### Child Control Constraints
📄 **Read:** [references/child-control-constraints.md](references/child-control-constraints.md)

Apply per-control constraints for advanced layout scenarios:
- HAlign and VAlign for individual control positioning
- Justify option with space distribution
- Active property to include/exclude specific controls
- NewLine property to force row/column breaks
- ProportionalRowHeight and ProportionalColWidth
- SetConstraints and GetConstraints methods
- Complex form layout patterns
- Rearranging controls programmatically

**When to read:** When building complex forms with varied control alignment needs

---

## Quick Start Example

```csharp
// Basic horizontal layout with buttons
using Syncfusion.Windows.Forms.Tools;

public partial class MyForm : Form
{
    private FlowLayout flowLayout1;
    
    public MyForm()
    {
        InitializeComponent();
        
        // Create and configure FlowLayout
        flowLayout1 = new FlowLayout();
        flowLayout1.ContainerControl = this;
        flowLayout1.LayoutMode = FlowLayoutMode.Horizontal;
        flowLayout1.HGap = 10;
        flowLayout1.VGap = 10;
        
        // Create buttons
        Button btn1 = new Button { Text = "Button 1", Size = new Size(80, 30) };
        Button btn2 = new Button { Text = "Button 2", Size = new Size(80, 30) };
        Button btn3 = new Button { Text = "Button 3", Size = new Size(80, 30) };
        
        // Add to form (automatically laid out)
        this.Controls.Add(btn1);
        this.Controls.Add(btn2);
        this.Controls.Add(btn3);
    }
}
```

**Result:** Three buttons arranged horizontally with 10-pixel gaps, automatically wrapping to the next row when space is limited.

## Common Patterns

### Horizontal Button Bar
```csharp
flowLayout1.LayoutMode = FlowLayoutMode.Horizontal;
flowLayout1.Alignment = FlowAlignment.Near;
flowLayout1.HGap = 5;
flowLayout1.VGap = 5;
```

### Vertical Control List
```csharp
flowLayout1.LayoutMode = FlowLayoutMode.Vertical;
flowLayout1.Alignment = FlowAlignment.Center;
flowLayout1.HGap = 10;
flowLayout1.VGap = 5;
```

### Responsive Form Layout
```csharp
flowLayout1.Alignment = FlowAlignment.ChildConstraints;
flowLayout1.AutoHeight = true;
// Set per-control constraints using SetConstraints()
```

### Right-to-Left Flow
```csharp
flowLayout1.ReverseRows = true;
flowLayout1.LayoutMode = FlowLayoutMode.Horizontal;
```

## Key Properties Reference

| Property | Type | Purpose |
|----------|------|---------|
| `LayoutMode` | FlowLayoutMode | Horizontal or Vertical arrangement |
| `Alignment` | FlowAlignment | Center, Near, Far, or ChildConstraints |
| `HGap` | int | Horizontal spacing between controls |
| `VGap` | int | Vertical spacing between controls |
| `AutoHeight` | bool | Enable automatic container height adjustment |
| `ReverseRows` | bool | Reverse flow direction (RTL/BTL) |
| `ContainerControl` | Control | The container holding child controls |

## Common Use Cases

### Data Entry Forms
Arrange input fields, labels, and buttons with automatic wrapping and constraint-based alignment for responsive form layouts.

### Tool Button Bars
Create dynamic button collections that wrap intelligently as window size changes.

### Option Panels
Organize checkboxes and radio buttons vertically with auto-sizing.

### Responsive Dashboards
Combine FlowLayout with panels to build flexible dashboard layouts that resize content intelligently.

### Configuration Dialogs
Build dialog forms with complex alignment requirements using constraint-based layouts.

---

**Next:** Choose a reference above based on your needs, or start with Getting Started for first-time implementation.
