---
name: syncfusion-winforms-autolabel
description: Guides implementation of the Syncfusion WinForms AutoLabel control for automatic label positioning with form controls. Use when users want to add labels that automatically reposition when controls move, create form layouts with paired label-control units, implement complex form designs with FlowLayout, or ensure labels stay synchronized with their associated controls. Covers labeling controls, positioning, spacing, size settings, theming, and events.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion WinForms AutoLabel Control

The AutoLabel control is a Label-inspired control that lets you pair a label with any other control. Once paired, the AutoLabel automatically repositions itself as the labeled control's position changes, ensuring labels and controls always stay synchronized.

## When to Use This Skill

Use the AutoLabel control when you need to:
- Add labels that automatically follow their associated controls
- Create dynamic form layouts where controls can move
- Implement complex form designs with FlowLayout manager
- Ensure labels always stay positioned correctly relative to controls
- Build forms that resize or reorganize controls dynamically
- Create professional forms with consistent label-control spacing
- Simplify form layout management with automatic positioning

## Installation

### NuGet Installation

```bash
Install-Package Syncfusion.Tools.Windows
```

### Assembly Reference

Add reference to:
- `Syncfusion.Shared.Base.dll`

## Quick Start

### Basic Setup

```csharp
using System;
using System.Windows.Forms;
using Syncfusion.Windows.Forms.Tools;

namespace AutoLabelDemo
{
    public partial class Form1 : Form
    {
        private AutoLabel autoLabel1;
        private TextBoxExt textBoxExt1;
        
        public Form1()
        {
            InitializeComponent();
            
            // Create a control to label (e.g., TextBox)
            textBoxExt1 = new TextBoxExt();
            textBoxExt1.Location = new System.Drawing.Point(150, 50);
            textBoxExt1.Size = new System.Drawing.Size(200, 20);
            
            // Create AutoLabel
            autoLabel1 = new AutoLabel();
            autoLabel1.Text = "Username:";
            autoLabel1.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Regular);
            
            // Pair the label with the control
            autoLabel1.LabeledControl = textBoxExt1;
            autoLabel1.Position = AutoLabelPosition.Left;
            autoLabel1.Gap = 10;
            
            // Add to form
            this.Controls.Add(textBoxExt1);
            this.Controls.Add(autoLabel1);
        }
    }
}
```

### Designer Setup

1. Drag `AutoLabel` control from Toolbox to Form
2. Drag another control (e.g., TextBox) to the form
3. Right-click AutoLabel → Properties → Set `LabeledControl` to your control
4. Configure `Position` and `Gap` properties
5. The label will now auto-position relative to the control

## Core Concepts

### Label-Control Pairing
The AutoLabel pairs with any control through the `LabeledControl` property. Once paired, the label automatically tracks the control's position.

### Automatic Repositioning
When the labeled control moves, the AutoLabel automatically adjusts its position based on the `Position` and `Gap` settings.

### FlowLayout Integration
FlowLayout managers treat AutoLabel-labeled control pairs as a single unit, enabling powerful dynamic form layouts.

## Navigation Guide

### 🚀 Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and assembly deployment
- Adding AutoLabel via Designer
- Adding AutoLabel programmatically
- Labeling a control
- Basic configuration
- Running your first AutoLabel application

### 📐 Positioning and Spacing
📄 **Read:** [references/positioning-spacing.md](references/positioning-spacing.md)
- Position property (Left, Top, Side, Custom)
- Gap setting between label and control
- DX and DY properties for fine control
- Custom positioning with mouse
- Spacing best practices

### 🎨 Appearance and Theming
📄 **Read:** [references/appearance-theming.md](references/appearance-theming.md)
- AutoSize for automatic label sizing
- BackColor and ForeColor customization
- Font settings
- TextAlign property
- SkinManager theming (Office 2016 styles)
- Visual styles

### ⚡ Events
📄 **Read:** [references/events.md](references/events.md)
- PropertyChanged event
- Handling label-control updates
- Event arguments
- Common event scenarios

### 🎯 Overview and Use Cases
📄 **Read:** [references/overview.md](references/overview.md)
- Component architecture
- FlowLayout integration
- Form layout patterns
- When to use AutoLabel vs standard Label

## Common Patterns

### Pattern 1: Simple Form with Left-Aligned Labels
```csharp
// Create form fields with left-aligned labels
AutoLabel nameLabel = new AutoLabel();
nameLabel.Text = "Name:";
nameLabel.LabeledControl = nameTextBox;
nameLabel.Position = AutoLabelPosition.Left;
nameLabel.Gap = 10;

AutoLabel emailLabel = new AutoLabel();
emailLabel.Text = "Email:";
emailLabel.LabeledControl = emailTextBox;
emailLabel.Position = AutoLabelPosition.Left;
emailLabel.Gap = 10;

this.Controls.Add(nameTextBox);
this.Controls.Add(nameLabel);
this.Controls.Add(emailTextBox);
this.Controls.Add(emailLabel);
```

### Pattern 2: Top-Aligned Labels (Vertical Form)
```csharp
AutoLabel addressLabel = new AutoLabel();
addressLabel.Text = "Address:";
addressLabel.LabeledControl = addressTextBox;
addressLabel.Position = AutoLabelPosition.Top;
addressLabel.Gap = 5;
addressLabel.AutoSize = true;
```

### Pattern 3: Custom Positioned Labels
```csharp
AutoLabel customLabel = new AutoLabel();
customLabel.Text = "Custom:";
customLabel.LabeledControl = myControl;
customLabel.Position = AutoLabelPosition.Custom;
customLabel.DX = -100;  // 100 pixels to the left
customLabel.DY = 15;    // 15 pixels down from control top
```

### Pattern 4: Themed Form with AutoLabels
```csharp
using Syncfusion.Windows.Forms;

// Apply Office 2016 theme to all labels
SkinManager.SetVisualStyle(label1, VisualTheme.Office2016Colorful);
SkinManager.SetVisualStyle(label2, VisualTheme.Office2016Colorful);
SkinManager.SetVisualStyle(label3, VisualTheme.Office2016Colorful);
```

### Pattern 5: FlowLayout with AutoLabel Pairs
```csharp
FlowLayoutPanel flowPanel = new FlowLayoutPanel();
flowPanel.FlowDirection = FlowDirection.TopDown;
flowPanel.Dock = DockStyle.Fill;

// FlowLayout treats AutoLabel + Control as one unit
flowPanel.Controls.Add(firstNameTextBox);
flowPanel.Controls.Add(firstNameLabel);  // Paired with firstNameTextBox
flowPanel.Controls.Add(lastNameTextBox);
flowPanel.Controls.Add(lastNameLabel);   // Paired with lastNameTextBox

// Labels automatically move with their controls
this.Controls.Add(flowPanel);
```

## Key Properties Reference

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `LabeledControl` | Control | null | The control that this label is paired with |
| `Position` | AutoLabelPosition | Left | Relative position: Left, Top, Side, Custom |
| `Gap` | int | 0 | Horizontal and vertical gap between label and control |
| `DX` | int | 0 | Horizontal distance from label left to control left |
| `DY` | int | 0 | Vertical distance from label top to control top |
| `AutoSize` | bool | false | Automatically resize based on font size |
| `Text` | string | "" | Label text content |
| `TextAlign` | ContentAlignment | TopLeft | Text alignment within label |
| `BackColor` | Color | Control | Background color of the label |
| `ForeColor` | Color | ControlText | Text color of the label |
| `Font` | Font | - | Font for the label text |

## Position Options

| Position | Behavior |
|----------|----------|
| **Left** | Label appears to the left of the control |
| **Top** | Label appears above the control |
| **Side** | Label appears on the side (right) of the control |
| **Custom** | Manual positioning using DX and DY or mouse drag |

## Events

| Event | Description |
|-------|-------------|
| `PropertyChanged` | Fired when LabeledControl, Gap, or Position properties change |

## Best Practices

1. **Pair Before Adding**: Set `LabeledControl` before adding to form for proper initialization

2. **Use Gap for Spacing**: Use the `Gap` property instead of manual positioning for consistent spacing

3. **Choose Appropriate Position**: 
   - Use `Left` for horizontal forms
   - Use `Top` for stacked/vertical forms
   - Use `Custom` only when necessary

4. **Enable AutoSize**: Set `AutoSize = true` for labels that don't wrap text

5. **FlowLayout Integration**: Leverage FlowLayout to treat label-control pairs as units

6. **Consistent Theming**: Apply the same visual style to all AutoLabels in a form

7. **Test Movement**: Verify labels follow controls when controls are repositioned dynamically

8. **Avoid Overlapping**: Ensure Gap and positioning prevent label-control overlap

## Visual Styles

Supported themes via SkinManager:
- **Office2016Colorful**
- **Office2016Black**
- **Office2016DarkGray**
- **Office2016White**

```csharp
SkinManager.SetVisualStyle(this.autoLabel1, VisualTheme.Office2016Colorful);
```

## Framework Support

- .NET Framework 4.5 and above
- .NET 6.0, .NET 7.0, .NET 8.0 (Windows)
- .NET Core 3.1 (Windows)

## Additional Resources

- [Syncfusion AutoLabel Documentation](https://help.syncfusion.com/windowsforms/autolabel/overview)
- [API Reference](https://help.syncfusion.com/cr/windowsforms/Syncfusion.Windows.Forms.Tools.AutoLabel.html)
- [Knowledge Base Articles](https://www.syncfusion.com/kb/windowsforms/autolabel)
- [GitHub Samples](https://github.com/syncfusion/winforms-demos)

## Related Controls

- **Label**: Standard Windows Forms label (no auto-positioning)
- **FlowLayoutPanel**: Container for dynamic layouts
- **TextBoxExt**: Enhanced textbox often used with AutoLabel
- **AutoSizeForm**: Form with automatic sizing capabilities

## Troubleshooting

**Issue**: Label doesn't move with control
- Ensure `LabeledControl` property is set
- Verify both label and control are added to the same container
- Check that the control's position is actually changing

**Issue**: Label positioning is off
- Adjust `Gap` property for spacing
- Use `DX` and `DY` for fine-tuning if needed
- Verify `Position` property is set correctly

**Issue**: Label overlaps control
- Increase `Gap` value
- Choose different `Position` (e.g., Top instead of Left)
- Check control sizes allow sufficient space

**Issue**: Theme not applied
- Ensure SkinManager assembly is referenced
- Verify theme is supported (Office 2016 variants only)
- Apply theme after adding control to form
