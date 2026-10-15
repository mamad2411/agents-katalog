---
name: syncfusion-winforms-button
description: Guide developers to implement and customize the Syncfusion Windows Forms SfButton control for desktop applications. Use this when creating interactive buttons with text, images, styling, and theming in Windows Forms applications. Covers implementation, customization, and interaction handling.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion Windows Forms SfButton

Welcome to the comprehensive guide for implementing and customizing the **Syncfusion Windows Forms SfButton** control. SfButton is an advanced button control that provides rich text, image support, extensive customization options, and professional theming capabilities.

## When to Use This Skill

Use this skill whenever you need to:
- Create interactive buttons in Windows Forms applications
- Display text and images together on buttons
- Customize button appearance for different states (hover, pressed, focused, disabled)
- Implement rich text formatting in buttons
- Apply themes and styling to buttons
- Handle button click events and user interactions
- Create icon-only or image-only buttons
- Show tooltips on button hover
- Set Accept or Cancel buttons for forms
- Implement animated GIF images in buttons

## Component Overview

**SfButton** is an advanced button control superior to the standard Windows Forms Button. Key capabilities include:

- **Rich Content**: Display text, images, rich text, and animated GIFs
- **State-Based Customization**: Customize appearance for hover, pressed, focused, and disabled states
- **Professional Theming**: Built-in Office 2016 themes (Colorful, White, DarkGray, Black)
- **Text Control**: Support for text wrapping, trimming with ellipsis, and rich text formatting
- **Auto-Sizing**: Automatic button resizing based on content
- **Flexible Positioning**: Control image and text alignment, positioning, and spacing
- **Event Support**: Full support for click events, focus handling, and user interactions
- **Background Customization**: Solid colors, gradients, and background images

---

## Documentation Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)

Start here to learn:
- Assembly dependencies and NuGet installation
- Adding SfButton to forms (designer and code)
- Basic button setup with text and properties
- Handling click events
- First working example

### Button Types & Content
📄 **Read:** [references/button-types-and-content.md](references/button-types-and-content.md)

Learn how to create different button styles:
- Text and image buttons
- Image-only and icon-only buttons
- Text and image positioning using TextImageRelation
- Image size customization
- Rich text support and formatting
- Text wrapping and ellipsis trimming
- Content alignment (text and image)
- Auto-sizing buttons

### Appearance & Styling
📄 **Read:** [references/appearance-and-styling.md](references/appearance-and-styling.md)

Master button styling and customization:
- Solid color backgrounds
- Gradient brush backgrounds
- Background images with layouts
- Customizing appearance by button state
- Back color and fore color in all states
- Image changes in hover, pressed, focused, disabled states
- Border customization per state
- Focus rectangle visibility
- Rounded rectangle button implementation
- Animated GIF images

### Events & Interactions
📄 **Read:** [references/events-and-interactions.md](references/events-and-interactions.md)

Implement button interactions:
- Click event handling
- Setting Accept buttons for forms (ENTER key)
- Setting Cancel buttons for forms (ESC key)
- Tooltip support with SfToolTip
- Focus and keyboard handling


---

## Quick Start Example

Here's a minimal example to get started with SfButton:

```csharp
using Syncfusion.WinForms.Buttons;
using System.Windows.Forms;

public partial class Form1 : Form
{
    public Form1()
    {
        InitializeComponent();
        
        // Create and configure SfButton
        SfButton sfButton1 = new SfButton();
        sfButton1.Text = "Click Me";
        sfButton1.Font = new System.Drawing.Font("Segoe UI", 10F);
        sfButton1.Location = new System.Drawing.Point(50, 50);
        sfButton1.Size = new System.Drawing.Size(120, 40);
        
        // Add click event
        sfButton1.Click += SfButton1_Click;
        
        // Add to form
        this.Controls.Add(sfButton1);
    }
    
    private void SfButton1_Click(object sender, System.EventArgs e)
    {
        MessageBox.Show("Button clicked!");
    }
}
```

---

## Common Patterns

### Pattern 1: Button with Image and Text
```csharp
sfButton1.Text = "Save";
sfButton1.Image = Image.FromFile(@"save-icon.png");
sfButton1.TextImageRelation = TextImageRelation.ImageBeforeText;
sfButton1.ImageSize = new Size(20, 20);
```

### Pattern 2: Icon-Only Button
```csharp
sfButton1.Text = "";  // Empty text
sfButton1.Image = Image.FromFile(@"icon.png");
sfButton1.ImageSize = new Size(24, 24);
sfButton1.Style.BackColor = Color.White;
sfButton1.Style.Border = null;
```

### Pattern 3: Button with State-Based Colors
```csharp
sfButton1.Style.BackColor = Color.LightBlue;
sfButton1.Style.ForeColor = Color.Black;
sfButton1.Style.HoverBackColor = Color.Blue;
sfButton1.Style.HoverForeColor = Color.White;
sfButton1.Style.PressedBackColor = Color.DarkBlue;
sfButton1.Style.PressedForeColor = Color.White;
```

### Pattern 4: Auto-Sizing Button
```csharp
sfButton1.Text = "Variable Length Content";
sfButton1.AutoSize = true;  // Auto-adjust to content
sfButton1.Font = new Font("Segoe UI", 11F);
```

### Pattern 5: Themed Button
```csharp
// In Program.cs Main():
SfSkinManager.LoadAssembly(typeof(Office2016Theme).Assembly);

// In form:
sfButton1.ThemeName = "Office2016Colorful";
```

---

## Key Properties at a Glance

| Property | Type | Purpose |
|----------|------|---------|
| `Text` | string | Button display text |
| `Image` | Image | Button image/icon |
| `ImageSize` | Size | Dimensions of displayed image |
| `TextImageRelation` | TextImageRelation | Position of image relative to text |
| `TextAlign` | ContentAlignment | Text alignment within button |
| `ImageAlign` | ContentAlignment | Image alignment within button |
| `AutoSize` | bool | Auto-fit button to content |
| `AllowWrapText` | bool | Enable text wrapping |
| `AutoEllipsis` | bool | Show ellipsis for trimmed text |
| `AllowRichText` | bool | Enable rich text formatting |
| `BackgroundImage` | Image | Background fill image |
| `FocusRectangleVisible` | bool | Show focus indicator rectangle |
| `ThemeName` | string | Apply built-in theme |
| `Style` | ButtonVisualStyle | Access appearance customization |

---

## Common Use Cases

1. **Save/Submit Button**: Text with icon, colored background, hover effects
2. **Icon Toolbar**: Image-only buttons arranged in rows
3. **Themed Dialog Buttons**: Accept/Cancel with consistent theming
4. **Rich Text Buttons**: Formatted text with custom colors
5. **Dynamic Buttons**: Buttons that change appearance based on state
6. **Form Control Buttons**: Accept button (ENTER), Cancel button (ESC)
7. **Multi-Content Buttons**: Text above/below image with custom alignment

---

## Next Steps

1. ✅ Review the **Getting Started** guide to set up your first SfButton
2. ✅ Choose a button style from **Button Types & Content** that matches your UI
3. ✅ Apply styling from **Appearance & Styling** for professional look
4. ✅ Implement interactions from **Events & Interactions**

---

## Assembly Dependencies

Required assemblies for SfButton:
- `Syncfusion.Core.WinForms` (Main assembly containing SfButton)
- `Syncfusion.Shared.Base` (Shared base library)
- `Syncfusion.Office2016Theme.WinForms` (for themes)

See **Getting Started** reference for detailed NuGet installation instructions.
