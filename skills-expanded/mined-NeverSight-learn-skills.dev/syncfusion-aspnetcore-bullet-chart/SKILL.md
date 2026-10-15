---
name: syncfusion-aspnetcore-bullet-chart
description: Guide for implementing Syncfusion Bullet Chart in ASP.NET Core applications. Use this skill when building comparative performance visualizations, KPI dashboards, progress tracking, goal comparison charts, or any scenario requiring actual vs. target value display. Bullet charts effectively compare actual performance against target benchmarks in a compact format—ideal for dashboards, executive summaries, and performance monitoring systems. Trigger when user mentions bullet chart, performance comparison, target visualization, KPI dashboard, progress bars with targets.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion ASP.NET Core Bullet Chart

The Bullet Chart is a variation of a bar chart that displays actual performance against target benchmarks in a compact, visually efficient format. It combines multiple data elements (value bar, target marker, ranges) to provide immediate performance insights.

## When to Use This Skill

Use the Bullet Chart skill when you need to:

- **Compare Performance vs. Target** - Display actual values alongside target/goal values in a single visualization
- **Build KPI Dashboards** - Quickly assess key performance indicators at a glance
- **Show Progress with Benchmarks** - Track progress toward goals with comparative ranges (poor, satisfactory, good)
- **Monitor Multiple Metrics** - Present multiple bullet charts in a dashboard for comparative analysis
- **Create Compact Visualizations** - Fit more data in less space compared to traditional bar charts
- **Build Performance Reports** - Executive dashboards, sales tracking, productivity metrics, revenue forecasting

Common scenarios:
- Sales vs. quota tracking
- Employee performance vs. targets
- Project milestones vs. deadlines
- Revenue vs. forecasts
- Customer satisfaction scores vs. goals

---

## Navigation and Documentation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and ASP.NET Core project setup
- NuGet package installation
- Adding TagHelper and script resources
- Creating your first bullet chart with data
- Adding titles to charts

### Data Binding and Configuration
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Configuring DataSource property
- Mapping value and target fields
- Working with data models
- Dynamic and static data binding
- Data structure best practices

### Axis Customization
📄 **Read:** [references/axis-customization.md](references/axis-customization.md)
- Customizing tick lines and labels
- Label formatting and number formatting
- Tick placement and label placement options
- Category label configuration
- Advanced axis positioning

### Ranges and Comparative Bars
📄 **Read:** [references/ranges-and-bars.md](references/ranges-and-bars.md)
- Configuring performance ranges (poor, satisfactory, good)
- Target bar types (Rect, Cross, circle)
- Value bar customization
- Creating effective comparative visualizations
- Color schemes and styling ranges

### Customization and Layout
📄 **Read:** [references/customization.md](references/customization.md)
- Orientation (horizontal vs. vertical rendering)
- Right-to-Left (RTL) support
- Animation settings and transitions
- Chart sizing and responsive dimensions
- Theme and color customization

### Data Labels, Tooltips, and Accessibility
📄 **Read:** [references/data-and-accessibility.md](references/data-and-accessibility.md)
- Displaying data labels
- Configuring hover tooltips
- WAI-ARIA attributes for accessibility
- Keyboard navigation support
- Creating accessible dashboards

---

## Quick Start Example

**Basic Bullet Chart with Value and Target:**

```csharp
// CSHTML.cs - Controller/Page code
public class QuickStartBulletData
{
    public double Value { get; set; }
    public double Target { get; set; }
    public string Category { get; set; }
}

public IActionResult Index()
{
    ViewBag.ChartData = new List<QuickStartBulletData>
    {
        new QuickStartBulletData { Value = 75, Target = 80, Category = "Q1" },
        new QuickStartBulletData { Value = 85, Target = 90, Category = "Q2" },
        new QuickStartBulletData { Value = 65, Target = 75, Category = "Q3" }
    };
    return View();
}
```

```cshtml
<!-- CSHTML View -->
<ejs-bulletchart id="container" 
    dataSource="@ViewBag.ChartData" 
    valueField="Value" 
    targetField="Target"
    categoryField="Category"
    minimum="0"
    maximum="100"
    interval="20"
    title="Sales Performance">
    <e-bullet-range-collection>
        <e-bullet-range end="50" color="lightgray"></e-bullet-range>
        <e-bullet-range end="75" color="lightblue"></e-bullet-range>
        <e-bullet-range end="100" color="lightgreen"></e-bullet-range>
    </e-bullet-range-collection>
</ejs-bulletchart>
```

---

## Common Patterns

### Pattern 1: Dashboard with Multiple Bullet Charts

Display multiple metrics side-by-side for executive monitoring:

```csharp
// Each metric has its own data and configuration
var salesData = new List<BulletChartData> { /* sales vs quota */ };
var revenueData = new List<BulletChartData> { /* revenue vs forecast */ };
var customerSatisfaction = new List<BulletChartData> { /* score vs target */ };
```

### Pattern 2: Using Categories for Multiple Values

Display multiple categories in one chart:

```cshtml
<ejs-bulletchart id="container" 
    dataSource="@ViewBag.MultipleCategoryData"
    categoryField="Category"
    valueField="Value"
    targetField="Target">
</ejs-bulletchart>
```

### Pattern 3: Range-Based Color Coding

Define ranges to automatically color-code performance levels:

```cshtml
<e-bullet-range-collection>
    <e-bullet-range end="25" color="#ff6b6b"></e-bullet-range>  <!-- Poor -->
    <e-bullet-range end="50" color="#ffd43b"></e-bullet-range>  <!-- Fair -->
    <e-bullet-range end="75" color="#69db7c"></e-bullet-range>  <!-- Good -->
    <e-bullet-range end="100" color="#51cf66"></e-bullet-range> <!-- Excellent -->
</e-bullet-range-collection>
```

---

## Key Configuration Props

Prop | Type | Default | Purpose |
|------|------|---------|---------|
| `dataSource` | object | null | Data collection to display |
| `valueField` | string | "" | Field name mapping to actual/feature values |
| `targetField` | string | "" | Field name mapping to target/comparative values |
| `categoryField` | string | null | Field for category labels on multi-row charts |
| `title` | string | "" | Chart title text |
| `subtitle` | string | "" | Chart subtitle text |
| `titlePosition` | TextPosition | Top | Position of title: `Top`, `Bottom`, `Left`, `Right` |
| `titleStyle` | BulletChartBulletLabelStyle | null | Font/style for the chart title |
| `subtitleStyle` | BulletChartBulletLabelStyle | null | Font/style for the chart subtitle |
| `orientation` | OrientationType | Horizontal | Layout direction: `Horizontal` or `Vertical` |
| `minimum` | double | NaN | Minimum value of the scale axis |
| `maximum` | double | NaN | Maximum value of the scale axis |
| `interval` | double | NaN | Interval between axis tick marks |
| `ranges` | List\<Range\> | null | Qualitative range definitions for background coloring |
| `animation` | BulletChartAnimation | null | Animation settings (`enable`, `duration`, `delay`) |
| `tooltip` | BulletChartBulletTooltipSettings | null | Hover tooltip configuration |
| `dataLabel` | BulletChartBulletDataLabel | null | Value labels displayed on the feature bar |
| `labelStyle` | BulletChartBulletLabelStyle | null | Font/style for axis labels |
| `categoryLabelStyle` | BulletChartBulletLabelStyle | null | Font/style for category labels |
| `labelFormat` | string | "" | Axis label number format (e.g., `"n2"`, `"c2"`, `"p1"`) |
| `labelPosition` | LabelsPlacement | Outside | Axis label placement: `Inside` or `Outside` |
| `tickPosition` | TickPosition | Outside | Tick mark placement: `Inside` or `Outside` |
| `majorTickLines` | BulletChartMajorTickLines | null | Major tick line width, height, and color |
| `minorTickLines` | BulletChartMinorTickLines | null | Minor tick line width, height, and color |
| `minorTicksPerInterval` | double | 4 | Number of minor ticks between each major tick |
| `opposedPosition` | boolean | false | Render axis on opposite side |
| `enableGroupSeparator` | boolean | false | Show thousands separator in axis labels |
| `enableRtl` | boolean | false | Right-to-left rendering support |
| `enablePersistence` | boolean | false | Persist component state between page reloads |
| `theme` | ChartTheme | Material | Visual theme (e.g., `Material`, `Bootstrap5`, `Fluent2`) |
| `width` | string | null | Chart width in pixels or percentage (e.g., `"500px"`, `"100%"`) |
| `height` | string | null | Chart height in pixels or percentage |
| `margin` | BulletChartMargin | null | Left, right, top, and bottom margins |
| `border` | BulletChartContainerBorder | null | Chart border color and width |
| `valueFill` | string | null | Fill color for the feature/actual bar |
| `valueHeight` | double | 6 | Height/thickness of the feature bar |
| `valueBorder` | BulletChartValueBorder | null | Border color and width around the feature bar |
| `type` | FeatureType | Rect | Shape of the feature bar: `Rect` or `Dot` |
| `targetColor` | string | "#191919" | Color of the comparative/target marker |
| `targetWidth` | double | 5 | Width/thickness of the target marker |
| `targetTypes` | object | null | Shape of the target marker(s): `Rect`, `Circle`, or `Cross` |
| `legendSettings` | BulletChartBulletChartLegendSettings | null | Legend visibility and positioning |
| `query` | string | null | Query string for filtering the data source |
| `locale` | string | null | Locale for number formatting |
| `tabIndex` | double | 1 | Tab index for keyboard accessibility |
| `htmlAttributes` | object | — | Additional HTML attributes (title, name, etc.) |

### Events

| Event | Purpose |
|-------|---------|
| `load` | Fires before the bullet chart loads |
| `loaded` | Fires after the bullet chart renders |
| `tooltipRender` | Fires before a tooltip is rendered |
| `legendRender` | Fires before the legend is rendered |
| `beforePrint` | Fires before the chart is printed |
| `bulletChartMouseClick` | Fires when the chart is clicked |

---

## Common Use Cases

**Sales Dashboard:**
- Track individual sales rep performance vs. quota
- Display quarterly revenue vs. forecast
- Monitor pipeline vs. targets

**HR & Performance:**
- Employee KPIs vs. goals
- Team productivity metrics
- Project milestone progress

**Operations:**
- System uptime vs. SLA targets
- Response time vs. acceptable levels
- Cost vs. budget

**Retail:**
- Store sales vs. targets
- Inventory turnover vs. goals
- Customer satisfaction vs. benchmarks
