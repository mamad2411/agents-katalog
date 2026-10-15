---
name: syncfusion-aspnetcore-stock-chart
description: Create and configure Syncfusion Stock Chart controls in ASP.NET Core applications. Use this skill when building financial data visualizations with stock charts, candlestick series, technical indicators, or trading dashboards. Covers setup, series types, data binding, legends, indicators, and user interactions.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
  category: "Data Visualization"
---

# Implementing Syncfusion Stock Chart

Syncfusion Stock Chart is a specialized data visualization control designed for displaying financial market data with support for multiple series types, technical indicators, and interactive features.

## When to Use This Skill

Use this skill when you need to:
- Display stock price data with candlestick, line, or OHLC charts
- Add technical analysis indicators (moving averages, RSI, Bollinger Bands, etc.)
- Create interactive trading dashboards with zoom, selection, and tooltips
- Implement range and period selectors for time-based filtering
- Visualize trend lines and stock events on financial charts
- Customize chart appearance with themes and gradients

## Component Overview

The Stock Chart component provides:
- **6 series types** for different data visualization needs
- **10 technical indicators** for financial analysis
- **Interactive features** like crosshairs, tooltips, and zoom
- **Legend and axis customization** for flexible layouts
- **Stock events and trend lines** for annotations
- **Export and print capabilities** for reporting
- **Period and range selectors** for time-based navigation
- **Annotations** for custom markings and labels
- **Multiple axes support** for complex layouts

## Documentation and Navigation Guide

### API Reference
📄 **Read:** [references/api-reference.md](references/api-reference.md)
- Complete API documentation for Stock Chart component
- Constructor and property definitions
- Event properties and callbacks
- Configuration options and usage patterns
- Related settings classes and data structures

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- NuGet package installation and setup
- Creating ASP.NET Core applications
- Tag helper configuration
- Basic control rendering
- Script manager registration

### Series Types & Data Visualization
📄 **Read:** [references/series-types.md](references/series-types.md)
- 6 major series types (Line, Candle, HollowCandle, Spline, Hilo, HiloOpenClose)
- Choosing the right series for your data
- Series configuration and customization
- Data requirements for each series type

### Data Binding & Configuration
📄 **Read:** [references/data-binding.md](references/data-binding.md)
- DataSource configuration and binding
- DateTime vs Numeric axes
- OHLC data structure
- Financial data formatting
- Date-based axis configuration

### Legend Customization
📄 **Read:** [references/legend-customization.md](references/legend-customization.md)
- Enabling and disabling legends
- Legend positioning (Left, Right, Top, Bottom, Custom)
- Legend alignment (Center, Near, Far)
- Custom positioning with coordinates
- Legend visibility toggling

### Technical Indicators
📄 **Read:** [references/technical-indicators.md](references/technical-indicators.md)
- 10 indicator types (AccumulationDistribution, ATR, EMA, SMA, TMA, Momentum, MACD, RSI, Stochastic, BollingerBand)
- Adding and removing indicators
- Indicator configuration and customization
- Overbought/oversold thresholds
- Volume-based indicators

### User Interactions
📄 **Read:** [references/user-interactions.md](references/user-interactions.md)
- Crosshairs and trackballs
- Selection modes for data points
- Tooltip configuration
- Zoom and scroll interactions
- Interactive feature customization

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Trend lines (linear, exponential, polynomial, etc.)
- Stock events and annotations
- Range selectors for filtering
- Period selectors for time navigation
- Accessibility features

### Customization & Appearance
📄 **Read:** [references/customization-appearance.md](references/customization-appearance.md)
- Chart dimensions and sizing
- Themes and color schemes
- Axis customization
- Gradient fills for visual enhancement
- Export and print options

## Quick Start

```csharp
@{
    var stockData = new[]
    {
        new { x = new DateTime(2023, 1, 1), open = 150, high = 155, low = 145, close = 152, volume = 1000000 },
        new { x = new DateTime(2023, 1, 2), open = 152, high = 158, low = 151, close = 156, volume = 1200000 }
    };
}

<ejs-stockchart id="container">
    <e-stockchart-series-collection>
        <e-stockchart-series dataSource="stockData"
                             xName="x"
                             yName="close"
                             type="Candle">
        </e-stockchart-series>
    </e-stockchart-series-collection>
</ejs-stockchart>
```

## Common Patterns

### Pattern 1: Candlestick Chart with DateTime Axis
Create a financial chart showing OHLC (Open, High, Low, Close) data:

```csharp
<ejs-stockchart id="stockChart">
    <e-stockchart-primaryxaxis 
        valueType="DateTime">
    </e-stockchart-primaryxaxis>
    <e-stockchart-series-collection>
        <e-stockchart-series 
            dataSource="financialData" 
            xName="date" 
            yName="close" 
            type="Candle">
        </e-stockchart-series>
    </e-stockchart-series-collection>
</ejs-stockchart>
```

### Pattern 2: Adding Technical Indicators
Enhance analysis with moving averages:

```csharp
<ejs-stockchart id="stockChart">
    <e-stockchart-indicators>
        <e-stockchart-indicator 
            type="Ema" 
            field="Close" 
            period="14">
        </e-stockchart-indicator>
    </e-stockchart-indicators>
</ejs-stockchart>
```

### Pattern 3: Interactive Features
Enable crosshairs and tooltips for user interaction:

```csharp
<ejs-stockchart id="stockChart">
    <e-stockchart-tooltipsettings enable="true"></e-stockchart-tooltipsettings>
    <e-stockchart-crosshairsettings lineType="Vertical">
        <e-crosshairsettings-line color="red"></e-crosshairsettings-line>
    </e-stockchart-crosshairsettings>
</ejs-stockchart>
```

### Pattern 4: Legend Configuration
Position and customize the legend:

```csharp
<ejs-stockchart id="stockChart">
    <e-stockchart-legendsettings 
        visible="true" 
        position="Bottom" 
        alignment="Center">
    </e-stockchart-legendsettings>
</ejs-stockchart>
```

## Key Properties

### Core Properties
- **dataSource**: Data collection for the chart (array or DataManager)
- **xName**: Property name for X-axis values
- **yName**: Property name for Y-axis values (typically Close price)
- **type**: Series type (Line, Candle, HollowCandle, Spline, Hilo, HiloOpenClose)

### Appearance Properties
- **background**: Chart background color (hex or rgba)
- **theme**: Visual theme (Material, Fabric, Bootstrap, MaterialDark, etc.)
- **width**: Chart width (string with px or %)
- **height**: Chart height (string with px or %)
- **title**: Chart title text
- **isTransposed**: Render chart in transposed manner

### Feature Control Properties
- **enablePeriodSelector**: Show/hide period selector (default: true)
- **enableSelector**: Show/hide range selector (default: true)
- **enableCustomRange**: Allow custom range selection (default: true)
- **enablePersistence**: Persist component state between page reloads
- **enableRtl**: Render in right-to-left direction
- **isMultiSelect**: Enable multiple point selection
- **isSelect**: Enable selection feature

### Export Properties
- **exportType**: Export format types (PNG, SVG, PDF)
- **indicatorType**: Technical indicator types
- **seriesType**: Series type options
- **trendlineType**: Trend line type options

### Configuration Objects
- **annotations**: Annotation settings collection
- **axes**: Secondary axis collection
- **border**: Border color and width settings
- **chartArea**: Chart area border and background
- **crosshair**: Crosshair customization settings
- **legendSettings**: Legend appearance and behavior
- **margin**: Chart margins (left, right, top, bottom)
- **periods**: Period selector options
- **primaryXAxis**: Primary X-axis configuration
- **primaryYAxis**: Primary Y-axis configuration
- **rows**: Multiple plotting area settings
- **selectedDataIndexes**: Pre-selected data points
- **selectionMode**: Selection mode (Point, Series, Cluster, DragXY, DragX, DragY, None)
- **series**: Series collection
- **stockEvents**: Stock event annotations
- **tooltip**: Tooltip settings
- **zoomSettings**: Zoom and pan configuration

### Template Properties
- **locale**: Culture and localization value
- **noDataTemplate**: Template for empty chart display

## Key Events

### Chart Lifecycle Events
- **load**: Triggers before the chart rendering begins
- **loaded**: Triggers after the chart rendering completes
- **beforeExport**: Triggers before export process begins (allows export customization)

### User Interaction Events
- **axisLabelRender**: Triggers before each axis label is rendered
- **pointClick**: Triggers when clicking on a data point
- **pointMove**: Triggers when moving over data points
- **stockChartMouseClick**: Triggers on clicking the chart
- **stockChartMouseDown**: Triggers on mouse down
- **stockChartMouseUp**: Triggers on mouse up
- **stockChartMouseMove**: Triggers on hovering the chart
- **stockChartMouseLeave**: Triggers when cursor leaves the chart
- **onZooming**: Triggers after zoom selection is completed
- **rangeChange**: Triggers when the range is changed

### Rendering Events
- **seriesRender**: Triggers before each series is rendered
- **legendRender**: Triggers before the legend is rendered
- **legendClick**: Triggers after clicking on legend items
- **tooltipRender**: Triggers before the tooltip is rendered
- **crosshairLabelRender**: Triggers before crosshair tooltip is rendered
- **selectorRender**: Triggers before rendering the selector
- **stockEventRender**: Triggers before stock events are rendered

## Common Use Cases

1. **Stock Price Monitoring**: Display real-time stock prices with candlestick charts
2. **Technical Analysis Dashboard**: Combine multiple indicators for trading analysis
3. **Portfolio Overview**: Visualize multiple stocks side-by-side
4. **Historical Price Trends**: Show long-term price movements with smooth line charts
5. **Trading Signals**: Annotate charts with trend lines and stock events
6. **Period-Based Filtering**: Allow users to select time ranges with period selectors

---

## Next Steps

Select the reference file that matches your current task from the Navigation Guide above. Each reference provides complete, self-contained documentation for its specific feature area.
