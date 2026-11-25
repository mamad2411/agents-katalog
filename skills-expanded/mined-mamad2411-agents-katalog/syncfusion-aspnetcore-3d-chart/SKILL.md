---
name: syncfusion-aspnetcore-3d-chart
description: Guide for implementing Syncfusion 3D Chart in ASP.NET Core. Always use this skill when user needs 3D chart functionality, data visualization, series configuration, axes setup, or interactive chart features like tooltips and selection. Covers setup, data binding, chart types, styling, and user interactions.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Charts"
---

# Implementing Syncfusion 3D Chart

The Syncfusion 3D Chart is a powerful data visualization component for ASP.NET Core applications. It provides comprehensive support for multiple chart types, data binding, axis configuration, and rich interactive features.

## When to Use This Skill

Use this skill when you need to:
- Render 3D charts in ASP.NET Core Razor applications
- Bind data from local, remote, or OData sources
- Configure multiple chart types (bar, column, stacked variants)
- Customize axes, legends, and data labels
- Add styling and appearance customization
- Implement user interactions (selection, tooltips)
- Export or print chart data
- Improve chart accessibility

## Component Overview

The Syncfusion 3D Chart (`<ejs-chart3d>`) is a tag helper component that:
- Renders interactive 3D visualizations with mouse and touch support
- Supports multiple series and data points with smart label positioning
- Provides configurable legends, data labels, and tooltips
- Enables selection of data points, series, or clusters
- Offers extensive styling through custom color palettes and CSS

**Key Capabilities:**
- Multiple chart types with stacking options
- Local, remote, and OData data binding
- Responsive design and RTL support
- Export to PNG/SVG format
- Print functionality
- WCAG accessibility compliance

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and NuGet package setup
- ASP.NET Core project configuration
- Tag helper registration
- Script and style references
- Basic chart rendering with minimal example
- Initial data binding setup

### Data Binding & Series Configuration
📄 **Read:** [references/data-binding-series.md](references/data-binding-series.md)
- Binding local JSON data to series
- Remote data binding with DataManager
- OData adaptor configuration
- Handling empty data points
- Mapping XName and YName properties
- Query filtering for remote data

### Chart Types & Series
📄 **Read:** [references/chart-types-series.md](references/chart-types-series.md)
- Bar chart type implementation
- Column chart type setup
- Stacked bar and stacked column charts
- Stacked 100% bar and column variants
- Series visibility and data mapping
- Type-specific configurations

### Axes & Scales Configuration
📄 **Read:** [references/axes-configuration.md](references/axes-configuration.md)
- Category axis setup and labels
- Numeric axis configuration and ranges
- Date-time axis binding and formatting
- Logarithmic axis for exponential data
- Multiple panes in single chart
- Axis customization and label positioning

### Data Labels & Legends
📄 **Read:** [references/data-labels-legends.md](references/data-labels-legends.md)
- Enabling and positioning data labels
- Data label templates and formatting
- Legend positioning (top, bottom, left, right)
- Custom legend positioning with coordinates
- Legend alignment and reverse options
- Label visibility and overlapping handling

### Styling & Appearance
📄 **Read:** [references/styling-appearance.md](references/styling-appearance.md)
- Custom color palettes for series
- Point-level color mapping from data
- Chart background and border customization
- Individual data point customization
- Border styling and chart dimensions
- Theme and color scheme configuration

### User Interactions & Events
📄 **Read:** [references/user-interactions.md](references/user-interactions.md)
- Selection modes: Point, Series, and Cluster
- Point selection highlighting and events
- Series selection behavior
- Tooltip enabling and configuration
- Fixed vs tracking tooltip positioning
- Tooltip format templates and styling
- Selection event handling

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Print functionality configuration
- Export to PNG/SVG formats
- Accessibility features and WCAG compliance
- Event handling (PointRender, TextRender, SelectionComplete)
- Performance optimization for large datasets
- Cross-browser compatibility

## Quick Start Example

Here's a minimal example to render a 3D column chart with data:

```html
<!-- ASP.NET Core Razor -->
<ejs-chart3d id="container" title="Product Sales" enableRotation="true" rotation="7" tilt="10" depth="100">
    <e-chart3d-primaryxaxis valueType="@Syncfusion.EJ2.Charts.ValueType.Category">
    </e-chart3d-primaryxaxis>
    <e-chart3d-series-collection>
        <e-chart3d-series dataSource="ViewBag.chartData" 
                          xName="month" 
                          yName="sales" 
                          type="@Syncfusion.EJ2.Charts.Chart3DSeriesType.Column">
        </e-chart3d-series>
    </e-chart3d-series-collection>
    <e-chart3d-legendsettings position="@Syncfusion.EJ2.Charts.LegendPosition.Bottom"></e-chart3d-legendsettings>
    <e-chart3d-tooltipsettings enable="true"></e-chart3d-tooltipsettings>
</ejs-chart3d>
```

```csharp
// Controller
public class HomeController : Controller
{
    public IActionResult Index()
    {
        List<ChartData> chartData = new List<ChartData>
        {
            new ChartData { month = "Jan", sales = 35 },
            new ChartData { month = "Feb", sales = 28 },
            new ChartData { month = "Mar", sales = 34 }
        };
        ViewBag.chartData = chartData;
        return View();
    }
}

public class ChartData
{
    public string month { get; set; }
    public double sales { get; set; }
}
```

## Common Patterns

### Pattern 1: Multi-Series Comparison
When visualizing multiple data series for comparison:
1. Define multiple `<e-chart3d-series>` elements with different data sources
2. Use contrasting colors via custom palettes
3. Enable legend for series identification
4. Use legend click events to toggle series visibility

### Pattern 2: Interactive Data Exploration
When enabling user interaction with data:
1. Set `SelectionMode="@Syncfusion.EJ2.Charts.Chart3DSelectionMode.Point"` for individual point selection
2. Enable tooltips with custom format templates
3. Handle `PointRender` event for dynamic styling
4. Implement selection event callbacks for updates

### Pattern 3: Real-time Data Updates
When displaying changing data:
1. Bind data to a dynamic data source
2. Update the data collection and call refresh
3. Consider using remote data binding for large datasets
4. Implement appropriate axes scaling for data ranges

### Pattern 4: Multi-Pane Displays
When comparing data across different scales:
1. Define multiple rows in chart with row span
2. Assign series to specific rows via index
3. Configure independent axes for each row
4. Use synchronized x-axis for alignment

## Key Properties Quick Reference

| Property | Purpose | Common Values |
|----------|---------|----------------|
| `type` | Chart type | Column, Bar, StackingColumn, StackingBar, StackingColumn100, StackingBar100 |
| `xName` | X-axis data field | Field name from data object |
| `yName` | Y-axis data field | Field name from data object |
| `dataSource` | Series data | List of objects or DataManager |
| `visible` | Series visibility | true, false |
| `cornerRadius` | Bar/column roundness | 0-10 (pixels) |
| `marker.visible` | Show data point markers | true, false |
| `dataLabel.visible` | Show data labels | true, false |
| `tooltip.enable` | Enable tooltips | true, false |
| `selectionMode` | Selection behavior | None, Point, Series, Cluster |
| `background` | Chart background color | Hex color or named color |
| `wallColor` | Back wall color in 3D | Hex color |

## Getting Help

For detailed examples and advanced usage, refer to the individual reference guides above. Each covers a specific feature area with complete code samples, edge cases, and troubleshooting.

---

**Next Steps:**
- Start with "Getting Started" to set up your first chart
- Choose relevant reference guides based on your feature needs
- Each reference file is self-contained with all necessary examples
