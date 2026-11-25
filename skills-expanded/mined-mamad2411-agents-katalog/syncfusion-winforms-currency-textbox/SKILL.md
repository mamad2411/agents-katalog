---
name: syncfusion-winforms-currency-textbox
description: Implement currency input controls in Windows Forms applications using Syncfusion CurrencyTextBox. Use this skill when developers need to create currency entry fields with validation, formatting, decimal handling, positive/negative color coding, and clipboard support. Essential for financial forms, payment inputs, budget applications, and any scenario requiring validated currency input.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion Windows Forms CurrencyTextBox

Syncfusion CurrencyTextBox is a specialized text input control derived from System.Windows.Forms.TextBox
that provides currency-specific validation, formatting, and behavior. It handles keyboard input validation,
culture-aware decimal formatting, and value constraints automatically.

## When to Use This Skill

- Creating currency input fields with automatic validation
- Building financial data entry forms (invoices, payments, budgets)
- Implementing currency display with positive/negative color coding
- Working with decimal precision and grouping separators
- Handling clipboard operations with currency data
- Adding keyboard shortcuts for multiplying values (Mega, Kilo, etc.)
- Enforcing minimum and maximum currency values
- Displaying overflow indicators for large numbers

## Component Overview

The CurrencyTextBox control intercepts user keyboard input and prevents entry of invalid currency characters.
It automatically formats the display based on decimal digits, group separators, and the currency symbol.
Unlike the standard TextBox, it validates against min/max bounds and supports currency-specific events.

**Key Capabilities:**
- Automatic keyboard input validation
- Culture-aware decimal formatting
- Max/Min value constraints with enforcement
- Positive, negative, and zero value color coding
- Clipboard support with optional format stripping
- Overflow indicators with tooltips
- Keyboard shortcuts for multiplying values
- ValidationError event for invalid input handling

## Documentation Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and assembly dependencies
- Creating a project and adding the control
- Designer and code-based control creation
- Setting up MaxValue/MinValue constraints
- Configuring currency symbols
- Basic control properties

### Text Field Customization
📄 **Read:** [references/text-field-customization.md](references/text-field-customization.md)
- Text display and alignment (Left, Center, Right)
- Multiline support with word wrapping
- Password character masking
- Banner text for empty state
- Number and decimal digit formatting
- Handling negative values and signs
- Null string configuration

### Value Formatting
📄 **Read:** [references/value-formatting.md](references/value-formatting.md)
- DecimalValue programmatic access
- Currency symbol customization
- Number formatting (total digits before decimal)
- Decimal digit precision
- Group separator configuration
- Removing trailing decimal zeros
- Currency positive and negative patterns

### Event Handling
📄 **Read:** [references/event-handling.md](references/event-handling.md)
- KeyDown event for keyboard shortcuts
- Adding multiplier keys (G, M, K for Giga/Mega/Kilo)
- ValidationError event for invalid input
- Error message handling with StartPosition
- Using ErrorProvider for visual feedback
- Custom validation scenarios

### Appearance Customization
📄 **Read:** [references/appearance-customization.md](references/appearance-customization.md)
- Border styles (FixedSingle, Fixed3D, None)
- 3D border effects (Raised, Sunken, Flat, etc.)
- Border color and side configuration
- Color coding by value (Positive, Negative, Zero)
- ReadOnly background color
- Visual style application

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Clipboard support with formatting options
- Overflow indicator display
- Overflow indicator tooltips
- Multiple clipboard modes
- Data preservation strategies

### Validation and Constraints
📄 **Read:** [references/validation-and-constraints.md](references/validation-and-constraints.md)
- Setting min/max boundaries
- Enforcing constraints during validation
- Negative input behavior with selected text
- AllowNull configuration
- NullString custom display values
- Value range enforcement

## Quick Start Example

```csharp
using System.Windows.Forms;
using Syncfusion.Windows.Forms.Tools;

public partial class Form1 : Form
{
    private CurrencyTextBox currencyTextBox1;
    
    public Form1()
    {
        InitializeComponent();
        
        // Create and configure CurrencyTextBox
        currencyTextBox1 = new CurrencyTextBox();
        currencyTextBox1.Location = new System.Drawing.Point(10, 10);
        currencyTextBox1.Size = new System.Drawing.Size(200, 25);
        
        // Set currency format
        currencyTextBox1.CurrencySymbol = "$";
        currencyTextBox1.CurrencyDecimalDigits = 2;
        currencyTextBox1.CurrencyGroupSeparator = ",";
        currencyTextBox1.CurrencyGroupSizes = new int[] { 3 };
        
        // Set value constraints
        currencyTextBox1.MaxValue = 999999.99m;
        currencyTextBox1.MinValue = 0m;
        currencyTextBox1.DecimalValue = 100.00m;
        
        // Set colors for value states
        currencyTextBox1.PositiveColor = System.Drawing.Color.Black;
        currencyTextBox1.NegativeColor = System.Drawing.Color.Red;
        currencyTextBox1.ZeroColor = System.Drawing.Color.Gray;
        
        this.Controls.Add(currencyTextBox1);
    }
}
```

## Common Patterns

### Currency Entry Form
```csharp
// For collecting currency amounts (payments, invoices, etc.)
currencyTextBox.MaxValue = decimal.MaxValue;
currencyTextBox.MinValue = 0m;
currencyTextBox.CurrencySymbol = "$";
currencyTextBox.CurrencyDecimalDigits = 2;
currencyTextBox.AllowNull = false;
```

### Profit/Loss Display
```csharp
// Color-code by sign (green for profit, red for loss)
currencyTextBox.PositiveColor = System.Drawing.Color.Green;
currencyTextBox.NegativeColor = System.Drawing.Color.Red;
currencyTextBox.MaxValue = decimal.MaxValue;
currencyTextBox.MinValue = decimal.MinValue;
```

### Optional Amount with Placeholder
```csharp
// Allow null values with custom placeholder text
currencyTextBox.AllowNull = true;
currencyTextBox.NullString = "(Not Specified)";
currencyTextBox.Text = "";
```

### Keyboard Shortcuts for Large Numbers
```csharp
// Handle KeyDown event to add multiplier shortcuts
private void currencyTextBox1_KeyDown(object sender, KeyEventArgs e)
{
    decimal value = currencyTextBox1.DecimalValue;
    switch(e.KeyCode)
    {
        case Keys.G: // Giga (billion)
            currencyTextBox1.DecimalValue = value * 1000000000m;
            break;
        case Keys.M: // Mega (million)
            currencyTextBox1.DecimalValue = value * 1000000m;
            break;
        case Keys.K: // Kilo (thousand)
            currencyTextBox1.DecimalValue = value * 1000m;
            break;
    }
}
```

## Key Properties Reference

| Property | Type | Purpose | Common Values |
|----------|------|---------|----------------|
| DecimalValue | decimal | Get/set numeric value programmatically | Any valid decimal |
| CurrencySymbol | string | Currency symbol display | "$", "€", "£", "¥" |
| CurrencyDecimalDigits | int | Decimal places displayed | 2, 3, 4 |
| CurrencyGroupSeparator | string | Thousands separator | ",", ".", " " |
| MaxValue | decimal | Maximum allowed value | 999999.99, 100000, etc. |
| MinValue | decimal | Minimum allowed value | 0, -999999.99, etc. |
| PositiveColor | Color | Color for positive values | Color.Black, Color.Green |
| NegativeColor | Color | Color for negative values | Color.Red, Color.Maroon |
| ZeroColor | Color | Color for zero value | Color.Gray, Color.DarkGray |
| TextAlign | HorizontalAlignment | Text position | Left, Center, Right |
| BorderStyle | BorderStyle | Border appearance | FixedSingle, Fixed3D, None |
| AllowNull | bool | Allow empty/null values | true, false |
| ShowOverflowIndicator | bool | Show indicator when value exceeds bounds | true, false |

## Use Cases by Scenario

**Financial Application**
- Use positive/negative color coding
- Set MaxValue to prevent data type overflow
- Handle ValidationError for audit logging
- Support clipboard for paste operations

**Budget Entry Form**
- Set reasonable MaxValue (e.g., 999999.99)
- Use TextAlign.Right for numeric convention
- Display banner text for required fields
- Enforce MinValue of 0 if amounts must be positive

**Multi-Currency Display**
- Change CurrencySymbol based on user locale
- Keep CurrencyDecimalDigits consistent (usually 2)
- Adjust CurrencyGroupSeparator per region
- Display DecimalValue consistently in database

**Large Number Handling**
- Enable keyboard multiplier shortcuts (G, M, K)
- Use ShowOverflowIndicator for values exceeding visible space
- Remove decimal zeros with RemoveDecimalZeros property
- Increase number digits with CurrencyNumberDigits

## Next Steps

- Choose the reference file matching your task
- Implement the control following the code examples
- Test with both valid and edge-case values
- Handle ValidationError event for invalid input
- Use DecimalValue for business logic, Text for display
