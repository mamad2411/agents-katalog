---
name: syncfusion-aspnetcore-treemap
description: Implement interactive hierarchical TreeMap visualizations in ASP.NET Core using Syncfusion. Create tree maps for hierarchical data with multiple layouts, color mapping, drill-down capabilities, and interactive features. Use this skill whenever the user needs to visualize hierarchical data structures, display nested categories with relative sizes, implement interactive drill-down navigation, or enable data exploration through tree maps.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion TreeMap in ASP.NET Core

The Syncfusion TreeMap control visualizes hierarchical data using nested rectangles, where each item's area represents its numeric value. It is suitable for displaying organizational structures, budget distributions, market segments, population distribution, sales performance, or any hierarchical dataset that requires size-based visual representation.


## Table of Contents
- [When to Use This Skill](#when-to-use-this-skill)
- [Component Overview](#component-overview)
- [Documentation and Navigation Guide](#documentation-and-navigation-guide)
  - [Getting Started](#getting-started)
  - [Data Organization](#data-organization)
  - [Visual Layouts](#visual-layouts)
  - [Hierarchical Organization](#hierarchical-organization)
  - [Leaf Items Leaf-Level Display](#leaf-items-leaf-level-display)
  - [Color Mapping Strategies](#color-mapping-strategies)
  - [Data Display Labels -- Tooltips](#data-display-labels---tooltips)
  - [Interactive Features](#interactive-features)
  - [Publishing -- Accessibility](#publishing---accessibility)
  - [Advanced Customization](#advanced-customization)
- [Quick Start Example](#quick-start-example)
- [Common Patterns](#common-patterns)
  - [Pattern 1 Multi-Level Hierarchy with Headers](#pattern-1-multi-level-hierarchy-with-headers)
  - [Pattern 2 Range-Based Color Mapping](#pattern-2-range-based-color-mapping)
  - [Pattern 3 Interactive Drill-Down with Breadcrumbs](#pattern-3-interactive-drill-down-with-breadcrumbs)
- [Key Properties](#key-properties)
- [Next Steps](#next-steps)
- [Combined Mistakes and Future References](#combined-mistakes-and-future-references)

## When to Use This Skill

Use the TreeMap skill when you need to:

- **Visualize hierarchical data** with multiple levels, such as continent → country → city.
- **Display nested categories** where rectangle size represents a numeric value.
- **Enable drill-down exploration** to let users navigate through hierarchy levels.
- **Apply color mapping** to show value ranges, categories, or performance metrics.
- **Add interactive features** such as selection, highlight, tooltip, and legend.
- **Create multi-level displays** with custom headers, grouping, and label formatting.

## Component Overview

The TreeMap control renders hierarchical data as nested rectangles using SVG. It supports:

- **Multiple layout types** such as Squarified, SliceAndDiceVertical, SliceAndDiceHorizontal, and SliceAndDiceAuto.
- **Hierarchical levels** using `groupPath` to organize flat data into visual groups.
- **Color mapping** using range-based, equal/category-based, desaturation, opacity, or palette-based configuration.
- **Interactive drill-down** for navigating from parent groups into child groups.
- **Data labels and tooltips** to display contextual information.
- **Selection and highlight** modes for user interaction.
- **Print and export** capabilities for PNG, JPEG, SVG, and PDF output.
- **Accessibility support** for keyboard interaction and screen-reader-friendly rendering.

## Documentation and Navigation Guide

### Getting Started

📄 **Read:** [references/getting-started.md](references/getting-started.md)

- Installation and package setup
- Registering Syncfusion services in ASP.NET Core
- Creating your first TreeMap control
- Basic data binding and rendering
- Common initial configuration

### Data Organization

📄 **Read:** [references/data-binding.md](references/data-binding.md)

- Flat collection data binding
- Hierarchical collection data binding
- Data source field mapping patterns
- Data structure best practices
- Mapping the value field through `weightValuePath`

### Visual Layouts

📄 **Read:** [references/layouts.md](references/layouts.md)

- Layout types such as Squarified and Slice-and-Dice variants
- Choosing the right layout for your data
- Right-to-left rendering support
- Rendering direction and layout behavior

### Hierarchical Organization

📄 **Read:** [references/levels-and-hierarchy.md](references/levels-and-hierarchy.md)

- Multi-level hierarchies with `groupPath`
- Header customization with `headerFormat`
- Group gaps and spacing
- Header templates and positioning

### Leaf Items (Leaf-Level Display)

📄 **Read:** [references/leaf-items.md](references/leaf-items.md)

- Leaf item rendering and appearance
- Label positioning and formatting
- Label templates and customization
- Item gaps and spacing

### Color Mapping Strategies

📄 **Read:** [references/color-mapping.md](references/color-mapping.md)

- Range color mapping for continuous numeric values
- Equal color mapping for discrete categories
- Desaturation and opacity-based mapping
- Palette and direct color binding from data

### Data Display (Labels & Tooltips)

📄 **Read:** [references/data-labels-and-tooltips.md](references/data-labels-and-tooltips.md)

- Data label formatting and templates
- Label intersection handling
- Tooltip visibility and formatting
- Tooltip templates and custom content

### Interactive Features

📄 **Read:** [references/interactive-features.md](references/interactive-features.md)

- Selection modes and customization
- Highlight behavior and styling
- Drill-down functionality
- Breadcrumb-style navigation behavior
- On-demand data loading patterns for performance

### Publishing & Accessibility

📄 **Read:** [references/print-export-accessibility.md](references/print-export-accessibility.md)

- Print functionality
- Image export as PNG, JPEG, and SVG
- PDF export with orientation settings
- Base64 export for programmatic use
- Accessibility and screen reader support

### Advanced Customization

📄 **Read:** [references/advanced-customization.md](references/advanced-customization.md)

- Internationalization and number formatting
- Legend customization and interactive modes
- Real-world customization patterns
- Migration guidance from older APIs

## Quick Start Example

```cshtml
@page
@using Syncfusion.EJ2.TreeMap

@{
    List<TreeMapData> data = new List<TreeMapData>
    {
        new TreeMapData { Name = "Electronics", Category = "Tech", Sales = 5000 },
        new TreeMapData { Name = "Furniture", Category = "Home", Sales = 3000 }
    };

    ViewBag.data = data;
}

<ejs-treemap id="treemap"
             dataSource="ViewBag.data"
             weightValuePath="Sales"
             layoutType="Squarified">
    <e-treemap-leafitemsettings labelPath="Name">
    </e-treemap-leafitemsettings>
    <e-treemap-levels>
        <e-treemap-level groupPath="Category"
                         headerFormat="${Category}"
                         fill="#336699">
        </e-treemap-level>
    </e-treemap-levels>
</ejs-treemap>

@functions {
    public class TreeMapData
    {
        public string Name { get; set; }
        public string Category { get; set; }
        public double Sales { get; set; }
    }
}
```

## Common Patterns

### Pattern 1: Multi-Level Hierarchy with Headers

Create a 3-level TreeMap showing continent → country → city with formatted headers:

```cshtml
@page
@{
    List<PopulationData> populationData = new List<PopulationData>
    {
        new PopulationData { Continent = "Asia", Country = "India", City = "Chennai", Population = 12000000 },
        new PopulationData { Continent = "Asia", Country = "India", City = "Mumbai", Population = 20000000 },
        new PopulationData { Continent = "Europe", Country = "Germany", City = "Berlin", Population = 3600000 }
    };

    ViewBag.populationData = populationData;
}

<ejs-treemap id="treemap"
             dataSource="ViewBag.populationData"
             weightValuePath="Population"
             layoutType="Squarified">
    <e-treemap-leafitemsettings labelPath="City">
    </e-treemap-leafitemsettings>
    <e-treemap-levels>
        <e-treemap-level groupPath="Continent"
                         headerFormat="${Continent}">
        </e-treemap-level>
        <e-treemap-level groupPath="Country"
                         headerFormat="${Country}">
        </e-treemap-level>
    </e-treemap-levels>
</ejs-treemap>

@functions {
    public class PopulationData
    {
        public string Continent { get; set; }
        public string Country { get; set; }
        public string City { get; set; }
        public double Population { get; set; }
    }
}
```

### Pattern 2: Range-Based Color Mapping

Apply colors based on value ranges, such as low, medium, and high sales performance:

```cshtml
@page
@{
    List<SalesData> salesData = new List<SalesData>
    {
        new SalesData { Name = "Electronics", Category = "Technology", Sales = 4500 },
        new SalesData { Name = "Furniture", Category = "Home", Sales = 8500 },
        new SalesData { Name = "Appliances", Category = "Home", Sales = 12500 }
    };

    ViewBag.salesData = salesData;
}

<ejs-treemap id="treemap"
             dataSource="ViewBag.salesData"
             weightValuePath="Sales"
             rangeColorValuePath="Sales"
             layoutType="Squarified">
    <e-treemap-leafitemsettings labelPath="Name">
        <e-leafitemsettings-colormappings>
            <e-leafitemsettings-colormapping From="0"
                                             To="5000"
                                             Color=@("#66BB6A")>
            </e-leafitemsettings-colormapping>
            <e-leafitemsettings-colormapping From="5000"
                                             To="10000"
                                             Color=@("#FDD835")>
            </e-leafitemsettings-colormapping>
            <e-leafitemsettings-colormapping From="10000"
                                             To="15000"
                                             Color=@("#EF5350")>
            </e-leafitemsettings-colormapping>
        </e-leafitemsettings-colormappings>
    </e-treemap-leafitemsettings>
</ejs-treemap>

@functions {
    public class SalesData
    {
        public string Name { get; set; }
        public string Category { get; set; }
        public double Sales { get; set; }
    }
}
```

### Pattern 3: Interactive Drill-Down with Breadcrumbs

Enable hierarchical exploration by configuring `enableDrillDown` and hierarchical levels:

```cshtml
@page
@{
    List<DrillDownData> drillDownData = new List<DrillDownData>
    {
        new DrillDownData { Continent = "Asia", Country = "India", State = "Tamil Nadu", Name = "Chennai", Sales = 7000 },
        new DrillDownData { Continent = "Asia", Country = "India", State = "Maharashtra", Name = "Mumbai", Sales = 9000 },
        new DrillDownData { Continent = "Europe", Country = "Germany", State = "Berlin", Name = "Berlin City", Sales = 6000 }
    };

    ViewBag.drillDownData = drillDownData;
}

<ejs-treemap id="treemap"
             dataSource="ViewBag.drillDownData"
             weightValuePath="Sales"
             enableDrillDown="true"
             layoutType="Squarified">
    <e-treemap-leafitemsettings labelPath="Name">
    </e-treemap-leafitemsettings>
    <e-treemap-levels>
        <e-treemap-level groupPath="Continent"
                         headerFormat="${Continent}">
        </e-treemap-level>
        <e-treemap-level groupPath="Country"
                         headerFormat="${Country}">
        </e-treemap-level>
        <e-treemap-level groupPath="State"
                         headerFormat="${State}">
        </e-treemap-level>
    </e-treemap-levels>
</ejs-treemap>

@functions {
    public class DrillDownData
    {
        public string Continent { get; set; }
        public string Country { get; set; }
        public string State { get; set; }
        public string Name { get; set; }
        public double Sales { get; set; }
    }
}
```

## Key Properties

- **`dataSource`** - Specifies the data collection used to render the TreeMap.
- **`weightValuePath`** - Maps the numeric field used to calculate rectangle size.
- **`layoutType`** - Defines the layout algorithm, such as `Squarified`, `SliceAndDiceVertical`, `SliceAndDiceHorizontal`, or `SliceAndDiceAuto`.
- **`rangeColorValuePath`** - Maps the numeric field used for range-based color mapping.
- **`equalColorValuePath`** - Maps the field used for equal/category-based color mapping.
- **`enableDrillDown`** - Enables hierarchical drill-down navigation.
- **`enableRtl`** - Enables right-to-left rendering support.
- **`levels`** - Defines hierarchical grouping using one or more `groupPath` levels.
- **`leafItemSettings`** - Configures leaf item appearance, including labels, gaps, templates, and color mapping.
- **`colorMapping`** - Defines rules for applying colors based on value ranges, equal values, opacity, or desaturation.

## Next Steps

1. Choose the **layout type** based on your data shape and readability requirements.
2. Prepare the **data structure** as either flat data with grouping fields or hierarchical data.
3. Configure **`weightValuePath`** to represent the numeric value used for rectangle sizing.
4. Configure **color mapping** to visualize metrics, categories, or performance ranges.
5. Add **interactive features** such as drill-down, selection, highlight, tooltip, and legend.
6. Customize **labels, headers, and formatting** for better readability.
7. Enable **accessibility and export options** when required for production use.