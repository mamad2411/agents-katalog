---
name: syncfusion-aspnetcore-range-navigator
description: Implement Syncfusion RangeNavigator (Range Selector) in ASP.NET Core applications for interactive data range selection and navigation. Use this skill when user needs to select data ranges, visualize time-series data with interactive sliders, add period selectors, customize range appearance, export range visualizations, or integrate range selection into dashboards and charts.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion ASP.NET Core RangeNavigator

The RangeNavigator is a data visualization control that allows users to select and navigate through data ranges using interactive thumbs and sliders. It integrates seamlessly with charts, grids, and dashboards to create rich, interactive data exploration experiences.

## When to Use This Skill

Use the RangeNavigator component when you need to:

- **Select date/time ranges** - Let users pick specific time periods from large datasets
- **Navigate large datasets** - Provide scroll and range selection capabilities for big data
- **Visualize time-series data** - Display charts or series within a selectable range
- **Add period buttons** - Offer quick pre-defined time intervals (1D, 5D, 1M, 3M, 6M, 1Y)
- **Create lightweight selectors** - Display range selection without chart visualization
- **Customize appearance** - Style thumbs, borders, colors, and animations
- **Export visualizations** - Generate images or PDFs of range visualizations
- **Support accessibility** - Ensure screen reader support

## Component Overview

The RangeNavigator provides:

- **Multiple data types:** Numeric, DateTime, and Logarithmic scales
- **Three series types:** Line, Area, and StepLine
- **Interactive range selection:** Drag thumbs, tap labels, or set programmatically
- **Period selector:** Quick buttons for common date intervals
- **Customization options:** Colors, sizes, animations, RTL support
- **Export/Print:** JPEG, PNG, SVG, PDF formats
- **Accessibility:** WCAG 2.2 AA compliant, screen reader support

## Navigation and Documentation Guide

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Complete API documentation for RangeNavigator component
- Constructor and property definitions
- Event properties and callbacks
- Configuration options and usage patterns
- Related settings classes

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- NuGet package installation
- ASP.NET Core project setup
- Tag helper registration
- Script references and script manager
- Basic RangeNavigator implementation
- Data binding with series

### Data Binding and Series Types
📄 **Read:** [references/data-binding-and-series.md](references/data-binding-and-series.md)
- Numeric scale configuration
- DateTime scale support
- Logarithmic scale
- Series types (Line, Area, StepLine)
- Data source binding
- X/Y field mapping

### Range Selection and Values
📄 **Read:** [references/range-and-values.md](references/range-and-values.md)
- Range selection methods (drag, tap, programmatic)
- Value property configuration
- Value types and scales
- Min/Max settings
- Deferred updates
- Snapping behavior

### Period Selector Configuration
📄 **Read:** [references/period-selector.md](references/period-selector.md)
- Period selector setup
- Interval types and counts
- Positioning (Top/Bottom)
- Height customization
- Visibility control

### Labels, Grid Lines, and Axis
📄 **Read:** [references/labels-and-axis.md](references/labels-and-axis.md)
- Multi-level labels with grouping
- Label positioning and formatting
- Smart label management
- Grid line customization
- Tick line customization
- Interval configuration

### Tooltips and Interactions
📄 **Read:** [references/tooltip-and-interactions.md](references/tooltip-and-interactions.md)
- Tooltip enable/disable
- Tooltip customization (colors, opacity, fonts)
- Tooltip label formatting
- Animation duration
- Accessibility features

### Customization and Appearance
📄 **Read:** [references/customization-and-appearance.md](references/customization-and-appearance.md)
- Navigator colors (selected/unselected regions)
- Thumb customization (shape, size, color)
- Border customization
- RTL (right-to-left) support
- Lightweight mode
- Theme selection

### Export, Print, and Advanced
📄 **Read:** [references/export-print-and-advanced.md](references/export-print-and-advanced.md)
- Export to image formats (JPEG, PNG, SVG, PDF)
- Print functionality
- API migration from EJ1 to EJ2
- Accessibility standards compliance

## Quick Start Example

```cshtml
<!-- Basic RangeNavigator with DateTime data -->
<ejs-rangenavigator id="rangeNavigator" 
    valueType="DateTime" 
    width="100%" 
    height="150px">
    <e-rangenavigator-rangenavigatorseriescollection>
        <e-rangenavigator-rangenavigatorseries 
            datasource="ViewBag.Data" 
            xName="x" 
            yName="y" 
            type="Area">
        </e-rangenavigator-rangenavigatorseries>
    </e-rangenavigator-rangenavigatorseriescollection>
</ejs-rangenavigator>
```

**C# Code-behind:**
```csharp
public class IndexModel
{
    public void OnGet()
    {
        ViewBag.Data = GetChartData();
    }
    
    public List<RangeData> GetChartData()
    {
        return new List<RangeData>
        {
            new RangeData { x = new DateTime(2005, 1, 1), y = 21 },
            new RangeData { x = new DateTime(2005, 2, 1), y = 24 },
            new RangeData { x = new DateTime(2005, 3, 1), y = 36 }
        };
    }
}

public class RangeData
{
    public DateTime x { get; set; }
    public double y { get; set; }
}
```

## Common Patterns

### Pattern 1: RangeNavigator with Period Selector

Quick buttons for common date ranges (1D, 5D, 1M, 3M, 6M, 1Y):

```cshtml
<ejs-rangenavigator valueType="DateTime" width="100%" height="150px" id="PeriodSelector">
    <e-rangenavigator-periodselectorsettings>
        <e-periods>
            <e-period interval="1" intervalType="Days" text="1D"></e-period>
            <e-period interval="5" intervalType="Days" text="5D"></e-period>
            <e-period interval="1" intervalType="Months" text="1M"></e-period>
            <e-period interval="3" intervalType="Months" text="3M"></e-period>
            <e-period interval="6" intervalType="Months" text="6M"></e-period>
            <e-period interval="1" intervalType="Years" text="1Y"></e-period>
        </e-periods>
    </e-rangenavigator-periodselectorsettings>
    <e-rangenavigator-rangenavigatorseriescollection>
        <e-rangenavigator-rangenavigatorseries datasource="ViewBag.Data" xName="x" yName="y" type="Area"></e-rangenavigator-rangenavigatorseries>
    </e-rangenavigator-rangenavigatorseriescollection>
</ejs-rangenavigator>
```

### Pattern 2: Lightweight Range Selector (No Chart)

Display range selection without data visualization:

```cshtml
<ejs-rangenavigator valueType="DateTime" 
    minimum="new DateTime(2018, 1, 1)" 
    maximum="new DateTime(2018, 12, 31)"
    datasource="ViewBag.Data" xName="x" yName="y">
</ejs-rangenavigator>
```

## Key Properties

| Property | Type | Purpose | Example |
|----------|------|---------|---------|
| `valueType` | DateTime, Double, Logarithmic | Data scale type | `valueType="DateTime"` |
| `width` | string/number | Component width | `width="100%"` |
| `height` | string/number | Component height | `height="150px"` |
| `minimum` | DateTime/number | Minimum axis value | `minimum="1"` |
| `maximum` | DateTime/number | Maximum axis value | `maximum="100"` |
| `value` | DateTime[]/number[] | Selected range | `value="new DateTime[]{start, end}"` |
| `intervalType` | Years, Months, Days, Hours, Minutes, Seconds | Date interval type | `intervalType="Months"` |
| `interval` | number | Interval count | `interval="3"` |
| `labelFormat` | string | Date/number label format | `labelFormat="MMM dd, yyyy"` |
| `enableGrouping` | bool | Multi-level labels | `enableGrouping="true"` |
| `enableRtl` | bool | Right-to-left support | `enableRtl="true"` |
| `allowSnapping` | bool | Snap to intervals | `allowSnapping="true"` |
| `enableDeferredUpdate` | bool | Update on release | `enableDeferredUpdate="true"` |
| `animationDuration` | number | Animation speed (ms) | `animationDuration="500"` |

## Common Use Cases

1. **Stock Price Range Selector** - Allow users to select time periods to analyze historical stock data
2. **Sales Dashboard Filter** - Let users pick date ranges to filter sales reports and metrics
3. **Time-Series Data Explorer** - Enable exploration of large datasets with interactive range selection
4. **Event Timeline Navigation** - Navigate through historical events or logs by date range
5. **Lightweight Date Filter** - Simple range selector without chart for mobile or embedded scenarios
6. **Multi-Period Analysis** - Quick buttons to switch between predefined time intervals (daily, monthly, yearly)

---

**Need help?** Read the appropriate reference file from the Navigation Guide above based on what you want to accomplish.
