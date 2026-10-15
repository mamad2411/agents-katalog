---
name: syncfusion-winui-slider
description: Implements Syncfusion WinUI Slider (SfSlider) control for numeric value selection in desktop applications. Use this when working with sliders, range selectors, value pickers, or interactive range controls. This skill covers slider configuration, ticks, labels, tooltips, value selection, and customization for WinUI applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion WinUI Slider

## When to Use This Skill

Use the Syncfusion WinUI Slider when you need to:
- Allow users to select a single numeric value from a range
- Provide an interactive way to adjust values (volume, brightness, price range, etc.)
- Display value selection with visual feedback (labels, ticks, tooltips)
- Create slider controls with customizable appearance and behavior
- Implement range selectors for filtering or configuration
- Build settings panels with adjustable numeric parameters
- Add interactive controls for measurements, ratings, or scores

## Component Overview

The Syncfusion WinUI Slider (SfSlider) is a highly interactive UI control that enables users to select a single value from a range of values. It provides rich features including:

- **Numeric Value Support** - Select values in any numeric range
- **Labels** - Display formatted values with customizable styles
- **Ticks** - Show major and minor tick marks at intervals
- **Dividers** - Visual separators between intervals
- **Thumb Customization** - Various built-in icons and custom styles
- **Tooltips** - Show selected value with custom formatting
- **Track Styling** - Customize active and inactive track appearance
- **Orientation** - Horizontal or vertical layout
- **Accessibility** - Full keyboard and screen reader support

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Creating a WinUI 3 desktop application
- Installing the Syncfusion.Sliders.WinUI NuGet package
- Adding namespace imports
- Basic slider initialization
- Setting minimum, maximum, and current values
- Enabling ticks, labels, and dividers
- Quick implementation examples

### Core Features and Configuration
📄 **Read:** [references/basic-features.md](references/basic-features.md)
- Numeric value support and ranges
- Orientation (Horizontal/Vertical)
- Value property and data binding
- Interval and step frequency
- IsEnabled and IsInversed properties
- ValueChanged event handling
- Custom range implementation
- Edge cases and validation

### Labels
📄 **Read:** [references/labels.md](references/labels.md)
- ShowLabels property
- Label placement and positioning
- Label format strings (numeric, percentage, currency, custom)
- LabelStyle customization
- LabelOffset configuration
- Custom label templates
- Label visibility and spacing
- RTL support for labels

### Ticks
📄 **Read:** [references/ticks.md](references/ticks.md)
- ShowTicks property for major ticks
- Minor ticks with MinorTicksPerInterval 
- Tick placement and offset
- MajorTickStyle customization
- MinorTickStyle customization
- TickPlacement (After, Before)
- Custom tick templates
- Tick frequency and spacing

### Dividers
📄 **Read:** [references/dividers.md](references/dividers.md)
- ShowDividers property
- DividerHeight and DividerWidth
- Divider styling and colors
- Custom divider templates
- Divider placement relative to track
- Visual separation between intervals

### Thumb and Tooltip
📄 **Read:** [references/thumb-tooltip.md](references/thumb-tooltip.md)
- Thumb icon and customization
- ThumbStyle property
- Thumb overlay effects
- ShowToolTip property
- Tooltip placement (Top/Bottom)
- TooltipFormat for custom display
- Custom tooltip templates
- Hover and interaction states
- Thumb accessibility features

### Track Customization
📄 **Read:** [references/track-customization.md](references/track-customization.md)
- ActiveTrackHeight and InactiveTrackHeight
- ActiveTrackStyle and InactiveTrackStyle
- Track colors and brushes
- Track fill customization
- Gradient tracks
- Custom track templates
- Corner radius and styling
- Track interaction states

## Quick Start Example

### Basic Slider Implementation

```xml
<!-- Add namespace -->
<Window xmlns:slider="using:Syncfusion.UI.Xaml.Sliders">

    <Grid>
        <slider:SfSlider Value="50"
                         Minimum="0"
                         Maximum="100"
                         Width="400"
                         Margin="20" />
    </Grid>
</Window>
```

### Slider with Labels and Ticks

```xml
<slider:SfSlider Value="50"
                 Minimum="0"
                 Maximum="100"
                 Interval="10"
                 ShowLabels="True"
                 ShowTicks="True"
                 Width="400" />
```

### Fully Featured Slider

```xml
<slider:SfSlider Value="50"
                 Minimum="0"
                 Maximum="100"
                 Interval="10"
                 ShowLabels="True"
                 ShowTicks="True"
                 ShowDividers="True"
                 ShowToolTip="True"
                 MinorTicksPerInterval ="1"
                 Width="400"
                 Height="60" />
```

### Code-Behind Implementation

```csharp
using Syncfusion.UI.Xaml.Sliders;

// Create slider
SfSlider slider = new SfSlider();
slider.Value = 50;
slider.Minimum = 0;
slider.Maximum = 100;
slider.Interval = 10;
slider.ShowLabels = true;
slider.ShowTicks = true;
slider.Width = 400;

// Handle value changes
slider.ValueChanged += (sender, e) =>
{
    double newValue = e.NewValue;
    Console.WriteLine($"Value changed to: {newValue}");
};

// Add to layout
rootGrid.Children.Add(slider);
```

## Common Patterns

### Volume Control Pattern
```xml
<slider:SfSlider Value="{Binding Volume, Mode=TwoWay}"
                 Minimum="0"
                 Maximum="100"
                 Interval="10"
                 ShowLabels="True"
                 ShowTicks="True"
                 ShowToolTip="True"
                 Width="300">
</slider:SfSlider>
```

### Price Range Filter Pattern
```xml
<slider:SfSlider Value="{Binding MaxPrice, Mode=TwoWay}"
                 Minimum="0"
                 Maximum="1000"
                 Interval="100"
                 ShowLabels="True"
                 ShowTicks="True"
                 Width="400">
</slider:SfSlider>
```

### Vertical Slider Pattern
```xml
<slider:SfSlider Value="50"
                 Minimum="0"
                 Maximum="100"
                 Orientation="Vertical"
                 ShowLabels="True"
                 ShowTicks="True"
                 Height="300"
                 Width="80" />
```

### Disabled State Pattern
```xml
<slider:SfSlider Value="50"
                 IsEnabled="False"
                 ShowLabels="True"
                 ShowTicks="True"
                 Width="400" />
```

## Key Properties

| Property | Type | Description |
|----------|------|-------------|
| `Value` | `double` | Current value of the slider |
| `Minimum` | `double` | Minimum value (default: 0) |
| `Maximum` | `double` | Maximum value (default: 100) |
| `Interval` | `double` | Spacing between labels and ticks (default: calculated) |
| `ShowLabels` | `bool` | Display value labels (default: false) |
| `ShowTicks` | `bool` | Display tick marks (default: false) |
| `ShowDividers` | `bool` | Display dividers between intervals (default: false) |
| `ShowToolTip` | `bool` | Display tooltip on thumb hover/drag (default: false) |
| `Orientation` | `Orientation` | Horizontal or Vertical (default: Horizontal) |
| `IsInversed` | `bool` | Reverse the direction (default: false) |
| `MinorTicksPerInterval` | `int` | Number of minor ticks per interval (default: 0) |
| `ActiveTrackHeight` | `double` | Height of the filled track |
| `InactiveTrackHeight` | `double` | Height of the unfilled track |
| `DividerHeight` | `double` | Height of divider markers |
| `DividerWidth` | `double` | Width of divider markers |

## Key Events

| Event | Description |
|-------|-------------|
| `ValueChanged` | Fired when the slider value changes |

## Common Use Cases

1. **Audio/Video Controls** - Volume, playback position, brightness
2. **Filter Sliders** - Price range, age range, rating filters
3. **Settings Panels** - Adjustable parameters, configuration values
4. **Image Editing** - Brightness, contrast, saturation adjustments
5. **Measurement Tools** - Temperature, pressure, scale selectors
6. **Rating Systems** - Score selection, satisfaction ratings
7. **Progress Indicators** - Interactive progress bars
8. **Zoom Controls** - Scale/zoom level adjustment

## Best Practices

1. **Set Appropriate Ranges:** Define meaningful Minimum and Maximum values
2. **Use Intervals Wisely:** Choose intervals that make sense for your data
3. **Enable Visual Feedback:** Show labels, ticks, or tooltips for better UX
4. **Data Binding:** Use two-way binding for reactive updates
5. **Accessibility:** Ensure keyboard navigation works (Tab, Arrow keys)
6. **Custom Formatting:** Use LabelFormat and TooltipFormat for clarity
7. **Responsive Width:** Set appropriate Width for your layout
8. **Validation:** Handle ValueChanged to validate and constrain values

## Troubleshooting

**Slider Not Showing:**
- Verify Syncfusion.Sliders.WinUI NuGet is installed
- Check namespace import: `xmlns:slider="using:Syncfusion.UI.Xaml.Sliders"`
- Ensure Width or Height is set appropriately

**Value Not Updating:**
- Use Mode=TwoWay for data binding
- Handle ValueChanged event properly
- Check if IsEnabled is true

**Labels/Ticks Not Visible:**
- Set ShowLabels="True" and ShowTicks="True"
- Define Interval property
- Ensure sufficient Width/Height for layout

**Tooltip Not Appearing:**
- Set ShowToolTip="True"
- Verify mouse/touch interaction works

## Next Steps

- Explore [labels.md](references/labels.md) for custom label formatting
- Learn about [ticks.md](references/ticks.md) for precise value indicators
- Customize appearance with [track-customization.md](references/track-customization.md)
- Add tooltips via [thumb-tooltip.md](references/thumb-tooltip.md)