---
name: syncfusion-winforms-numericupdown
description: Guide for implementing Syncfusion WinForms NumericUpDownExt control in Windows Forms applications. Use when users need enhanced numeric input with XP themes, value constraints (min/max/increment), hexadecimal display, decimal places, thousands separator, or themed borders beyond standard WinForms NumericUpDown.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing NumericUpDownExt in Syncfusion WinForms

This skill guides you in implementing **Syncfusion WinForms NumericUpDownExt** control—an enhanced numeric up/down control with XP themes, value constraints, hexadecimal display, decimal formatting, and professional appearance features.

## When to Use This Skill

Use this skill when the user needs to:

- Implement **enhanced numeric up/down controls** with XP themes support
- Set **value constraints** (Minimum, Maximum, Increment values)
- Display **hexadecimal values** in numeric input
- Format numbers with **decimal places** and **thousands separators**
- Apply **themed borders** (FixedSingle, Fixed3D, ThemedBorder)
- Use **separate colors for negative values** (NegativeForeColor)
- Enable **keyboard arrow key input** for value changes
- Support **large value entry** via keyboard
- Configure **text and button alignment** (left/right/center)
- Create **professional numeric input forms** with consistent theming
- Replace **standard NumericUpDown** with visually enhanced alternatives

NumericUpDownExt is ideal when visual theming and advanced formatting are important for numeric input controls.

## Component Overview

**NumericUpDownExt** is an advanced numeric up/down control that extends the standard WinForms NumericUpDown with XP themes and enhanced features. It provides:

- **XP Themes Support**: Enhanced look and feel missing in standard .NET control
- **Value Constraints**: Minimum, Maximum, Increment properties
- **Display Options**: Decimal places, thousands separator, hexadecimal format
- **Appearance Customization**: Colors, borders, alignment options
- **Themed Borders**: FixedSingle, Fixed3D, None, ThemedBorder
- **Keyboard Support**: Arrow keys, large value entry
- **Negative Value Styling**: Separate foreground color for negative numbers
- **Layout Control**: MinSize, MaxSize properties

**Key Difference from Standard NumericUpDown:**
NumericUpDownExt adds XP themes, hexadecimal display, themed borders, and negative value color styling.

## Documentation and Navigation Guide

### Getting Started and Basic Setup

📄 **Read:** [references/getting-started.md](references/getting-started.md)

Read this reference when users need:
- Assembly dependencies and NuGet package installation
- Creating NumericUpDownExt via designer or code
- Basic properties and configuration
- Adding NumericUpDownExt to forms
- Understanding control hierarchy
- Complete minimal working example

### Value Settings and Constraints

📄 **Read:** [references/value-settings.md](references/value-settings.md)

Read this reference when users need:
- Value property for current numeric value
- Minimum and Maximum constraints
- Increment property for step values
- Hexadecimal display mode
- HexValue property for hex representation
- UpButton/DownButton methods
- Value constraint examples and patterns

### Display Settings

📄 **Read:** [references/display-settings.md](references/display-settings.md)

Read this reference when users need:
- DecimalPlaces property for fractional display
- ThousandsSeparator for large numbers
- Display formatting options
- Currency and percentage formatting
- Examples with different number formats

### Appearance Customization

📄 **Read:** [references/appearance-customization.md](references/appearance-customization.md)

Read this reference when users need:
- Background and foreground colors
- NegativeForeColor for negative values
- Border styles (FixedSingle, Fixed3D, None)
- ThemedBorder property
- Text and button alignment
- Layout settings (MaxSize, MinSize)
- Complete custom styling examples

### Behavior Settings

📄 **Read:** [references/behavior-settings.md](references/behavior-settings.md)

Read this reference when users need:
- InterceptArrowKeys property for keyboard input
- ReadOnly mode configuration
- Key support for large value entry
- Behavior configuration options
- User interaction patterns

### Themes and Visual Styles

📄 **Read:** [references/themes-and-styles.md](references/themes-and-styles.md)

Read this reference when users need:
- Visual styles overview
- Applying themes to NumericUpDownExt
- XP Themes look and feel
- Theme integration with application
- Style best practices

## Quick Start Example

Here's a minimal example creating a NumericUpDownExt control with constraints:

```csharp
using Syncfusion.Windows.Forms.Tools;
using System;
using System.Drawing;
using System.Windows.Forms;

public class NumericUpDownExample : Form
{
    private NumericUpDownExt numericUpDownExt1;
    
    public NumericUpDownExample()
    {
        // Create NumericUpDownExt
        numericUpDownExt1 = new NumericUpDownExt();
        numericUpDownExt1.Location = new Point(70, 29);
        numericUpDownExt1.Size = new Size(120, 20);
        
        // Set value constraints
        numericUpDownExt1.Minimum = 0;
        numericUpDownExt1.Maximum = 100;
        numericUpDownExt1.Value = 50;
        numericUpDownExt1.Increment = 5;
        
        // Set display formatting
        numericUpDownExt1.DecimalPlaces = 2;
        numericUpDownExt1.ThousandsSeparator = true;
        
        // Add to form
        this.Controls.Add(numericUpDownExt1);
        
        this.Text = "NumericUpDownExt Example";
        this.Size = new Size(300, 150);
    }
}
```

**Result:** A numeric up/down control with values ranging 0-100, incrementing by 5, displaying 2 decimal places with thousands separator.

## Common Patterns

### Currency Input Control

**Pattern:** Create a numeric control for currency input with proper formatting.

```csharp
// Currency input with constraints
NumericUpDownExt currencyInput = new NumericUpDownExt();
currencyInput.Location = new Point(100, 20);
currencyInput.Size = new Size(120, 20);

// Value settings
currencyInput.Minimum = 0;
currencyInput.Maximum = 999999.99m;
currencyInput.Increment = 0.01m;
currencyInput.Value = 0;

// Display formatting
currencyInput.DecimalPlaces = 2;
currencyInput.ThousandsSeparator = true;

// Add label for context
Label label = new Label();
label.Text = "Price: $";
label.Location = new Point(50, 23);
label.AutoSize = true;

this.Controls.Add(label);
this.Controls.Add(currencyInput);
```

**When:** User needs currency input with cents precision and large number formatting.

### Percentage Selector

**Pattern:** Numeric control for percentage values (0-100).

```csharp
NumericUpDownExt percentInput = new NumericUpDownExt();
percentInput.Location = new Point(100, 50);
percentInput.Size = new Size(100, 20);

// Percentage constraints
percentInput.Minimum = 0;
percentInput.Maximum = 100;
percentInput.Increment = 5;
percentInput.Value = 50;
percentInput.DecimalPlaces = 1;

// Add % suffix label
Label percentLabel = new Label();
percentLabel.Text = "%";
percentLabel.Location = new Point(205, 53);
percentLabel.AutoSize = true;

this.Controls.Add(percentInput);
this.Controls.Add(percentLabel);
```

**When:** User needs percentage input with constrained range.

### Hexadecimal Color Value Input

**Pattern:** Display and edit values in hexadecimal format.

```csharp
NumericUpDownExt hexInput = new NumericUpDownExt();
hexInput.Location = new Point(100, 80);
hexInput.Size = new Size(120, 20);

// Hex mode for color values
hexInput.Hexadecimal = true;
hexInput.Minimum = 0;
hexInput.Maximum = 0xFFFFFF; // Max RGB value
hexInput.Increment = 0x10;
hexInput.Value = 0xFF5733; // Example color

// Add label
Label hexLabel = new Label();
hexLabel.Text = "Color (Hex):";
hexLabel.Location = new Point(20, 83);
hexLabel.AutoSize = true;

this.Controls.Add(hexLabel);
this.Controls.Add(hexInput);
```

**When:** User needs hexadecimal input for colors, memory addresses, or byte values.

## Key Properties

### Value Properties

| Property | Type | Description | When to Use |
|----------|------|-------------|-------------|
| `Value` | decimal | Current numeric value | Get/set control value |
| `Minimum` | decimal | Minimum allowed value | Set lower constraint |
| `Maximum` | decimal | Maximum allowed value | Set upper constraint |
| `Increment` | decimal | Value change step | Control increment size |
| `Hexadecimal` | bool | Display in hex format | Hex value input |
| `HexValue` | string | Hex representation (read-only) | Get hex string |

### Display Properties

| Property | Type | Description | When to Use |
|----------|------|-------------|-------------|
| `DecimalPlaces` | int | Number of decimal places | Fractional precision |
| `ThousandsSeparator` | bool | Show thousands separator | Large number formatting |

### Appearance Properties

| Property | Type | Description | When to Use |
|----------|------|-------------|-------------|
| `BackColor` | Color | Background color | Custom backgrounds |
| `ForeColor` | Color | Text color | Custom text colors |
| `NegativeForeColor` | Color | Color for negative values | Highlight negative numbers |
| `BorderStyle` | BorderStyle | Border style (FixedSingle/Fixed3D/None) | Control appearance |
| `ThemedBorder` | bool | Use themed border | Modern appearance |

### Behavior Properties

| Property | Type | Description | When to Use |
|----------|------|-------------|-------------|
| `InterceptArrowKeys` | bool | Allow arrow key input | Keyboard value changes |
| `ReadOnly` | bool | Prevent value editing | Display-only mode |
| `UpDownAlign` | LeftRightAlignment | Button position (Left/Right) | Layout customization |
| `TextAlign` | HorizontalAlignment | Text alignment | Left/Right/Center alignment |

## Common Use Cases

### Settings Forms

Numeric inputs for application settings:
- Font size selector (8-72 pt)
- Timeout values (seconds/minutes)
- Buffer size settings
- Thread count configuration

### Financial Applications

Currency and percentage inputs:
- Price entry with decimal precision
- Discount percentage selectors
- Tax rate inputs
- Account balance displays

### Scientific/Engineering Tools

Precision numeric input:
- Measurement values with decimal places
- Calibration parameters
- Calculation inputs with constraints
- Unit conversion interfaces

### Color Pickers

Hexadecimal color value input:
- RGB component values (0-255)
- Hex color codes (#000000-#FFFFFF)
- Alpha channel values
- Color palette editors

## Implementation Checklist

When implementing NumericUpDownExt, ensure:

- ✅ **Required assemblies** referenced (Syncfusion.Tools.Windows.dll, etc.)
- ✅ **Namespace** included (Syncfusion.Windows.Forms.Tools)
- ✅ **NumericUpDownExt instance** created and configured
- ✅ **Value constraints** set (Minimum, Maximum, Increment)
- ✅ **Display formatting** configured (DecimalPlaces, ThousandsSeparator)
- ✅ **Location and Size** specified for layout
- ✅ **Default value** set with Value property
- ✅ **Event handlers** added for ValueChanged if needed
- ✅ **Validation** implemented for business rules
- ✅ **Testing** with boundary values (min, max, zero, negatives)

## Troubleshooting Quick Reference

**Issue:** Value not changing with arrow keys
- Set `InterceptArrowKeys = true`
- Ensure control has focus
- Check if ReadOnly is false

**Issue:** Decimal places not displaying
- Set `DecimalPlaces` property to desired count
- Ensure Value has decimal component
- Check Value is not integer-only

**Issue:** Thousands separator not showing
- Set `ThousandsSeparator = true`
- Ensure value is >= 1000
- Verify culture settings support separator

**Issue:** Cannot set value outside range
- Check `Minimum` and `Maximum` properties
- Ensure desired value is within constraints
- Use decimal type for large values

**Issue:** Hexadecimal display not working
- Set `Hexadecimal = true`
- Ensure value is valid hex range
- Use HexValue property to read hex string

**Issue:** Negative values not showing in different color
- Set `NegativeForeColor` property explicitly
- Ensure Minimum allows negative values
- Check value is actually negative

## Summary

NumericUpDownExt provides enhanced numeric input functionality with:

- **XP Themes**: Modern look and feel
- **Value Constraints**: Min/Max/Increment control
- **Display Formatting**: Decimal places, thousands separator, hexadecimal
- **Visual Customization**: Colors, borders, alignment, themed appearance

Use NumericUpDownExt when visual theming, advanced formatting, and precise value control are important for creating professional numeric input controls in WinForms applications.
