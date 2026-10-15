---
name: syncfusion-angular-sparkline
description: Implement Syncfusion Angular Sparkline component for compact data visualization. Use this skill whenever the user needs to create sparkline charts, visualize small datasets inline, add markers or data labels, implement different sparkline types (Line, Column, Area, Pie, Win-Loss), or handle sparkline customization like tooltips, axis settings, and theme styling. Covers installation, basic rendering, type selection, marker configuration, data label formatting, advanced features, accessibility, and migration from EJ1.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing Syncfusion Angular Sparkline Component

## When to Use This Skill

Use this skill when you need to:
- **Visualize compact data** - Display small time-series datasets inline within tables, grids, or dashboards
- **Add sparkline charts** - Render Line, Column, Area, Pie, or Win-Loss sparklines
- **Enhance data presentation** - Add markers for key points (high, low, start, end, negative)
- **Display metrics inline** - Show data labels and tooltips within sparklines
- **Customize appearance** - Apply themes, styling, accessibility features, or range bands
- **Integrate into existing apps** - Set up the Sparkline module with proper service injection
- **Migrate from legacy** - Move from EJ1 Sparkline to EJ2 Angular Sparkline

## Component Overview

The **Syncfusion Angular Sparkline** is a lightweight data visualization component that displays compact charts in a small space. Sparklines are ideal for:
- Trend indicators within tables or dashboards
- Visual representation of sequential data
- Inline metrics showing performance or changes over time

**Key characteristics:**
- **Compact rendering** - Fits within grid cells or inline metrics
- **Multiple types** - Line, Column, Area, Pie, Win-Loss visualizations
- **Interactive features** - Tooltips, markers, data labels
- **Customizable** - Markers, colors, axis settings, themes
- **Accessible** - WCAG support, keyboard navigation, RTL support

> ⚠️ **CRITICAL: Multiple Sparklines Require Unique IDs**
> 
> When using **more than one sparkline component** on the same page, you **MUST** provide a unique `id` attribute to each sparkline to ensure proper rendering.
> 
> ```html
> <!-- ✓ CORRECT - Unique IDs for multiple sparklines -->
> <ejs-sparkline id="sparkline1" [dataSource]="data1"></ejs-sparkline>
> <ejs-sparkline id="sparkline2" [dataSource]="data2"></ejs-sparkline>
> <ejs-sparkline id="sparkline3" [dataSource]="data3"></ejs-sparkline>
> 
> <!-- ✗ WRONG - No IDs or duplicate IDs causes rendering issues -->
> <ejs-sparkline [dataSource]="data1"></ejs-sparkline>
> <ejs-sparkline [dataSource]="data2"></ejs-sparkline>
> ```
> 
> **Without unique IDs, sparklines may:**
> - Not render at all
> - Render with incorrect data
> - Overlap or conflict with each other
> - Display inconsistent styles

## Documentation and Navigation Guide

This skill guides you through implementing sparklines. Here are the key topics:

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup for Angular 19+
- Basic sparkline component implementation
- Module injection for SparklineTooltipService
- Data binding with dataSource, xName, and yName
- Enabling tooltips and running the application
- When to read: Before implementing your first sparkline

### Sparkline Types
📄 **Read:** [references/sparkline-types.md](references/sparkline-types.md)
- Line type (default, line chart visualization)
- Column type (vertical bar representation)
- Area type (filled area charts)
- Pie type (proportional/compositional data)
- Win-Loss type (binary outcomes: success/failure)
- Type comparison and selection criteria
- When to read: Choose which sparkline type best represents your data

### Markers
📄 **Read:** [references/markers.md](references/markers.md)
- Enabling markers for all points or specific points
- Marker options: All, Start, End, High, Low, Negative
- Customizing marker appearance (fill, border, size, opacity)
- Combining multiple marker types
- When to read: Highlight key data points (peaks, valleys, start/end)

### Data Labels
📄 **Read:** [references/data-labels.md](references/data-labels.md)
- Enabling data labels for specific points
- Label options: All, Start, End, High, Low, Negative
- Customizing label styling (fill, border, text color)
- Formatting label text with custom formats
- Displaying x and y values in labels
- When to read: Add numeric or formatted values directly on the sparkline

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Range band visualization (shaded background regions)
- Axis customization (min, max, interval settings)
- User interactions (tooltip configuration, event handling)
- Special points customization (high/low point colors)
- Container sizing and responsive dimensions
- RTL (Right-to-Left) support
- When to read: Implement complex features like range bands, axis control, or events

### Appearance and Accessibility
📄 **Read:** [references/appearance-and-accessibility.md](references/appearance-and-accessibility.md)
- CSS themes and theme switching
- Appearance customization with CSS classes
- Localization (locale-specific formatting)
- WCAG accessibility compliance
- Keyboard navigation support
- Responsive design for different screen sizes
- When to read: Style the sparkline, support multiple locales, or ensure accessibility

### Migration Guide
📄 **Read:** [references/migration-guide.md](references/migration-guide.md)
- Migrating from EJ1 Sparkline to EJ2
- API property mapping and changes
- Breaking changes and deprecated features
- Finding equivalents for legacy functionality
- When to read: You're upgrading from an older Syncfusion version

## Quick Start Example

Here's a minimal example to render a basic sparkline:

```typescript
import { SparklineModule } from '@syncfusion/ej2-angular-charts'
import { Component } from '@angular/core';

@Component({
  imports: [SparklineModule],
  standalone: true,
  selector: 'app-container',
  template: `<ejs-sparkline 
    id='sparkline-container'
    [dataSource]="data"
    xName="x"
    yName="y"
    type="Line">
  </ejs-sparkline>`
})
export class AppComponent {
  data = [
    { x: 'Jan', y: 2 },
    { x: 'Feb', y: 6 },
    { x: 'Mar', y: 4 },
    { x: 'Apr', y: 8 },
    { x: 'May', y: 5 }
  ]
}
```

**Output:** A simple line sparkline showing the trend across months.

## Common Patterns

### Pattern 1: Sparkline in a Table Cell

Embed a sparkline within a grid or table to show trends for each row:

```html
<table>
  <tr>
    <td>Product A</td>
    <td><ejs-sparkline [dataSource]="salesA" type="Column" height="50px" width="150px"></ejs-sparkline></td>
  </tr>
  <tr>
    <td>Product B</td>
    <td><ejs-sparkline [dataSource]="salesB" type="Column" height="50px" width="150px"></ejs-sparkline></td>
  </tr>
</table>
```

### Pattern 2: Highlight Key Points with Markers

Show markers on high and low points to emphasize performance peaks:

```typescript
@Component({
  template: `<ejs-sparkline 
    [dataSource]="data"
    type="Line"
    [markerSettings]="markerSettings">
  </ejs-sparkline>`
})
export class HighlightComponent {
  data = [10, 25, 15, 35, 20, 30]
  markerSettings = {
    visible: ['High', 'Low'],
    fill: '#FF5733',
    size: 8,
    opacity: 1
  }
}
```

### Pattern 3: Add Tooltip for Details

Enable tooltip to show exact values on hover with custom formatting:

```typescript
import { SparklineModule, SparklineTooltipService } from '@syncfusion/ej2-angular-charts'

@Component({
  imports: [SparklineModule],
  standalone: true,
  providers: [SparklineTooltipService],
  template: `<ejs-sparkline 
    [dataSource]="data"
    xName="month"
    yName="sales"
    [tooltipSettings]="tooltipSettings">
  </ejs-sparkline>`
})
export class TooltipComponent {
  data = [
    { month: 'Jan', sales: 10000 },
    { month: 'Feb', sales: 15000 }
  ]
  tooltipSettings = { 
    visible: true,
    format: '${month}: ${sales} units'
  }
}
```

### Pattern 4: Range Bands for Thresholds

Display shaded regions to show acceptable performance ranges:

```typescript
@Component({
  template: `<ejs-sparkline 
    [dataSource]="data"
    type="Area"
    [rangeBandSettings]="rangeBandSettings">
  </ejs-sparkline>`
})
export class RangeBandComponent {
  data = [20, 30, 25, 35, 28, 32, 40]
  rangeBandSettings = [
    { startRange: 25, endRange: 35, color: '#90EE90', opacity: 0.3 },  // Good range
    { startRange: 15, endRange: 25, color: '#FFD700', opacity: 0.3 }   // Warning range
  ]
}
```

### Pattern 5: Event Handling

Handle sparkline events for user interactions:

```typescript
@Component({
  template: `<ejs-sparkline 
    [dataSource]="data"
    (pointRegionMouseClick)="onPointClick($event)"
    (sparklineMouseClick)="onSparklineClick($event)">
  </ejs-sparkline>`
})
export class EventComponent {
  data = [10, 25, 15, 35, 20]
  
  onPointClick(args: any) {
    console.log('Point clicked:', args.pointIndex, args.value)
  }
  
  onSparklineClick(args: any) {
    console.log('Sparkline clicked')
  }
}
```

## Key Props

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `dataSource` | Array | `[]` | Data array (primitives or objects) - binds data to sparkline |
| `xName` | string | - | Object property name for X values (e.g., 'month', 'date') |
| `yName` | string | - | Object property name for Y values (e.g., 'sales', 'count') |
| `type` | string | `'Line'` | Sparkline type: Line, Column, Area, Pie, WinLoss |
| `markerSettings` | object | - | Configure marker display and style (High, Low, Start, End, Negative, All) with fill, border, size, opacity properties |
| `dataLabelSettings` | object | - | Configure data label display with visible array, format string, fill color, border, textStyle, and edgeLabelMode |
| `tooltipSettings` | object | - | Tooltip configuration (visible, format with ${x}/${y} tokens, fill, border, textStyle, trackLineSettings) |
| `height` | string/number | `'100px'` | Container height in px (e.g., '150px') or percentage (e.g., '100%') |
| `width` | string/number | `'100%'` | Container width in px (e.g., '300px') or percentage (e.g., '100%') |
| `rangeBandSettings` | object/array | - | Configure background shading regions (startRange, endRange, color, opacity) - supports single object or array for multiple bands |
| `axisSettings` | object | - | Axis configuration (minX, maxX, minY, maxY, intervalX, intervalY, valueType: Numeric/Category/DateTime) |
| `highPointColor` | string | - | Color for highest point in data series (hex or named color) |
| `lowPointColor` | string | - | Color for lowest point in data series (hex or named color) |
| `startPointColor` | string | - | Color for first/start point in the series |
| `endPointColor` | string | - | Color for last/end point in the series |
| `negativePointColor` | string | - | Color for negative data values (below zero) |
| `fill` | string | - | Fill color for the sparkline area/column/bars (primary series color) |
| `lineWidth` | number | 1 | Thickness of line type sparkline (1-10 range recommended) |
| `opacity` | number | 1 | Opacity of the sparkline series (0-1 range) |
| `enableRtl` | boolean | false | Enable Right-to-Left layout for RTL languages (Arabic, Hebrew) |
| `valueType` | string | 'Numeric' | Data type for axis values: Numeric, Category, DateTime |
| `format` | string | - | Number format for axis values (e.g., 'n2' for 2 decimals, 'c' for currency) |
| `useGroupingSeparator` | boolean | false | Enable thousand separator formatting (e.g., 1,000) |
| `theme` | string | 'Material' | Visual theme: Material, Fabric, Bootstrap, HighContrast, etc. |
| `border` | object | - | Border configuration (color, width) for sparkline container |
| `containerArea` | object | - | Container customization (background color, border settings) |
| `padding` | object | - | Padding for sparkline (left, right, top, bottom in pixels) |

## Common Use Cases

1. **Dashboard Metrics** - Display mini charts showing KPI trends in real-time dashboards and metrics views. Ideal for executive dashboards with multiple metrics displayed in a compact grid layout.

2. **Financial Data Visualization** - Visualize stock prices, trading volumes, or currency trends with range bands for support/resistance zones. Use markers to highlight significant price points and tooltips for detailed values.

3. **Performance Monitoring** - Show system metrics (CPU, memory, disk usage, network throughput) monitored over 24-hour periods. Color-code negative spikes and use range bands to show acceptable operating ranges.

4. **Data Table Integration** - Embed sparklines within data grid cells to compare performance trends across multiple products, users, or regions in table rows. Each row shows its own mini trend visualization.

5. **Win-Loss Analysis** - Track success/failure outcomes (pass/fail, approved/rejected, win/loss) in a compact binary format using the WinLoss type. Perfect for game results, test outcomes, or approval workflows.

6. **Time Series Condensed View** - Display historical data in a condensed format with trend visualization. Show weekly, monthly, or yearly patterns without taking up significant screen space.

7. **Sales Pipeline Tracking** - Show monthly/quarterly sales trends by product category or sales territory. Use different sparkline types to represent different metrics (revenue as Area, units as Column).

8. **User Activity Analytics** - Track engagement metrics (page visits, active users, session duration) over specific time periods. Identify patterns and anomalies with marker highlighting.

9. **Quality Metrics Dashboard** - Display defect rates, uptime percentages, or quality scores across production batches. Use range bands to show acceptable quality zones and markers to flag outliers.

10. **Resource Utilization Monitoring** - Monitor bandwidth consumption, storage capacity trends, or license usage patterns at a glance. Set axis bounds to show capacity limits and use color-coded points for threshold breaches.

11. **IoT Sensor Data** - Display real-time sensor readings (temperature, humidity, pressure) in compact charts within IoT monitoring dashboards. Show 24-hour trends for each sensor in minimal space.

12. **Social Media Analytics** - Track follower growth, engagement rates, or post reach over time. Use Pie sparklines to show proportional engagement across different platforms.

---

**Next Steps:** Start with [getting-started.md](references/getting-started.md) to install and render your first sparkline, then explore other reference guides based on your needs.

## API Reference

A concise API reference for the Syncfusion Angular `Sparkline` is available in the `references` folder. It includes property anchors, method links, and event argument types mapped to the official docs.

Read the API reference: [references/api-reference.md](references/api-reference.md)
