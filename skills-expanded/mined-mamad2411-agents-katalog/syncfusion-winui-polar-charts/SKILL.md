---
name: syncfusion-winui-polar-charts
description: Implementation guide for Syncfusion WinUI Polar Chart (SfPolarChart) control. Use this when working with polar charts, radar charts, or spider charts for radial data visualization in WinUI applications. This skill covers line and area series for visualizing data in terms of values and angles, multi-dimensional data comparison, and directional data visualization with PolarLineSeries and PolarAreaSeries.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Polar Charts in WinUI

Comprehensive guide for implementing the Syncfusion® WinUI Polar Chart (SfPolarChart) control in Windows App SDK applications. Polar charts visualize data in terms of values and angles, making them ideal for comparing multiple dimensions or showing directional data.

## When to Use This Skill

Use this skill when the user needs to:
- **Create polar charts** (also known as radar, spider, web, star, or cobweb charts)
- **Visualize multi-dimensional data** with multiple categories around a center point
- **Compare multiple data series** on the same radial scale
- **Display directional data** (compass data, wind direction, plant distribution)
- **Show cyclical patterns** or seasonal variations
- **Implement line or area series** in polar coordinates
- **Customize grid line types** (circular or polygon/radar style)
- **Configure axis types** (Category, Numerical, DateTime, Logarithmic)
- **Add legends, data labels, and titles** to polar charts
- **Apply custom styling and themes** to polar visualizations

## Component Overview

**Control:** `SfPolarChart`  
**Namespace:** `Syncfusion.UI.Xaml.Charts`  
**Package:** `Syncfusion.Chart.WinUI`  
**Platform:** WinUI 3 (Windows App SDK)

### Key Features

- ✓ **Two series types:** PolarLineSeries and PolarAreaSeries
- ✓ **Multiple series support:** Compare different datasets on the same chart
- ✓ **Grid line types:** Circle (default) or Polygon (radar/spider style)
- ✓ **Four axis types:** Category, Numerical, DateTime, Logarithmic
- ✓ **Rich customization:** Legends, data labels, titles, appearance
- ✓ **Interactive features:** Toggle series visibility, checkbox legends
- ✓ **Start angle control:** Rotate chart to different starting positions (0°, 90°, 180°, 270°)
- ✓ **Closed/Open paths:** Control whether series form closed loops
- ✓ **MVVM-friendly:** Full data binding support

### Typical Use Cases

- **Business analytics:** Market analysis, competitive comparisons
- **Scientific visualization:** Experiment results, multi-parameter analysis
- **Weather data:** Wind patterns, precipitation by direction
- **Quality metrics:** Performance across multiple dimensions
- **Sports analytics:** Player statistics across different skills
- **Survey results:** Opinion data across categories

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and NuGet package setup (`Syncfusion.Chart.WinUI`)
- Basic polar chart implementation in XAML and C#
- Creating data models and view models
- Binding data to series (ItemsSource, XBindingPath, YBindingPath)
- Setting up primary and secondary axes
- Complete working example from scratch

### Series Types
📄 **Read:** [references/series-types.md](references/series-types.md)
- **PolarLineSeries:** Line-based polar series
- **PolarAreaSeries:** Filled area polar series
- **Grid line types:** Circle vs Polygon (radar/spider chart)
- **Closing paths:** IsClosed property for open/closed series
- **Multiple series:** Displaying multiple datasets together
- Series customization and styling

### Axis Configuration
📄 **Read:** [references/axis-configuration.md](references/axis-configuration.md)
- **CategoryAxis:** Index-based axis for categorical data
- **NumericalAxis:** Numeric values with range customization
- **DateTimeAxis:** Time-based data plotting
- **LogarithmicAxis:** Logarithmic scale for large value ranges
- Axis range customization (Minimum, Maximum, Interval)
- Axis events (ActualRangeChanged, LabelCreated)

### Axis Customization
📄 **Read:** [references/axis-customization.md](references/axis-customization.md)
- **Axis labels:** Rotation, formatting, custom templates
- **Axis titles/headers:** Adding and styling axis headers
- Label style customization (fonts, colors, margins)
- Header templates for advanced customization
- Label format strings for different data types

### Title and Legend
📄 **Read:** [references/title-legend.md](references/title-legend.md)
- **Chart title:** Header property and customization
- Title alignment (left, center, right)
- **Legend configuration:** Icons, spacing, placement
- Checkbox legends for toggling series
- Toggle series visibility interactively
- Legend templates and background styling

### Data Labels
📄 **Read:** [references/data-labels.md](references/data-labels.md)
- Enabling data labels (ShowDataLabels property)
- Label context (YValue, XValue, Percentage)
- Customization (fonts, colors, borders, margins)
- Data label templates for advanced layouts
- Format strings and rotation
- UseSeriesPalette for color coordination
- Connector lines between labels and data points

### Appearance and Styling
📄 **Read:** [references/appearance.md](references/appearance.md)
- **Default palette brushes**
- **Custom palette brushes:** Define your own color schemes
- **Gradient support:** LinearGradientBrush and RadialGradientBrush
- Applying gradients to entire charts or individual series
- Series Fill property customization
- Theme integration

### Start Angle and Positioning
📄 **Read:** [references/start-angle.md](references/start-angle.md)
- StartAngle property (Rotate0, Rotate90, Rotate180, Rotate270)
- Changing rendering position of the chart
- Use cases for different starting angles
- Aligning charts with specific orientations

### Troubleshooting
📄 **Read:** [references/troubleshooting.md](references/troubleshooting.md)
- Common setup and installation issues
- Data binding problems and solutions
- Rendering and display issues
- Performance optimization tips
- Best practices and FAQ

## Quick Start Example

Here's a minimal working example to create a polar area chart:

### 1. Data Model

```csharp
public class PlantData
{
    public string Direction { get; set; }
    public double Tree { get; set; }
}
```

### 2. View Model

```csharp
using System.Collections.ObjectModel;

public class ChartViewModel
{
    public ObservableCollection<PlantData> PlantDetails { get; set; }

    public ChartViewModel()
    {
        PlantDetails = new ObservableCollection<PlantData>()
        {
            new PlantData { Direction = "North", Tree = 80 },
            new PlantData { Direction = "NorthEast", Tree = 87 },
            new PlantData { Direction = "East", Tree = 78 },
            new PlantData { Direction = "SouthEast", Tree = 85 },
            new PlantData { Direction = "South", Tree = 81 },
            new PlantData { Direction = "SouthWest", Tree = 88 },
            new PlantData { Direction = "West", Tree = 80 },
            new PlantData { Direction = "NorthWest", Tree = 85 }
        };
    }
}
```

### 3. XAML Implementation

```xml
<Window
    x:Class="PolarChartDemo.MainWindow"
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    xmlns:chart="using:Syncfusion.UI.Xaml.Charts"
    xmlns:local="using:PolarChartDemo">

    <chart:SfPolarChart Header="Plant Distribution">
        
        <!-- Set DataContext to ViewModel -->
        <chart:SfPolarChart.DataContext>
            <local:ChartViewModel/>
        </chart:SfPolarChart.DataContext>
        
        <!-- Primary Axis (Angular) -->
        <chart:SfPolarChart.PrimaryAxis>
            <chart:CategoryAxis/>
        </chart:SfPolarChart.PrimaryAxis>
        
        <!-- Secondary Axis (Radial) -->
        <chart:SfPolarChart.SecondaryAxis>
            <chart:NumericalAxis/>
        </chart:SfPolarChart.SecondaryAxis>
        
        <!-- Legend -->
        <chart:SfPolarChart.Legend>
            <chart:ChartLegend/>
        </chart:SfPolarChart.Legend>
        
        <!-- Series -->
        <chart:SfPolarChart.Series>
            <chart:PolarAreaSeries ItemsSource="{Binding PlantDetails}"
                                   XBindingPath="Direction"
                                   YBindingPath="Tree"
                                   Label="Tree"
                                   ShowDataLabels="True"/>
        </chart:SfPolarChart.Series>
        
    </chart:SfPolarChart>

</Window>
```

### 4. C# Code-Behind (Alternative)

```csharp
using Syncfusion.UI.Xaml.Charts;

public sealed partial class MainWindow : Window
{
    public MainWindow()
    {
        this.InitializeComponent();
        
        // Create chart
        SfPolarChart chart = new SfPolarChart();
        chart.Header = "Plant Distribution";
        
        // Set ViewModel
        ChartViewModel viewModel = new ChartViewModel();
        chart.DataContext = viewModel;
        
        // Configure axes
        chart.PrimaryAxis = new CategoryAxis();
        chart.SecondaryAxis = new NumericalAxis();
        
        // Add legend
        chart.Legend = new ChartLegend();
        
        // Create series
        PolarAreaSeries series = new PolarAreaSeries();
        series.XBindingPath = "Direction";
        series.YBindingPath = "Tree";
        series.Label = "Tree";
        series.ShowDataLabels = true;
        series.SetBinding(
            ChartSeriesBase.ItemsSourceProperty,
            new Binding() { Path = new PropertyPath("PlantDetails") });
        
        chart.Series.Add(series);
        
        // Add chart to window
        this.Content = chart;
    }
}
```

## Common Patterns

### Pattern 1: Radar/Spider Chart (Polygon Grid)

Create a classic radar chart with polygon grid lines:

```xml
<chart:SfPolarChart GridLineType="Polygon">
    <chart:SfPolarChart.PrimaryAxis>
        <chart:CategoryAxis/>
    </chart:SfPolarChart.PrimaryAxis>
    <chart:SfPolarChart.SecondaryAxis>
        <chart:NumericalAxis/>
    </chart:SfPolarChart.SecondaryAxis>
    
    <chart:PolarLineSeries ItemsSource="{Binding Data}"
                           XBindingPath="Category"
                           YBindingPath="Value"
                           IsClosed="True"/>
</chart:SfPolarChart>
```

### Pattern 2: Multiple Series Comparison

Compare multiple datasets on the same chart:

```xml
<chart:SfPolarChart Header="Multi-Series Comparison">
    <chart:SfPolarChart.Legend>
        <chart:ChartLegend/>
    </chart:SfPolarChart.Legend>
    
    <chart:SfPolarChart.Series>
        <chart:PolarLineSeries ItemsSource="{Binding SeriesA}"
                               XBindingPath="Category"
                               YBindingPath="Value"
                               Label="Product A"/>
        
        <chart:PolarLineSeries ItemsSource="{Binding SeriesB}"
                               XBindingPath="Category"
                               YBindingPath="Value"
                               Label="Product B"/>
        
        <chart:PolarLineSeries ItemsSource="{Binding SeriesC}"
                               XBindingPath="Category"
                               YBindingPath="Value"
                               Label="Product C"/>
    </chart:SfPolarChart.Series>
</chart:SfPolarChart>
```

### Pattern 3: Styled Data Labels

Add formatted data labels with custom appearance:

```xml
<chart:PolarAreaSeries ShowDataLabels="True">
    <chart:PolarAreaSeries.DataLabelSettings>
        <chart:PolarDataLabelSettings Context="YValue"
                                      Foreground="White"
                                      Background="#1E88E5"
                                      BorderBrush="White"
                                      BorderThickness="1"
                                      FontSize="12"
                                      FontFamily="Calibri"
                                      Format="#.0"/>
    </chart:PolarAreaSeries.DataLabelSettings>
</chart:PolarAreaSeries>
```

### Pattern 4: Custom Color Palette

Apply custom colors to the chart:

```xml
<chart:SfPolarChart>
    <chart:SfPolarChart.Resources>
        <BrushCollection x:Key="customBrushes">
            <SolidColorBrush Color="#4dd0e1"/>
            <SolidColorBrush Color="#26c6da"/>
            <SolidColorBrush Color="#00bcd4"/>
        </BrushCollection>
    </chart:SfPolarChart.Resources>
    
    <chart:SfPolarChart PaletteBrushes="{StaticResource customBrushes}">
        <!-- Chart content -->
    </chart:SfPolarChart>
</chart:SfPolarChart>
```

## Key Properties

### SfPolarChart Properties

| Property | Type | Description |
|----------|------|-------------|
| `Header` | object | Chart title/header |
| `PrimaryAxis` | ChartAxis | Angular axis (around the circle) |
| `SecondaryAxis` | ChartAxis | Radial axis (from center outward) |
| `Series` | ChartSeriesCollection | Collection of series to display |
| `Legend` | ChartLegend | Legend configuration |
| `GridLineType` | PolarChartGridLineType | Circle or Polygon |
| `StartAngle` | ChartPolarAngle | Starting angle (0°, 90°, 180°, 270°) |
| `PaletteBrushes` | IList<Brush> | Custom color palette |

### PolarSeries Properties

| Property | Type | Description |
|----------|------|-------------|
| `ItemsSource` | IEnumerable | Data source for the series |
| `XBindingPath` | string | Property path for X values (categories) |
| `YBindingPath` | string | Property path for Y values (numeric) |
| `Label` | string | Series label for legend |
| `ShowDataLabels` | bool | Show/hide data labels |
| `IsClosed` | bool | Close the path (connect last to first) |
| `Fill` | Brush | Fill color for the series |
| `Stroke` | Brush | Stroke color for line series |
| `DataLabelSettings` | PolarDataLabelSettings | Data label configuration |

### Axis Properties

| Property | Type | Description |
|----------|------|-------------|
| `Header` | object | Axis title |
| `Minimum` | double | Minimum axis value |
| `Maximum` | double | Maximum axis value |
| `Interval` | double | Interval between labels |
| `LabelRotation` | double | Rotation angle for labels |
| `LabelStyle` | LabelStyle | Label formatting and appearance |

## Common Use Cases

### Use Case 1: Market Analysis Dashboard
**Scenario:** Compare product performance across multiple metrics  
**Implementation:** Multi-series polar chart with polygon grid  
**Read:** [references/series-types.md](references/series-types.md) for multiple series

### Use Case 2: Weather Data Visualization
**Scenario:** Display wind speed/direction or precipitation patterns  
**Implementation:** Polar area chart with directional categories  
**Read:** [references/getting-started.md](references/getting-started.md) for data binding

### Use Case 3: Skills Assessment
**Scenario:** Visualize employee or player skills across dimensions  
**Implementation:** Radar chart with data labels showing scores  
**Read:** [references/data-labels.md](references/data-labels.md) for label customization

### Use Case 4: Quality Metrics
**Scenario:** Show product quality across multiple test parameters  
**Implementation:** Polar line chart with custom color coding  
**Read:** [references/appearance.md](references/appearance.md) for styling

### Use Case 5: Scientific Data
**Scenario:** Plot experimental results with logarithmic scale  
**Implementation:** Polar chart with logarithmic axis  
**Read:** [references/axis-configuration.md](references/axis-configuration.md) for axis types

## Best Practices

1. **Choose the right series type:**
   - Use **PolarLineSeries** for trends and comparisons
   - Use **PolarAreaSeries** to emphasize magnitude and coverage

2. **Grid line type selection:**
   - Use **Circle** for continuous data and smoother appearance
   - Use **Polygon** for categorical data and classic radar chart look

3. **Axis configuration:**
   - Use **CategoryAxis** for named categories (directions, labels)
   - Use **NumericalAxis** for numeric ranges on radial axis
   - Set appropriate Minimum, Maximum, and Interval for readability

4. **Data labels:**
   - Enable for small to medium datasets (< 20 points)
   - Use rotation and connector lines for better positioning
   - Format values appropriately for the data type

5. **Multiple series:**
   - Limit to 3-5 series for clarity
   - Use distinct colors and legend
   - Consider line series for overlapping data

6. **Performance:**
   - Use ObservableCollection for dynamic data
   - Avoid excessive data points in a single series
   - Implement data virtualization for very large datasets

7. **Accessibility:**
   - Provide meaningful chart titles and axis labels
   - Use high-contrast colors
   - Include legend for series identification

## Related Components

- **Circular Charts:** For pie, doughnut, and radial bar charts
- **Cartesian Charts:** For traditional X-Y coordinate charts (line, bar, column)
- **Gauges:** For single-value radial indicators

## Resources

- [Official Documentation](https://help.syncfusion.com/winui/polar-chart/overview)
- [API Reference - SfPolarChart](https://help.syncfusion.com/cr/winui/Syncfusion.UI.Xaml.Charts.SfPolarChart.html)
- [GitHub Samples](https://github.com/syncfusion/winui-demos)
- [Knowledge Base](https://www.syncfusion.com/kb/winui)

---

**Next Steps:** Navigate to a specific reference document above to implement polar chart features in your WinUI application.
