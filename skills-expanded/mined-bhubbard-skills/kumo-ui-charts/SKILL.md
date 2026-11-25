---
name: kumo-ui-charts
description: Guide for using Kumo UI's charting library (@cloudflare/kumo) built on Apache ECharts. Covers TimeseriesChart, SankeyChart, custom charts, color systems, and ChartLegend. Trigger when building charts or data visualizations in a Kumo UI project.
---

# Kumo UI Charts

Kumo UI charts are built on **Apache ECharts** and designed for Cloudflare dashboard-style data visualization. They support dark mode natively, have built-in accessibility, and use Kumo's color token system.

---

## 1. Installation & Setup

```bash
pnpm add @cloudflare/kumo echarts
```

Register the ECharts modules you need **once** at your app entry point:

```tsx
import * as echarts from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { AriaComponent, AxisPointerComponent, BrushComponent, GridComponent, LegendComponent, TooltipComponent } from "echarts/components";
import { BarChart, LineChart, PieChart } from "echarts/charts";

echarts.use([
  BarChart, LineChart, PieChart,
  AxisPointerComponent, BrushComponent, GridComponent,
  TooltipComponent, LegendComponent, AriaComponent,
  CanvasRenderer,
]);
```

Import chart components:

```tsx
import { TimeseriesChart, SankeyChart, Chart, ChartPalette, ChartLegend } from "@cloudflare/kumo";
```

---

## 2. TimeseriesChart

Displays time-based metrics as line/area/bar charts.

### Basic Usage

```tsx
import { TimeseriesChart, ChartPalette } from "@cloudflare/kumo";
import * as echarts from "echarts/core";
import { useIsDarkMode } from "~/lib/use-is-dark-mode";

export function RequestsChart() {
  const isDarkMode = useIsDarkMode();

  const data = [
    {
      name: "Requests",
      color: ChartPalette.semantic("Neutral", isDarkMode),
      data: [[1700000000000, 1234], [1700003600000, 1456]], // [timestamp_ms, value][]
    },
  ];

  return (
    <TimeseriesChart
      echarts={echarts}
      isDarkMode={isDarkMode}
      data={data}
      xAxisName="Time (UTC)"
      yAxisName="Requests"
      height={300}
    />
  );
}
```

### Key Props

| Prop | Type | Description |
|---|---|---|
| `echarts` | ECharts instance | Pass the `echarts` core object |
| `isDarkMode` | `boolean` | Drives theme switching |
| `data` | `{ name, color, data: [number, number][] }[]` | Series data as `[timestamp_ms, value]` pairs |
| `xAxisName` | `string` | X-axis label |
| `yAxisName` | `string` | Y-axis label |
| `height` | `number` | Chart height in px |
| `gradient` | `boolean` | Area gradient fill beneath each line |
| `loading` | `boolean` | Shows animated skeleton state |
| `incomplete` | `{ after: number }` | Highlights data after this timestamp as incomplete |
| `onTimeRangeChange` | `(from: number, to: number) => void` | Enables click-drag time range selection |
| `tooltipFollowCursor` | `"both" \| "x"` | `"x"` locks tooltip to horizontal axis only |

### Custom Axis Formatters

```tsx
<TimeseriesChart
  xAxisTickFormat={(ts) => new Date(ts).toLocaleTimeString("en-US", { hour: "2-digit", minute: "2-digit" })}
  yAxisTickFormat={(val) => val >= 1_000_000 ? `${val / 1_000_000}M` : val >= 1000 ? `${val / 1000}k` : String(val)}
  tooltipValueFormat={(val) => `${val.toLocaleString()} req/s`}
  {...otherProps}
/>
```

### Interactive Legend (Click-to-Isolate)

```tsx
const chartRef = useRef<echarts.ECharts>(null);
const [hiddenSeries, setHiddenSeries] = useState<Record<string, boolean>>({});

// Trigger ECharts legend actions programmatically
const toggleSeries = (name: string) => {
  const instance = chartRef.current;
  const isCurrentlyHidden = hiddenSeries[name];
  instance?.dispatchAction({ type: isCurrentlyHidden ? "legendSelect" : "legendUnSelect", name });
  setHiddenSeries(prev => ({ ...prev, [name]: !isCurrentlyHidden }));
};
```

---

## 3. SankeyChart

Visualizes flow between nodes. Use for traffic flows, pipeline stages, or funnel analysis.

### Basic Usage

```tsx
import { SankeyChart, ChartPalette } from "@cloudflare/kumo";
import * as echarts from "echarts/core";

const nodes = [
  { name: "Users",    value: 100_000, color: ChartPalette.categorical(0) },
  { name: "Auth",     value: 95_000,  color: ChartPalette.categorical(1) },
  { name: "API",      value: 80_000,  color: ChartPalette.categorical(2) },
];

const links = [
  { source: "Users", target: "Auth", value: 95_000 },
  { source: "Auth",  target: "API",  value: 80_000 },
];

export function TrafficFlow() {
  return (
    <SankeyChart
      echarts={echarts}
      nodes={nodes}
      links={links}
      height={400}
    />
  );
}
```

### Key Props

| Prop | Type | Description |
|---|---|---|
| `nodes` | `{ name, value, color }[]` | Node definitions |
| `links` | `{ source, target, value }[]` | Flow connections |
| `nodeWidth` | `number` | Width of node bars (default: `20`) |
| `nodePadding` | `number` | Vertical gap between nodes (default: `15`) |
| `left` / `right` | `string \| number` | Horizontal margins (set both to `0` for full-width) |
| `nodeLabelLayout` | `"inline" \| "outside"` | `"inline"` prevents label collision on dense graphs |
| `onNodeClick` | `(node) => void` | Click handler for drill-down filtering |
| `onLinkClick` | `(link) => void` | Click handler for link selection |
| `tooltipFormatter` | `(params: SankeyTooltipParams) => string` | Custom tooltip HTML |

---

## 4. Custom Charts (Base `<Chart>`)

Use the raw `<Chart>` component when built-in charts don't fit (e.g., Pie, Donut, Radar, Scatter).

```tsx
import { Chart } from "@cloudflare/kumo";
import * as echarts from "echarts/core";
import type { EChartsOption } from "echarts";

export function DonutChart({ isDarkMode }: { isDarkMode: boolean }) {
  const options: EChartsOption = {
    series: [{
      type: "pie",
      radius: ["40%", "70%"],
      data: [
        { value: 1048, name: "Cache Hit" },
        { value: 735, name: "Cache Miss" },
      ],
    }],
  };

  return <Chart echarts={echarts} options={options} isDarkMode={isDarkMode} height={400} />;
}
```

### Security: HTML Tooltips

When using custom HTML in tooltips, **always** sanitize with `echarts.format.encodeHTML` to prevent XSS:

```tsx
tooltip: {
  trigger: "item",
  // Use dangerousHtmlFormatter (not formatter) when returning HTML
  dangerousHtmlFormatter: (params: any) => {
    const safeName = echarts.format.encodeHTML(params.name);
    const safeValue = echarts.format.encodeHTML(String(params.value));
    return `<div><strong>${safeName}</strong>: ${safeValue}</div>`;
  },
}
```

> Never interpolate raw user data into tooltip HTML strings without `encodeHTML`.

---

## 5. Color Systems

Choose the right system based on your data type:

| System | When | User Goal | Examples |
|---|---|---|---|
| **Semantic** | Data has inherent polarity (good/bad, pass/fail) | Evaluate status | WAF actions, error rates, Web Vitals |
| **Categorical** | Nominal categories, no inherent order | Identify series | Countries, URLs, ASNs, service names |
| **Sequential** | Single metric varying in magnitude | Read density | Heatmaps, choropleths, histograms |

### Semantic Tokens (via `ChartPalette.semantic(key, isDarkMode)`)

| Key | Purpose |
|---|---|
| `"Attention"` | High-severity / errors |
| `"Warning"` | Medium-severity / caution |
| `"Success"` | Positive / allowed |
| `"Neutral"` | Default / no polarity |
| `"Disabled"` | Inactive series |

### Categorical Palette (via `ChartPalette.categorical(index)`)

6 CVD-friendly colors, ordered for max perceptual distance:

```
0: #4290F0  (Blue)
1: #F5B647  (Yellow-Orange)
2: #E8649D  (Pink)
3: #8D58EE  (Purple)
4: #50C3B6  (Teal)
5: #D37536  (Brown)
```

For more than 6 series, cycle with modulo: `ChartPalette.categorical(i % 6)`

> Always pair color with line pattern (`lineStyle.type: "dashed"`) for line charts. Color alone is insufficient for accessibility.

### Sequential Scale (5 Steps)

Darker = higher magnitude in light mode; lighter = higher in dark mode.

```
Step 1: #E1EAF4  (lightest)
Step 2: #8EBCF6
Step 3: #4290F0
Step 4: #0E58B4
Step 5: #03254F  (darkest)
```

Use for: choropleth maps, heatmaps, histogram fills. **Not** for categorical series.

---

## 6. ChartLegend

Use alongside charts — **not** ECharts' built-in legend — for Kumo-styled legends.

```tsx
import { ChartLegend, ChartPalette } from "@cloudflare/kumo";

// Large legend item (for primary metrics)
<ChartLegend.LargeItem
  name="Requests"
  color={ChartPalette.semantic("Neutral", isDarkMode)}
  value="1,234"
  unit="req/s"
  inactive={isHidden}
  onClick={() => toggleSeries("Requests")}
/>

// Small/compact legend item
<ChartLegend.SmallItem
  name="Errors"
  color={ChartPalette.semantic("Attention", isDarkMode)}
  value="42"
  inactive={isHidden}
/>
```
