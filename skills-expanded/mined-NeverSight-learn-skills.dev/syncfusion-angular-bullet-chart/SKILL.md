---
name: syncfusion-angular-bullet-chart
description: Implement Syncfusion Angular Bullet Chart component for performance comparison visualizations. Use this when displaying actual vs target values, defining quality ranges, customizing axes and labels, or creating accessible performance indicators. Covers getting started, data binding, axes configuration, visual elements, and customization.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing Syncfusion Angular Bullet Chart

## When to Use This Skill

Use this skill when you need to:
- Create a Bullet Chart component in an Angular application
- Display performance data with actual vs target comparisons
- Define and customize quality ranges (good, satisfactory, poor)
- Customize axes, labels, and data visualization elements
- Add accessibility features and keyboard navigation
- Configure tooltips, data labels, and animations
- Change chart orientation or apply themes

## Component Overview

The **Syncfusion Angular Bullet Chart** is a specialized data visualization component designed for comparing actual values against target values. It's ideal for displaying performance metrics, progress tracking, and goal achievement visualization. The component displays:

- **Value Bar (Actual Bar)**: The primary data measurement (feature measure)
- **Target Bar (Comparative Bar)**: The goal or benchmark value
- **Ranges**: Color-coded zones representing quality levels (Good, Satisfactory, Poor)
- **Axis**: Configurable scale for data values
- **Labels & Tooltips**: Additional context and information on hover

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup (`@syncfusion/ej2-angular-charts`)
- Basic Bullet Chart initialization
- Angular CLI setup for Angular 21+
- Standalone component architecture
- Module injection for features (tooltips, etc.)
- Adding data source and basic configuration

### Data Binding and Sources
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- Local data binding for static datasets
- Remote data binding for dynamic data
- Data source structure and field mapping
- Mapping valueField and targetField
- Dynamic data updates

### Axes and Ranges Configuration
📄 **Read:** [references/axes-and-ranges.md](references/axes-and-ranges.md)
- Major and minor tick customization
- Tick placement (inside/outside)
- Label formatting (number, percentage, currency)
- Axis label positioning and customization
- Category labels and custom label styles
- Opposed position for right-aligned axes
- Range definition and color customization
- Quality range visualization (Good, Satisfactory, Poor)

### Visual Elements and Data Display
📄 **Read:** [references/visual-elements.md](references/visual-elements.md)
- Value bar styling and shape customization (Rect, Dot)
- Border and fill customization for actual bars
- Target bar types (Circle, Cross, Rect)
- Target bar color and width customization
- Data labels configuration and styling
- Tooltip setup and customization
- Tooltip templates with custom HTML
- Title and subtitle positioning
- Chart dimensions (pixels, percentage)

### Customization and Styling
📄 **Read:** [references/customization.md](references/customization.md)
- Horizontal vs Vertical orientation
- Right-to-left (RTL) support
- Animation configuration (duration, delay)
- Theme selection and application
- CSS customization approaches
- Responsive design patterns

### Accessibility Features
📄 **Read:** [references/accessibility.md](references/accessibility.md)
- WCAG 2.2, Section 508, and ADA compliance
- Keyboard navigation (Tab, Shift+Tab, Ctrl+P)
- Screen reader support and WAI-ARIA attributes
- Color contrast standards
- Mobile device support

## Quick Start Example

Here's a minimal working example:

```typescript
import { Component, OnInit } from '@angular/core';
import { BulletChartModule, BulletTooltipService } from '@syncfusion/ej2-angular-charts';

@Component({
    imports: [BulletChartModule],
    standalone: true,
    selector: 'app-container',
    template: `<ejs-bulletchart 
        [dataSource]='data' 
        valueField='value' 
        targetField='target'
        [tooltip]='{ enable: true }'
        title='Sales Performance'
        [ranges]='ranges'>
    </ejs-bulletchart>`,
    providers: [BulletTooltipService]
})
export class AppComponent implements OnInit {
    public data: any;
    public ranges: any;

    ngOnInit(): void {
        this.data = [
            { value: 100, target: 80 },
            { value: 200, target: 180 }
        ];
        
        this.ranges = [
            { end: 50, color: '#ffe0b2', opacity: 0.6 },    // Poor
            { end: 100, color: '#fff9c4', opacity: 0.6 },   // Satisfactory
            { end: 150, color: '#c8e6c9', opacity: 0.6 }    // Good
        ];
    }
}
```

## Common Patterns

### Pattern 1: Sales Performance Dashboard
When displaying sales metrics against targets:
```typescript
data = [
    { category: 'Q1', value: 25000, target: 30000 },
    { category: 'Q2', value: 28000, target: 30000 },
    { category: 'Q3', value: 35000, target: 30000 }
];

ranges = [
    { end: 20000, color: '#ffe0b2' },      // Below Target
    { end: 30000, color: '#fff9c4' },      // On Target
    { end: 40000, color: '#c8e6c9' }       // Above Target
];
```

### Pattern 2: Employee Performance Ratings
When comparing individual performance scores:
```typescript
data = [
    { name: 'Alice', value: 85, target: 80 },
    { name: 'Bob', value: 72, target: 80 },
    { name: 'Charlie', value: 90, target: 80 }
];
```

### Pattern 3: KPI Tracking with Orientation
When space is limited or vertical display is preferred:
```typescript
<ejs-bulletchart orientation='Vertical' ...></ejs-bulletchart>
```

## Key Properties

| Property | Type | Purpose |
|----------|------|---------|
| `dataSource` | Array | Array of data objects containing value and target fields |
| `valueField` | String | Property name for actual/feature measure value |
| `targetField` | String | Property name for target/comparative measure value |
| `ranges` | Array | Array of range objects defining quality zones |
| `title` | String | Title displayed at the top of chart |
| `subtitle` | String | Subtitle for additional context |
| `orientation` | String | 'Horizontal' (default) or 'Vertical' |
| `tooltip` | Object | Configuration for hover tooltips |
| `dataLabel` | Object | Configuration for value labels |
| `type` | String | Shape of value bar: 'Rect' (default) or 'Dot' |
| `targetTypes` | String | Shape of target bar: 'Rect', 'Circle', or 'Cross' |
| `width` | String/Number | Chart width in pixels or percentage |
| `height` | String/Number | Chart height in pixels or percentage |
| `theme` | String | Theme name (Material, Fabric, Bootstrap, Tailwind, etc.) |
| `enableRtl` | Boolean | Enable right-to-left rendering |
| `animation` | Object | Configuration for entrance animations |

## Common Use Cases
## API Reference

A complete API reference for the Syncfusion Angular `BulletChart` is available in the `references` folder. It lists component properties, methods, events, and usage notes that match the official API docs.

Read the full API reference here: [references/api-reference.md](references/api-reference.md)

1. **Sales Performance Tracking**: Display actual sales vs target with quality zones
2. **Quality Metrics**: Monitor production quality against benchmarks
3. **HR Metrics**: Track employee performance against goals
4. **Budget Analysis**: Compare actual spending vs budgeted amounts
5. **Learning Progress**: Show student progress toward learning objectives
6. **Health Metrics**: Display health indicators against recommended values
7. **Project Status**: Track project metrics against planned targets

---

**Next Steps:** Choose the reference file that matches your immediate need based on the guidance above, or start with [getting-started.md](references/getting-started.md) if this is your first time using Bullet Chart.
