---
name: syncfusion-winforms-radio-button
description: Guide for implementing Syncfusion RadioButtonAdv control in Windows Forms applications. Use when creating enhanced radio buttons with Office themes (2007/2016), Metro style, gradient backgrounds, text shadow effects, custom images per state, or 2D/3D borders for professional styling beyond standard WinForms RadioButton.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing RadioButtonAdv in Syncfusion WinForms

This skill guides you in implementing **Syncfusion WinForms RadioButtonAdv** control—an enhanced radio button with advanced styling options including Office themes, gradient backgrounds, text shadow effects, custom images, and professional appearance features.

## When to Use This Skill

Use this skill when the user needs to:

- Implement **enhanced radio buttons** with modern styling beyond standard RadioButton
- Apply **Office themes** (Office2007, Office2016 Colorful/White/Black/DarkGray)
- Use **Metro-style radio buttons** for modern UI design
- Add **text shadow effects** with custom colors and offsets
- Create **gradient backgrounds** for radio buttons
- Display **custom images** for different radio button states
- Apply **2D or 3D border styles** to radio buttons
- Configure **text and button alignment** for custom layouts
- Associate **integer or string values** with radio button states
- Build **professional forms** with consistent Office-style theming
- Replace **standard RadioButton** with visually enhanced alternatives

RadioButtonAdv is ideal when visual appearance and theming are important for radio button controls.

## Component Overview

**RadioButtonAdv** is an advanced radio button control that extends the standard WinForms RadioButton with rich styling capabilities. It provides:

- **Theme Support**: Office2007, Office2016, Metro, and Default themes
- **Text Effects**: Shadow text with color and offset customization
- **Backgrounds**: Gradient backgrounds with custom colors
- **Borders**: 2D and 3D border style options
- **Images**: Custom images for each check state
- **Alignment**: Flexible text and button positioning
- **Value Association**: Integer/string values per state
- **Behavior Options**: Auto-height, focus rectangle, click events

**Key Difference from Standard RadioButton:**
RadioButtonAdv adds visual styling and theming capabilities while maintaining standard radio button functionality.

## Documentation and Navigation Guide

### Getting Started and Basic Setup

📄 **Read:** [references/getting-started.md](references/getting-started.md)

Read this reference when users need:
- Assembly dependencies and NuGet package installation
- Creating RadioButtonAdv via designer or code
- Basic properties (Text, Font, ForeColor, BackColor)
- Adding RadioButtonAdv to forms
- Understanding control hierarchy
- Complete minimal working example

### Themes and Visual Styles

📄 **Read:** [references/themes-and-styles.md](references/themes-and-styles.md)

Read this reference when users need:
- Enabling themes with ThemesEnabled property
- Applying Style property (Default, Office2007, Metro, Office2016 variants)
- Office2007ColorScheme (Managed, Blue, Silver, Black)
- Custom managed colors for Office2007 theme
- Complete themed examples
- Professional Office-style appearance

### Text Settings and Effects

📄 **Read:** [references/text-settings.md](references/text-settings.md)

Read this reference when users need:
- TextShadow property for shadow effects
- ShadowColor customization
- ShadowOffset positioning
- WrapText for long text handling
- Text effect examples
- Text styling best practices

### Appearance Customization

📄 **Read:** [references/appearance-customization.md](references/appearance-customization.md)

Read this reference when users need:
- Gradient backgrounds with custom colors
- Border styles (2D and 3D options)
- Alignment settings for text and button
- Custom images for different states
- Complete appearance customization
- Advanced styling patterns

### Behavior Settings

📄 **Read:** [references/behavior-settings.md](references/behavior-settings.md)

Read this reference when users need:
- AutoHeight for automatic height calculation
- DrawFocusRectangle visibility control
- RaiseEventOnClick event behavior
- RadioButtonAdv Settings (integer/string value association)
- Behavior configuration options

### Events

📄 **Read:** [references/events.md](references/events.md)

Read this reference when users need:
- Available RadioButtonAdv events
- Click event handling
- CheckedChanged event
- Event best practices
- Common event patterns

## Quick Start Example

Here's a minimal example creating themed RadioButtonAdv controls:

```csharp
using Syncfusion.Windows.Forms.Tools;
using System;
using System.Drawing;
using System.Windows.Forms;

public class RadioButtonExample : Form
{
    private RadioButtonAdv radioButtonAdv1;
    private RadioButtonAdv radioButtonAdv2;
    private RadioButtonAdv radioButtonAdv3;
    
    public RadioButtonExample()
    {
        // Create first radio button
        radioButtonAdv1 = new RadioButtonAdv();
        radioButtonAdv1.Text = "Option 1";
        radioButtonAdv1.Location = new Point(20, 20);
        radioButtonAdv1.Size = new Size(120, 21);
        radioButtonAdv1.Style = RadioButtonAdvStyle.Office2016Colorful;
        radioButtonAdv1.Checked = true;
        
        // Create second radio button
        radioButtonAdv2 = new RadioButtonAdv();
        radioButtonAdv2.Text = "Option 2";
        radioButtonAdv2.Location = new Point(20, 50);
        radioButtonAdv2.Size = new Size(120, 21);
        radioButtonAdv2.Style = RadioButtonAdvStyle.Office2016Colorful;
        
        // Create third radio button
        radioButtonAdv3 = new RadioButtonAdv();
        radioButtonAdv3.Text = "Option 3";
        radioButtonAdv3.Location = new Point(20, 80);
        radioButtonAdv3.Size = new Size(120, 21);
        radioButtonAdv3.Style = RadioButtonAdvStyle.Office2016Colorful;
        
        // Add to form
        this.Controls.Add(radioButtonAdv1);
        this.Controls.Add(radioButtonAdv2);
        this.Controls.Add(radioButtonAdv3);
        
        this.Text = "RadioButtonAdv Example";
        this.Size = new Size(300, 200);
    }
}
```

**Result:** Three Office2016-themed radio buttons with modern appearance.

## Common Patterns

### Themed Radio Button Group

**Pattern:** Create a group of radio buttons with consistent Office2016 theming.

```csharp
// Create GroupBox for radio buttons
GroupBox groupBox = new GroupBox();
groupBox.Text = "Select Option";
groupBox.Location = new Point(10, 10);
groupBox.Size = new Size(200, 120);

// Create themed radio buttons
string[] options = { "Small", "Medium", "Large" };
int yPos = 20;

foreach (string option in options)
{
    RadioButtonAdv radio = new RadioButtonAdv();
    radio.Text = option;
    radio.Location = new Point(10, yPos);
    radio.Style = RadioButtonAdvStyle.Office2016Colorful;
    radio.ThemesEnabled = true;
    groupBox.Controls.Add(radio);
    yPos += 30;
}

this.Controls.Add(groupBox);
```

**When:** User needs multiple related options with consistent theming.

### Radio Button with Text Shadow

**Pattern:** Add visual emphasis with text shadow effects.

```csharp
RadioButtonAdv shadowRadio = new RadioButtonAdv();
shadowRadio.Text = "Important Option";
shadowRadio.TextShadow = true;
shadowRadio.ShadowColor = Color.Gold;
shadowRadio.ShadowOffset = new Point(2, 2);
shadowRadio.Font = new Font("Segoe UI", 10, FontStyle.Bold);
shadowRadio.Location = new Point(20, 20);
```

**When:** User wants to emphasize specific radio button options.

### Custom Gradient Background

**Pattern:** Create radio buttons with gradient backgrounds for modern appearance.

```csharp
RadioButtonAdv gradientRadio = new RadioButtonAdv();
gradientRadio.Text = "Premium Option";
// Gradient properties set via designer or property grid
// GradientStart, GradientEnd, GradientStyle
gradientRadio.Location = new Point(20, 20);
```

**When:** User needs custom branded or styled radio buttons.

## Key Properties

### Theme and Style Properties

| Property | Type | Description | When to Use |
|----------|------|-------------|-------------|
| `Style` | RadioButtonAdvStyle | Office2007, Metro, Office2016 variants | Apply modern themes |
| `ThemesEnabled` | bool | Enable/disable theming | Control theme application |
| `Office2007ColorScheme` | Office2007Theme | Blue, Silver, Black, Managed | Office2007 color variants |

### Text Properties

| Property | Type | Description | When to Use |
|----------|------|-------------|-------------|
| `TextShadow` | bool | Enable text shadow effect | Add visual depth to text |
| `ShadowColor` | Color | Shadow color | Customize shadow appearance |
| `ShadowOffset` | Point | Shadow position offset | Control shadow placement |
| `WrapText` | bool | Enable text wrapping | Handle long text labels |

### Appearance Properties

| Property | Type | Description | When to Use |
|----------|------|-------------|-------------|
| `DrawFocusRectangle` | bool | Show/hide focus rectangle | Control focus indicator |
| `AutoHeight` | bool | Auto-calculate height | Adjust to content size |
| `BackColor` | Color | Background color | Custom backgrounds |
| `ForeColor` | Color | Text color | Custom text colors |

### Behavior Properties

| Property | Type | Description | When to Use |
|----------|------|-------------|-------------|
| `RaiseEventOnClick` | bool | Fire OnClick event | Control click behavior |
| `Checked` | bool | Radio button state | Set default selection |

## Common Use Cases

### Settings Dialog

Create a settings form with themed radio buttons:
- Group related options (Theme, Size, Layout)
- Apply consistent Office2016 theming
- Professional appearance matching application style

### Wizard Step Selection

Radio buttons for wizard navigation:
- Metro or Office2016 style for modern look
- Text shadow for emphasis on current step
- Clear visual hierarchy

### Survey/Questionnaire Forms

Multiple-choice questions with styled radio buttons:
- Consistent theming across all questions
- Text wrapping for long option labels
- Professional survey appearance

### Preference Configuration

User preference selection:
- Gradient backgrounds for premium options
- Custom images per state for visual indicators
- Value association for easy preference storage

## Implementation Checklist

When implementing RadioButtonAdv, ensure:

- ✅ **Required assemblies** referenced (Syncfusion.Tools.Windows.dll, etc.)
- ✅ **Namespace** included (Syncfusion.Windows.Forms.Tools)
- ✅ **RadioButtonAdv instances** created and configured
- ✅ **Style/Theme** applied for consistent appearance
- ✅ **Text properties** set (Text, Font, optional shadow)
- ✅ **Location and Size** specified for layout
- ✅ **Event handlers** added for CheckedChanged or Click
- ✅ **Radio button groups** properly configured (only one selected per group)
- ✅ **Default selection** set with Checked property
- ✅ **Testing** with different themes and styles

## Troubleshooting Quick Reference

**Issue:** Theme not applying
- Set `ThemesEnabled = true`
- Ensure `Style` property is set to desired theme
- Check if custom BackColor overrides theme

**Issue:** Text shadow not visible
- Set `TextShadow = true`
- Choose contrasting `ShadowColor`
- Adjust `ShadowOffset` for visibility

**Issue:** Radio buttons not mutually exclusive
- Ensure radio buttons are in same container (Form, Panel, GroupBox)
- Only radio buttons in same parent container are grouped

**Issue:** Focus rectangle always visible
- Set `DrawFocusRectangle = false` to hide
- Check if form-level setting overrides control

**Issue:** Height not adjusting to text
- Set `AutoHeight = true`
- Ensure `WrapText` is configured if text is long

## Summary

RadioButtonAdv provides enhanced radio button functionality with:

- **Professional Themes**: Office2007, Office2016, Metro styles
- **Text Effects**: Shadow with custom colors and offsets
- **Visual Customization**: Gradients, borders, images
- **Flexible Styling**: Alignment, appearance, and behavior options

Use RadioButtonAdv when visual appearance and theming are important for creating professional, modern WinForms applications.
