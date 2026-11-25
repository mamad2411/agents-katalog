---
name: syncfusion-winforms-button-edit
description: Implement Syncfusion WinForms ButtonEdit control for creating text input with embedded buttons. Use this skill when users need to build file/folder browsers, dropdown controls, or custom input controls with action buttons. Includes assembly setup, designer/code approaches, appearance customization, child button configuration, events, and interaction patterns.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion WinForms ButtonEdit

The ButtonEdit control embeds a text box with customizable child buttons to create interfaces like file browsers, dropdown controls, or specialized input controls. It combines text input capability with actionable buttons.

## When to Use This Skill

- **File/folder browser UI:** Create dialogs with browse buttons
- **Custom dropdown input:** Build dropdown or selection controls
- **Date/time picker:** Implement date picker with calendar button
- **Multi-button text fields:** Create input with multiple action buttons (clear, calculate, search, etc.)
- **Specialized data input:** Currency, percentage, or validated text input with action buttons
- **Dynamic button arrangement:** Position buttons left or right of textbox

## Documentation & Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Assembly deployment and NuGet setup
- Creating ButtonEdit in Visual Studio designer
- Adding ButtonEdit programmatically
- Embedding custom textbox types
- Adding child buttons to collection

### Appearance & Styling
📄 **Read:** [references/appearance-styling.md](references/appearance-styling.md)
- Visual styles and button styles (Office2007, Office2016, Metro, etc.)
- Custom colors and Office color schemes
- Border styles and customization
- Size constraints (MinimumSize, MaximumSize)
- Font and foreground colors
- Text casing options

### Child Button Customization
📄 **Read:** [references/child-button-customization.md](references/child-button-customization.md)
- Button types and border styles
- Button alignment (Left/Right positioning)
- Image and text settings
- Flat style configuration
- Focus and tab navigation
- Hiding buttons at runtime

### Events & Interaction
📄 **Read:** [references/events-and-interaction.md](references/events-and-interaction.md)
- ButtonClicked event handling
- Border property change events
- Child button click events
- Mouse events (MouseDown, MouseUp, MouseEnter, MouseLeave, MouseHover)
- Complete calendar picker example

## Quick Start

```csharp
// Add ButtonEdit through code
using Syncfusion.Windows.Forms.Tools;

public Form1()
{
    InitializeComponent();
    
    // Create ButtonEdit control
    ButtonEdit buttonEdit = new ButtonEdit();
    buttonEdit.Location = new Point(50, 50);
    buttonEdit.Size = new Size(250, 21);
    buttonEdit.Name = "buttonEdit1";
    this.Controls.Add(buttonEdit);
    
    // Add child button
    ButtonEditChildButton childButton = new ButtonEditChildButton();
    childButton.Text = "Browse";
    childButton.ButtonAlign = ButtonAlignment.Right;
    buttonEdit.Buttons.Add(childButton);
    
    // Handle button click
    buttonEdit.ButtonClicked += (s, e) => 
    {
        MessageBox.Show("Button clicked!");
    };
}
```

## Common Patterns

### File Browser Pattern
Create a file browser using ButtonEdit with a browse button that opens FolderBrowserDialog:

```csharp
ButtonEdit folderEdit = new ButtonEdit();
ButtonEditChildButton browseBtn = new ButtonEditChildButton();
browseBtn.Text = "...";
folderEdit.Buttons.Add(browseBtn);

folderEdit.ButtonClicked += (s, e) => 
{
    FolderBrowserDialog dialog = new FolderBrowserDialog();
    if (dialog.ShowDialog() == DialogResult.OK)
    {
        folderEdit.TextBox.Text = dialog.SelectedPath;
    }
};
```

### Multi-Button Input Pattern
Multiple buttons with different actions on same control:

```csharp
ButtonEdit inputEdit = new ButtonEdit();

// Clear button (left)
ButtonEditChildButton clearBtn = new ButtonEditChildButton();
clearBtn.Text = "C";
clearBtn.ButtonAlign = ButtonAlignment.Left;
inputEdit.Buttons.Add(clearBtn);

// Calculate button (right)
ButtonEditChildButton calcBtn = new ButtonEditChildButton();
calcBtn.Text = "=";
calcBtn.ButtonAlign = ButtonAlignment.Right;
inputEdit.Buttons.Add(calcBtn);

inputEdit.ButtonClicked += (s, e) => 
{
    if (e.ClickedButton == clearBtn)
        inputEdit.TextBox.Text = string.Empty;
    else if (e.ClickedButton == calcBtn)
        inputEdit.TextBox.Text = "Calculate...";
};
```

### Custom Textbox Integration
Replace default textbox with specialized textbox:

```csharp
ButtonEdit buttonEdit = new ButtonEdit();

// Use specialized textbox
PercentTextBox percentBox = new PercentTextBox();
buttonEdit.TextBox = percentBox;
buttonEdit.Controls.Add(percentBox);

ButtonEditChildButton btn = new ButtonEditChildButton();
btn.Text = "%";
buttonEdit.Buttons.Add(btn);
```

## Key Props & Configuration

| Property | Purpose |
|----------|---------|
| **TextBox** | Embedded textbox control (can replace with custom textbox) |
| **Buttons** | Collection of ButtonEditChildButton controls |
| **ButtonStyle** | Visual style (Office2007, Office2016, Metro, etc.) |
| **UseVisualStyle** | Enable visual style rendering |
| **Border3DStyle** | Border appearance (Raised, Sunken, Flat, etc.) |
| **ShowTextBox** | Show/hide embedded textbox |
| **MinimumSize / MaximumSize** | Size constraints |
| **CharacterCasing** | Text casing (Upper, Lower, Normal) |

---

**Next Steps:** Select a reference above based on what you need to implement, or start with "Getting Started" for setup instructions.
