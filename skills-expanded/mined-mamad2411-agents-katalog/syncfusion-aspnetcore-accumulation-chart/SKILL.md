---
name: syncfusion-aspnetcore-accumulation-chart
description: Implement Syncfusion ASP.NET Core Accumulation Charts for proportional data visualization. Use this when creating pie charts, doughnut charts, pyramid charts, or funnel charts in ASP.NET Core applications. This skill covers chart setup, data binding, legends, tooltips, data labels, grouping, and accessibility features. Suitable for visualizing market share, sales distribution, survey results, and other percentage-based data representations.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing Syncfusion ASP.NET Core Accumulation Charts

A comprehensive skill for implementing Syncfusion's ASP.NET Core Accumulation Chart component. This component renders circular data visualizations including Pie, Doughnut, Pyramid, and Funnel charts using Scalable Vector Graphics (SVG).

## When to Use This Skill

Use this skill when you need to:
- Create pie, doughnut, pyramid, or funnel charts in ASP.NET Core applications
- Visualize proportional data or percentage distributions
- Display hierarchical data with pyramid/funnel charts
- Add data labels, tooltips, and legends to accumulation charts
- Implement interactive features (exploding slices, selection, drill-down)
- Handle grouped data or empty points in charts
- Export or print accumulation charts
- Make charts accessible (WCAG 2.2 compliant)
- Dynamically update chart data in real-time
- Customize chart appearance with themes, colors, and gradients

## Component Overview

**AccumulationChart** is a circular graphics component that divides data into segments to illustrate numerical proportions. It supports:

- **Chart Types:** Pie (including Doughnut variant), Pyramid, Funnel
  - **Note:** Doughnut is achieved by setting `innerRadius` on a Pie chart, not a separate type
- **Smart Labels:** Automatic label positioning to prevent overlapping
- **Grouping:** Combine small data points based on value or count
- **Semi-Charts:** Customize start and end angles for semi-pie/doughnut
- **Legend:** Display additional point information
- **Tooltips:** Interactive data point details
- **Empty Points:** Graceful handling of missing data
- **Accessibility:** Full WCAG 2.2 Level A & AA compliance
- **Export:** PNG, JPEG, SVG, PDF formats
- **Print:** Direct browser printing support

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)

**When to read:** Setting up accumulation charts for the first time, or need complete installation and basic implementation guidance.

**What you'll learn:**
- Prerequisites and system requirements
- Installing Syncfusion NuGet packages
- Registering tag helpers and script resources
- Creating your first pie/doughnut chart
- Basic data binding (dataSource, xName, yName)
- CSS theme imports and script manager setup
- Running and testing the chart
- Complete minimal working example

### Chart Types and Variants
📄 **Read:** [references/chart-types.md](references/chart-types.md)

**When to read:** Need to implement specific chart types (Pie, Doughnut, Pyramid, Funnel) or customize chart geometry and appearance.

**What you'll learn:**
- Pie chart implementation and configuration
- Doughnut chart with inner radius and center labels
- Pyramid chart with width, gap, and neck customization
- Funnel chart with neck dimensions
- Radius customization for all chart types
- Start and end angles for semi-pie/semi-doughnut
- Exploding slices (single and multiple points)
- Chart center positioning
- Complete code examples for each type

### Data Visualization Features
📄 **Read:** [references/data-visualization.md](references/data-visualization.md)

**When to read:** Enhancing charts with data labels, tooltips, legends, colors, or custom styling.

**What you'll learn:**
- Data label visibility, positioning, and templates
- Smart labels for overlap prevention
- Connector lines for outside labels
- Tooltip configuration and templates
- Legend positioning, alignment, and customization
- Title and subtitle configuration
- Point colors and gradient fills
- Text mapping from data source
- Border and margin customization
- Complete styling patterns

### Data Handling
📄 **Read:** [references/data-handling.md](references/data-handling.md)

**When to read:** Working with complex data scenarios like grouping small values, handling missing data, or updating charts dynamically.

**What you'll learn:**
- Grouping points by value or count threshold
- Group settings (threshold, mode, color, name)
- Empty points handling (null/undefined values)
- Empty point modes (Zero, Drop, Average, Gap)
- Dynamic data updates and live scenarios
- Data source binding patterns
- Sorting and ordering data
- Edge cases and troubleshooting

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)

**When to read:** Implementing annotations, export/print functionality, or migrating from EJ1 to EJ2.

**What you'll learn:**
- Chart annotations (text, shapes, images)
- Annotation positioning (coordinate, region, alignment)
- Export to image formats (PNG, JPEG, SVG)
- Export to PDF
- Print functionality and customization
- EJ1 to EJ2 API migration guide
- Performance optimization tips
- Complex implementation patterns

### Accessibility
📄 **Read:** [references/accessibility.md](references/accessibility.md)

**When to read:** Making charts accessible for users with disabilities or ensuring WCAG 2.2 compliance.

**What you'll learn:**
- WCAG 2.2 Level A & AA compliance features
- Keyboard navigation (Tab, arrow keys, Enter)
- ARIA attributes and roles
- Screen reader support and announcements
- High contrast theme support
- Focus indicators and visual feedback
- Color contrast requirements
- Accessible color palettes
- Testing with assistive technologies
- Complete accessible chart implementation

## Quick Start Example

Here's a minimal example to render a pie chart in ASP.NET Core:

### 1. Install Package

```bash
Install-Package Syncfusion.EJ2.AspNet.Core -Version <your_version_here>
```

### 2. Register Tag Helper (~/Pages/_ViewImports.cshtml)

```csharp
@addTagHelper *, Syncfusion.EJ2
```

### 3. Add Scripts (~/Pages/Shared/_Layout.cshtml)

```html
<head>
    <!-- Syncfusion JS -->
    <script src="<!-- Add the appropriate Syncfusion CDN script link here -->"></script>
</head>
<body>
    <!-- Content -->
    <ejs-scripts></ejs-scripts>
</body>
```

### 4. Create Pie Chart (~/Pages/Index.cshtml)

```cshtml
@{
    List<PieChartData> chartData = new List<PieChartData>
    {
        new PieChartData { xValue = "Chrome", yValue = 37 },
        new PieChartData { xValue = "Firefox", yValue = 22 },
        new PieChartData { xValue = "Safari", yValue = 19 },
        new PieChartData { xValue = "Edge", yValue = 12 },
        new PieChartData { xValue = "Others", yValue = 10 }
    };
}

<ejs-accumulationchart id="pieChart">
    <e-accumulation-series-collection>
        <e-accumulation-series dataSource="@chartData" xName="xValue" yName="yValue">
        </e-accumulation-series>
    </e-accumulation-series-collection>
</ejs-accumulationchart>
```

### 5. Define Data Model (~/Pages/Index.cshtml.cs or separate class)

```csharp
public class PieChartData
{
    public string xValue { get; set; }
    public double yValue { get; set; }
}
```

**Result:** A basic pie chart displaying browser usage statistics.

## Common Patterns

### Pattern 1: Doughnut Chart with Center Label

```cshtml
<ejs-accumulationchart id="container">
    <e-accumulation-series-collection>
        <e-accumulation-series dataSource="chartData" xName="x" yName="y" innerRadius="65%">
        </e-accumulation-series>
    </e-accumulation-series-collection>
    <e-accumulationchart-centerlabel text="Mobile<br>Browsers<br>Statistics">
    </e-accumulationchart-centerlabel>
    <e-accumulationchart-legendsettings visible="false">
    </e-accumulationchart-legendsettings>
</ejs-accumulationchart>
```

**Use Case:** Dashboard KPIs with center text showing total value.

### Pattern 2: Pie Chart with Smart Labels and Tooltips

```cshtml
<ejs-accumulationchart id="smartLabelChart" enableSmartLabels="true">
    <e-accumulation-series-collection>
        <e-accumulation-series dataSource="@chartData" xName="xValue" yName="yValue">
            <e-accumulationseries-datalabel visible="true" 
                                          position="Outside" 
                                          name="text">
                <e-connectorstyle type="Curve"></e-connectorstyle>
            </e-accumulationseries-datalabel>
        </e-accumulation-series>
    </e-accumulation-series-collection>
    <e-accumulationchart-tooltipsettings enable="true" format="${point.x}: ${point.y}%">
    </e-accumulationchart-tooltipsettings>
</ejs-accumulationchart>
```

**Use Case:** Preventing label overlap in charts with many small slices.

### Pattern 3: Grouped Data with Small Values

```cshtml
<ejs-accumulationchart id="groupedChart">
    <e-accumulation-series-collection>
        <e-accumulation-series dataSource="@chartData" 
                              xName="xValue" 
                              yName="yValue"
                              groupTo="11">
        </e-accumulation-series>
    </e-accumulation-series-collection>
</ejs-accumulationchart>
```

**Use Case:** Combining values below 11% into a single "Others" group.

### Pattern 4: Funnel Chart with Export

```cshtml
<button id="exportBtn">Export as PNG</button>

<ejs-accumulationchart id="funnelChart">
    <e-accumulation-series-collection>
        <e-accumulation-series dataSource="@chartData" 
                              xName="xValue" 
                              yName="yValue" 
                              type="Funnel"
                              neckWidth="15%"
                              neckHeight="18%">
        </e-accumulation-series>
    </e-accumulation-series-collection>
</ejs-accumulationchart>

<script>
    document.getElementById('exportBtn').onclick = function() {
        var chart = document.getElementById('funnelChart').ej2_instances[0];
        chart.export('PNG', 'funnel-chart');
    };
</script>
```

**Use Case:** Sales funnel visualization with image export.

## API Reference

### AccumulationChart Class

Represents the main accumulation chart component. All properties are defined in the `Syncfusion.EJ2.Charts` namespace.

#### Constructor

```csharp
public AccumulationChart()
```

#### Core Properties

| Property | Type | Default | Description | API Reference |
|----------|------|---------|-------------|---|
| `Accessibility` | `AccumulationAccessibility` | null | Options to improve accessibility for accumulation chart elements | [AccumulationAccessibility](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Charts.AccumulationAccessibility.html) |
| `Annotations` | `List<AccumulationAnnotationSettings>` | null | Annotations for highlighting specific data points | [AccumulationAnnotationSettings](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Charts.AccumulationAnnotationSettings.html) |
| `Background` | `string` | null | Background color (hex or rgba) | - |
| `BackgroundImage` | `string` | null | Background image URL | - |
| `Border` | `AccumulationChartBorder` | null | Chart border configuration | [AccumulationChartBorder](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Charts.AccumulationChartBorder.html) |
| `Center` | `AccumulationChartCenter` | null | Center position of pie/doughnut (x, y percentages) | [AccumulationChartCenter](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Charts.AccumulationChartCenter.html) |
| `CenterLabel` | `AccumulationChartCenterLabel` | null | Center label configuration for doughnut charts | [AccumulationChartCenterLabel](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Charts.AccumulationChartCenterLabel.html) |
| `DataSource` | `object` | null | Chart data collection | - |
| `EnableAnimation` | `bool` | true | Enable chart animation on load | - |
| `EnableBorderOnMouseMove` | `bool` | true | Enable border on mouse hover | - |
| `EnableExport` | `bool` | true | Enable export to JPEG, PNG, SVG, PDF, XLSX, CSV | - |
| `EnableHtmlSanitizer` | `bool` | false | Sanitize untrusted HTML in chart content | - |
| `EnablePersistence` | `bool` | false | Persist component state across page reloads | - |
| `EnableRtl` | `bool` | false | Enable right-to-left rendering | - |
| `EnableSmartLabels` | `bool` | true | Auto-arrange labels to prevent overlap | - |
| `FocusBorderColor` | `string` | - | Focus border color for accessibility | - |
| `FocusBorderMargin` | `double` | 0 | Focus border margin | - |
| `FocusBorderWidth` | `double` | 1.5 | Focus border width | - |
| `Height` | `string` | null | Chart height (e.g., "450px", "100%") | - |
| `HighlightColor` | `string` | "" | Color for highlighting data points on hover | - |
| `HighlightMode` | `AccumulationHighlightMode` | None | Highlight mode: None or Point | [AccumulationHighlightMode](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Charts.AccumulationHighlightMode.html) |
| `HighlightPattern` | `SelectionPattern` | None | Pattern for highlighting series/points | [SelectionPattern](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Charts.SelectionPattern.html) |
| `IsMultiSelect` | `bool` | false | Enable multiple point selection (requires selectionMode=Point) | - |
| `LegendSettings` | `AccumulationChartLegendSettings` | null | Legend configuration | [AccumulationChartLegendSettings](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Charts.AccumulationChartLegendSettings.html) |
| `Locale` | `string` | "" | Culture/localization override (default: en-US) | - |
| `Margin` | `AccumulationChartMargin` | null | Chart margins (left, right, top, bottom) | [AccumulationChartMargin](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Charts.AccumulationChartMargin.html) |
| `NoDataTemplate` | `object` | null | Template for empty chart state | - |
| `SelectedDataIndexes` | `object` | null | Initial selected point indexes | - |
| `SelectionMode` | `AccumulationSelectionMode` | None | Selection mode: None or Point | [AccumulationSelectionMode](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Charts.AccumulationSelectionMode.html) |
| `SelectionPattern` | `SelectionPattern` | None | Pattern for selected series/points | [SelectionPattern](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Charts.SelectionPattern.html) |
| `Series` | `List<AccumulationSeries>` | null | Chart series collection | [AccumulationSeries](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Charts.AccumulationSeries.html) |
| `SubTitle` | `string` | null | Chart subtitle text | - |
| `SubTitleStyle` | `AccumulationChartSubTitleStyle` | null | Subtitle font and styling | [AccumulationChartSubTitleStyle](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Charts.AccumulationChartSubTitleStyle.html) |
| `Theme` | `AccumulationTheme` | Material | Visual theme | [AccumulationTheme](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Charts.AccumulationTheme.html) |
| `Title` | `string` | null | Chart title text | - |
| `TitleStyle` | `AccumulationChartTitleStyleSettings` | null | Title font and styling | [AccumulationChartTitleStyleSettings](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Charts.AccumulationChartTitleStyleSettings.html) |
| `Tooltip` | `AccumulationChartTooltipSettings` | null | Tooltip configuration | [AccumulationChartTooltipSettings](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Charts.AccumulationChartTooltipSettings.html) |
| `UseGroupingSeparator` | `bool` | false | Use thousand separator for numbers | - |
| `Width` | `string` | null | Chart width (e.g., "100px", "100%") | - |

#### Event Properties

| Event | Type | Description |
|-------|------|-------------|
| `AfterExport` | `string` | Triggered after export completes |
| `AnimationComplete` | `string` | Triggered after animation completes |
| `AnnotationRender` | `string` | Triggered before annotation renders |
| `BeforeExport` | `string` | Triggered before export starts |
| `BeforePrint` | `string` | Triggered before print starts |
| `BeforeResize` | `string` | Triggered before window resize |
| `ChartDoubleClick` | `string` | Triggered on double-click |
| `ChartMouseClick` | `string` | Triggered on mouse click |
| `ChartMouseDown` | `string` | Triggered on mouse down |
| `ChartMouseLeave` | `string` | Triggered when cursor leaves |
| `ChartMouseMove` | `string` | Triggered on mouse move/hover |
| `ChartMouseUp` | `string` | Triggered on mouse up |
| `LegendClick` | `string` | Triggered after legend click |
| `LegendRender` | `string` | Triggered before legend renders |
| `Load` | `string` | Triggered before chart loads |
| `Loaded` | `string` | Triggered after chart loads |
| `PointClick` | `string` | Triggered when point is clicked |
| `PointMove` | `string` | Triggered when point is hovered |
| `PointRender` | `string` | Triggered before point renders |
| `Resized` | `string` | Triggered after window resize completes |
| `SelectionComplete` | `string` | Triggered after selection completes |
| `SeriesRender` | `string` | Triggered before series renders |
| `TextRender` | `string` | Triggered before data label renders |
| `TooltipRender` | `string` | Triggered before tooltip renders |

### AccumulationSeries Class

Represents a data series in the accumulation chart.

#### Properties

| Property | Type | Default | Description | API Reference |
|----------|------|---------|-------------|---|
| `DataSource` | `object[]` | null | Series data collection | - |
| `XName` | `string` | null | Field name for X values (categories) | - |
| `YName` | `string` | null | Field name for Y values (numeric data) | - |
| `Type` | `string` | "Pie" | Series type: Pie, Pyramid, Funnel (Doughnut = Pie + innerRadius) | - |
| `Radius` | `string` | "80%" | Chart radius (percentage or pixels) | - |
| `InnerRadius` | `string` | "0%" | Inner radius for doughnut effect (percentage) | - |
| `StartAngle` | `double` | 0 | Start angle in degrees (0-360) | - |
| `EndAngle` | `double` | 360 | End angle in degrees (0-360) | - |
| `Explode` | `bool` | false | Enable explosion on click | - |
| `ExplodeIndex` | `double` | null | Index of pre-exploded point | - |
| `ExplodeOffset` | `string` | "10%" | Distance exploded slice moves | - |
| `GroupTo` | `string` | null | Grouping threshold (value or percentage) | - |
| `GroupMode` | `string` | "Value" | Group mode: Value or Point | - |
| `GroupName` | `string` | "Others" | Name for grouped points | - |
| `PyramidMode` | `string` | "Linear" | Pyramid mode: Linear or Surface | - |
| `FunnelMode` | `string` | "Standard" | Funnel mode: Standard or Trapezoidal | - |
| `NeckWidth` | `string` | "20%" | Funnel neck width (percentage) | - |
| `NeckHeight` | `string` | "20%" | Funnel neck height (percentage) | - |
| `Width` | `string` | "80%" | Pyramid/Funnel width (percentage) | - |
| `Height` | `string` | "80%" | Pyramid/Funnel height (percentage) | - |
| `GapRatio` | `double` | 0 | Gap between pyramid/funnel segments | - |
| `Palettes` | `string[]` | null | Custom color palette | - |
| `PointColorMapping` | `string` | null | Field name for point colors | - |
| `PointRender` | `string` | null | Event triggered before point renders | - |
| `DataLabel` | `AccumulationDataLabelSettings` | null | Data label configuration | [AccumulationDataLabelSettings](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Charts.AccumulationDataLabelSettings.html) |
| `EmptyPointSettings` | `AccumulationChartEmptyPointSettings` | null | Empty point handling | [AccumulationChartEmptyPointSettings](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Charts.AccumulationChartEmptyPointSettings.html) |
| `ConnectorStyle` | `AccumulationChartConnector` | null | Connector line styling | [AccumulationChartConnector](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Charts.AccumulationChartConnector.html) |
| `Border` | `AccumulationChartBorder` | null | Series border styling | [AccumulationChartBorder](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Charts.AccumulationChartBorder.html) |
| `LegendShape` | `LegendShape` | SeriesType | Legend icon shape | [LegendShape](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Charts.LegendShape.html) |
| `TooltipMappingName` | `string` | null | Field for custom tooltip content | - |

### AccumulationDataLabelSettings Class

Configures data labels displayed on data points.

#### Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `Visible` | `bool` | false | Show/hide data labels |
| `Position` | `string` | "Outside" | Label position: Inside or Outside |
| `Name` | `string` | null | Field name for label text |
| `Template` | `string` | null | HTML template for labels |
| `Format` | `string` | null | Number format (e.g., "p1", "n2", "c2") |
| `TextWrap` | `string` | "Normal" | Text wrapping: Normal, Wrap, AnyWhere |
| `MaxWidth` | `double` | null | Max label width (pixels) |
| `Font` | `object` | null | Font configuration |
| `Border` | `object` | null | Label border configuration |
| `ConnectorStyle` | `string` | "Line" | Connector type: Line or Curve |

### AccumulationChartLegendSettings Class

Configures the legend for the chart.

#### Properties

| Property | Type | Default | Description | API Reference |
|----------|------|---------|-------------|---|
| `Visible` | `bool` | false | Show/hide legend | - |
| `Position` | `string` | "Right" | Legend position: Top, Bottom, Left, Right | [LegendPosition](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Charts.LegendPosition.html) |
| `Alignment` | `string` | "Center" | Legend alignment: Near, Center, Far | [Alignment](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Charts.Alignment.html) |
| `Width` | `string` | "0" | Legend width (pixels or percentage) | - |
| `Height` | `string` | "0" | Legend height (pixels or percentage) | - |
| `Reverse` | `bool` | false | Reverse legend item order | - |
| `Layout` | `string` | "Vertical" | Layout: Vertical or Horizontal | - |
| `MaximumColumns` | `double` | null | Max columns in horizontal layout | - |
| `ShapeWidth` | `double` | 15 | Legend shape width | - |
| `ShapeHeight` | `double` | 15 | Legend shape height | - |
| `Title` | `object` | null | Legend title configuration | - |
| `Template` | `string` | null | Custom HTML template for legend | - |
| `TextWrap` | `string` | "Normal" | Text wrapping: Normal or Wrap | - |
| `MaximumLabelWidth` | `double` | null | Max legend item label width | - |
| `EnablePages` | `bool` | false | Enable paging for large legends | - |
| `ToggleVisibility` | `bool` | true | Toggle point visibility on legend click | - |

### AccumulationChartTooltipSettings Class

Configures tooltips for the chart.

#### Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `Enable` | `bool` | false | Enable/disable tooltips |
| `Header` | `string` | null | Custom tooltip header |
| `Format` | `string` | null | Tooltip text format |
| `Template` | `string` | null | HTML template for tooltips |
| `Fill` | `string` | null | Tooltip background color |
| `Border` | `object` | null | Tooltip border configuration |
| `TextStyle` | `object` | null | Tooltip text styling |
| `Location` | `object` | null | Fixed tooltip position (x, y) |
| `Opacity` | `double` | 1 | Tooltip opacity |
| `Shared` | `bool` | false | Show shared tooltip |

### Available Enumerations

| Enum | Values | Description |
|------|--------|-------------|
| `AccumulationTheme` | Fabric, FabricDark, Bootstrap4, Bootstrap, BootstrapDark, HighContrastLight, HighContrast, Tailwind, TailwindDark, Bootstrap5, Bootstrap5Dark, Fluent, FluentDark, Fluent2, Fluent2Dark, Fluent2HighContrast, Material3, Material3Dark, Material, MaterialDark | Chart theme options |
| `AccumulationHighlightMode` | None, Point | Highlight behavior |
| `AccumulationSelectionMode` | None, Point | Selection behavior |
| `SelectionPattern` | None, Chessboard, Dots, DiagonalForward, Crosshatch, Pacman, DiagonalBackward, Grid, Turquoise, Star, Triangle, Circle, Tile, HorizontalDash, VerticalDash, Rectangle, Box, VerticalStripe, HorizontalStripe, Bubble | Pattern options for highlighting/selection |
| `LegendShape` | Circle, Rectangle, Triangle, Diamond, Cross, HorizontalLine, VerticalLine, Pentagon, InvertedTriangle, SeriesType | Legend icon shapes |

### Related Classes

| Class | Namespace | Description | API Reference |
|-------|-----------|-------------|---|
| `AccumulationChartBorder` | Syncfusion.EJ2.Charts | Border configuration | [AccumulationChartBorder](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Charts.AccumulationChartBorder.html) |
| `AccumulationChartCenter` | Syncfusion.EJ2.Charts | Center position | [AccumulationChartCenter](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Charts.AccumulationChartCenter.html) |
| `AccumulationChartMargin` | Syncfusion.EJ2.Charts | Margin configuration | [AccumulationChartMargin](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Charts.AccumulationChartMargin.html) |
| `AccumulationChartConnector` | Syncfusion.EJ2.Charts | Connector line styling | [AccumulationChartConnector](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Charts.AccumulationChartConnector.html) |
| `AccumulationChartEmptyPointSettings` | Syncfusion.EJ2.Charts | Empty point handling | [AccumulationChartEmptyPointSettings](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Charts.AccumulationChartEmptyPointSettings.html) |
| `AccumulationAnnotationSettings` | Syncfusion.EJ2.Charts | Annotation configuration | [AccumulationAnnotationSettings](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Charts.AccumulationAnnotationSettings.html) |
| `AccumulationAccessibility` | Syncfusion.EJ2.Charts | Accessibility options | [AccumulationAccessibility](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Charts.AccumulationAccessibility.html) |

## Key Properties

### AccumulationChart Properties

| Property | Type | Description | Example |
|----------|------|-------------|---------|
| `enableSmartLabels` | boolean | Auto-arrange labels to prevent overlap | `true` |
| `center` | object | Position of chart center (x, y percentages) | `{x: "50%", y: "50%"}` |
| `legendSettings` | object | Legend configuration (position, alignment) | `{visible: true, position: 'Right'}` |
| `tooltipSettings` | object | Tooltip configuration and templates | `{enable: true, format: '${point.x}: ${point.y}'}` |
| `title` | string | Chart title text | `"Browser Market Share"` |
| `height` | string | Chart height | `"450px"` |
| `width` | string | Chart width | `"100%"` |
| `theme` | string | Visual theme | `"Material"` |
| `background` | string | Background color | `"#ffffff"` |

### AccumulationSeries Properties

| Property | Type | Description | Example |
|----------|------|-------------|---------|
| `type` | string | Chart type: Pie, Pyramid, Funnel (Doughnut = Pie + innerRadius) | `"Pie"` |
| `dataSource` | object[] | Data collection | `@chartData` |
| `xName` | string | Field for category labels | `"xValue"` |
| `yName` | string | Field for values | `"yValue"` |
| `radius` | string | Chart radius (percentage or pixel) | `"80%"` |
| `innerRadius` | string | Inner radius for doughnut (percentage) | `"40%"` |
| `startAngle` | number | Start angle in degrees | `0` |
| `endAngle` | number | End angle in degrees | `360` |
| `explode` | boolean | Enable slice explosion on click | `true` |
| `explodeIndex` | number | Index of pre-exploded slice | `2` |
| `explodeOffset` | string | Explode distance | `"10%"` |
| `groupTo` | string | Threshold for grouping | `"11"` |
| `groupMode` | string | Group by: Point, Value | `"Value"` |

### DataLabel Properties

| Property | Type | Description | Example |
|----------|------|-------------|---------|
| `visible` | boolean | Show/hide data labels | `true` |
| `position` | string | Inside or Outside | `"Outside"` |
| `name` | string | Field name for label text | `"text"` |
| `template` | string | Custom HTML template | `"<div>${point.x}: ${point.y}%</div>"` |
| `connectorStyle` | string | Line or Curve | `"Curve"` |
| `font` | object | Font customization | `{size: '12px', color: '#000'}` |

## Common Use Cases

### 1. Market Share Analysis
Display product/service market distribution with pie charts showing competitor percentages.

### 2. Budget Allocation
Visualize department spending or resource allocation with doughnut charts and center totals.

### 3. Survey Results
Present poll or survey responses with grouped categories for small values.

### 4. Sales Funnel Tracking
Monitor conversion stages from leads to customers using funnel charts.

### 5. Organizational Hierarchy
Display team size distribution or role distribution with pyramid charts.

### 6. Mobile Dashboards
Create responsive data visualizations optimized for touch interactions and small screens.

### 7. Report Generation
Export charts as images or PDFs for automated reporting systems.

### 8. Real-Time Monitoring
Update charts dynamically to show live statistics (server status, user activity).

## Related Components

- **Chart:** For line, bar, column, area, and other Cartesian charts
- **RangeNavigator:** For timeline-based data exploration
- **StockChart:** For financial data visualization
- **TreeMap:** For hierarchical data with rectangles

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Opera (latest)

## Additional Resources

- [Syncfusion ASP.NET Core Accumulation Chart Documentation](https://ej2.syncfusion.com/aspnetcore/documentation/accumulation-chart/getting-started)
- [API Reference](https://help.syncfusion.com/cr/aspnetcore-js2/Syncfusion.EJ2.Charts.AccumulationChart.html)
- [Live Demos](https://ej2.syncfusion.com/aspnetcore/AccumulationChart/Pie)
- [GitHub Examples](https://github.com/SyncfusionExamples/ASP-NET-Core-Getting-Started-Examples/tree/main/AccumulationChart)

---

**Next Steps:**
1. Read [getting-started.md](references/getting-started.md) for detailed installation
2. Explore [chart-types.md](references/chart-types.md) for type-specific features
3. Review [data-visualization.md](references/data-visualization.md) for styling
4. Check [accessibility.md](references/accessibility.md) for compliance requirements
