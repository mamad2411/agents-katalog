---
name: syncfusion-winui-numberbox
description: Learn to implement Syncfusion WinUI NumberBox (SfNumberBox) control for numeric input with validation, custom formatting, and value restrictions. Use this skill when you need numeric input fields with currency, percentage, or decimal formatting in WinUI applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing WinUI NumberBox

The Syncfusion WinUI NumberBox (SfNumberBox) is an advanced numeric input control that provides validation, custom formatting, and interactive features for entering numeric values.

## When to Use This Component

Use NumberBox when you need to:
- Accept numeric input with validation
- Display values in currency, percentage, or decimal formats
- Restrict input to a specific range (min/max)
- Provide UpDown buttons for value adjustment
- Support multiple numeric data types (double, decimal, int, long, etc.)
- Enable keyboard and mouse wheel value changes
- Handle watermark text and placeholder values

## Component Overview

The NumberBox control combines these key features:
- **Numeric Validation** - Automatically validates and formats input
- **Multiple Formats** - Currency (C), Percentage (P), Decimal (N), and custom formats
- **Value Control** - Min/max bounds and null handling
- **Interactive Adjustment** - UpDown buttons, keyboard arrows, mouse scrolling
- **Data Type Support** - Double, Decimal, Float, Long, Int, UInt, Byte, SByte
- **Accessibility** - Full keyboard navigation and screen reader support

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and NuGet package setup
- Adding NumberBox in XAML and C#
- Basic control creation
- Supported data types (Double, Decimal, Float, Long, Int, UInt, Byte, SByte)
- Placeholder text and description properties
- Header customization
- Value editing and validation on Enter/focus loss

### UpDown Button & Value Adjustment
📄 **Read:** [references/updown-button.md](references/updown-button.md)
- UpDown button placement modes (Hidden, Inline, Compact)
- SmallChange for keyboard/mouse increment
- LargeChange for Page Up/Page Down increment
- TextBox visibility control
- Keyboard support (Arrow, Page keys)
- Mouse scrolling for value changes

### Value Formatting
📄 **Read:** [references/formatting.md](references/formatting.md)
- CustomFormat property (C2, P2, N3 formats)
- NumberFormatter classes (CurrencyFormatter, PercentFormatter, DecimalFormatter)
- Currency formatting with region/culture support
- Percentage and decimal formatting
- Integer and fractional digit control
- Culture-specific formatting
- Handling both CustomFormat and NumberFormatter

### Value Restrictions & Validation
📄 **Read:** [references/restrictions.md](references/restrictions.md)
- AllowNull property for null value handling
- Minimum and Maximum bounds
- Range validation behavior
- IsEditable property for read-only mode
- Text editing restrictions
- Default value fallback when AllowNull=false

## Quick Start Example

### Basic NumberBox Setup

**XAML:**
```xaml
<editors:SfNumberBox 
    x:Name="priceInput"
    HorizontalAlignment="Center"
    VerticalAlignment="Center"
    Header="Price"
    Value="0"
    Minimum="0"
    Maximum="999.99"
    CustomFormat="C2" />
```

**C#:**
```csharp
SfNumberBox priceInput = new SfNumberBox();
priceInput.Header = "Price";
priceInput.Value = 0;
priceInput.Minimum = 0;
priceInput.Maximum = 999.99;
priceInput.CustomFormat = "C2";

// Handle value changes
priceInput.ValueChanged += (s, e) => {
    var newValue = e.NewValue;
    var oldValue = e.OldValue;
};
```

## Common Implementation Patterns

### Pattern 1: Currency Input Field
**When:** User needs to enter monetary amounts
```xaml
<editors:SfNumberBox 
    Header="Amount"
    Value="0"
    CustomFormat="C2"
    Minimum="0"
    Maximum="10000"
    AllowNull="False"
    SmallChange="1" />
```

### Pattern 2: Percentage Input Field
**When:** User needs to enter percentage values
```xaml
<editors:SfNumberBox 
    Header="Discount"
    Value="0"
    CustomFormat="P2"
    Minimum="0"
    Maximum="100"
    SmallChange="5" />
```

### Pattern 3: Quantity Selector with UpDown Buttons
**When:** User selects discrete quantities
```xaml
<editors:SfNumberBox 
    Header="Quantity"
    Value="1"
    Minimum="1"
    Maximum="100"
    UpDownPlacementMode="Inline"
    SmallChange="1"
    AllowNull="False" />
```

### Pattern 4: Read-Only Display with Adjustment
**When:** Display value with UpDown buttons but prevent typing
```xaml
<editors:SfNumberBox 
    Value="50"
    IsEditable="False"
    UpDownPlacementMode="Inline"
    SmallChange="1" />
```

### Pattern 5: High-Precision Decimal Input
**When:** Financial or scientific calculations needed
```xaml
<editors:SfNumberBox 
    ValueType="Decimal"
    Value="1234.56"
    CustomFormat="0.00"
    Minimum="0"
    Maximum="999999.99" />
```

## Key Properties Quick Reference

### Value Properties
- **Value** - Current numeric value
- **ValueType** - Data type (Double, Decimal, Float, Long, Int, UInt, Byte, SByte)
- **AllowNull** - Permit null/empty values (default: True)

### Formatting Properties
- **CustomFormat** - Format string (C2=currency, P2=percent, N3=decimal)
- **NumberFormatter** - Advanced formatter objects
- **Culture** - Culture-specific formatting

### Range Properties
- **Minimum** - Lowest allowed value
- **Maximum** - Highest allowed value

### Display Properties
- **Header** - Label text
- **HeaderTemplate** - Custom header layout
- **PlaceholderText** - Watermark when empty
- **Description** - Help text below control
- **ShowClearButton** - Show/hide clear button

### Interaction Properties
- **UpDownPlacementMode** - Button position (Hidden, Inline, Compact)
- **SmallChange** - Increment for arrows/scrolling (default: 1)
- **LargeChange** - Increment for Page keys (default: 10)
- **IsEditable** - Allow text input (default: True)
- **TextBoxVisibility** - Show/hide text box

### Events
- **ValueChanged** - Fires when value changes after validation

## Common Use Cases

1. **Price Input** - Use C2 format, set realistic min/max bounds
2. **Age Input** - Use int ValueType, set 0-150 range
3. **Discount Field** - Use P2 format, set 0-100 range
4. **Quantity Picker** - Use Inline UpDown, set practical limits
5. **Percentage Calculation** - Use P2 format with appropriate decimals
6. **Payment Amount** - Use C2 format with currency rules
7. **Decimal Precision** - Use Decimal type for financial data

## Installation

### NuGet Package
```
Install-Package Syncfusion.Editors.WinUI
```

### XAML Namespace
```xaml
xmlns:editors="using:Syncfusion.UI.Xaml.Editors"
```

## Next Steps

- Read [Getting Started](references/getting-started.md) for setup details
- Review [UpDown Button Features](references/updown-button.md) for value adjustment
- Explore [Value Formatting](references/formatting.md) for currency/percentage support
- Check [Value Restrictions](references/restrictions.md) for validation and bounds
