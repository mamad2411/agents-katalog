---
name: syncfusion-winforms-color-ui-control
description: Guide for implementing Syncfusion ColorUIControl in Windows Forms applications. Use this when working with color selection UI, color pickers, or color palette controls. Covers color groups (System, Standard, Custom, User), appearance customization, and popup menu integration in .NET Windows Forms applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing ColorUIControl

## When to Use This Skill

Use this skill when you need to implement color selection functionality in Windows Forms applications using Syncfusion's ColorUIControl. This skill is relevant when users:

- Need to add color picker UI to Windows Forms applications
- Want to provide Visual Studio-style color selection interface
- Require inline color selection controls (not just dialogs)
- Need customizable color palettes with predefined color groups
- Want to integrate color pickers into popup menus or dropdowns
- Need to implement color selection with System, Standard, Custom, or User-defined colors
- Are working with .NET Framework Windows Forms applications
- Want to provide ColorPickerButton dropdown functionality

The ColorUIControl provides a palette-style interface similar to Visual Studio's color picker, offering four color groupings (SystemColors, StandardColors, CustomColors, UserColors) that can be displayed inline in your application or as a dropdown.

## Component Overview

**ColorUIControl** is a Windows Forms control that provides a rich color selection interface with predefined color palettes. Unlike the standard ColorDialog which appears as a modal dialog, ColorUIControl can be placed inline within your application's layout or used as a dropdown control.

**Key Capabilities:**
- Four predefined color groups (System, Standard, Custom, User)
- Inline placement within application layout
- Popup/dropdown integration via PopupControlContainer
- Customizable color palettes and tab names
- Visual Studio-style color picker interface
- Programmatic and interactive color selection
- Border style customization and panel stretching

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)

When users need to:
- Install and set up the ColorUIControl component
- Add ColorUIControl via designer or code
- Understand assembly dependencies (Syncfusion.Shared.Base)
- Initialize the control in C# or VB.NET
- Set initial selected color and color group
- Import required namespaces (Syncfusion.Windows.Forms)

### Color Groups and Selection
📄 **Read:** [references/color-groups.md](references/color-groups.md)

When users need to:
- Understand the four color groups (System, Standard, Custom, User)
- Control which color groups are displayed
- Select default color groups programmatically
- Customize UserColors and UserCustomColors collections
- Add or remove specific color groups
- Programmatically populate custom color cells

### Appearance and Customization
📄 **Read:** [references/appearance-customization.md](references/appearance-customization.md)

When users need to:
- Set border styles (FixedSingle, Fixed3D, None)
- Enable panel stretching for Custom and User color groups
- Customize tab text for each color group
- Change font styles for tab text
- Reset tab names to defaults
- Adjust visual appearance of the control

### Events and Interaction
📄 **Read:** [references/events.md](references/events.md)

When users need to:
- Handle the ColorSelected event
- Close popups when colors are selected
- Access selected color from event handlers
- Work with PopupControlContainer in events
- Implement color selection callbacks

### Advanced Scenarios
📄 **Read:** [references/popup-integration.md](references/popup-integration.md)

When users need to:
- Add ColorUIControl to popup menus
- Integrate with PopupMenu and PopupControlContainer
- Configure DropDownBarItem for color pickers
- Show color picker on mouse clicks
- Use ColorPickerButton for dropdown functionality
- Create complete popup color selection workflows

## Quick Start Example

Here's a minimal example to add ColorUIControl to a Windows Forms application:

```csharp
using System;
using System.Drawing;
using System.Windows.Forms;
using Syncfusion.Windows.Forms;

public class ColorPickerForm : Form
{
    private ColorUIControl colorUIControl1;
    
    public ColorPickerForm()
    {
        InitializeComponent();
    }
    
    private void InitializeComponent()
    {
        // Create ColorUIControl instance
        this.colorUIControl1 = new ColorUIControl();
        
        // Set size
        this.colorUIControl1.Size = new Size(210, 200);
        this.colorUIControl1.Location = new Point(20, 20);
        
        // Set initial color and group
        this.colorUIControl1.SelectedColor = Color.OrangeRed;
        this.colorUIControl1.SelectedColorGroup = 
            ColorUISelectedGroup.StandardColors;
        
        // Handle color selection
        this.colorUIControl1.ColorSelected += ColorUIControl1_ColorSelected;
        
        // Add to form
        this.Controls.Add(this.colorUIControl1);
        
        // Form settings
        this.Text = "Color Picker Example";
        this.Size = new Size(300, 300);
    }
    
    private void ColorUIControl1_ColorSelected(object sender, EventArgs e)
    {
        Color selectedColor = this.colorUIControl1.SelectedColor;
        MessageBox.Show($"Selected Color: {selectedColor.Name}");
    }
}
```

**VB.NET:**
```vb
Imports System.Drawing
Imports System.Windows.Forms
Imports Syncfusion.Windows.Forms

Public Class ColorPickerForm
    Inherits Form
    
    Private colorUIControl1 As ColorUIControl
    
    Public Sub New()
        InitializeComponent()
    End Sub
    
    Private Sub InitializeComponent()
        ' Create ColorUIControl instance
        Me.colorUIControl1 = New ColorUIControl()
        
        ' Set size
        Me.colorUIControl1.Size = New Size(210, 200)
        Me.colorUIControl1.Location = New Point(20, 20)
        
        ' Set initial color and group
        Me.colorUIControl1.SelectedColor = Color.OrangeRed
        Me.colorUIControl1.SelectedColorGroup = _
            ColorUISelectedGroup.StandardColors
        
        ' Handle color selection
        AddHandler Me.colorUIControl1.ColorSelected, _
            AddressOf ColorUIControl1_ColorSelected
        
        ' Add to form
        Me.Controls.Add(Me.colorUIControl1)
        
        ' Form settings
        Me.Text = "Color Picker Example"
        Me.Size = New Size(300, 300)
    End Sub
    
    Private Sub ColorUIControl1_ColorSelected(sender As Object, e As EventArgs)
        Dim selectedColor As Color = Me.colorUIControl1.SelectedColor
        MessageBox.Show($"Selected Color: {selectedColor.Name}")
    End Sub
End Class
```

## Common Patterns

### Pattern 1: Inline Color Picker with Specific Groups

Show only Standard and Custom colors for a simplified picker:

```csharp
// Display only Standard and Custom color groups
this.colorUIControl1.ColorGroups = 
    ColorUIGroups.StandardColors | ColorUIGroups.CustomColors;

// Enable panel stretching for better visual layout
this.colorUIControl1.CustomColorsStretchOnResize = true;

// Set border style
this.colorUIControl1.BorderStyle = BorderStyle.FixedSingle;
```

### Pattern 2: Custom Tab Names

Customize tab text for better context:

```csharp
// Customize tab names
this.colorUIControl1.StandardTabName = "Web Colors";
this.colorUIControl1.SystemTabName = "System";
this.colorUIControl1.UserTabName = "My Colors";
this.colorUIControl1.CustomTabName = "Theme Palette";

// Customize font
this.colorUIControl1.Font = new Font("Segoe UI", 9F);
```

### Pattern 3: Popup Color Picker

Integrate ColorUIControl into a popup menu:

```csharp
// Setup: Create PopupMenu, PopupControlContainer, and ColorUIControl
private PopupMenu popupMenu1;
private PopupControlContainer popupContainer1;
private ColorUIControl colorUIControl1;
private Panel colorButton;

private void InitializePopupColorPicker()
{
    // Create and configure ColorUIControl
    colorUIControl1 = new ColorUIControl();
    colorUIControl1.Size = new Size(210, 200);
    
    // Create PopupControlContainer and add ColorUI
    popupContainer1 = new PopupControlContainer();
    popupContainer1.Controls.Add(colorUIControl1);
    
    // Create PopupMenu
    popupMenu1 = new PopupMenu();
    
    // Add DropDownBarItem to popup menu
    var dropDownItem = new DropDownBarItem();
    dropDownItem.PopupControlContainer = popupContainer1;
    popupMenu1.ParentBarItem.Items.Add(dropDownItem);
    
    // Handle panel click to show popup
    colorButton.MouseUp += ColorButton_MouseUp;
    
    // Close popup when color selected
    colorUIControl1.ColorSelected += ColorUIControl1_ColorSelected;
}

private void ColorButton_MouseUp(object sender, MouseEventArgs e)
{
    popupMenu1.Show(colorButton, new Point(e.X, e.Y));
}

private void ColorUIControl1_ColorSelected(object sender, EventArgs e)
{
    // Update UI with selected color
    colorButton.BackColor = colorUIControl1.SelectedColor;
    
    // Close the popup
    var cuiControl = sender as ColorUIControl;
    var pcc = cuiControl.Parent as PopupControlContainer;
    pcc.HidePopup(PopupCloseType.Done);
}
```

### Pattern 4: Customizing User Color Palette

Programmatically populate custom colors:

```csharp
// Customize UserColors collection with blue gradient
for (int i = 0; i < colorUIControl1.UserColors.Count; i++)
{
    colorUIControl1.UserColors[i] = Color.FromArgb(0, 0, i * 5);
}

// Customize UserCustomColors collection with red gradient
for (int i = 0; i < colorUIControl1.UserCustomColors.Count; i++)
{
    colorUIControl1.UserCustomColors[i] = Color.FromArgb(i * 15, 0, 0);
}

// Make sure UserColors group is displayed
colorUIControl1.ColorGroups = 
    ColorUIGroups.StandardColors | 
    ColorUIGroups.CustomColors | 
    ColorUIGroups.UserColors;

// Select UserColors group by default
colorUIControl1.SelectedColorGroup = ColorUISelectedGroup.UserColors;

// Enable stretching
colorUIControl1.UserColorsStretchOnResize = true;
```

## Key Properties

### Selection Properties
- **`SelectedColor`** (Color): Gets or sets the currently selected color
- **`SelectedColorGroup`** (ColorUISelectedGroup): Gets or sets which color group tab is active
  - Options: `SystemColors`, `StandardColors`, `CustomColors`, `UserColors`, `None`

### Display Properties
- **`ColorGroups`** (ColorUIGroups): Controls which color groups are visible (flags enum)
  - Combine with: `ColorUIGroups.StandardColors | ColorUIGroups.CustomColors`
- **`BorderStyle`** (BorderStyle): Sets border appearance (`FixedSingle`, `Fixed3D`, `None`)

### Customization Properties
- **`CustomColorsStretchOnResize`** (bool): Enables stretching of Custom colors panel
- **`UserColorsStretchOnResize`** (bool): Enables stretching of User colors panel
- **`StandardTabName`** (string): Custom text for Standard colors tab
- **`SystemTabName`** (string): Custom text for System colors tab
- **`CustomTabName`** (string): Custom text for Custom colors tab
- **`UserTabName`** (string): Custom text for User colors tab
- **`Font`** (Font): Font style for tab text

### Collection Properties
- **`UserColors`** (ColorCollection): Collection of colors in the User colors group
- **`UserCustomColors`** (ColorCollection): Additional custom colors in User group

### Events
- **`ColorSelected`**: Raised when a color is selected by the user

## Common Use Cases

1. **Text Editor Color Selection:** Add inline color picker for font colors, background colors, or highlighting
2. **Design Tools:** Provide color palette for drawing applications or design tools
3. **Theme Configuration:** Allow users to customize application themes with color selection
4. **Chart/Graph Customization:** Let users select colors for data series in charts
5. **Form Control Styling:** Enable runtime color customization for form controls
6. **Color Property Editors:** Integrate into property grids for color-based settings
7. **Popup Color Pickers:** Create ColorPickerButton-style dropdowns for toolbar buttons
8. **Custom Color Schemes:** Allow users to define and save custom color palettes

## Tips and Best Practices

- **Use SelectedColorGroup** to automatically focus the appropriate color tab based on user context
- **Enable panel stretching** (`CustomColorsStretchOnResize`, `UserColorsStretchOnResize`) for better visual layout in larger containers
- **Customize tab names** to match your application's terminology (e.g., "Theme Colors", "Brand Colors")
- **Handle ColorSelected event** to close popups or update UI immediately when colors are chosen
- **For dropdown functionality**, consider using ColorPickerButton instead of manually creating popup infrastructure
- **Limit visible groups** using `ColorGroups` property to simplify the UI when users only need specific color types
- **Programmatically set UserColors** when you have a predefined color scheme or theme
- **Reset methods** (`ResetSelectedColor()`, `ResetSelectedColorGroup()`) are useful for "Clear" or "Default" buttons


For ColorPickerButton dropdown functionality, refer to the Syncfusion documentation on using ColorUIControl as a drop-down control.
