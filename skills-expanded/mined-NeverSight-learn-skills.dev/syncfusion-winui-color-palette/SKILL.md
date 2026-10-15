---
name: syncfusion-winui-color-palette
description: Guide implementation of the Syncfusion WinUI Color Palette control (SfColorPalette) for swatch-based color selection in Windows desktop applications. Use this skill when working with theme colors, standard colors, custom color palettes, or the More Colors dialog. Covers color palette setup, theme color support, standard color configurations, UI customization, and best practices.
metadata:
   author: "Syncfusion Inc"
   version: "33.1.44"
---

## When to Use This Skill

Use this skill **immediately** when the user:

- Needs to implement a color palette (swatch-based) UI in WinUI applications
- Wants to display theme colors with their variant shades
- Needs to show standard colors with or without color shade variants
- Requires adding custom colors to the theme or standard color palette
- Wants to open a More Colors dialog for extended color selection
- Needs a "No Color" (transparent) selection option
- Wants to track recently used colors from the More Colors dialog
- Needs to set or get the selected color programmatically via `SelectedBrush`
- Requires customizing palette headers, header templates, or color shade spacing
- Needs to change layout flow direction or foreground styling
- Wants to set an automatic/default color that users can restore easily

This skill is specifically for the **Syncfusion WinUI Color Palette** control (`SfColorPalette`), not for gradient-based or spectrum-based color pickers.

## Component Overview

The **SfColorPalette** is a WinUI control that provides a swatch-based color selection interface. It supports:

- **Theme Colors**: Built-in palette themes (Office, Yellow, Green, etc.) with variant shades
- **Standard Colors**: Fixed set of standard colors with optional shade variants
- **Custom Colors**: Add your own colors to theme or standard palettes
- **More Colors Dialog**: Extended selection via color spectrum with opacity control
- **Recent Colors**: Tracks colors selected from the More Colors dialog
- **Automatic Color**: Default/automatic color button with configurable color
- **No Color Option**: Transparent color selection button
- **Tooltip Support**: Color name shown on hover
- **Programmatic Access**: Get/set selected color via `SelectedBrush`
- **Event Notifications**: `SelectedBrushChanged` for real-time change detection

**Key Namespace:**
```csharp
using Syncfusion.UI.Xaml.Editors;
```

**NuGet Package:**
```
Syncfusion.Editors.WinUI
```

## Documentation and Navigation Guide

### Getting Started with SfColorPalette

📄 **Read:** [references/getting-started.md](references/getting-started.md)

**Read this reference when you need:**
- Installation and NuGet package setup instructions
- Basic `SfColorPalette` control implementation
- Namespace and assembly references
- Accessing and setting selected color programmatically
- Handling the SelectedBrushChanged event
- Showing/hiding No Color button
- First working  XAML + C# example with minimal configuration

**Topics covered:**
- Creating a WinUI 3 desktop application
- Adding `Syncfusion.Editors.WinUI` NuGet package
- Importing the control namespace
- Basic XAML and C# initialization
- SelectedBrush property (get/set)
- SelectedBrushChanged event handling
- ShowNoColorButton property
- ShowMoreColorsButton property
- RecentColors collection
- Control structure overview

---

### Theme Colors

📄 **Read:** [references/theme-colors.md](references/theme-colors.md)

**Read this reference when you need:**
- Selecting colors from built-in theme palettes
- Switching the active theme palette at runtime
- Adding custom colors to the theme palette
- Showing or hiding base theme colors
- Showing or hiding theme color variant shades
- Customizing the theme palette header text or template
- Hiding the theme palette header
- Adjusting spacing between base colors and their variants

**Topics covered:**
- ActivePalette property and available ColorPaletteNames
- PaletteColors property (ColorPaletteModel)
- PaletteColors.ShowColors — show/hide base theme colors
- PaletteColors.ShowColorShades — show/hide variant shades
- PaletteColors.Colors — adding custom ColorModel entries
- PaletteColors.Header — custom header text
- PaletteColors.ShowHeader — header visibility
- PaletteColors.HeaderTemplate — custom header UI
- PaletteColors.ColorShadesSpacing — variant spacing
- Hiding the entire theme palette

---

### Standard Colors

📄 **Read:** [references/standard-colors.md](references/standard-colors.md)

**Read this reference when you need:**
- Selecting colors from the built-in standard colors panel
- Adding custom colors to the standard color palette
- Showing or hiding standard color variant shades
- Hiding the standard colors panel entirely
- Customizing the standard palette header text or template
- Hiding the standard palette header
- Adjusting spacing between standard colors and their variants

**Topics covered:**
- StandardColors property (StandardPaletteModel)
- StandardColors.ShowColors — show/hide standard colors
- StandardColors.ShowColorShades — show/hide variant shades
- StandardColors.Colors — adding custom ColorModel entries
- StandardColors.Header — custom header text
- StandardColors.ShowHeader — header visibility
- StandardColors.HeaderTemplate — custom header UI
- StandardColors.ColorShadesSpacing — variant spacing
- Hiding the entire standard colors panel

---

### More Color Dialog

📄 **Read:** [references/more-color-dialog.md](references/more-color-dialog.md)

**Read this reference when you need:**
- Enabling or disabling the More Colors button
- Understanding how the More Colors dialog works
- Hiding the More Colors option to restrict color choices

**Topics covered:**
- ShowMoreColorsButton property
- Selecting custom colors from the color spectrum dialog
- Hiding the More Colors button

---

### UI Customization

📄 **Read:** [references/ui-customization.md](references/ui-customization.md)

**Read this reference when you need:**
- Setting or getting the selected color programmatically
- Setting a null/transparent color value
- Configuring the automatic (default) color button
- Hiding the default color button
- Customizing palette header foreground color
- Changing flow direction (right-to-left support)
- Understanding tooltip behavior for color items
- Working with recently used colors panel

**Topics covered:**
- SelectedBrush property (programmatic access)
- Setting null/transparent color (Colors.Transparent)
- AutomaticBrush property — default color configuration
- ShowDefaultColorButton property — default color button visibility
- Foreground property — header text color
- FlowDirection property — RTL support
- Tooltip behavior for color items
- RecentColors collection — recently used colors

---

### Best Practices and Troubleshooting

📄 **Read:** [references/best-practices.md](references/best-practices.md)

**Read this reference when you need:**
- Guidance on when to use SfColorPalette vs SfColorPicker
- Common implementation patterns and use cases
- Troubleshooting color selection or display issues
- Understanding edge cases and limitations
- Accessibility considerations
- Integration with flyouts, dialogs, and property panels

**Topics covered:**
- When to use palette vs picker
- Common use cases (theme selector, document editor, drawing tool)
- Troubleshooting guide
- Edge cases to avoid
- Accessibility best practices
- Integration patterns (flyout, dialog, property panel)

---

## Quick Start Example

Here's a minimal example to get started with SfColorPalette:

### XAML Implementation

```xml
<Page
    x:Class="ColorPaletteApp.MainPage"
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    xmlns:editors="using:Syncfusion.UI.Xaml.Editors">

    <Grid Padding="20">
        <!-- Basic Color Palette -->
        <editors:SfColorPalette 
            x:Name="colorPalette"
            ShowMoreColorsButton="True"
            ShowNoColorButton="True"
            SelectedBrushChanged="ColorPalette_SelectedBrushChanged" />
    </Grid>
</Page>
```

### C# Code-Behind

```csharp
using Syncfusion.UI.Xaml.Editors;
using Microsoft.UI.Xaml.Media;
using Windows.UI;

namespace ColorPaletteApp
{
    public sealed partial class MainPage : Page
    {
        public MainPage()
        {
            this.InitializeComponent();
        }

        private void ColorPalette_SelectedBrushChanged(object sender, SelectedBrushChangedEventArgs e)
        {
            var oldBrush = e.OldBrush;
            var newBrush = e.NewBrush;

            // Apply selected color to a target element
            if (newBrush is SolidColorBrush solidBrush)
            {
                targetRectangle.Fill = solidBrush;
            }
        }
    }
}
```

---

## Common Patterns

### Pattern 1: Basic Palette with Theme and Standard Colors

```xml
<editors:SfColorPalette Name="colorPalette">
    <editors:SfColorPalette.PaletteColors>
        <editors:ColorPaletteModel ShowColorShades="True"/>
    </editors:SfColorPalette.PaletteColors>
    <editors:SfColorPalette.StandardColors>
        <editors:StandardPaletteModel ShowColorShades="True"/>
    </editors:SfColorPalette.StandardColors>
</editors:SfColorPalette>
```

### Pattern 2: Active Palette (Theme Switching)

```xml
<!-- Show "Yellow" theme colors by default -->
<editors:SfColorPalette ActivePalette="Yellow" Name="colorPalette" />
```

```csharp
// Switch theme programmatically
colorPalette.ActivePalette = ColorPaletteNames.Office;
```

### Pattern 3: Custom Theme and Standard Colors

```xml
<editors:SfColorPalette Name="colorPalette">
    <editors:SfColorPalette.PaletteColors>
        <editors:ColorPaletteModel ShowColors="True" ShowColorShades="True" Header="Brand Colors">
            <editors:ColorPaletteModel.Colors>
                <editors:ColorCollection>
                    <editors:ColorModel Color="#FF1464A0" Tooltip="Brand Blue" />
                    <editors:ColorModel Color="#FF00A651" Tooltip="Brand Green" />
                    <editors:ColorModel Color="#FFFF6600" Tooltip="Brand Orange" />
                </editors:ColorCollection>
            </editors:ColorPaletteModel.Colors>
        </editors:ColorPaletteModel>
    </editors:SfColorPalette.PaletteColors>
</editors:SfColorPalette>
```

### Pattern 4: Programmatic Color Selection

```csharp
// Set selected color
colorPalette.SelectedBrush = new SolidColorBrush(Colors.Yellow);

// Set transparent/no color
colorPalette.SelectedBrush = new SolidColorBrush(Colors.Transparent);

// Read selected color
if (colorPalette.SelectedBrush is SolidColorBrush brush)
{
    var color = brush.Color;
}
```

### Pattern 5: Enable All Options

```xml
<editors:SfColorPalette 
    ShowMoreColorsButton="True"
    ShowNoColorButton="True"
    AutomaticBrush="Black"
    ShowDefaultColorButton="True"
    Name="colorPalette" />
```

---

## Key Properties Reference

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| **SelectedBrush** | Brush | Transparent | Gets or sets the currently selected color |
| **ActivePalette** | ColorPaletteNames | Office | Sets the active built-in theme palette |
| **PaletteColors** | ColorPaletteModel | — | Configures theme color panel |
| **StandardColors** | StandardPaletteModel | — | Configures standard color panel |
| **ShowMoreColorsButton** | bool | true | Shows/hides the More Colors button |
| **ShowNoColorButton** | bool | false | Shows/hides the No Color (transparent) button |
| **AutomaticBrush** | Brush | Black | Sets the default/automatic color |
| **ShowDefaultColorButton** | bool | true | Shows/hides the default color button |
| **RecentColors** | Collection | — | Gets the recently used colors list |
| **Foreground** | Brush | Black | Sets header text foreground color |
| **FlowDirection** | FlowDirection | LeftToRight | Sets RTL/LTR layout direction |

**ColorPaletteModel / StandardPaletteModel Properties:**

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| **ShowColors** | bool | true | Shows/hides base colors |
| **ShowColorShades** | bool | true/false | Shows/hides variant shades |
| **Colors** | ColorCollection | — | Custom color entries |
| **Header** | string | "Theme Colors" / "Standard Colors" | Panel header text |
| **ShowHeader** | bool | true | Shows/hides the header |
| **HeaderTemplate** | DataTemplate | — | Custom header UI |
| **ColorShadesSpacing** | double | 10 | Space between base color and shades |

---

## Key Events

| Event | Args | Purpose |
|-------|------|---------|
| **SelectedBrushChanged** | SelectedBrushChangedEventArgs | Fired when selected color changes |

**Event Args Properties:**
- `OldBrush` — Previously selected brush
- `NewBrush` — Newly selected brush

---

## Common Use Cases

1. **Document Editor** — Font and highlight color selection (like MS Word color palette)
2. **Theme Customizer** — Let users pick from brand or theme colors
3. **Drawing/Annotation Tool** — Color picker for pen, highlighter, or shape fill
4. **Form Design Tool** — Background and text color selection for form elements
5. **Dashboard Builder** — Widget color assignment from a predefined palette

---

## Next Steps

1. **Start Simple:** Begin with [getting-started.md](references/getting-started.md) for basic setup
2. **Theme Colors:** Customize palette themes using [theme-colors.md](references/theme-colors.md)
3. **Standard Colors:** Configure standard color panel via [standard-colors.md](references/standard-colors.md)
4. **More Colors:** Add extended color dialog using [more-color-dialog.md](references/more-color-dialog.md)
5. **Customize UI:** Apply visual customizations from [ui-customization.md](references/ui-customization.md)
6. **Optimize:** Review [best-practices.md](references/best-practices.md) for production-ready implementation

---

**Note:** This skill focuses on the Syncfusion WinUI Color Palette control (`SfColorPalette`). For gradient/spectrum-based color picking, refer to the `syncfusion-winui-colorpicker` skill.

```
