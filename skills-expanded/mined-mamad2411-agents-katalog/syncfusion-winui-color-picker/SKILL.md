---
name: syncfusion-winui-color-picker
description: Guide implementation of the Syncfusion SfColorPicker control in WinUI applications. Use this skill when implementing color picker UI, solid color selection with RGB/HSV/HSL/CMYK models, or gradient brushes (linear and radial). Covers color spectrum customization, opacity control, brush mode switching, and color value management in WinUI/WinUI 3 projects.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion WinUI Color Picker (SfColorPicker)

## When to Use This Skill

Use this skill **immediately** when the user:

- Needs to implement a color picker UI in a WinUI application
- Wants to select solid colors with multiple color models (RGB, HSV, HSL, CMYK)
- Requires gradient brush creation (linear or radial)
- Needs to customize the color spectrum shape (box or ring)
- Wants to provide color editing with alpha/opacity control
- Needs to switch between solid and gradient brush modes
- Requires hexadecimal color input/output
- Wants to handle color selection change events
- Needs to customize color channel input options (sliders, text inputs)
- Requires programmatic color brush selection

This skill is specifically for the **Syncfusion WinUI Color Picker** (`SfColorPicker`) control, not generic color picking solutions.

## Component Overview

The **SfColorPicker** is a WinUI control for selecting and adjusting color values. It supports:

- **Solid Colors**: RGB, HSV, HSL, CMYK color models with hexadecimal editor
- **Gradient Brushes**: Linear and radial gradient color brushes with multiple stops
- **Color Spectrum**: Interactive color selection with box or ring shape
- **Opacity Control**: Alpha channel adjustment via sliders and text inputs
- **Mode Switching**: Dynamic switching between solid and gradient modes
- **Event Notifications**: Real-time color selection change events

**Key Namespace:**
```csharp
using Syncfusion.UI.Xaml.Editors;
```

**NuGet Package:**
```
Syncfusion.Editors.WinUI
```

---

## Documentation and Navigation Guide

### Getting Started with SfColorPicker

📄 **Read:** [references/getting-started.md](references/getting-started.md)

**Read this reference when you need:**
- Installation and NuGet package setup instructions
- Basic `SfColorPicker` control implementation
- Namespace and assembly references
- First working XAML + C# example with event handling
- Understanding the control structure and troubleshooting setup issues

**Topics covered:**
- Creating a WinUI 3 desktop application
- Adding `Syncfusion.Editors.WinUI` NuGet package
- Importing the control namespace
- Basic XAML and C# initialization
- Control structure overview
- Common initial configurations

---

### Solid Color Selection

📄 **Read:** [references/solid-color-selection.md](references/solid-color-selection.md)

**Read this reference when you need:**
- Selecting solid color brushes programmatically or interactively
- Working with different color models (RGB, HSV, HSL, CMYK)
- Switching between color channels at runtime
- Implementing hexadecimal color input/output
- Controlling opacity/alpha values
- Customizing color channel input options (sliders vs text)
- Handling solid color selection change events

**Topics covered:**
- `SelectedBrush` property for programmatic and interactive selection
- `ColorChannelOptions` (RGB, HSV, HSL, CMYK) with usage examples
- `BrushTypeOptions` to restrict solid-only mode
- `AlphaInputOptions` for opacity control (All, TextInput, SliderInput)
- `IsHexInputVisible` for hexadecimal editor visibility
- `ColorChannelInputOptions` (TextInput, SliderInput, All)
- `ColorEditorsVisibilityMode` (Inline, Expandable, Collapsed)
- `SelectedBrushChanged` event handling

---

### Gradient Color Selection

📄 **Read:** [references/gradient-color-selection.md](references/gradient-color-selection.md)

**Read this reference when you need:**
- Creating linear gradient brushes with multiple color stops
- Creating radial gradient brushes with gradient origin and center
- Programmatic gradient brush configuration
- Interactive gradient editing at runtime
- Adjusting gradient angles and directions
- Modifying gradient offsets (start/end points, radius)
- Controlling gradient opacity
- Handling gradient color change events

**Topics covered:**
- `LinearGradientBrush` with `GradientStop`, `StartPoint`, `EndPoint`
- `RadialGradientBrush` with `GradientOrigin`, `Center`, `RadiusX`, `RadiusY`
- Interactive gradient creation with `BrushTypeOptions`
- `AxisInputOption` — Simple (angle/direction) vs Advanced (precise editors)
- Adding, removing, and reordering gradient stops
- Gradient opacity control
- `SelectedBrushChanged` event for gradient brushes

---

### UI Customization and Modes

📄 **Read:** [references/ui-customization.md](references/ui-customization.md)

**Read this reference when you need:**
- Switching between solid, linear, and radial brush modes
- Enabling or restricting specific brush types
- Changing color spectrum shapes (box vs ring)
- Customizing color spectrum components (hue, saturation, value)
- Understanding `BrushTypeOptions` combinations
- Runtime brush mode switching behavior

**Topics covered:**
- `BrushTypeOptions` configurations (SolidColorBrush, LinearGradientBrush, RadialGradientBrush, All)
- Interactive brush mode dropdown behavior
- `ColorSpectrumShape` (Box vs Ring) with when-to-use guidance
- `ColorSpectrumComponents` (SaturationValue, HueSaturation, HueValue, etc.)
- Common customization patterns for different app types

---

### Best Practices and Troubleshooting

📄 **Read:** [references/best-practices.md](references/best-practices.md)

**Read this reference when you need:**
- Guidance on when to use solid vs gradient colors
- Performance optimization tips for gradients
- Common use case implementation patterns
- Troubleshooting color selection or rendering issues
- Accessibility considerations
- Integration patterns (flyout, dialog, property panel)

**Topics covered:**
- Solid vs gradient decision matrix
- Performance tips: gradient stop limits, caching brushes, debouncing events
- Common use cases: theme picker, drawing tool, text highlighter, background editor
- Flyout, dialog, and property panel integration patterns
- Common mistakes (brush type mismatch, missing null checks)
- Accessibility: keyboard navigation, ARIA attributes, screen reader support

---

## Quick Start Example

### XAML
```xml
<Page
    x:Class="ColorPickerApp.MainPage"
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    xmlns:editors="using:Syncfusion.UI.Xaml.Editors">

    <Grid>
        <editors:SfColorPicker
            x:Name="colorPicker"
            SelectedBrush="Blue"
            BrushTypeOptions="All"
            SelectedBrushChanged="ColorPicker_SelectedBrushChanged" />
    </Grid>
</Page>
```

### C# Code-Behind
```csharp
using Syncfusion.UI.Xaml.Editors;
using Microsoft.UI.Xaml.Media;

private void ColorPicker_SelectedBrushChanged(object sender, SelectedBrushChangedEventArgs args)
{
    if (args?.NewBrush is SolidColorBrush solidBrush)
    {
        var color = solidBrush.Color; // Access R, G, B, A
    }
    else if (args?.NewBrush is LinearGradientBrush linearBrush)
    {
        var stops = linearBrush.GradientStops;
    }
    else if (args?.NewBrush is RadialGradientBrush radialBrush)
    {
        var stops = radialBrush.GradientStops;
    }
}
```

---

## Common Patterns

### Pattern 1: Solid Color Picker Only
```xml
<editors:SfColorPicker
    BrushTypeOptions="SolidColorBrush"
    ColorChannelOptions="RGB"
    IsHexInputVisible="True" />
```

### Pattern 2: Gradient Editor Only
```xml
<editors:SfColorPicker
    BrushTypeOptions="LinearGradientBrush,RadialGradientBrush"
    AxisInputOption="Simple" />
```

### Pattern 3: Programmatic Color Selection
```csharp
// Solid color
colorPicker.SelectedBrush = new SolidColorBrush(Colors.Red);

// Linear gradient
var linearGradient = new LinearGradientBrush();
linearGradient.StartPoint = new Point(0, 0);
linearGradient.EndPoint = new Point(1, 1);
linearGradient.GradientStops.Add(new GradientStop() { Color = Colors.Yellow, Offset = 0.0 });
linearGradient.GradientStops.Add(new GradientStop() { Color = Colors.Red, Offset = 1.0 });
colorPicker.SelectedBrush = linearGradient;
```

### Pattern 4: Custom Spectrum Shape
```xml
<editors:SfColorPicker
    ColorSpectrumShape="Ring"
    ColorSpectrumComponents="HueSaturation" />
```

---

## Key Properties Reference

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `SelectedBrush` | Brush | Blue | Gets/sets the selected color brush |
| `BrushTypeOptions` | BrushTypeOptions | All | Enables specific brush modes (Solid, Linear, Radial) |
| `ColorChannelOptions` | ColorChannelOptions | RGB | Sets color model (RGB, HSV, HSL, CMYK) |
| `ColorSpectrumShape` | ColorSpectrumShape | Box | Sets spectrum shape (Box or Ring) |
| `ColorSpectrumComponents` | ColorSpectrumComponents | SaturationValue | Defines spectrum axes |
| `AlphaInputOptions` | ColorInputOptions | All | Controls alpha/opacity input visibility |
| `IsHexInputVisible` | bool | true | Shows/hides hexadecimal editor |
| `ColorChannelInputOptions` | ColorInputOptions | All | Controls channel input type (Slider/Text/All) |
| `ColorEditorsVisibilityMode` | ColorEditorsVisibilityMode | Inline | Sets editor visibility (Inline/Expandable/Collapsed) |
| `AxisInputOption` | AxisInputOption | Simple | Controls gradient axis input complexity |

## Key Events

| Event | Args | Purpose |
|-------|------|---------|
| `SelectedBrushChanged` | SelectedBrushChangedEventArgs | Fired when selected brush changes |

**Event Args:** `OldBrush` (previous selection) · `NewBrush` (new selection)

---

## Common Use Cases

1. **Theme Color Selector** — Let users customize app theme colors
2. **Drawing Tool** — Color selection for graphic/drawing applications
3. **Style Editor** — UI element color customization in design tools
4. **Gradient Background Editor** — Create gradient backgrounds or visual effects
5. **Color Palette Manager** — Manage color palettes in creative applications
