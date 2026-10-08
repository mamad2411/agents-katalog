---
name: syncfusion-react-sparkline
description: Implement Syncfusion React Sparkline components for compact, inline data visualization. Use this when working with sparklines, mini charts, or trend indicators in constrained spaces. This skill covers all 5 sparkline types (line, column, area, win-loss, pie), tooltips, markers, data labels, range bands, axis customization, and themes. Ideal for displaying data trends within grids, dashboards, or tables without full-sized charts.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
  category: "Data Visualization"
---

# Implementing Syncfusion React Sparklines

A comprehensive guide for implementing Syncfusion React Sparkline components - lightweight, compact charts designed to visualize data trends in minimal space without axes or coordinates.

## When to Use This Skill

Use this skill when you need to:
- Create compact data visualizations in dashboards or grids
- Display trend indicators inline with data
- Implement mini charts that consume minimal space
- Show data patterns in table cells or small containers
- Create any of the 5 sparkline types: Line, Column, Area, Win-Loss, or Pie
- Add tooltips, markers, or data labels to sparklines
- Customize sparkline appearance with themes and colors
- Implement accessible, responsive sparkline visualizations
- Integrate sparklines with grids or other components
- Highlight specific data ranges with range bands

## Component Overview

The Syncfusion React Sparkline is a highly condensed chart component that presents data in a simple, compact format. Key features include:

- **5 Sparkline Types:** Line, Column, Area, Win-Loss, and Pie
- **Interactive Features:** Tooltips with customization and templates, track lines
- **Visual Markers:** Highlight start, end, high, low, and negative points
- **Data Labels:** Display values at specific points with formatting
- **Range Bands:** Highlight specific value ranges along the y-axis
- **Axis Customization:** Support for Numeric, Category, and DateTime value types
- **Themes:** Material, Fabric, Bootstrap, and Highcontrast themes
- **Accessibility:** WCAG 2.2, Section 508 compliance with WAI-ARIA support
- **Grid Integration:** Designed to work seamlessly within grid cells
- **Localization:** Support for internationalization

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Dependencies and package installation (`@syncfusion/ej2-react-charts`)
- Creating React application with Vite
- Adding SparklineComponent to project
- Module injection for tooltip feature
- Binding data source with dataSource property
- Changing sparkline type (Line, Column, Area, Win-Loss, Pie)
- Basic tooltip configuration
- First working example

### Sparkline Types
📄 **Read:** [references/sparkline-types.md](references/sparkline-types.md)
- Overview of all 5 sparkline types
- Line type: Continuous trend visualization
- Column type: Discrete value comparison
- Area type: Filled trend visualization
- Win-Loss type: Binary outcome representation
- Pie type: Proportional data display
- Type selection guide based on data and use case
- Complete examples for each type

### Appearance Customization
📄 **Read:** [references/appearance-customization.md](references/appearance-customization.md)
- Sparkline border configuration with containerArea
- Padding customization (left, right, top, bottom)
- Container background color
- Theme selection (Material, Fabric, Bootstrap, Highcontrast)
- Color and styling best practices
- Visual design guidelines

### Data Labels
📄 **Read:** [references/data-labels.md](references/data-labels.md)
- Enabling data labels for specific points
- Visibility options: All, Start, End, High, Low, Negative
- Customizing fill color, border, opacity, and text styles
- Formatting data label text with format property
- Displaying x and y values together
- Data label positioning and readability

### Markers
📄 **Read:** [references/markers.md](references/markers.md)
- Adding markers to sparkline points
- Marker visibility options: All, Start, End, High, Low, Negative
- Special point marker configuration
- Customizing marker fill, border, size, and opacity
- Combining markers with other features
- Best practices for marker usage

### User Interaction
📄 **Read:** [references/user-interaction.md](references/user-interaction.md)
- Tooltip configuration and SparklineTooltip injection
- Tooltip customization (fill, text styles, format, border)
- Creating custom tooltip templates with HTML
- Track line feature for mouse tracking
- Track line color and styling
- Interactive feature best practices

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Axis customization with valueType (Numeric, Category, DateTime)
- Setting min/max values (minX, maxX, minY, maxY)
- Axis line customization (color, width, opacity, dashArray)
- Range bands for highlighting value ranges
- Multiple range band configuration
- Special points customization (start, end, positive, negative, low)
- Tie point color for Win-Loss sparklines
- Sparkline dimensions (container, pixel, percentage sizing)
- Localization and culture support

### Accessibility
📄 **Read:** [references/accessibility.md](references/accessibility.md)
- WCAG 2.2 and Section 508 compliance
- WAI-ARIA attributes (img role, aria-label, aria-hidden)
- Keyboard interaction (Ctrl + P for printing)
- Screen reader support
- Right-to-left (RTL) support
- Color contrast guidelines
- Mobile device support
- Accessibility testing tools

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Complete API reference for `SparklineComponent`: props, events, methods, child directives, and a usage example (based on the official Syncfusion React Sparkline API).

## Quick Start

### Installation

```bash
npm install @syncfusion/ej2-react-charts --save
```

### Basic Sparkline

```javascript
import { SparklineComponent } from '@syncfusion/ej2-react-charts';
import * as React from 'react';
import * as ReactDOM from 'react-dom';

function App() {
  const data = [0, 6, 4, 1, 3, 2, 5];
  
  return (
    <SparklineComponent
      dataSource={data}
      type="Line"
      height="150px"
      width="300px"
    />
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById('charts'));
```

### Sparkline with Tooltip

```javascript
import { SparklineComponent, Inject, SparklineTooltip } from '@syncfusion/ej2-react-charts';
import * as React from 'react';
import * as ReactDOM from 'react-dom';

function App() {
  const data = [0, 6, 4, 1, 3, 2, 5];
  
  return (
    <SparklineComponent
      dataSource={data}
      type="Area"
      height="150px"
      width="300px"
      tooltipSettings={{ visible: true, format: '${x} : ${y}' }}
    >
      <Inject services={[SparklineTooltip]} />
    </SparklineComponent>
  );
}

export default App;
ReactDOM.render(<App />, document.getElementById('charts'));
```

## Common Patterns

### Column Sparkline with Markers

```javascript
import { SparklineComponent } from '@syncfusion/ej2-react-charts';
import * as React from 'react';
import * as ReactDOM from 'react-dom';

function ColumnSparkline() {
  const data = [3, 6, 4, 1, 3, 2, 5];
  
  return (
    <SparklineComponent
      dataSource={data}
      type="Column"
      height="150px"
      width="300px"
      markerSettings={{ visible: ['High', 'Low'] }}
      highPointColor="green"
      lowPointColor="red"
    />
  );
}

export default ColumnSparkline;
ReactDOM.render(<ColumnSparkline />, document.getElementById('charts'));
```

### Win-Loss Sparkline

```javascript
import { SparklineComponent } from '@syncfusion/ej2-react-charts';
import * as React from 'react';
import * as ReactDOM from 'react-dom';

function WinLossSparkline() {
  const data = [12, 15, -10, 13, 15, 6, -12, 17, 13, 0, 8, -10];
  
  return (
    <SparklineComponent
      dataSource={data}
      type="WinLoss"
      height="150px"
      width="300px"
      tiePointColor="blue"
    />
  );
}

export default WinLossSparkline;
ReactDOM.render(<WinLossSparkline />, document.getElementById('charts'));
```

### Sparkline with Data Labels

```javascript
import { SparklineComponent } from '@syncfusion/ej2-react-charts';
import * as React from 'react';
import * as ReactDOM from 'react-dom';

function SparklineWithLabels() {
  const data = [0, 6, 4, 1, 3, 2, 5];
  
  return (
    <SparklineComponent
      dataSource={data}
      type="Line"
      height="150px"
      width="300px"
      dataLabelSettings={{
        visible: ['Start', 'End'],
        border: { color: 'blue', width: 1 },
        fill: 'blue',
        opacity: 0.4,
        textStyle: { color: 'white' }
      }}
    />
  );
}

export default SparklineWithLabels;
ReactDOM.render(<SparklineWithLabels />, document.getElementById('charts'));
```

### Sparkline with Range Band

```javascript
import { SparklineComponent } from '@syncfusion/ej2-react-charts';
import * as React from 'react';
import * as ReactDOM from 'react-dom';

function SparklineWithRangeBand() {
  const data = [0, 6, 4, 1, 3, 2, 5];
  
  return (
    <SparklineComponent
      dataSource={data}
      type="Area"
      height="150px"
      width="300px"
      rangeBandSettings={[
        { startRange: 1, endRange: 3, color: '#bfd4fc', opacity: 0.4 }
      ]}
    />
  );
}

export default SparklineWithRangeBand;
ReactDOM.render(<SparklineWithRangeBand />, document.getElementById('charts'));
```

## Key Props Reference

| Property | Type | Description |
|----------|------|-------------|
| `dataSource` | object[] | Data for the sparkline |
| `type` | string | Sparkline type: 'Line', 'Column', 'Area', 'WinLoss', 'Pie' |
| `xName` | string | Property name for x-axis from dataSource |
| `yName` | string | Property name for y-axis from dataSource |
| `height` | string | Height of the sparkline |
| `width` | string | Width of the sparkline |
| `fill` | string | Color of the sparkline |
| `valueType` | string | Axis value type: 'Numeric', 'Category', 'DateTime' |
| `markerSettings` | object | Configuration for markers |
| `dataLabelSettings` | object | Configuration for data labels |
| `tooltipSettings` | object | Configuration for tooltips |
| `axisSettings` | object | Axis min/max and line customization |
| `rangeBandSettings` | object[] | Range band configurations |
| `theme` | string | Theme: 'Material', 'Fabric', 'Bootstrap', 'Highcontrast' |
| `padding` | object | Padding around sparkline (left, right, top, bottom) |
| `containerArea` | object | Border and background for sparkline area |

## Common Use Cases

1. **Dashboard Trend Indicators:** Display KPI trends inline with metrics
2. **Grid Integration:** Show mini charts in table cells
3. **Financial Data:** Win-Loss sparklines for stock market gains/losses
4. **Performance Monitoring:** Quick visualization of server metrics or response times
5. **Comparison Views:** Multiple sparklines side-by-side for data comparison
6. **Mobile Dashboards:** Compact visualizations for small screens
7. **Email Reports:** Lightweight charts that render quickly
8. **Real-time Monitoring:** Simple, fast-updating visualizations

## Next Steps

1. **Start with Getting Started:** Read `references/getting-started.md` for installation and basic setup
2. **Choose Your Type:** Read `references/sparkline-types.md` to select the right sparkline type
3. **Customize Appearance:** Read `references/appearance-customization.md` for styling
4. **Add Interactivity:** Read `references/user-interaction.md` for tooltips and track lines
5. **Advanced Configuration:** Read `references/advanced-features.md` for axis, range bands, and more
