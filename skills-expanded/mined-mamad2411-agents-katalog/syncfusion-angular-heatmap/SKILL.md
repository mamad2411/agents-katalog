---
name: syncfusion-angular-heatmap
description: Implement Syncfusion Angular HeatMap Chart component for visualizing two-dimensional data with color gradients. Use this skill whenever users need to create heatmaps, visualize data matrices, display data with color-coded cells, configure axes (numeric/categorical/datetime), add legends, customize colors and rendering modes, handle cell selection and events, or implement accessibility features. Includes data binding, axis types, interactive selection, tooltips, and bubble heatmaps.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing HeatMap

The HeatMap Chart component is a powerful visualization tool for displaying two-dimensional data where values are represented through color gradients or fixed colors. Perfect for analyzing patterns, correlations, and distributions in matrix data, time-series heatmaps, and any scenario requiring color-encoded data representation.

## When to Use This Skill

- **Data Matrix Visualization:** Display 2D data arrays with color-coded cells
- **Correlation Analysis:** Visualize relationships between multiple variables
- **Time-Series Heatmaps:** Show patterns over time (e.g., hourly/daily activity)
- **Category Comparison:** Compare performance across categories and metrics
- **Intensity Mapping:** Display heatmaps with gradient colors representing value intensity
- **Interactive Selection:** Enable user selection of cells with tooltips and event handling
- **Accessibility Requirements:** Implement WCAG-compliant heatmaps with ARIA support
- **Custom Styling:** Apply themes, palettes, and custom rendering (SVG/Canvas)
- **Bubble Heatmaps:** Visualize data as bubbles with size and color encoding
- **Large Datasets:** Handle auto-switching between SVG and Canvas rendering modes

## Component Overview

HeatMap is a flexible, high-performance visualization component with rich customization:
- **Axis Types:** Numeric, Categorical, and DateTime axes
- **Data Binding:** JSON arrays and 2D matrix formats
- **Rendering Modes:** Auto-switching SVG (small data) and Canvas (large data)
- **Interactive Features:** Cell selection, tooltips, data labels, events
- **Customization:** Color palettes, themes, cell styling, borders
- **Accessibility:** WCAG compliance, ARIA attributes, keyboard navigation
- **Legend Support:** Automatic and custom legend rendering
- **Bubble Variant:** Alternative bubble heatmap visualization
- **Standalone Ready:** Compatible with Angular 19+ standalone components

## Documentation and Navigation Guide

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)

### Getting Started & Installation
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installing @syncfusion/ej2-angular-heatmap package
- Module imports for Angular standalone and traditional modules
- Creating your first heatmap
- Basic data binding setup
- Verifying installation works

### Data Binding & Formats
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- JSON array format for structured data
- 2D array format for matrix data
- DataManager for remote data
- Binding x/y axis fields
- Live data updates and dynamic binding

### Axes Configuration
📄 **Read:** [references/axes-configuration.md](references/axes-configuration.md)
- X/Y axis types: Numeric, Categorical, DateTime
- Axis labels, titles, and intervals
- Inverted axes and opposed positions
- Axis customization and properties
- Working with date/time data

### Legend Rendering
📄 **Read:** [references/legend-rendering.md](references/legend-rendering.md)
- Legend positioning and alignment
- Legend sizing and appearance
- Custom legend data display
- Interactive legend behavior
- Legend label formatting

### Visual Customization & Rendering
📄 **Read:** [references/visual-customization.md](references/visual-customization.md)
- Color palettes and themes
- SVG vs Canvas rendering modes
- Cell styling and borders
- Gradient and fixed colors
- Bubble heatmap variations
- Responsive design

### Interactivity, Events & Accessibility
📄 **Read:** [references/interactivity-events.md](references/interactivity-events.md)
- Cell selection modes and events
- Tooltip customization and templating
- Data labels and formatting
- Cell click and selection handlers
- WCAG accessibility compliance
- ARIA attributes and keyboard navigation
- Screen reader support

### Advanced Features & How-tos
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- EJ1 to EJ2 migration guide
- How-to: Custom tooltip templates
- How-to: Legend customization
- How-to: Performance optimization for large datasets
- Combining selection with data updates
- Multi-dimensional data representation

## Quick Start

### Minimal HeatMap Setup

```typescript
import { Component, ViewEncapsulation } from '@angular/core';
import { HeatMapModule } from '@syncfusion/ej2-angular-heatmap';

@Component({
    imports: [HeatMapModule],
    standalone: true,
    selector: 'app-heatmap',
    template: `
        <ejs-heatmap id='heatmap-container' 
            [dataSource]='dataSource'
            [xAxis]='xAxis'
            [yAxis]='yAxis'>
        </ejs-heatmap>
    `,
    encapsulation: ViewEncapsulation.None
})
export class HeatMapComponent {
    dataSource: any[] = [
        { ProductName: 'Milk', Year: 2005, Sales: 21, Quarter: 'Q1' },
        { ProductName: 'Milk', Year: 2006, Sales: 22, Quarter: 'Q1' },
        { ProductName: 'Milk', Year: 2007, Sales: 23, Quarter: 'Q1' },
        { ProductName: 'Bread', Year: 2005, Sales: 18, Quarter: 'Q1' },
        { ProductName: 'Bread', Year: 2006, Sales: 19, Quarter: 'Q1' },
        { ProductName: 'Bread', Year: 2007, Sales: 20, Quarter: 'Q1' }
    ];

    xAxis: any = {
        labels: ['2005', '2006', '2007'],
        type: 'Labels',
        opposedPosition: true
    };

    yAxis: any = {
        labels: ['Milk', 'Bread'],
        type: 'Labels'
    };
}
```

## Common Patterns

### Pattern 1: Sales Performance Matrix
Display product sales by year with color gradient representing performance levels.

```typescript
dataSource = [
    { Product: 'Product A', Year: 2020, Sales: 50 },
    { Product: 'Product A', Year: 2021, Sales: 75 },
    { Product: 'Product B', Year: 2020, Sales: 60 },
    { Product: 'Product B', Year: 2021, Sales: 85 }
];

xAxis = { labels: ['2020', '2021'], type: 'Labels' };
yAxis = { labels: ['Product A', 'Product B'], type: 'Labels' };
```

**When:** Comparing performance metrics across multiple dimensions  
**Why:** Color-coded cells make patterns immediately visible

### Pattern 2: Time-Series Activity Heatmap
Show hourly or daily activity patterns with DateTime axis.

```typescript
<ejs-heatmap [xAxis]='{ type: "DateTime", intervalType: "Days" }'
    [yAxis]='{ labels: ["12 AM", "1 AM", "2 AM", "3 AM"] }'>
</ejs-heatmap>
```

**When:** Analyzing time-based patterns (traffic, usage, activity)  
**Why:** DateTime axis automatically formats and scales time data

### Pattern 3: Interactive Cell Selection
Enable users to select cells and respond to selection events.

```typescript
<ejs-heatmap [cellSettings]='{ border: { width: 1 } }'
    (cellSelected)='onCellSelect($event)'
    [allowSelection]='true'>
</ejs-heatmap>

onCellSelect(event: any) {
    console.log('Selected cell:', event.cellCollection);
}
```

**When:** Building interactive dashboards with drill-down capability  
**Why:** Selection events enable dynamic filtering and detail views

### Pattern 4: Custom Tooltip with Data Labels
Display detailed information on hover and within cells.

```typescript
<ejs-heatmap [tooltip]='{ enable: true }'>
    <e-heatmap-cellsettings [showLabel]='true' 
        [labelFormat]='{ format: "{value}" }'>
    </e-heatmap-cellsettings>
</ejs-heatmap>
```

**When:** Users need detailed values without clicking  
**Why:** Tooltips reduce cognitive load while maintaining clean appearance

### Pattern 5: Bubble Heatmap Variation
Use bubbles instead of cells for alternative visualization.

```typescript
<ejs-heatmap [renderingMode]='BubbleHeatMap'>
    <e-heatmap-cellsettings showLabel='true' bubbleType='Size'>
    </e-heatmap-cellsettings>
</ejs-heatmap>
```

**When:** Emphasizing value magnitude through bubble size  
**Why:** Bubble size adds an additional visual dimension

## Key Props

### Data and Axes
- `dataSource`: Array of data objects (JSON format)
- `xAxis`: X-axis configuration (Labels, Numeric, DateTime)
- `yAxis`: Y-axis configuration (Labels, Numeric, DateTime)
- `valueBound`: Range of color gradient values [min, max]
- `cellSettings`: Cell appearance and labels

### Legend and Display
- `legendSettings`: Legend positioning, alignment, and appearance
- `palette`: Color scheme array or predefined theme
- `title`: Heatmap title
- `height`, `width`: Chart dimensions

### Interactivity
- `allowSelection`: Enable/disable cell selection
- `cellSelected`: Event fired on cell selection
- `cellRender`: Customize cell appearance
- `cellHover`: Hover event for cells
- `tooltipSettings`: Tooltip display configuration

### Rendering
- `renderingMode`: SVG or Canvas mode
- `cellBorder`: Cell border configuration
- `showGradientLegend`: Display gradient legend

## Common Use Cases

### Use Case 1: Product Performance Dashboard
Display quarterly sales metrics across products using a heatmap. Color intensity shows performance level. Users click cells to see drill-down details.

### Use Case 2: Server Activity Monitor
Track server CPU/memory usage by hour of day and day of week. Time-series heatmap with DateTime axes. Auto-switching Canvas mode for large datasets.

### Use Case 3: Correlation Matrix
Visualize statistical correlations between multiple variables. Color gradients represent correlation strength. Hover tooltips show exact values.

### Use Case 4: Website Traffic Heatmap
Analyze visitor traffic patterns by page and time. Bubble heatmap shows traffic volume. Selection enables filtering by time periods.

