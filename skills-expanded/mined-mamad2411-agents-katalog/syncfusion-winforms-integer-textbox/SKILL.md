---
name: syncfusion-winforms-integer-textbox
description: Guide for implementing Syncfusion Windows Forms Integer TextBox control. Use when creating integer input fields with numeric validation, number formatting, or value constraints in data entry scenarios. Covers integer validation, number formatting, min/max constraints, value formatting, and numeric input fields in WinForms applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion Windows Forms Integer TextBox

## When to Use This Skill

Use this skill when you need to:
- Create numeric input fields that accept only integer values
- Set up value constraints (minimum and maximum bounds)
- Format and display numbers with custom separators
- Handle negative values and validation
- Respond to value changes and validation errors in Windows Forms applications
- Apply visual styling to numeric inputs (colors, borders)

## Component Overview

The **IntegerTextBox** is a specialized Windows Forms control derived from the standard TextBox. It:
- Accepts and displays only integer data types
- Enforces min/max value constraints automatically
- Supports custom number formatting with group separators
- Provides events for value changes and validation errors
- Allows visual customization through colors and styling
- Handles null values and read-only states
- Supports leading zeros and negative value handling

**Key Characteristics:**
- Restricts input to integer values only
- Validates input in real-time
- Provides wrapper properties for null handling
- Offers formatting options without themes or localization
- Lightweight and responsive to user interactions

---

## Documentation & Navigation Guide

Choose the reference that matches your current task:

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and NuGet package setup
- Adding control through designer
- Adding control manually in C# code
- Setting minimum and maximum value constraints
- Initial configuration patterns

### Visual Appearance
📄 **Read:** [references/appearance.md](references/appearance.md)
- Setting background colors
- Configuring text colors by value type (positive/negative/zero)
- Border styling
- Read-only state appearance
- Color reset methods

### Data Handling & Formatting
📄 **Read:** [references/data-formatting.md](references/data-formatting.md)
- Number formatting options
- Group separators and group sizes
- Handling negative values and key inputs
- Leading zeros support
- Null value management
- Read-only with separate colors

### Events & Interactions
📄 **Read:** [references/events.md](references/events.md)
- BindableValueChanged event usage
- IntegerValueChanged event handling
- ValidationError event patterns
- FormattedTextChanged and ClipTextChanged
- Event handler implementation examples

---

## Quick Start Example

Here's a minimal working example:

```csharp
using Syncfusion.Windows.Forms.Tools;

// Add assembly reference: Syncfusion.Shared.Base
// Include namespace: Syncfusion.Windows.Forms.Tools

// Create and add control
IntegerTextBox integerTextBox1 = new IntegerTextBox();
this.Controls.Add(integerTextBox1);

// Set constraints
integerTextBox1.MaxValue = 999999;
integerTextBox1.MinValue = -999999;
integerTextBox1.IntegerValue = 0;
```

---

## Common Patterns

### Pattern 1: Value-Based Color Coding
Display positive values in green, negative in red, zero in gray:

```csharp
integerTextBox1.PositiveColor = System.Drawing.Color.Green;
integerTextBox1.NegativeColor = System.Drawing.Color.Red;
integerTextBox1.ZeroColor = System.Drawing.Color.Gray;
```

### Pattern 2: Number Formatting with Separators
Format large numbers with custom separators (e.g., "1,234,567"):

```csharp
integerTextBox1.NumberGroupSeparator = ",";
integerTextBox1.NumberGroupSizes = new int[] { 3 };
integerTextBox1.IntegerValue = 1234567;
```

### Pattern 3: Handling Value Changes
Respond when the user enters a new value:

```csharp
integerTextBox1.BindableValueChanged += 
    (sender, e) => MessageBox.Show($"New value: {integerTextBox1.IntegerValue}");
```

### Pattern 4: Validation with Error Handling
Catch and respond to validation errors:

```csharp
integerTextBox1.ValidationError += (sender, e) =>
{
    MessageBox.Show("Invalid input! Please enter a valid integer.");
};
```

---

## Key Properties

| Property | Purpose | Example |
|----------|---------|---------|
| **MaxValue** | Upper bound for integer values | `integerTextBox1.MaxValue = 100;` |
| **MinValue** | Lower bound for integer values | `integerTextBox1.MinValue = 0;` |
| **IntegerValue** | Get/set the current integer value | `int val = integerTextBox1.IntegerValue;` |
| **BindableValue** | Wrapper for null-safe value access | `integerTextBox1.BindableValue = null;` |
| **AllowLeadingZeros** | Allow zeros before number (e.g., "0123") | `integerTextBox1.AllowLeadingZeros = true;` |
| **NumberGroupSeparator** | Character to separate digit groups | `integerTextBox1.NumberGroupSeparator = ",";` |
| **NumberGroupSizes** | Size of each digit group | `integerTextBox1.NumberGroupSizes = new int[] { 3 };` |
| **PositiveColor** | Color for positive values | `integerTextBox1.PositiveColor = Color.Green;` |
| **NegativeColor** | Color for negative values | `integerTextBox1.NegativeColor = Color.Red;` |
| **ZeroColor** | Color when value is zero | `integerTextBox1.ZeroColor = Color.Gray;` |
| **BackColor** | Control background color | `integerTextBox1.BackColor = Color.White;` |
| **ReadOnlyBackColor** | Background when read-only | `integerTextBox1.ReadOnlyBackColor = Color.LightGray;` |
| **ReadOnly** | Prevent user editing | `integerTextBox1.ReadOnly = true;` |
| **DeleteSelectionOnNegative** | Delete selected text when minus pressed | `integerTextBox1.DeleteSelectionOnNegative = true;` |

---

## Common Use Cases

**Use Case 1: Financial Input with Constraints**
Create a textbox for dollar amounts (0 to 999,999):

```csharp
integerTextBox1.MinValue = 0;
integerTextBox1.MaxValue = 999999;
integerTextBox1.NumberGroupSeparator = ",";
integerTextBox1.NumberGroupSizes = new int[] { 3 };
```

**Use Case 2: Temperature Input (Negative & Positive)**
Allow temperatures from -50 to 50 degrees:

```csharp
integerTextBox1.MinValue = -50;
integerTextBox1.MaxValue = 50;
integerTextBox1.NegativeColor = Color.Blue;
integerTextBox1.PositiveColor = Color.Red;
```

**Use Case 3: Read-Only Display**
Show a value that users cannot modify:

```csharp
integerTextBox1.IntegerValue = 42;
integerTextBox1.ReadOnly = true;
integerTextBox1.ReadOnlyBackColor = Color.LightGray;
```

**Use Case 4: Null-Able Integer with Validation**
Allow null values with error handling:

```csharp
integerTextBox1.BindableValueChanged += (sender, e) =>
{
    if (integerTextBox1.BindableValue == null)
        MessageBox.Show("Value cleared (null)");
    else
        MessageBox.Show($"Value: {integerTextBox1.IntegerValue}");
};
```

---

## Next Steps

- Start with [Getting Started](references/getting-started.md) to install and create the control
- Customize appearance using [Visual Appearance](references/appearance.md)
- Handle data with [Data Formatting](references/data-formatting.md)
- Respond to user interactions with [Events](references/events.md)
