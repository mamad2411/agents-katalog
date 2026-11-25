---
name: syncfusion-winforms-radial-gauge
description: Guide for implementing Syncfusion Gauge controls in Windows Forms applications. Use when creating data visualization gauges such as RadialGauge for circular displays (speedometers, temperature dials), LinearGauge for horizontal/vertical bars and progress indicators, or DigitalGauge for LED-style alphanumeric displays. Covers dashboard gauges, instrument panels, real-time monitoring, and KPI displays with needles, ranges, and scales.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Gauges

## When to Use This Skill

Use this skill when the user needs to implement Syncfusion **Gauge controls** in a Windows Forms application. This skill covers three gauge types for different visualization needs:

### RadialGauge Use Cases
1. **Speedometers and tachometers** - Vehicle instrumentation, RPM displays
2. **Temperature gauges** - HVAC controls, system monitoring, weather displays
3. **Pressure gauges** - Industrial monitoring, tire pressure, hydraulic systems
4. **Progress indicators** - Circular progress for loading, completion percentage
5. **KPI dashboards** - Performance metrics with color-coded ranges
6. **Dial controls** - Volume, brightness, or any rotary control visualization
7. **Compass displays** - Navigation, orientation indicators
8. **Clock faces** - Analog time displays with custom styling

### LinearGauge Use Cases
1. **Progress bars** - Task completion, download progress, loading status
2. **Level indicators** - Battery level, fuel gauge, volume meters
3. **Slider visualizations** - Temperature sliders, adjustment controls
4. **Horizontal meters** - Audio levels, signal strength, capacity indicators
5. **Vertical meters** - Building height indicators, elevator position
6. **Thermometer displays** - Temperature scales, medical thermometers
7. **Timeline indicators** - Project timelines, milestone tracking

### DigitalGauge Use Cases
1. **Digital clocks** - Time displays, countdown timers, stopwatches
2. **Counters** - Visitor counters, production counters, score displays
3. **Alphanumeric status** - System codes, product IDs, status messages
4. **LED displays** - Retro-style indicators, industrial displays
5. **Price displays** - Gas station prices, retail pricing
6. **Measurement readouts** - Digital multimeters, sensor readings

**When NOT to use:** For simple text displays without gauge visualization, use standard Label or TextBox controls. For charts and graphs, use Chart controls.

## Component Overview

Syncfusion provides **three gauge controls** for data visualization in Windows Forms:

### 1. RadialGauge
Visualizes values on a **circular or arc scale** with customizable needles, ranges, and frames.

**Key Features:**
- 4 frame types: FullCircle, HalfCircle, QuarterCircle, Fill
- Multiple needles support
- Color-coded ranges for visual thresholds
- Customizable scales, ticks, and labels
- Gradient backgrounds and styling
- Custom needle styles (Default, Advanced, Pointer)

### 2. LinearGauge
Visualizes values on a **linear scale** (horizontal or vertical) with pointer indicators.

**Key Features:**
- Horizontal and vertical orientations
- Pointer placement (Top, Center, Bottom)
- Color-coded ranges
- Major and minor tick marks
- Value indicator bars
- Gradient styling

### 3. DigitalGauge
Displays **alphanumeric characters** in LED/digital format.

**Key Features:**
- 4 character types: DotMatrix, SevenSegment, FourteenSegment, SixteenSegment
- Configurable character count
- Segment spacing control
- Invisible segment display option
- Rounded corners support

**All gauges support:**
- Visual themes (9 built-in + custom)
- Data binding for real-time updates
- Custom renderers for complete visual control
- Professional styling options

## Documentation and Navigation Guide

### Installation and Setup
📄 **Read:** [references/installation-and-setup.md](references/installation-and-setup.md)

When user needs to set up gauge controls for the first time. Covers:
- Assembly references (Syncfusion.Gauge.Windows.dll, Syncfusion.Shared.Base.dll)
- NuGet package installation
- Namespace imports (Syncfusion.Windows.Forms.Gauge)
- Framework support (.NET 4.5+, .NET 6.0-8.0)
- Deployment requirements
- Toolbox configuration
- Sample browser location

### RadialGauge (Circular Gauges)
📄 **Read:** [references/radial-gauge.md](references/radial-gauge.md)

When user needs circular, arc, or dial-style gauges. Covers:
- Frame types (FullCircle, HalfCircle, QuarterCircle, Fill)
- Designer and code-based setup
- Scales and labels (placement, orientation, colors)
- Ticks (major/minor configuration, heights, colors)
- Needles (single and multiple, styles, colors)
- Ranges (color-coded value ranges with start/end)
- Scaling divisions (MajorDifference, MinorDifference)
- StartAngle and SweepAngle customization
- Frame appearance (gradients, arc colors)
- Label customization with DrawLabel event
- Performance optimization tips

### LinearGauge (Bar/Slider Gauges)
📄 **Read:** [references/linear-gauge.md](references/linear-gauge.md)

When user needs horizontal or vertical bar-style gauges. Covers:
- Frame types (Horizontal, Vertical)
- Designer and code-based setup
- Scales and label configuration
- Tick marks (major/minor)
- Pointer placement options
- Needle display and styling
- Ranges (LinearRange with colors)
- Value indicator positioning
- Frame appearance customization
- Complete orientation examples

### DigitalGauge (LED Display)
📄 **Read:** [references/digital-gauge.md](references/digital-gauge.md)

When user needs LED-style alphanumeric displays. Covers:
- Character types (DotMatrix, SevenSegment, FourteenSegment, SixteenSegment)
- Designer and code-based setup
- Character count limiting
- Segment spacing configuration
- ShowInvisibleSegments property
- RoundCornerRadius for rounded edges
- Value property for string display
- Frame customization
- Examples for each character type

### Visual Themes and Styling
📄 **Read:** [references/visual-themes.md](references/visual-themes.md)

When user wants to apply professional themes or custom styling. Covers:
- VisualStyle property (applies to all 3 gauge types)
- Built-in themes (Blue, Black, Silver, Metro, Office2016 variants)
- Custom theme creation (ThemeBrush collections)
- Color customization properties
- Design-time theme setup
- Theme-specific examples for each gauge type
- Consistent application-wide theming

### Custom Renderers
📄 **Read:** [references/custom-renderers.md](references/custom-renderers.md)

When user needs complete control over gauge rendering and appearance. Covers:
- IRadialGaugeRenderer interface
- ILinearGaugeRenderer interface
- Creating custom renderer classes
- DrawOuterArc, DrawNeedle, DrawLabel, DrawRanges methods
- Renderer property assignment
- Advanced customization scenarios
- Complete custom renderer examples

### Data Binding
📄 **Read:** [references/data-binding.md](references/data-binding.md)

When user needs real-time data updates or database-driven gauges. Covers:
- DataSource property configuration
- DisplayMember (column mapping)
- DisplayRecordIndex (row mapping)
- High-frequency data updates
- Real-time monitoring scenarios
- Performance considerations
- Complete binding examples for all gauge types

## Quick Start Examples

### RadialGauge: Speedometer

```csharp
using Syncfusion.Windows.Forms.Gauge;

// Create RadialGauge
RadialGauge speedometer = new RadialGauge();
speedometer.Size = new Size(300, 300);
speedometer.Location = new Point(20, 20);

// Configure gauge properties
speedometer.MinimumValue = 0;
speedometer.MaximumValue = 200;
speedometer.MajorDifference = 20;
speedometer.MinorDifference = 5;
speedometer.Value = 60;

// Set frame type
speedometer.FrameType = FrameType.HalfCircle;

// Configure appearance
speedometer.ShowNeedle = true;
speedometer.NeedleStyle = NeedleStyle.Advanced;
speedometer.GaugeLabel = "Speed (MPH)";

// Add color-coded ranges
Range range1 = new Range();
range1.StartValue = 0;
range1.EndValue = 80;
range1.Color = Color.Green;
range1.Height = 10;
speedometer.Ranges.Add(range1);

Range range2 = new Range();
range2.StartValue = 80;
range2.EndValue = 150;
range2.Color = Color.Yellow;
range2.Height = 10;
speedometer.Ranges.Add(range2);

Range range3 = new Range();
range3.StartValue = 150;
range3.EndValue = 200;
range3.Color = Color.Red;
range3.Height = 10;
speedometer.Ranges.Add(range3);

// Add to form
this.Controls.Add(speedometer);
```

### LinearGauge: Battery Level

```csharp
using Syncfusion.Windows.Forms.Gauge;

// Create LinearGauge
LinearGauge batteryLevel = new LinearGauge();
batteryLevel.Size = new Size(300, 125);
batteryLevel.Location = new Point(20, 20);

// Set horizontal orientation
batteryLevel.LinearFrameType = LinearFrameType.Horizontal;

// Configure gauge properties
batteryLevel.MinimumValue = 0;
batteryLevel.MaximumValue = 100;
batteryLevel.MajorDifference = 20;
batteryLevel.MinorTickCount = 3;
batteryLevel.Value = 75;

// Configure appearance
batteryLevel.ShowNeedle = true;
batteryLevel.PointerPlacement = Placement.Center;

// Add color-coded ranges
LinearRange lowRange = new LinearRange();
lowRange.StartValue = 0;
lowRange.EndValue = 20;
lowRange.Color = Color.Red;
lowRange.Height = 8;
batteryLevel.Ranges.Add(lowRange);

LinearRange normalRange = new LinearRange();
normalRange.StartValue = 20;
normalRange.EndValue = 80;
normalRange.Color = Color.Yellow;
normalRange.Height = 8;
batteryLevel.Ranges.Add(normalRange);

LinearRange highRange = new LinearRange();
highRange.StartValue = 80;
highRange.EndValue = 100;
highRange.Color = Color.Green;
highRange.Height = 8;
batteryLevel.Ranges.Add(highRange);

// Add to form
this.Controls.Add(batteryLevel);
```

### DigitalGauge: LED Clock

```csharp
using Syncfusion.Windows.Forms.Gauge;

// Create DigitalGauge
DigitalGauge digitalClock = new DigitalGauge();
digitalClock.Size = new Size(250, 100);
digitalClock.Location = new Point(20, 20);

// Configure character display
digitalClock.CharacterType = CharacterType.SevenSegment;
digitalClock.CharacterCount = 8;
digitalClock.SegmentSpacing = 2.0f;

// Set initial value
digitalClock.Value = DateTime.Now.ToString("HH:mm:ss");

// Configure appearance
digitalClock.ForeColor = Color.Red;
digitalClock.ShowInvisibleSegments = true;

// Add timer to update clock
Timer clockTimer = new Timer();
clockTimer.Interval = 1000; // 1 second
clockTimer.Tick += (s, e) => {
    digitalClock.Value = DateTime.Now.ToString("HH:mm:ss");
};
clockTimer.Start();

// Add to form
this.Controls.Add(digitalClock);
```

## Common Patterns

### Pattern 1: Dashboard with Multiple Gauges

```csharp
// Create dashboard layout
FlowLayoutPanel dashboard = new FlowLayoutPanel();
dashboard.Dock = DockStyle.Fill;

// Temperature gauge (RadialGauge)
RadialGauge tempGauge = new RadialGauge();
tempGauge.MinimumValue = -20;
tempGauge.MaximumValue = 120;
tempGauge.Value = 72;
tempGauge.GaugeLabel = "°F";
tempGauge.FrameType = FrameType.HalfCircle;
dashboard.Controls.Add(tempGauge);

// Fuel level (LinearGauge)
LinearGauge fuelGauge = new LinearGauge();
fuelGauge.LinearFrameType = LinearFrameType.Vertical;
fuelGauge.MinimumValue = 0;
fuelGauge.MaximumValue = 100;
fuelGauge.Value = 45;
dashboard.Controls.Add(fuelGauge);

// Status counter (DigitalGauge)
DigitalGauge statusCounter = new DigitalGauge();
statusCounter.CharacterType = CharacterType.SevenSegment;
statusCounter.Value = "1234";
dashboard.Controls.Add(statusCounter);

this.Controls.Add(dashboard);
```

### Pattern 2: Data-Bound Real-Time Gauge

```csharp
// Setup data source
DataTable sensorData = new DataTable();
sensorData.Columns.Add("SensorValue", typeof(float));
sensorData.Rows.Add(0);

// Create and bind gauge
RadialGauge sensorGauge = new RadialGauge();
sensorGauge.DataSource = sensorData;
sensorGauge.DisplayMember = "SensorValue";
sensorGauge.DisplayRecordIndex = 0;

// Timer to simulate sensor updates
Timer dataTimer = new Timer();
dataTimer.Interval = 100; // 10 updates per second
dataTimer.Tick += (s, e) => {
    // Update data source (gauge updates automatically)
    sensorData.Rows[0]["SensorValue"] = GetSensorReading();
};
dataTimer.Start();
```

### Pattern 3: Themed Gauge Set

```csharp
// Apply consistent theme to all gauges
void ApplyTheme(Control.ControlCollection controls, ThemeStyle theme)
{
    foreach (Control control in controls)
    {
        if (control is RadialGauge radial)
            radial.VisualStyle = theme;
        else if (control is LinearGauge linear)
            linear.VisualStyle = theme;
        else if (control is DigitalGauge digital)
            digital.VisualStyle = theme;
            
        if (control.HasChildren)
            ApplyTheme(control.Controls, theme);
    }
}

// Usage
ApplyTheme(this.Controls, ThemeStyle.Office2016Colorful);
```

## Gauge Type Selection Guide

| Need | Use This Gauge | Why |
|------|---------------|-----|
| Circular display (speedometer style) | **RadialGauge** | Natural for rotary values, intuitive needle movement |
| Arc/partial circle | **RadialGauge** (HalfCircle/QuarterCircle) | Space-efficient, modern dashboard look |
| Horizontal progress bar | **LinearGauge** (Horizontal) | Clear left-to-right progression |
| Vertical level indicator | **LinearGauge** (Vertical) | Natural for height/depth/level visualization |
| Time display (LED style) | **DigitalGauge** (SevenSegment) | Classic digital clock appearance |
| Alphanumeric status code | **DigitalGauge** (FourteenSegment/SixteenSegment) | Supports letters and numbers |
| Multiple needles on one dial | **RadialGauge** (EnableCustomNeedles) | Compare multiple values on same scale |
| Fill-based progress indicator | **RadialGauge** (FrameType.Fill) | Visual fill from start to current value |

## Key Properties Comparison

### Common to All Gauges

| Property | Type | Description |
|----------|------|-------------|
| `Value` | float (Radial/Linear) / string (Digital) | Current displayed value |
| `MinimumValue` | float | Minimum scale value (Radial/Linear only) |
| `MaximumValue` | float | Maximum scale value (Radial/Linear only) |
| `VisualStyle` | ThemeStyle | Theme: Blue, Black, Silver, Metro, Office2016*, Custom |
| `DataSource` | object | Data source for binding |
| `DisplayMember` | string | Column name for value binding |
| `DisplayRecordIndex` | int | Row index for value binding |

### RadialGauge Specific

| Property | Type | Description |
|----------|------|-------------|
| `FrameType` | FrameType | FullCircle, HalfCircle, QuarterCircle, Fill |
| `StartAngle` | int | Starting angle of arc (degrees) |
| `SweepAngle` | int | Arc span length (degrees) |
| `ShowNeedle` | bool | Display pointer needle |
| `NeedleStyle` | NeedleStyle | Default, Advanced, Pointer |
| `EnableCustomNeedles` | bool | Allow multiple needles |
| `Ranges` | RangeCollection | Color-coded value ranges |
| `MajorDifference` | float | Spacing between major ticks |
| `MinorDifference` | float | Spacing between minor ticks |

### LinearGauge Specific

| Property | Type | Description |
|----------|------|-------------|
| `LinearFrameType` | LinearFrameType | Horizontal or Vertical |
| `PointerPlacement` | Placement | Top, Center, Bottom |
| `ShowNeedle` | bool | Display pointer |
| `Ranges` | LinearRangeCollection | Color-coded value ranges |
| `MajorDifference` | float | Spacing between major ticks |
| `MinorTickCount` | int | Number of minor ticks between majors |

### DigitalGauge Specific

| Property | Type | Description |
|----------|------|-------------|
| `Value` | string | Text to display |
| `CharacterType` | CharacterType | DotMatrix, SevenSegment, FourteenSegment, SixteenSegment |
| `CharacterCount` | int | Number of characters to display |
| `SegmentSpacing` | float | Spacing between characters |
| `ShowInvisibleSegments` | bool | Show inactive segments |
| `RoundCornerRadius` | int | Corner rounding radius |

## Common Use Cases

### 1. Industrial Dashboard
**Scenario:** Monitor multiple sensors (pressure, temperature, RPM)  
**Solution:** Multiple RadialGauges with color-coded ranges and real-time data binding

### 2. Progress Indicator
**Scenario:** Show task completion percentage  
**Solution:** LinearGauge (Horizontal) or RadialGauge (Fill type) with 0-100 range

### 3. Digital Clock Display
**Scenario:** Display current time in LED format  
**Solution:** DigitalGauge with SevenSegment character type, timer for updates

### 4. Vehicle Instrument Cluster
**Scenario:** Speedometer, tachometer, fuel gauge  
**Solution:** RadialGauges (HalfCircle for speed/RPM), LinearGauge (Vertical for fuel)

### 5. System Monitor
**Scenario:** CPU usage, memory, network speed  
**Solution:** Mix of RadialGauges (percentage dials) and DigitalGauges (numeric readouts)

### 6. Temperature Control
**Scenario:** Thermostat with visual temperature display  
**Solution:** RadialGauge (FullCircle) with color ranges (blue=cold, yellow=moderate, red=hot)

## Best Practices

1. **Choose appropriate gauge type** - RadialGauge for rotary values, LinearGauge for linear progression, DigitalGauge for alphanumeric
2. **Use color-coded ranges** - Visual thresholds improve readability (green=good, yellow=warning, red=critical)
3. **Set meaningful scales** - Configure Min/Max and MajorDifference to match your data range
4. **Apply consistent themes** - Use same VisualStyle across all gauges in application
5. **Optimize real-time updates** - Use data binding for frequent updates instead of manual Value setting
6. **Label your gauges** - Set GaugeLabel property to clarify what's being measured
7. **Consider performance** - For many gauges, use SuspendLayout/ResumeLayout when configuring multiple properties
8. **Test different frame types** - HalfCircle and QuarterCircle save space while remaining readable
