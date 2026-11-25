---
name: syncfusion-winui-radial-gauge
description: Implement Syncfusion WinUI Radial Gauge (SfRadialGauge) component for circular data visualization in desktop applications. Use this when working with radial gauges, speedometers, temperature monitors, or dashboard meters. This skill covers axis configuration, multiple pointer types (needle, shape, content, range), ranges with gradients, annotations, animations, and interactive dragging for WinUI/.NET desktop applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Radial Gauge

The Syncfusion WinUI Radial Gauge (SfRadialGauge) is a multi-purpose data visualization control that displays numerical values on a circular scale. It's ideal for creating speedometers, temperature monitors, dashboard gauges, meter gauges, multi-axis clocks, watches, activity gauges, compasses, and other circular indicators.

## When to Use This Skill

Use this skill when you need to:

- **Display metrics circularly** - Speedometers, tachometers, fuel gauges, pressure meters
- **Create dashboard indicators** - KPI gauges, performance monitors, progress indicators
- **Build measurement displays** - Temperature monitors, humidity gauges, voltage meters
- **Implement activity trackers** - Fitness rings, progress circles, goal trackers
- **Design custom dials** - Compass displays, clock faces, directional indicators
- **Show ranges visually** - Color-coded zones (red/yellow/green), danger/warning/safe areas
- **Animate value changes** - Smooth transitions with pointer animations
- **Enable user interaction** - Draggable pointers for value adjustment
- **Display multiple metrics** - Multi-axis gauges showing related data points

## Component Overview

**Key Features:**
- **Circular axis** with customizable scale, labels, ticks, and styling
- **Four pointer types** - Needle, Shape, Content, and Range pointers
- **Visual ranges** - Color-coded segments with gradient support
- **Annotations** - Add text, images, or custom UI elements
- **Animations** - Smooth pointer movements with easing functions
- **Interactive dragging** - User-adjustable pointer values
- **Multiple axes** - Display multiple scales in one gauge
- **Flexible styling** - Pixel or factor-based sizing for responsive layouts

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)

Use when you need to:
- Install and set up Syncfusion WinUI Radial Gauge
- Create your first radial gauge
- Add basic axis, ranges, pointers, and annotations
- Understand the component structure
- Get a complete working example

### Axis Configuration
📄 **Read:** [references/axis-configuration.md](references/axis-configuration.md)

Use when you need to:
- Configure axis minimum, maximum, and interval
- Customize start and end angles (180°, 270°, 360°, etc.)
- Adjust axis radius and positioning
- Style axis line (width, color, gradients)
- Customize labels (format, template, rotation, position)
- Configure ticks (major/minor, length, style, position)
- Show/hide axis elements
- Implement multiple axes
- Create custom scale ranges
- Handle axis events

### Pointers
📄 **Read:** [references/pointers.md](references/pointers.md)

Use when you need to:
- Add needle pointers with knobs and tails
- Use shape pointers (circle, diamond, triangle, etc.)
- Create content pointers with custom UI
- Implement range pointers for arc segments
- Add multiple pointers to one axis
- Enable interactive pointer dragging
- Animate pointer movements
- Handle pointer value change events
- Customize pointer appearance and offset

### Ranges
📄 **Read:** [references/ranges.md](references/ranges.md)

Use when you need to:
- Create color-coded value ranges
- Define start and end values for ranges
- Customize range width (equal or tapered)
- Apply gradients to ranges
- Position ranges (offset from axis)
- Add labels to ranges
- Use range colors for axis elements
- Create template-based range labels

### Annotations
📄 **Read:** [references/annotations.md](references/annotations.md)

Use when you need to:
- Add text labels at specific positions
- Display images on the gauge
- Position annotations using angles or axis values
- Adjust annotation distance from center
- Align annotations (horizontal/vertical)
- Add custom UI elements as annotations

### Animation
📄 **Read:** [references/animation.md](references/animation.md)

Use when you need to:
- Enable pointer animations
- Control animation duration
- Apply easing functions (linear, bounce, elastic, etc.)
- Create smooth value transitions

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)

Use when you need to:
- Look up specific properties
- Understand class hierarchies
- Find available customization options
- Reference complete API documentation

## Quick Start Example

Here's a basic speedometer gauge with ranges and needle pointer:

```xaml
<Window x:Class="RadialGaugeApp.MainWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        xmlns:gauge="using:Syncfusion.UI.Xaml.Gauges">
    
    <gauge:SfRadialGauge>
        <gauge:SfRadialGauge.Axes>
            <gauge:RadialAxis Maximum="150"
                              Interval="10">
                
                <!-- Color-coded ranges -->
                <gauge:RadialAxis.Ranges>
                    <gauge:GaugeRange StartValue="0"
                                      EndValue="50"
                                      Background="Green" />
                    <gauge:GaugeRange StartValue="50"
                                      EndValue="100"
                                      Background="Orange" />
                    <gauge:GaugeRange StartValue="100"
                                      EndValue="150"
                                      Background="Red" />
                </gauge:RadialAxis.Ranges>
                
                <!-- Needle pointer -->
                <gauge:RadialAxis.Pointers>
                    <gauge:NeedlePointer Value="90"
                                         EnableAnimation="True" />
                </gauge:RadialAxis.Pointers>
                
                <!-- Value annotation -->
                <gauge:RadialAxis.Annotations>
                    <gauge:GaugeAnnotation DirectionUnit="Angle"
                                           DirectionValue="90"
                                           PositionFactor="0.5">
                        <gauge:GaugeAnnotation.Content>
                            <TextBlock Text="90"
                                       FontSize="25"
                                       FontWeight="Bold" />
                        </gauge:GaugeAnnotation.Content>
                    </gauge:GaugeAnnotation>
                </gauge:RadialAxis.Annotations>
                
            </gauge:RadialAxis>
        </gauge:SfRadialGauge.Axes>
    </gauge:SfRadialGauge>
    
</Window>
```

```csharp
using Syncfusion.UI.Xaml.Gauges;
using Microsoft.UI.Xaml;

namespace RadialGaugeApp
{
    public sealed partial class MainWindow : Window
    {
        public MainWindow()
        {
            this.InitializeComponent();
            
            // Can also create gauge programmatically
            SfRadialGauge gauge = new SfRadialGauge();
            
            RadialAxis axis = new RadialAxis();
            axis.Maximum = 150;
            axis.Interval = 10;
            
            // Add ranges
            axis.Ranges.Add(new GaugeRange { 
                StartValue = 0, 
                EndValue = 50, 
                Background = new SolidColorBrush(Colors.Green) 
            });
            
            // Add pointer
            axis.Pointers.Add(new NeedlePointer { 
                Value = 90, 
                EnableAnimation = true 
            });
            
            gauge.Axes.Add(axis);
        }
    }
}
```

## Common Patterns

### Pattern 1: Temperature Monitor

```xaml
<gauge:SfRadialGauge>
    <gauge:SfRadialGauge.Axes>
        <gauge:RadialAxis Minimum="-60"
                          Maximum="60"
                          Interval="20"
                          StartAngle="180"
                          EndAngle="0">
            
            <gauge:RadialAxis.Ranges>
                <gauge:GaugeRange StartValue="-60"
                                  EndValue="0"
                                  Background="#2196F3" />
                <gauge:GaugeRange StartValue="0"
                                  EndValue="30"
                                  Background="#4CAF50" />
                <gauge:GaugeRange StartValue="30"
                                  EndValue="60"
                                  Background="#FF5722" />
            </gauge:RadialAxis.Ranges>
            
            <gauge:RadialAxis.Pointers>
                <gauge:RangePointer Value="25"
                                    PointerWidth="15"
                                    EnableAnimation="True" />
            </gauge:RadialAxis.Pointers>
            
            <gauge:RadialAxis.Annotations>
                <gauge:GaugeAnnotation>
                    <gauge:GaugeAnnotation.Content>
                        <TextBlock Text="25°C"
                                   FontSize="30"
                                   FontWeight="Bold" />
                    </gauge:GaugeAnnotation.Content>
                </gauge:GaugeAnnotation>
            </gauge:RadialAxis.Annotations>
            
        </gauge:RadialAxis>
    </gauge:SfRadialGauge.Axes>
</gauge:SfRadialGauge>
```

### Pattern 2: Interactive Draggable Gauge

```xaml
<gauge:SfRadialGauge>
    <gauge:SfRadialGauge.Axes>
        <gauge:RadialAxis ShowTicks="False"
                          AxisLineFill="CornflowerBlue"
                          AxisLineWidth="30">
            
            <gauge:RadialAxis.Pointers>
                <gauge:ShapePointer Value="60"
                                    IsInteractive="True"
                                    MarkerOffset="-30"
                                    Background="Indigo"
                                    ValueChanged="Pointer_ValueChanged" />
            </gauge:RadialAxis.Pointers>
            
        </gauge:RadialAxis>
    </gauge:SfRadialGauge.Axes>
</gauge:SfRadialGauge>
```

```csharp
private void Pointer_ValueChanged(object sender, ValueChangedEventArgs e)
{
    // Handle pointer value changes
    Debug.WriteLine($"New value: {e.Value}");
}
```

### Pattern 3: Multi-Axis Clock

```xaml
<gauge:SfRadialGauge>
    <gauge:SfRadialGauge.Axes>
        <!-- Hours axis -->
        <gauge:RadialAxis Maximum="12"
                          Interval="1"
                          RadiusFactor="0.8"
                          LabelPosition="Outside">
            <gauge:RadialAxis.Pointers>
                <gauge:NeedlePointer Value="10"
                                     NeedleLength="0.5"
                                     NeedleEndWidth="8" />
            </gauge:RadialAxis.Pointers>
        </gauge:RadialAxis>
        
        <!-- Minutes axis -->
        <gauge:RadialAxis Maximum="60"
                          Interval="5"
                          RadiusFactor="0.95"
                          LabelPosition="Outside">
            <gauge:RadialAxis.Pointers>
                <gauge:NeedlePointer Value="35"
                                     NeedleLength="0.7"
                                     NeedleEndWidth="4" />
            </gauge:RadialAxis.Pointers>
        </gauge:RadialAxis>
    </gauge:SfRadialGauge.Axes>
</gauge:SfRadialGauge>
```

### Pattern 4: Progress Ring with Percentage

```xaml
<gauge:SfRadialGauge>
    <gauge:SfRadialGauge.Axes>
        <gauge:RadialAxis ShowLabels="False"
                          ShowTicks="False"
                          StartAngle="270"
                          EndAngle="270"
                          Maximum="100"
                          AxisLineWidth="20"
                          AxisLineFill="LightGray">
            
            <gauge:RadialAxis.Pointers>
                <gauge:RangePointer Value="73"
                                    PointerWidth="20"
                                    Background="#4CAF50"
                                    CornerStyle="BothCurve"
                                    EnableAnimation="True" />
            </gauge:RadialAxis.Pointers>
            
            <gauge:RadialAxis.Annotations>
                <gauge:GaugeAnnotation>
                    <gauge:GaugeAnnotation.Content>
                        <TextBlock>
                            <Run Text="73" FontSize="40" FontWeight="Bold" />
                            <Run Text="%" FontSize="20" />
                        </TextBlock>
                    </gauge:GaugeAnnotation.Content>
                </gauge:GaugeAnnotation>
            </gauge:RadialAxis.Annotations>
            
        </gauge:RadialAxis>
    </gauge:SfRadialGauge.Axes>
</gauge:SfRadialGauge>
```

## Key Properties by Category

### SfRadialGauge
- `Axes` - Collection of RadialAxis objects
- `CanScaleToFit` - Position axis based on start/end angles

### Axis Configuration
- `Minimum` / `Maximum` - Axis value range
- `Interval` - Space between labels
- `StartAngle` / `EndAngle` - Circular arc angles (0-360°)
- `RadiusFactor` - Axis size (0-1 factor of available space)
- `IsInversed` - Counter-clockwise direction

### Axis Styling
- `AxisLineWidth` / `AxisLineWidthUnit` - Line thickness (Pixel/Factor)
- `AxisLineFill` - Line color/brush
- `GradientStops` - Gradient colors on axis line
- `ShowAxisLine` - Axis line visibility

### Labels & Ticks
- `ShowLabels` / `ShowTicks` - Element visibility
- `LabelFormat` - Number format (currency, percent, etc.)
- `LabelTemplate` - Custom label template
- `LabelPosition` / `TickPosition` - Inside/Outside/Cross
- `LabelOffset` / `TickOffset` - Distance from axis
- `MajorTickLength` / `MinorTickLength` - Tick sizes
- `MinorTicksPerInterval` - Minor tick count

### Pointers (All Types)
- `Value` - Current pointer value
- `EnableAnimation` - Animate on value change
- `AnimationDuration` - Animation time (ms)
- `AnimationEasingFunction` - Easing function
- `IsInteractive` - Enable dragging

### Needle Pointer Specific
- `NeedleLength` / `NeedleStartWidth` / `NeedleEndWidth` - Needle shape
- `KnobRadius` / `KnobFill` / `KnobStroke` - Center knob
- `TailLength` / `TailWidth` - Needle tail

### Shape Pointer Specific
- `ShapeType` - Circle, Diamond, Triangle, etc.
- `ShapeHeight` / `ShapeWidth` - Shape size
- `MarkerOffset` - Distance from axis

### Range Pointer Specific
- `PointerWidth` - Arc width
- `CornerStyle` - BothFlat, BothCurve, StartCurve, EndCurve

### Ranges
- `StartValue` / `EndValue` - Range boundaries
- `StartWidth` / `EndWidth` - Range thickness
- `WidthUnit` - Pixel or Factor
- `RangeOffset` - Distance from axis
- `Background` - Range color
- `GradientStops` - Gradient colors
- `Label` / `LabelTemplate` - Range label

### Annotations
- `DirectionUnit` - Angle or AxisValue
- `DirectionValue` - Position value
- `PositionFactor` - Distance from center (0-1)
- `Content` - Any UIElement

## Common Use Cases

1. **Speedometer/Tachometer** - Vehicle speed/RPM display with color-coded danger zones
2. **Temperature Gauge** - Climate monitors with cold/moderate/hot ranges
3. **Pressure Meter** - Tire pressure, hydraulic pressure with threshold indicators
4. **Battery Level** - Circular battery indicator with percentage annotation
5. **Fitness Tracker** - Activity rings showing steps, calories, distance
6. **KPI Dashboard** - Business metrics with goal thresholds
7. **Volume Control** - Draggable circular volume adjuster
8. **Compass** - Directional gauge with degree markings
9. **Timer/Stopwatch** - Elapsed time visualization
10. **Progress Indicator** - Task completion, download progress
11. **Rating Display** - Score visualization (1-10 scale)
12. **Multi-Metric Display** - Multiple axes showing related measurements

## Notes

- All size properties support **Pixel** or **Factor** units for responsive layouts
- Factor values (0-1) are multiplied by axis radius for proportional sizing
- Use **animations** for smooth transitions when updating values
- Enable **IsInteractive** for user-adjustable pointers with drag support
- Multiple axes can share the same center with different radius factors
- **GradientStops** provide smooth color transitions based on axis values
- Annotations can contain any WinUI UIElement (TextBlock, Image, Grid, etc.)

---

**Installation:** Install the `Syncfusion.Gauge.WinUI` NuGet package

**Namespace:** `Syncfusion.UI.Xaml.Gauges`

**GitHub Samples:** [WinUI Radial Gauge Demos](https://github.com/syncfusion/winui-demos/tree/master/radialgauge)
