---
name: syncfusion-aspnetcore-lineargauge
description: Implement Syncfusion Linear Gauge component to visualize numerical values in a linear manner with support for pointers, ranges, annotations, and interactive features. Use this skill to create responsive gauge controls with customizable appearance, animations, and accessibility.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Gauges"
---

# Implementing Syncfusion Linear Gauge

## When to Use This Skill

Use this skill when you need to:
- Display numerical values in a linear gauge format (temperature, speed, performance metrics)
- Create interactive gauges with draggable pointers
- Visualize ranges and thresholds on a linear scale
- Add annotations and custom elements to gauges
- Implement dashboard gauges with real-time data updates
- Build thermometer-style or progress indicator components

## Component Overview

The Linear Gauge component visualizes numerical values of an axis in a linear manner. All elements are rendered using Scalable Vector Graphics (SVG). Key features include:

- **Multiple pointers** - Support for Marker and Bar pointer types
- **Range highlighting** - Define color ranges to highlight value zones
- **Annotations** - Add text, images, or HTML elements anywhere on the gauge
- **Interactive features** - Drag-and-drop pointers, tooltips, and events
- **Animations** - Smooth pointer animations on load and value changes
- **Customization** - Colors, themes, borders, scales, and container types (Normal, RoundedRectangle, Thermometer)
- **Accessibility** - WCAG 2.2 compliance with screen reader support
- **Print & Export** - Print and export gauge images

## Quick Start Example

Here's a minimal Linear Gauge implementation:

```cshtml
<!-- ASP.NET Core Tag Helper -->
<ejs-lineargauge id="linear" title="Temperature Gauge" orientation="Horizontal">
    <e-lineargauge-axes>
        <e-lineargauge-axis minimum="0" maximum="200">
            <e-lineargauge-ranges>
                <e-lineargauge-range start="0" end="50" color="blue"></e-lineargauge-range>
                <e-lineargauge-range start="50" end="150" color="green"></e-lineargauge-range>
                <e-lineargauge-range start="150" end="200" color="red"></e-lineargauge-range>
            </e-lineargauge-ranges>
            <e-lineargauge-pointers>
                <e-lineargauge-pointer value="75" type="Bar"></e-lineargauge-pointer>
            </e-lineargauge-pointers>
        </e-lineargauge-axis>
    </e-lineargauge-axes>
</ejs-lineargauge>
```

## Common Patterns

**Pattern 1: Temperature Display**
- Vertical orientation with thermometer container
- Range colors: blue (cold), green (normal), red (hot)
- Single bar pointer for current temperature

**Pattern 2: Progress Indicator**
- Horizontal orientation with percentage values
- Single range from 0-100
- Bar pointer showing completion percentage

**Pattern 3: Dashboard Metric**
- Horizontal orientation with multiple ranges
- Marker pointers for actual vs target values
- Annotations for labels and notes

**Pattern 4: Real-Time Monitoring**
- Event binding to `ValueChange` event
- Pointer animation with specified duration
- Tooltip for hover information

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup
- Basic linear gauge implementation
- CSS imports and theme configuration
- Initial configuration and rendering

### Gauge Dimensions
📄 **Read:** [references/gauge-dimensions.md](references/gauge-dimensions.md)
- Container size and dimensions (pixel vs percentage)
- Orientation (horizontal/vertical)
- Sizing configurations
- Responsive behavior and margin control

### Ranges and Values
📄 **Read:** [references/ranges-and-values.md](references/ranges-and-values.md)
- Range definitions and colors
- Multiple ranges configuration
- Value binding and axis scaling
- Minimum/maximum values
- Range styling and gradient colors

### Pointers and Indicators
📄 **Read:** [references/pointers-and-indicators.md](references/pointers-and-indicators.md)
- Pointer types and styles (Marker, Bar)
- Marker shapes (Circle, Rectangle, Triangle, Diamond, Image, Text)
- Animation and movement
- Multiple pointers
- Pointer styling and customization

### Appearance and Styling
📄 **Read:** [references/appearance-and-styling.md](references/appearance-and-styling.md)
- Visual customization
- Container types (Normal, RoundedRectangle, Thermometer)
- Colors and themes
- Title styling
- Borders and scales
- Label customization

### Interactions and Events
📄 **Read:** [references/interactions-and-events.md](references/interactions-and-events.md)
- Click events and drag operations
- Value change events
- Animation complete events
- Mouse events (down, move, up, leave)
- Tooltip rendering and handling

### Annotations
📄 **Read:** [references/annotations.md](references/annotations.md)
- Adding text and image annotations
- Positioning annotations (x, y coordinates)
- Z-index and layering
- Horizontal and vertical alignment
- Multiple annotations

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Accessibility (WCAG 2.2, screen readers)
- Print and export functionality
- Internationalization (i18n)
- API methods and properties
- RTL support

### Examples and Use Cases
📄 **Read:** [references/examples-and-use-cases.md](references/examples-and-use-cases.md)
- Dashboard gauges
- Speed indicators
- Temperature displays
- Performance metrics
- Real-world patterns and best practices
