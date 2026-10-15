---
name: syncfusion-winforms-calculator
description: Implement and configure Syncfusion Windows Forms Calculator control for numeric input and calculation interfaces. Use this when creating calculator UIs, handling calculator events, supporting keyboard input, displaying calculation results, or integrating calculator functionality into Windows Forms applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion Windows Forms Calculator

The Syncfusion Calculator control is a fully-featured calculator for Windows Forms applications. It supports both standard and financial layouts, keyboard operations, memory functions, and can be embedded as a popup control.

## When to Use This Skill

Use the Calculator control when your application needs:
- Standard or scientific calculator functionality
- Keyboard and mouse input support
- Memory operations (MS, MR, M+, MC)
- Popup calculator attached to input fields
- Display of calculation results and intermediate values
- Support for both C# and VB.NET

## Component Overview

**CalculatorControl** — The main calculator component with layout modes, keyboard support, and value calculation events

**PopupCalculator** — A wrapper class to display CalculatorControl as a popup attached to buttons or other controls

### Key Characteristics

- Two layout modes: Standard (default) and Financial
- Full keyboard support with standard calculator shortcuts
- Memory management (MS, MR, M+, MC operations)
- Display TextBox with customizable alignment and font
- Event-driven architecture (ValueCalculated, Closing events)
- Culture-aware value formatting
- Lightweight, embeddable component

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Assembly dependencies and NuGet installation
- Create Windows Forms project with Calculator
- Add control via Designer or manual code
- Required namespaces and basic instantiation

### Layout and Appearance
📄 **Read:** [references/layout-and-appearance.md](references/layout-and-appearance.md)
- Standard vs Financial layout modes
- Background color and images
- Border styles
- Button spacing and styling
- Display text alignment

### Display and Value Handling
📄 **Read:** [references/display-and-value-handling.md](references/display-and-value-handling.md)
- Display TextBox properties and visibility
- Managing numeric values (String vs Double)
- Culture-specific formatting
- Font customization

### Keyboard and Runtime Features
📄 **Read:** [references/keyboard-and-runtime-features.md](references/keyboard-and-runtime-features.md)
- Complete keyboard shortcut reference
- Memory operations (MS, MR, M+, MC)
- Numeric operations and calculations
- Special functions (sqrt, reciprocal, percentage)

### Events and Interaction
📄 **Read:** [references/events-and-interaction.md](references/events-and-interaction.md)
- ValueCalculated event handling
- Closing event for PopupCalculator
- LastAction property for determining completed operations
- Error condition handling

### Popup Calculator
📄 **Read:** [references/popup-calculator.md](references/popup-calculator.md)
- Creating PopupCalculator instances
- ParentControl association
- Popup alignment options
- Displaying and using popup calculator

## Quick Start Example

```csharp
using Syncfusion.Windows.Forms.Tools;
using System.Windows.Forms;

public partial class Form1 : Form
{
    public Form1()
    {
        InitializeComponent();
        
        // Create Calculator control
        CalculatorControl calculatorControl = new CalculatorControl();
        calculatorControl.Size = new System.Drawing.Size(300, 250);
        calculatorControl.LayoutType = CalculatorLayoutTypes.WindowsStandard;
        
        // Add to form
        this.Controls.Add(calculatorControl);
        
        // Handle value changes
        calculatorControl.ValueCalculated += (sender, args) =>
        {
            if (!args.ErrorCondition && args.LastAction == CalcActions.CalcOperatorEquals)
            {
                MessageBox.Show($"Result: {calculatorControl.Value}");
            }
        };
    }
}
```

## Common Patterns

### Pattern 1: Standard Calculator with Event Handling
Create a calculator that logs all operations and displays final results when "=" is pressed.

```csharp
CalculatorControl calc = new CalculatorControl();
calc.ValueCalculated += (sender, args) =>
{
    if (!args.ErrorCondition && args.LastAction == CalcActions.CalcOperatorEquals)
    {
        // Process final value
        double result = calc.DoubleValue;
    }
};
```

### Pattern 2: Popup Calculator on Button Click
Embed calculator as a popup that displays when button is clicked.

```csharp
PopupCalculator popupCalc = new PopupCalculator();
popupCalc.ParentControl = myButton;
popupCalc.PopupCalculatorAlignment = CalculatorPopupAlignment.Right;
popupCalc.Closing += (sender, args) => 
{
    decimal finalValue = args.FinalValue;
};
```

### Pattern 3: Financial Layout with Custom Styling
Display a financial calculator with custom appearance.

```csharp
CalculatorControl calc = new CalculatorControl();
calc.LayoutType = CalculatorLayoutTypes.Financial;
calc.DisplayTextAlign = System.Windows.Forms.HorizontalAlignment.Right;
calc.UseVerticalAndHorizontalSpacing = true;
calc.HorizontalSpacing = 5;
calc.VerticalSpacing = 5;
```

## Key Properties

| Property | Purpose | Notes |
|----------|---------|-------|
| `LayoutType` | Switch between Standard and Financial layouts | Default is WindowsStandard |
| `ShowDisplayArea` | Show/hide the display TextBox | True by default |
| `DoubleValue` | Get/set numeric value as double | Use for calculations |
| `Value` | Get current value | Returns CalculatorValue object |
| `Culture` | Set culture for number formatting | Affects decimal separator |
| `DisplayTextAlign` | Align display text (Left/Center/Right) | Default is Right |
| `FlatStyle` | Button appearance (Flat/Popup/Standard) | Changes button rendering |

## Common Use Cases

1. **Financial Calculator** — Use Financial layout mode with memory operations for accounting applications
2. **Quick Calculation Popup** — Attach PopupCalculator to TextBox for quick value entry
3. **Multi-Input Form** — Place calculator on form for users to compute values before entering
4. **Keyboard-Only Input** — Calculator accessible via keyboard shortcuts in keyboard-driven apps
5. **Value Validation** — Display calculator result in TextBox after "=" pressed

---

## Next Steps

- Start with [Getting Started](references/getting-started.md) to add the control to your project
- Explore [Layout and Appearance](references/layout-and-appearance.md) to customize the UI
- Review [Events and Interaction](references/events-and-interaction.md) to handle user operations
