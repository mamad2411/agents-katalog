---
name: syncfusion-winforms-color-picker-dropdown
description: Implement and customize the Syncfusion Windows Forms ColorPickerButton control for color selection. Trigger when user needs a color picker dropdown, color selection UI, color input control, or needs to let users select from color groups (standard, system, custom, user colors). Covers getting started, color selection, customization, and UI appearance properties.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing ColorPickerButton

The **ColorPickerButton** is a Windows Forms control that displays a dropdown with the ColorUIControl, allowing users to select colors from predefined groups (Standard, System, Custom, and User colors). It combines a button with a professional color picker interface similar to Visual Studio's color picker.

## When to Use This Skill

- User needs a color picker dropdown control in a Windows Forms application
- Implementing color selection UI with multiple color groups
- Customizing button appearance to reflect selected colors
- Integrating color input into forms without a full dialog
- Displaying colors inline within application layouts

## Component Overview

The ColorPickerButton provides:

- **Multiple Color Groups:** Standard, System, Custom, and User color options
- **Color Selection:** Interactive color picking with programmatic access
- **Button Integration:** Displays colors on the button face or as text
- **Dropdown Customization:** Adjustable ColorUIControl size and appearance
- **Easy Integration:** Works in designer and programmatic code

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Assembly deployment and NuGet setup
- Adding via Visual Studio designer
- Adding via code programmatically
- Creating and initializing instances
- Testing the component

### Color Selection & Groups
📄 **Read:** [references/color-selection.md](references/color-selection.md)
- Selecting colors programmatically and interactively
- Working with color groups (SystemColors, StandardColors, CustomColors, UserColors)
- Setting initial selected color and group
- Color change events and handling
- Getting selected color at runtime

### Customization Settings
📄 **Read:** [references/customization.md](references/customization.md)
- Sizing the dropdown ColorUIControl
- Button appearance properties
- Display selected color as button background
- Display selected color as button text
- Advanced customization and styling

### UI Appearance Properties
📄 **Read:** [references/ui-properties.md](references/ui-properties.md)
- Button text, size, and positioning
- Color display modes and appearance
- Component properties and events
- Border and styling
- Layout and docking

## Quick Start Example

```csharp
using Syncfusion.Windows.Forms;

public class ColorPickerForm : Form
{
    public ColorPickerForm()
    {
        // Create ColorPickerButton instance
        var colorPicker = new ColorPickerButton();
        colorPicker.Text = "Select a Color";
        colorPicker.Location = new System.Drawing.Point(10, 10);
        colorPicker.Size = new System.Drawing.Size(150, 30);
        
        // Set initial selected color and group
        colorPicker.SelectedColor = System.Drawing.Color.Red;
        colorPicker.SelectedColorGroup = Syncfusion.Windows.Forms.ColorUISelectedGroup.StandardColors;
        
        // Add to form
        this.Controls.Add(colorPicker);
        
        // Set initial form properties
        this.Text = "ColorPickerButton Demo";
        this.Size = new System.Drawing.Size(400, 300);
    }
}
```

## Common Patterns

### Pattern 1: Display Selected Color as Button Background
```csharp
colorPickerButton1.SelectedAsBackcolor = true;
colorPickerButton1.SelectedColor = System.Drawing.Color.OrangeRed;
// Button background now shows the selected color
```

### Pattern 2: Display Selected Color as Text
```csharp
colorPickerButton1.SelectedAsText = true;
colorPickerButton1.SelectedColor = System.Drawing.Color.Blue;
// Button text displays the selected color name/value
```

### Pattern 3: Set Color Group and Color
```csharp
colorPickerButton1.SelectedColorGroup = Syncfusion.Windows.Forms.ColorUISelectedGroup.StandardColors;
colorPickerButton1.SelectedColor = System.Drawing.Color.Green;
// Focus the Standard Colors group when dropdown opens
```

### Pattern 4: Customize Dropdown Size
```csharp
colorPickerButton1.ColorUISize = new System.Drawing.Size(250, 280);
// Adjust dropdown dimensions for your layout
```

## Key Props

| Property | Type | Purpose |
|----------|------|---------|
| `SelectedColor` | System.Drawing.Color | Gets/sets the currently selected color |
| `SelectedColorGroup` | ColorUISelectedGroup | Sets which color group tab is focused (StandardColors, SystemColors, CustomColors, UserColors, None) |
| `SelectedAsBackcolor` | bool | When true, button background displays the selected color |
| `SelectedAsText` | bool | When true, button text displays the selected color value |
| `ColorUISize` | System.Drawing.Size | Gets/sets the size of the dropdown ColorUIControl |
| `Text` | string | Gets/sets the button text |

## Common Use Cases

### Use Case 1: Theme Color Selector
```csharp
// Let users pick a theme color that shows on the button
colorPickerButton.SelectedAsBackcolor = true;
colorPickerButton.SelectedColorGroup = ColorUISelectedGroup.StandardColors;
```

### Use Case 2: Color Code Input
```csharp
// Show selected color value and group
colorPickerButton.SelectedAsText = true;
colorPickerButton.SelectedColorGroup = ColorUISelectedGroup.CustomColors;
```

### Use Case 3: Compact Color Picker
```csharp
// Minimize space with compact size
colorPickerButton.ColorUISize = new System.Drawing.Size(200, 200);
colorPickerButton.Size = new System.Drawing.Size(80, 25);
```

## Next Steps

- Read **[references/getting-started.md](references/getting-started.md)** to set up the component
- Check **[references/color-selection.md](references/color-selection.md)** for color handling
- Review **[references/customization.md](references/customization.md)** for styling options
- See **[references/ui-properties.md](references/ui-properties.md)** for appearance control
