---
name: syncfusion-winui-range-slider
description: Implements Syncfusion WinUI RangeSlider (SfRangeSlider) control for range selection in desktop applications. Use this when working with range selectors, dual-thumb sliders, or numeric range selection interfaces. This skill covers configuration, labels, ticks, dividers, track customization, thumb styling, tooltips, and value handling for interactive range selection in WinUI applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing WinUI RangeSlider (SfRangeSlider)

Complete guide for implementing the Syncfusion WinUI RangeSlider control - a highly interactive UI component for selecting numeric ranges with dual thumbs, labels, ticks, and rich customization options.

## When to Use This Skill

Use this skill when you need to:
- Implement a range selector or range picker in WinUI applications
- Allow users to select a value range with dual thumbs
- Create price range filters, date range pickers, or numeric range selectors
- Add interactive sliders with labels, ticks, and tooltips
- Customize track, thumb, or overlay appearance
- Handle range value changes and validation
- Work with the SfRangeSlider control in WinUI apps

## WinUI RangeSlider Overview

The [Syncfusion WinUI RangeSlider](https://www.syncfusion.com/winui-controls/range-slider) (SfRangeSlider) is a highly interactive UI control that allows users to select a smaller range from a larger data set by moving dual thumbs along a track.

**Key Features:**
- **Numeric Range Selection**: Select numeric values within any range
- **Visual Elements**: Labels, ticks, dividers for intuitive value display
- **Customization**: Extensive styling for track, thumbs, overlays
- **Tooltips**: Show selected values with customizable formatting
- **Events**: RangeValueChanged for range tracking
- **Responsive**: Smooth thumb interaction and visual feedback

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Creating WinUI application
- Installing Syncfusion.Sliders.WinUI NuGet package
- Basic SfRangeSlider initialization
- Setting RangeStart and RangeEnd values
- Complete working example

### Basic Configuration
📄 **Read:** [references/basic-features.md](references/basic-features.md)
- Minimum and Maximum values
- Interval configuration
- Step frequency
- Value change events
- Orientation (Horizontal/Vertical)
- Discrete vs continuous mode

### Labels
📄 **Read:** [references/labels.md](references/labels.md)
- Enabling labels (ShowLabels)
- Maximum labels count
- Label offset and placement
- Label format customization
- Custom label templates
- Label styling

### Ticks
📄 **Read:** [references/ticks.md](references/ticks.md)
- Major ticks (ShowTicks)
- Minor ticks (MinorTicksPerInterval)
- Tick length and offset
- Tick placement
- Styling ticks

### Dividers
📄 **Read:** [references/dividers.md](references/dividers.md)
- Enabling dividers (ShowDividers)
- Divider dimensions
- Divider styling
- Use cases

### Track Customization
📄 **Read:** [references/track.md](references/track.md)
- Active track styling
- Inactive track styling
- Track height and corners
- Track fill customization

### Thumb and Overlay
📄 **Read:** [references/thumb-and-overlay.md](references/thumb-and-overlay.md)
- Thumb customization
- Thumb size and icons
- ThumbStyle property
- Overlay styling
- Custom thumb templates

### Tooltips
📄 **Read:** [references/tooltip.md](references/tooltip.md)
- Enabling tooltips (ShowTooltip)
- Tooltip format and placement
- Custom tooltip templates
- Tooltip styling

### Advanced Range Handling
📄 **Read:** [references/custom-range.md](references/custom-range.md)
- RangeValueChanged and other events
- Programmatic value updates
- Range validation
- Custom range scenarios

## Quick Start

### 1. Install NuGet Package

```xml
<PackageReference Include="Syncfusion.Sliders.WinUI" Version="Latest" />
```

### 2. Add Namespace

```xaml
<Page xmlns:slider="using:Syncfusion.UI.Xaml.Sliders">
```

### 3. Basic Implementation

```xaml
<slider:SfRangeSlider 
    RangeStart="30"
    RangeEnd="70"
    ShowLabels="True"
    ShowTicks="True" />
```

### 4. Code-Behind

```csharp
using Syncfusion.UI.Xaml.Sliders;

SfRangeSlider rangeSlider = new SfRangeSlider();
rangeSlider.Minimum = 0;
rangeSlider.Maximum = 100;
rangeSlider.RangeStart = 30;
rangeSlider.RangeEnd = 70;
rangeSlider.ShowLabels = true;
rangeSlider.ShowTicks = true;
this.Content = rangeSlider;
```

## Common Patterns

### Price Range Filter
```xaml
<slider:SfRangeSlider 
    Minimum="0"
    Maximum="1000"
    Interval="100"
    RangeStart="200"
    RangeEnd="800"
    ShowLabels="True"
    ShowTicks="True"
    ShowTooltip="True" />
```

### Custom Styled Range Slider
```xaml
<slider:SfRangeSlider 
    RangeStart="25"
    RangeEnd="75"
    ShowLabels="True"
    ShowTicks="True"
    ShowDividers="True"
    ActiveTrackHeight="4"
    InactiveTrackHeight="4"
    DividerHeight="4"
    DividerWidth="4"
    ThumbHeight="20"
    ThumbWidth="20" />
```

### Value Change Tracking
```xaml
<slider:SfRangeSlider 
    x:Name="rangeSlider"
    RangeStart="30"
    RangeEnd="70"
    RangeValueChanged="OnRangeChanged" />
```

```csharp
private void OnRangeChanged(object sender, RangeValueChangedEventArgs e)
{
    double oldStart = e.RangeStartOldValue;
    double oldEnd = e.RangeEndOldValue;
    double newStart = e.RangeStartNewValue;
    double newEnd = e.RangeEndNewValue;
    
    // Update UI or perform validation
    Debug.WriteLine($"Range: {newStart} - {newEnd}");
}
```

## Key Properties

### Range Configuration
- `Minimum` (double): Minimum value (default: 0)
- `Maximum` (double): Maximum value (default: 100)
- `RangeStart` (double): Start value of selected range
- `RangeEnd` (double): End value of selected range
- `Interval` (double): Step interval for labels/ticks
- `StepFrequency` (double): Value change step size

### Visual Elements
- `ShowLabels` (bool): Display labels on interval points
- `ShowTicks` (bool): Display major ticks
- `ShowDividers` (bool): Display dividers
- `ShowTooltip` (bool): Display tooltip on thumb

### Customization
- `ActiveTrackHeight` (double): Height of active track
- `InactiveTrackHeight` (double): Height of inactive track
- `ThumbHeight` (double): Thumb height
- `ThumbWidth` (double): Thumb width
- `OverlayRadius` (double): Thumb overlay radius

### Behavior
- `IsInversed` (bool): Reverse direction
- `MinorTicksPerInterval` (int): Minor ticks between intervals
- `MaximumLabelsCount` (int): Max labels per 100 logical pixels

## Common Use Cases

### E-Commerce Price Filters
Use RangeSlider for filtering products by price range with labels and tooltips showing currency values.

### Date Range Pickers
Implement month/year range selection with custom label formatting for calendar applications.

### Audio/Video Timeline Selection
Create clip selection tools with precise range control and visual feedback.

### Data Filtering Dashboards
Enable users to filter datasets by numeric ranges (age, quantity, ratings, etc.).

### Settings and Configuration
Provide intuitive range selectors for app settings (volume range, brightness range, etc.).

## Troubleshooting

**Range values not updating:**
- Ensure RangeStart and RangeEnd are within Minimum and Maximum
- Check if two-way data binding is configured correctly
- Verify RangeValueChanged event is wired up

**Labels not showing:**
- Set `ShowLabels="True"`
- Configure `Interval` property for label spacing
- Check `MaximumLabelsCount` if using automatic intervals

**Ticks not visible:**
- Set `ShowTicks="True"`
- Ensure `Interval` is defined
- Adjust `TickOffset` if needed

**Tooltip not appearing:**
- Set `ShowTooltip="True"`
- Check `TooltipPlacement` property
- Verify tooltip template is valid

## Related Components

- **Slider (SfSlider)**: Single-thumb slider for single value selection
- **DateRangeSlider**: Specialized slider for date range selection

## Resources

- [WinUI RangeSlider Documentation](https://help.syncfusion.com/winui/rangeslider/getting-started)
- [API Reference](https://help.syncfusion.com/cr/winui/Syncfusion.UI.Xaml.Sliders.SfRangeSlider.html)
- [GitHub Examples](https://github.com/SyncfusionExamples/WinUI_Sliders_Getting_Started)
- [NuGet Package](https://www.nuget.org/packages/Syncfusion.Sliders.WinUI)