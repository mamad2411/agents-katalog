---
name: syncfusion-javascript-accumulation-chart
description: Implements Syncfusion JavaScript accumulation charts (Pie, Doughnut, Funnel, Pyramid) for proportional and percentage-based visualizations. Use when displaying categorical or proportional data. Covers legend and label configuration, interactivity, accessibility, and customization. Works with TypeScript (modules) and JavaScript (CDN/ES5).
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing Accumulation Charts in Syncfusion TypeScript & JavaScript

The Syncfusion Accumulation Chart component provides powerful visualization tools for creating interactive pie charts, doughnut charts, funnel charts, and pyramid charts. With advanced customization options, interactive features, multiple chart types, and comprehensive data handling capabilities, you can create professional percentage-based and categorical visualizations for any use case. Works in both TypeScript (with full type safety) and JavaScript (ES5 CDN-based or webpack).

## Platform Support

This skill covers both TypeScript and JavaScript implementations:

**TypeScript (Primary):**
- Full type definitions and IDE support
- Module-based imports with `AccumulationChart.Inject()`
- Webpack/bundler-based setup
- Advanced type checking

**JavaScript (ES5):**
- CDN-based or local script loading
- Global namespace access (`ej.charts.AccumulationChart`)
- No build step required
- Compatible with ES5 and modern browsers

**Where noted**, code examples show both TS and JS variants. Choose based on your project setup.

## When to Use This Skill

Use this skill when you need to:
- **Create pie charts** - Basic pie chart with data points and series
- **Build doughnut charts** - Pie chart with inner radius (donut hole)
- **Implement funnel charts** - Funnel-shaped data visualization
- **Design pyramid charts** - Pyramid-shaped hierarchical visualization
- **Configure chart types** - Switch between Pie, Doughnut, Funnel, Pyramid
- **Customize legends** - Position, align, and style legend elements
- **Add data labels** - Configure label positioning and content
- **Enable tooltips** - Interactive hover information
- **Implement selection** - Point and series selection modes
- **Add annotations** - Custom annotations and markers
- **Apply styling** - Colors, gradients, themes, and responsive design
- **Ensure accessibility** - WCAG compliance, keyboard navigation, screen reader support
- **Export charts** - PNG, SVG, PDF, or print functionality
- **Handle dynamic data** - Real-time data updates and animations

## Accumulation Chart Overview

Accumulation charts visualize data as proportions of a whole, ideal for:
- **Pie Charts** - Show percentage distribution of categories
- **Doughnut Charts** - Pie variant with center label capability
- **Funnel Charts** - Funnel-shaped representations (stages, conversion funnels)
- **Pyramid Charts** - Pyramid-shaped hierarchical data visualization

All types support interactive features, custom styling, multiple series, and rich configuration options.

## Navigation Guide

Choose the reference that matches your task:

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and setup for TypeScript and JavaScript
- Dependencies and package configuration
- Creating your first accumulation chart
- Basic pie chart implementation
- Module injection and initialization patterns

### Chart Types & Selection
📄 **Read:** [references/chart-types.md](references/chart-types.md)
- Pie chart fundamentals and implementation
- Doughnut charts with inner radius and center labels
- Funnel charts and data arrangement
- Pyramid charts and reverse mode
- Radius and size customization for each type
- Comparison matrix: when to use each type

### Legend Configuration
📄 **Read:** [references/legend-configuration.md](references/legend-configuration.md)
- Legend positioning (left, right, top, bottom)
- Alignment options (center, near, far)
- Legend styling and customization
- Visibility and interactive legend features
- Responsive legend behavior

### Data Labels
📄 **Read:** [references/data-labels.md](references/data-labels.md)
- Enabling and configuring data labels
- Label positioning (inside, outside)
- Smart label arrangement and overlap prevention
- Label formatting and templates
- Dynamic label visibility

### Tooltips & Selection
📄 **Read:** [references/tooltips-and-selection.md](references/tooltips-and-selection.md)
- Tooltip configuration and styling
- Custom tooltip templates
- Point selection modes (Single, Multiple, None)
- Series selection capabilities
- Event handling for interactions

### Annotations & Features
📄 **Read:** [references/annotations-and-features.md](references/annotations-and-features.md)
- Adding annotations to charts
- Gradient fills and custom colors
- Center labels for doughnut charts
- Grouping and clubbing data points
- Empty point handling and visibility

### Customization & Styling
📄 **Read:** [references/customization-and-styling.md](references/customization-and-styling.md)
- CSS class customization and styling
- Theme options (Material, Bootstrap, Fabric, etc.)
- Responsive sizing and dimensions
- Print and export functionality
- Title and subtitle configuration

### Accessibility & Advanced Features
📄 **Read:** [references/accessibility-and-advanced.md](references/accessibility-and-advanced.md)
- WCAG compliance and accessibility standards
- Keyboard navigation and focus management
- Screen reader support and ARIA attributes
- Dynamic data updates and animations
- Real-time chart updates
- Performance optimization for large datasets
- Troubleshooting common issues

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Complete AccumulationChart API reference
- All properties, methods, and events
- Interface and model definitions
- Module injection and enums
- Comprehensive API tables with links to official documentation

## Quick Start Example

**TypeScript:**
```typescript
import { AccumulationChart, AccumulationDataLabel, AccumulationLegend, AccumulationTooltip } from '@syncfusion/ej2-charts';

// Inject required modules
AccumulationChart.Inject( AccumulationDataLabel, AccumulationLegend, AccumulationTooltip);

const data = [
  { x: 'Jan', y: 18, text: 'January' },
  { x: 'Feb', y: 18, text: 'February' },
  { x: 'Mar', y: 18, text: 'March' },
  { x: 'Apr', y: 20, text: 'April' }
];

const chart = new AccumulationChart({
  series: [{
    dataSource: data,
    xName: 'x',
    yName: 'y',
    type: 'Pie'
  }],
  tooltip: { enable: true },
  legendSettings: { visible: true }
}, '#chart');
```

## Common Patterns

### Pattern 1: Basic Pie Chart with Legend
Standard pie chart showing data distribution with legend for category identification:

```typescript
const chart = new AccumulationChart({
  series: [{
    dataSource: data,
    xName: 'x',
    yName: 'y',
    type: 'Pie' // `type` is optional for `Pie` since it is default
  }],
  legendSettings: { visible: true, position: 'Right' }
}, '#chart');
```

### Pattern 2: Doughnut Chart with Center Label
Doughnut chart with center text for additional information:

```typescript
const chart = new AccumulationChart({
  series: [{
    dataSource: data,
    xName: 'x',
    yName: 'y',
    innerRadius: '40%'    // no explicit type for doughnut chart, innerRadius itself renders doughnut.
  }],
  centerLabel: { text: 'Sales', hoverTextFormat: '${point.x}: ${point.y}%' }
}, '#chart');
```

### Pattern 3: Funnel Chart with Custom Colors
Funnel visualization showing progression through stages:

**Note** Import and Inject `FunnelSeries`.

```typescript
const chart = new AccumulationChart({
  series: [{
    dataSource: stageData,
    xName: 'stage',
    yName: 'users',
    type: 'Funnel',
    neckWidth: '15%'
  }]
}, '#chart');
```

### Pattern 4: Pyramid Chart Reversed
Pyramid visualization:

**Note** Import and Inject `PyramidSeries`.

```typescript
const chart = new AccumulationChart({
  series: [{
    dataSource: data,
    xName: 'x',
    yName: 'y',
    type: 'Pyramid',
    pyramidMode: 'Linear',
  }]
}, '#chart');
```

### Pattern 5: Interactive Selection with Tooltip
Point selection with detailed tooltips:

**Note** Import and Inject `AccumulationTooltip` and `AccumulationSelection`.

```typescript
const chart = new AccumulationChart({
  series: [{
    dataSource: data,
    xName: 'x',
    yName: 'y',
    type: 'Pie',
    dataLabel: { 
      visible: true,
      position: 'Outside',
      name: 'text'
    }
  }],
  selectionMode: 'Point',
  tooltip: { 
    enable: true,
    format: '${point.x}: <b>${point.y}%</b>'
  }
}, '#chart');
```

## Key Properties

For detailed information on all properties, methods, and events, see [API Reference](references/api-reference.md).

**Chart-level:**
- `series` - Array of series configurations | [API](https://ej2.syncfusion.com/documentation/api/accumulation-chart/accumulationseriesmodel/)
- `height`, `width` - Chart dimensions | [API](https://ej2.syncfusion.com/documentation/api/accumulation-chart/#height)
- `title` - Chart title text | [API](https://ej2.syncfusion.com/documentation/api/accumulation-chart/#title)
- `tooltip` - Tooltip configuration | [API](https://ej2.syncfusion.com/documentation/api/accumulation-chart/tooltipsettingsmodel/)
- `legendSettings` - Legend positioning and styling | [API](https://ej2.syncfusion.com/documentation/api/accumulation-chart/legendsettingsmodel/)
- `background` - Chart background color/image | [API](https://ej2.syncfusion.com/documentation/api/accumulation-chart/#background)
- `centerLabel` - Center label for doughnut (TS & JS) | [API](https://ej2.syncfusion.com/documentation/api/accumulation-chart/centerlabelmodel/)

**Series-level:**
- `dataSource` - Array of data points | [API](https://ej2.syncfusion.com/documentation/api/accumulation-chart/#datasource)
- `xName`, `yName` - Data field mapping | [API](https://ej2.syncfusion.com/documentation/api/accumulation-chart/accumulationseriesmodel/)
- `type` - Chart type: 'Pie', 'Doughnut', 'Funnel', 'Pyramid'
- `radius` - Chart radius (percentage or pixel)
- `innerRadius` - Inner radius for doughnut charts
- `neckWidth` - Funnel neck width
- `gapRatio` - Space between pyramid segments
- `explode` - Point explosion (separation)
- `dataLabel` - Data label configuration | [API](https://ej2.syncfusion.com/documentation/api/accumulation-chart/)
- `marker` - Point marker styling

**Interaction:**
- `selectionMode` - 'Point', 'Series', or 'None' | [API](https://ej2.syncfusion.com/documentation/api/accumulation-chart/accumulationselectionmode/)
- `selectionPattern` - Chessboard, Dots, DiagonalForward, etc. | [API](https://ej2.syncfusion.com/documentation/api/accumulation-chart/selectionpattern/)
- `highlightPattern` - Highlight pattern on hover | [API](https://ej2.syncfusion.com/documentation/api/accumulation-chart/selectionpattern/)
- `highlightMode` - 'Point', 'Series', or 'None' | [API](https://ej2.syncfusion.com/documentation/api/accumulation-chart/accumulationhighlightmode/)

**Styling:**
- `palette` - Color scheme array
- `theme` - Material, Bootstrap, Fabric, HighContrast, Fluent | [API](https://ej2.syncfusion.com/documentation/api/accumulation-chart/accumulationtheme/)
- `enableSmartLabels` - Smart label positioning | [API](https://ej2.syncfusion.com/documentation/api/accumulation-chart/#enablesmartlabels)
- `enableAnimation` - Animation on load | [API](https://ej2.syncfusion.com/documentation/api/accumulation-chart/#enableanimation)
- `animationDuration` - Animation duration in milliseconds

**Accessibility:**
- `accessibility` - Accessibility configuration object | [API](https://ej2.syncfusion.com/documentation/api/accumulation-chart/accessibilitymodel/)
- `tabIndex` - Tab index for keyboard navigation
- `ariaLabel` - ARIA label for screen readers
