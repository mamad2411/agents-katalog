---
name: syncfusion-winui-circular-charts
description: Implement Syncfusion WinUI Circular Charts (SfCircularChart) with pie and doughnut visualizations for proportional data display. Use this when working with circular charts, pie charts, or doughnut charts in WinUI applications. This skill covers chart series configuration, data labels, legends, tooltips, segment selection, exploding segments, and visual customization for interactive circular visualizations.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion WinUI Circular Charts

This skill guides you in implementing Syncfusion WinUI Circular Charts (SfCircularChart) for visualizing proportional data with pie and doughnut charts. The component provides rich interactive features including legends, data labels, tooltips, selection, and segment explosion.

## When to Use This Skill

Use this skill when the user needs to:

- Create **pie charts** or **doughnut charts** in WinUI applications
- Display **proportional or percentage data** visually
- Implement **circular data visualizations** (market share, budget breakdown, survey results)
- Add **interactive features** to circular charts (tooltips, selection, exploding segments)
- Configure **data labels**, **legends**, or **tooltips** for circular charts
- Customize **appearance** with palettes, gradients, or custom colors
- Create **semi-circular** or **quarter-circular** chart variations
- Implement **combination charts** (pie + doughnut in same chart)
- Handle **user interactions** (segment selection, tap to explode)

## Component Overview

**Syncfusion SfCircularChart** is a powerful data visualization component for WinUI that displays data in circular formats. It supports:

- **Two Chart Types:** Pie and Doughnut series
- **Rich Visual Elements:** Legends, data labels, tooltips, headers
- **User Interactions:** Selection, explode segments, toggle visibility
- **Multiple Series:** Display multiple pie or doughnut series simultaneously
- **Dynamic Updates:** Real-time data binding and updates
- **Extensive Customization:** Palettes, gradients, templates, styling

## Documentation and Navigation Guide

### Getting Started

📄 **Read:** [references/getting-started.md](references/getting-started.md)

Read this reference when the user needs to:
- Install the Syncfusion.Chart.WinUI NuGet package
- Set up basic circular chart in XAML or C#
- Create a ViewModel with data model
- Bind data to the chart series
- Understand complete initial setup and configuration
- See a working minimal example

### Chart Types

#### Pie Charts

📄 **Read:** [references/pie-charts.md](references/pie-charts.md)

Read this reference when the user needs to:
- Create and configure PieSeries
- Adjust pie chart radius
- Group small data points into "Others" category (GroupTo, GroupMode)
- Create semi-pie or quarter-pie charts (StartAngle, EndAngle)
- Implement combination charts (pie + doughnut together)
- Understand pie-specific features and configurations

#### Doughnut Charts

📄 **Read:** [references/doughnut-charts.md](references/doughnut-charts.md)

Read this reference when the user needs to:
- Create and configure DoughnutSeries
- Set inner radius (InnerRadius property)
- Display multiple doughnut series in one chart
- Create semi-doughnut or quarter-doughnut shapes
- Understand differences between pie and doughnut series
- Size and position doughnut charts

### Visual Elements

#### Legend

📄 **Read:** [references/legend.md](references/legend.md)

Read this reference when the user needs to:
- Enable and configure chart legend
- Add legend title or header
- Customize legend icons (type, size, template)
- Adjust legend placement (Left, Right, Top, Bottom)
- Add checkboxes for toggling segment visibility
- Customize legend appearance (background, borders, spacing)
- Create custom legend item templates
- Control legend item margins and alignment

#### Data Labels

📄 **Read:** [references/data-labels.md](references/data-labels.md)

Read this reference when the user needs to:
- Enable and display data labels on segments
- Configure label context (Percentage, YValue, DataLabelItem)
- Customize label appearance (fonts, colors, borders)
- Position labels (Inside, Outside, OutsideExtended)
- Add connector lines between labels and segments
- Customize connector line styles and types (Line, Bezier, StraightLine)
- Rotate data labels
- Create custom data label templates
- Apply series palette to labels

#### Tooltips

📄 **Read:** [references/tooltips.md](references/tooltips.md)

Read this reference when the user needs to:
- Enable tooltips on segment hover
- Configure tooltip behavior (duration, animation, delay)
- Customize tooltip styling (background, borders)
- Style tooltip labels (fonts, colors)
- Position tooltips (alignment, offsets)
- Create custom tooltip templates
- Control tooltip display settings

#### Title and Header

📄 **Read:** [references/title-header.md](references/title-header.md)

Read this reference when the user needs to:
- Add a title or header to the chart
- Use custom UIElements as chart header
- Align chart header (left, center, right)
- Style and format the chart title
- Create bordered or decorated headers

### User Interactions

#### Selection

📄 **Read:** [references/selection.md](references/selection.md)

Read this reference when the user needs to:
- Enable segment selection behavior
- Configure single or multi-selection modes
- Customize selection appearance (SelectionBrush)
- Programmatically select segments (SelectedIndex, SelectedIndexes)
- Handle selection events (SelectionChanging, SelectionChanged)
- Implement deselection behavior
- Control selection types (Single, SingleDeselect, Multiple, None)

#### Explode Segments

📄 **Read:** [references/explode-segments.md](references/explode-segments.md)

Read this reference when the user needs to:
- Explode specific segments to highlight them
- Set explode radius for separation distance
- Explode all segments simultaneously
- Enable tap-to-explode interaction
- Programmatically control exploded segments
- Understand when to use segment explosion

### Customization

#### Appearance

📄 **Read:** [references/appearance.md](references/appearance.md)

Read this reference when the user needs to:
- Apply predefined palette brushes
- Create custom color palettes (PaletteBrushes)
- Apply gradients to segments (LinearGradientBrush, RadialGradientBrush)
- Customize segment colors and styling
- Understand visual customization patterns

## Quick Start Example

Here's a minimal example to create a basic pie chart:

**1. Install NuGet Package:**
```
Install-Package Syncfusion.Chart.WinUI
```

**2. Create Data Model and ViewModel:**

```csharp
public class Sales
{
    public string Product { get; set; }
    public double SalesRate { get; set; }
}

public class ChartViewModel
{
    public List<Sales> Data { get; set; }

    public ChartViewModel()
    {
        Data = new List<Sales>()
        {
            new Sales() { Product = "iPad", SalesRate = 25 },
            new Sales() { Product = "iPhone", SalesRate = 35 },
            new Sales() { Product = "MacBook", SalesRate = 15 },
            new Sales() { Product = "Mac", SalesRate = 5 },
            new Sales() { Product = "Others", SalesRate = 10 }
        };
    }
}
```

**3. Create Circular Chart in XAML:**

```xml
<Window
    xmlns:chart="using:Syncfusion.UI.Xaml.Charts"
    xmlns:model="using:YourNamespace.ViewModel">

    <chart:SfCircularChart Header="Product Sales">
        <!-- Set DataContext -->
        <chart:SfCircularChart.DataContext>
            <model:ChartViewModel/>
        </chart:SfCircularChart.DataContext>
        
        <!-- Add Legend -->
        <chart:SfCircularChart.Legend>
            <chart:ChartLegend/>
        </chart:SfCircularChart.Legend>
        
        <!-- Add Pie Series -->
        <chart:SfCircularChart.Series>
            <chart:PieSeries ItemsSource="{Binding Data}"
                           XBindingPath="Product"
                           YBindingPath="SalesRate"
                           ShowDataLabels="True"
                           EnableTooltip="True"/>
        </chart:SfCircularChart.Series>
    </chart:SfCircularChart>
</Window>
```

**4. Or Create in C#:**

```csharp
SfCircularChart chart = new SfCircularChart();
chart.Header = "Product Sales";
chart.DataContext = new ChartViewModel();
chart.Legend = new ChartLegend();

PieSeries series = new PieSeries();
series.SetBinding(PieSeries.ItemsSourceProperty, new Binding() { Path = new PropertyPath("Data") });
series.XBindingPath = "Product";
series.YBindingPath = "SalesRate";
series.ShowDataLabels = true;
series.EnableTooltip = true;

chart.Series.Add(series);
this.Content = chart;
```

## Common Patterns

### Pattern 1: Pie Chart with Data Labels and Legend

```xml
<chart:SfCircularChart Header="Sales Distribution">
    <chart:SfCircularChart.Legend>
        <chart:ChartLegend/>
    </chart:SfCircularChart.Legend>
    
    <chart:SfCircularChart.Series>
        <chart:PieSeries ItemsSource="{Binding Data}"
                       XBindingPath="Category"
                       YBindingPath="Value"
                       ShowDataLabels="True">
            <chart:PieSeries.DataLabelSettings>
                <chart:CircularDataLabelSettings Context="Percentage"
                                               Position="Outside"
                                               ShowConnectorLine="True"/>
            </chart:PieSeries.DataLabelSettings>
        </chart:PieSeries>
    </chart:SfCircularChart.Series>
</chart:SfCircularChart>
```

### Pattern 2: Doughnut Chart with Custom Colors

```xml
<chart:SfCircularChart>
    <chart:SfCircularChart.Resources>
        <BrushCollection x:Key="customBrushes">
            <SolidColorBrush Color="#4dd0e1"/>
            <SolidColorBrush Color="#26c6da"/>
            <SolidColorBrush Color="#00bcd4"/>
        </BrushCollection>
    </chart:SfCircularChart.Resources>
    
    <chart:SfCircularChart.Series>
        <chart:DoughnutSeries ItemsSource="{Binding Data}"
                            XBindingPath="Name"
                            YBindingPath="Amount"
                            InnerRadius="0.6"
                            PaletteBrushes="{StaticResource customBrushes}"/>
    </chart:SfCircularChart.Series>
</chart:SfCircularChart>
```

### Pattern 3: Interactive Chart with Selection and Explode

```xml
<chart:SfCircularChart>
    <chart:SfCircularChart.Series>
        <chart:PieSeries ItemsSource="{Binding Data}"
                       XBindingPath="Product"
                       YBindingPath="Sales"
                       ExplodeOnTap="True"
                       ExplodeRadius="10">
            <chart:PieSeries.SelectionBehavior>
                <chart:DataPointSelectionBehavior SelectionBrush="Orange"
                                                Type="Single"/>
            </chart:PieSeries.SelectionBehavior>
        </chart:PieSeries>
    </chart:SfCircularChart.Series>
</chart:SfCircularChart>
```

### Pattern 4: Semi-Circular Chart

```xml
<chart:SfCircularChart>
    <chart:SfCircularChart.Series>
        <chart:PieSeries ItemsSource="{Binding Data}"
                       XBindingPath="Category"
                       YBindingPath="Value"
                       StartAngle="180"
                       EndAngle="360"
                       ShowDataLabels="True"/>
    </chart:SfCircularChart.Series>
</chart:SfCircularChart>
```

## Key Properties

### SfCircularChart Properties

- **Header** - Sets the chart title/header
- **Legend** - Configures the chart legend
- **Series** - Collection of circular series (PieSeries, DoughnutSeries)
- **TooltipBehavior** - Configures tooltip display behavior

### Series Properties (PieSeries/DoughnutSeries)

- **ItemsSource** - Data source for the series
- **XBindingPath** - Property path for category/label values
- **YBindingPath** - Property path for numeric values
- **ShowDataLabels** - Enables data labels on segments
- **EnableTooltip** - Enables tooltips on hover
- **PaletteBrushes** - Custom colors for segments
- **Radius** - Size of the pie/doughnut (0 to 1)
- **InnerRadius** - Inner hole size for doughnut (0 to 1)
- **StartAngle** - Starting angle for rendering (0-360)
- **EndAngle** - Ending angle for rendering (0-360)
- **ExplodeIndex** - Index of segment to explode
- **ExplodeAll** - Explodes all segments
- **ExplodeRadius** - Distance for exploded segments
- **ExplodeOnTap** - Enables tap-to-explode interaction
- **GroupTo** - Threshold for grouping small segments
- **GroupMode** - Grouping mode (Value, Percentage, Angle)
- **SelectionBehavior** - Configures segment selection
- **DataLabelSettings** - Configures data label appearance
- **LegendIcon** - Icon type for legend items

## Common Use Cases

### When to Use Pie Charts

- Showing **parts of a whole** (market share, budget allocation)
- Displaying **percentage distributions** (survey results, demographics)
- **Simple comparisons** with 5-7 categories
- When **proportions** are more important than exact values
- **Single data series** visualization

### When to Use Doughnut Charts

- Similar to pie charts but with **better label placement** (can use center)
- **Multiple concentric series** for comparison
- When you want to **display central content** (total, summary)
- **More modern aesthetic** preference
- **Better for dense data** with many categories

### When to Use Explode Segments

- **Highlighting specific data points** (best performer, focus area)
- Drawing attention to **important segments**
- Creating **visual emphasis** for presentation
- **Interactive exploration** (tap to explode)

### When to Use Selection

- Allowing users to **filter or drill down** into data
- **Interactive dashboards** where segment selection triggers other views
- **Comparison scenarios** (select multiple segments)
- **Data exploration** interfaces

## Related Components

- **Cartesian Charts** - For time-series, trends, and comparisons (bar, line, column charts)
- **Funnel/Pyramid Charts** - For hierarchical or stage-based data
- **Gauge Charts** - For single-value indicators with ranges

## Tips and Best Practices

1. **Limit segments** to 5-7 for readability; use GroupTo for small values
2. **Use data labels** for exact values; legends for category names
3. **Enable tooltips** for interactive exploration
4. **Consider doughnut** for multiple series or central content
5. **Use selection** sparingly; explode for emphasis only
6. **Choose contrasting colors** for better segment differentiation
7. **Test responsiveness** - circular charts adapt well to different sizes
