---
name: syncfusion-aspnetcore-heatmap-chart
description: Implementing Syncfusion HeatMap Chart component for ASP.NET Core Razor Pages. Use this skill ALWAYS when the user needs to create heat maps to visualize two-dimensional data, customize cells with gradients or fixed colors, configure axes with multiple types, add legends with flexible positioning, bind array or JSON data, enable tooltips and cell selection, create bubble heat maps, or customize appearance and styling. Essential for data visualization, pattern detection, and matrix visualization use cases.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing Syncfusion HeatMap Chart

- [When to Use This Skill](#when-to-use-this-skill)
- [Component Overview](#component-overview)
  - [Key Capabilities](#key-capabilities)
- [Documentation and Navigation Guide](#documentation-and-navigation-guide)
  - [Getting Started](#getting-started)
  - [Data Binding and Rendering Modes](#data-binding-and-rendering-modes)
  - [Bubble HeatMap Visualization](#bubble-heatmap-visualization)
  - [Appearance and Styling](#appearance-and-styling)
  - [Axis Configuration](#axis-configuration)
  - [Legend and Palette System](#legend-and-palette-system)
  - [Tooltips and Cell Selection](#tooltips-and-cell-selection)
  - [Advanced Scenarios and Best Practices](#advanced-scenarios-and-best-practices)
- [Quick Start Example](#quick-start-example)
  - [Pages/Index.cshtml](#pagesindexcshtml)
  - [Pages/Index.cshtml.cs](#pagesindexcshtmlcs)
- [Common Patterns](#common-patterns)
  - [Pattern 1: Category Axis with Labels](#pattern-1-category-axis-with-labels)
  - [Pattern 2: Gradient Color Mapping](#pattern-2-gradient-color-mapping)
  - [Pattern 3: Fixed Palette Categorization](#pattern-3-fixed-palette-categorization)
  - [Pattern 4: Responsive Rendering](#pattern-4-responsive-rendering)
- [Key Props and Configuration](#key-props-and-configuration)
  - [Required Configuration](#required-configuration)
  - [Cell Customization](#cell-customization)
  - [Appearance](#appearance)
  - [Legend Configuration](#legend-configuration)
  - [Palette](#palette)
- [Common Use Cases](#common-use-cases)

## When to Use This Skill

Use this skill when you need to:

- Visualize two-dimensional matrix data using color-coded cells.
- Display business, scientific, operational, or analytical values in a grid layout.
- Bind HeatMap data from C# collections in ASP.NET Core Razor Pages.
- Keep HeatMap markup in `Index.cshtml` and move data preparation/configuration into `Index.cshtml.cs`.
- Configure category, numeric, or date-time axes.
- Add title, legend, tooltip, cell labels, and palette customization.
- Use gradient or fixed color mapping for continuous or classified values.
- Enable cell selection and handle HeatMap events.
- Improve performance for larger datasets by using the correct rendering mode.

## Component Overview

The Syncfusion ASP.NET Core HeatMap Chart is a data visualization component used to represent two-dimensional data through color intensity. Each cell represents a value, and the color of that cell is calculated from the configured palette.

It is useful for:

- Sales performance matrices.
- Attendance and productivity reports.
- Correlation matrices.
- Temperature or density visualization.
- Inventory status dashboards.
- Sensor reading grids.
- Usage or activity analysis over time.

### Key Capabilities

- Supports array and JSON-style data binding.
- Supports category, numeric, and date-time axes.
- Supports gradient and fixed palettes.
- Supports cell labels, legends, and tooltips.
- Supports SVG, Canvas, and Auto rendering modes.
- Supports single and multiple cell selection.
- Supports event customization such as cell render, tooltip render, and cell selected.
- Supports Razor Pages implementation with `Index.cshtml` and `Index.cshtml.cs`.

## Documentation and Navigation Guide

### Getting Started

Use this section for:

- Installing the required Syncfusion ASP.NET Core package.
- Registering Syncfusion Tag Helpers.
- Adding Syncfusion styles and scripts.
- Creating the first HeatMap Chart.
- Rendering the component in Razor Pages.

Required setup in `Pages/_ViewImports.cshtml`:

```cshtml
@using YourApplication
@namespace YourApplication.Pages
@addTagHelper *, Microsoft.AspNetCore.Mvc.TagHelpers
@addTagHelper *, Syncfusion.EJ2
```

Replace `YourApplication` with the actual project namespace. For example, if the project name is `AspNetCoreWebApp`, use:

```cshtml
@using AspNetCoreWebApp
@namespace AspNetCoreWebApp.Pages
@addTagHelper *, Microsoft.AspNetCore.Mvc.TagHelpers
@addTagHelper *, Syncfusion.EJ2
```

Add the required theme and script references in `Pages/Shared/_Layout.cshtml` inside the `head` tag.

```html
<link rel="stylesheet" href="https://cdn.syncfusion.com/ej2/33.2.3/fluent.css" />
<script src="https://cdn.syncfusion.com/ej2/33.2.3/dist/ej2.min.js"></script>
```

Add the Syncfusion script manager before the closing `body` tag in `Pages/Shared/_Layout.cshtml`.

```cshtml
<ejs-scripts></ejs-scripts>
```

### Data Binding and Rendering Modes

The HeatMap Chart can bind data in multiple forms:

- Two-dimensional array data.
- JSON table data.
- JSON cell data.
- Remote data.
- Strongly typed C# model collections.

For Razor Pages, the recommended approach is to keep data and configuration objects in `Index.cshtml.cs` and bind them in `Index.cshtml` through `@Model`.

Rendering modes:

- `SVG`: Best for small and moderate datasets.
- `Canvas`: Best for large datasets.
- `Auto`: Lets the component choose the suitable rendering mode.

### Bubble HeatMap Visualization

Bubble HeatMap is useful when the cell should show values through bubble size, color, or both.

Common bubble options:

- Bubble by size.
- Bubble by color.
- Bubble by sector.
- Bubble by size and color.

Use bubble HeatMap when each cell needs more visual differentiation than a plain rectangular tile.

### Appearance and Styling

The HeatMap appearance can be customized using:

- `titleSettings`
- `cellSettings`
- `paletteSettings`
- `legendSettings`
- `tooltipSettings`
- `backgroundColor`
- `margin`
- `height`
- `width`

For ASP.NET Core Razor Pages, strongly typed objects should be declared in `Index.cshtml.cs` and passed to the Tag Helper from `Index.cshtml`.

### Axis Configuration

The HeatMap Chart supports these axis value types:

- `Category`
- `Numeric`
- `DateTime`

Use category axes when labels are names such as months, products, regions, or departments.

Use numeric axes when X and Y values are index-based or numeric ranges.

Use date-time axes when values represent dates or time intervals.

### Legend and Palette System

Use legends to explain how colors map to values.

Palette types:

- `Gradient`: Best for continuous values.
- `Fixed`: Best for classified values or thresholds.

Legend positions:

- `Right`
- `Left`
- `Top`
- `Bottom`

### Tooltips and Cell Selection

Tooltips can be enabled using `showTooltip="true"` on the HeatMap.

Tooltip style can be customized with `tooltipSettings`.

Cell selection can be enabled using:

```cshtml
allowSelection="true"
enableMultiSelect="true"
```

Use events such as `cellSelected`, `cellClick`, and `tooltipRender` when custom interaction logic is required.

### Advanced Scenarios and Best Practices

Recommended best practices:

- Keep only UI markup in `Index.cshtml`.
- Keep data, palettes, font styles, labels, and strongly typed models in `Index.cshtml.cs`.
- Use `@Model.PropertyName` for all Razor Page bindings.
- Use `renderingMode="Auto"` for responsive performance behavior.
- Use `showLabel="false"` for very large datasets.
- Use strongly typed classes instead of anonymous objects when the data is reused.
- Use `dataSourceSettings` when JSON-style cell mapping is required.
- Keep the namespace in `Index.cshtml.cs`, `Index.cshtml`, and `_ViewImports.cshtml` consistent.
- Use real Razor/HTML tags in `.cshtml` files. Do not paste encoded tags like `&lt;ejs-heatmap&gt;` into the actual Razor file.

## Quick Start Example

The following example demonstrates a complete ASP.NET Core Razor Pages HeatMap Chart implementation using both `Index.cshtml` and `Index.cshtml.cs`.

This version keeps the Razor file clean and moves data generation, palette configuration, title styling, tooltip styling, and labels into the PageModel.

Replace `YourApplication` with your actual project namespace. For example, if your project is named `AspNetCoreWebApp`, use `AspNetCoreWebApp.Pages`.

### Pages/Index.cshtml

```cshtml
@page
@model YourApplication.Pages.IndexModel

<ejs-heatmap
    id="heatmap"
    dataSource="@Model.DataSource"
    showTooltip="true"
    renderingMode="Auto"
    allowSelection="true"
    enableMultiSelect="true">

    <e-heatmap-titlesettings
        text="Sales Performance HeatMap"
        textStyle="@Model.TitleTextStyle">
    </e-heatmap-titlesettings>

    <e-heatmap-xaxis
        valueType="Category"
        labels="@Model.XAxisLabels">
    </e-heatmap-xaxis>

    <e-heatmap-yaxis
        valueType="Category"
        labels="@Model.YAxisLabels">
    </e-heatmap-yaxis>

    <e-heatmap-datasourcesettings
        isJsonData="true"
        adaptorType="Cell"
        xDataMapping="XValue"
        yDataMapping="YValue"
        valueMapping="Value">
    </e-heatmap-datasourcesettings>

    <e-heatmap-cellsettings
        showLabel="true"
        format="{value}"
        textStyle="@Model.CellTextStyle">
    </e-heatmap-cellsettings>

    <e-heatmap-palettesettings
        type="Gradient"
        palette="@Model.Palette">
    </e-heatmap-palettesettings>

    <e-heatmap-legendsettings
        visible="true"
        position="Right"
        showLabel="true"
        height="150">
    </e-heatmap-legendsettings>

    <e-heatmap-tooltipsettings
        textStyle="@Model.TooltipTextStyle">
    </e-heatmap-tooltipsettings>
</ejs-heatmap>
```

### Pages/Index.cshtml.cs

```csharp
using Microsoft.AspNetCore.Mvc.RazorPages;
using Syncfusion.EJ2.HeatMap;
using System.Collections.Generic;

namespace YourApplication.Pages
{
    public class IndexModel : PageModel
    {
        public List<HeatMapDataPoint> DataSource { get; set; } = new List<HeatMapDataPoint>();

        public string[] XAxisLabels { get; set; } =
        {
            "Jan", "Feb", "Mar", "Apr", "May"
        };

        public string[] YAxisLabels { get; set; } =
        {
            "Product A", "Product B", "Product C", "Product D", "Product E"
        };

        public HeatMapFont TitleTextStyle { get; set; } = new HeatMapFont
        {
            Size = "15px",
            FontWeight = "500",
            FontStyle = "Normal",
            FontFamily = "Segoe UI"
        };

        public HeatMapFont CellTextStyle { get; set; } = new HeatMapFont
        {
            FontFamily = "Segoe UI",
            Size = "12px",
            FontWeight = "400"
        };

        public HeatMapFont TooltipTextStyle { get; set; } = new HeatMapFont
        {
            Color = "#FFFFFF",
            FontFamily = "Segoe UI"
        };

        public List<HeatMapPalette> Palette { get; set; } = new List<HeatMapPalette>
        {
            new HeatMapPalette { Value = 0, Color = "#C2E7EC", Label = "Very Low" },
            new HeatMapPalette { Value = 25, Color = "#AED6DC", Label = "Low" },
            new HeatMapPalette { Value = 50, Color = "#87C1C9", Label = "Medium" },
            new HeatMapPalette { Value = 75, Color = "#4CA3AF", Label = "High" },
            new HeatMapPalette { Value = 100, Color = "#1B7280", Label = "Very High" }
        };

        public List<HeatMapPalette> FixedPalette { get; set; } = new List<HeatMapPalette>
        {
            new HeatMapPalette { Value = 0, Color = "#DFF6DD", Label = "Low" },
            new HeatMapPalette { Value = 50, Color = "#FFF4CE", Label = "Medium" },
            new HeatMapPalette { Value = 80, Color = "#FDE7E9", Label = "High" }
        };

        public void OnGet()
        {
            DataSource = new List<HeatMapDataPoint>
            {
                new HeatMapDataPoint { XValue = "Jan", YValue = "Product A", Value = 73 },
                new HeatMapDataPoint { XValue = "Feb", YValue = "Product A", Value = 39 },
                new HeatMapDataPoint { XValue = "Mar", YValue = "Product A", Value = 26 },
                new HeatMapDataPoint { XValue = "Apr", YValue = "Product A", Value = 39 },
                new HeatMapDataPoint { XValue = "May", YValue = "Product A", Value = 94 },

                new HeatMapDataPoint { XValue = "Jan", YValue = "Product B", Value = 93 },
                new HeatMapDataPoint { XValue = "Feb", YValue = "Product B", Value = 58 },
                new HeatMapDataPoint { XValue = "Mar", YValue = "Product B", Value = 53 },
                new HeatMapDataPoint { XValue = "Apr", YValue = "Product B", Value = 38 },
                new HeatMapDataPoint { XValue = "May", YValue = "Product B", Value = 26 },

                new HeatMapDataPoint { XValue = "Jan", YValue = "Product C", Value = 99 },
                new HeatMapDataPoint { XValue = "Feb", YValue = "Product C", Value = 28 },
                new HeatMapDataPoint { XValue = "Mar", YValue = "Product C", Value = 22 },
                new HeatMapDataPoint { XValue = "Apr", YValue = "Product C", Value = 4 },
                new HeatMapDataPoint { XValue = "May", YValue = "Product C", Value = 66 },

                new HeatMapDataPoint { XValue = "Jan", YValue = "Product D", Value = 14 },
                new HeatMapDataPoint { XValue = "Feb", YValue = "Product D", Value = 26 },
                new HeatMapDataPoint { XValue = "Mar", YValue = "Product D", Value = 97 },
                new HeatMapDataPoint { XValue = "Apr", YValue = "Product D", Value = 69 },
                new HeatMapDataPoint { XValue = "May", YValue = "Product D", Value = 69 },

                new HeatMapDataPoint { XValue = "Jan", YValue = "Product E", Value = 7 },
                new HeatMapDataPoint { XValue = "Feb", YValue = "Product E", Value = 46 },
                new HeatMapDataPoint { XValue = "Mar", YValue = "Product E", Value = 47 },
                new HeatMapDataPoint { XValue = "Apr", YValue = "Product E", Value = 47 },
                new HeatMapDataPoint { XValue = "May", YValue = "Product E", Value = 88 }
            };
        }
    }

    public class HeatMapDataPoint
    {
        public string XValue { get; set; } = string.Empty;

        public string YValue { get; set; } = string.Empty;

        public double Value { get; set; }
    }
}
```

## Common Patterns

### Pattern 1: Category Axis with Labels

Use category axes when displaying named row and column headers such as months, products, teams, regions, or departments.

Recommended usage:

- Set `valueType="Category"` for the required axis.
- Provide labels from `Index.cshtml.cs` as `string[]`.
- Bind labels in `Index.cshtml` using `@Model.XAxisLabels` and `@Model.YAxisLabels`.

Example configuration in `Index.cshtml`:

```cshtml
<e-heatmap-xaxis
    valueType="Category"
    labels="@Model.XAxisLabels">
</e-heatmap-xaxis>

<e-heatmap-yaxis
    valueType="Category"
    labels="@Model.YAxisLabels">
</e-heatmap-yaxis>
```

Example configuration in `Index.cshtml.cs`:

```csharp
public string[] XAxisLabels { get; set; } =
{
    "Jan", "Feb", "Mar", "Apr", "May"
};

public string[] YAxisLabels { get; set; } =
{
    "Product A", "Product B", "Product C", "Product D", "Product E"
};
```

### Pattern 2: Gradient Color Mapping

Use gradient color mapping when values are continuous and should be interpolated between multiple color stops.

Recommended usage:

- Set `type="Gradient"` in `paletteSettings`.
- Define the palette as `List<HeatMapPalette>` in `Index.cshtml.cs`.
- Use this for scores, density, temperature, traffic intensity, utilization, or performance values.

Example configuration in `Index.cshtml`:

```cshtml
<e-heatmap-palettesettings
    type="Gradient"
    palette="@Model.Palette">
</e-heatmap-palettesettings>
```

Example configuration in `Index.cshtml.cs`:

```csharp
public List<HeatMapPalette> Palette { get; set; } = new List<HeatMapPalette>
{
    new HeatMapPalette { Value = 0, Color = "#C2E7EC", Label = "Very Low" },
    new HeatMapPalette { Value = 25, Color = "#AED6DC", Label = "Low" },
    new HeatMapPalette { Value = 50, Color = "#87C1C9", Label = "Medium" },
    new HeatMapPalette { Value = 75, Color = "#4CA3AF", Label = "High" },
    new HeatMapPalette { Value = 100, Color = "#1B7280", Label = "Very High" }
};
```

### Pattern 3: Fixed Palette Categorization

Use fixed palette mapping when values represent discrete ranges, statuses, or classification levels.

Recommended usage:

- Set `type="Fixed"` in `paletteSettings`.
- Define the palette as `List<HeatMapPalette>` in `Index.cshtml.cs`.
- Ensure the property name used in the Razor file exists in the PageModel.
- Use this for risk levels, availability states, SLA status, or category-based heat maps.

Yes, the following snippet will work only if `FixedPalette` exists in `Index.cshtml.cs` and the snippet is pasted as real tags in a `.cshtml` file.

Correct usage in `Index.cshtml`:

```cshtml
<e-heatmap-palettesettings
    type="Fixed"
    palette="@Model.FixedPalette">
</e-heatmap-palettesettings>
```

Do not paste the encoded version below into the actual `.cshtml` file:

```html
&lt;e-heatmap-palettesettings
    type="Fixed"
    palette="@Model.FixedPalette"&gt;
&lt;/e-heatmap-palettesettings&gt;
```

Required property in `Index.cshtml.cs`:

```csharp
public List<HeatMapPalette> FixedPalette { get; set; } = new List<HeatMapPalette>
{
    new HeatMapPalette { Value = 0, Color = "#DFF6DD", Label = "Low" },
    new HeatMapPalette { Value = 50, Color = "#FFF4CE", Label = "Medium" },
    new HeatMapPalette { Value = 80, Color = "#FDE7E9", Label = "High" }
};
```

If you want to use the fixed palette in the main quick start sample, replace this block:

```cshtml
<e-heatmap-palettesettings
    type="Gradient"
    palette="@Model.Palette">
</e-heatmap-palettesettings>
```

with this block:

```cshtml
<e-heatmap-palettesettings
    type="Fixed"
    palette="@Model.FixedPalette">
</e-heatmap-palettesettings>
```

### Pattern 4: Responsive Rendering

Use responsive rendering practices when working with medium or large datasets.

Recommended usage:

- Use `renderingMode="SVG"` for smaller datasets.
- Use `renderingMode="Canvas"` for large datasets.
- Use `renderingMode="Auto"` when the component should determine the suitable rendering mode.
- Disable labels for high-density data.
- Avoid complex label templates for thousands of cells.

Example configuration in `Index.cshtml`:

```cshtml
<ejs-heatmap
    id="heatmap"
    dataSource="@Model.DataSource"
    renderingMode="Auto">

    <e-heatmap-cellsettings
        showLabel="false">
    </e-heatmap-cellsettings>
</ejs-heatmap>
```

## Key Props and Configuration

### Required Configuration

- `dataSource`: Assigns the data collection to the HeatMap.
- `xAxis.valueType`: Defines the X-axis value type. Common values are `Category`, `Numeric`, and `DateTime`.
- `yAxis.valueType`: Defines the Y-axis value type. Common values are `Category`, `Numeric`, and `DateTime`.
- `dataSourceSettings`: Required when using JSON-style object mapping.
- `dataSourceSettings.isJsonData`: Set this to `true` when binding object collections.
- `dataSourceSettings.adaptorType`: Use `Cell` for cell-based records.
- `dataSourceSettings.xDataMapping`: Maps the X value field.
- `dataSourceSettings.yDataMapping`: Maps the Y value field.
- `dataSourceSettings.valueMapping`: Maps the cell value field.

### Cell Customization

- `cellSettings.showLabel`: Displays values inside cells.
- `cellSettings.format`: Formats the displayed cell value.
- `cellSettings.textStyle`: Customizes label font style.
- `cellSettings.tileType`: Defines the tile type, such as rectangular cell or bubble cell.

### Appearance

- `backgroundColor`: Defines the HeatMap background color.
- `margin`: Defines spacing around the HeatMap.
- `titleSettings.text`: Defines the HeatMap title.
- `titleSettings.textStyle`: Defines the title font style.
- `height`: Defines the component height.
- `width`: Defines the component width.

### Legend Configuration

- `legendSettings.visible`: Shows or hides the legend.
- `legendSettings.position`: Defines the legend position.
- `legendSettings.type`: Defines the legend type.
- `legendSettings.showLabel`: Shows or hides legend labels.
- `legendSettings.height`: Defines legend height.
- `legendSettings.width`: Defines legend width.
- `legendSettings.toggleVisibility`: Enables legend-based visibility toggling when applicable.

### Palette

- `paletteSettings.type`: Defines palette behavior. Common values are `Gradient` and `Fixed`.
- `paletteSettings.palette`: Assigns the strongly typed `List<HeatMapPalette>`.
- `HeatMapPalette.Value`: Defines the value threshold.
- `HeatMapPalette.Color`: Defines the color for the threshold.
- `HeatMapPalette.Label`: Defines the label for the palette item.

## Common Use Cases

1. Employee performance matrix across months and departments.
2. Product sales comparison by region and time period.
3. Website traffic or usage intensity visualization.
4. Correlation matrix for analytical dashboards.
5. Temperature distribution across locations and time slots.
6. Inventory status by warehouse and product.
7. User activity analysis across days and hours.
8. Sensor readings from multiple devices.
9. Risk level visualization by category.
10. SLA or ticket volume analysis.