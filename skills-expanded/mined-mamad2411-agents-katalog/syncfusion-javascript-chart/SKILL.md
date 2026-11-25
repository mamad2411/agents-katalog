---
name: syncfusion-javascript-chart
description: Implements Syncfusion JavaScript chart controls (Line, Area, Bar, Column, Pie, Polar, Radar, Waterfall, Stock). Use when building interactive data visualizations, dashboards, or real-time charts. Covers series and axes configuration, styling, animations, exporting, and technical indicators. Works with TypeScript (webpack/modules) and JavaScript (CDN/ES5).
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing Charts in Syncfusion TypeScript & JavaScript

The Syncfusion Chart component provides a comprehensive suite of visualization tools for building interactive, data-driven dashboards. With 15+ chart types, advanced customization options, and real-time data support, you can create professional visualizations for any use case. Works in both TypeScript (with full type safety) and JavaScript (ES5 CDN-based or webpack).

## Platform Support

This skill covers both TypeScript and JavaScript implementations:

**TypeScript (Primary):**
- Full type definitions and IDE support
- Module-based imports with `Chart.Inject()`
- Webpack/bundler-based setup
- Advanced type checking

**JavaScript (ES5):**
- CDN-based or local script loading
- Global namespace access (`ej.charts.Chart`)
- No build step required
- Compatible with ES5 and modern browsers

**Where noted**, code examples show both TS and JS variants. Choose based on your project setup.

## When to Use This Skill

Use this skill when you need to:
- **Create basic charts** - Line, area, bar, column, pie, or scatter plots
- **Visualize complex data** - Multiple series, stacked charts, grouped data
- **Build dashboards** - Combine charts with real-time data updates
- **Customize appearance** - Colors, fonts, animations, themes
- **Add interactivity** - Tooltips, legends, selection, zooming, crosshairs
- **Implement advanced features** - Technical indicators, trendlines, annotations
- **Export charts** - PNG, SVG, PDF, or print functionality
- **Optimize performance** - Handle large datasets efficiently
- **Support accessibility** - WCAG compliance, keyboard navigation, RTL

## Navigation Guide

Choose the reference that matches your task:

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and setup
- Basic chart creation with minimal code
- Data binding fundamentals
- Theme selection and initial configuration

### Chart Types & Selection
📄 **Read:** [references/chart-types.md](references/chart-types.md)
- Overview of 15+ chart types (Line, Area, Bar, Column, Pie, Doughnut, Polar, Radar, Waterfall, Funnel, Stock, etc.)
- When to use each type
- Basic implementation for each chart type
- Series combinations and variations

### Series Configuration
📄 **Read:** [references/series-configuration.md](references/series-configuration.md)
- Configuring series properties and data
- Data labels and marker customization
- Stacking and grouping strategies
- Empty point handling and data gaps

### Axes Customization
📄 **Read:** [references/axes-customization.md](references/axes-customization.md)
- Category, numeric, and datetime axes
- Axis labels, formatting, and ranges
- Multiple axes and panes
- Custom axis positioning and scrolling

### Features & Interaction
📄 **Read:** [references/features-interaction.md](references/features-interaction.md)
- Tooltips, crosshairs, and track balls
- Legend configuration and positioning
- Selection, zooming, and panning
- Annotations, markers, and indicators

### Styling & Appearance
📄 **Read:** [references/styling-appearance.md](references/styling-appearance.md)
- Color schemes, gradients, and themes
- Font, border, and background customization
- Chart area and plot area styling
- Responsive design and layout

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Technical indicators (SMA, EMA, MACD, RSI, Stochastic, etc.)
- Trendlines and trend analysis
- Export to PNG, SVG, PDF, Print
- Animations and smooth transitions

### Data Handling & Updates
📄 **Read:** [references/data-handling.md](references/data-handling.md)
- Dynamic data updates and real-time charts
- Data editing and user interaction
- Loading and caching large datasets
- Working with various data sources

### Accessibility & RTL
📄 **Read:** [references/accessibility-rtl.md](references/accessibility-rtl.md)
- WCAG compliance and accessibility standards
- Keyboard navigation
- ARIA labels and screen reader support
- Right-to-left (RTL) language support

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Complete Chart API documentation
- All classes, enumerations, and interfaces
- Methods and events reference
- Module injection guide
- Configuration patterns

### Troubleshooting & Optimization
📄 **Read:** [references/troubleshooting.md](references/troubleshooting.md)
- Common issues and solutions
- Performance optimization techniques
- Browser compatibility notes
- Debugging strategies

## Quick Start Example

**TypeScript:**
```typescript
import { Chart, LineSeries, DateTime, Legend, Tooltip, Category } from '@syncfusion/ej2-charts';

// Inject required modules
Chart.Inject(LineSeries, DateTime, Legend, Tooltip, Category);

const data = [
  { month: 'Jan', sales: 21 },
  { month: 'Feb', sales: 24 },
  { month: 'Mar', sales: 36 },
  { month: 'Apr', sales: 38 },
  { month: 'May', sales: 54 }
];

const chart = new Chart({
  primaryXAxis: { valueType: 'Category' },
  title: 'Monthly Sales',
  tooltip: { enable: true },
  legendSettings:{ visible: true },
  series: [{
    dataSource: data,
    xName: 'month',
    yName: 'sales',
    type: 'Line',
    name: 'Sales'
  }]
}, '#chart');
```

## Common Patterns

### Pattern 1: Multi-Series Bar Chart
Multiple data series displayed side-by-side for comparison:

```typescript
series: [
  { dataSource: data, xName: 'month', yName: 'sales', type: 'Column', name: 'Sales' },
  { dataSource: data, xName: 'month', yName: 'revenue', type: 'Column', name: 'Revenue' }
]
```

### Pattern 2: Stacked Column with Legend
Stacked visualization showing composition and trends:

```typescript
series: [
  { dataSource: data, xName: 'category', yName: 'value1', type: 'StackingColumn' },
  { dataSource: data, xName: 'category', yName: 'value2', type: 'StackingColumn' }
],
legend: { visible: true, position: 'Bottom' }
```

### Pattern 3: Real-Time Data Update
Continuously updating chart with new data points:

```typescript
// Update with new data
chart.series[0].dataSource = updatedData;
chart.refresh();
```

### Pattern 4: Interactive Selection
Enable user selection with event handling:

```typescript
pointRender: (args: IPointRenderEventArgs) => {
  // Customize point on selection
},
selectionMode: 'Point'
```

## Key Properties

**Chart-level:**
- `primaryXAxis`, `primaryYAxis` - Configure axes
- `series` - Define data series
- `tooltip` - Enable/configure tooltips
- `legend` - Control legend display
- `title` - Chart title

**Series-level:**
- `dataSource` - Data binding
- `xName`, `yName` - Data field mapping
- `type` - Chart type (Line, Column, Pie, etc.)
- `marker` - Point customization
- `dataLabel` - Label display

**Customization:**
- `palette` - Color scheme
- `theme` - Built-in theme
- `background` - Chart background
- `height`, `width` - Dimensions
