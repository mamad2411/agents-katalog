---
name: syncfusion-angular-chart
description: Implement Syncfusion Angular Chart component for professional data visualization. Use this when creating or customizing charts such as line, bar, column, area, pie, financial (candlestick, OHLC), scatter, bubble, or stock charts. Supports axes configuration, series binding, legends, tooltips, zooming, real-time updates, technical indicators, themes, export, and accessibility features.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing Syncfusion Angular Chart Component

A comprehensive guide for implementing the Syncfusion Angular Chart component, a high-performance, interactive data visualization library supporting 25+ chart types including line, bar, area, column, pie, financial, and specialized series. Optimized for responsive rendering, smooth interactions, and large datasets.

## When to Use This Skill

Use this skill when you need to:

- **Visualize Data:** Display numerical data as charts, graphs, or plots in Angular applications
- **Trend Analysis:** Show data trends over time using line, spline, or area charts
- **Comparisons:** Compare categorical data using column, bar, or grouped charts
- **Financial Data:** Implement stock charts with candlestick, OHLC, or technical indicators
- **Statistical Analysis:** Use box plots, histograms, or pareto charts for distributions
- **Multi-dimensional Data:** Display scatter plots or bubble charts for correlation analysis
- **Real-time Monitoring:** Create live-updating charts for dashboards or monitoring systems
- **Interactive Exploration:** Add zooming, panning, crosshair, tooltips, or selection features
- **Custom Visualizations:** Combine multiple series types, axes, or create complex layouts
- **Accessible Charts:** Implement WCAG-compliant charts with keyboard navigation and screen reader support

## Component Overview

The Syncfusion Angular Chart is a feature-rich data visualization component with:

- **25+ Series Types:** Line, spline, step line, area, column, bar, scatter, bubble, pie, financial (candlestick, OHLC), statistical (box & whisker, histogram, pareto), polar, radar, waterfall, and more
- **Interactive Features:** Zooming (selection, mouse wheel, pinch), panning, tooltips, crosshair, trackball, selection, data editing
- **Multiple Axes:** Support for primary, secondary, and multiple axes with different data types (numeric, datetime, logarithmic, category)
- **Chart Elements:** Legends, data markers, data labels, annotations, trendlines, technical indicators, striplines
- **Data Binding:** Local arrays, remote data (OData, DataManager), JSON sources, dynamic updates
- **Customization:** Themes, CSS styling, color palettes, responsive design, animations
- **Export & Print:** Export to PDF, SVG, PNG, JPEG, CSV, XLSX formats
- **Accessibility:** WCAG compliance, keyboard navigation, ARIA attributes, internationalization, RTL support

## Documentation and Navigation Guide

### Getting Started

📄 **Read:** [references/getting-started.md](references/getting-started.md)

When you need to:
- Install and set up the Chart component in an Angular project
- Understand prerequisites and system requirements
- Add the `@syncfusion/ej2-angular-charts` package
- Configure CSS themes and imports
- Create your first basic chart
- Understand the chart module structure

### Series Types

📄 **Read:** [references/series-types.md](references/series-types.md)

When you need to:
- Choose the appropriate chart type for your data
- Implement line series (line, step line, spline, stacked, multi-colored)
- Create area charts (area, stacked, 100% stacked, range, spline range)
- Build column and bar charts (column, bar, stacked, range)
- Visualize financial data (candlestick, hilo, hilo-open-close)
- Use statistical charts (box & whisker, histogram, pareto, error bar)
- Create specialized charts (scatter, bubble, polar, radar, waterfall, vertical)
- Combine multiple series types in one chart

### Chart Elements

📄 **Read:** [references/chart-elements.md](references/chart-elements.md)

When you need to:
- Configure and customize legends (positioning, templates, styling)
- Add data markers to highlight points (shapes, sizes, visibility)
- Display data labels on chart elements (positioning, templates, formatting)
- Add custom annotations (text, shapes, images at specific coordinates)
- Include trendlines (linear, exponential, polynomial, moving average)
- Add technical indicators (RSI, MACD, Bollinger Bands, EMA, SMA)
- Highlight specific ranges with striplines
- Apply gradient fills to series

### Axes and Layout

📄 **Read:** [references/axes-and-layout.md](references/axes-and-layout.md)

When you need to:
- Configure axis types (numeric, datetime, logarithmic, category)
- Set up primary and secondary axes
- Add multiple axes for different data scales
- Format axis labels (rotation, alignment, multilevel labels)
- Customize gridlines and tick marks
- Implement axis crossing and inversed axes
- Create charts with multiple panes
- Configure chart title, subtitle, and dimensions
- Set chart margins and padding

### Interactive Features

📄 **Read:** [references/interactive-features.md](references/interactive-features.md)

When you need to:
- Enable zooming (selection zoom, mouse wheel zoom, pinch zoom, zoom toolbar)
- Implement panning for navigating zoomed charts
- Add tooltips (default, custom templates, shared tooltips)
- Enable crosshair for precise value reading
- Use trackball for multi-series point tracking
- Implement selection (point, series, cluster, drag selection)
- Enable data editing by dragging points
- Synchronize multiple charts for coordinated interactions

### Data Binding

📄 **Read:** [references/data-binding.md](references/data-binding.md)

When you need to:
- Bind local data (arrays of objects, JSON)
- Connect to remote data sources (OData, RESTful APIs)
- Use DataManager for advanced data operations
- Handle dynamic data updates and real-time data
- Manage empty points and null values
- Map data fields to chart properties
- Optimize performance for large datasets
- Handle asynchronous data loading

### Customization

📄 **Read:** [references/customization.md](references/customization.md)

When you need to:
- Apply built-in themes (Material, Bootstrap, Fabric, Tailwind, etc.)
- Customize chart appearance with CSS
- Use Theme Studio for custom theme generation
- Configure color palettes for series
- Style individual series with custom colors and patterns
- Implement responsive design for different screen sizes
- Configure chart background, border, and area
- Customize animation effects

### Accessibility

📄 **Read:** [references/accessibility.md](references/accessibility.md)

When you need to:
- Implement WCAG 2.0/2.1 compliant charts
- Enable keyboard navigation (arrow keys, tab, enter)
- Configure ARIA attributes for screen readers
- Ensure proper color contrast and focus indicators
- Support high contrast themes
- Implement internationalization (i18n) for multiple languages
- Enable localization (l10n) for regional formats
- Add RTL (right-to-left) support for appropriate languages
- Configure advanced accessibility features

### Advanced Features

📄 **Read:** [references/advanced-features.md](references/advanced-features.md)

When you need to:
- Handle chart events (load, loaded, pointClick, seriesRender, axisLabelRender, etc.)
- Export charts (PDF, SVG, PNG, JPEG, CSV, XLSX)
- Implement print functionality
- Understand module injection for tree-shaking
- Use different render methods (SVG, Canvas)
- Configure animation settings
- Handle empty point modes
- Access chart API methods programmatically
- Implement advanced event-driven interactions

### Common Patterns and Examples

📄 **Read:** [references/common-patterns.md](references/common-patterns.md)

When you need to:
- See complete examples for common use cases
- Build a trend analysis dashboard
- Create a financial stock chart with technical indicators
- Implement real-time data monitoring with live updates
- Build multi-axis comparison charts
- Create distribution analysis visualizations
- Find troubleshooting solutions for common issues
- Learn performance optimization techniques
- Migrate from EJ1 to EJ2 Chart
- Follow best practices for chart implementation

## Quick Start Example

Here's a minimal example to create a basic line chart:

```typescript
// app.component.ts
import { Component } from '@angular/core';
import { ChartModule } from '@syncfusion/ej2-angular-charts';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [ChartModule],
  template: `
    <ejs-chart [primaryXAxis]='primaryXAxis' [primaryYAxis]='primaryYAxis' [title]='title'>
      <e-series-collection>
        <e-series [dataSource]='chartData' type='Line' xName='month' yName='sales' name='Sales'>
        </e-series>
      </e-series-collection>
    </ejs-chart>
  `
})
export class AppComponent {
  public primaryXAxis = { valueType: 'Category' };
  public primaryYAxis = { title: 'Sales (in USD)' };
  public title = 'Monthly Sales Report';
  
  public chartData = [
    { month: 'Jan', sales: 35000 },
    { month: 'Feb', sales: 28000 },
    { month: 'Mar', sales: 34000 },
    { month: 'Apr', sales: 32000 },
    { month: 'May', sales: 40000 },
    { month: 'Jun', sales: 32000 }
  ];
}
```

```typescript
// app.config.ts (for Angular 19+)
import { ApplicationConfig } from '@angular/core';
import { registerLicense } from '@syncfusion/ej2-base';

// Register Syncfusion license (get free trial at syncfusion.com)
registerLicense('YOUR_LICENSE_KEY');

export const appConfig: ApplicationConfig = {
  providers: []
};
```

## Common Patterns

### Pattern 1: Multi-Series Comparison Chart

```typescript
public chartData = [
  { month: 'Jan', product1: 35, product2: 28, product3: 34 },
  { month: 'Feb', product1: 28, product2: 44, product3: 32 },
  { month: 'Mar', product1: 34, product2: 48, product3: 41 }
];
```

```html
<ejs-chart [primaryXAxis]='primaryXAxis' [title]='title'>
  <e-series-collection>
    <e-series [dataSource]='chartData' type='Column' xName='month' yName='product1' name='Product A'></e-series>
    <e-series [dataSource]='chartData' type='Column' xName='month' yName='product2' name='Product B'></e-series>
    <e-series [dataSource]='chartData' type='Column' xName='month' yName='product3' name='Product C'></e-series>
  </e-series-collection>
</ejs-chart>
```

### Pattern 2: Interactive Chart with Zoom and Tooltip

```typescript
import { Component } from '@angular/core';
import { ChartModule, ZoomService, TooltipService } from '@syncfusion/ej2-angular-charts';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [ChartModule],
  providers: [ZoomService, TooltipService],
  template: `
    <ejs-chart [zoomSettings]='zoomSettings' [tooltip]='tooltip'>
      <e-series-collection>
        <e-series [dataSource]='data' type='Line' xName='x' yName='y'></e-series>
      </e-series-collection>
    </ejs-chart>
  `
})
export class AppComponent {
  public zoomSettings = {
    enableSelectionZooming: true,
    enableMouseWheelZooming: true,
    enablePinchZooming: true,
    enablePan: true
  };
  
  public tooltip = { enable: true };
  public data = [/* your data */];
}
```

### Pattern 3: Financial Stock Chart

```typescript
public stockData = [
  { date: new Date(2024, 1, 1), open: 120, high: 135, low: 110, close: 130, volume: 1000000 },
  { date: new Date(2024, 1, 2), open: 130, high: 145, low: 125, close: 140, volume: 1200000 }
  // ... more data
];
```

```html
<ejs-chart [primaryXAxis]='primaryXAxis' [primaryYAxis]='primaryYAxis'>
  <e-series-collection>
    <e-series [dataSource]='stockData' type='Candle' 
              xName='date' high='high' low='low' open='open' close='close'>
    </e-series>
  </e-series-collection>
</ejs-chart>
```

## Key Configuration Options

### Series Configuration
- `type`: Chart type (Line, Column, Bar, Area, Scatter, etc.)
- `dataSource`: Data array for the series
- `xName`, `yName`: Property names for x and y values
- `name`: Series name for legend
- `marker`: Marker configuration for data points
- `fill`: Series color

### Axis Configuration
- `valueType`: Axis type (Double, DateTime, Category, Logarithmic)
- `title`: Axis title text
- `minimum`, `maximum`: Axis range
- `interval`: Label interval
- `labelFormat`: Format string for labels
- `opposedPosition`: Position axis on opposite side

### Chart Configuration
- `title`: Chart title
- `width`, `height`: Chart dimensions
- `theme`: Built-in theme name
- `background`: Chart background color
- `legendSettings`: Legend configuration
- `zoomSettings`: Zoom configuration
- `tooltip`: Tooltip configuration

## Common Use Cases

1. **Business Dashboards:** Display KPIs, sales trends, revenue comparisons
2. **Financial Applications:** Stock charts, portfolio performance, technical analysis
3. **Analytics Platforms:** User behavior, traffic analysis, conversion funnels
4. **Scientific Visualization:** Experimental data, statistical distributions, correlation analysis
5. **Monitoring Systems:** Real-time metrics, system performance, IoT data
6. **Reporting Tools:** Automated reports, data exports, scheduled visualizations
7. **Educational Applications:** Math graphs, statistics teaching, data science demonstrations

## Next Steps

After creating your basic chart:
- Explore different series types for your specific data visualization needs
- Add interactive features like zooming and tooltips for better user experience
- Customize appearance with themes and styling
- Implement data binding for dynamic data sources
- Ensure accessibility compliance for all users
- Export and print capabilities for sharing visualizations

For detailed implementation guidance, refer to the specific reference files listed in the navigation guide above.

## API Reference Documentation

📄 **Complete API Guide:** [references/api-reference.md](references/api-reference.md)

The Syncfusion Angular Chart component provides 200+ API documentation files covering:

- **Core APIs:** ChartModel (40+ properties), AxisModel (50+ properties), SeriesDirective (60+ properties)
- **Chart Elements:** Legend, Markers, Data Labels, Tooltip, Annotations, Trendlines, Technical Indicators, Striplines
- **Interactive Features:** Zooming, Panning, Crosshair, Selection, Drag Settings
- **Events:** 40+ event interfaces (ILoadedEventArgs, IPointRenderEventArgs, IZoomingEventArgs, etc.)
- **Enumerations:** 50+ enums (ChartSeriesType, ValueType, ChartTheme, SelectionMode, ExportType, etc.)
- **Utilities:** BorderModel, FontModel, MarginModel, AnimationModel, and more

All API documentation is available at https://ej2.syncfusion.com/angular/documentation/api/chart/. See [references/api-reference.md](references/api-reference.md) for comprehensive API navigation and documentation structure.

Each reference guide (getting-started.md, series-types.md, axes-and-layout.md, etc.) links to the official online API documentation throughout the content.
