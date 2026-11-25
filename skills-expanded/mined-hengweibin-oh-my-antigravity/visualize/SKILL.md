---
name: visualize
description: "Autonomous generation of self-contained, zero-network, responsive HTML data visualizations, interactive charts, and dashboards. Triggers: visualize, visual dashboard, html chart, chart generation, data visualization, 視覺化, 圖表生成."
---

# Visualize — Zero-Network Self-Contained HTML Visualization & Dashboards

Autonomous generation of standalone, responsive, interactive HTML data visualizations, charts, and executive dashboards with **zero external network dependencies**.

Every visualization artifact is completely self-contained in a single `.html` file: styles are inlined, scripts are inlined, assets are SVG/Data URIs, and charts are rendered via pure SVG, HTML5 Canvas, or vanilla zero-dependency JavaScript.

---

## 1. Core Philosophy & Architectural Constraints

1. **Zero Network Dependencies (Strict Air-Gap Guarantee)**:
   - **NO external CDNs**: Do NOT use `<script src="https://cdn.jsdelivr.net/npm/chart.js">`, D3, ECharts, Mermaid CDN, Tailwind CDN, etc.
   - **NO remote CSS or Web Fonts**: Do NOT include Google Fonts (`@import url('https://fonts.googleapis.com/...')`), FontAwesome, or external stylesheets.
   - **NO remote images or icons**: Inlined SVG elements or base64 data URIs only.
   - **Guaranteed Offline Execution**: The output must render identically inside air-gapped environments, local `file:///` paths, sandboxed iframes (`sandbox="allow-scripts"`), and behind strict corporate firewalls.

2. **Single-File Portability**:
   - Deliver everything in a single, unbundled `.html` file.
   - Standard DOM layout: `<style>` inside `<head>`, semantic markup inside `<body>`, and inline `<script>` before `</body>`.

3. **Deterministic & Performant**:
   - Zero DNS latency, 0ms external network lag.
   - Native 60fps animations, hardware-accelerated CSS transforms, zero bundle overhead.

---

## 2. Theming & Design System

Every visualization artifact must provide a modern, high-contrast, professional theme system powered by native CSS Custom Properties.

### 2.1 CSS Variables & Palette Tokens
Provide complete Light Mode and Dark Mode palettes with smooth transitions:

```css
:root {
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji";
  --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
  
  /* Light Theme (Default) */
  --bg-page: #f8fafc;
  --bg-surface: #ffffff;
  --bg-surface-elevated: #f1f5f9;
  --bg-card: #ffffff;
  --border-color: #e2e8f0;
  --border-focus: #3b82f6;
  
  --text-primary: #0f172a;
  --text-secondary: #475569;
  --text-muted: #94a3b8;
  
  --color-primary: #2563eb;
  --color-primary-hover: #1d4ed8;
  --color-primary-light: #eff6ff;
  --color-success: #10b981;
  --color-success-light: #ecfdf5;
  --color-warning: #f59e0b;
  --color-warning-light: #fffbeb;
  --color-danger: #ef4444;
  --color-danger-light: #fef2f2;
  --color-info: #06b6d4;
  --color-info-light: #ecfeff;
  
  /* Chart Categorical Series */
  --chart-series-1: #3b82f6;
  --chart-series-2: #10b981;
  --chart-series-3: #8b5cf6;
  --chart-series-4: #f59e0b;
  --chart-series-5: #ec4899;
  --chart-series-6: #06b6d4;
  --chart-fill: rgba(59, 130, 246, 0.12);

  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 16px;
}

[data-theme="dark"] {
  --bg-page: #0f172a;
  --bg-surface: #1e293b;
  --bg-surface-elevated: #334155;
  --bg-card: #1e293b;
  --border-color: #334155;
  --border-focus: #60a5fa;
  
  --text-primary: #f8fafc;
  --text-secondary: #cbd5e1;
  --text-muted: #64748b;
  
  --color-primary: #3b82f6;
  --color-primary-hover: #60a5fa;
  --color-primary-light: #172554;
  --color-success: #10b981;
  --color-success-light: #064e3b;
  --color-warning: #f59e0b;
  --color-warning-light: #78350f;
  --color-danger: #ef4444;
  --color-danger-light: #7f1d1d;
  --color-info: #06b6d4;
  --color-info-light: #164e63;
  
  --chart-series-1: #60a5fa;
  --chart-series-2: #34d399;
  --chart-series-3: #a78bfa;
  --chart-series-4: #fbbf24;
  --chart-series-5: #f472b6;
  --chart-series-6: #22d3ee;
  --chart-fill: rgba(96, 165, 250, 0.18);
  
  --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.3);
  --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.4);
}
```

### 2.2 Theme Switching Routine
```javascript
function initTheme() {
  const saved = localStorage.getItem('theme') || 
    (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  setTheme(saved);
}

function setTheme(theme) {
  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('theme', theme);
  const toggleBtn = document.getElementById('theme-toggle');
  if (toggleBtn) {
    toggleBtn.innerHTML = theme === 'dark' ? '☀️ Light' : '🌙 Dark';
    toggleBtn.setAttribute('aria-label', `Switch to ${theme === 'dark' ? 'Light' : 'Dark'} mode`);
  }
  window.dispatchEvent(new CustomEvent('themechange', { detail: { theme } }));
}
```

---

## 3. Responsive Design & Multi-Viewport Verification

Fluid layouts verified across mobile (390px viewport) and desktop (1280px+).

### 3.1 Breakpoints & Layout Adapters
- **Mobile Viewport (390px)**: iPhone portrait baseline width.
  - Metrics cards collapse into single-column (`grid-template-columns: 1fr`).
  - Data tables wrapped in horizontal scroll container (`overflow-x: auto; -webkit-overflow-scrolling: touch;`).
  - Interactive tap targets must be at least 44px × 44px.
  - SVG charts scale seamlessly via responsive `viewBox="0 0 W H"` with `width="100%" height="auto"`.
- **Tablet (768px - 1024px)**: 2-column metric cards, inline filter controls.
- **Desktop (1280px+)**: 4-column KPI cards, side-by-side multi-chart grid (`2fr 1fr` or `1fr 1fr`), expansive sortable data tables.

```css
.container {
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem;
}

@media (min-width: 640px) {
  .metrics-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (min-width: 1024px) {
  .container { padding: 2rem; }
  .metrics-grid { grid-template-columns: repeat(4, 1fr); }
  .charts-grid { display: grid; grid-template-columns: 2fr 1fr; gap: 1.5rem; }
}
```

---

## 4. Visualization Techniques: Zero-Dependency Engines

Select the optimal rendering technique based on data requirements:

| Technique | Optimal Scenarios | Engine Details |
|---|---|---|
| **Inline SVG** | Time-series lines, multi-series area charts, bar charts, donut/pie charts, sparklines (< 1,000 points) | Scalable vector graphics, CSS styled, declarative DOM, native tooltip hover tracking. |
| **HTML5 Canvas** | High-density data points (> 1,000 points), heatmaps, scatter plots, real-time particle rendering | High-throughput 2D context, direct pixel buffers, `requestAnimationFrame`. |
| **Pure CSS/HTML** | Progress gauges, KPI delta badges, status meters, tabular heat bars | 0 lines of JS required, accessible to screen readers, instant render. |

### 4.1 SVG Math & Chart Generation
- **Coordinate Normalization**: Map domain `[minX, maxX]` and range `[minY, maxY]` into SVG pixel coordinates `[padding, width - padding]`.
- **Interactive Tooltips**: Floating absolute positioned `div` tracking pointer events with auto boundary-flipping to prevent viewport edge clipping.
- **Interactive Legends**: Clickable series chips to toggle visibility with CSS transition opacity.

---

## 5. Mandatory Dashboard Structure

Every generated dashboard must follow this 6-part architecture:

```
┌────────────────────────────────────────────────────────────────────────┐
│ 1. Header: Title, Status Badge, Timestamp, Theme Toggle, Export Button │
├────────────────────────────────────────────────────────────────────────┤
│ 2. KPI Metrics Bar: 3-4 Metric Cards (Value, Delta badge, Subtext)     │
├────────────────────────────────────────────────────────────────────────┤
│ 3. Filter Controls: Timeframe Pills, Category Selectors, Live Search   │
├────────────────────────────────────────────────────────────────────────┤
│ 4. Main Chart Section: Primary Trend Chart + Secondary Breakdown Chart │
├────────────────────────────────────────────────────────────────────────┤
│ 5. Detailed Data Table: Sortable, Filterable Columns with Pager/Search │
├────────────────────────────────────────────────────────────────────────┤
│ 6. Footer: Metadata, Data Provenance, Export & Attribution Info        │
└────────────────────────────────────────────────────────────────────────┘
```

1. **Header**:
   - `<h1>` dashboard title with description/subtitle.
   - Live status indicator (e.g., `● Live System Status`).
   - Theme toggle button (`☀️ / 🌙`).
   - Export action (`window.print()` or CSV export).
2. **KPI Summary Cards**:
   - Card title (muted label).
   - Primary metric figure (large bold tabular numbers).
   - Trend badge: `+14.2%` (green) or `-3.1%` (red) with directional arrows (`↑`, `↓`).
   - Sparkline or contextual explanation.
3. **Interactive Filter & Selector Controls**:
   - Timeframe pills: `[24h] [7d] [30d] [90d] [All]`.
   - Category / Dimension filter dropdowns.
   - Real-time text search input for filtering table and chart items.
4. **Main Chart Section**:
   - Primary chart card (e.g., SVG Area/Line Chart of trend over time).
   - Secondary distribution card (e.g., Donut or Bar chart for category breakdown).
5. **Detailed Data Table**:
   - Interactive column headers with sort indicators (`↕`, `▲`, `▼`).
   - Tabular numbers with right-alignment.
   - Status tag pills (Operational, Degraded, Outage, Warning).
6. **Footer**:
   - Data provenance and timestamp.
   - "Self-contained · Zero-network · Antigravity Visualize" badge.

---

## 6. Output Path & Delivery Conventions

1. **Output Destinations**:
   - Output artifacts directly into the conversation artifact directory (`<appDataDir>\brain\<conversation-id>/<slug>.html`) or workspace directory (`.scratch/visualizations/<slug>.html` or designated project path).
2. **Pre-Delivery Verification Checklist**:
   - [ ] **Strict Zero-Network**: No remote `<script>`, `<link>`, or `@import` tags.
   - [ ] **File Protocol Test**: Double-click opening via `file:///` works with zero errors.
   - [ ] **Mobile Responsiveness**: Verified clean at 390px viewport width (no horizontal page blowout).
   - [ ] **Desktop Grid**: Verified balanced and aligned at 1280px+ viewport.
   - [ ] **Theme Switching**: Dark and Light themes both maintain WCAG AA contrast.
   - [ ] **Interactive Elements**: Tooltips, filters, and table sorting work without console exceptions.

---

## 7. Production-Grade Reference Boilerplate

When generating visualizations, use this complete, standalone boilerplate as a baseline:

```html
<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Executive Analytics Dashboard</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    
    :root {
      --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      
      --bg-page: #f8fafc;
      --bg-surface: #ffffff;
      --bg-surface-elevated: #f1f5f9;
      --border-color: #e2e8f0;
      
      --text-primary: #0f172a;
      --text-secondary: #475569;
      --text-muted: #94a3b8;
      
      --color-primary: #2563eb;
      --color-primary-light: #eff6ff;
      --color-success: #10b981;
      --color-success-light: #ecfdf5;
      --color-warning: #f59e0b;
      --color-danger: #ef4444;
      --color-danger-light: #fef2f2;
      
      --chart-line: #3b82f6;
      --chart-fill: rgba(59, 130, 246, 0.12);
      
      --shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
      --radius: 12px;
    }

    [data-theme="dark"] {
      --bg-page: #0f172a;
      --bg-surface: #1e293b;
      --bg-surface-elevated: #334155;
      --border-color: #334155;
      
      --text-primary: #f8fafc;
      --text-secondary: #cbd5e1;
      --text-muted: #64748b;
      
      --color-primary: #3b82f6;
      --color-primary-light: #1e3a8a;
      --color-success: #10b981;
      --color-success-light: #064e3b;
      --color-warning: #fbbf24;
      --color-danger: #f87171;
      --color-danger-light: #7f1d1d;
      
      --chart-line: #60a5fa;
      --chart-fill: rgba(96, 165, 250, 0.18);
      
      --shadow: 0 4px 6px -1px rgb(0 0 0 / 0.3);
    }

    body {
      font-family: var(--font-sans);
      background-color: var(--bg-page);
      color: var(--text-primary);
      line-height: 1.5;
      transition: background-color 0.2s, color 0.2s;
      padding: 1.5rem;
    }

    .container {
      max-width: 1320px;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      gap: 1.5rem;
    }

    /* 1. Header */
    header {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 1rem;
      padding-bottom: 1rem;
      border-bottom: 1px solid var(--border-color);
    }
    .header-title h1 { font-size: 1.5rem; font-weight: 700; }
    .header-title p { font-size: 0.875rem; color: var(--text-muted); }
    .header-actions { display: flex; gap: 0.75rem; align-items: center; }

    button, select, input {
      font-family: inherit;
      font-size: 0.875rem;
      border-radius: 8px;
      border: 1px solid var(--border-color);
      background: var(--bg-surface);
      color: var(--text-primary);
      padding: 0.5rem 0.875rem;
      cursor: pointer;
      transition: all 0.15s;
    }
    button:hover { background: var(--bg-surface-elevated); }
    .btn-primary { background: var(--color-primary); color: #fff; border: none; }
    .btn-primary:hover { opacity: 0.9; }

    /* 2. Metrics Grid */
    .metrics-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 1rem;
    }
    @media (min-width: 640px) { .metrics-grid { grid-template-columns: repeat(2, 1fr); } }
    @media (min-width: 1024px) { .metrics-grid { grid-template-columns: repeat(4, 1fr); } }

    .card {
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: var(--radius);
      padding: 1.25rem;
      box-shadow: var(--shadow);
    }
    .metric-card .label { font-size: 0.8125rem; color: var(--text-secondary); margin-bottom: 0.5rem; }
    .metric-card .val-row { display: flex; align-items: baseline; justify-content: space-between; }
    .metric-card .value { font-size: 1.75rem; font-weight: 700; font-family: var(--font-mono); }
    .badge {
      display: inline-flex;
      align-items: center;
      gap: 0.25rem;
      padding: 0.25rem 0.5rem;
      border-radius: 6px;
      font-size: 0.75rem;
      font-weight: 600;
    }
    .badge-success { background: var(--color-success-light); color: var(--color-success); }
    .badge-danger { background: var(--color-danger-light); color: var(--color-danger); }

    /* 3. Filter Controls */
    .filter-bar {
      display: flex;
      flex-wrap: wrap;
      gap: 0.75rem;
      align-items: center;
      justify-content: space-between;
    }
    .pill-group { display: flex; gap: 0.25rem; background: var(--bg-surface-elevated); padding: 0.25rem; border-radius: 8px; }
    .pill-group button { border: none; background: transparent; padding: 0.375rem 0.75rem; }
    .pill-group button.active { background: var(--bg-surface); font-weight: 600; box-shadow: var(--shadow); }

    /* 4. Main Chart Section */
    .charts-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 1.5rem;
    }
    @media (min-width: 1024px) {
      .charts-grid { grid-template-columns: 2fr 1fr; }
    }
    .chart-container {
      width: 100%;
      height: 300px;
      position: relative;
    }
    svg.chart-svg {
      width: 100%;
      height: 100%;
      overflow: visible;
    }
    .tooltip {
      position: absolute;
      padding: 0.5rem 0.75rem;
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: 6px;
      box-shadow: var(--shadow);
      font-size: 0.75rem;
      pointer-events: none;
      opacity: 0;
      transition: opacity 0.15s;
      z-index: 10;
    }

    /* 5. Detailed Data Table */
    .table-container {
      overflow-x: auto;
      border-radius: var(--radius);
      border: 1px solid var(--border-color);
      background: var(--bg-surface);
    }
    table {
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 0.875rem;
    }
    th, td {
      padding: 0.75rem 1rem;
      border-bottom: 1px solid var(--border-color);
    }
    th {
      background: var(--bg-surface-elevated);
      color: var(--text-secondary);
      font-weight: 600;
      cursor: pointer;
      user-select: none;
    }
    th:hover { color: var(--text-primary); }
    td.num, th.num { text-align: right; font-variant-numeric: tabular-nums; }

    /* 6. Footer */
    footer {
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 0.5rem;
      padding-top: 1rem;
      font-size: 0.75rem;
      color: var(--text-muted);
      border-top: 1px solid var(--border-color);
    }
  </style>
</head>
<body>
  <div class="container">
    <!-- Header -->
    <header>
      <div class="header-title">
        <h1>Executive Performance Dashboard</h1>
        <p>Operational health & traffic metrics · Updated: <span id="last-updated">2026-10-11</span></p>
      </div>
      <div class="header-actions">
        <button id="theme-toggle" onclick="toggleTheme()">🌙 Dark Mode</button>
        <button class="btn-primary" onclick="window.print()">Print / Export</button>
      </div>
    </header>

    <!-- Metrics Cards -->
    <section class="metrics-grid">
      <div class="card metric-card">
        <div class="label">Total Processed Events</div>
        <div class="val-row">
          <span class="value">1,248,300</span>
          <span class="badge badge-success">↑ 18.2%</span>
        </div>
      </div>
      <div class="card metric-card">
        <div class="label">Average Latency</div>
        <div class="val-row">
          <span class="value">42.5ms</span>
          <span class="badge badge-success">↓ 4.1ms</span>
        </div>
      </div>
      <div class="card metric-card">
        <div class="label">Error Budget Remaining</div>
        <div class="val-row">
          <span class="value">99.94%</span>
          <span class="badge badge-success">↑ 0.02%</span>
        </div>
      </div>
      <div class="card metric-card">
        <div class="label">Degraded Instances</div>
        <div class="val-row">
          <span class="value">2</span>
          <span class="badge badge-danger">↑ 1</span>
        </div>
      </div>
    </section>

    <!-- Filter Controls -->
    <section class="filter-bar">
      <div class="pill-group" id="time-pills">
        <button class="active" onclick="setTimeframe('7d', this)">Last 7 Days</button>
        <button onclick="setTimeframe('30d', this)">Last 30 Days</button>
        <button onclick="setTimeframe('90d', this)">Last 90 Days</button>
      </div>
      <input type="text" id="table-search" placeholder="Filter table records..." oninput="filterTable(this.value)">
    </section>

    <!-- Main Chart Section -->
    <section class="charts-grid">
      <div class="card">
        <h2 style="font-size: 1rem; margin-bottom: 1rem; font-weight: 600;">System Throughput Trend (RPS)</h2>
        <div class="chart-container" id="chart-box">
          <svg class="chart-svg" id="trend-chart" viewBox="0 0 800 300" preserveAspectRatio="none"></svg>
          <div class="tooltip" id="chart-tooltip"></div>
        </div>
      </div>
      <div class="card">
        <h2 style="font-size: 1rem; margin-bottom: 1rem; font-weight: 600;">Regional Traffic Share</h2>
        <div class="chart-container" id="donut-box">
          <svg class="chart-svg" id="donut-chart" viewBox="0 0 300 300"></svg>
        </div>
      </div>
    </section>

    <!-- Data Table -->
    <section class="table-container">
      <table id="data-table">
        <thead>
          <tr>
            <th onclick="sortTable(0)">Service Node ↕</th>
            <th onclick="sortTable(1)">Region ↕</th>
            <th onclick="sortTable(2)">Status ↕</th>
            <th class="num" onclick="sortTable(3)">Requests / min ↕</th>
            <th class="num" onclick="sortTable(4)">P99 Latency (ms) ↕</th>
          </tr>
        </thead>
        <tbody id="table-body"></tbody>
      </table>
    </section>

    <!-- Footer -->
    <footer>
      <span>Zero-network dependency · Single self-contained file</span>
      <span>Antigravity Visualize Skill</span>
    </footer>
  </div>

  <script>
    const dataset = [
      { day: 'Mon', val: 450, node: 'edge-auth-01', region: 'US-East', status: 'Operational', req: 48200, p99: 38 },
      { day: 'Tue', val: 580, node: 'api-gateway-02', region: 'US-West', status: 'Operational', req: 62100, p99: 45 },
      { day: 'Wed', val: 510, node: 'payment-svc-01', region: 'EU-Central', status: 'Operational', req: 38400, p99: 52 },
      { day: 'Thu', val: 720, node: 'data-pipeline-04', region: 'AP-East', status: 'Degraded', req: 84000, p99: 112 },
      { day: 'Fri', val: 890, node: 'cache-redis-03', region: 'US-East', status: 'Operational', req: 98100, p99: 24 },
      { day: 'Sat', val: 640, node: 'search-index-01', region: 'EU-West', status: 'Operational', req: 51200, p99: 49 },
      { day: 'Sun', val: 780, node: 'webhook-worker-02', region: 'SA-East', status: 'Operational', req: 67300, p99: 58 }
    ];

    function toggleTheme() {
      const cur = document.documentElement.getAttribute('data-theme') || 'light';
      const target = cur === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', target);
      document.getElementById('theme-toggle').innerText = target === 'dark' ? '☀️ Light Mode' : '🌙 Dark Mode';
    }

    function renderLineChart() {
      const svg = document.getElementById('trend-chart');
      const tooltip = document.getElementById('chart-tooltip');
      const w = 800, h = 300, p = 40;
      
      const maxVal = Math.max(...dataset.map(d => d.val)) * 1.2;
      const points = dataset.map((d, i) => ({
        x: p + (i / (dataset.length - 1)) * (w - 2 * p),
        y: h - p - (d.val / maxVal) * (h - 2 * p),
        data: d
      }));

      const pathD = points.reduce((acc, pt, i) => `${acc} ${i === 0 ? 'M' : 'L'} ${pt.x} ${pt.y}`, '');
      const areaD = `${pathD} L ${points[points.length - 1].x} ${h - p} L ${points[0].x} ${h - p} Z`;

      let grid = '';
      for (let i = 0; i <= 4; i++) {
        const yVal = h - p - (i / 4) * (h - 2 * p);
        grid += `<line x1="${p}" y1="${yVal}" x2="${w - p}" y2="${yVal}" stroke="var(--border-color)" stroke-dasharray="4" />`;
      }

      const circles = points.map(pt => 
        `<circle cx="${pt.x}" cy="${pt.y}" r="5" fill="var(--color-primary)" stroke="var(--bg-surface)" stroke-width="2" class="chart-point" data-info="${pt.data.day}: ${pt.data.val} RPS"></circle>`
      ).join('');

      svg.innerHTML = `
        ${grid}
        <path d="${areaD}" fill="var(--chart-fill)" />
        <path d="${pathD}" fill="none" stroke="var(--chart-line)" stroke-width="3" stroke-linecap="round" />
        ${circles}
      `;

      svg.querySelectorAll('.chart-point').forEach(c => {
        c.addEventListener('mouseenter', e => {
          tooltip.style.opacity = '1';
          tooltip.innerText = c.getAttribute('data-info');
          const box = c.getBoundingClientRect();
          const pBox = document.getElementById('chart-box').getBoundingClientRect();
          tooltip.style.left = `${box.left - pBox.left}px`;
          tooltip.style.top = `${box.top - pBox.top - 32}px`;
        });
        c.addEventListener('mouseleave', () => { tooltip.style.opacity = '0'; });
      });
    }

    function renderDonutChart() {
      const svg = document.getElementById('donut-chart');
      const slices = [
        { label: 'US-East', pct: 40, color: 'var(--chart-series-1)' },
        { label: 'US-West', pct: 25, color: 'var(--chart-series-2)' },
        { label: 'EU-West', pct: 20, color: 'var(--chart-series-3)' },
        { label: 'Other', pct: 15, color: 'var(--chart-series-4)' }
      ];
      
      let accum = 0;
      const r = 90, cx = 150, cy = 150;
      const paths = slices.map(s => {
        const startA = (accum / 100) * 2 * Math.PI - Math.PI / 2;
        accum += s.pct;
        const endA = (accum / 100) * 2 * Math.PI - Math.PI / 2;
        
        const x1 = cx + r * Math.cos(startA), y1 = cy + r * Math.sin(startA);
        const x2 = cx + r * Math.cos(endA), y2 = cy + r * Math.sin(endA);
        const largeArc = s.pct > 50 ? 1 : 0;
        
        return `<path d="M ${x1} ${y1} A ${r} ${r} 0 ${largeArc} 1 ${x2} ${y2}" fill="none" stroke="${s.color}" stroke-width="32" stroke-linecap="butt" />`;
      }).join('');

      svg.innerHTML = `
        ${paths}
        <text x="${cx}" y="${cy - 5}" text-anchor="middle" font-size="20" font-weight="700" fill="var(--text-primary)">100%</text>
        <text x="${cx}" y="${cy + 16}" text-anchor="middle" font-size="11" fill="var(--text-muted)">Global Traffic</text>
      `;
    }

    let tableRows = [...dataset];
    function renderTable() {
      const tbody = document.getElementById('table-body');
      tbody.innerHTML = tableRows.map(r => `
        <tr>
          <td><strong>${r.node}</strong></td>
          <td>${r.region}</td>
          <td><span class="badge ${r.status === 'Operational' ? 'badge-success' : 'badge-danger'}">${r.status}</span></td>
          <td class="num">${r.req.toLocaleString()}</td>
          <td class="num">${r.p99} ms</td>
        </tr>
      `).join('');
    }

    let sortAsc = true;
    function sortTable(idx) {
      sortAsc = !sortAsc;
      const keys = ['node', 'region', 'status', 'req', 'p99'];
      const key = keys[idx];
      tableRows.sort((a, b) => {
        if (typeof a[key] === 'number') return sortAsc ? a[key] - b[key] : b[key] - a[key];
        return sortAsc ? a[key].localeCompare(b[key]) : b[key].localeCompare(a[key]);
      });
      renderTable();
    }

    function filterTable(q) {
      const term = q.toLowerCase();
      tableRows = dataset.filter(d => 
        d.node.toLowerCase().includes(term) ||
        d.region.toLowerCase().includes(term) ||
        d.status.toLowerCase().includes(term)
      );
      renderTable();
    }

    function setTimeframe(tf, btn) {
      document.querySelectorAll('#time-pills button').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
    }

    window.addEventListener('DOMContentLoaded', () => {
      renderLineChart();
      renderDonutChart();
      renderTable();
    });
  </script>
</body>
</html>
```
