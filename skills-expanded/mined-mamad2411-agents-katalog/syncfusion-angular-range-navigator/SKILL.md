---
name: syncfusion-angular-range-navigator
description: Implement interactive Range Navigator in Angular applications using Syncfusion. Covers data binding from local and remote sources, axis configuration (numeric and date-time), series types, tooltip customization, period selector setup, lightweight mode, RTL support, axis labels and formatting, grid ticks, print/export functionality (PNG, SVG, PDF), and accessibility features. Use this skill when creating data range selection tools, timeline navigators, and interactive data exploration components.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing Syncfusion Angular Range Navigator

## When to Use This Skill

Use this skill when you need to:
- **Create a Range Navigator component** from scratch in an Angular application
- **Set up data binding** with local arrays or remote data sources
- **Configure date-time or numeric axes** for different data types
- **Customize tooltips** with formatted display and custom templates
- **Implement period selectors** for quick date range selection
- **Add multiple series types** (Area, Line, Spline, StepLine, etc.)
- **Enable lightweight mode** for mobile and performance-optimized applications
- **Support RTL (Right-to-Left)** layouts for international applications
- **Format axis labels** and customize grid ticks
- **Export or print Range Navigator** as images or PDFs
- **Ensure accessibility** with keyboard navigation and ARIA attributes
- **Handle empty data points** and edge cases gracefully

---

## Component Overview

The **Syncfusion Angular Range Navigator** is a powerful data visualization component for browsing, selecting, and navigating through time-series data. It allows users to scroll and select ranges from large datasets and integrates seamlessly with other Syncfusion components like Chart and DataGrid. Designed for Angular 21+ with standalone architecture, it provides multiple axis types, series configurations, interactive tooltips, and comprehensive export/print capabilities.

### Key Capabilities
- **Data Binding:** Local arrays, remote data sources, JSON arrays
- **Axis Types:** Numeric and DateTime axes with custom intervals
- **Series Types:** Area, Line, Spline, StepLine, StepArea with automatic data mapping
- **Tooltips:** Enable/disable, custom formatting, headers, HTML templates
- **Period Selector:** Quick selection buttons (Day, Week, Month, Year, custom ranges)
- **Lightweight Mode:** Optimized for mobile and performance-critical applications
- **Labels & Grid:** Customizable axis labels, grid ticks, label formats
- **RTL Support:** Full right-to-left text and layout support
- **Export/Print:** PNG, SVG, PDF formats with high-quality output
- **Accessibility:** WCAG compliance, keyboard navigation, ARIA attributes

---

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup
- Create your first Range Navigator
- Basic component configuration with data binding
- CSS and theme imports
- Minimal working example
- Module injection and service providers

### Axis Configuration & Types
📄 **Read:** [references/axis-configuration.md](references/axis-configuration.md)
- Numeric axis setup and configuration
- DateTime axis implementation
- Axis interval and range customization
- Axis label formatting
- Axis types comparison and selection guidance
- Custom axis value mapping

### Series Types & Data Binding
📄 **Read:** [references/series-types.md](references/series-types.md)
- Available series types (Area, Line, Spline, StepLine, StepArea)
- Series data binding and xName/yName mapping
- Multiple series configuration
- Series color and style customization
- Data source configuration (local and remote)
- Empty point handling

### Tooltips & Interactivity
📄 **Read:** [references/tooltips-interactivity.md](references/tooltips-interactivity.md)
- Enable and configure tooltips
- Tooltip formatting and headers
- Tooltip templates with HTML
- Custom tooltip content
- Tooltip positioning and behavior
- Range selection events and handling

### Period Selector & Range Selection
📄 **Read:** [references/period-selector.md](references/period-selector.md)
- Period selector configuration
- Built-in period options (Day, Week, Month, Year)
- Custom period ranges
- Period selector styling
- Range selection programmatically
- Event handling for selection changes

### Labels, Ticks & Formatting
📄 **Read:** [references/labels-formatting.md](references/labels-formatting.md)
- Axis label customization and formatting
- Label format strings and custom functions
- Grid tick configuration and styling
- Label positioning and rotation
- Date and number format customization

### Lightweight Mode & Performance
📄 **Read:** [references/lightweight-mode.md](references/lightweight-mode.md)
- Enable lightweight mode for mobile
- Performance considerations and optimization
- Mobile device optimization techniques
- Lightweight mode limitations and features
- When to use lightweight mode vs standard mode

### RTL & Internationalization
📄 **Read:** [references/rtl-internationalization.md](references/rtl-internationalization.md)
- RTL (Right-to-Left) support and configuration
- Component behavior in RTL mode
- Locale and number formatting
- Language-specific configurations
- Multilingual support patterns

### Print, Export & Accessibility
📄 **Read:** [references/print-export-accessibility.md](references/print-export-accessibility.md)
- Export Range Navigator as PNG, SVG, PDF
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
import { RangeNavigatorModule, AreaSeriesService, DateTimeService, RangeTooltipService } from '@syncfusion/ej2-angular-charts';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RangeNavigatorModule],
  providers: [AreaSeriesService, DateTimeService, RangeTooltipService],
  template: `
    <ejs-rangenavigator 
      id="rn-container" 
      [tooltip]="{ enable: true }"
      valueType="DateTime">
      <e-rangenavigator-series-collection>
        <e-rangenavigator-series 
          [dataSource]="chartData" 
          xName="date" 
          yName="value" 
          type="Area">
        </e-rangenavigator-series>
      </e-rangenavigator-series-collection>
    </ejs-rangenavigator>
  `
})
export class AppComponent {
  chartData = [
    { date: new Date(2023, 0, 1), value: 21 },
    { date: new Date(2023, 1, 1), value: 24 },
    { date: new Date(2023, 2, 1), value: 36 },
    { date: new Date(2023, 3, 1), value: 38 }
  ];
}
```

---

## Common Patterns

### Pattern 1: DateTime Range Navigator with Area Series
When user needs to browse time-series data with date range selection:

```typescript
@Component({
  template: `
    <ejs-rangenavigator 
      id="range-navigator"
      [dataSource]="timeSeries" 
      valueType="DateTime"
      [intervalType]="'Months'">
      <e-rangenavigator-series-collection>
        <e-rangenavigator-series 
          xName="date" 
          yName="value" 
          type="Area">
        </e-rangenavigator-series>
      </e-rangenavigator-series-collection>
    </ejs-rangenavigator>
  `
})
export class TimeSeriesComponent {
  timeSeries = [
    { date: new Date(2020, 0, 1), value: 40 },
    { date: new Date(2020, 1, 1), value: 50 },
    { date: new Date(2020, 2, 1), value: 60 }
  ];
}
```

### Pattern 2: Range Navigator with Period Selector
When user needs quick selection buttons for common time periods:

```typescript
@Component({
imports: [
         ChartModule, RangeNavigatorModule
    ],

providers: [ AreaSeriesService, DateTimeService, PeriodSelectorService ],
standalone: true,
    selector: 'app-container',
    template: `<ejs-rangenavigator id="rn-container" valueType='DateTime' [periodSelectorSettings]='periodSelectorConfig'>
            <e-rangenavigator-series-collection>
                <e-rangenavigator-series [dataSource]='chartData' type='Area' xName='x' yName='close' width=2>
                </e-rangenavigator-series>
            </e-rangenavigator-series-collection>
        </ejs-rangenavigator>`
})
export class PeriodSelectorComponent {
  chartData = [...]; // time series data

  periodSelectorConfig = {
    periods: [
      { text: '1M', interval: 1, intervalType: 'Months' },
      { text: '3M', interval: 3, intervalType: 'Months' },
      { text: '6M', interval: 6, intervalType: 'Months' },
      { text: '1Y', interval: 1, intervalType: 'Years' }
    ]
  };

  tooltipSettings = {
    enable: true,
    format: 'MMM dd, yyyy'
  };
}
```

### Pattern 3: Lightweight Range Navigator for Mobile
When user needs optimized Range Navigator for mobile devices:

```typescript
@Component({
  template: `
    <ejs-rangenavigator id="rn-container" valueType='DateTime' [value]='value' [labelFormat]='labelFormat'[dataSource]='mobileData' xName='x' yName='y'>
    </ejs-rangenavigator>
  `
})
export class MobileOptimizedComponent {
  mobileData = [...]; // optimized dataset for mobile
}
```

### Pattern 4: Numeric Axis Range Navigator
When user needs to browse numeric data ranges:

```typescript
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { 
  RangeNavigatorAllModule, 
  AreaSeriesService 
} from '@syncfusion/ej2-angular-charts';

@Component({
  selector: 'app-container',
  standalone: true,
  imports: [CommonModule, RangeNavigatorAllModule],
  providers: [AreaSeriesService],
  template: `
    <div style="padding: 20px;">
      <h2>Numeric Range Selector</h2>
      
      <ejs-rangenavigator 
        id="numericRange"
        [valueType]="rangeSettings.valueType"
        labelFormat="n0">
        <e-rangenavigator-series-collection>
          <e-rangenavigator-series 
            [dataSource]="data" 
            xName="index" 
            yName="value" 
            type="Area">
          </e-rangenavigator-series>
        </e-rangenavigator-series-collection>
      </ejs-rangenavigator>
    </div>
  `
})
export class AppComponent {
  public data = [
    { index: 0, value: 100 },
    { index: 10, value: 150 },
    { index: 20, value: 200 }
  ];

  public rangeSettings = {
    valueType: 'Double'
  };
}
```

### Pattern 5: Range Navigator with Custom Tooltip
When user needs formatted, custom tooltip display:

```typescript
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { 
  RangeNavigatorAllModule, 
  AreaSeriesService 
} from '@syncfusion/ej2-angular-charts';

@Component({
  selector: 'app-container',
  standalone: true,
  imports: [CommonModule, RangeNavigatorAllModule],
  providers: [AreaSeriesService],
  template: `
    <div style="padding: 20px;">
      <h2>Numeric Range Selector</h2>
      
      <ejs-rangenavigator 
        id="numericRange"
        [valueType]="rangeSettings.valueType"
        labelFormat="n0"
        [tooltip]='tooltipSettings'>
        <e-rangenavigator-series-collection>
          <e-rangenavigator-series 
            [dataSource]="data" 
            xName="index" 
            yName="value" 
            type="Area">
          </e-rangenavigator-series>
        </e-rangenavigator-series-collection>
      </ejs-rangenavigator>
    </div>
  `
})
export class CustomTooltipComponent {
  public data = [
    { index: 0, value: 100 },
    { index: 10, value: 150 },
    { index: 20, value: 200 }
  ];

  public rangeSettings = {
    valueType: 'Double'
  };
  tooltipSettings = {
    enable: true,
    template: '<div>${value}</div>',
    header: 'Stock Price'
  };
}

```

---

## Key Props Reference

| Prop | Type | Purpose |
|------|------|---------|
| `valueType` | string | Axis value type: 'Numeric' or 'DateTime' (default: 'DateTime') |
| `dataSource` | any[] | Array of data objects |
| `tooltip` | TooltipSettings | Tooltip settings (enable, format, template) |
| `intervalType` | string | Axis interval: 'Years', 'Months', 'Days', 'Hours', 'Minutes', 'Seconds' |
| `intervals` | number | Interval count for axis labels |
| `labelFormat` | string | Format string for labels (e.g., 'MMM dd, yyyy') |
| `lightWeight` | boolean | Enable lightweight mode (default: false) |
| `enableRtl` | boolean | Enable RTL support (default: false) |
| `series` | RangeNavigatorSeries[] | Series collection configuration |
| `periodSelectorSettings` | PeriodSelectorSettings | Period selector configuration |
| `navigatorStyleSettings` | NavigatorStyleSettings | Style customization |
| `gridLineSettings` | GridLineSettings | Grid tick appearance |
| `labelStyle` | FontModel | Axis label font and style |

---

## API Reference

A complete API reference for the Syncfusion Angular `RangeNavigator` is available in the `references` folder. It includes property anchors, method links, and event argument types that map to the official docs.

Read the API reference: [references/api-reference.md](references/api-reference.md)


## Common Use Cases

1. **Stock Market Data:** Browse historical stock prices with date range selection
2. **Sensor Data Monitoring:** Navigate through time-series sensor readings and metrics
3. **Website Analytics:** Select date ranges for traffic and user behavior analysis
4. **Financial Charts:** Explore financial data with interactive period selection
5. **Application Performance:** Monitor performance metrics over time with quick period selectors
6. **Sales Dashboard:** Review sales data across different time periods
7. **Weather Data:** Browse historical weather patterns with date navigation
8. **IoT Data Visualization:** Navigate through large IoT sensor datasets efficiently

---

## Integration with Other Components

The Range Navigator works seamlessly with other Syncfusion components:

- **Chart Component:** Synchronize Range Navigator selection with main chart display
- **DataGrid:** Filter grid data based on selected date range
- **Stock Chart:** Combine with stock data visualization for enhanced analysis

---

For more information, visit the [Syncfusion Angular Range Navigator Documentation](https://ej2.syncfusion.com/angular/documentation/range-navigator/range-navigator).
