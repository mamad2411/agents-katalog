---
name: syncfusion-winforms-metroform
description: Implements Syncfusion MetroForm control for creating modern Metro-styled Windows Forms with customizable caption bars, borders, and colors. Use this when working with MetroForm, custom title bars, flat UI forms, or modernizing Windows Forms appearance. The skill provides guidance for caption bar customization, rounded corners, caption labels and images, and advanced styling features.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion MetroForm

MetroForm is a Syncfusion Windows Forms control that provides modern Metro UI styling with flat appearance for desktop applications. It offers extensive customization options including caption bar labels, images, colors, borders, and advanced features like rounded corners (Windows 11+).

## When to Use This Skill

Use this skill when you need to:

- Create modern, Metro-styled Windows Forms applications
- Customize window title bars with labels, images, and custom colors
- Replace standard Windows Forms with flat, modern appearance
- Add caption bar elements (labels, images, icons) to forms
- Customize form borders, colors, and caption bar height
- Implement custom painting on caption bars
- Handle mouse events for caption images
- Create rounded corner forms (Windows 11+)
- Build professional desktop applications with modern UI

## Component Overview

**MetroForm** extends the standard Windows Forms `Form` class with:
- Modern Metro UI flat appearance
- Customizable caption bar with configurable height
- Support for caption labels and images
- Extensive color customization (borders, caption bar, buttons)
- Caption alignment options (horizontal and vertical)
- Custom brush effects for caption bar background
- Mouse event handling for caption images
- Rounded corners support (Windows 11+)
- Built-in theme support

### Key Features

- **Color Customization** - Caption background, foreground, control box buttons, border colors
- **Caption Elements** - Add labels and images to the caption bar
- **Help Button Support** - Optional help button in title bar
- **Right-to-Left Layout** - RTL language support
- **Flexible Alignment** - Caption text and icon alignment options
- **Custom Painting** - Paint events for advanced caption bar customization
- **Modern Appearance** - Flat Metro style with optional rounded corners

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)

Read this reference when you need to:
- Install and configure MetroForm for the first time
- Set up assembly references and NuGet packages
- Create a new project with MetroForm
- Convert existing Form to MetroForm
- Add basic caption labels and images
- Understand the initial setup workflow

### Caption Customization
📄 **Read:** [references/caption-customization.md](references/caption-customization.md)

Read this reference when you need to:
- Add caption labels through designer or code
- Add caption images through designer or code
- Configure CaptionLabels collection
- Configure CaptionImages collection
- Customize label properties (font, color, size, text)
- Customize image properties (location, size, image resource)

### Appearance and Styling
📄 **Read:** [references/appearance-styling.md](references/appearance-styling.md)

Read this reference when you need to:
- Customize border thickness and color
- Set caption bar height and modes
- Change caption bar colors
- Align caption text (left, center, right)
- Align caption text vertically (top, center, bottom)
- Configure icon alignment
- Customize caption fore color and font
- Style caption buttons (color, hover color)

### Advanced Customization
📄 **Read:** [references/advanced-customization.md](references/advanced-customization.md)

Read this reference when you need to:
- Apply custom brushes to caption bar background
- Implement custom painting with CaptionBarPaint event
- Create gradient effects in caption bar
- Handle mouse events for caption images (MouseDown, MouseUp, MouseEnter, MouseLeave, MouseMove)
- Enable rounded corners (Windows 11+)
- Implement advanced visual effects

## Quick Start

### Step 1: Install Package

```bash
Install-Package Syncfusion.Shared.Base
```

### Step 2: Add Assembly Reference

Add reference to:
- `Syncfusion.Shared.Base.dll`

### Step 3: Configure Your Form

```csharp
using Syncfusion.Windows.Forms;

namespace MyApplication
{
    // Inherit from MetroForm instead of Form
    public partial class MainForm : MetroForm
    {
        public MainForm()
        {
            InitializeComponent();
            
            // Basic configuration
            this.Text = "My Metro Application";
            this.CaptionBarHeight = 40;
            this.CaptionBarColor = Color.FromArgb(17, 158, 218);
            this.CaptionForeColor = Color.White;
            this.BorderColor = Color.FromArgb(17, 158, 218);
            this.BorderThickness = 2;
        }
    }
}
```

```vb
Imports Syncfusion.Windows.Forms

Namespace MyApplication
    ' Inherit from MetroForm instead of Form
    Public Partial Class MainForm
        Inherits MetroForm
        
        Public Sub New()
            InitializeComponent()
            
            ' Basic configuration
            Me.Text = "My Metro Application"
            Me.CaptionBarHeight = 40
            Me.CaptionBarColor = Color.FromArgb(17, 158, 218)
            Me.CaptionForeColor = Color.White
            Me.BorderColor = Color.FromArgb(17, 158, 218)
            Me.BorderThickness = 2
        End Sub
    End Class
End Namespace
```

## Common Patterns

### Pattern 1: Adding Caption Label

```csharp
// Create and configure caption label
CaptionLabel captionLabel = new CaptionLabel();
captionLabel.Text = "Dashboard";
captionLabel.Font = new Font("Segoe UI", 10F, FontStyle.Regular);
captionLabel.ForeColor = Color.White;
captionLabel.Size = new Size(200, 24);

// Add to form
this.CaptionLabels.Add(captionLabel);
```

### Pattern 2: Adding Caption Image with Click Handler

```csharp
// Create and configure caption image
CaptionImage logoImage = new CaptionImage();
logoImage.Image = Properties.Resources.AppLogo;
logoImage.Location = new Point(10, 5);
logoImage.Size = new Size(32, 32);
logoImage.BackColor = Color.Transparent;

// Handle click event
logoImage.ImageMouseDown += (sender, e) =>
{
    MessageBox.Show("Logo clicked!");
};

// Add to form
this.CaptionImages.Add(logoImage);
```

### Pattern 3: Custom Caption Bar Gradient

```csharp
// Apply gradient brush to caption bar
this.CaptionBarBrush = new LinearGradientBrush(
    new Rectangle(0, 0, this.Width, this.CaptionBarHeight),
    Color.DarkBlue,
    Color.LightBlue,
    LinearGradientMode.Horizontal
);

// Optional: Custom paint event for more control
this.CaptionBarPaint += (sender, e) =>
{
    using (var brush = new LinearGradientBrush(
        e.ClipRectangle,
        Color.DarkBlue,
        Color.LightBlue,
        LinearGradientMode.Horizontal))
    {
        e.Graphics.FillRectangle(brush, e.ClipRectangle);
    }
};
```

### Pattern 4: Rounded Corners (Windows 11+)

```csharp
// Enable rounded corners (Windows 11 only)
this.AllowRoundedCorners = true;
this.BorderColor = Color.FromArgb(17, 158, 218);
```

## Key Properties

### Caption Bar Properties
- `CaptionBarHeight` - Height of the caption bar (default varies)
- `CaptionBarColor` - Background color of caption bar
- `CaptionForeColor` - Text color in caption bar
- `CaptionFont` - Font for caption text
- `CaptionAlign` - Horizontal alignment (Left, Center, Right)
- `CaptionVerticalAlignment` - Vertical alignment (Top, Center, Bottom)
- `CaptionBarHeightMode` - Height behavior on maximize

### Border Properties
- `BorderColor` - Color of the form border
- `BorderThickness` - Thickness of the border in pixels
- `AllowRoundedCorners` - Enable rounded corners (Windows 11+)

### Button Properties
- `CaptionButtonColor` - Color of caption buttons (minimize, maximize, close)
- `CaptionButtonHoverColor` - Button color on hover

### Collections
- `CaptionLabels` - Collection of CaptionLabel objects
- `CaptionImages` - Collection of CaptionImage objects

### Icon Properties
- `IconAlign` - Alignment of form icon (Left, Center, Right)

### Advanced Properties
- `CaptionBarBrush` - Custom brush for caption bar background

## Common Use Cases

### Use Case 1: Dashboard Application
Create a modern dashboard with custom branding in the caption bar:
```csharp
this.Text = "Analytics Dashboard";
this.CaptionBarHeight = 50;
this.CaptionBarColor = Color.FromArgb(41, 128, 185);

// Add company logo
CaptionImage logo = new CaptionImage
{
    Image = Resources.CompanyLogo,
    Location = new Point(10, 10),
    Size = new Size(30, 30)
};
this.CaptionImages.Add(logo);

// Add title label
CaptionLabel title = new CaptionLabel
{
    Text = "Real-Time Analytics",
    Font = new Font("Segoe UI Semibold", 11F),
    ForeColor = Color.White
};
this.CaptionLabels.Add(title);
```

### Use Case 2: Settings Dialog
Create a simple, clean settings dialog:
```csharp
this.Text = "Settings";
this.CaptionBarHeight = 35;
this.CaptionBarColor = Color.FromArgb(52, 73, 94);
this.CaptionForeColor = Color.White;
this.BorderColor = Color.FromArgb(52, 73, 94);
this.BorderThickness = 1;
this.FormBorderStyle = FormBorderStyle.FixedDialog;
this.MaximizeBox = false;
this.MinimizeBox = false;
```

### Use Case 3: Main Application Window with Custom Appearance
Create a main window with gradient caption and custom controls:
```csharp
// Gradient caption bar
this.CaptionBarBrush = new LinearGradientBrush(
    new Rectangle(0, 0, this.Width, this.CaptionBarHeight),
    Color.FromArgb(44, 62, 80),
    Color.FromArgb(52, 152, 219),
    LinearGradientMode.Horizontal
);

// Caption buttons
this.CaptionButtonColor = Color.White;
this.CaptionButtonHoverColor = Color.FromArgb(231, 76, 60);

// Add user info to caption
CaptionLabel userLabel = new CaptionLabel
{
    Text = "Welcome, John Doe",
    ForeColor = Color.White,
    Font = new Font("Segoe UI", 9F),
    Location = new Point(100, 10)
};
this.CaptionLabels.Add(userLabel);
```

## Events

### Caption Bar Events
- `CaptionBarPaint` - Raised when caption bar needs repainting (for custom drawing)

### Caption Image Events (per image)
- `ImageMouseDown` - Mouse button pressed on caption image
- `ImageMouseUp` - Mouse button released on caption image
- `ImageMouseEnter` - Mouse enters caption image area
- `ImageMouseLeave` - Mouse leaves caption image area
- `ImageMouseMove` - Mouse moves within caption image area

## Troubleshooting

### Form Doesn't Show Metro Style
- Ensure you're inheriting from `MetroForm`, not `Form`
- Verify `Syncfusion.Shared.Base.dll` is referenced
- Check that the namespace `Syncfusion.Windows.Forms` is imported

### Caption Labels/Images Not Visible
- Verify `CaptionBarHeight` is sufficient for the content
- Check that foreground colors contrast with caption bar color
- Ensure Size property is set appropriately

### Rounded Corners Not Working
- Rounded corners only work on Windows 11+
- Set `AllowRoundedCorners = true`
- Note: Border and shadow are drawn by OS when rounded corners are enabled

### Designer Errors
- Clean and rebuild the solution
- Restart Visual Studio
- Ensure NuGet packages are properly restored

## Related Components

- **Office2007Form** - Office 2007 styled forms
- **OfficeForm** - Office styled forms with ribbon support
- **Form** - Standard Windows Forms (for comparison)

## Additional Resources

- [MetroForm API Reference](https://help.syncfusion.com/cr/windowsforms/Syncfusion.Windows.Forms.MetroForm.html)
- [Control Dependencies](https://help.syncfusion.com/windowsforms/control-dependencies#metroform)
- [NuGet Installation Guide](https://help.syncfusion.com/windowsforms/installation/install-nuget-packages)
