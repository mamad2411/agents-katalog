---
name: syncfusion-angular-circular-gauge
description: Implement Syncfusion Angular Circular Gauge component for radial data visualization. Use this when building circular gauges for dashboards, monitoring displays, performance metrics, speedometers, or KPI indicators. Covers installation, axes configuration, pointer types (needle, range bar, marker), ranges, styling, animations, and user interactions.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing Syncfusion Angular Circular Gauge

## Table of Contents

- [When to Use This Skill](#when-to-use-this-skill)
- [Component Overview](#component-overview)
- [Documentation and Navigation Guide](#documentation-and-navigation-guide)
- [Quick Start Example](quick-start-example)
- [Common Patterns](#common-patterns)
- [Key Concepts](#key-concepts)

## When to Use This Skill

Use the Circular Gauge skill when you need to:

- **Display radial metrics:** Temperature, RPM, speed, pressure, or performance indicators
- **Build dashboards:** KPI dashboards, monitoring systems, real-time data visualization
- **Create speedometer gauges:** Visual representation of continuous values within a range
- **Show progress or status:** Multi-step processes, completion percentages, status indicators
- **Implement interactive gauges:** Draggable pointers, range indicators, user-controlled values
- **Customize gauge appearance:** Multiple styles, themes, animations, and layout options

## Component Overview

Syncfusion's Circular Gauge component provides a flexible, feature-rich control for displaying radial data visualization. Key capabilities include:

| Feature | Description |
|---------|-------------|
| **Axes** | Customizable circular axes with configurable start/end angles, labels, ticks, and ranges |
| **Pointers** | Three pointer types: Needle (with cap/tail), RangeBar (fill-based), Marker (shapes or images) |
| **Ranges** | Colored zones to highlight value intervals with gradient support |
| **Annotations** | Place text, shapes, or images at specific positions on the gauge |
| **Animations** | Smooth animations for gauge elements on load and value changes |
| **User Interaction** | Draggable pointers, tooltips, click events, and dynamic value updates |
| **Responsive Design** | Adapts to container size with flexible sizing options |
| **Multiple Axes** | Support for multiple concurrent axes with independent ranges and pointers |

## Documentation and Navigation Guide

Select the reference that matches your current need:

-### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup (Ivy and ngcc versions)
- Module registration and service providers
- Basic gauge implementation
- Setting pointer values
- Quick integration examples

**When to read:** First time setup, installation issues, basic gauge rendering

### Axes Configuration
📄 **Read:** [references/axes-configuration.md](references/axes-configuration.md)
- Axis customization (line style, background, colors)
- Angles and direction (clockwise/anticlockwise, start/end angles)
- Axis radius (pixel-based and percentage-based sizing)
- Ticks configuration (major/minor ticks, position, offset, styling)
- Labels (font, positioning, formats, angle rotation, smart label handling)
- Minimum/maximum value ranges
- Multiple axes on single gauge

**When to read:** Configuring gauge layout, adjusting tick/label appearance, positioning elements

### Pointers and Types
📄 **Read:** [references/pointers-and-types.md](references/pointers-and-types.md)
- Pointer types overview (Needle, RangeBar, Marker)
- Needle pointers (radius, cap customization, tail length, width variation)
- RangeBar pointers (bar-style indicators, rounded corners)
- Marker pointers (shapes: circle, rectangle, triangle, diamond; custom images)
- Pointer dragging (global enable/disable, individual pointer configuration)
- Multiple pointers on single axis
- Pointer animation (enable, duration, timing)
- Gradient colors (linear and radial gradients)

**When to read:** Choosing pointer type, customizing pointer appearance, adding user interaction

### Ranges and Styling
📄 **Read:** [references/ranges-and-styling.md](references/ranges-and-styling.md)
- Range basics (start/end values, colored zones)
- Range customization (color, thickness, radius)
- Multiple ranges on single axis
- Rounded corner radius for visual polish
- Range positioning (inside/outside axis)
- Range dragging functionality
- Gradient support (linear and radial)
- Applying range colors to ticks and labels

**When to read:** Adding colored zones, creating layered visualizations, styling zones

### Appearance and Animation
📄 **Read:** [references/appearance-and-animation.md](references/appearance-and-animation.md)
- Gauge title (text, font styling, positioning)
- Gauge positioning (centerX, centerY in pixels or percentage)
- Background and border customization
- Margin and spacing configuration
- Gauge dimensions (responsive sizing, fixed dimensions)
- Animation (global animationDuration for all elements, pointer-specific animation)
- Radius calculation for semi/quarter circular gauges
- Creating non-circular gauge layouts

**When to read:** Styling gauge container, enabling animations, creating themed displays

### Annotations and Interaction
📄 **Read:** [references/annotations-and-interaction.md](references/annotations-and-interaction.md)
- Annotations (custom HTML/elements, positioning via radius and angle)
- Sub-gauges (nested gauges within annotations)
- Tooltips (hover information, custom tooltip content)
- User interaction events (pointer drag, value change, gauge interaction)
- Print and export functionality
- Internationalization and localization
- Accessibility features (WCAG compliance, keyboard navigation)

**When to read:** Adding custom content, handling user interactions, accessible gauge implementation

## Quick Start Example

**Basic Circular Gauge with Single Pointer:**

```typescript
import { CircularGaugeModule } from '@syncfusion/ej2-angular-circulargauge';
import { GaugeTooltipService } from '@syncfusion/ej2-angular-circulargauge';
import { Component, ViewEncapsulation } from '@angular/core';

@Component({
  imports: [CircularGaugeModule],
  providers: [GaugeTooltipService],
  standalone: true,
  selector: 'app-gauge',
  template: `
    <ejs-circulargauge id='gauge-container' [title]='title'>
      <e-axes>
        <e-axis [startAngle]='200' [endAngle]='160' [minimum]='0' [maximum]='100'>
          <e-pointers>
            <e-pointer [value]='75' type='Needle'></e-pointer>
          </e-pointers>
        </e-axis>
      </e-axes>
    </ejs-circulargauge>
  `,
  encapsulation: ViewEncapsulation.None
})
export class AppComponent {
  title = 'Speed Gauge';
}
```

**Steps:**
1. Install package: `npm install @syncfusion/ej2-angular-circulargauge`
2. Import `CircularGaugeModule` in component
3. Add services if needed (GaugeTooltipService, etc.)
4. Configure `ejs-circulargauge` with axes and pointers
5. Set pointer `value` and `type`

## Common Patterns

### Pattern 1: Speedometer Display
Create a speedometer gauge with ranges indicating speed zones (safe, warning, danger):

```typescript
// Basic structure:
<ejs-circulargauge>
  <e-axes>
    <e-axis [minimum]='0' [maximum]='200'>
      <!-- Green range (0-80): Safe -->
      <!-- Yellow range (80-150): Caution -->
      <!-- Red range (150-200): Danger -->
      <e-ranges>
        <e-range [start]='0' [end]='80' color='green'></e-range>
        <e-range [start]='80' [end]='150' color='orange'></e-range>
        <e-range [start]='150' [end]='200' color='red'></e-range>
      </e-ranges>
      <e-pointers>
        <e-pointer [value]='speedValue' type='Needle'></e-pointer>
      </e-pointers>
    </e-axis>
  </e-axes>
</ejs-cirulargauge>
```
**Reference:** ranges-and-styling.md (multiple ranges), pointers-and-types.md (needle pointer)

### Pattern 2: Multiple Metrics with Multiple Axes
Display multiple related metrics (inner and outer axes) simultaneously:

```typescript
// Configure multiple axes:
<e-axes>
  <e-axis [radius]='60%'><!-- Outer axis --></e-axis>
  <e-axis [radius]='40%'><!-- Inner axis --></e-axis>
</e-axes>
```
**Reference:** axes-configuration.md (multiple axes section)

### Pattern 3: Interactive Gauge with Draggable Pointers
Allow users to adjust values by dragging the pointer:

```typescript
// Enable dragging globally or per-pointer:
<ejs-circulargauge [enablePointerDrag]='true'>
  <!-- or per-pointer: -->
  <e-pointer [enableDrag]='true'></e-pointer>
</ejs-circulargauge>
```
**Reference:** pointers-and-types.md (dragging pointer section)

### Pattern 4: Animated Gauge Load
Add smooth entrance animations when gauge loads:

```typescript
// Enable animation for all elements:
<ejs-circulargauge [animationDuration]='2000'>
  <!-- Entire gauge animates in over 2 seconds -->
</ejs-circulargauge>
```
**Reference:** appearance-and-animation.md (animation section)

## Key Concepts

### Angles and Direction

The circular gauge rotates in a circular plane. You control the visible arc using:

- **startAngle:** Beginning of the arc (default: 200°)
- **endAngle:** End of the arc (default: 160°)
- **direction:** ClockWise or AntiClockWise

This lets you create full circles (0-360°) or partial gauges (semi-circles, quarter-circles).

### Radius and Sizing

Gauges use flexible sizing:

- **Pixel-based:** Fixed size (e.g., `500px`)
- **Percentage-based:** Relative to container (e.g., `80%`)

Set radius on axes, ranges, pointers, and annotations independently.

### Pointers vs Ranges

- **Pointers:** Show a specific value (like a speedometer needle)
- **Ranges:** Show zones or intervals (like color-coded areas)

Use together for rich visualizations (e.g., pointer shows current speed, ranges show safe/warning zones).

### Animations

Animation affects:
1. Axis line rendering (follows direction)
2. Ticks and labels
3. Ranges
4. Pointers (individual control available)
5. Annotations

Set `animationDuration` in milliseconds (0 = disabled).

### Multiple Pointers & Axes

Support n+ pointers and axes:
- **Multiple pointers:** Show different metrics (humidity + temperature)
- **Multiple axes:** Layers of information (inner/outer rings)

Each axis has independent ranges, pointers, and styling.

---

**Ready to implement?** Start with [getting-started.md](references/getting-started.md) for installation, then navigate to feature-specific references as needed.
