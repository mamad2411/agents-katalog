---
name: syncfusion-winforms-gradient-label
description: Implement Syncfusion WinForms GradientLabel control - an enhanced label with gradient backgrounds and custom borders. Use this when creating visually styled labels, colorful headers, or decorative text displays. Covers gradient effects, custom borders, shading configuration, and appearance customization for attractive label designs in Windows Forms applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing GradientLabel

An enhanced label control for Windows Forms that provides gradient backgrounds, attractive shading, custom borders, and visual styling capabilities for creating appealing UI labels.

## When to Use This Skill

Use this skill when you need to:
- **Gradient Labels**: Create labels with gradient backgrounds and color transitions
- **Decorative Headers**: Design visually appealing section headers and titles
- **Styled Text Display**: Implement fancy labels with custom shading and borders
- **UI Enhancement**: Add visual appeal to form labels and descriptive text
- **Custom Branding**: Create branded labels with specific color schemes
- **Informational Panels**: Build attractive informational labels with background effects

## Component Overview

The **GradientLabel** is an enhanced label control derived from the standard Windows Forms Label that provides:
- Multiple gradient styles (Horizontal, Vertical, Diagonal, PathRectangle, PathEllipse)
- Solid and pattern background options
- Customizable 3D and 2D borders
- Multi-color gradient support
- XML serialization for state persistence
- Full compatibility with standard Label functionality

**Key Capabilities:**
- Gradient background with BrushInfo class
- 6 gradient styles for different visual effects
- Pattern backgrounds with multiple styles
- Border customization (sides, styles, colors)
- Text appearance control including disabled state
- Save/load gradient settings to XML
- Inherits all standard Label features (text, font, alignment)

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)

**When to read:** Starting new implementation, setting up dependencies, first-time usage

**Topics covered:**
- Assembly deployment and NuGet packages
- Control dependencies for GradientLabel
- Adding via Visual Studio designer (toolbox drag-drop)
- Adding via code (manual instantiation)
- Basic initialization and configuration
- Simple gradient setup examples
- Namespace requirements

---

### Background Styling
📄 **Read:** [references/background-styling.md](references/background-styling.md)

**When to read:** Configuring gradients, setting colors, customizing background appearance

**Topics covered:**
- BackgroundColor property and BrushInfo class
- Brush styles (Solid, Pattern, Gradient, None)
- Gradient styles (ForwardDiagonal, BackwardDiagonal, Horizontal, Vertical, PathRectangle, PathEllipse)
- BackColor and ForeColor properties
- PatternStyle options for pattern backgrounds
- GradientColors array for multi-color gradients
- Creating custom color transitions
- Complete styling examples

---

### Border Configuration
📄 **Read:** [references/border-configuration.md](references/border-configuration.md)

**When to read:** Adding borders, customizing border styles, controlling border appearance

**Topics covered:**
- BorderSides property (Left, Top, Right, Bottom, Middle, All)
- BorderStyle options (Raised, Sunken, Flat, Etched, Bump, etc.)
- BorderColor for 2D border colors
- Border3DStyle enumeration
- FixedSingle border mode
- Selective side borders
- 3D border effects
- Complete border examples

---

### Foreground and Text Settings
📄 **Read:** [references/foreground-text-settings.md](references/foreground-text-settings.md)

**When to read:** Configuring text appearance, setting font properties, managing disabled state

**Topics covered:**
- Text property for label content
- ForeColor for text color
- DrawActiveWhenDisabled property
- Font properties inherited from Label
- Text alignment options (inherited)
- TextAlign property usage
- Disabled state appearance control
- Text visibility and styling

---

### Serialization
📄 **Read:** [references/serialization.md](references/serialization.md)

**When to read:** Saving/loading gradient settings, persisting visual state, implementing themes

**Topics covered:**
- XML serialization overview
- Saving BackgroundColor to XML files
- Loading BackgroundColor from XML files
- XmlSerializer class usage
- FileStream and XmlTextWriter implementation
- Persisting gradient state across sessions
- Theme save/load patterns
- Complete serialization examples

---

## Quick Start

### Basic Gradient Label Setup

```csharp
using Syncfusion.Windows.Forms.Tools;
using Syncfusion.Drawing;

// Create and configure GradientLabel
GradientLabel gradientLabel = new GradientLabel();
gradientLabel.Size = new Size(200, 60);
gradientLabel.Location = new Point(20, 20);

// Set gradient background (horizontal red to blue)
gradientLabel.BackgroundColor = new BrushInfo(
    GradientStyle.Horizontal,
    Color.Red,
    Color.MediumBlue
);

// Set text properties
gradientLabel.Text = "Welcome";
gradientLabel.ForeColor = Color.White;
gradientLabel.Font = new Font("Arial", 14, FontStyle.Bold);

// Add to form
this.Controls.Add(gradientLabel);
```

### With Border Styling

```csharp
// Add 3D border effect
gradientLabel.BorderStyle = Border3DStyle.Raised;
gradientLabel.BorderSides = Border3DSide.All;
```

## Common Patterns

### Pattern 1: Section Header with Vertical Gradient
```csharp
// Create attractive section header
GradientLabel header = new GradientLabel
{
    Size = new Size(300, 50),
    Location = new Point(10, 10),
    Text = "User Information",
    Font = new Font("Segoe UI", 16, FontStyle.Bold),
    TextAlign = ContentAlignment.MiddleCenter,
    ForeColor = Color.White
};

// Vertical gradient from dark to light blue
header.BackgroundColor = new BrushInfo(
    GradientStyle.Vertical,
    Color.DarkBlue,
    Color.LightSkyBlue
);

// Raised 3D border
header.BorderStyle = Border3DStyle.Raised;
```

### Pattern 2: Multi-Color Gradient Label
```csharp
// Create label with multiple gradient colors
GradientLabel colorfulLabel = new GradientLabel
{
    Size = new Size(250, 80),
    Text = "Special Offer!",
    Font = new Font("Arial", 18, FontStyle.Bold),
    ForeColor = Color.White,
    TextAlign = ContentAlignment.MiddleCenter
};

// Path rectangle gradient with 5 colors
colorfulLabel.BackgroundColor = new BrushInfo(
    GradientStyle.PathRectangle,
    new Color[]
    {
        Color.LavenderBlush,
        Color.LemonChiffon,
        Color.DarkKhaki,
        Color.SandyBrown,
        Color.LightSeaGreen
    }
);
```

### Pattern 3: Styled Status Label
```csharp
// Create status indicator label
GradientLabel statusLabel = new GradientLabel
{
    Size = new Size(150, 30),
    Text = "Active",
    TextAlign = ContentAlignment.MiddleCenter,
    ForeColor = Color.DarkGreen,
    Font = new Font("Arial", 10, FontStyle.Bold)
};

// Horizontal gradient (light green)
statusLabel.BackgroundColor = new BrushInfo(
    GradientStyle.Horizontal,
    Color.LightGreen,
    Color.PaleGreen
);

// Flat border with custom color
statusLabel.BorderStyle = Border3DStyle.Flat;
statusLabel.BorderSides = Border3DSide.All;
statusLabel.BorderColor = Color.DarkGreen;
```

## Key Properties

### Background Properties
- **BackgroundColor**: Gets/sets background color and styles using BrushInfo class
- **BackgroundColor.Style**: Brush style (Solid, Pattern, Gradient, None)
- **BackgroundColor.GradientStyle**: Gradient direction (Horizontal, Vertical, ForwardDiagonal, BackwardDiagonal, PathRectangle, PathEllipse)
- **BackgroundColor.BackColor**: Starting color for gradient
- **BackgroundColor.ForeColor**: Ending color for gradient
- **BackgroundColor.PatternStyle**: Pattern style when using Pattern mode
- **BackgroundColor.GradientColors**: Array of colors for multi-color gradients

### Border Properties
- **BorderSides**: Sides that display border (Left, Top, Right, Bottom, Middle, All)
- **BorderStyle**: 3D border style (Raised, RaisedOuter, RaisedInner, Sunken, SunkenOuter, SunkenInner, Etched, Bump, Adjust, Flat)
- **BorderColor**: Color for 2D border (effective when BorderStyle is FixedSingle)

### Text Properties (Inherited from Label)
- **Text**: Label text content
- **Font**: Font used for text display
- **ForeColor**: Text color
- **TextAlign**: Text alignment (ContentAlignment enum)
- **DrawActiveWhenDisabled**: Whether text draws normally when control is disabled

### Standard Label Properties
- All properties from System.Windows.Forms.Label are available
- Size, Location, Enabled, Visible, etc.

## Common Use Cases

### Form Section Headers
Create visually distinct section headers for grouping related controls in forms.

### Dashboard Panels
Build attractive informational panels and status displays in dashboard applications.

### Branding Elements
Implement company branding with custom color schemes and gradient effects.

### Status Indicators
Design eye-catching status labels with color-coded gradients (success, warning, error).

### Decorative Text
Add visual appeal to important text, announcements, or promotional messages.

### Theme-Based Labeling
Create themed labels that can be saved and loaded via serialization.

## Related Skills

- [AutoLabel](../implementing-autolabels/) - Automatic label positioning and sizing
- [GradientPanel](../implementing-gradient-panels/) - Panels with gradient backgrounds

## Notes

- GradientLabel derives from System.Windows.Forms.Label, so all standard Label functionality is available
- The BrushInfo class provides the gradient and styling capabilities
- BackgroundColor property is the key to customization
- BorderColor only works when BorderStyle is set to FixedSingle
- Gradient colors array first entry matches BackColor, last entry matches ForeColor
- XML serialization allows persisting gradient settings across application sessions
- Performance is optimized for typical usage; avoid excessive gradient complexity for large numbers of controls
