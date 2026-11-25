---
name: syncfusion-winforms-color-picker
description: Guide to implement and customize the Syncfusion WinForms ColorPickerUIAdv control. Use this when implementing color-selection interfaces with organized palettes (Recent, Standard, Theme), custom color groups, Office-style layouts, a 'More Colors' dialog, or runtime color additions in Windows Forms applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Color Picker (ColorPickerUIAdv)

Guide for implementing the Syncfusion ColorPickerUIAdv control in Windows Forms applications.

## Overview

The **ColorPickerUIAdv** control provides a Microsoft Word 2007-style color selection interface for Windows Forms applications. It offers organized color groups (Recent, Standard, Theme), customizable color palettes, multiple visual styles, and an optional "More Colors" dialog for advanced color selection.

**Key Features:**
- **Color Groups:** Recent Colors, Standard Colors, Theme Colors
- **Custom Groups:** Add user-defined color collections
- **Visual Styles:** Office2007, Office2010, Office2016, Metro
- **Color Dialog:** "More Colors" button for advanced selection
- **Sub-Items:** Color variations and tints
- **Events:** Picked (on selection), ItemSelection (on hover)
- **Automatic Color:** Configurable default color button
- **Runtime Selection:** Dynamic color addition via dialog

## When to Use This Skill

Use this skill when you need to:
- Implement color selection in Windows Forms applications
- Provide Microsoft Word-style color picker interface
- Organize colors into groups (Recent, Standard, Theme, Custom)
- Allow users to select from predefined color palettes
- Support theme-based color selection
- Add color input controls with Office styling
- Implement "More Colors" dialog for advanced selection
- Handle color selection events in desktop applications
- Create custom color collections for specific domains

## Component Features Summary

| Feature | Description |
|---------|-------------|
| **Color Groups** | Recent, Standard, Theme, and Custom groups |
| **Sub-Items** | Color variations/tints for each base color |
| **Visual Styles** | Office2007, Office2010, Office2016, Metro |
| **Events** | Picked (selection), ItemSelection (hover) |
| **Dialog** | "More Colors" option for advanced selection |
| **Customization** | Item sizing, spacing, headers, borders |
| **Runtime** | Dynamic color addition via dialog |
| **Themes** | Office color schemes (Blue, Silver, Black) |

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)  
When you need:
- Assembly dependencies and NuGet packages
- Adding ColorPickerUIAdv via designer or code
- Namespace imports (Syncfusion.Windows.Forms.Tools)
- Basic color selection with SelectedColor property
- Initial setup and configuration
- Minimal working example

### Color Groups and Organization
📄 **Read:** [references/color-groups.md](references/color-groups.md)  
When you need:
- Understanding default groups (Recent, Standard, Theme)
- Creating custom color groups with CustomGroups property
- Adding color items and sub-items to groups
- Using GroupColorItem and ColorItem classes
- Configuring IsSubItemsVisible and SubItemsDepth
- Setting group names and header heights
- Organizing colors by category or theme

### Appearance and Styling
📄 **Read:** [references/appearance-styling.md](references/appearance-styling.md)  
When you need:
- Applying visual styles (Office2007, Office2010, Office2016, Metro)
- Configuring Office2007 color schemes (Blue, Silver, Black)
- Using custom colors with Managed theme
- ApplyManagedColors method for app-wide theming
- Border styles (Fixed3D, FixedSingle, None)
- BorderStyle and BorderOffset properties
- UseOffice2007Style property configuration

### Events and Runtime Selection
📄 **Read:** [references/events-selection.md](references/events-selection.md)  
When you need:
- Handling Picked event when color is selected
- Using ItemSelection event for hover interactions
- ColorPickedEventArgs and event properties
- Runtime color selection dialog ("More Colors")
- Configuring AutomaticColor property
- ButtonHeight for automatic button sizing
- Event-driven color handling patterns

### Customization and Layout
📄 **Read:** [references/customization.md](references/customization.md)  
When you need:
- Color item sizing with ColorItemSize property
- Horizontal and vertical spacing between items
- HorizontalItemsSpacing and VerticalItemsSpacing
- Header text alignment with TextAlignment
- Font customization for group headers
- Design-time color editing in property grid
- Advanced layout and spacing options

## Quick Start

### Basic ColorPickerUIAdv Implementation

```csharp
using System;
using System.Drawing;
using System.Windows.Forms;
using Syncfusion.Windows.Forms.Tools;

public partial class ColorPickerForm : Form
{
    private ColorPickerUIAdv colorPickerUIAdv1;
    
    public ColorPickerForm()
    {
        InitializeComponent();
        
        // Create ColorPickerUIAdv
        colorPickerUIAdv1 = new ColorPickerUIAdv();
        colorPickerUIAdv1.Size = new Size(200, 180);
        colorPickerUIAdv1.Location = new Point(20, 20);
        
        // Set initial selected color
        colorPickerUIAdv1.SelectedColor = Color.Blue;
        
        // Apply Office2016 style
        colorPickerUIAdv1.Style = ColorPickerUIAdv.visualstyle.Office2016Colorful;
        
        // Handle color selection
        colorPickerUIAdv1.Picked += ColorPickerUIAdv1_Picked;
        
        // Add to form
        this.Controls.Add(colorPickerUIAdv1);
    }
    
    private void ColorPickerUIAdv1_Picked(object sender, 
                                          ColorPickerUIAdv.ColorPickedEventArgs args)
    {
        // Update form background with selected color
        this.BackColor = args.Color;
        MessageBox.Show($"Selected Color: {args.Color.Name}");
    }
}
```

### Assembly Requirements

**Required Assemblies:**
- Syncfusion.Grid.Base
- Syncfusion.Grid.Windows
- Syncfusion.Shared.Base
- Syncfusion.Shared.Windows
- Syncfusion.Tools.Base
- Syncfusion.Tools.Windows

**NuGet Package:**
```powershell
Install-Package Syncfusion.Tools.Windows
```

## Common Patterns

### Pattern 1: Color Selection with Event Handler

```csharp
// Setup
private void SetupColorPicker()
{
    colorPickerUIAdv1.SelectedColor = Color.White;
    colorPickerUIAdv1.Picked += OnColorPicked;
}

// Event handler
private void OnColorPicked(object sender, ColorPickerUIAdv.ColorPickedEventArgs e)
{
    // Apply color to target control
    targetLabel.ForeColor = e.Color;
    
    // Or update drawing operations
    currentBrush = new SolidBrush(e.Color);
    canvas.Invalidate();
}
```

### Pattern 2: Applying Office2016 Theme

```csharp
// Office2016 Colorful style
colorPickerUIAdv1.Style = ColorPickerUIAdv.visualstyle.Office2016Colorful;

// Or Office2016 White
colorPickerUIAdv1.Style = ColorPickerUIAdv.visualstyle.Office2016White;

// Or Office2016 Black
colorPickerUIAdv1.Style = ColorPickerUIAdv.visualstyle.Office2016Black;

// Or Office2016 DarkGray
colorPickerUIAdv1.Style = ColorPickerUIAdv.visualstyle.Office2016DarkGray;
```

### Pattern 3: Creating Custom Color Group

```csharp
// Create custom color group
ColorUIAdvGroup customGroup = new ColorUIAdvGroup();
customGroup.Name = "Brand Colors";
customGroup.HeaderHeight = 25;

// Create color items
GroupColorItem primaryColor = new GroupColorItem(customGroup, Color.FromArgb(0, 120, 215));
primaryColor.Index = 0;

// Add tint variations as sub-items
primaryColor.SubItems.Add(new ColorItem(primaryColor, Color.FromArgb(204, 228, 247)));
primaryColor.SubItems.Add(new ColorItem(primaryColor, Color.FromArgb(153, 204, 239)));
primaryColor.SubItems.Add(new ColorItem(primaryColor, Color.FromArgb(102, 163, 224)));

// Add to group and control
customGroup.Items.Add(primaryColor);
customGroup.SubItemsDepth = 1;
customGroup.IsSubItemsVisible = true;

colorPickerUIAdv1.CustomGroups.Add(customGroup);
```

### Pattern 4: Office2007 Theme with Custom Colors

```csharp
// Set Managed theme
colorPickerUIAdv1.UseOffice2007Style = true;
colorPickerUIAdv1.Office2007Theme = Office2007Theme.Managed;

// Apply custom color scheme
Office2007Colors.ApplyManagedColors(this, Color.Teal);
```

### Pattern 5: Hover Preview with ItemSelection Event

```csharp
// Setup hover event
colorPickerUIAdv1.ItemSelection += ColorPickerUIAdv1_ItemSelection;

// Event handler for hover preview
private void ColorPickerUIAdv1_ItemSelection(object sender, 
                                              ColorPickerUIAdv.ColorPickedEventArgs e)
{
    // Show preview without committing
    previewPanel.BackColor = e.Color;
    statusLabel.Text = $"Preview: {e.Color.Name} (RGB: {e.Color.R}, {e.Color.G}, {e.Color.B})";
}
```

### Pattern 6: Configuring Automatic Color Button

```csharp
// Set automatic color (shown when "Automatic" button is clicked)
colorPickerUIAdv1.AutomaticColor = Color.Black;

// Adjust button height
colorPickerUIAdv1.ButtonHeight = 30;
```

## Key Properties

### Color Selection
- **SelectedColor** - Gets/sets the currently selected color
- **SelectedItem** - Gets the selected color item object
- **AutomaticColor** - Default color for "Automatic" button

### Color Groups
- **RecentGroup** - Recent colors collection
- **StandardGroup** - Standard colors collection
- **ThemeGroup** - Theme colors collection
- **CustomGroups** - User-defined color groups collection

### Visual Style
- **Style** - Visual style (Default, Office2007, Office2010, Office2016*, Metro)
- **UseOffice2007Style** - Enable/disable Office2007 styling
- **Office2007Theme** - Office2007 color scheme (Blue, Silver, Black, Managed)

### Layout and Appearance
- **ColorItemSize** - Size of individual color items (default: 13x13)
- **HorizontalItemsSpacing** - Horizontal space between items (default: 4)
- **VerticalItemsSpacing** - Vertical space between items (default: 0)
- **BorderStyle** - Border appearance (None, FixedSingle, Fixed3D)
- **BorderOffset** - Border height (default: 3)
- **TextAlign** - Header text alignment (default: MiddleLeft)
- **ButtonHeight** - Height of automatic button (default: 23)

### Events
- **Picked** - Raised when a color is selected
- **ItemSelection** - Raised when mouse hovers over a color item

## Common Use Cases

### Use Case 1: Text Editor Color Selection
Implement color picker for changing text or background colors in a text editor.

```csharp
private void SetupTextColorPicker()
{
    textColorPicker.Style = ColorPickerUIAdv.visualstyle.Office2016Colorful;
    textColorPicker.SelectedColor = richTextBox.SelectionColor;
    textColorPicker.Picked += (s, e) => richTextBox.SelectionColor = e.Color;
}
```

### Use Case 2: Drawing Application Color Palette
Provide color selection for drawing tools with preview on hover.

```csharp
private void SetupDrawingColorPicker()
{
    colorPicker.Style = ColorPickerUIAdv.visualstyle.Office2016Black;
    colorPicker.ItemSelection += (s, e) => ShowColorPreview(e.Color);
    colorPicker.Picked += (s, e) => SetActiveBrushColor(e.Color);
}
```

### Use Case 3: Theme Color Customization
Allow users to customize application theme colors with organized groups.

```csharp
private void SetupThemeColorPicker()
{
    // Add custom theme colors group
    ColorUIAdvGroup themeGroup = new ColorUIAdvGroup();
    themeGroup.Name = "Theme Colors";
    
    // Add primary, accent, background colors
    themeGroup.Items.Add(CreateColorItem(primaryColor, "Primary"));
    themeGroup.Items.Add(CreateColorItem(accentColor, "Accent"));
    themeGroup.Items.Add(CreateColorItem(backgroundColor, "Background"));
    
    colorPicker.CustomGroups.Add(themeGroup);
    colorPicker.Picked += ApplyThemeColor;
}
```

### Use Case 4: Form Designer Property Editor
Integrate color picker for property editing in a form designer tool.

```csharp
private void ShowColorPickerForProperty(Control control, string propertyName)
{
    ColorPickerUIAdv picker = new ColorPickerUIAdv();
    picker.SelectedColor = (Color)control.GetType()
                                   .GetProperty(propertyName)
                                   .GetValue(control);
    
    picker.Picked += (s, e) => {
        control.GetType()
               .GetProperty(propertyName)
               .SetValue(control, e.Color);
    };
    
    ShowPickerInPopup(picker);
}
```

### Use Case 5: Conditional Formatting Color Selection
Provide color picker for conditional formatting rules in data grids.

```csharp
private void SetupConditionalFormatColorPicker()
{
    // Create custom group with warning/info/success colors
    ColorUIAdvGroup formatGroup = new ColorUIAdvGroup();
    formatGroup.Name = "Formatting Colors";
    
    formatGroup.Items.Add(new GroupColorItem(formatGroup, Color.Red));      // Error
    formatGroup.Items.Add(new GroupColorItem(formatGroup, Color.Orange));   // Warning
    formatGroup.Items.Add(new GroupColorItem(formatGroup, Color.Yellow));   // Caution
    formatGroup.Items.Add(new GroupColorItem(formatGroup, Color.LightGreen)); // Success
    
    colorPicker.CustomGroups.Add(formatGroup);
    colorPicker.Picked += ApplyConditionalFormatting;
}
```

## Troubleshooting

### Issue: Control Not Appearing in Toolbox
**Solution:** Install Syncfusion.Tools.WinForms NuGet package and rebuild solution.

### Issue: Colors Not Displaying Correctly
**Solution:** Ensure proper initialization of color groups before adding to form. Check SubItemsDepth and IsSubItemsVisible properties.

### Issue: Theme Not Applying
**Solution:** Set UseOffice2007Style = true for Office2007 themes. For other styles, use the Style property directly.

### Issue: Events Not Firing
**Solution:** Verify event handlers are attached after control initialization but before form load. Check that control is added to form's Controls collection.

### Issue: Custom Groups Not Showing
**Solution:** Ensure CustomGroups.Add() is called after creating and populating the ColorUIAdvGroup. Verify HeaderHeight is set appropriately.

## Next Steps

1. Read [getting-started.md](references/getting-started.md) for initial setup
2. Explore [color-groups.md](references/color-groups.md) to organize colors effectively
3. Review [appearance-styling.md](references/appearance-styling.md) for visual customization
4. Implement event handling with [events-selection.md](references/events-selection.md)
5. Fine-tune layout using [customization.md](references/customization.md)
