---
name: syncfusion-winforms-form
description: Implements Syncfusion SfForm control for Windows Forms with advanced customization features including custom title bars, MDI support, and modern appearance options. Use this when working with customizable window forms, title bar customization, MDI parent-child relationships, or form theming. The skill covers user controls in title bars, form borders, shadow effects, rounded corners, and complete appearance control.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Windows Forms (SfForm)

The Syncfusion `SfForm` is an advanced window control for Windows Forms applications that provides complete customization of form appearance, custom user interface in the title bar, and comprehensive MDI (Multiple Document Interface) support.

## When to Use This Skill

Use `SfForm` when you need to:

- **Customize title bar appearance** - Colors, text alignment, button styles, custom icons
- **Load custom controls in title bar** - Add search boxes, navigation controls, or any user control
- **Build MDI applications** - Parent forms with multiple child windows
- **Apply professional themes** - Built-in Office 2016/2019 and high contrast themes
- **Customize form borders** - Active/inactive states, colors, thickness, rounded corners
- **Add shadow effects** - Customizable shadow opacity for modern appearance
- **Support rich text in title bar** - Display formatted text in form title
- **Localize form elements** - Multi-language support for global applications

**SfForm vs MetroForm vs Office2007Form:**
- Use `SfForm` for modern applications requiring custom title bar controls and full appearance control
- Use `MetroForm` if you only need caption images and labels with built-in skins
- Use `Office2007Form` for Microsoft Office 2007-style UI with built-in color schemes

## Key Features

- **Title Bar Customization** - Height, colors, text alignment, button customization
- **User Control Loading** - Place any WinForms control in the title bar
- **MDI Support** - Complete parent-child form management
- **Border Customization** - Active/inactive border colors and thickness
- **Theme Support** - 6 built-in professional themes
- **Rich Text Support** - RTF formatting in title bar text
- **Shadow Effects** - Adjustable shadow opacity
- **Rounded Corners** - Windows 11 style rounded corners
- **Localization** - Full resource file support

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Assembly deployment and dependencies
- Converting standard Form to SfForm
- Basic setup and initialization
- Initial customization examples
- Loading user controls to title bar

### Title Bar Customization
📄 **Read:** [references/titlebar-customization.md](references/titlebar-customization.md)
- Adjusting title bar height
- Text alignment (horizontal and vertical)
- Customizing title bar buttons (icons, colors, states)
- Hiding buttons (minimize, maximize, close)
- Rich text formatting in title bar
- Loading user controls to title bar
- Icon and caption customization

### Form Customization
📄 **Read:** [references/form-customization.md](references/form-customization.md)
- Setting and aligning form icons
- Border customization (active/inactive states)
- Shadow effect configuration
- Shadow opacity settings
- Rounded corners (Windows 11+)

### MDI Customization
📄 **Read:** [references/mdi-customization.md](references/mdi-customization.md)
- Creating MDI parent forms
- Adding MDI child forms
- Customizing child form appearance
- Getting active MDI child
- Key event handling in MDI children

### Theming
📄 **Read:** [references/theming.md](references/theming.md)
- Loading theme assemblies
- Applying themes to forms
- Available themes (Office2016/2019, HighContrast)
- Theme customization options

### Localization
📄 **Read:** [references/localization.md](references/localization.md)
- Creating resource files for localization
- Setting culture and UI culture
- Localizing at sample level
- Editing default resource files
- Different assembly/namespace configurations

## Quick Start

### Step 1: Add Assembly References

Add the following references to your project:
- `Syncfusion.Core.WinForms.dll`
- `Syncfusion.Shared.Base.dll`

### Step 2: Convert Form to SfForm

```csharp
using Syncfusion.WinForms.Controls;

namespace MyApplication
{
    public partial class Form1 : SfForm  // Change from Form to SfForm
    {
        public Form1()
        {
            InitializeComponent();
            
            // Basic customization
            this.Style.TitleBar.BackColor = Color.FromArgb(46, 46, 46);
            this.Style.TitleBar.ForeColor = Color.White;
        }
    }
}
```

**VB.NET:**
```vb
Imports Syncfusion.WinForms.Controls

Public Class Form1
    Inherits SfForm  ' Change from Form to SfForm
    
    Public Sub New()
        InitializeComponent()
        
        ' Basic customization
        Me.Style.TitleBar.BackColor = Color.FromArgb(46, 46, 46)
        Me.Style.TitleBar.ForeColor = Color.White
    End Sub
End Class
```

### Step 3: Customize Appearance

```csharp
// Title bar button colors
this.Style.TitleBar.CloseButtonForeColor = Color.White;
this.Style.TitleBar.MinimizeButtonForeColor = Color.White;
this.Style.TitleBar.MaximizeButtonForeColor = Color.White;

// Button hover colors
this.Style.TitleBar.CloseButtonHoverBackColor = Color.Red;
this.Style.TitleBar.MinimizeButtonHoverBackColor = Color.DarkGray;
this.Style.TitleBar.MaximizeButtonHoverBackColor = Color.DarkGray;

// Form border
this.Style.Border = new Pen(Color.FromArgb(0, 122, 204), 2);
this.Style.InactiveBorder = new Pen(Color.Gray, 2);
```

## Common Patterns

### Pattern 1: Dark Theme Form

```csharp
public Form1()
{
    InitializeComponent();
    
    // Dark title bar
    this.Style.TitleBar.BackColor = Color.FromArgb(30, 30, 30);
    this.Style.TitleBar.ForeColor = Color.White;
    this.Style.TitleBar.Height = 35;
    
    // Button styling
    this.Style.TitleBar.CloseButtonForeColor = Color.White;
    this.Style.TitleBar.CloseButtonHoverBackColor = Color.FromArgb(232, 17, 35);
    this.Style.TitleBar.MinimizeButtonForeColor = Color.White;
    this.Style.TitleBar.MaximizeButtonForeColor = Color.White;
    
    // Border and shadow
    this.Style.Border = new Pen(Color.FromArgb(0, 122, 204), 2);
    this.Style.ShadowOpacity = 150;
    
    // Client area
    this.Style.BackColor = Color.FromArgb(45, 45, 48);
}
```

### Pattern 2: Custom Title Bar with Search Control

```csharp
public Form1()
{
    InitializeComponent();
    
    // Create search panel
    FlowLayoutPanel searchPanel = new FlowLayoutPanel();
    searchPanel.Size = new Size(250, 28);
    searchPanel.FlowDirection = FlowDirection.LeftToRight;
    
    // Add search label
    Label searchLabel = new Label();
    searchLabel.Text = "Search:";
    searchLabel.ForeColor = Color.White;
    searchLabel.AutoSize = true;
    searchLabel.Margin = new Padding(5, 5, 5, 0);
    
    // Add search textbox
    TextBox searchBox = new TextBox();
    searchBox.Width = 180;
    searchBox.Margin = new Padding(5, 2, 0, 0);
    
    searchPanel.Controls.Add(searchLabel);
    searchPanel.Controls.Add(searchBox);
    
    // Load to title bar
    this.TitleBarTextControl = searchPanel;
    
    // Style title bar
    this.Style.TitleBar.BackColor = Color.FromArgb(0, 120, 215);
    this.Style.TitleBar.Height = 35;
}
```

### Pattern 3: MDI Parent with Child Forms

```csharp
// Parent Form
public class MainForm : SfForm
{
    public MainForm()
    {
        InitializeComponent();
        
        // Enable MDI container
        this.IsMdiContainer = true;
        
        // Customize parent appearance
        this.Style.TitleBar.BackColor = Color.FromArgb(0, 122, 204);
        this.Style.TitleBar.ForeColor = Color.White;
    }
    
    private void CreateChildForm()
    {
        // Create child form
        SfForm childForm = new SfForm();
        childForm.Text = "Child Window 1";
        childForm.MdiParent = this;
        
        // Customize child appearance
        childForm.Style.TitleBar.BackColor = Color.White;
        childForm.Style.TitleBar.ForeColor = Color.Black;
        childForm.Style.Border = new Pen(Color.LightGray, 1);
        
        childForm.Show();
    }
}
```

### Pattern 4: Apply Built-in Theme

```csharp
// In Program.cs
static class Program
{
    [STAThread]
    static void Main()
    {
        // Register Syncfusion license
        Syncfusion.Licensing.SyncfusionLicenseProvider.RegisterLicense("YOUR_LICENSE_KEY");
        
        // Load theme assemblies
        SfSkinManager.LoadAssembly(typeof(Office2016Theme).Assembly);
        SfSkinManager.LoadAssembly(typeof(Office2019Theme).Assembly);
        
        Application.EnableVisualStyles();
        Application.SetCompatibleTextRenderingDefault(false);
        Application.Run(new Form1());
    }
}

// In Form
public Form1()
{
    InitializeComponent();
    
    // Apply theme
    this.ThemeName = "Office2016Colorful";
}
```

### Pattern 5: Localized Form

```csharp
public Form1()
{
    // Set culture before initialization
    System.Threading.Thread.CurrentThread.CurrentCulture = 
        new System.Globalization.CultureInfo("de-DE");
    System.Threading.Thread.CurrentThread.CurrentUICulture = 
        new System.Globalization.CultureInfo("de-DE");
    
    InitializeComponent();
}
```

## Key Properties

### Form Properties
- **`Style`** - Access all appearance customization options
- **`TitleBarTextControl`** - Load custom user control to title bar
- **`AllowRoundedCorners`** - Enable Windows 11 style rounded corners (bool)
- **`ThemeName`** - Apply built-in theme (string)
- **`IsMdiContainer`** - Enable MDI parent mode (bool)

### TitleBar Properties (Style.TitleBar)
- **`Height`** - Title bar height (int)
- **`BackColor`** - Title bar background color
- **`ForeColor`** - Title bar text color
- **`TextHorizontalAlignment`** - Left, Center, Right
- **`TextVerticalAlignment`** - Top, Center, Bottom
- **`IconHorizontalAlignment`** - Icon horizontal position
- **`IconVerticalAlignment`** - Icon vertical position
- **`AllowRichText`** - Enable RTF formatting (bool)

### Button Properties (Style.TitleBar)
- **`CloseButtonForeColor`** - Close button icon color
- **`MinimizeButtonForeColor`** - Minimize button icon color
- **`MaximizeButtonForeColor`** - Maximize button icon color
- **`CloseButtonHoverBackColor`** - Close button hover background
- **`CloseButtonPressedBackColor`** - Close button pressed background
- **`CloseButtonImage`** - Custom close button icon
- **`CloseButtonHoverImage`** - Custom close button hover icon
- **`CloseButtonPressedImage`** - Custom close button pressed icon

### Border and Shadow Properties (Style)
- **`Border`** - Active state border (Pen)
- **`InactiveBorder`** - Inactive state border (Pen)
- **`ShadowOpacity`** - Active shadow opacity (0-255)
- **`InactiveShadowOpacity`** - Inactive shadow opacity (0-255)

## Common Use Cases

### Use Case 1: Modern Application with Custom Title Bar
**Scenario:** Building a modern desktop application with branding in the title bar  
**Solution:** Use `TitleBarTextControl` to load a panel with logo and navigation controls  
**Reference:** [titlebar-customization.md](references/titlebar-customization.md)

### Use Case 2: Document Editor with MDI
**Scenario:** Creating a text editor that supports multiple open documents  
**Solution:** Use MDI parent form with child forms for each document  
**Reference:** [mdi-customization.md](references/mdi-customization.md)

### Use Case 3: Enterprise Application with Consistent Branding
**Scenario:** Apply company theme across all forms in the application  
**Solution:** Use built-in themes or create custom theme with Style properties  
**Reference:** [theming.md](references/theming.md)

### Use Case 4: Multi-language Application
**Scenario:** Support multiple languages for international users  
**Solution:** Implement localization with resource files  
**Reference:** [localization.md](references/localization.md)

### Use Case 5: Minimalist Form Design
**Scenario:** Create clean, distraction-free form with minimal UI  
**Solution:** Hide title bar buttons, use custom colors, add subtle shadow  
**Reference:** [form-customization.md](references/form-customization.md)

## Comparison with Other Form Controls

| Feature | SfForm | MetroForm | Office2007Form |
|---------|--------|-----------|----------------|
| Custom Title Bar Controls | ✅ Yes | ❌ No | ❌ No |
| MDI Support | ✅ Yes | ✅ Yes | ✅ Yes |
| Active/Inactive Border | ✅ Yes | ⚠️ Limited | ⚠️ Limited |
| Rich Text Title | ✅ Yes | ❌ No | ❌ No |
| Shadow Customization | ✅ Yes | ❌ No | ❌ No |
| Rounded Corners | ✅ Yes (Win11+) | ❌ No | ❌ No |
| Theme Support | ✅ 6 themes | ✅ Built-in skins | ✅ Office schemes |
| Caption Images | ✅ Yes | ✅ Yes | ✅ Yes |

**Recommendation:** Use `SfForm` for maximum flexibility and modern features. Use `MetroForm` or `Office2007Form` only for legacy applications or specific style requirements.

## Tips and Best Practices

### Performance
- Set all style properties in the constructor before showing the form
- Use `SuspendLayout()`/`ResumeLayout()` when adding multiple controls
- Dispose of custom images and resources properly

### Design
- Keep title bar height between 30-40 pixels for optimal appearance
- Use subtle shadows (opacity 100-150) for professional look
- Ensure sufficient contrast between title bar and buttons
- Test custom title bar controls at different DPI settings

### MDI Applications
- Set `IsMdiContainer = true` before creating child forms
- Apply consistent styling to all child forms
- Use `ActiveMdiChild` to manage current child window
- Consider using menu strip for window management

### Theme Usage
- Load theme assemblies in `Program.cs` before creating forms
- Apply consistent theme across all forms in application
- Test with HighContrast theme for accessibility
- Avoid mixing themed and non-themed forms

### Accessibility
- Provide sufficient color contrast for title bar text
- Support keyboard navigation for all custom controls
- Test with Windows high contrast settings
- Ensure custom title bar controls are accessible

## Troubleshooting

**Title bar custom control not visible:**
- Ensure control size fits within title bar height
- Check control's `Visible` property is `true`
- Verify background colors aren't transparent

**Theme not applying:**
- Verify theme assembly is loaded in `Program.cs`
- Check theme name spelling (case-sensitive)
- Ensure `ThemeName` is set after `InitializeComponent()`

**MDI child not displaying:**
- Verify parent's `IsMdiContainer = true`
- Check child's `MdiParent` is set correctly
- Ensure child form is shown with `.Show()` not `.ShowDialog()`

**Border not showing:**
- Verify `FormBorderStyle` is not `None`
- Check `Border` pen width is > 0
- Ensure border color contrasts with background

## Related Components

- **MetroForm** - Alternative form with built-in Metro styling
- **Office2007Form** - Alternative form with Office 2007 appearance
- **Ribbon** - For Office-style ribbon interface in title bar area
- **SfSkinManager** - For applying themes globally

## Additional Resources

- **API Reference:** [SfForm Class Documentation](https://help.syncfusion.com/cr/windowsforms/Syncfusion.WinForms.Controls.SfForm.html)
- **Sample Applications:** Check installation directory for complete examples
- **Support:** Syncfusion Community Forums
