---
name: syncfusion-angular-3d-chart
description: Implement interactive 3D charts in Angular applications using Syncfusion. Guide covers setup, chart types (bar, column, stacked variants), customization, data binding, axis configuration, legends, tooltips, selection, data labels, appearance styling, dimensions, print/export, and accessibility. Use this skill whenever a user needs to create, configure, or customize 3D chart visualizations.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing Syncfusion Angular 3D Chart

## When to Use This Skill

Use this skill when you need to:
- **Create a 3D chart** from scratch in an Angular application
- **Display data** in interactive 3D visualizations (bar, column, stacked variants)
- **Customize chart appearance**, colors, and styling
- **Configure axes** with different types (category, numeric, datetime, logarithmic)
- **Add interactive features** like tooltips, selection, data labels, and legends
- **Implement data binding** with local or remote data
- **Export or print** charts as images or PDFs
- **Ensure accessibility** for screen readers and keyboard navigation
- **Work with dimensions** and 3D perspective settings

---

## Component Overview

The **Syncfusion Angular 3D Chart** component provides a comprehensive solution for creating interactive three-dimensional data visualizations. It supports multiple chart types (bar, column, stacked configurations), advanced customization options, and robust data binding capabilities. The component is designed for Angular 21+ with standalone architecture and includes accessibility features, keyboard navigation, and multiple export formats.

### Key Capabilities
- **Multiple Chart Types:** Bar, Column, Stacked Bar, Stacked Column
- **Axis Types:** Category, Numeric, DateTime, Logarithmic
- **Interactive Features:** Tooltips, selection modes, data labels, legends
- **Customization:** Colors, themes, styling, 3D dimensions
- **Data Binding:** Local arrays, remote data sources, dynamic updates
- **Export/Print:** PNG, SVG, PDF formats
- **Accessibility:** WCAG compliance, ARIA attributes, keyboard support

---

## Documentation and Navigation Guide

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup
- Create your first 3D chart
- Basic component configuration
- CSS and theme imports
- Minimal working example

### Chart Types & Configuration
📄 **Read:** [references/chart-types.md](references/chart-types.md)
- Bar chart implementation
- Column chart implementation
- Stacked column configuration
- Stacked bar configuration
- Switching between chart types
- Series configuration

### Axis & Data Setup
📄 **Read:** [references/axis-customization.md](references/axis-customization.md)
- Category axis setup
- Numeric axis configuration
- DateTime axis setup
- Logarithmic axis support
- Multi-pane configurations

📄 **Read:** [references/axis-labels.md](references/axis-labels.md)
- Label formatting and display
- Label positioning and rotation
- Custom label templates
- Label appearance customization

### Data & Labels
📄 **Read:** [references/data-labels.md](references/data-labels.md)
- Enable and position data labels
- Label formatting options
- Custom data label templates
- Conditional label display

📄 **Read:** [references/working-with-data.md](references/working-with-data.md)
- Data binding approaches (arrays, objects)
- Category data configuration
- Remote data loading
- Real-time data updates
- Data refresh patterns

### Appearance & Styling
📄 **Read:** [references/appearance.md](references/appearance.md)
- Custom color palettes
- Point color customization
- Series styling options
- Theme application

📄 **Read:** [references/dimensions.md](references/dimensions.md)
- 3D depth and perspective control
- Chart width and height configuration
- Rotation and tilt settings
- Wall and corner customization

### Interactive Features
📄 **Read:** [references/tool-tip.md](references/tool-tip.md)
- Enable and configure tooltips
- Tooltip templates and formatting
- Custom styling options
- Tooltip events and interactions

📄 **Read:** [references/selection.md](references/selection.md)
- Point selection modes
- Multiple selection configurations
- Selection styling
- Selection events

📄 **Read:** [references/legend.md](references/legend.md)
- Enable and position legends
- Legend customization
- Custom legend items
- Legend interactions

### Advanced Features
📄 **Read:** [references/print-export.md](references/print-export.md)
- Export as PNG, SVG, PDF
- Print functionality
- Export configuration options
- File naming and paths

📄 **Read:** [references/accessibility.md](references/accessibility.md)
- WCAG 2.1 compliance guidelines
- Keyboard navigation support
- ARIA attributes and labels
- Screen reader optimization
- Color contrast and visual accessibility

---

## Quick Start Example

Here's a minimal example to get you started:

```typescript
import { Component } from '@angular/core';
import { Chart3DComponent, Chart3DSeriesCollectionDirective, Chart3DSeriesDirective } from '@syncfusion/ej2-angular-charts';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [Chart3DComponent, Chart3DSeriesCollectionDirective, Chart3DSeriesDirective],
  template: `
    <ejs-chart3d [primaryXAxis]="xAxis" [primaryYAxis]="yAxis">
      <e-chart3d-series-collection>
        <e-chart3d-series [dataSource]="chartData" xName="month" yName="sales" type="Column">
        </e-chart3d-series>
      </e-chart3d-series-collection>
    </ejs-chart3d>
  `
})
export class AppComponent {
  chartData = [
    { month: 'Jan', sales: 35 },
    { month: 'Feb', sales: 28 },
    { month: 'Mar', sales: 34 },
    { month: 'Apr', sales: 32 },
    { month: 'May', sales: 40 }
  ];

  xAxis = { valueType: 'Category' };
  yAxis = { labelFormat: '{value}%' };
}
```

---

## Common Patterns

### Pattern 1: Dynamic Data Binding
When user needs real-time updates, bind data to a property and use change detection:

```typescript
@Component({
  template: `
    <ejs-chart3d [primaryXAxis]="xAxis">
      <e-chart3d-series-collection>
        <e-chart3d-series [dataSource]="dynamicData" xName="x" yName="y" type="Column">
        </e-chart3d-series>
      </e-chart3d-series-collection>
    </ejs-chart3d>
  `
})
export class DynamicChartComponent {
  dynamicData: any[] = [];

  constructor() {
    this.loadData();
    setInterval(() => this.loadData(), 5000); // Update every 5 seconds
  }

  loadData() {
    this.dynamicData = this.generateData();
  }

  private generateData() {
    return [
      { x: 'A', y: Math.random() * 100 },
      { x: 'B', y: Math.random() * 100 }
    ];
  }
}
```

### Pattern 2: Multiple Chart Types
When user needs to switch between visualization types:

```typescript
export class MultiTypeChartComponent {
  chartType: string = 'Column';

  switchChartType(type: string) {
    this.chartType = type; // Changes 'type' in series
  }
}
```

### Pattern 3: Custom Color Palette
When user wants brand-specific colors:

```typescript
@Component({
  template: `
    <ejs-chart3d [palettes]="customPalette">
      ...
    </ejs-chart3d>
  `
})
export class CustomPaletteComponent {
  customPalette = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8'];
}
```

---

## Key Props Reference

| Prop | Type | Purpose |
|------|------|---------|
| `primaryXAxis` | AxisModel | Configures X-axis (type, labels, range) |
| `primaryYAxis` | AxisModel | Configures Y-axis (type, labels, range) |
| `dataSource` | any[] | Array of data objects for chart |
| `xName` | string | Data property for X values |
| `yName` | string | Data property for Y values |
| `type` | string | Chart type (Column, Bar, StackedColumn, StackedBar) |
| `name` | string | Series name for legend |
| `palettes` | string[] | Custom color array for series |
| `enableTooltip` | boolean | Show tooltips on hover |
| `legendSettings` | LegendSettings | Configure legend appearance and behavior |
| `tooltip` | TooltipSettings | Customize tooltip template and styling |
| `marker` | MarkerSettings | Configure data point markers |
| `dataLabel` | DataLabelSettings | Enable and format data labels |

---

## Common Use Cases

1. **Sales Dashboard:** Display monthly sales by region using stacked columns
2. **Inventory Analytics:** Compare stock levels across warehouses using bar charts
3. **Performance Tracking:** Visualize KPIs over time with multiple series
4. **Comparative Analysis:** Side-by-side data comparison using grouped columns
5. **Trend Analysis:** Track changes across categories with animated transitions
6. **Budget vs. Actual:** Compare planned vs. actual spending using stacked configurations

---

For more information, visit the [Syncfusion Angular 3D Chart Documentation](https://ej2.syncfusion.com/angular/documentation/chart-3d/chart-types/).
