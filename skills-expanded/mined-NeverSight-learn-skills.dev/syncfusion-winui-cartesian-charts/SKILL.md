---
name: syncfusion-winui-cartesian-charts
description: Implements Syncfusion WinUI Cartesian Charts (SfCartesianChart) for data visualization in WinUI applications. Use this when working with column, line, bar, area, or financial charts (OHLC, Candle). This skill covers axis configuration, legends, tooltips, zooming/panning, data labels, and high-performance fast series for large datasets.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion WinUI Cartesian Charts

The Syncfusion WinUI Cartesian Chart (SfCartesianChart) provides a powerful way to visualize data with high interactivity, flexibility, and performance. It supports multiple series types, extensive customization options, and interactive features like zooming, panning, tooltips, and selection.

## When to Use This Skill

Use this skill when the user needs to:

- **Create any cartesian chart** in a WinUI application (column, line, area, bar, scatter, bubble, financial, stacked charts)
- **Configure chart axes** (CategoryAxis, NumericalAxis, DateTimeAxis, LogarithmicAxis, multiple axes)
- **Implement high-performance charts** with large datasets (fast series with millions of data points)
- **Add interactive features** (zooming, panning, tooltips, trackball, crosshair, selection)
- **Customize chart appearance** (legends, data labels, colors, themes, styling)
- **Display financial data** (OHLC, candlestick charts)
- **Compare multiple data series** in the same chart area
- **Create stacked visualizations** to show part-to-whole relationships
- **Handle touch and mouse interactions** for data exploration

## Component Overview

The **SfCartesianChart** is Syncfusion's primary charting control for WinUI applications, designed to visualize data using a two-dimensional cartesian coordinate system with horizontal (X) and vertical (Y) axes. It excels at displaying relationships, trends, comparisons, and distributions across various data types.

### What Makes SfCartesianChart Powerful

**Versatile Visualization**: Supports 15+ series types ranging from basic (column, line, area, bar) to specialized (scatter, bubble, financial OHLC/Candle) to high-performance (fast series for millions of data points). All series can be mixed within the same chart for rich, multi-dimensional visualizations.

**Flexible Axis System**: Provides four axis types (Numerical, Category, DateTime, Logarithmic) with support for multiple axes per chart. This enables complex scenarios like displaying stock prices with volume on separate Y-axes, or comparing datasets with different scales side-by-side.

**High Performance**: Fast series variants use optimized rendering techniques (polyline segments and WriteableBitmap) to handle massive datasets—up to millions of data points—with smooth interactions. Essential for real-time monitoring, IoT telemetry, and scientific applications.

**Rich Interactivity**: Built-in support for zooming (pinch, mouse wheel), panning, tooltips, trackball (multi-series tracking), crosshair, and selection. Users can explore data naturally through touch and mouse gestures without custom code.

**Enterprise-Ready Customization**: Every visual aspect is customizable—from axis labels, grid lines, and legends to series colors, data labels, and chart areas. Supports templates for tooltips and legends, enabling branded, professional visualizations that match application themes.

### Core Architecture

```
SfCartesianChart
├── XAxes Collection (1+ horizontal axes)
├── YAxes Collection (1+ vertical axes)
├── Series Collection (1+ data series)
│   ├── Basic: ColumnSeries, BarSeries, LineSeries, AreaSeries
│   ├── Specialized: ScatterSeries, BubbleSeries, CandleSeries, OHLCSeries
│   ├── Stacked: StackedColumnSeries, StackedAreaSeries, Stacked100Series
│   └── Fast: FastLineBitmapSeries, FastColumnBitmapSeries, FastScatterBitmapSeries
├── Legend (optional)
├── ZoomPanBehavior (optional)
└── Visual Elements (Header, ChartArea, PlotArea, PaletteBrushes)
```

### Key Capabilities at a Glance

- **Data Binding**: Direct binding to ObservableCollection, List, or any IEnumerable with automatic updates
- **Multiple Series**: Display unlimited series in one chart with automatic color assignment and legend coordination
- **Real-Time Updates**: Supports dynamic data with efficient rendering for live dashboards and monitoring
- **Touch & Mouse**: Full gesture support for mobile and desktop scenarios (pinch-zoom, pan, hover tooltips)
- **Accessibility**: Built with WinUI standards for keyboard navigation and screen reader support
- **Responsive**: Adapts to container size changes with automatic axis label optimization

### When to Choose SfCartesianChart vs. Other Chart Types

**Use SfCartesianChart when**: Data has two quantitative dimensions (X and Y), time-series analysis, comparisons across categories, trend analysis, financial data (OHLC), scientific plots, or any scenario requiring rectangular coordinate system.

**Consider alternatives when**: 
- **Circular relationships** → Use SfCircularChart (Pie, Doughnut, Radial Bar)
- **Hierarchical data** → Use SfPyramidChart or SfFunnelChart
- **Directional data** → Use SfPolarChart

## Key Features

### Series Types
- **Basic Series:** Column, Bar, Line, Area
- **Specialized Series:** Scatter, Bubble, Candle, OHLC
- **Stacked Series:** Stacked Column/Bar/Line/Area, Stacked100
- **Fast Series:** FastLine, FastLineBitmap, FastColumn, FastScatter, FastStepLine (optimized for millions of points)

### Axes
- **Types:** NumericalAxis, CategoryAxis, DateTimeAxis, LogarithmicAxis
- **Features:** Multiple axes, custom intervals, range customization, inversed/opposed positioning
- **Customization:** Labels, headers, grid lines, tick lines, padding, auto-scrolling

### Interactive Features
- Zooming and panning (touch/mouse)
- Tooltips with custom templates
- Trackball for multi-series tracking
- Crosshair for precise reading
- Segment and series selection

### Customization
- Legends with positioning and templates
- Data labels with positioning and formatting
- Chart titles and headers
- ChartArea and PlotArea styling
- Color palettes and themes

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installing Syncfusion.Chart.WinUI NuGet package
- Namespace imports and control initialization
- Creating ViewModel with data binding
- Setting up XAxes and YAxes
- Adding your first series
- Complete working example with ColumnSeries

### Axes Configuration

#### Axis Types
📄 **Read:** [references/axis-types.md](references/axis-types.md)
- **NumericalAxis** - For numeric data with interval and range customization
- **CategoryAxis** - For categorical data with index-based plotting and label placement options
- **DateTimeAxis** - For time-series data with date/time formatting and interval types
- **LogarithmicAxis** - For logarithmic scale with customizable base
- When to use each axis type
- Interval configuration and range customization

#### Axis Customization
📄 **Read:** [references/axis-customization.md](references/axis-customization.md)
- Axis labels (rotation, formatting, styling)
- Axis headers and titles
- Grid lines (major/minor, visibility, styling)
- Tick lines (customization and styling)
- Axis line styling
- Padding and range padding
- IsInversed and OpposedPosition properties
- Auto-scrolling with AutoScrollingDelta

#### Multiple Axes
📄 **Read:** [references/multiple-axes.md](references/multiple-axes.md)
- Using XAxes and YAxes collections
- Assigning series to specific axes (XAxisName, YAxisName)
- Arranging multiple series with different scales
- Stacked vs side-by-side axis arrangements
- Axis events (ActualRangeChanged, LabelCreated)

### Series Types

#### Basic Series
📄 **Read:** [references/basic-series.md](references/basic-series.md)
- **ColumnSeries** - Vertical bars for comparing categories
- **BarSeries** - Horizontal bars for ranking or comparison
- **LineSeries** - Connected points showing trends over time
- **AreaSeries** - Filled regions showing magnitude and trends
- ItemsSource, XBindingPath, YBindingPath configuration
- Common properties and styling

#### Specialized Series
📄 **Read:** [references/specialized-series.md](references/specialized-series.md)
- **ScatterSeries** - XY plots for correlation analysis
- **BubbleSeries** - Three-dimensional data with size representation
- **CandleSeries** - Financial OHLC data with filled bodies
- **OHLCSeries** - Open-High-Low-Close financial data
- Financial data binding patterns
- Bubble size configuration

#### Stacked Series
📄 **Read:** [references/stacked-series.md](references/stacked-series.md)
- **Stacked series** - Column, Bar, Line, Area (show cumulative totals)
- **Stacked100 series** - Percentage-based comparison (100% stacked)
- Grouping multiple stacked series
- Data requirements and coordination
- Use cases for part-to-whole analysis

#### Fast Series (High Performance)
📄 **Read:** [references/fast-series.md](references/fast-series.md)
- **FastLineSeries** - Polyline rendering for large line datasets
- **FastLineBitmapSeries** - WriteableBitmap rendering (millions of points)
- **FastColumnBitmapSeries** - High-performance column rendering
- **FastScatterBitmapSeries** - Large scatter plots
- **FastStepLineBitmapSeries** - Step line charts with performance optimization
- EnableAntiAliasing for bitmap-based series
- When to use fast series vs standard series
- Performance best practices

### Interactive Features

#### Tooltip, Trackball, and Crosshair
📄 **Read:** [references/tooltip-trackball-crosshair.md](references/tooltip-trackball-crosshair.md)
- **Tooltips** - EnableTooltip, custom templates, styling
- **Trackball** - Multi-series tracking with vertical line indicator
- **Crosshair** - Precise reading with horizontal and vertical lines
- Touch and mouse interaction patterns
- Custom content and positioning

#### Selection
📄 **Read:** [references/selection.md](references/selection.md)
- EnableSegmentSelection and EnableSeriesSelection
- Selection modes (Single, Multiple)
- SelectedIndex property
- SelectionBehavior configuration
- Visual feedback customization
- Selection events

#### Zooming and Panning
📄 **Read:** [references/zooming-panning.md](references/zooming-panning.md)
- EnableZooming property
- ZoomMode (X, Y, XY)
- EnablePanning for data exploration
- Touch gestures (pinch-to-zoom)
- Mouse wheel zooming
- Programmatic zoom (ZoomPosition, ZoomFactor)
- Reset zoom functionality
- Zoom toolbar

### Customization

#### Data Labels
📄 **Read:** [references/data-labels.md](references/data-labels.md)
- ShowDataLabels property
- DataLabelSettings configuration
- Label positioning (Inner, Outer, Auto)
- Label templates and formatting
- Style customization (fonts, colors)
- Rotation and alignment

#### Legend
📄 **Read:** [references/legend.md](references/legend.md)
- Enabling ChartLegend
- Positioning and placement options
- Legend template customization
- Icon types and styles
- Item clicking and toggling series visibility
- Label customization

#### Multiple Series Visualization
📄 **Read:** [references/multiple-series.md](references/multiple-series.md)
- Adding multiple series to Series collection
- Comparing different datasets
- Series visibility toggling
- Color palettes for visual distinction
- Legend coordination
- Performance considerations
- Mixed series types in one chart

#### Appearance Customization
📄 **Read:** [references/appearance-customization.md](references/appearance-customization.md)
- Chart Header and Title configuration
- ChartArea background and borders
- PaletteBrushes for series colors
- Series-level styling (Fill, Stroke, StrokeThickness)
- PlotArea customization
- Grid line styling
- Theme integration
- Responsive design patterns

## Quick Start Example

Here's a minimal example to create a basic cartesian chart with column series:

```xaml
<Window
    xmlns:chart="using:Syncfusion.UI.Xaml.Charts">
    
    <chart:SfCartesianChart Header="Sales Comparison">
        
        <!-- Define X-Axis (Category) -->
        <chart:SfCartesianChart.XAxes>
            <chart:CategoryAxis Header="Products"/>
        </chart:SfCartesianChart.XAxes>
        
        <!-- Define Y-Axis (Numerical) -->
        <chart:SfCartesianChart.YAxes>
            <chart:NumericalAxis Header="Sales ($)"/>
        </chart:SfCartesianChart.YAxes>
        
        <!-- Add Column Series -->
        <chart:ColumnSeries ItemsSource="{Binding SalesData}"
                           XBindingPath="Product" 
                           YBindingPath="Amount"
                           Label="Q1 Sales"
                           ShowDataLabels="True"/>
        
    </chart:SfCartesianChart>
    
</Window>
```

```csharp
using Syncfusion.UI.Xaml.Charts;

// Data Model
public class SalesData
{
    public string Product { get; set; }
    public double Amount { get; set; }
}

// ViewModel
public class ViewModel
{
    public List<SalesData> SalesData { get; set; }
    
    public ViewModel()
    {
        SalesData = new List<SalesData>
        {
            new SalesData { Product = "Product A", Amount = 25000 },
            new SalesData { Product = "Product B", Amount = 38000 },
            new SalesData { Product = "Product C", Amount = 17000 },
            new SalesData { Product = "Product D", Amount = 42000 }
        };
    }
}

// Code-behind
SfCartesianChart chart = new SfCartesianChart();
chart.Header = "Sales Comparison";

// Configure axes
CategoryAxis xAxis = new CategoryAxis { Header = "Products" };
chart.XAxes.Add(xAxis);

NumericalAxis yAxis = new NumericalAxis { Header = "Sales ($)" };
chart.YAxes.Add(yAxis);

// Add series
ColumnSeries series = new ColumnSeries
{
    ItemsSource = new ViewModel().SalesData,
    XBindingPath = "Product",
    YBindingPath = "Amount",
    Label = "Q1 Sales",
    ShowDataLabels = true
};
chart.Series.Add(series);
```

## Common Patterns

### Pattern 1: Multi-Series Comparison

Compare multiple datasets in the same chart:

```xaml
<chart:SfCartesianChart Header="Quarterly Sales Comparison">
    
    <chart:SfCartesianChart.Legend>
        <chart:ChartLegend/>
    </chart:SfCartesianChart.Legend>
    
    <chart:SfCartesianChart.XAxes>
        <chart:CategoryAxis/>
    </chart:SfCartesianChart.XAxes>
    
    <chart:SfCartesianChart.YAxes>
        <chart:NumericalAxis/>
    </chart:SfCartesianChart.YAxes>
    
    <!-- Multiple series -->
    <chart:ColumnSeries Label="Q1" 
                       ItemsSource="{Binding Q1Data}"
                       XBindingPath="Month" 
                       YBindingPath="Sales"/>
    
    <chart:ColumnSeries Label="Q2" 
                       ItemsSource="{Binding Q2Data}"
                       XBindingPath="Month" 
                       YBindingPath="Sales"/>
    
</chart:SfCartesianChart>
```

### Pattern 2: Time-Series Line Chart with Zooming

Display time-based data with interactive zooming:

```xaml
<chart:SfCartesianChart>
    
    <chart:SfCartesianChart.XAxes>
        <chart:DateTimeAxis>
            <chart:DateTimeAxis.LabelStyle>
                <chart:LabelStyle LabelFormat="MMM-dd"/>
            </chart:DateTimeAxis.LabelStyle>
        </chart:DateTimeAxis>
    </chart:SfCartesianChart.XAxes>
    
    <chart:SfCartesianChart.YAxes>
        <chart:NumericalAxis/>
    </chart:SfCartesianChart.YAxes>
    
    <chart:LineSeries ItemsSource="{Binding TimeSeriesData}"
                     XBindingPath="Date" 
                     YBindingPath="Value"
                     EnableTooltip="True"/>
    
    <!-- Enable zooming and panning -->
    <chart:SfCartesianChart.ZoomPanBehavior>
        <chart:ChartZoomPanBehavior EnableZooming="True" 
                                   EnablePanning="True"
                                   ZoomMode="XY"/>
    </chart:SfCartesianChart.ZoomPanBehavior>
    
</chart:SfCartesianChart>
```

### Pattern 3: Stacked Chart for Part-to-Whole Analysis

Show contribution of parts to a total:

```xaml
<chart:SfCartesianChart Header="Market Share by Region">
    
    <chart:SfCartesianChart.XAxes>
        <chart:CategoryAxis/>
    </chart:SfCartesianChart.XAxes>
    
    <chart:SfCartesianChart.YAxes>
        <chart:NumericalAxis/>
    </chart:SfCartesianChart.YAxes>
    
    <!-- Stacked Column Series -->
    <chart:StackedColumnSeries Label="Region A" 
                              ItemsSource="{Binding Data}"
                              XBindingPath="Year" 
                              YBindingPath="RegionA"/>
    
    <chart:StackedColumnSeries Label="Region B" 
                              ItemsSource="{Binding Data}"
                              XBindingPath="Year" 
                              YBindingPath="RegionB"/>
    
    <chart:StackedColumnSeries Label="Region C" 
                              ItemsSource="{Binding Data}"
                              XBindingPath="Year" 
                              YBindingPath="RegionC"/>
    
</chart:SfCartesianChart>
```

### Pattern 4: High-Performance Chart for Large Datasets

Use fast series for millions of data points:

```csharp
SfCartesianChart chart = new SfCartesianChart();

DateTimeAxis xAxis = new DateTimeAxis();
chart.XAxes.Add(xAxis);

NumericalAxis yAxis = new NumericalAxis();
chart.YAxes.Add(yAxis);

// Use FastLineBitmapSeries for performance
FastLineBitmapSeries series = new FastLineBitmapSeries
{
    ItemsSource = GenerateLargeDataset(1000000), // 1 million points
    XBindingPath = "Time",
    YBindingPath = "Value",
    EnableAntiAliasing = true // Smooth rendering
};

chart.Series.Add(series);
```

### Pattern 5: Financial Chart with Multiple Axes

Display OHLC data with volume on separate axis:

```xaml
<chart:SfCartesianChart>
    
    <chart:SfCartesianChart.XAxes>
        <chart:DateTimeAxis/>
    </chart:SfCartesianChart.XAxes>
    
    <chart:SfCartesianChart.YAxes>
        <chart:NumericalAxis Header="Price"/>
        <chart:NumericalAxis Name="VolumeAxis" 
                           Header="Volume"
                           OpposedPosition="True"/>
    </chart:SfCartesianChart.YAxes>
    
    <!-- OHLC Series on primary axis -->
    <chart:CandleSeries ItemsSource="{Binding StockData}"
                       XBindingPath="Date"
                       Open="Open"
                       High="High"
                       Low="Low"
                       Close="Close"/>
    
    <!-- Volume on secondary axis -->
    <chart:ColumnSeries ItemsSource="{Binding StockData}"
                       XBindingPath="Date"
                       YBindingPath="Volume"
                       YAxisName="VolumeAxis"/>
    
</chart:SfCartesianChart>
```

## Key Properties Overview

### SfCartesianChart
- **Header** - Chart title
- **XAxes** - Collection of horizontal axes
- **YAxes** - Collection of vertical axes
- **Series** - Collection of chart series
- **Legend** - Legend configuration
- **ZoomPanBehavior** - Zooming and panning behavior
- **PaletteBrushes** - Color palette for series

### ChartSeries (Base)
- **ItemsSource** - Data source
- **XBindingPath** - Property path for X values
- **YBindingPath** - Property path for Y values
- **Label** - Series label for legend
- **ShowDataLabels** - Enable data labels
- **EnableTooltip** - Enable tooltips
- **EnableAnimation** - Enable series animation
- **XAxisName** - Name of X-axis to use
- **YAxisName** - Name of Y-axis to use

### Axis (Base)
- **Header** - Axis title
- **Interval** - Interval between labels
- **Minimum** - Minimum axis value
- **Maximum** - Maximum axis value
- **LabelRotation** - Label rotation angle
- **LabelStyle** - Label formatting and styling
- **ShowMajorGridLines** - Show/hide grid lines
- **IsInversed** - Invert axis direction
- **OpposedPosition** - Position axis on opposite side

## Performance Considerations

### When to Use Fast Series
- **Dataset size > 10,000 points**: Consider FastLineSeries or FastLineBitmapSeries
- **Dataset size > 100,000 points**: Use FastLineBitmapSeries, FastColumnBitmapSeries, or FastScatterBitmapSeries
- **Real-time updates**: Fast series provide better performance for streaming data
- **Trade-offs**: Fast series have limited interactivity (no segment selection, limited tooltip customization)

### Optimization Tips
- Use **CategoryAxis** for categorical data instead of formatting NumericalAxis
- Enable **EnableAntiAliasing** for FastBitmap series to improve visual quality
- Limit **ShowDataLabels** usage for large datasets
- Use **data virtualization** in ViewModel for very large datasets
- Consider **sampling or aggregation** for datasets over 1 million points
- Disable **animations** for better initial render performance

## Common Use Cases

1. **Business Dashboards** - Multi-series column/line charts with legends and tooltips
2. **Financial Analysis** - Candlestick/OHLC charts with volume overlay on multiple axes
3. **Scientific Data** - Scatter plots for correlation, line charts for trends
4. **Time-Series Monitoring** - Real-time line charts with zooming/panning
5. **Comparative Analysis** - Stacked charts for part-to-whole relationships
6. **IoT/Telemetry** - Fast series for high-frequency sensor data (millions of points)
7. **Sales Reports** - Bar/column charts with data labels
8. **Market Research** - Bubble charts for three-dimensional data analysis

## Troubleshooting Tips

- **Series not visible**: Verify XAxes and YAxes are defined before adding series
- **Data not binding**: Check XBindingPath and YBindingPath match data model property names
- **Performance issues**: Switch to fast series for datasets over 10,000 points
- **Axis labels overlapping**: Use LabelRotation or increase chart width
- **Multiple axes not working**: Ensure XAxisName/YAxisName matches the Name property of the axis
- **Zooming not working**: Add ChartZoomPanBehavior to chart and set EnableZooming=True

## Related Skills

When working with Syncfusion WinUI components, you may also need:
- **Circular Charts** - For pie, doughnut, and radial charts
- **Polar Charts** - For polar and radar visualizations
- **3D Charts** - For three-dimensional data representation
- **Funnel/Pyramid Charts** - For hierarchical data visualization

---

**Installation**: Install the `Syncfusion.Chart.WinUI` NuGet package to get started.

**Namespace**: `using Syncfusion.UI.Xaml.Charts;`

**Documentation**: Refer to the reference files in this skill for detailed implementation guidance.
