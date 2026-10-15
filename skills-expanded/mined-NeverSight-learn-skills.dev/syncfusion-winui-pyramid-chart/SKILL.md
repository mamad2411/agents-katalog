---
name: syncfusion-winui-pyramid-chart
description: Implement Syncfusion WinUI Pyramid Charts (SfPyramidChart) for visualizing hierarchical proportional data. Use this when working with pyramid charts, hierarchical visualization, or proportional data display in WinUI applications. This skill covers data binding, legend configuration, exploding segments, tooltips, data labels, selection interactions, and custom styling with palettes and gradients.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion WinUI Pyramid Charts

The Syncfusion WinUI Pyramid Chart (SfPyramidChart) is a specialized control for visualizing proportions of a total in hierarchies. It displays data in a pyramid structure where each segment represents a data point, making it ideal for showing hierarchical relationships and proportional comparisons.

## When to Use This Skill

Use this skill when the user needs to:

- **Create pyramid visualizations** - Display hierarchical or proportional data in a pyramid structure
- **Set up WinUI pyramid charts** - Install, configure, and initialize SfPyramidChart controls
- **Bind data to pyramid charts** - Configure ItemsSource, XBindingPath, YBindingPath for data binding
- **Customize appearance** - Apply colors, palettes, gradients, or custom styling to pyramid segments
- **Add interactivity** - Enable tooltips, selection, or exploding segments for user interaction
- **Configure legends** - Add and customize chart legends with icons, titles, and placement
- **Display data labels** - Show values or labels on pyramid segments
- **Advanced customization** - Configure titles, segment spacing, rendering modes, or templates

## Component Overview

The **SfPyramidChart** control provides:

- **Hierarchical visualization** - Pyramid-shaped display for proportional data
- **Rich data binding** - XAML and code-behind data binding support
- **Interactive features** - Tooltips, selection, exploding segments
- **Extensive customization** - Palettes, gradients, templates, and styling
- **Legend support** - Configurable legends with multiple placement options
- **Accessibility** - Built-in support for keyboard navigation and screen readers

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)

When you need:
- Installation and NuGet package setup (Syncfusion.Chart.WinUI)
- Namespace imports (Syncfusion.UI.Xaml.Charts)
- Basic SfPyramidChart initialization in XAML or C#
- Creating view models and data binding patterns
- Complete working example with ItemsSource, XBindingPath, YBindingPath
- First pyramid chart implementation

### Appearance and Styling
📄 **Read:** [references/appearance.md](references/appearance.md)

When you need:
- Predefined palette brushes
- Custom PaletteBrushes configuration
- Applying linear or radial gradients to segments
- Color customization and visual styling
- Creating attractive color schemes

### Legend Configuration
📄 **Read:** [references/legend.md](references/legend.md)

When you need:
- Enabling and positioning ChartLegend
- Adding legend titles (Header property)
- Customizing legend icons (size, visibility)
- Configuring item spacing and layout
- Adding checkboxes to legend items
- Implementing toggle series visibility
- Customizing legend background and borders
- Creating custom legend templates

### Data Labels
📄 **Read:** [references/data-labels.md](references/data-labels.md)

When you need:
- Enabling data labels on pyramid segments
- Positioning and formatting labels
- Creating custom label templates
- Smart label placement strategies
- Label visibility and styling

### Tooltips
📄 **Read:** [references/tooltip.md](references/tooltip.md)

When you need:
- Enabling tooltips (EnableTooltip property)
- Customizing tooltip appearance
- Creating custom tooltip templates
- Formatting tooltip content
- Interactive tooltip behavior

### Selection
📄 **Read:** [references/selection.md](references/selection.md)

When you need:
- Enabling segment selection
- Configuring selection modes
- Handling selection events
- Visual feedback for selected segments
- Multi-selection scenarios

### Exploding Segments
📄 **Read:** [references/exploding-segments.md](references/exploding-segments.md)

When you need:
- Exploding segments on touch/click
- Programmatic segment explosion
- Configuring ExplodeIndex property
- Setting ExplodeRadius for explosion distance
- Animation and visual effects for exploded segments

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)

When you need:
- Adding chart titles and headers
- Configuring segment spacing (GapRatio)
- Setting rendering modes
- Adjusting pyramid height and mode properties
- Performance optimization
- Advanced customization scenarios

## Quick Start Example

### Basic Pyramid Chart Implementation

**XAML:**
```xml
<Window
    x:Class="PyramidChartApp.MainWindow"
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    xmlns:chart="using:Syncfusion.UI.Xaml.Charts"
    xmlns:local="using:PyramidChartApp">
    
    <chart:SfPyramidChart x:Name="chart"
                          Header="Food Nutrition Pyramid"
                          ItemsSource="{Binding Data}"
                          XBindingPath="FoodName"
                          YBindingPath="Calories"
                          EnableTooltip="True"
                          ShowDataLabels="True">
        
        <chart:SfPyramidChart.DataContext>
            <local:ChartViewModel/>
        </chart:SfPyramidChart.DataContext>
        
        <chart:SfPyramidChart.Legend>
            <chart:ChartLegend/>
        </chart:SfPyramidChart.Legend>
        
    </chart:SfPyramidChart>
</Window>
```

**View Model (C#):**
```csharp
public class Model
{
    public string FoodName { get; set; }
    public double Calories { get; set; }
}

public class ChartViewModel
{
    public List<Model> Data { get; set; }
    
    public ChartViewModel()
    {
        Data = new List<Model>()
        {
            new Model { FoodName = "Sweet treats", Calories = 250 },
            new Model { FoodName = "Cheese", Calories = 402 },
            new Model { FoodName = "Vegetables", Calories = 65 },
            new Model { FoodName = "Fish", Calories = 206 },
            new Model { FoodName = "Fruits", Calories = 52 },
            new Model { FoodName = "Rice", Calories = 130 }
        };
    }
}
```

**Code-Behind (C#):**
```csharp
using Syncfusion.UI.Xaml.Charts;
using Microsoft.UI.Xaml;

public sealed partial class MainWindow : Window
{
    public MainWindow()
    {
        this.InitializeComponent();
        
        // Alternative: Create chart programmatically
        SfPyramidChart chart = new SfPyramidChart();
        ChartViewModel viewModel = new ChartViewModel();
        chart.DataContext = viewModel;
        chart.SetBinding(SfPyramidChart.ItemsSourceProperty, 
            new Binding() { Path = new PropertyPath("Data") });
        chart.XBindingPath = "FoodName";
        chart.YBindingPath = "Calories";
        chart.Header = "Food Nutrition Pyramid";
        chart.Legend = new ChartLegend();
        chart.EnableTooltip = true;
        chart.ShowDataLabels = true;
        
        this.Content = chart;
    }
}
```

## Common Patterns

### Pattern 1: Custom Color Palette

```xml
<Grid>
    <Grid.Resources>
        <BrushCollection x:Key="customColors">
            <SolidColorBrush Color="#4dd0e1"/>
            <SolidColorBrush Color="#26c6da"/>
            <SolidColorBrush Color="#00bcd4"/>
            <SolidColorBrush Color="#00acc1"/>
            <SolidColorBrush Color="#0097a7"/>
        </BrushCollection>
    </Grid.Resources>
    
    <chart:SfPyramidChart Palette="Custom"
                          PaletteBrushes="{StaticResource customColors}"
                          ItemsSource="{Binding Data}"
                          XBindingPath="Category"
                          YBindingPath="Value"/>
</Grid>
```

### Pattern 2: Interactive Pyramid with Selection

```xml
<chart:SfPyramidChart ItemsSource="{Binding Data}"
                      XBindingPath="Category"
                      YBindingPath="Value"
                      SelectionBehavior="SelectSingle">
    
    <chart:SfPyramidChart.SelectionBrush>
        <SolidColorBrush Color="#FF6B6B"/>
    </chart:SfPyramidChart.SelectionBrush>
    
</chart:SfPyramidChart>
```

### Pattern 3: Exploding Segment on Click

```xml
<chart:SfPyramidChart ItemsSource="{Binding Data}"
                      XBindingPath="Category"
                      YBindingPath="Value"
                      ExplodeOnClick="True"
                      ExplodeRadius="10"/>
```

### Pattern 4: Gradient-Styled Pyramid

```xml
<Grid>
    <Grid.Resources>
        <BrushCollection x:Key="gradientColors">
            <LinearGradientBrush>
                <GradientStop Offset="1" Color="#FFE7C7"/>
                <GradientStop Offset="0" Color="#FCB69F"/>
            </LinearGradientBrush>
            <LinearGradientBrush>
                <GradientStop Offset="1" Color="#fadd7d"/>
                <GradientStop Offset="0" Color="#fccc2d"/>
            </LinearGradientBrush>
        </BrushCollection>
    </Grid.Resources>
    
    <chart:SfPyramidChart Palette="Custom"
                          PaletteBrushes="{StaticResource gradientColors}"
                          ItemsSource="{Binding Data}"
                          XBindingPath="Category"
                          YBindingPath="Value"/>
</Grid>
```

## Key Properties

| Property | Type | Description |
|----------|------|-------------|
| **ItemsSource** | object | Data source for the pyramid chart |
| **XBindingPath** | string | Property path for X-axis data (labels) |
| **YBindingPath** | string | Property path for Y-axis data (values) |
| **Header** | object | Chart title or header content |
| **Legend** | ChartLegend | Legend configuration object |
| **EnableTooltip** | bool | Enable/disable tooltips on hover |
| **ShowDataLabels** | bool | Show/hide data labels on segments |
| **Palette** | ChartColorPalette | Predefined color palette |
| **PaletteBrushes** | IList<Brush> | Custom color collection |
| **ExplodeOnClick** | bool | Enable segment explosion on click |
| **ExplodeIndex** | int | Index of segment to explode |
| **ExplodeRadius** | double | Distance for exploded segment |
| **GapRatio** | double | Spacing between segments (0-1) |
| **SelectionBehavior** | SelectionBehavior | Selection mode configuration |

## Common Use Cases

1. **Food/Nutrition Pyramids** - Display food groups or nutritional hierarchies
2. **Sales Funnels** - Visualize sales pipeline stages from leads to conversions
3. **Population Demographics** - Show age or demographic distributions
4. **Market Segmentation** - Display market share or customer segments
5. **Cost Breakdowns** - Visualize expense categories in hierarchical order
6. **Priority Analysis** - Show task or issue priorities in descending order
7. **Resource Allocation** - Display resource distribution across categories

## Related Skills

- [Implementing Syncfusion WinUI Components](../../../) - Main WinUI components library
- For other chart types, explore the data-visualization category

---

**Next Steps:** Read the relevant reference file based on your specific needs. Start with `getting-started.md` for initial setup, or jump directly to feature-specific guides for targeted implementations.
