---
name: syncfusion-angular-circular-3d-chart
description: Implement interactive 3D circular charts in Angular applications using Syncfusion. Covers pie and donut chart creation, data binding, data labels with positioning and templates, empty points handling, tooltips with custom formatting, legend configuration, titles and subtitles, and print/export functionality (PNG, SVG, PDF). Use this skill when creating 3D circular visualizations for data representation, comparison, and interactive user engagement.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing Syncfusion Angular Circular 3D Chart

## When to Use This Skill

Use this skill when you need to:
- **Create a 3D circular chart** from scratch in an Angular application
- **Display pie and donut charts** for proportional data visualization
- **Add and customize data labels** with positioning and templates
- **Handle empty data points** gracefully in your chart
- **Configure tooltips** with custom formatting and templates
- **Set up and customize legends** for chart interactivity
- **Add titles and subtitles** to your visualizations
- **Export or print charts** as images or PDFs
- **Ensure accessibility** for keyboard navigation and screen readers

---

## Component Overview

The **Syncfusion Angular Circular 3D Chart** component provides a powerful solution for creating three-dimensional pie and donut chart visualizations. It supports multiple data representations with interactive features including smart label positioning, custom data label templates, tooltip formatting, and comprehensive export capabilities. The component is designed for Angular 21+ with standalone architecture and includes accessibility features for inclusive user experiences.

### Key Capabilities
- **Chart Types:** Pie and Donut charts with 3D perspective
- **Data Labels:** Automatic positioning, custom templates, connector lines, formatting options
- **Empty Points:** Intelligent handling of missing or zero-value data points
- **Tooltips:** Custom formatting, headers, and HTML templates
- **Legends:** Configurable positioning, interactions, and styling
- **Titles:** Main title and subtitle support with customization
- **Export/Print:** PNG, SVG, PDF formats with high-quality output
- **Accessibility:** WCAG compliance, keyboard navigation, ARIA attributes

---

## Documentation and Navigation Guide

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup
- Create your first 3D circular chart
- Basic component configuration
- CSS and theme imports
- Minimal working example

### Pie vs Donut Configuration
📄 **Read:** [references/pie-donut-types.md](references/pie-donut-types.md)
- Pie chart implementation
- Donut chart implementation with innerRadius
- Converting between chart types
- Radius customization and various radius charts
- Series configuration and data mapping
- Point color mapping from data source

### Data Labels & Empty Points
📄 **Read:** [references/data-labels-empty-points.md](references/data-labels-empty-points.md)
- Enable and position data labels (inside/outside)
- Data label formatting with templates
- Connector line customization
- Empty point detection and handling
- Point color customization
- Conditional display strategies

### Interactivity: Tooltips, Legends & Selection
📄 **Read:** [references/interactivity-legends-tooltips.md](references/interactivity-legends-tooltips.md)
- Enable and configure tooltips
- Tooltip headers and custom formatting
- Tooltip templates with HTML
- Legend positioning and customization
- Legend interactions (show/hide series)
- Point and series selection

### Appearance, Titles & Styling
📄 **Read:** [references/appearance-titles-styling.md](references/appearance-titles-styling.md)
- Title and subtitle configuration
- Custom color palettes for series
- Point color customization
- Series styling options
- Theme application and customization
- Border and fill styling

### Print, Export & Accessibility
📄 **Read:** [references/print-export-accessibility.md](references/print-export-accessibility.md)
- Export charts as PNG, SVG, PDF
- Print functionality configuration
- WCAG 2.1 compliance guidelines
- Keyboard navigation support
- ARIA attributes and labels
- Screen reader optimization

---

## Quick Start Example

Here's a minimal example to get you started:

```typescript
import { Component } from '@angular/core';
import { CircularChart3DComponent, CircularChartSeriesCollectionDirective, CircularChartSeriesDirective } from '@syncfusion/ej2-angular-charts';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CircularChart3DComponent, CircularChartSeriesCollectionDirective, CircularChartSeriesDirective],
  template: `
    <ejs-circularchart3d id="container" [tooltip]="{ enable: true }">
      <e-circularchart3d-series-collection>
        <e-circularchart3d-series [dataSource]="chartData" xName="x" yName="y" type="Pie">
        </e-circularchart3d-series>
      </e-circularchart3d-series-collection>
    </ejs-circularchart3d>
  `
})
export class AppComponent {
  chartData = [
    { x: 'Product A', y: 25 },
    { x: 'Product B', y: 20 },
    { x: 'Product C', y: 30 },
    { x: 'Product D', y: 25 }
  ];
}
```

---

## Common Patterns

### Pattern 1: Pie Chart with Data Labels
When user needs proportional data visualization with clear labels:

```typescript
@Component({
  template: `
    <ejs-circularchart3d>
      <e-circularchart3d-series-collection>
        <e-circularchart3d-series 
          [dataSource]="data" 
          xName="name" 
          yName="value" 
          type="Pie"
          [dataLabel]="{ visible: true, position: 'Outside', name: 'x' }">
        </e-circularchart3d-series>
      </e-circularchart3d-series-collection>
    </ejs-circularchart3d>
  `
})
export class PieChartComponent {
  data = [
    { name: 'Sales', value: 40 },
    { name: 'Marketing', value: 30 },
    { name: 'Support', value: 20 },
    { name: 'Operations', value: 10 }
  ];
}
```

### Pattern 2: Donut Chart with Legend and Tooltip
When user needs donut visualization with interactivity:

```typescript
export class DonutChartComponent {
  @ViewChild('chart')
  public chart!: CircularChart3DComponent;

  data = [
    { x: 'Chrome', y: 45, color: '#5DADE2' },
    { x: 'Firefox', y: 25, color: '#F39C12' },
    { x: 'Safari', y: 20, color: '#48C9B0' },
    { x: 'Edge', y: 10, color: '#E74C3C' }
  ];

  seriesSettings = {
    dataSource: this.data,
    xName: 'x',
    yName: 'y',
    pointColorMapping: 'color',
    innerRadius: '50%',
    type: 'Pie'
  };

  tooltipSettings = {
    enable: true,
    format: '${point.x}: ${point.y}%'
  };

  legendSettings = {
    visible: true,
    position: 'Bottom'
  };
}
```

### Pattern 3: Chart with Custom Data Label Templates
When user needs formatted labels with dynamic values:

```typescript
export class CustomLabelChartComponent {
  data = [
    { category: 'Jan', sales: 35 },
    { category: 'Feb', sales: 28 },
    { category: 'Mar', sales: 34 }
  ];

  dataLabelTemplate = '<div>${point.x}: ${point.y}K</div>';

  dataLabelSettings = {
    visible: true,
    template: this.dataLabelTemplate,
    position: 'Outside'
  };
}
```

---

## Key Props Reference

| Prop | Type | Purpose |
|------|------|---------|
| `type` | string | Chart type: 'Pie' or 'Donut' |
| `dataSource` | any[] | Array of data objects for chart |
| `xName` | string | Data property for category/label |
| `yName` | string | Data property for values |
| `innerRadius` | string | Donut hole size (0-100%, Pie: 0%, Donut: 40-60%) |
| `radius` | string | Chart radius (default: 80% of min width/height) |
| `pointColorMapping` | string | Data property for point colors |
| `dataLabel` | DataLabelSettings | Label configuration (visible, position, template) |
| `tooltip` | TooltipSettings | Tooltip settings (enable, format, template, header) |
| `legendSettings` | LegendSettings | Legend position and behavior |
| `title` | string | Chart title text |
| `subTitle` | string | Chart subtitle text |
| `enableSmartLabels` | boolean | Auto-arrange labels to avoid overlap (default: true) |
| `emptyPointSettings` | EmptyPointSettings | Handle missing data points |

---

## Common Use Cases

1. **Market Share Distribution:** Visualize product or service market share using pie charts
2. **Budget Allocation:** Show departmental budget breakdown with donut charts
3. **User Demographics:** Display audience distribution by region, age, or other categories
4. **Sales Composition:** Compare sales contribution by product line or territory
5. **Quality Metrics:** Represent quality issue categories as proportions
6. **Survey Results:** Visualize survey response distribution and percentages

---

For more information, visit the [Syncfusion Angular Circular 3D Chart Documentation](https://ej2.syncfusion.com/angular/documentation/circular-chart-3d/circular-chart-types/).
