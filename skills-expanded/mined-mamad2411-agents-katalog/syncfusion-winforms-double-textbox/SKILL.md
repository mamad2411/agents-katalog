---
name: syncfusion-winforms-double-textbox
description: Guide to implementing Syncfusion WinForms DoubleTextBox control for accepting double-precision floating-point values with customizable formatting and validation. Use this when working with numeric input controls requiring double data type support, decimal formatting, or value range constraints in Windows Forms applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion WinForms DoubleTextBox

## When to Use This Skill

Use this skill when you need to:
- Accept and display double-precision floating-point values in a Windows Forms application
- Implement numeric input with customizable decimal places and group separators
- Apply min/max value constraints to numeric input
- Handle value change events or keyboard shortcuts for incrementing/decrementing values
- Override the control's default keystroke handling for custom behavior
- Apply visual styling based on positive, negative, or zero values

## Component Overview

The **DoubleTextBox** is a specialized text box control derived from the Windows Forms Framework that handles double data type values. It provides:
- Automatic double value validation and formatting
- Customizable number display (decimal digits, separators, patterns)
- Min/max value constraints
- Event handling for value changes and keyboard input
- Keyboard shortcut support for incrementing/decrementing values
- Extensibility through method overrides

## Documentation Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Assembly deployment and setup
- Adding control via designer
- Adding control via C# code
- Setting maximum and minimum values
- Customizing number format

### Number and Format Settings
📄 **Read:** [references/number-and-format-settings.md](references/number-and-format-settings.md)
- Number formatting properties overview
- Decimal digits and separators
- Value range configuration (MaxValue/MinValue)
- Banner text support
- Hiding trailing zeros

### Appearance and Behavior
📄 **Read:** [references/appearance-and-behavior.md](references/appearance-and-behavior.md)
- Border style settings
- Color settings for value states
- Keyboard support configuration
- Overflow indicator display
- Active when disabled behavior

### Event Handling and Customization
📄 **Read:** [references/event-handling-and-customization.md](references/event-handling-and-customization.md)
- DoubleValueChanged event handling
- Keyboard events for increment/decrement
- Overriding control behavior
- Custom HandleSubtractKey implementation
- Extending control functionality

## Quick Start Example

**Basic setup in C#:**

```csharp
using Syncfusion.Windows.Forms.Tools;

// Create instance
DoubleTextBox doubleTextBox1 = new DoubleTextBox();
this.Controls.Add(doubleTextBox1);

// Set value constraints
doubleTextBox1.MaxValue = 100;
doubleTextBox1.MinValue = 0;

// Handle value changes
doubleTextBox1.DoubleValueChanged += (s, e) => 
    MessageBox.Show("Value changed");
```

**Key properties:**
- `DoubleValue` - Gets or sets the double value
- `MaxValue` - Maximum allowed value
- `MinValue` - Minimum allowed value
- `NumberDecimalDigits` - Number of decimal places to display
- `NumberDecimalSeparator` - Character used as decimal separator
- `NumberGroupSeparator` - Character used as thousands separator

## Common Patterns

### Pattern 1: Accept Percentage Input (0-100)
```csharp
doubleTextBox1.MinValue = 0;
doubleTextBox1.MaxValue = 100;
doubleTextBox1.NumberDecimalDigits = 2;
doubleTextBox1.Text = "50";
```

### Pattern 2: Accept Currency Values
```csharp
doubleTextBox1.NumberDecimalDigits = 2;
doubleTextBox1.NumberGroupSeparator = ",";
doubleTextBox1.NumberDecimalSeparator = ".";
doubleTextBox1.Text = "1234.56";
```

### Pattern 3: Increment/Decrement with Keyboard
```csharp
doubleTextBox1.KeyDown += (s, e) =>
{
    if (e.KeyCode == Keys.Up)
        doubleTextBox1.DoubleValue++;
    else if (e.KeyCode == Keys.Down)
        doubleTextBox1.DoubleValue--;
};
```

### Pattern 4: Allow Null/Empty Values
```csharp
doubleTextBox1.AllowNull = true;
doubleTextBox1.NullString = "";
doubleTextBox1.Text = "";
```

## Key Properties

| Property | Type | Purpose |
|----------|------|---------|
| `DoubleValue` | double | Gets or sets the double value of the textbox |
| `MaxValue` | double | Maximum allowed value |
| `MinValue` | double | Minimum allowed value |
| `NumberDecimalDigits` | int | Number of decimal places to display |
| `NumberDecimalSeparator` | string | Decimal separator character |
| `NumberGroupSeparator` | string | Thousands separator character |
| `NumberGroupSizes` | int[] | Sizes of number groups |
| `NumberNegativePattern` | int | Pattern for negative numbers |
| `HideTrailingZeros` | bool | Hide trailing zeros in display |
| `AllowNull` | bool | Allow null/empty values |
| `NullString` | string | String representation of null |

## Common Use Cases

1. **Financial Applications** - Currency input with two decimal places, value constraints
2. **Measurement Input** - Scientific data with variable decimal precision
3. **Percentage Fields** - Constrained to 0-100 range with validation
4. **Configuration Settings** - Numeric parameters for application tuning
5. **Data Entry Forms** - Validated numeric fields with formatting
6. **Calculate Totals** - Increment/decrement values with keyboard shortcuts
