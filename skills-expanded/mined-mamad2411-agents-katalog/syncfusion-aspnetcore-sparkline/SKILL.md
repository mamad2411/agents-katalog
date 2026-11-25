---
name: syncfusion-aspnetcore-sparkline
description: When user needs to create sparklines (compact data visualizations) in ASP.NET Core applications, always use this skill to implement sparkline components, configure chart types (line, column, area, win-loss, pie), bind data, customize appearance, add markers and data labels, enable user interactions (tooltips, track lines), and ensure accessibility compliance immediately.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization - Charts"
---

# Implementing Syncfusion Sparkline

## When to Use This Skill

Use this skill when you need to:

- **Create compact data visualizations** - Sparklines are very small charts that visualize data in a condensed format without axes or coordinates
- **Integrate with ASP.NET Core applications** - Setting up Syncfusion Sparkline control in Razor pages or MVC applications
- **Display temporal data trends** - Showing data patterns over time in minimal space (perfect for dashboards and grids)
- **Highlight specific data points** - Using markers to show high, low, start, end, or negative values
- **Support interactive data exploration** - Adding tooltips and track lines for user interactivity
- **Meet accessibility requirements** - Ensuring WCAG 2.2 compliance and keyboard navigation support

## Component Overview

The Syncfusion Sparkline is a lightweight chart component that presents common data shapes in a highly condensed format. Key characteristics:

- **Consumes minimal space** - Perfect for dashboards and grid integrations
- **Five chart types** - Line, Column, Area, Win-Loss, and Pie
- **Visual enhancements** - Markers, data labels, range bands
- **Interactive features** - Tooltips and track lines
- **Customizable appearance** - Themes, colors, borders, padding
- **Accessibility ready** - WCAG 2.2 AA compliant with keyboard shortcuts

## Documentation and Navigation Guide

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Complete Sparkline class API documentation (40+ properties)
- SparklineAxisSettings, ContainerArea, Padding, Border configuration
- MarkerSettings for point highlighting (All, Start, End, High, Low, Negative)
- DataLabelSettings for label configuration and positioning
- TooltipSettings for interactive tooltips with custom templates
- RangeBandSettings for highlighting value ranges
- TrackLineSettings for mouse tracking lines
- Five SparklineType options (Line, Column, Area, Win-Loss, Pie)
- SparklineValueType options (Numeric, Category, DateTime)
- Theme support (Material, Fabric, Bootstrap, HighContrast)
- RangePadding options (None, Normal, Additional, Round)
- Comprehensive events reference (Load, Loaded, AxisRendering, SeriesRendering, etc.)
- User interaction events (SparklineMouseClick, PointRegionMouseMove, etc.)
- Data rendering events (PointRendering, MarkerRendering, DataLabelRendering, TooltipInitialize)
- Usage patterns for all sparkline types with code examples
- Official Syncfusion API reference links

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- ASP.NET Core project setup requirements
- NuGet package installation (Syncfusion.EJ2.AspNet.Core)
- TagHelper configuration and script manager registration
- Creating your first sparkline
- Data source binding and initialization
- Changing sparkline types
- Enabling tooltips

### Sparkline Types & Configuration
📄 **Read:** [references/sparkline-types.md](references/sparkline-types.md)
- Five chart type options (Line, Column, Area, Win-Loss, Pie)
- When to use each type for different data scenarios
- Implementation patterns for each sparkline type
- Code examples for all type variations

### Data Features & Customization
📄 **Read:** [references/data-features.md](references/data-features.md)
- Data binding approaches and data source preparation
- Adding markers (All, Start, End, High, Low, Negative)
- Customizing marker appearance (fill, border, size, opacity)
- Data labels configuration and point selection
- Range bands for highlighting value ranges
- Data label customization (fill, border, text style)
- Formatting data label text

### Appearance & Theming
📄 **Read:** [references/appearance-theming.md](references/appearance-theming.md)
- Container area border and padding configuration
- Background color customization
- Theme selection (Material, Fabric, Bootstrap, Highcontrast)
- Text color and data label appearance by theme
- Size and spacing adjustments
- CSS customization approaches

### User Interaction & Tooltips
📄 **Read:** [references/user-interaction.md](references/user-interaction.md)
- Tooltip implementation and module injection
- Tooltip customization (fill, text style, format, border)
- Tooltip templates with custom HTML
- Track line configuration and behavior
- Mouse-based point tracking
- Tooltip formatting options

### Accessibility & Deployment
📄 **Read:** [references/accessibility-deployment.md](references/accessibility-deployment.md)
- WCAG 2.2 AA compliance and standards adherence
- Section 508 support and screen reader compatibility
- Keyboard navigation shortcuts (Ctrl+P for printing)
- WAI-ARIA attributes and patterns
- Right-to-left (RTL) language support
- Color contrast and mobile device considerations
- Accessibility validation tools and checklist

## Quick Start Example

Here's a minimal sparkline implementation:

```csharp
// Controller: Index.cs
public class DataSource
{
    public int x { get; set; }
    public string xval { get; set; }
    public double yval { get; set; }
    
    public static List<DataSource> GetData()
    {
        List<DataSource> data = new List<DataSource>();
        data.Add(new DataSource() { x = 0, xval = "2020", yval = 2000 });
        data.Add(new DataSource() { x = 1, xval = "2021", yval = 3000 });
        data.Add(new DataSource() { x = 2, xval = "2022", yval = 2500 });
        data.Add(new DataSource() { x = 3, xval = "2023", yval = 4000 });
        return data;
    }
}
```

```cshtml
<!-- View: Index.cshtml -->
<ejs-sparkline id="sparkline" 
    type="Line" 
    dataSource="ViewBag.DataPoints">
    <e-sparkline-tooltipsettings visible="true"></e-sparkline-tooltipsettings>
</ejs-sparkline>
```

## Common Patterns

### Pattern 1: Dashboard Summary Sparklines
Use compact Line sparklines in dashboard summary cards to show key metric trends at a glance.

### Pattern 2: Grid Integration
Embed sparklines within grid columns to visualize data distribution across rows without excessive space consumption.

### Pattern 3: Status Indicators with Win-Loss
Use Win-Loss sparklines to show success/failure patterns or positive/negative outcomes in historical data.

### Pattern 4: Financial Charts
Use Column sparklines for revenue/expense comparisons, and Area sparklines for cumulative financial trends.

### Pattern 5: Data Point Highlighting
Combine markers and range bands to emphasize exceptional values (high/low points) and target ranges.

## Key Properties

| Property | Purpose | Example |
|----------|---------|---------|
| `type` | Sets sparkline chart type | `type="Line"` |
| `dataSource` | Binds data to sparkline | `dataSource="@ViewBag.Data"` |
| `xName` | X-axis data field | `xName="xval"` |
| `yName` | Y-axis data field | `yName="yval"` |
| `theme` | Sets color theme | `theme="Material"` |
| `markerSettings.visible` | Shows markers at points | `visible="All"` |
| `dataLabelSettings.visible` | Displays data labels | `visible="All"` |
| `tooltipSettings.visible` | Enables tooltips | `visible="true"` |
| `trackLineSettings.visible` | Shows track line on hover | `visible="true"` |

## Common Use Cases

1. **Financial Dashboards**: Show revenue trends using Area sparklines in summary widgets
2. **KPI Monitoring**: Display performance metrics with Line sparklines and highlighted range bands
3. **Data Tables**: Add sparklines to grid columns showing sales history or performance over time
4. **Status Reports**: Use Win-Loss sparklines to visualize project outcomes or test results
5. **Mobile Dashboards**: Utilize compact Pie sparklines for portfolio allocation or category distribution
