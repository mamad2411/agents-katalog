---
name: syncfusion-aspnetcore-circular-chart-3d
description: Create interactive 3D Circular Charts with Syncfusion ASP.NET Core. Implement pie/donut series, data labels, legends, tooltips, custom styling, titles, empty point handling, and print/export functionality. Use this skill when the user needs to build or configure pie charts, donut charts, circular data visualizations, or charts showing proportional data in ASP.NET Core applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion ASP.NET Core 3D Circular Chart

Syncfusion's 3D Circular Chart provides a powerful component for visualizing proportional data using 3D Circular Chart formats. This skill guides you through implementing, configuring, and customizing pie/donut charts in ASP.NET Core applications, from basic setup to advanced interactive features.

## When to Use This Skill

Use this skill when you need to:
- Create a pie or donut chart to display proportional data
- Configure and format data labels, legends, and tooltips
- Customize chart appearance with titles, colors, and styling
- Handle empty or missing data points
- Enable interactive features like print and export
- Implement user interactions with pie chart slices
- Configure chart behavior in ASP.NET Core applications

## Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and NuGet package setup
- Adding tag helpers and script references
- Creating your first pie chart
- Basic ASP.NET Core configuration
- Project structure setup

### Pie and Donut Variations
📄 **Read:** [references/pie-donut-variations.md](references/pie-donut-variations.md)
- Rendering pie series vs donut series
- Radius customization and configuration
- Inner radius for donut effect
- Multiple series rendering
- Color mapping and styling

### Data Labels
📄 **Read:** [references/data-labels.md](references/data-labels.md)
- Enabling and positioning data labels
- Label templates and custom formatting
- Connector lines and styling
- Text mapping from data source
- Percentage and value formatting
- Label customization with events

### Legend and Tooltips
📄 **Read:** [references/legend-tooltips.md](references/legend-tooltips.md)
- Legend configuration and positioning
- Legend alignment, sizing, and shapes
- Legend paging and navigation
- Tooltip enabling and formatting
- Custom tooltip templates
- Interactive tooltip behavior
- Styling and appearance

### Titles, Subtitles, and Empty Points
📄 **Read:** [references/titles-empty-points.md](references/titles-empty-points.md)
- Adding titles and subtitles
- Title customization and styling
- Handling empty/null data points
- Empty point modes (Gap, Average, Drop, Zero)
- Customizing empty point appearance
- Subtitle styling and positioning

### Print and Export
📄 **Read:** [references/print-export.md](references/print-export.md)
- Printing pie/donut charts
- Enabling export with `enableExport="true"`
- Exporting to image formats (JPEG, PNG, SVG)
- PDF export functionality
- Export configuration options
- Button integration for user interactions

## Quick Start

Here's a minimal working example to get started with a pie chart:

```cshtml
// CSHTML View
<ejs-circularchart3d id="chartContainer" title="Sales Distribution" tilt="-45">
    <e-circularchart3d-legendsettings visible="true" position="@Syncfusion.EJ2.Charts.LegendPosition.Right">
    </e-circularchart3d-legendsettings>
    <e-circularchart3d-series-collection>
        <e-circularchart3d-series dataSource="@chartData" xName="Category" yName="Value">
            <e-circularchart3d-series-datalabel visible="true" position="@Syncfusion.EJ2.Charts.CircularChart3DLabelPosition.Outside">
                <e-connectorstyle length="40px"></e-connectorstyle>
            </e-circularchart3d-series-datalabel>
        </e-circularchart3d-series>
    </e-circularchart3d-series-collection>
</ejs-circularchart3d>
```
```csharp
// Code-behind
public class ChartData
{
    public string Category { get; set; }
    public double Value { get; set; }
}

// Controller
List<ChartData> chartData = new()
{
    new ChartData { Category = "Product A", Value = 35 },
    new ChartData { Category = "Product B", Value = 28 },
    new ChartData { Category = "Product C", Value = 37 }
};
```

## Common Patterns

### Pattern 1: Pie Chart with Formatted Data Labels
```cshtml
<e-circularchart3d-series-datalabel visible="true" format="n1" position="@Syncfusion.EJ2.Charts.CircularChart3DLabelPosition.Outside">
    <e-font size="12px" fontWeight="600"></e-font>
    <e-connectorstyle length="50px" color="gray"></e-connectorstyle>
</e-circularchart3d-series-datalabel>
```

### Pattern 2: Donut Chart Configuration
```cshtml
<e-circularchart3d-series dataSource="@data" xName="X" yName="Y" innerRadius="50%">
</e-circularchart3d-series>
```

### Pattern 3: Legend with Customized Appearance
```cshtml
<e-circularchart3d-legendsettings visible="true" position="@Syncfusion.EJ2.Charts.LegendPosition.Bottom" 
    alignment="@Syncfusion.EJ2.Charts.Alignment.Center" width="100%">
</e-circularchart3d-legendsettings>
```

### Pattern 4: Tooltip with Custom Format
```cshtml
<e-circularchart3d-tooltipsettings enable="true" format="${point.x}: ${point.y}%"></e-circularchart3d-tooltipsettings>
```

## Key Configuration Properties

| Property | Purpose | Default |
|----------|---------|---------|
| `Type` | Series type (Pie for pie, Donut via InnerRadius) | Pie |
| `Radius` | Pie radius percentage | 80% |
| `InnerRadius` | Inner radius for donut effect (0-100%) | 0% |
| `DataLabel.Visible` | Show/hide data labels | false |
| `DataLabel.Position` | Label position (Inside/Outside) | Inside |
| `LegendSettings.Visible` | Show/hide legend | true |
| `Tooltip.Enable` | Enable tooltip on hover | false |
| `EmptyPointSettings.Mode` | Handle null values (Gap/Average/Drop/Zero) | Gap |

## Common Use Cases

1. **Market Share Visualization**: Display product or market segment distribution using pie/donut charts
2. **Budget Breakdown**: Show expense categories as pie slices with percentages
3. **Survey Results**: Visualize survey response distribution proportionally
4. **Status Distribution**: Display project status distribution (Completed, In Progress, Pending, etc.)
5. **Sales Performance**: Compare sales by region or product category
6. **Inventory Levels**: Show inventory distribution across warehouses or categories
7. **Dashboard Analytics**: Include pie/donut charts in business analytics dashboards

## Next Steps

- Read the **Getting Started** guide to set up your first chart
- Explore **Pie and Donut Variations** for different visual styles
- Configure **Data Labels** for better data representation
- Add **Legends and Tooltips** for interactive data exploration
- Handle **Titles and Empty Points** for completeness
- Enable **Print and Export** for report generation
