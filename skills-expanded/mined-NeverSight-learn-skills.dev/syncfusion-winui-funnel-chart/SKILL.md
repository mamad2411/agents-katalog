---
name: syncfusion-winui-funnel-chart
description: Implement Syncfusion WinUI Funnel Chart (SfFunnelChart) for visualizing data across stages in a process or workflow. Use this when working with funnel charts, conversion funnels, sales pipelines, or process stage analysis in WinUI applications. This skill covers stage-based metrics, hierarchical data representation with decreasing values, and visual representation of progressive reduction in data values across sequential stages.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion WinUI Funnel Charts

The Syncfusion WinUI Funnel Chart (`SfFunnelChart`) is a specialized data visualization control for representing data that progressively decreases across stages in a process. It's ideal for analyzing conversion rates, sales pipelines, recruitment processes, and any workflow with sequential stages.

## When to Use This Skill

Use this skill when the user needs to:

- **Visualize conversion funnels** - Sales pipelines, marketing campaigns, user acquisition flows
- **Analyze process stages** - Recruitment pipelines, order fulfillment, application workflows
- **Display hierarchical data** - Data that naturally decreases from stage to stage
- **Create stage-based metrics** - Performance tracking across sequential phases
- **Implement interactive data exploration** - With tooltips, selection, and segment explosion
- **Customize visual appearance** - Palettes, gradients, labels, legends, and styling

## Component Overview

The `SfFunnelChart` is part of the `Syncfusion.Chart.WinUI` NuGet package and provides:

- **Data binding** with `ItemsSource`, `XBindingPath`, and `YBindingPath`
- **Visual customization** through titles, legends, data labels, and appearance settings
- **Interactive features** including tooltips, selection, and exploding segments
- **Flexible rendering** with multiple modes and layout options
- **Rich styling** using palettes, gradients, and custom templates

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)

Use this reference when you need to:
- Install the Syncfusion.Chart.WinUI NuGet package
- Set up basic chart structure with XAML or C#
- Configure namespace imports (`Syncfusion.UI.Xaml.Charts`)
- Create and bind a ViewModel with data
- Set `XBindingPath` and `YBindingPath` for data mapping
- Display your first funnel chart with basic configuration

### Title Customization
📄 **Read:** [references/title-customization.md](references/title-customization.md)

Use this reference when you need to:
- Add a title to the chart using the `Header` property
- Customize title appearance with custom templates
- Align the title (left, center, right)
- Style title elements with borders, colors, and fonts
- Create complex title layouts

### Legend Configuration
📄 **Read:** [references/legend.md](references/legend.md)

Use this reference when you need to:
- Enable and configure the chart legend
- Add a legend title or header
- Customize legend icons (size, visibility)
- Control legend item spacing and layout
- Add checkboxes for toggling segment visibility
- Position the legend (top, bottom, left, right)
- Style the legend background and borders
- Create custom legend item templates

### Data Labels
📄 **Read:** [references/data-labels.md](references/data-labels.md)

Use this reference when you need to:
- Enable data labels with `ShowDataLabels`
- Configure label context (YValue, Percentage, XValue)
- Customize label appearance (colors, fonts, borders)
- Format label values with custom patterns
- Rotate labels for better positioning
- Create custom label templates

### Tooltips
📄 **Read:** [references/tooltip.md](references/tooltip.md)

Use this reference when you need to:
- Enable tooltips with `EnableTooltip`
- Configure `ChartTooltipBehavior` for customization
- Style tooltip background and borders
- Customize tooltip label text styles
- Position tooltips with alignment and offset properties
- Control tooltip timing (duration, delay, animation)
- Create custom tooltip templates

### Selection
📄 **Read:** [references/selection.md](references/selection.md)

Use this reference when you need to:
- Enable segment selection with `DataPointSelectionBehavior`
- Configure selection types (Single, SingleDeselect, Multiple, None)
- Customize selection appearance with `SelectionBrush`
- Programmatically select segments using `SelectedIndex` or `SelectedIndexes`
- Handle selection events (`SelectionChanging`, `SelectionChanged`)
- Implement custom selection logic

### Exploding Segments
📄 **Read:** [references/exploding-segments.md](references/exploding-segments.md)

Use this reference when you need to:
- Explode specific segments to draw attention
- Configure `ExplodeIndex` for initial explosion
- Set `ExplodeOffset` to control explosion distance
- Enable `ExplodeOnTap` for interactive explosion
- Highlight important data points visually

### Appearance and Styling
📄 **Read:** [references/appearance-styling.md](references/appearance-styling.md)

Use this reference when you need to:
- Apply predefined palette brushes
- Create custom color palettes
- Apply linear gradients to segments
- Apply radial gradients to segments
- Configure gradient stops and colors
- Design cohesive color schemes

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)

Use this reference when you need to:
- Add spacing between segments using `GapRatio`
- Customize the neck width with `MinimumWidth`
- Create inverted pyramids
- Configure rendering mode (`ValueIsHeight` vs `ValueIsWidth`)
- Optimize chart performance
- Handle edge cases and complex scenarios

## Quick Start Example

Here's a minimal example to create a funnel chart with legend and data labels:

### XAML Implementation

```xml
<Window
    x:Class="FunnelChartDemo.MainWindow"
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    xmlns:chart="using:Syncfusion.UI.Xaml.Charts"
    xmlns:model="using:FunnelChartDemo.ViewModel">

    <chart:SfFunnelChart x:Name="chart"
                         Header="SALES PIPELINE"
                         EnableTooltip="True"
                         ShowDataLabels="True"
                         Height="400" Width="600"
                         ItemsSource="{Binding Data}"
                         XBindingPath="Stage"
                         YBindingPath="Value">
        
        <chart:SfFunnelChart.DataContext>
            <model:ChartViewModel />
        </chart:SfFunnelChart.DataContext>
        
        <chart:SfFunnelChart.Legend>
            <chart:ChartLegend />
        </chart:SfFunnelChart.Legend>
    </chart:SfFunnelChart>
</Window>
```

### C# Implementation

```csharp
using Syncfusion.UI.Xaml.Charts;

public sealed partial class MainWindow : Window
{
    public MainWindow()
    {
        this.InitializeComponent();
        
        SfFunnelChart chart = new SfFunnelChart();
        ChartViewModel viewModel = new ChartViewModel();
        chart.DataContext = viewModel;
        
        chart.SetBinding(
            SfFunnelChart.ItemsSourceProperty,
            new Binding() { Path = new PropertyPath("Data") });
        
        chart.XBindingPath = "Stage";
        chart.YBindingPath = "Value";
        chart.Header = "SALES PIPELINE";
        chart.Height = 400;
        chart.Width = 600;
        chart.Legend = new ChartLegend();
        chart.EnableTooltip = true;
        chart.ShowDataLabels = true;
        
        this.Content = chart;
    }
}
```

### ViewModel

```csharp
public class Model
{
    public string Stage { get; set; }
    public double Value { get; set; }
}

public class ChartViewModel
{
    public List<Model> Data { get; set; }
    
    public ChartViewModel()
    {
        Data = new List<Model>()
        {
            new Model() { Stage = "Leads", Value = 1000 },
            new Model() { Stage = "Qualified", Value = 750 },
            new Model() { Stage = "Proposal", Value = 500 },
            new Model() { Stage = "Negotiation", Value = 300 },
            new Model() { Stage = "Closed Won", Value = 150 }
        };
    }
}
```

## Common Patterns

### Pattern 1: Sales Funnel with Custom Colors

```xml
<Grid>
    <Grid.Resources>
        <BrushCollection x:Key="salesColors">
            <SolidColorBrush Color="#4dd0e1"/>
            <SolidColorBrush Color="#26c6da"/>
            <SolidColorBrush Color="#00bcd4"/>
            <SolidColorBrush Color="#0097a7"/>
            <SolidColorBrush Color="#00838f"/>
        </BrushCollection>
    </Grid.Resources>
    
    <chart:SfFunnelChart ItemsSource="{Binding Data}"
                         XBindingPath="Stage"
                         YBindingPath="Value"
                         PaletteBrushes="{StaticResource salesColors}"
                         ShowDataLabels="True">
        <chart:SfFunnelChart.DataLabelSettings>
            <chart:FunnelDataLabelSettings Context="Percentage" 
                                          Foreground="White" />
        </chart:SfFunnelChart.DataLabelSettings>
    </chart:SfFunnelChart>
</Grid>
```

### Pattern 2: Interactive Funnel with Selection

```xml
<chart:SfFunnelChart ItemsSource="{Binding Data}"
                     XBindingPath="Stage"
                     YBindingPath="Value"
                     EnableTooltip="True">
    
    <chart:SfFunnelChart.SelectionBehavior>
        <chart:DataPointSelectionBehavior SelectionBrush="Orange"
                                         Type="Single"/>
    </chart:SfFunnelChart.SelectionBehavior>
    
    <chart:SfFunnelChart.TooltipBehavior>
        <chart:ChartTooltipBehavior />
    </chart:SfFunnelChart.TooltipBehavior>
</chart:SfFunnelChart>
```

### Pattern 3: Exploded Segment Emphasis

```xml
<chart:SfFunnelChart ItemsSource="{Binding Data}"
                     XBindingPath="Stage"
                     YBindingPath="Value"
                     ExplodeIndex="2"
                     ExplodeOffset="40"
                     ExplodeOnTap="True"
                     GapRatio="0.1">
</chart:SfFunnelChart>
```

## Key Properties Reference

### Essential Properties
- `ItemsSource` - Data source for the chart
- `XBindingPath` - Property path for segment labels (stage names)
- `YBindingPath` - Property path for segment values
- `Header` - Chart title (string or UIElement)
- `Legend` - ChartLegend instance for displaying segment information

### Visual Properties
- `ShowDataLabels` - Enable/disable data labels (bool)
- `EnableTooltip` - Enable/disable tooltips (bool)
- `PaletteBrushes` - Custom color palette (BrushCollection)
- `GapRatio` - Spacing between segments (0.0 to 1.0)
- `MinimumWidth` - Neck width at the bottom (double)

### Rendering Properties
- `Mode` - Rendering mode: `ValueIsHeight` or `ValueIsWidth`
- `Height` / `Width` - Chart dimensions

### Interaction Properties
- `SelectionBehavior` - Configure segment selection
- `ExplodeIndex` - Index of segment to explode
- `ExplodeOffset` - Distance of exploded segment
- `ExplodeOnTap` - Enable interactive explosion

### Configuration Objects
- `DataLabelSettings` - FunnelDataLabelSettings for label customization
- `TooltipBehavior` - ChartTooltipBehavior for tooltip customization

## Common Use Cases

### Sales and Marketing Analytics
- Visualize sales pipeline stages from leads to closed deals
- Track marketing campaign conversion rates
- Analyze customer acquisition funnels
- Display website visitor conversion paths

### Business Process Analysis
- Recruitment pipeline visualization (applicants → hired)
- Order fulfillment stages
- Customer support ticket resolution flow
- Product development milestones

### E-commerce and Retail
- Shopping cart abandonment analysis
- Checkout process completion rates
- Product browsing to purchase conversion
- Customer journey mapping

### Financial Services
- Loan application process stages
- Investment funnel analysis
- Customer onboarding progress
- Account upgrade conversion tracking

## Related Skills

- [Implementing Syncfusion WinUI Components](../../) - Parent library skill
- Other WinUI Chart Types (if available in the library)

---

**Need help?** Refer to the specific reference files above based on the feature you want to implement.
