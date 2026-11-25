---
name: data-storytelling-design
description: Comprehensive reference for Data Visualization, Dashboard UX/UI, Chart Selection, and Storytelling with Data.
allowed-tools: Read, Write, Edit
---

# Data Visualization & Storytelling Skill

> Universal reference for building premium, readable, and actionable data dashboards in web environments.

---

## 1. Dashboard Architecture (The Pyramid)

Always design page layouts based on the audience's operational level:

1. **Strategic (Top - Executives):**
   - **Focus:** High-level KPIs, Month-over-Month (MoM) variations, Goal tracking.
   - **Components:** Big Number cards, simple sparklines, progress bars.
2. **Tactical (Middle - Managers):**
   - **Focus:** Trends over time, comparisons, segmentation.
   - **Components:** Line charts, Stacked Bar charts, Heatmaps.
3. **Operational (Bottom - Analysts):**
   - **Focus:** Granular data, exact numbers, raw exports.
   - **Components:** Interactive Data Tables (TanStack Table, Ag-Grid) with sorting and filtering.

---

## 2. Chart Selection Matrix

Choose the right component based on the data relationship:

| Goal                             | Best Component Choice                  | DO NOT USE                       |
| :------------------------------- | :------------------------------------- | :------------------------------- |
| **Single Metric**                | Big Number + Sparkline / Delta %       | Gauges / Speedometers            |
| **Trend over Time**              | Line Chart / Area Chart                | Bar Charts (if many data points) |
| **Comparison (Categorical)**     | Horizontal Bar Chart                   | Pie Charts / Donut Charts        |
| **Composition (Parts of Whole)** | Stacked Bar (100%) / Treemap           | 3D Pie Charts                    |
| **Relationship/Distribution**    | Scatter Plot / Bubble Chart            | Line Chart                       |
| **Dense Cross-sectional Data**   | Heatmap (Table with conditional color) | Complex spider/radar charts      |

---

## 3. Decluttering (Applying Gestalt to UI)

When building a chart component (e.g., in Recharts or Visx), actively disable default "noise":

### Implementation Rules:

- **Remove Chart Borders:** `<CartesianGrid strokeDasharray="3 3" vertical={false} />` (Keep horizontal only, make them very light gray).
- **Remove Backgrounds:** Chart background must match the page background (usually `transparent`).
- **Direct Labeling:** Instead of using a separate Legend that forces the user's eyes to bounce back and forth, put the label directly next to the line/bar.
- **Clean Axes:** Remove the axis line itself. Remove decimal points if the numbers are large (e.g., show `10K` instead of `10,000.00`).

---

## 4. Preattentive Attributes (Focusing Attention)

Humans process certain visual cues instantly. Use them in CSS/Chart configs:

1. **Size:** Make the most important KPI physically larger (`text-4xl font-bold`).
2. **Color Hue:** Use a neutral palette (grays/slates) for context data, and ONE bold brand color (e.g., `text-blue-600` or `fill-blue-500`) for the data point you want to highlight.
3. **Color Intensity:** Use saturation to show value (Heatmaps).
4. **Position:** Top-left is the most valuable real estate on a screen. Put the most critical KPI there.

### The "WAYED" Test (Where Are Your Eyes Drawn?)

Always ask: _If I squint at this React component, what is the brightest, most prominent element?_ If it's a border or a logo, the design is wrong. It must be the data insight.

---

## 5. Storytelling Structure in UI

A dashboard page should follow a narrative arc:

- **1. Context (Introduction):** "What are we looking at?" -> Clear Page Titles, Subtitles, and Date Filters at the top.
- **2. Conflict (The Problem/Insight):** "What changed?" -> Big Number KPIs with Red/Green delta indicators showing variance against targets (SMART KPIs).
- **3. Resolution (The Details/Action):** "Why did it change?" -> Breakdown charts (by region, by product) and interactive tables at the bottom to allow drill-down.

---

## 6. Frontend Implementation Patterns

### 6.1 KPIs with Context (React/Tailwind)

```tsx
// ✅ DO: Show the number, the context, and the trend
<div className="rounded-xl border border-gray-100 bg-white p-6 shadow-sm">
  <h3 className="text-sm font-medium text-gray-500">Revenue (August)</h3>
  <div className="mt-2 flex items-baseline gap-2">
    <span className="text-3xl font-semibold text-gray-900">€613.5k</span>
    <span className="rounded-full bg-emerald-50 px-2 py-0.5 text-sm font-medium text-emerald-600">
      +15.2% YoY
    </span>
  </div>
  <p className="mt-1 text-sm text-gray-500">Target: €660.0k</p>
</div>
```

### 6.2 Tooltip UX

NEVER use default, ugly tooltips.

ALWAYS customize tooltips to show the exact context:

- Include the **Date/Category**, the **Metric**, and ideally the **comparison**.
- Use consistent formatting (same number format as the chart).
- Keep tooltip backgrounds opaque with high contrast text.

### 6.3 State Management for Dashboards

- Use **URL Query Parameters** (`?region=eu&year=2023`) for global dashboard filters so links are shareable.
- Use **local state** (`useState`) for micro-interactions (like hovering over a chart or toggling a specific chart view).
- Use **server-side data fetching** (RSC / Server Actions) for initial chart data — avoid client-side waterfalls.

---

## 7. Accessibility in Data Visualization

### Color-Blind Safe Design

- **Never use color alone** to convey meaning — always pair with shape, pattern, or label.
- **Avoid red/green only** combinations. Use blue/orange or blue/red as safer alternatives.
- **Test palettes** with tools like [Coblis](https://www.color-blindness.com/coblis-color-blindness-simulator/) or Chrome DevTools' vision emulation.

### Recommended Safe Palettes

| Use Case             | Primary                                  | Secondary        | Danger        |
| -------------------- | ---------------------------------------- | ---------------- | ------------- |
| **Diverging**        | Blue `#4E79A7`                           | Orange `#F28E2B` | Red `#E15759` |
| **Sequential**       | Light blue → Dark blue (single hue ramp) | —                | —             |
| **Categorical (≤6)** | Tableau 10 or IBM Design palette         | —                | —             |

### WCAG Compliance

- **Contrast**: All text on charts must meet AA (4.5:1 body, 3:1 large text).
- **Focus states**: Interactive chart elements (tooltips, filters, toggleable legends) must have visible focus rings.
- **Screen readers**: Provide `aria-label` or an accessible data table alternative for every chart.
- **Reduced motion**: Respect `prefers-reduced-motion` — disable chart entrance animations.

---

## 8. Tech Stack Reference

### Primary (React / Next.js)

| Tool               | Use Case                               |
| ------------------ | -------------------------------------- |
| **Recharts**       | Standard charts (line, bar, area, pie) |
| **TanStack Table** | Interactive data tables with sorting   |
| **Tailwind CSS**   | Layout, spacing, typography            |

### Alternatives (evaluate per project)

| Tool         | Use Case                                 |
| ------------ | ---------------------------------------- |
| **Visx**     | Custom D3-based visualizations in React  |
| **Tremor**   | Fast Tailwind-based dashboard components |
| **Ag-Grid**  | Enterprise-grade data grids              |
| **Chart.js** | Lightweight canvas-based charts          |

### Secondary (Non-React projects)

| Tool          | Use Case                              |
| ------------- | ------------------------------------- |
| **Plotly**    | Interactive charts in Python          |
| **Streamlit** | Rapid dashboard prototyping           |
| **Altair**    | Declarative statistical visualization |

> These are for projects outside the React/Next.js stack. Evaluate based on project requirements.

---

> **Remember:** Data without a story is just noise. Every chart must drive a decision.

---

## 9. Dashboard Art Direction (Visual Composition)

> Merged from `dashboard-art-direction` — guides premium, clear, domain-appropriate dashboard design.

### Dashboard Types

| Type           | Characteristics                                                |
| -------------- | -------------------------------------------------------------- |
| **Executive**  | Fewer KPI blocks, more breathing room, summary-first, premium  |
| **Operator**   | Denser layout, stronger controls, stable navigation, task flow |
| **Analytical** | Charts + filtering prominence, comparative structures          |
| **Narrative**  | Insights, summaries, guided interpretation over raw controls   |

### Required Process

1. Identify dashboard type
2. Identify primary decision-making tasks
3. Define top-of-page hierarchy
4. Define KPI, chart, and table treatment
5. Define section rhythm
6. Define secondary insight surfaces

### Composition Anti-Patterns

- Too many equal-weight cards
- Every module using the same card style
- Weak top-of-page structure
- Charts dropped in without narrative hierarchy
- Tables looking like raw admin leftovers
- Filters floating without strong grouping
