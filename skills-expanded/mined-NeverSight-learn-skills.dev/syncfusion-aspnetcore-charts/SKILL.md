---
name: syncfusion-aspnetcore-charts
description: Implements Syncfusion ASP.NET Core Chart (SfChart) for data visualization. Use this when building charts, visualizing time-series or categorical data, or creating dashboards. Covers series configuration (line, bar, pie), axes, tooltips, legends, and customization for ASP.NET Core applications.
metadata:
    author: "Syncfusion Inc"
    version: "33.1.44"
    category: "Data Visualization"
---

# Implementing Syncfusion ASP.NET Core Charts

The Syncfusion ASP.NET Core Chart component is a feature-rich data visualization control that supports 25+ interactive chart types. It provides extensive customization options, multiple axes, data binding capabilities, and interactive features like zooming, panning, crosshair, and tooltips.

## When to Use This Skill

Use this skill when you need to:
- Create any type of chart or graph in ASP.NET Core applications
- Visualize data with line, area, column, bar, or other chart types
- Display financial data with candlestick, OHLC, or technical indicators
- Implement interactive charts with zoom, pan, crosshair, or selection
- Create multi-series charts or combination charts
- Add data labels, markers, legends, or annotations to charts
- Configure axes (numeric, datetime, category, logarithmic)
- Export charts to PDF, SVG, or image formats
- Build dashboards with multiple chart components
- Implement accessible charts with WCAG compliance

## Component Overview

**Key Capabilities:**
- **25+ Chart Types:** Line, Area, Column, Bar, Scatter, Bubble, Candle, OHLC, and more
- **Data Binding:** JSON arrays, DataManager, OData services, dynamic updates
- **Multiple Axes:** Support for multiple X and Y axes with different scales
- **Interactivity:** Zooming, panning, crosshair, trackball, selection, tooltips
- **Customization:** Themes, colors, gradients, custom templates
- **Advanced Features:** Annotations, striplines, trendlines, technical indicators, error bars
- **Export:** PDF, SVG, PNG, JPEG, CSV formats
- **Accessibility:** WCAG 2.0 compliant, keyboard navigation, RTL support

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and NuGet package setup
- Adding Chart tag helper to ASP.NET Core project
- Script manager registration
- Creating your first chart
- Basic configuration and running the application

### Chart Types

📄 **Read:** [references/line-area-charts.md](references/line-area-charts.md)
- Line, Step Line, Spline charts
- Area, Step Area, Spline Area charts
- Stacked Area and 100% Stacked Area
- Range Area and Spline Range Area
- When to use each type and complete examples

📄 **Read:** [references/column-bar-charts.md](references/column-bar-charts.md)
- Column and Bar charts
- Stacked Column/Bar and 100% Stacked
- Range Column charts
- Vertical chart orientation
- Complete configuration examples

📄 **Read:** [references/financial-charts.md](references/financial-charts.md)
- Candlestick charts
- OHLC (Open-High-Low-Close) charts
- HiLo and HiLoOpenClose charts
- Technical indicators (SMA, EMA, RSI, MACD, etc.)
- Financial data binding patterns

📄 **Read:** [references/scatter-bubble-charts.md](references/scatter-bubble-charts.md)
- Scatter plots for correlation analysis
- Bubble charts with three dimensions
- Point customization and sizing
- Complete implementation examples

📄 **Read:** [references/specialized-charts.md](references/specialized-charts.md)
- Box and Whisker (statistical distribution)
- Histogram (frequency distribution)
- Pareto (cumulative analysis)
- Waterfall (sequential value changes)
- Polar and Radar charts
- Complete examples for each type

### Data Binding
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Binding to JSON object arrays
- DataManager integration
- OData web services
- Complex property binding
- Dynamic data updates
- Local vs remote data

### Axes Configuration
📄 **Read:** [references/axes-configuration.md](references/axes-configuration.md)
- Axis types: Numeric, DateTime, Category, Logarithmic
- Multiple axes configuration
- Axis crossing and positioning
- Inversed axis
- Axis title and styling
- Range and interval customization

📄 **Read:** [references/axis-labels.md](references/axis-labels.md)
- Smart label management (trim, wrap, rotate, hide)
- Multilevel labels for grouping
- Label formatting and templates
- Custom label placement
- Edge label handling
- Label rotation and alignment

### Series Configuration
📄 **Read:** [references/series-configuration.md](references/series-configuration.md)
- Adding multiple series
- Series types and properties
- Combination charts (mixing chart types)
- Empty points handling
- Series customization
- Performance optimization

### Visual Elements

📄 **Read:** [references/data-labels.md](references/data-labels.md)
- Enabling and positioning data labels
- Label templates and formatting
- Text mapping from data source
- Smart label arrangement
- Customization (font, color, border)
- Label connectors

📄 **Read:** [references/markers-and-legends.md](references/markers-and-legends.md)
- Data marker shapes and customization
- Marker visibility and sizing
- Legend positioning and layout
- Legend customization and templates
- Legend pagination
- Toggle series visibility

### Interactivity Features

📄 **Read:** [references/zooming-panning.md](references/zooming-panning.md)
- Zooming modes: Selection, Pinch, Mousewheel
- Panning support
- Zoom toolbar configuration
- Reset zoom functionality
- Programmatic zoom control

📄 **Read:** [references/crosshair-trackball.md](references/crosshair-trackball.md)
- Crosshair configuration and customization
- Trackball mode for multiple series
- Tooltip integration
- Line styles and labels
- Shared tooltips

📄 **Read:** [references/tooltips.md](references/tooltips.md)
- Enabling and customizing tooltips
- Tooltip templates
- Shared tooltips across series
- Format and styling
- Tooltip animations

📄 **Read:** [references/selection.md](references/selection.md)
- Point and series selection
- Selection modes and patterns
- Multiple selection
- Selection events
- Visual feedback customization

### Advanced Features

📄 **Read:** [references/annotations-striplines.md](references/annotations-striplines.md)
- Chart annotations (text, shapes, images)
- Annotation positioning and alignment
- Strip lines for highlighting regions
- Segment and recurrence patterns
- Customization and styling

📄 **Read:** [references/trendlines-error-bars.md](references/trendlines-error-bars.md)
- Trendline types: Linear, Exponential, Logarithmic, Polynomial
- Forecasting with trendlines
- Error bars for uncertainty
- Error bar modes and types
- Customization options

📄 **Read:** [references/multiple-panes.md](references/multiple-panes.md)
- Creating multiple chart panes
- Pane configuration and sizing
- Associating series with panes
- Synchronized axes
- Layout customization

### Appearance and Theming

📄 **Read:** [references/appearance-customization.md](references/appearance-customization.md)
- Built-in themes (Material, Bootstrap, Fabric, etc.)
- Chart dimensions and sizing
- Background and border customization
- Gradient colors and fills
- Chart title and subtitle
- Print and export support

### Accessibility and Localization

📄 **Read:** [references/accessibility-localization.md](references/accessibility-localization.md)
- WCAG 2.0 compliance
- Keyboard navigation
- Screen reader support
- RTL (Right-to-Left) support
- Internationalization (i18n)
- Localization of chart elements

## Quick Start Example

Here's a minimal example to create a basic line chart:

```cshtml
@* Add to your .cshtml page *@
<ejs-chart id="container" title="Sales Analysis">
    <e-chart-primaryxaxis valueType="@Syncfusion.EJ2.Charts.ValueType.Category"></e-chart-primaryxaxis>
    <e-series-collection>
        <e-series dataSource="@ViewBag.ChartData" xName="Month" yName="Sales" 
                  type="@Syncfusion.EJ2.Charts.ChartSeriesType.Line">
        </e-series>
    </e-series-collection>
</ejs-chart>
```

```csharp
// In your controller
public IActionResult Index()
{
    ViewBag.ChartData = new object[]
    {
        new { Month = "Jan", Sales = 35 },
        new { Month = "Feb", Sales = 28 },
        new { Month = "Mar", Sales = 34 },
        new { Month = "Apr", Sales = 32 },
        new { Month = "May", Sales = 40 }
    };
    return View();
}
```

## Common Patterns

### Multiple Series Chart

```cshtml
<ejs-chart id="container" title="Product Comparison">
    <e-chart-primaryxaxis valueType="@Syncfusion.EJ2.Charts.ValueType.Category"></e-chart-primaryxaxis>
    <e-series-collection>
        <e-series dataSource="@ViewBag.ProductA" xName="Month" yName="Sales" 
                  name="Product A" type="@Syncfusion.EJ2.Charts.ChartSeriesType.Column">
        </e-series>
        <e-series dataSource="@ViewBag.ProductB" xName="Month" yName="Sales" 
                  name="Product B" type="@Syncfusion.EJ2.Charts.ChartSeriesType.Column">
        </e-series>
    </e-series-collection>
    <e-chart-legendsettings visible="true"></e-chart-legendsettings>
</ejs-chart>
```

### Chart with Data Labels and Markers

```cshtml
<ejs-chart id="container">
    <e-chart-primaryxaxis valueType="@Syncfusion.EJ2.Charts.ValueType.Category"></e-chart-primaryxaxis>
    <e-series-collection>
        <e-series dataSource="@ViewBag.Data" xName="X" yName="Y" 
                  type="@Syncfusion.EJ2.Charts.ChartSeriesType.Line">
            <e-series-marker visible="true" height="10" width="10">
            </e-series-marker>
            <e-series-datalabel visible="true" position="Top">
            </e-series-datalabel>
        </e-series>
    </e-series-collection>
</ejs-chart>
```

### Combination Chart

```cshtml
<ejs-chart id="container" title="Weather Analysis">
    <e-chart-primaryxaxis valueType="@Syncfusion.EJ2.Charts.ValueType.Category"></e-chart-primaryxaxis>
    <e-series-collection>
        <e-series dataSource="@ViewBag.Data" xName="Month" yName="Temperature" 
                  name="Temperature" type="@Syncfusion.EJ2.Charts.ChartSeriesType.Line">
        </e-series>
        <e-series dataSource="@ViewBag.Data" xName="Month" yName="Rainfall" 
                  name="Rainfall" type="@Syncfusion.EJ2.Charts.ChartSeriesType.Column">
        </e-series>
    </e-series-collection>
</ejs-chart>
```

### Chart with Zooming and Crosshair

```cshtml
<ejs-chart id="container">
    <e-chart-primaryxaxis valueType="@Syncfusion.EJ2.Charts.ValueType.DateTime" ></e-chart-primaryxaxis>
    <e-chart-zoomsettings enableSelectionZooming="true" enablePinchZooming="true">
    </e-chart-zoomsettings>
    <e-chart-crosshairsettings enable="true">
    </e-chart-crosshairsettings>
    <e-series-collection>
        <e-series dataSource="@ViewBag.Data" xName="Date" yName="Value" 
                  type="@Syncfusion.EJ2.Charts.ChartSeriesType.Area">
        </e-series>
    </e-series-collection>
</ejs-chart>
```

## Key Configuration Options

### Chart-Level Properties
- `title`: Chart title text
- `width`/`height`: Chart dimensions
- `theme`: Visual theme (Material, Bootstrap, Fabric, etc.)
- `background`: Background color
- `palettes`: Custom color palette for series

### Primary Axis (`e-chart-primaryxaxis`)
- `valueType`: Category, Numeric, DateTime, Logarithmic
- `title`: Axis title
- `minimum`/`maximum`: Axis range
- `interval`: Label interval
- `labelFormat`: Format string for labels

### Series Properties (`e-series`)
- `type`: Chart type (Line, Column, Bar, Area, etc.)
- `dataSource`: Data to visualize
- `xName`/`yName`: Property names for X and Y values
- `name`: Series name for legend
- `fill`: Custom color
- `width`: Line/border width

### Interactive Features
- `e-chart-zoomsettings`: Enable zooming capabilities
- `e-chart-crosshairsettings`: Configure crosshair
- `e-chart-tooltipsettings`: Tooltip customization
- `e-chart-legendsettings`: Legend configuration

### Visual Elements
- `e-series-marker`: Data point markers
- `e-series-datalabel`: Labels on data points
- `e-chart-annotations`: Custom annotations
- `e-striplines`: Highlight regions

## Common Use Cases

### 1. Sales Dashboard
Use Column or Bar charts with multiple series to compare sales across products, regions, or time periods. Add data labels for exact values and legends for clarity.

### 2. Financial Analysis
Use Candlestick or OHLC charts for stock price visualization. Add technical indicators (SMA, EMA, RSI) and enable zooming for detailed analysis.

### 3. Trend Analysis
Use Line or Spline charts with trendlines to show data trends over time. Add forecasting to predict future values.

### 4. Statistical Distribution
Use Box and Whisker charts for statistical analysis, Histogram for frequency distribution, or Scatter plots for correlation analysis.

### 5. Performance Monitoring
Use Area charts with multiple series and real-time data updates. Add annotations and striplines to mark significant events or thresholds.

### 6. Comparison Analysis
Use Stacked Column/Bar or 100% Stacked charts to show part-to-whole relationships. Use Pareto charts for cumulative analysis.

## Troubleshooting Tips

**Chart not rendering:**
- Verify `Syncfusion.EJ2.AspNet.Core` NuGet package is installed
- Ensure `@addTagHelper *, Syncfusion.EJ2` is in `_ViewImports.cshtml`
- Check that `<ejs-scripts>` is added at the end of `<body>` in layout
- Confirm script reference is included in `<head>`

**Data not displaying:**
- Verify `dataSource` is properly bound
- Check `xName` and `yName` match property names (case-sensitive)
- Ensure data is not null or empty
- Verify axis `valueType` matches data type

**Performance issues with large data:**
- Use `enableDataVirtualization` for large datasets
- Reduce marker size or disable markers
- Use lighter chart types (Line instead of Spline)
- Consider data aggregation or sampling

**Styling not applied:**
- Verify theme is correctly set
- Check CSS import order
- Use browser developer tools to inspect elements
- Ensure custom styles have proper specificity

## Related Components

- **3D Chart:** For three-dimensional visualization
- **Stock Chart:** Specialized for financial data with navigator
- **Range Navigator:** Timeline control for date-based filtering
- **Sparkline:** Compact inline charts
- **Bullet Chart:** For KPI visualization
- **Smith Chart:** For electrical impedance visualization

## API Reference

For a comprehensive reference of all Chart API properties, methods, and events, see:

📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Complete list of all properties (configuration, data binding, display, interactivity, accessibility)
- All event properties and their purposes
- Series and axis configuration options
- Common property combinations and usage patterns
- Link to official Syncfusion documentation

## Additional Resources

- **Official API Documentation:** [Chart API Reference](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Charts.Chart.html)
- **Live Demos:** [ASP.NET Core Chart Demos](https://ej2.syncfusion.com/aspnetcore/Chart/Overview)
- **GitHub Samples:** [ASP.NET Core Examples](https://github.com/SyncfusionExamples/ASP-NET-Core-Getting-Started-Examples)
