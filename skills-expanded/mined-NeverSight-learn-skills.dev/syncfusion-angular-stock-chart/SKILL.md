---
name: syncfusion-angular-stock-chart
description: Implement Syncfusion Angular Stock Chart component for displaying financial data and OHLC charts. Use this skill whenever users need to create stock charts, display candlestick or OHLC data, add technical indicators, implement date range selection, or work with time-series financial visualization. Includes series types, axis customization, interactive features, and export capabilities.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing Stock Chart

The Stock Chart component is a specialized visualization for displaying financial data over time, including OHLC (Open, High, Low, Close) data, technical indicators, and interactive range selection. Perfect for stock market analysis, cryptocurrency tracking, and any time-series financial data visualization.

## When to Use This Skill

- **Financial Data Visualization:** Display stock prices, cryptocurrency prices, or forex data over time
- **OHLC Charts:** Render candlestick, bar, or line data for price movements
- **Technical Analysis:** Add moving averages, Bollinger Bands, RSI, MACD, and other indicators
- **Date Range Selection:** Allow users to select specific time periods with range or period selectors
- **Interactive Exploration:** Implement crosshairs, tooltips, and dynamic series switching
- **Real-time Updates:** Handle live data feeds with automatic chart updates
- **Export & Sharing:** Generate PNG, SVG, PDF exports or print charts
- **Multi-series Analysis:** Compare multiple financial instruments on the same chart

## Component Overview

Stock Chart is built on Syncfusion's Chart component with specialized features:
- **7 Series Types:** Line, Spline, Area, HiLo, HiLoOpenClose, Hollow Candle, Candle
- **Technical Indicators:** MA, BB, RSI, MACD, Stochastic, and more
- **Interactive Controls:** Range selector, period selector, crosshair, tooltips
- **DateTime Axes:** Automatically handles dates, supports zooming and panning
- **Export Ready:** PNG, SVG, PDF, and print capabilities
- **Standalone Architecture:** Works with Angular 19+ standalone components

## Documentation and Navigation Guide

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)

### Getting Started & Setup
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installing @syncfusion/ej2-angular-charts package
- Initial module imports and providers
- Creating your first stock chart
- Binding data from JSON, API, or DataManager
- Verifying the setup works

### Series Configuration
📄 **Read:** [references/series-types.md](references/series-types.md)
- Understanding 7 series types (Candle, HiLo, Line, Area, etc.)
- When to use each series type for different data
- Configuring series properties and colors
- Switching between series types dynamically
- Multi-series charts

### Axis Customization
📄 **Read:** [references/axis-customization.md](references/axis-customization.md)
- DateTime axis for time-series data
- Numeric and logarithmic axes
- Axis labels, titles, and ranges
- Crosshair and tooltip configuration
- Range zooming and panning

### Legend and Styling
📄 **Read:** [references/legend.md](references/legend.md)
- Enabling and positioning legends
- Legend alignment and sizing
- Custom icon shapes
- Toggling series visibility
- Legend interaction patterns

### Interactive Features
📄 **Read:** [references/interactive-features.md](references/interactive-features.md)
- Range selector (select date ranges)
- Period selector (1M, 3M, 6M, 1Y shortcuts)
- Data labels and formatting
- Tooltip customization
- Crosshair display and interaction
- Events and user actions

### Technical Indicators
📄 **Read:** [references/technical-indicators.md](references/technical-indicators.md)
- Adding technical indicators (MA, BB, RSI, MACD, etc.)
- Indicator calculation parameters
- Multiple indicators on same chart
- Customizing indicator colors and style
- Removing or toggling indicators

### Export and Print
📄 **Read:** [references/export-print.md](references/export-print.md)
- Exporting chart as PNG, SVG, PDF
- Print preview functionality
- Saving exported files
- Batch exporting multiple charts

### Advanced Features & Optimization
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Live data updates and real-time refresh
- Accessibility (WCAG, ARIA, keyboard navigation)
- Internationalization and localization
- Trend lines and annotations
- Performance optimization for large datasets

## Quick Start

### Minimal Stock Chart Setup

```typescript
import { Component, ViewEncapsulation } from '@angular/core';
import { ChartAllModule, StockChartAllModule } from '@syncfusion/ej2-angular-charts';

@Component({
    imports: [ChartAllModule, StockChartAllModule],
    standalone: true,
    selector: 'app-stock-chart',
    template: `
        <ejs-stockchart id='stockchart-container' [dataSource]='data'>
            <e-stockchart-series-collection>
                <e-stockchart-series [dataSource]='data' type='Candle' 
                    xName='x' high='high' low='low' 
                    open='open' close='close'>
                </e-stockchart-series>
            </e-stockchart-series-collection>
        </ejs-stockchart>
    `,
    encapsulation: ViewEncapsulation.None
})
export class StockChartComponent {
    data: any[] = [
        { x: new Date(2023, 0, 1), open: 100, high: 105, low: 95, close: 102 },
        { x: new Date(2023, 0, 2), open: 102, high: 108, low: 100, close: 105 },
        { x: new Date(2023, 0, 3), open: 105, high: 110, low: 103, close: 108 }
    ];
}
```

## Common Patterns

### Pattern 1: Candlestick Chart with DateTime Axis
Render OHLC data as candlesticks with automatic date formatting on the x-axis.

```typescript
<ejs-stockchart>
    <e-stockchart-series-collection>
        <e-stockchart-series type='Candle' xName='date' 
            high='high' low='low' open='open' close='close'>
        </e-stockchart-series>
    </e-stockchart-series-collection>
</ejs-stockchart>
```

**When:** Displaying stock OHLC data, analyzing price patterns  
**Why:** Candlesticks show open/close relationship at a glance

### Pattern 2: Multiple Series with Range Selector
Compare different indicators or instruments with date range selection.

```typescript
<ejs-stockchart [rangeSelector]='{ periods: [{text: "1M", interval: 1, intervalType: "Months"}, 
    {text: "1Y", interval: 1, intervalType: "Years"}] }'>
    <e-stockchart-series-collection>
        <e-stockchart-series type='Candle'></e-stockchart-series>
        <e-stockchart-series type='Line'></e-stockchart-series>
    </e-stockchart-series-collection>
</ejs-stockchart>
```

**When:** Users need to view different time windows, analyzing trends  
**Why:** Rapid period switching improves exploration efficiency

### Pattern 3: Add Technical Indicator
Display a moving average overlay on price data.

```typescript
<ejs-stockchart>
    <e-stockchart-series-collection>
        <e-stockchart-series type='Candle'></e-stockchart-series>
    </e-stockchart-series-collection>
    <e-indicators>
        <e-indicator type='Sma' field='close' period='14' seriesName='SMA'></e-indicator>
    </e-indicators>
</ejs-stockchart>
```

**When:** Adding moving averages, RSI, or other technical analysis  
**Why:** Indicators help identify trends and signals

### Pattern 4: Interactive Crosshair and Tooltip
Enable detailed value inspection on hover.

```typescript
<ejs-stockchart [crosshair]='{ enable: true, lineType: "Vertical" }' 
    [tooltip]='{ enable: true }'>
    <e-stockchart-series-collection>
        <e-stockchart-series type='Candle'></e-stockchart-series>
    </e-stockchart-series-collection>
</ejs-stockchart>
```

**When:** Users need precise value inspection  
**Why:** Reduces cognitive load, enables data discovery

## Key Props

### Series Configuration
- `type`: Series rendering type (Candle, Line, Area, HiLo, etc.)
- `xName`: Data field for x-axis (dates)
- `high`, `low`, `open`, `close`: OHLC data fields
- `dataSource`: Array of data points or DataManager

### Chart Display
- `height`, `width`: Chart dimensions
- `title`: Chart title
- `legendSettings`: Legend positioning and appearance
- `tooltip`: Value display on hover
- `crosshair`: Crosshair display and behavior

### Interactive Features
- `rangeSelector`: Date range selection buttons
- `periodSelector`: Quick period buttons (1M, 1Y, etc.)
- `zoomSettings`: Chart zooming configuration
- `chartArea`: Chart drawing area dimensions

### Axis Configuration
- `primaryXAxis`: X-axis (typically date/time)
- `primaryYAxis`: Y-axis (price values)
- `secondaryYAxis`: Optional secondary Y-axis for indicators

## Common Use Cases

### Use Case 1: Stock Analysis Dashboard
Display multiple stocks side-by-side with range selector for comparing performance over different periods. Technical indicators (MA, RSI) help identify trend strength.

### Use Case 2: Real-time Cryptocurrency Tracker
Update chart data every few seconds as new price candles form. Live range selector updates to include latest data. Tooltip shows real-time bid/ask spread.

### Use Case 3: Historical Data Analysis
Load complete historical dataset (months/years). Zoom/pan allows detailed inspection of specific periods. Export functionality lets users save analysis.

### Use Case 4: Multi-indicator Technical Analysis
Overlay multiple technical indicators on same price chart. Independent axes for different value ranges. Toggle indicators on/off via legend interaction.
