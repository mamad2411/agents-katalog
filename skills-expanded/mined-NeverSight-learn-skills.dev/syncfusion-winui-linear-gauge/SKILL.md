---
name: syncfusion-winui-linear-gauge
description: Implements Syncfusion WinUI Linear Gauge (SfLinearGauge) control for data visualization in desktop applications. Use this when building progress indicators, temperature displays, or data measurement gauges in WinUI. This skill covers axis configuration, pointer types (bar and shape), range customization, and animation.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# WinUI Linear Gauge (SfLinearGauge)

Comprehensive guide for implementing the Syncfusion WinUI Linear Gauge (SfLinearGauge) control for data visualization in Windows desktop applications. The Linear Gauge control displays numerical values on a linear scale horizontally or vertically with extensive customization options, ranges, multiple pointer types, and animation support.

## When to Use This Skill

Use this skill when you need to:
- **Create linear gauge controls** for data visualization in WinUI desktop applications
- **Display numerical values** on horizontal or vertical linear scales
- **Add range indicators** to visualize value categories with color-coded segments
- **Use bar pointers** to show current values with filled indicators
- **Use shape pointers** to mark values with different shapes (circle, diamond, triangle, etc.)
- **Use content pointers** to display custom content (text, images, icons) at values
- **Animate pointer movements** with customizable duration and easing functions
- **Enable interactive gauges** with draggable pointers for value input
- **Customize axis appearance** with labels, ticks, intervals, and formatting
- **Build dashboards** with temperature, pressure, speed, or other measurement displays
- **Create progress indicators** with visual feedback and ranges
- **Troubleshoot** gauge rendering, pointer positioning, or interaction issues

## Component Overview

**SfLinearGauge** is a multipurpose data visualization control that displays numerical values on a linear scale, offering:

- **Orientation:** Horizontal or vertical gauge layouts
- **Axis Customization:** Configurable scale with labels, ticks, intervals, and custom ranges
- **Range Support:** Multiple color-coded ranges to visualize value categories
- **Three Pointer Types:**
  - **Bar Pointer:** Filled bar from start to value
  - **Shape Pointer:** Markers with built-in shapes or custom templates
  - **Content Pointer:** Custom content (text, images, icons) at value position
- **Multiple Pointers:** Add multiple pointers to show different values on same scale
- **Animation:** Smooth pointer transitions with customizable easing functions
- **Interactivity:** Draggable shape pointers for user input
- **Customization:** Extensive styling, templates, gradients, and child content support
- **Data Binding:** MVVM-friendly with Value property binding

**Control Structure:**
- Single axis with configurable minimum, maximum, and interval
- Multiple ranges for color-coded value segments
- Bar pointers collection for filled indicators
- Marker pointers collection for shape and content pointers
- Full control over appearance, positioning, and behavior

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Creating a WinUI 3 desktop application
- Installing Syncfusion.Gauge.WinUI NuGet package
- Adding Linear Gauge control in XAML
- Adding Linear Gauge control in C#
- Adding axis to the gauge
- Adding ranges for value visualization
- Adding bar pointers
- Adding marker pointers (shape and content)
- Complete working example

### Axis Customization
📄 **Read:** [references/axis-customization.md](references/axis-customization.md)
- Setting minimum and maximum values
- Configuring intervals between labels
- Axis direction customization (IsInversed)
- Mirrored axis support (IsMirrored)
- Axis orientation (horizontal/vertical)
- Maximum labels count per 100 pixels
- Axis line styling (stroke, thickness, color)
- Axis line visibility control
- Label customization (fonts, colors, formats)
- Label templates for custom appearance
- Label visibility and placement (inside/outside)
- Label position and offset adjustment
- Tick customization (major and minor ticks)
- Tick styling and dashed patterns
- Tick placement and offset
- Custom scale ranges (logarithmic, etc.)

### Ranges
📄 **Read:** [references/ranges.md](references/ranges.md)
- Setting start and end values for ranges
- Range width customization (StartWidth, MidWidth, EndWidth)
- Equal vs. different width ranges
- Background color customization
- Gradient brush support with multiple stops
- Range position (inside/outside/cross axis)
- Using range colors for axis elements
- Range child content support for labels

### Pointers
📄 **Read:** [references/pointers.md](references/pointers.md)
- Overview of three pointer types
- Bar Pointer implementation and customization
- Shape Pointer with built-in and custom shapes
- Content Pointer for text, images, and icons
- Multiple pointers on single gauge
- Pointer dragging and interactivity
- Pointer events (ValueChangeStarted, ValueChanging, ValueChanged, ValueChangeCompleted)
- Pointer positioning and anchoring
- Pointer sizing and styling

### Animation
📄 **Read:** [references/animation.md](references/animation.md)
- Enabling pointer animation
- Animation duration configuration
- Animation easing functions
- Applying animation to bar pointers
- Applying animation to marker pointers
- Custom animation timing and effects

## Quick Start Example

Here's a minimal working example to get started:

### 1. Add Namespace

**XAML:**
```xml
<Window xmlns:gauge="using:Syncfusion.UI.Xaml.Gauges">
```

**C#:**
```csharp
using Syncfusion.UI.Xaml.Gauges;
```

### 2. Create Basic Linear Gauge (XAML)

```xml
<Window
    x:Class="GaugeApp.MainWindow"
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    xmlns:gauge="using:Syncfusion.UI.Xaml.Gauges">
    
    <Grid>
        <gauge:SfLinearGauge>
            <gauge:SfLinearGauge.Axis>
                <gauge:LinearAxis Minimum="0"
                                  Maximum="100"
                                  Interval="10">
                    <gauge:LinearAxis.BarPointers>
                        <gauge:BarPointer Value="60" />
                    </gauge:LinearAxis.BarPointers>
                </gauge:LinearAxis>
            </gauge:SfLinearGauge.Axis>
        </gauge:SfLinearGauge>
    </Grid>
</Window>
```

### 3. Or Create Programmatically (C#)

```csharp
using Syncfusion.UI.Xaml.Gauges;

namespace GaugeApp
{
    public sealed partial class MainWindow : Window
    {
        public MainWindow()
        {
            this.InitializeComponent();
            
            // Create gauge programmatically
            SfLinearGauge sfLinearGauge = new SfLinearGauge();
            sfLinearGauge.Axis.Minimum = 0;
            sfLinearGauge.Axis.Maximum = 100;
            sfLinearGauge.Axis.Interval = 10;
            
            // Add bar pointer
            BarPointer barPointer = new BarPointer();
            barPointer.Value = 60;
            sfLinearGauge.Axis.BarPointers.Add(barPointer);
            
            this.Content = sfLinearGauge;
        }
    }
}
```

### 4. Set Pointer Value (Optional)

```csharp
// Update pointer value
barPointer.Value = 75;

// With animation
barPointer.EnableAnimation = true;
barPointer.AnimationDuration = 1000; // 1 second
barPointer.Value = 90;
```

## Common Patterns

### Pattern 1: Basic Horizontal Gauge with Bar Pointer

```xml
<gauge:SfLinearGauge>
    <gauge:SfLinearGauge.Axis>
        <gauge:LinearAxis Minimum="0" Maximum="100" Interval="10">
            <gauge:LinearAxis.BarPointers>
                <gauge:BarPointer Value="60" Background="Green" />
            </gauge:LinearAxis.BarPointers>
        </gauge:LinearAxis>
    </gauge:SfLinearGauge.Axis>
</gauge:SfLinearGauge>
```

### Pattern 2: Vertical Temperature Gauge

```xml
<gauge:SfLinearGauge Orientation="Vertical">
    <gauge:SfLinearGauge.Axis>
        <gauge:LinearAxis Minimum="-60" Maximum="60" Interval="20">
            <gauge:LinearAxis.Ranges>
                <gauge:LinearGaugeRange StartValue="-60" EndValue="0" Background="Blue" />
                <gauge:LinearGaugeRange StartValue="0" EndValue="30" Background="Orange" />
                <gauge:LinearGaugeRange StartValue="30" EndValue="60" Background="Red" />
            </gauge:LinearAxis.Ranges>
            
            <gauge:LinearAxis.BarPointers>
                <gauge:BarPointer Value="25" />
            </gauge:LinearAxis.BarPointers>
        </gauge:LinearAxis>
    </gauge:SfLinearGauge.Axis>
</gauge:SfLinearGauge>
```

### Pattern 3: Gauge with Multiple Pointers

```xml
<gauge:SfLinearGauge>
    <gauge:SfLinearGauge.Axis>
        <gauge:LinearAxis Maximum="140" Interval="10">
            <!-- Bar pointer for current value -->
            <gauge:LinearAxis.BarPointers>
                <gauge:BarPointer Value="90" />
            </gauge:LinearAxis.BarPointers>
            
            <!-- Shape pointer for threshold -->
            <gauge:LinearAxis.MarkerPointers>
                <gauge:LinearShapePointer Value="90"
                                          VerticalAnchor="End"
                                          OffsetPoint="0,-8" />
                
                <!-- Content pointer for label -->
                <gauge:LinearContentPointer Value="90"
                                            VerticalAnchor="End"
                                            OffsetPoint="0,-28">
                    <gauge:LinearContentPointer.Content>
                        <TextBlock Text="90%" />
                    </gauge:LinearContentPointer.Content>
                </gauge:LinearContentPointer>
            </gauge:LinearAxis.MarkerPointers>
        </gauge:LinearAxis>
    </gauge:SfLinearGauge.Axis>
</gauge:SfLinearGauge>
```

### Pattern 4: Interactive Gauge with Draggable Pointer

```xml
<gauge:SfLinearGauge>
    <gauge:SfLinearGauge.Axis>
        <gauge:LinearAxis ShowTicks="False"
                          AxisLineStroke="CornflowerBlue"
                          AxisLineStrokeThickness="30">
            <gauge:LinearAxis.MarkerPointers>
                <gauge:LinearShapePointer Value="30"
                                          IsInteractive="True"
                                          OffsetPoint="0,-15"
                                          VerticalAnchor="End"
                                          Fill="Indigo"
                                          ValueChanged="OnPointerValueChanged" />
            </gauge:LinearAxis.MarkerPointers>
        </gauge:LinearAxis>
    </gauge:SfLinearGauge.Axis>
</gauge:SfLinearGauge>
```

```csharp
private void OnPointerValueChanged(object sender, ValueChangedEventArgs e)
{
    // Handle value change
    double newValue = e.NewValue;
}
```

### Pattern 5: Gauge with Color-Coded Ranges

```xml
<gauge:SfLinearGauge>
    <gauge:SfLinearGauge.Axis>
        <gauge:LinearAxis Maximum="140" Interval="10">
            <gauge:LinearAxis.Ranges>
                <gauge:LinearGaugeRange StartValue="0" EndValue="50" Background="Red" />
                <gauge:LinearGaugeRange StartValue="50" EndValue="100" Background="Orange" />
                <gauge:LinearGaugeRange StartValue="100" EndValue="140" Background="Green" />
            </gauge:LinearAxis.Ranges>
            
            <gauge:LinearAxis.BarPointers>
                <gauge:BarPointer Value="90" />
            </gauge:LinearAxis.BarPointers>
        </gauge:LinearAxis>
    </gauge:SfLinearGauge.Axis>
</gauge:SfLinearGauge>
```

### Pattern 6: Animated Pointer Updates

```xml
<gauge:SfLinearGauge>
    <gauge:SfLinearGauge.Axis>
        <gauge:LinearAxis Interval="10">
            <gauge:LinearAxis.BarPointers>
                <gauge:BarPointer Value="60"
                                  EnableAnimation="True"
                                  AnimationDuration="1500">
                    <gauge:BarPointer.AnimationEasingFunction>
                        <CircleEase EasingMode="EaseOut" />
                    </gauge:BarPointer.AnimationEasingFunction>
                </gauge:BarPointer>
            </gauge:LinearAxis.BarPointers>
        </gauge:LinearAxis>
    </gauge:SfLinearGauge.Axis>
</gauge:SfLinearGauge>
```

### Pattern 7: Gradient Bar Pointer

```xml
<gauge:SfLinearGauge>
    <gauge:SfLinearGauge.Axis>
        <gauge:LinearAxis>
            <gauge:LinearAxis.BarPointers>
                <gauge:BarPointer Value="40">
                    <gauge:BarPointer.GradientStops>
                        <gauge:GaugeGradientStop Value="0" Color="#FFCC2B5E" />
                        <gauge:GaugeGradientStop Value="40" Color="#FF753A88" />
                    </gauge:BarPointer.GradientStops>
                </gauge:BarPointer>
            </gauge:LinearAxis.BarPointers>
        </gauge:LinearAxis>
    </gauge:SfLinearGauge.Axis>
</gauge:SfLinearGauge>
```

### Pattern 8: ViewModel Data Binding

```csharp
public class GaugeViewModel : INotifyPropertyChanged
{
    private double currentValue;
    
    public double CurrentValue
    {
        get => currentValue;
        set
        {
            currentValue = value;
            OnPropertyChanged(nameof(CurrentValue));
        }
    }
    
    public event PropertyChangedEventHandler PropertyChanged;
    
    protected void OnPropertyChanged(string propertyName)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
}
```

```xml
<gauge:SfLinearGauge>
    <gauge:SfLinearGauge.Axis>
        <gauge:LinearAxis>
            <gauge:LinearAxis.BarPointers>
                <gauge:BarPointer Value="{x:Bind ViewModel.CurrentValue, Mode=TwoWay}" />
            </gauge:LinearAxis.BarPointers>
        </gauge:LinearAxis>
    </gauge:SfLinearGauge.Axis>
</gauge:SfLinearGauge>
```

## Key Properties Reference

### Gauge Properties (SfLinearGauge)

| Property | Type | Description |
|----------|------|-------------|
| `Axis` | LinearAxis | Gets or sets the linear axis configuration |
| `IsInversed` | bool | Gets or sets whether axis is inverted (right-to-left or bottom-to-top) |
| `IsMirrored` | bool | Gets or sets whether axis is mirrored (opposite side) |
| `Orientation` | Orientation | Gets or sets gauge orientation: Horizontal, Vertical |

### Axis Properties (LinearAxis)

| Property | Type | Description |
|----------|------|-------------|
| `Minimum` | double | Minimum value of the axis (default: 0) |
| `Maximum` | double | Maximum value of the axis (default: 100) |
| `Interval` | double | Interval between labels on the axis |
| `ShowAxisLine` | bool | Show or hide the axis line (default: true) |
| `ShowLabels` | bool | Show or hide axis labels (default: true) |
| `ShowTicks` | bool | Show or hide tick marks (default: true) |
| `AxisLineStroke` | Brush | Color of the axis line |
| `AxisLineStrokeThickness` | double | Thickness of the axis line |
| `LabelPosition` | GaugeLabelsPosition | Label position: Inside, Outside |
| `LabelOffset` | double | Distance between axis line and labels |
| `LabelFormat` | string | Format string for labels (e.g., "c" for currency) |
| `TickPosition` | GaugeElementPosition | Tick position: Inside, Outside, Cross |
| `MajorTickLength` | double | Length of major tick marks |
| `MinorTickLength` | double | Length of minor tick marks |
| `MinorTicksPerInterval` | int | Number of minor ticks per interval |
| `UseRangeColorForAxis` | bool | Apply range colors to axis labels and ticks |

### Pointer Properties (Base: LinearGaugePointer)

| Property | Type | Description |
|----------|------|-------------|
| `Value` | double | Current value of the pointer |
| `EnableAnimation` | bool | Enable pointer animation (default: false) |
| `AnimationDuration` | double | Animation duration in milliseconds (default: 1500) |
| `AnimationEasingFunction` | EasingFunctionBase | Easing function for animation |

### Bar Pointer Properties

| Property | Type | Description |
|----------|------|-------------|
| `Background` | Brush | Fill color of the bar pointer |
| `PointerSize` | double | Thickness of the bar pointer |
| `CornerStyle` | CornerStyle | Corner style: BothFlat, BothCurve, StartCurve, EndCurve |
| `Offset` | double | Distance from axis line (positive: inside, negative: outside) |
| `GradientStops` | ObservableCollection | Collection of gradient stops for color transition |
| `Child` | UIElement | Child content displayed inside the bar pointer |

### Shape Pointer Properties (LinearShapePointer)

| Property | Type | Description |
|----------|------|-------------|
| `ShapeType` | GaugeShapeType | Shape: Circle, Diamond, Triangle, InvertedTriangle, Rectangle |
| `ShapeHeight` | double | Height of the shape pointer |
| `ShapeWidth` | double | Width of the shape pointer |
| `Fill` | Brush | Fill color of the shape |
| `Stroke` | Brush | Border color of the shape |
| `StrokeThickness` | double | Border thickness of the shape |
| `HasShadow` | bool | Enable shadow effect (default: false) |
| `IsInteractive` | bool | Enable dragging (default: false) |
| `ShapeTemplate` | DataTemplate | Custom shape template |
| `OffsetPoint` | Point | X/Y offset from default position |
| `HorizontalAnchor` | GaugeAnchor | Horizontal alignment: Start, Center, End |
| `VerticalAnchor` | GaugeAnchor | Vertical alignment: Start, Center, End |

### Content Pointer Properties (LinearContentPointer)

| Property | Type | Description |
|----------|------|-------------|
| `Content` | object | Custom content (TextBlock, Image, etc.) |
| `OffsetPoint` | Point | X/Y offset from default position |
| `HorizontalAnchor` | GaugeAnchor | Horizontal alignment: Start, Center, End |
| `VerticalAnchor` | GaugeAnchor | Vertical alignment: Start, Center, End |

### Range Properties (LinearGaugeRange)

| Property | Type | Description |
|----------|------|-------------|
| `StartValue` | double | Start value of the range |
| `EndValue` | double | End value of the range |
| `StartWidth` | double | Width at range start |
| `MidWidth` | double | Width at range middle (optional) |
| `EndWidth` | double | Width at range end |
| `Background` | Brush | Fill color of the range |
| `RangePosition` | GaugeElementPosition | Position: Inside, Outside, Cross |
| `GradientStops` | ObservableCollection | Collection of gradient stops for color transition |
| `Child` | UIElement | Child content displayed inside the range |

## Common Use Cases

### Temperature Gauge for Weather App
Create vertical temperature gauges displaying current temperature with color-coded ranges (blue for cold, orange for moderate, red for hot) and animated pointer transitions.

### Battery Level Indicator
Build horizontal battery level gauges with green/yellow/red ranges, bar pointers showing charge level, and content pointers displaying percentage text.

### Speed Meter for Vehicle Dashboard
Implement horizontal or vertical speed gauges with tick marks every 10 units, shape pointers for current speed, and range indicators for speed limits.

### Progress Bar with Percentage
Create progress indicators using bar pointers with rounded corners, child content displaying percentage text, and smooth animations as values update.

### Pressure Gauge for Industrial Monitoring
Design pressure gauges with custom axis ranges, multiple ranges for safe/warning/danger zones, and interactive pointers for threshold adjustment.

### Volume Control Slider
Build interactive volume controls using horizontal gauges with draggable shape pointers, custom axis styling, and value change events for audio level adjustment.

### Data Analytics Dashboard
Create dashboard panels with multiple linear gauges showing KPIs, each with different orientations, color schemes, and ranges for performance visualization.

### System Resource Monitor
Implement CPU/memory/disk usage gauges with animated bar pointers, gradient fills showing resource consumption, and real-time value updates.

---

**Next Steps:** Read the reference documentation above based on what you need to implement. Start with [getting-started.md](references/getting-started.md) for initial setup, then explore specific features as needed.
