---
name: syncfusion-angular-linear-gauge
description: Create and customize Syncfusion Angular Linear Gauge components for displaying measurements and metrics. Use this skill when user needs to implement a linear gauge, display scalar values in a linear scale, create measurement interfaces, configure ranges and pointers, add annotations, handle user interactions, or customize gauge appearance. Covers installation, configuration, events, accessibility, printing, and internationalization.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing Syncfusion Angular Linear Gauge

The Linear Gauge is a component used to visualize measurements and metrics on a linear scale. It displays values in a horizontal or vertical bar with ranges, pointers, and labels for clear data representation.

## When to Use This Skill

- **Creating a gauge component**: Display scalar values on a linear scale
- **Measurement interfaces**: Show temperature, pressure, speed, or other metrics
- **Adding ranges**: Define colored zones for different value ranges
- **Configuring pointers**: Show multiple values with different pointer styles
- **Customizing appearance**: Modify colors, fonts, backgrounds, and animations
- **Handling interactions**: Add click, drag, or hover events
- **Adding annotations**: Include text or images to enhance the gauge
- **Exporting and printing**: Generate PNG, PDF, or SVG outputs
- **International support**: Enable i18n and RTL support
- **Accessibility**: Ensure WCAG compliance for accessible interfaces

## Documentation and Navigation Guide

Choose your reference based on what you need to accomplish:

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and npm package setup
- Importing Linear Gauge module
- Creating your first gauge component
- CSS theme imports
- Basic configuration

### Configuring Axes and Scales
📄 **Read:** [references/axis-and-scales.md](references/axis-and-scales.md)
- Axis properties and range setup
- Scale configuration and limits
- Major and minor tick marks
- Label formatting and positioning
- Multiple axes on a single gauge

### Adding Ranges and Pointers
📄 **Read:** [references/ranges-and-pointers.md](references/ranges-and-pointers.md)
- Creating and styling ranges
- Range animations and offsets
- Pointer types (marker and bar)
- Pointer animations and transitions
- Drag-enabled pointers for user input
- Multiple pointers on one gauge

### Customization and Appearance
📄 **Read:** [references/customization-and-appearance.md](references/customization-and-appearance.md)
- Container styling and sizing
- Color schemes and theme application
- Font and label customization
- Borders and shadow effects
- Background and gradient styling
- Custom label templates

### Interaction and Events
📄 **Read:** [references/interaction-and-events.md](references/interaction-and-events.md)
- Mouse event handling
- Click, hover, and drag interactions
- Event callbacks and listeners
- Form integration patterns
- Dynamic value updates from user input

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Print and export functionality (PNG, PDF, SVG)
- Annotations for additional information
- Animation configuration and timing
- Internationalization (i18n) setup
- Right-to-left (RTL) text support
- WCAG accessibility compliance
- Migrating from ej1 to ej2/ej3

### Responsive Design and Dimensions
📄 **Read:** [references/dimensions-and-responsive.md](references/dimensions-and-responsive.md)
- Container sizing and responsive layouts
- Dimension properties
- Print layout considerations
- Mobile-friendly gauge design

## Quick Start

```typescript
import { Component, OnInit } from '@angular/core';
import { LinearGaugeAllModule } from '@syncfusion/ej2-angular-gauges';

@Component({
  selector: 'app-linear-gauge',
  template: `
    <ejs-lineargauge 
      [orientation]="'Horizontal'" 
      [container]="{ width: '100', height: '150' }">
      <e-axes>
        <e-axis [minimum]="0" [maximum]="100" 
                [majorTicks]="majorTicks" 
                [minorTicks]="minorTicks">
          <e-ranges>
            <e-range [start]="0" [end]="30" [color]="'#F6B53F'"></e-range>
            <e-range [start]="30" [end]="70" [color]="'#0DC451'"></e-range>
            <e-range [start]="70" [end]="100" [color]="'#F64C38'"></e-range>
          </e-ranges>
          <e-pointers>
            <e-pointer [value]="45" [type]="'Bar'"></e-pointer>
          </e-pointers>
        </e-axis>
      </e-axes>
    </ejs-lineargauge>
  `
})
export class LinearGaugeComponent implements OnInit {
  majorTicks = { interval: 20 };
  minorTicks = { interval: 5 };

  ngOnInit(): void {
    // Component initialized
  }
}
```

## Common Patterns

### Pattern 1: Temperature Gauge
Display current temperature with hot/cold zones.

```typescript
<e-axis [minimum]="0" [maximum]="50">
  <e-ranges>
    <e-range [start]="0" [end]="15" [color]="'#3498db'" ></e-range>
    <e-range [start]="15" [end]="30" [color]="'#2ecc71'" ></e-range>
    <e-range [start]="30" [end]="50" [color]="'#e74c3c'" ></e-range>
  </e-ranges>
  <e-pointers>
    <e-pointer [value]="currentTemp" [type]="'Marker'"></e-pointer>
  </e-pointers>
</e-axis>
```

### Pattern 2: Interactive Gauge
Allow users to drag the pointer to change values.

```typescript
<e-pointer 
  [value]="gaugeValue" 
  [type]="'Bar'" 
  enableDrag=true
  [markerType]="'Circle'"
  (dragEnd)='dragEnd($event)'>
</e-pointer>

dragEnd(args: IPointerDragEventArgs): void {
  this.gaugeValue = event.currentValue;
  console.log('Gauge value changed to:', this.gaugeValue);
}
```

### Pattern 3: Multiple Pointers
Compare multiple values on the same scale.

```typescript
<e-pointers>
  <e-pointer [value]="actualValue" [type]="'Bar'" [color]="'#0066cc'"></e-pointer>
  <e-pointer [value]="targetValue" [type]="'Marker'" [color]="'#ff6600'"></e-pointer>
</e-pointers>
```

## Key Props and Configuration

| Property | Type | Purpose |
|----------|------|---------|
| `orientation` | 'Horizontal' \| 'Vertical' | Direction of the gauge |
| `container.width` | number | Gauge width (e.g., '100', '300') |
| `container.height` | number | Gauge height (e.g., '150') |
| `axes[].minimum` | number | Minimum value on scale |
| `axes[].maximum` | number | Maximum value on scale |
| `ranges[].start` | number | Range start value |
| `ranges[].end` | number | Range end value |
| `ranges[].color` | string | Range color (hex or named) |
| `pointers[].value` | number | Current pointer value |
| `pointers[].type` | 'Bar' \| 'Marker' | Pointer visual style |
| `animationDuration` | number | Enable pointer animations, if greater than 0 |
| `print()` | method | Export as PNG/PDF |
