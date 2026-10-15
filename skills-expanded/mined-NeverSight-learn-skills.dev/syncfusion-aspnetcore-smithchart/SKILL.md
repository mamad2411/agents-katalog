---
name: syncfusion-aspnetcore-smithchart
description: Implement Smith Chart visualization for RF and transmission line analysis. Use this skill when building high-frequency circuit applications, impedance/admittance series plots, or transmission line parameter visualizations. Perfect for network analysis dashboards, component testing interfaces, or technical engineering applications requiring Smith chart data representation.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing Syncfusion Smith Chart

The Syncfusion Smith Chart is a specialized data visualization control designed for high-frequency circuit applications, particularly useful for plotting transmission line parameters and impedance/admittance analysis. This skill guides you through implementing, configuring, and customizing Smith Charts in ASP.NET Core applications.

## When to Use This Skill

Use this skill when you need to:
- Visualize transmission line parameters on a Smith Chart
- Plot impedance and admittance series
- Create RF and microwave circuit analysis dashboards
- Display multiple series with markers and data labels
- Implement interactive charts with tooltips and legends
- Export or print Smith Chart visualizations
- Build accessible technical visualization interfaces

## Component Overview

The Smith Chart control provides:
- Support for any number of series and data points
- Impedance and admittance series render types
- Interactive markers and data labels
- Legend support with visibility toggling
- Tooltip interactions for detailed data insights
- Print and export capabilities (JPEG, PNG, SVG, PDF)
- Full accessibility compliance (WCAG 2.2 AA)
- Responsive sizing for various screen dimensions

## Documentation and Navigation Guide

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Complete API documentation for Smith Chart component
- Constructor and property definitions
- Event properties and callbacks
- Series, axis, and styling configuration
- Legend and tooltip setup
- Data structure requirements

### Getting Started & Setup
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- NuGet package installation for ASP.NET Core
- TagHelper configuration and imports
- Script resources and initialization
- Basic Smith Chart rendering
- Your first working example

### Data Binding & Series Configuration
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- JSON data structure with resistance/reactance fields
- Using points vs datasource properties
- Binding multiple series to Smith Charts
- Data preparation patterns

📄 **Read:** [references/series-configuration.md](references/series-configuration.md)
- Series customization (fill color, opacity, width)
- Smart label positioning
- Series visibility and styling
- Managing multiple series

### Axis & Dimensions
📄 **Read:** [references/axis-configuration.md](references/axis-configuration.md)
- Horizontal and radial axis configuration
- Label customization and positioning strategies
- Major and minor gridline setup
- Axis line styling and visibility

📄 **Read:** [references/dimensions-sizing.md](references/dimensions-sizing.md)
- Container-based sizing approaches
- Pixel-based width/height configuration
- Percentage-based responsive sizing
- Responsive design patterns

### Visual Elements (Markers, Labels, Legend)
📄 **Read:** [references/markers-labels.md](references/markers-labels.md)
- Enabling and configuring markers for data points
- Marker shape, color, opacity, and border customization
- Data label enablement and visibility
- Data label styling and text properties

📄 **Read:** [references/legend-tooltip.md](references/legend-tooltip.md)
- Legend positioning (top, bottom, left, right, custom)
- Legend alignment and shape customization
- Legend sizing and padding control
- Series visibility toggling
- Tooltip enablement and series-specific customization

### Output & Enhancements
📄 **Read:** [references/title-print-export.md](references/title-print-export.md)
- Adding and styling titles and subtitles
- Title trimming for space-constrained layouts
- Printing Smith Charts directly from the browser
- Exporting to multiple formats (JPEG, PNG, SVG, PDF)

📄 **Read:** [references/accessibility.md](references/accessibility.md)
- WCAG 2.2 AA accessibility compliance
- WAI-ARIA attributes and screen reader support
- Keyboard navigation shortcuts
- Ensuring accessible implementations

## Quick Start Example

```cshtml
<ejs-smithchart id="smithchart">
    <e-seriescollection>
        <e-series dataSource="TransmissionData" name="Transmission 1">
            <e-marker visible="true">
                <e-datalabel visible="true"></e-datalabel>
            </e-marker>
        </e-series>
    </e-seriescollection>
</ejs-smithchart>
```

With corresponding data model containing `resistance` and `reactance` fields.

## Common Patterns

### Pattern 1: Basic Chart with Series
Create a Smith Chart with one series, markers enabled, and basic styling.

### Pattern 2: Multiple Series with Legend
Render multiple transmission line series with a legend for visibility control and series identification.

### Pattern 3: Interactive Dashboard
Build a dashboard with tooltips, data labels, custom axis configuration, and print/export capabilities.

### Pattern 4: Responsive Layout
Implement percentage-based sizing to create Smith Charts that adapt to container dimensions.

## Key Properties

**Series Level:**
- `dataSource` - Array of data objects with resistance/reactance
- `points` - Direct array of point values
- `fill` - Series line color
- `opacity` - Series transparency
- `width` - Series line thickness
- `name` - Series identifier for legend

**Axis Level:**
- `labelPosition` - Inside or outside axis
- `labelIntersectAction` - Hide intersecting labels
- `visible` - Show/hide axis

**Legend:**
- `visible` - Enable/disable legend
- `position` - top, bottom, left, right, custom
- `alignment` - near, center, far

## Common Use Cases

1. **RF Circuit Analysis** - Plot transmission line parameters and impedance matching
2. **Network Analysis** - Visualize S-parameters and reflection coefficients
3. **Component Testing** - Display measurement data from high-frequency components
4. **Educational Dashboards** - Teach transmission line theory with interactive visualizations
5. **Technical Reports** - Generate exportable Smith Chart diagrams for documentation
