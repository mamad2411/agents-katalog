---
name: syncfusion-winforms-domainupdownext
description: Implement and configure the Syncfusion DomainUpdownExt control in Windows Forms applications. Use this skill when you need to create dropdown/selection controls with spin buttons, customize appearance, manage items, and enable keyboard navigation in WinForms projects.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing DomainUpdownExt in Windows Forms

DomainUpdownExt is an advanced Windows Forms control that provides a modern dropdown interface with spin buttons for value selection. It's ideal for scenarios where users need to browse through a predefined list of items using increment/decrement buttons or keyboard navigation.

## When to Use This Skill

Use this skill when you need to:
- Create a dropdown control with spin button navigation
- Allow users to browse through a list of predefined values
- Customize control appearance (borders, colors, styles)
- Enable arrow key navigation for value selection
- Configure text alignment and spin button orientation
- Handle user interactions and keyboard events
- Add dynamic items based on user input

## Component Overview

DomainUpdownExt combines the functionality of a text box with spin buttons and a predefined list of items. Unlike a standard ComboBox, it displays only the current item and lets users navigate through the list using arrow keys or spin buttons.

**Key Capabilities:**
- Item management with programmatic access
- Spin button customization (orientation, alignment)
- Keyboard support (arrow keys, keyboard events)
- Appearance customization (borders, colors, text alignment)
- Event handling for state changes
- Text and item validation

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Assembly dependencies and project setup
- Adding control via designer
- Adding control manually in code
- Creating your first DomainUpdownExt control
- Basic item management

### Text and Item Management
📄 **Read:** [references/text-and-items.md](references/text-and-items.md)
- Adding and removing items from the collection
- Text alignment properties
- MaxLength configuration
- Managing selected items programmatically
- Item validation patterns

### Spin Button Control
📄 **Read:** [references/spinbutton-control.md](references/spinbutton-control.md)
- SpinOrientation property (horizontal vs. vertical)
- UpDownAlign property (left vs. right alignment)
- Configuring spin button appearance
- Default button behaviors

### Appearance and Customization
📄 **Read:** [references/appearance-customization.md](references/appearance-customization.md)
- Border styles and properties
- Background and foreground colors
- Border 3D styles
- Customizing control look and feel
- Visual appearance patterns

### Keyboard Navigation and Interaction
📄 **Read:** [references/keyboard-and-interaction.md](references/keyboard-and-interaction.md)
- Arrow key support (InterceptArrowKeys property)
- KeyDown event handling
- UpButton and DownButton methods
- Programmatic value browsing
- Keyboard navigation patterns

### Advanced Usage and Patterns
📄 **Read:** [references/advanced-usage.md](references/advanced-usage.md)
- Adding items at runtime based on user input
- Programmatic navigation through values
- Event handling strategies
- Common use cases and patterns
- Best practices for interaction design

## Quick Start Example

Create a basic DomainUpdownExt control with items and keyboard navigation:

```csharp
using Syncfusion.Windows.Forms.Tools;
using System.Windows.Forms;

public class Form1 : Form
{
    private DomainUpDownExt domainUpDownExt1;

    public Form1()
    {
        // Create control
        domainUpDownExt1 = new DomainUpDownExt();
        
        // Add items
        domainUpDownExt1.Items.Add("Option 1");
        domainUpDownExt1.Items.Add("Option 2");
        domainUpDownExt1.Items.Add("Option 3");
        domainUpDownExt1.Items.Add("Option 4");
        
        // Configure appearance
        domainUpDownExt1.BorderStyle = BorderStyle.FixedSingle;
        domainUpDownExt1.BackColor = System.Drawing.Color.White;
        domainUpDownExt1.SpinOrientation = Orientation.Vertical;
        
        // Enable keyboard navigation
        domainUpDownExt1.InterceptArrowKeys = true;
        
        // Add to form
        this.Controls.Add(domainUpDownExt1);
    }
}
```

## Common Patterns

### Pattern 1: Vertical Spin Button with Right Alignment
```csharp
domainUpDownExt1.SpinOrientation = Orientation.Vertical;
domainUpDownExt1.UpDownAlign = LeftRightAlignment.Right;
```

### Pattern 2: Horizontal Spin Button with Left Alignment
```csharp
domainUpDownExt1.SpinOrientation = Orientation.Horizontal;
domainUpDownExt1.UpDownAlign = LeftRightAlignment.Left;
```

### Pattern 3: Custom Appearance with Colored Border
```csharp
domainUpDownExt1.BorderStyle = BorderStyle.FixedSingle;
domainUpDownExt1.BorderColor = System.Drawing.Color.Blue;
domainUpDownExt1.BackColor = System.Drawing.Color.LightGray;
```

### Pattern 4: Programmatic Navigation
```csharp
domainUpDownExt1.UpButton();    // Navigate to previous item
domainUpDownExt1.DownButton();  // Navigate to next item
```

## Key Properties

| Property | Type | Purpose | Common Values |
|----------|------|---------|----------------|
| `Items` | Collection | Gets the collection of items | Add/Remove items |
| `SelectedIndex` | Int32 | Gets/sets the selected item index | 0 to Items.Count - 1 |
| `Text` | String | Gets/sets the current display text | Any string |
| `SpinOrientation` | Orientation | Controls spin button direction | Vertical, Horizontal |
| `UpDownAlign` | LeftRightAlignment | Controls spin button position | Left, Right |
| `InterceptArrowKeys` | Boolean | Enable/disable arrow key navigation | true, false |
| `BorderStyle` | BorderStyle | Sets border appearance | FixedSingle, Fixed3D, None |
| `BorderColor` | Color | Sets border color | Any System.Drawing.Color |
| `BackColor` | Color | Sets background color | Any System.Drawing.Color |
| `TextAlign` | HorizontalAlignment | Controls text alignment | Left, Center, Right |
| `MaxLength` | Int32 | Maximum text length | 0 to 32768 |

## Common Use Cases

1. **Numeric Range Selection** - Allow users to select values from a predefined range
2. **Category Navigation** - Browse through predefined categories or options
3. **Status Selection** - Choose from discrete status values in a compact interface
4. **Configuration Options** - Select from a set of predefined configuration values
5. **Priority Levels** - Choose priority from a discrete set of values
6. **Difficulty Levels** - Select difficulty/intensity levels with spin navigation
