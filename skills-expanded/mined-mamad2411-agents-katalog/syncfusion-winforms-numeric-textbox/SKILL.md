---
name: syncfusion-winforms-numeric-textbox
description: Implement Syncfusion SfNumericTextBox for numeric input with formatting, validation, and customization in Windows Forms. Use when creating numeric input controls with currency formatting, percent values, number validation, or decimal formatting. Covers numeric formatting options, value range validation, and formatted numeric data entry with validation capabilities.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion WinForms SfNumericTextBox

The Syncfusion WinForms SfNumericTextBox control is an advanced text input control that displays and accepts numeric values in multiple formats (numeric, currency, percent) with comprehensive validation, customization, and cultural support. It provides formatting options, value constraints, appearance customization, and event-driven capabilities for professional numeric data entry scenarios.

## When to Use This Skill

Use this skill ALWAYS and immediately when you need to:
- **Numeric Input**: Accept and display numeric values with precision
- **Format Modes**: Support numeric, currency, or percent formats
- **Value Validation**: Enforce minimum and maximum value constraints
- **Formatting**: Apply custom formatting with prefix/suffix, hide trailing zeros
- **Watermark**: Display placeholder text when control is empty
- **Cultural Formatting**: Support multiple cultures and number formats
- **Appearance Customization**: Customize colors based on value (positive/negative/zero)
- **Event Handling**: Respond to value changes with ValueChanged event
- **Data Entry Forms**: Build professional forms with validated numeric fields

## Component Overview

The SfNumericTextBox control is part of Syncfusion Essential Studio for Windows Forms and provides:
- **Multiple Format Modes**: Numeric, Currency, and Percent modes
- **Value Range Support**: Define and validate minimum and maximum values
- **Precision Preservation**: Maintains full precision while displaying formatted text
- **Null Value Support**: AllowNull property for nullable numeric fields
- **Watermark Text**: Display guidance text when value is null
- **Custom Units**: Prefix and suffix support for units and labels
- **Trailing Zeros**: Option to hide trailing zeros for cleaner display
- **Validation Modes**: KeyPress or LostFocus validation timing
- **Color Customization**: Different colors for positive, negative, and zero values
- **Border Styling**: Customizable borders with focus and hover states
- **Event System**: ValueChanged event with OldValue and NewValue tracking
- **Cultural Support**: Culture-aware formatting via NumberFormatInfo
- **Designer Support**: Full design-time support via toolbox

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)

**When to read:** First-time setup, installation, basic implementation

**Topics covered:**
- Assembly deployment and NuGet package installation
- Adding SfNumericTextBox via designer or code
- Namespace imports
- Setting values (Value property)
- Basic format modes
- Watermark text basics
- Min/Max value setup

---

### Format Modes
📄 **Read:** [references/format-modes.md](references/format-modes.md)

**When to read:** Formatting numbers in different modes, cultural support

**Topics covered:**
- FormatMode property (Numeric, Currency, Percent)
- Numeric format mode with decimal control
- Currency formatting with symbols
- Percent mode for percentage values
- Culture-specific formatting
- NumberFormatInfo customization
- Decimal separators and group separators
- Practical examples for each mode

---

### Formatting Options
📄 **Read:** [references/formatting-options.md](references/formatting-options.md)

**When to read:** Hiding zeros, adding units, displaying watermarks

**Topics covered:**
- Hiding trailing zeros (HideTrailingZeros property)
- Prefix and suffix for custom units
- Watermark text implementation
- WatermarkText property and AllowNull
- Combining watermark with format modes
- Display examples
- Edge cases and best practices

---

### Validation and Value Ranges
📄 **Read:** [references/validation-and-ranges.md](references/validation-and-ranges.md)

**When to read:** Enforcing value constraints, configuring validation behavior

**Topics covered:**
- MinValue and MaxValue properties
- ValidationMode property (KeyPress vs LostFocus)
- ValueChangeMode property (when value updates)
- LostFocusValidation modes (Reset, MaxValue, MinValue)
- Validation flow and event timing
- Error scenarios and handling
- Practical validation examples

---

### Appearance and Styling
📄 **Read:** [references/appearance-and-styling.md](references/appearance-and-styling.md)

**When to read:** Customizing colors, borders, and visual appearance

**Topics covered:**
- PositiveForeColor for positive values
- NegativeForeColor for negative values
- ZeroForeColor for zero values
- WatermarkForeColor for placeholder text
- BorderColor, FocusBorderColor, HoverBorderColor
- DisabledBorderColor for disabled state
- BorderStyle property
- Background and font customization
- Visual state examples

---

### Events and Advanced Patterns
📄 **Read:** [references/events-and-advanced.md](references/events-and-advanced.md)

**When to read:** Handling value changes, advanced scenarios

**Topics covered:**
- ValueChanged event and subscription
- ValueChangedEventArgs (OldValue, NewValue)
- Event timing and validation interaction
- Responding to value changes
- Advanced patterns (conditional formatting, cascading updates)
- Performance considerations
- Common event patterns

---

## Quick Start Example

### Basic Numeric TextBox in Code

```csharp
using Syncfusion.WinForms.Input;

// Create SfNumericTextBox
var numericTextBox = new SfNumericTextBox();
numericTextBox.Size = new System.Drawing.Size(150, 20);
numericTextBox.Value = 123.45;
this.Controls.Add(numericTextBox);
```

### With Formatting and Validation

```csharp
// Set format mode to currency
numericTextBox.FormatMode = Syncfusion.WinForms.Input.Enums.FormatMode.Currency;

// Set value constraints
numericTextBox.MinValue = 0;
numericTextBox.MaxValue = 10000;

// Add watermark
numericTextBox.WatermarkText = "Enter amount";
numericTextBox.AllowNull = true;

// Subscribe to value changes
numericTextBox.ValueChanged += (sender, e) => 
{
    MessageBox.Show($"Value changed from {e.OldValue} to {e.NewValue}");
};
```

---

## Key Props and Methods

| Property | Type | Purpose |
|----------|------|---------|
| **Value** | double? | Gets or sets the numeric value |
| **FormatMode** | FormatMode | Sets format (Numeric, Currency, Percent) |
| **MinValue** | double | Minimum allowed value |
| **MaxValue** | double | Maximum allowed value |
| **AllowNull** | bool | Allow null values in control |
| **WatermarkText** | string | Placeholder text when empty |
| **HideTrailingZeros** | bool | Hide zeros after decimal point |
| **Prefix** | string | Text prepended to value |
| **Suffix** | string | Text appended to value |
| **ValidationMode** | ValidationMode | KeyPress or LostFocus |
| **ValueChangeMode** | ValueChangeMode | When value property updates |
| **NumberFormatInfo** | NumberFormatInfo | Culture-specific number formatting |

---

## Common Patterns

### Pattern 1: Currency Input with Range
```csharp
// Currency field with $0-$10,000 range
numericTextBox.FormatMode = FormatMode.Currency;
numericTextBox.MinValue = 0;
numericTextBox.MaxValue = 10000;
numericTextBox.WatermarkText = "Enter amount (0-10000)";
```

### Pattern 2: Percentage Display
```csharp
// Display and accept percentages
numericTextBox.FormatMode = FormatMode.Percent;
numericTextBox.MinValue = 0;
numericTextBox.MaxValue = 100;
numericTextBox.HideTrailingZeros = true;
```

### Pattern 3: Measurement with Units
```csharp
// Display with custom units
numericTextBox.Suffix = " inches";
numericTextBox.Value = 25.5;
numericTextBox.HideTrailingZeros = true;
```

### Pattern 4: Validation with Color Feedback
```csharp
// Color based on value
numericTextBox.Style.PositiveForeColor = Color.Green;
numericTextBox.Style.NegativeForeColor = Color.Red;
numericTextBox.Style.ZeroForeColor = Color.Gray;
```

---

## Next Steps

1. **Start here**: Read [getting-started.md](references/getting-started.md) for installation and basic setup
2. **Choose format**: Explore [format-modes.md](references/format-modes.md) for numeric, currency, or percent modes
3. **Add formatting**: Check [formatting-options.md](references/formatting-options.md) for units, watermarks, and display options
4. **Enable validation**: Review [validation-and-ranges.md](references/validation-and-ranges.md) for constraints
5. **Customize appearance**: Use [appearance-and-styling.md](references/appearance-and-styling.md) for colors and borders
6. **Handle events**: Implement [events-and-advanced.md](references/events-and-advanced.md) for dynamic behavior
