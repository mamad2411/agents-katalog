---
name: syncfusion-winforms-masked-textbox
description: Implement masked text input controls in WinForms applications. Use this skill whenever the user needs to create input fields with format masks (phone numbers, IP addresses, dates, currency), validate formatted input, restrict data entry to specific patterns, or configure how user input behaves with mask constraints.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing MaskedEditBox in Syncfusion WinForms

The **MaskedEditBox** control is a specialized input control for collecting formatted data with predefined patterns. It provides visual cues and input constraints through mask definitions, making it ideal for standardized data entry like phone numbers, IP addresses, and SSNs.

## When to Use MaskedEditBox

Use this control when you need to:
- Restrict user input to specific patterns (phone: `(###) ###-####`)
- Provide visual placeholders for expected data format
- Validate input as users type without separate validation logic
- Handle common patterns: phone numbers, IP addresses, dates, currency
- Prevent invalid data entry at the control level
- Display consistent formatting across your application

**Do NOT use** if users need completely free-form text input or when data format is unpredictable.

## Component Overview

### Key Concepts

**Mask:** A string defining the input format using:
- **Mask characters** (placeholders like `#` for digits, `&` for letters)
- **Literal characters** (fixed symbols like parentheses, dashes in `(###) ###-####`)

**Examples:**
- US Phone: `(###) ###-####`
- IP Address: `###.###.###.###`
- Social Security: `###-##-####`
- Date (MM/DD/YYYY): `##/##/####`

### Core Features

- **Multiple Modes:** ClipMode (strip separators), InputMode (include separators), UsageMode (programmatic)
- **Appearance Control:** Borders, fonts, colors, display options
- **Data Handling:** Separate Text (with masks) and Value (mask characters only)
- **Separators:** Date, decimal, thousand, time separators for regional formats
- **Events:** Input validation, completion, and interaction events

## Documentation Navigation

Read the references below based on your implementation needs:

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and assembly setup
- Adding MaskedEditBox via designer
- Adding MaskedEditBox via code
- Basic initialization

### Mask Configuration
📄 **Read:** [references/mask-settings.md](references/mask-settings.md)
- Mask character types and syntax
- Creating phone number masks
- IP address masks
- Custom mask patterns

### Behavior Modes
📄 **Read:** [references/behavior-modes.md](references/behavior-modes.md)
- ClipMode: Output format control
- InputMode: User input behavior
- UsageMode: Programmatic usage
- Selecting the right mode for your use case

### Text and Value Handling
📄 **Read:** [references/text-and-value-handling.md](references/text-and-value-handling.md)
- Text property (includes mask literals)
- Value property (mask characters only)
- DataGroups configuration
- Separator settings (Date, Decimal, Thousand, Time)
- Input validation patterns

### Appearance Settings
📄 **Read:** [references/appearance-settings.md](references/appearance-settings.md)
- Border styles and colors
- Font properties and sizes
- Display options and visibility
- Read-only mode
- Enabled/disabled states

### Events and Validation
📄 **Read:** [references/events-and-validation.md](references/events-and-validation.md)
- Available MaskedEditBox events
- Input validation events
- Completion and focus events
- Event handling examples

## Quick Start Example

```csharp
using Syncfusion.Windows.Forms.Tools;

// Create MaskedEditBox for phone number
MaskedEditBox phoneInput = new MaskedEditBox();
phoneInput.Mask = "(###) ###-####";  // US phone format
phoneInput.Location = new Point(10, 10);
phoneInput.Size = new Size(200, 25);
phoneInput.Placeholder = "(123) 456-7890";

// Add to form
this.Controls.Add(phoneInput);

// Access entered value
string phoneValue = phoneInput.Value;  // Without mask characters: "1234567890"
string phoneText = phoneInput.Text;    // With mask: "(123) 456-7890"
```

## Common Patterns

### Phone Number (US Format)
```csharp
maskedEditBox.Mask = "(###) ###-####";
```

### IP Address
```csharp
maskedEditBox.Mask = "###.###.###.###";
```

### Social Security Number
```csharp
maskedEditBox.Mask = "###-##-####";
```

### Date (MM/DD/YYYY)
```csharp
maskedEditBox.Mask = "##/##/####";
```

### Zip Code (US)
```csharp
maskedEditBox.Mask = "#####";
// Optional: Extended format
maskedEditBox.Mask = "#####-####";
```

## Key Properties

| Property | Purpose | Example |
|----------|---------|---------|
| `Mask` | Defines the input format pattern | `"(###) ###-####"` |
| `Text` | Gets/sets text including mask literals | `"(123) 456-7890"` |
| `Value` | Gets/sets text without mask characters | `"1234567890"` |
| `ClipMode` | Controls output format when mask is removed | `ClipModes.IncludeLiterals` |
| `InputMode` | Controls user input behavior | `InputModes.IgnoreSeparators` |
| `Border3DStyle` | Border appearance | `Border3DStyle.Raised` |
| `Font` | Font properties (name, size, style) | `new Font("Arial", 10)` |
| `ForeColor` | Text color | `Color.Black` |
| `BackColor` | Background color | `Color.White` |
| `ReadOnly` | Prevent user input | `true/false` |
| `Enabled` | Enable/disable control | `true/false` |

## Common Use Cases

### 1. Phone Number Input with Validation
Collect phone numbers in a standard format, preventing invalid entry at the control level.

### 2. International Format Support
Configure region-specific separators and date/time formats using separator properties.

### 3. Financial Data Entry
Use for currency input, account numbers, or formatted numeric data with controlled precision.

### 4. Medical/Government Forms
Enforce specific formats for medical IDs, social security numbers, and registration codes.

### 5. Network Configuration
IP addresses, MAC addresses, and other network identifiers requiring fixed formats.

---

**Next Steps:**
1. Start with [getting-started.md](references/getting-started.md) to set up the control
2. Choose your mask format from [mask-settings.md](references/mask-settings.md)
3. Configure behavior in [behavior-modes.md](references/behavior-modes.md)
4. Handle data with [text-and-value-handling.md](references/text-and-value-handling.md)
5. Customize appearance in [appearance-settings.md](references/appearance-settings.md)
6. Add events from [events-and-validation.md](references/events-and-validation.md)
