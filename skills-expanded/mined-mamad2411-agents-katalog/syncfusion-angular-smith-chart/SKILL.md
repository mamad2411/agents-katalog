---
name: syncfusion-angular-smith-chart
description: Implement Syncfusion Angular Smith Chart component for high-frequency circuit visualization and transmission line analysis. Use this skill whenever the user needs to create smith charts, visualize impedance or admittance parameters, add multiple series to a smith chart, customize axes and gridlines, configure markers and data labels, implement legends with visibility toggling, add tooltips and export functionality, or styling and accessibility. Covers installation, basic rendering, series management, axis configuration, marker/label customization, legend setup and advanced features.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing Syncfusion Angular Smith Chart Component

## When to Use This Skill

Use this skill when you need to:
- **Visualize transmission lines** - Plot impedance or admittance parameters on smith charts for circuit analysis
- **Create smith charts** - Render smith chart components with proper configuration and data binding
- **Add multiple series** - Display multiple transmission line series on a single chart
- **Customize axes** - Configure horizontal and radial axes with custom labels, gridlines, and styling
- **Highlight data points** - Add markers and data labels to emphasize key values
- **Display legends** - Implement legends with positioning, alignment, and visibility toggling
- **Enable interactivity** - Add tooltips, print functionality, and event handling
- **Style and theme** - Apply Syncfusion themes, custom colors, and responsive sizing
- **Ensure accessibility** - Support WCAG compliance, keyboard navigation, and RTL layouts

## Component Overview

The **Syncfusion Angular Smith Chart** is a specialized data visualization component for high-frequency circuit applications. It uses two sets of concentric circles (constant resistance and reactance) to plot transmission line parameters for impedance and admittance analysis.

**Key Characteristics:**
- **Dual-axis system** - Horizontal axis (straight line for resistance) and radial axis (circular path for reactance)
- **Render Types** - Support for both `Impedance` (default) and `Admittance` parameters
- **Multi-series support** - Display multiple transmission line series simultaneously with different colors and styles
- **Data binding** - Two methods: `points` array or `dataSource` with `resistance`/`reactance` property mapping
- **Interactive elements** - Markers, data labels, tooltips, legends with visibility toggle, and export functionality
- **Customizable styling** - Axis labels, major/minor gridlines, colors, themes (Material, Bootstrap, Tailwind), responsive sizing
- **Accessibility features** - WCAG compliance, keyboard navigation, RTL (right-to-left) support, screen reader compatibility
- **Event-driven** - Load events, series rendering, legend interactions, and tooltip customization
- **Export capabilities** - PNG, JPEG, SVG formats for reporting and documentation

## Documentation and Navigation Guide

This skill guides you through implementing smith charts. Here are the key topics:

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup for Angular 19+
- Basic smith chart component implementation
- Module injection requirements
- Data binding with resistance and rectangle values
- CSS imports and theming
- When to read: Before implementing your first smith chart

### Series and Data Management
📄 **Read:** [references/series-and-data.md](references/series-and-data.md)
- Understanding series concepts and data structure
- Points vs dataSource for data input
- Impedance and Admittance render types
- Series customization (fill, opacity, width, visibility)
- Multiple series examples and patterns
- Smart labels and overlapping prevention
- When to read: Bind data and configure multiple series

### Axis Customization
📄 **Read:** [references/axis-customization.md](references/axis-customization.md)
- Horizontal and radial axis configuration
- Axis labels (positioning, intersection handling, styling)
- Major and minor gridlines (visibility, width, dash patterns, opacity)
- Axis line customization
- Label and value formatting
- When to read: Customize axis appearance and behavior

### Markers and Data Labels
📄 **Read:** [references/markers-and-labels.md](references/markers-and-labels.md)
- Marker configuration and visibility
- Data label display and formatting
- Positioning markers and labels without overlap
- Custom label content (resistance, reactance values)
- Formatting numeric values
- When to read: Highlight specific data points or show detailed values

### Legend and Interaction
📄 **Read:** [references/legend-and-interaction.md](references/legend-and-interaction.md)
- Legend visibility and positioning (top, bottom, left, right, custom)
- Legend alignment and placement
- Legend shape customization (circle, rectangle, triangle)
- Legend sizing and responsiveness
- Series visibility toggle with legend clicks
- When to read: Add and configure legends for series identification

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Tooltip configuration and formatting
- Print and export functionality
- RTL (Right-to-Left) support
- Theming and CSS customization
- Container sizing and responsive behavior
- WCAG accessibility compliance
- Keyboard navigation
- Event handling (click, hover, legend toggle)
- When to read: Implement complex features like tooltips, export, events, or accessibility

### Troubleshooting
📄 **Read:** [references/troubleshooting.md](references/troubleshooting.md)
- Common implementation issues and solutions
- Data format validation and errors
- Module import troubleshooting
- Performance optimization tips
- Chart rendering and display issues
- When to read: Debug issues or optimize chart performance

## Quick Start Example

Here's a minimal example to render a basic smith chart:

```typescript
import { SmithchartModule } from '@syncfusion/ej2-angular-charts'
import { Component } from '@angular/core';

@Component({
  imports: [SmithchartModule],
  standalone: true,
  selector: 'app-container',
  template: `<ejs-smithchart 
    id='smithchart-container'
    [series]="series">
  </ejs-smithchart>`
})
export class AppComponent {
  series = [{
    points: [
      { resistance: 10, reactance: 10 },
      { resistance: 20, reactance: 15 },
      { resistance: 30, reactance: 5 },
      { resistance: 40, reactance: -5 },
      { resistance: 50, reactance: -15 }
    ]
  }]
}
```

**Output:** A basic smith chart with one series showing transmission line impedance values.

## Common Patterns

### Pattern 1: Multi-Series Transmission Line Comparison

Display multiple transmission line series with different colors for impedance comparison:

```typescript
series = [
  {
    name: 'Transmission Line A',
    points: [
      { resistance: 0.2, reactance: 0.1 },
      { resistance: 0.5, reactance: 0.3 },
      { resistance: 1.0, reactance: 0.5 }
    ],
    fill: '#0066CC',
    marker: { visible: true },
    tooltip: { visible: true }
  },
  {
    name: 'Transmission Line B',
    points: [
      { resistance: 0.3, reactance: 0.15 },
      { resistance: 0.6, reactance: 0.4 },
      { resistance: 1.2, reactance: 0.6 }
    ],
    fill: '#FF6633',
    marker: { visible: true },
    tooltip: { visible: true }
  }
]
```

### Pattern 2: Interactive Tooltips, Legends, and Markers

Enable legends for series identification, tooltips for detailed values, and markers to highlight data points:

```typescript
@Component({
  template: `
    <ejs-smithchart [series]="series" [legendSettings]="legendSettings">
    </ejs-smithchart>
  `
})
export class AppComponent {
  series = [
    {
      name: 'Device A',
      marker: { 
        visible: true, 
        shape: 'Circle', 
        width: 8,
        height: 8,
        dataLabel: { visible: true }  // ✓ dataLabel INSIDE marker
      },
      tooltip: { visible: true, template: 'R:${resistance}+jX:${reactance}' },
      points: [...]
    }
  ];

  legendSettings = { 
    visible: true, 
    position: 'Bottom',
    alignment: 'Center' 
  };
}
```

### Pattern 3: Admittance Render Type with Axis Customization

Switch to Admittance rendering and customize axes with gridlines:

```typescript
@Component({
  template: `
    <ejs-smithchart 
      [series]="series"
      [horizontalAxis]="hAxis"
      [radialAxis]="rAxis">
    </ejs-smithchart>
  `
})
export class AppComponent {
  series = [
    {
      points: [...],
      renderType: 'Admittance'
    }
  ];

  hAxis = {
    labelPosition: 'Outside',
    majorGridlines: { visible: true, width: 1, opacity: 0.8 },
    minorGridlines: { visible: true, count: 4, opacity: 0.4 }
  };

  rAxis = {
    majorGridlines: { visible: true, width: 1, opacity: 0.8 },
    minorGridlines: { visible: true, count: 4, opacity: 0.4 }
  };
}
```

### Pattern 4: Data-Driven Series from External Source

Bind series data from an array using dataSource property:

```typescript
series = [
  {
    name: 'Test Results',
    dataSource: [
      { impedance: 50, phase: 0 },     // Will be mapped to resistance/reactance
      { impedance: 75, phase: 15 },
      { impedance: 100, phase: 30 }
    ],
    resistance: 'impedance',
    reactance: 'phase'
  }
];
```

### Pattern 5: Export and Print Integration

Enable export and print functionality for documentation:

```typescript
@Component({
  template: `
    <div>
      <button (click)="exportChart('PNG')">Export PNG</button>
      <button (click)="exportChart('SVG')">Export SVG</button>
      <button (click)="printChart()">Print</button>
    </div>
    <ejs-smithchart #smithchart [series]="series"></ejs-smithchart>
  `
})
export class AppComponent {
  @ViewChild('smithchart') smithchart!: any;

  exportChart(format: string) {
    this.smithchart.export(format, 'smith-chart-export');
  }

  printChart() {
    this.smithchart.print();
  }
}

## Import Best Practices

### ✅ Minimal Imports (Most Cases)

For basic smith charts without advanced features, import only what you need:

```typescript
import { SmithchartModule } from '@syncfusion/ej2-angular-charts'
import { Component, ViewEncapsulation } from '@angular/core'

@Component({
  imports: [SmithchartModule],  // ✓ Only SmithchartModule needed
  standalone: true,
  encapsulation: ViewEncapsulation.None,
  template: `<ejs-smithchart [series]="series"></ejs-smithchart>`
})
export class AppComponent {
  series = [{ points: [...] }]
}
```

### ❌ Don't Import Unnecessary Modules

Avoid importing modules/services you're not using:

```typescript
// ✗ WRONG - CommonModule not needed in standalone component
import { CommonModule } from '@angular/common'
@Component({
  imports: [SmithchartModule, CommonModule],  // CommonModule is unnecessary
  standalone: true
})

// ✗ WRONG - SmithchartLegendService not needed without custom legend events
import { SmithchartLegendService } from '@syncfusion/ej2-angular-charts'
@Component({
  providers: [SmithchartLegendService],  // Only for custom legend click handling
  standalone: true
})
export class AppComponent {
  legendSettings = { visible: true }  // Basic legend doesn't need the service
}

// ✗ WRONG - TooltipRenderService not needed without tooltips
import { TooltipRenderService } from '@syncfusion/ej2-angular-charts'
@Component({
  providers: [TooltipRenderService],  // Only needed if tooltip: { visible: true }
  standalone: true
})
export class AppComponent {
  series = [{ points: [...] }]  // No tooltip configuration
}
```

### ✅ Add Services Only When Needed

| Use Case | Service | Import |
|----------|---------|--------|
| Basic chart | None | Only `SmithchartModule` |
| With tooltips | `TooltipRenderService` | Add when using `tooltip: { visible: true }` |
| Advanced legend clicks | `SmithchartLegendService` | Add when handling legend interaction events |

**Example: Tooltips Only When Used**
```typescript
import { SmithchartModule, TooltipRenderService } from '@syncfusion/ej2-angular-charts'

@Component({
  imports: [SmithchartModule],
  providers: [TooltipRenderService],  // ✓ Add only if using tooltips
  standalone: true
})
export class AppComponent {
  series = [{
    points: [
      { resistance: 0.2, reactance: 0.1 },
      { resistance: 0.4, reactance: 0.3 }
    ],
    tooltip: { visible: true }  // ✓ Tooltips are configured
  }]
}
```

## Key Configuration Properties

| Property | Type | Default | Purpose |
|----------|------|---------|---------|
| `series` | Array | `[]` | Array of series with points data for visualization |
| `points` | Array | - | Data array for a series (resistance, reactance pairs) |
| `dataSource` | Array | - | Bind data from external source or data array |
| `resistance` | string | - | Property name for X-axis value (resistance) from dataSource |
| `reactance` | string | - | Property name for Y-axis value (reactance) from dataSource |
| `name` | string | - | Series name for legend display |
| `renderType` | string | `'Impedance'` | Render type: `'Impedance'` or `'Admittance'` |
| `fill` | string | - | Series line color (hex or named color) |
| `width` | number | 2 | Series line width in pixels |
| `opacity` | number | 1 | Series line opacity (0-1) |
| `marker` | object | - | Marker configuration (visible, shape, size) |
| `dataLabel` | object | - | Data label configuration (visible, format) |
| `tooltip` | object | - | Tooltip configuration (visible, format, template) |
| `title` | object | - | Title configuration (text, visible, styling) |
| `height` | string/number | '400px' | Chart height (px or percentage) |
| `width` | string/number | '100%' | Chart width (px or percentage) |
| `theme` | string | `'Material'` | Built-in theme (Material, Bootstrap, Tailwind, etc.) |
| `legendSettings` | object | - | Legend configuration (visible, position, alignment) |
| `horizontalAxis` | object | - | Horizontal axis customization and labels |
| `radialAxis` | object | - | Radial axis customization and gridlines |
| `enableRtl` | boolean | `false` | Enable right-to-left text direction support |
| `ariaLabel` | string | - | Accessibility label for screen readers |

## Common Use Cases

1. **Circuit Analysis & Impedance Matching** - Visualize impedance matching and transmission line characteristics for high-frequency circuits
2. **Network & Filter Tuning** - Display multiple filter responses and network parameters for comparison and optimization
3. **Antenna Design & Optimization** - Plot impedance curves for antenna tuning, SWR analysis, and frequency response visualization
4. **RF Engineering** - Analyze reflection coefficients, standing wave patterns, and transmission line properties
5. **Microwave Engineering** - Design and analyze transmission lines, waveguides, and microwave components
6. **Educational Content** - Teach high-frequency circuit concepts with interactive charts and real-time parameter visualization
7. **Performance Dashboards** - Monitor multiple transmission line metrics and network parameters in real-time
8. **Device Testing & Validation** - Compare measured vs. simulated impedance data for device characterization
9. **Quality Control** - Visualize production test results for electronic components on smith charts
10. **Signal Integrity Analysis** - Analyze termination impedance and signal reflection for PCB design verification

---

## API Reference

A complete API reference for the Syncfusion Angular `Smithchart` is available in the `references` folder. It includes property anchors, method links, and event argument types that map to the official docs.

Read the API reference: [references/api-reference.md](references/api-reference.md)

**Next Steps:** Start with [getting-started.md](references/getting-started.md) to install and render your first smith chart, then explore other reference guides based on your needs.
