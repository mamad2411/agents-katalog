---
name: syncfusion-winui-masked-textbox
description: Guide for implementing Syncfusion WinUI MaskedTextBox (SfMaskedTextBox) for validated text input with customizable mask patterns. Use this when implementing masked input fields, formatted data entry (phone numbers, dates, SSN, IP addresses), or restricting text input to specific patterns in WinUI applications. This skill covers mask configuration, prompt characters, and error indication.
metadata:
 author: "Syncfusion Inc"
 version: "33.1.44"
---

# Implementing MaskedTextBox

Guide for implementing Syncfusion® WinUI MaskedTextBox (SfMaskedTextBox) — an advanced input control that restricts and formats user input using customizable mask patterns, supporting both simple and regex-based masks with error indication and validation.

## When to Use This Skill

Use this skill when you need to:
- **Create masked input fields** with pattern validation in WinUI applications
- **Implement phone number fields** with formatted input like (555) 123-4567
- **Add email validation** using regex patterns
- **Create date entry fields** with visual placeholders
- **Build product key inputs** like XXXXX-XXXXX-XXXXX
- **Validate SSN, credit cards, IP addresses** with custom masks
- **Show error indication** with icons and tooltips
- **Customize prompt characters** for empty fields
- **Format values** for display and clipboard operations
- **Add headers and descriptions** to input fields

This skill covers complete MaskedTextBox implementation including mask types, validation, error handling, and customization.

## Component Overview

**Control:** `SfMaskedTextBox`  
**Namespace:** `Syncfusion.UI.Xaml.Editors`  
**NuGet Package:** `Syncfusion.Editors.WinUI`  
**Platform:** WinUI 3 Desktop (.NET 5+)

The **SfMaskedTextBox** control provides:

- **Mask Types** - Simple (fixed-length) and RegEx (variable-length) patterns
- **Simple Masks** - Built-in elements: 0 (digit), L (letter), A (alphanumeric), etc.
- **RegEx Masks** - Full regex pattern support for complex validation
- **Prompt Character** - Customizable placeholder character (default '_')
- **Value Formatting** - Control how values appear with literals and prompts
- **Error Indication** - Built-in error types (Warning, Success, Critical, etc.)
- **Custom Errors** - Custom icons and border colors for validation
- **Header & Description** - Labels and help text for better UX
- **Events** - ValueChanging and ValueChanged for real-time validation

### Control Structure

```
SfMaskedTextBox
├── Header (optional) - Label above the control
├── Input Area - Masked text entry with prompt characters
├── Error Icon (optional) - Validation feedback indicator
└── Description (optional) - Help text below the control
```

## Documentation and Navigation Guide

### Getting Started

📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and NuGet package setup
- Adding control in XAML and code-behind
- Namespace imports
- Simple mask example (date pattern)
- RegEx mask example (email pattern)
- Setting prompt character
- Setting value property

### Mask Types

📄 **Read:** [references/mask-types.md](references/mask-types.md)
- Simple mask type for fixed-length inputs
- Simple mask elements (0, 9, #, L, ?, C, A, <, >)
- Element descriptions and usage
- RegEx mask type for variable-length inputs
- RegEx pattern elements and syntax
- Phone number mask examples
- Email pattern examples
- Product key patterns
- Custom mask creation

### Value Formatting

📄 **Read:** [references/value-formatting.md](references/value-formatting.md)
- Value property usage
- ValueMaskFormat options
- IncludeLiterals format
- IncludePrompt format
- ExcludePromptAndLiterals format
- Clipboard copy behavior
- Paste operations
- Retrieving formatted vs raw values

### Error Indication

📄 **Read:** [references/error-indication.md](references/error-indication.md)
- ErrorType property
- Built-in error types (None, Default, Warning, Information, Critical, Success)
- Setting error type based on validation
- Custom error type
- CustomErrorIcon property
- CustomErrorBorderBrush property
- ErrorContent property for tooltip messages
- Validation scenarios

### Customization

📄 **Read:** [references/customization.md](references/customization.md)
- Header property for labels
- HeaderTemplate for custom header design
- Description property for help text
- Styling the control
- Custom templates
- Visual appearance customization

### Events

📄 **Read:** [references/events.md](references/events.md)
- ValueChanging event (before change)
- ValueChanged event (after change)
- Event arguments and properties
- Validation with events
- Real-time feedback
- Canceling input changes

## Quick Start Example

### Phone Number Input with Validation

```xaml
<syncfusion:SfMaskedTextBox Width="200"
                            Header="Phone Number"
                            MaskType="Simple"
                            Mask="(000) 000-0000"
                            PromptChar="#"
                            ErrorType="Warning"
                            Description="Enter your 10-digit phone number"
                            ValueChanging="OnPhoneNumberChanging" />
```

```csharp
private void OnPhoneNumberChanging(object sender, MaskedTextBoxValueChangingEventArgs e)
{
    // Show success icon for valid input, warning otherwise
    var maskedTextBox = sender as SfMaskedTextBox;
    maskedTextBox.ErrorType = e.IsValid ? ErrorType.Success : ErrorType.Warning;
}
```

## Common Patterns

### Pattern 1: Date Entry with Simple Mask

```xaml
<syncfusion:SfMaskedTextBox Width="200"
                            Header="Date of Birth"
                            MaskType="Simple"
                            Mask="00/00/0000"
                            Value="12/31/1990" />
```

**Use when:** Fixed-format date entry (MM/DD/YYYY)

### Pattern 2: Email Validation with RegEx

```xaml
<syncfusion:SfMaskedTextBox Width="300"
                            Header="Email Address"
                            MaskType="RegEx"
                            Mask="[A-Za-z0-9._%-]+@[A-Za-z0-9]+\.[A-Za-z]{2,3}"
                            ErrorType="Information"
                            ValueChanging="OnEmailValidation" />
```

**Use when:** Variable-length input with pattern validation

### Pattern 3: Product Key with Uppercase Conversion

```xaml
<syncfusion:SfMaskedTextBox Width="300"
                            Header="Product Key"
                            MaskType="Simple"
                            Mask=">AAAAA-AAAAA-AAAAA-AAAAA"
                            Description="Format: XXXXX-XXXXX-XXXXX-XXXXX" />
```

**Use when:** Formatted serial numbers or license keys (> converts to uppercase)

### Pattern 4: Custom Error with Icon and Border

```xaml
<syncfusion:SfMaskedTextBox Width="250"
                            MaskType="Simple"
                            Mask="000-00-0000"
                            ErrorType="Custom"
                            CustomErrorIcon="ms-appx:///Assets/ErrorIcon.png"
                            CustomErrorBorderBrush="Red"
                            ErrorContent="Invalid SSN format" />
```

**Use when:** Need custom branding for error states

### Pattern 5: Credit Card with Formatted Display

```xaml
<syncfusion:SfMaskedTextBox Width="200"
                            Header="Credit Card"
                            MaskType="Simple"
                            Mask="0000 0000 0000 0000"
                            ValueMaskFormat="ExcludePromptAndLiterals" />
```

**Use when:** Display formatted input but return raw values

## Key Properties

| Property | Type | Description |
|----------|------|-------------|
| **Mask** | string | The pattern used to restrict input (e.g., "00/00/0000") |
| **MaskType** | MaskedTextBoxMaskType | Simple or RegEx mask type |
| **Value** | string | Current input value |
| **PromptChar** | char | Character shown for empty mask positions (default '_') |
| **ValueMaskFormat** | MaskedTextBoxValueMaskFormat | How value is formatted (literals, prompts) |
| **ErrorType** | ErrorType | Validation feedback type (None, Warning, Success, etc.) |
| **CustomErrorIcon** | ImageSource | Custom error icon for Custom error type |
| **CustomErrorBorderBrush** | Brush | Custom border brush for errors |
| **ErrorContent** | object | Tooltip content shown on error icon hover |
| **Header** | object | Label displayed above the control |
| **HeaderTemplate** | DataTemplate | Custom template for header |
| **Description** | object | Help text displayed below the control |

## Common Use Cases

### Use Case 1: Form with Multiple Validated Inputs
Create a registration form with phone, email, and SSN fields, each with appropriate masks and validation icons.

### Use Case 2: International Phone Numbers
Use RegEx masks to support various international phone number formats with country codes.

### Use Case 3: Credit Card Entry
Implement credit card input with formatted display (groups of 4 digits) and raw value for processing.

### Use Case 4: IP Address Entry
Use simple mask "000.000.000.000" with validation to ensure each octet is between 0-255.

### Use Case 5: Time Entry
Create time input fields with "00:00 >LL" mask supporting 24-hour format with AM/PM indicator.

### Use Case 6: Product Serial Number Scanner
Implement barcode-compatible input with uppercase conversion and segment validation.

### Use Case 7: Custom Validation Messages
Show contextual error messages based on specific validation rules using ErrorContent.

### Use Case 8: Multi-Language Support
Use regex patterns that adapt to different locale requirements for phone numbers and postal codes.

## Troubleshooting

**Issue: Mask not accepting input**
- Verify mask pattern matches expected input type (digits vs letters)
- Check MaskType is set correctly (Simple vs RegEx)
- Ensure mask elements are valid for chosen MaskType

**Issue: Value property not updating**
- Use ValueChanged event to track changes
- Check ValueMaskFormat if retrieved value seems wrong
- Ensure two-way binding: `Value="{x:Bind Property, Mode=TwoWay}"`

**Issue: Error icon not appearing**
- Set ErrorType to a value other than None
- For Custom type, provide CustomErrorIcon
- Ensure control has sufficient width to display icon

**Issue: RegEx mask not validating correctly**
- Escape special characters in XAML (use `\\.` for literal dot)
- Test regex pattern independently before using in mask
- Remember RegEx masks are for variable-length input

**Issue: Prompt character visible in value**
- Adjust ValueMaskFormat property
- Use ExcludePromptAndLiterals to get clean value
- Check if prompts are intentionally included

**Issue: Header or Description not showing**
- Verify property is set in XAML or code
- Check control height allows space for header/description
- Ensure HeaderTemplate syntax is correct if customizing

---

**Related Skills:**
- Parent Library: [implementing-syncfusion-winui-components](../../)
- WinUI Editors: Coming soon
- WinUI Data Validation: Coming soon
