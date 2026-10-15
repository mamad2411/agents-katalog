---
name: syncfusion-winforms-grid-layout
description: Implement grid-based layout management in Windows Forms using GridLayout component. Arrange child controls in rows and columns with configurable spacing and control participation.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing GridLayout in Windows Forms

GridLayout is a layout manager that automatically arranges child controls in a grid structure containing rows and columns. Use this skill when you need to organize multiple controls in a structured grid format with precise spacing control.

## When to Use This Skill

- Arranging child controls in grid-based layouts
- Creating uniform row and column structures
- Controlling horizontal and vertical spacing between controls
- Dynamically including or excluding controls from layout
- Programmatic or designer-based control arrangement

## Component Overview

GridLayout provides:
- **Grid Structure**: Automatic arrangement in rows and columns
- **Spacing Control**: Horizontal (HGap) and vertical (VGap) gap configuration
- **Control Participation**: Include or exclude controls from layout management
- **Dynamic Configuration**: Rows and columns can be set programmatically

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Assembly deployment and NuGet setup
- Creating GridLayout through designer or code
- Adding child controls to the layout
- Basic implementation patterns

### Rows and Columns Configuration
📄 **Read:** [references/rows-and-columns-configuration.md](references/rows-and-columns-configuration.md)
- Setting number of rows and columns
- Understanding Rows property precedence
- Auto-sizing behavior based on child control count
- Grid division strategies

### Spacing and Gaps
📄 **Read:** [references/spacing-and-gaps.md](references/spacing-and-gaps.md)
- Configuring horizontal gaps (HGap)
- Configuring vertical gaps (VGap)
- Spacing calculations and effects
- Common spacing patterns

### Managing Child Controls
📄 **Read:** [references/managing-child-controls.md](references/managing-child-controls.md)
- ParticipateInLayout property overview
- Adding or removing controls from layout
- Checking control layout participation
- Rearranging controls at design time

## Quick Start Example

```csharp
using Syncfusion.Windows.Forms.Tools;

// Create GridLayout instance
GridLayout gridLayout1 = new GridLayout();
gridLayout1.ContainerControl = this;

// Configure grid structure
gridLayout1.Rows = 2;
gridLayout1.Columns = 2;

// Set spacing
gridLayout1.HGap = 10;
gridLayout1.VGap = 10;

// Add child controls
ButtonAdv button1 = new ButtonAdv() { Text = "Button 1" };
ButtonAdv button2 = new ButtonAdv() { Text = "Button 2" };

this.Controls.Add(button1);
this.Controls.Add(button2);

// Include controls in layout
gridLayout1.SetParticipateInLayout(button1, true);
gridLayout1.SetParticipateInLayout(button2, true);
```

## Key Configuration Properties

| Property | Type | Purpose |
|----------|------|---------|
| **Rows** | int | Specifies number of rows in the grid (dictates columns if set) |
| **Columns** | int | Specifies number of columns (used when Rows is null or negative) |
| **HGap** | int | Horizontal spacing between controls and layout border |
| **VGap** | int | Vertical spacing between controls and layout border |
| **ContainerControl** | Control | The form or container that holds the layout manager |

## Common Patterns

### Pattern 1: Single Column Layout
```csharp
gridLayout1.Rows = null;  // Let rows auto-calculate
gridLayout1.Columns = 1;
```
Useful for vertical stacking of controls.

### Pattern 2: Grid with Uniform Spacing
```csharp
gridLayout1.Rows = 3;
gridLayout1.Columns = 3;
gridLayout1.HGap = 5;
gridLayout1.VGap = 5;
```
Creates 3x3 grid with 5-pixel spacing.

### Pattern 3: Conditional Control Visibility
```csharp
// Hide a control from layout without removing it
gridLayout1.SetParticipateInLayout(controlToHide, false);
```
Allows dynamic layout adjustments without removing controls.
