---
name: build-dashboard
description: >
  Build an interactive dashboard from data, selecting appropriate widgets, layouts, and interactivity patterns.
  TRIGGER when: user asks to "build a dashboard", "create a dashboard", "make a dashboard", "interactive report",
  "dashboard layout", "KPI dashboard", "monitoring dashboard", or "real-time dashboard".
argument-hint: "<data_source> [dashboard_type]"
user-invocable: true
---

# Dashboard Builder

You are an expert dashboard designer and developer. When the user asks you to build a dashboard, follow this structured process.

## Step 1: Requirements Gathering

Clarify these before building:

| Requirement | Question |
|-------------|----------|
| Audience | Who will use this dashboard? (executive, analyst, ops team) |
| Purpose | Monitor KPIs, explore data, trigger alerts, or tell a story? |
| Data source | File, database, API, or real-time stream? |
| Refresh cadence | Static, daily, hourly, real-time? |
| Interactivity | Filters, drill-downs, cross-filtering, date pickers? |
| Platform | Web app, notebook, PDF export, embedded? |

## Step 2: KPI and Metric Selection

Structure metrics using the SMART framework:

- **Specific**: Each metric answers one clear question
- **Measurable**: Quantifiable with available data
- **Actionable**: Users can act on changes in the metric
- **Relevant**: Aligned with the dashboard's purpose
- **Time-bound**: Has a clear time dimension or comparison period

### Metric Hierarchy

```
Primary KPIs (3-5)       -- Large cards at top, the "so what" numbers
Secondary Metrics (5-10) -- Charts and tables in the body
Supporting Detail         -- Drill-down tables, filters, tooltips
```

## Step 3: Layout Design

### Layout Patterns by Dashboard Type

| Type | Layout | Key Widgets |
|------|--------|-------------|
| Executive | Top KPI cards + trend lines + summary table | Scorecards, sparklines, gauges |
| Operational | Status indicators + real-time charts + alert list | Status lights, live line charts, tables |
| Analytical | Filters sidebar + multi-chart grid + detail table | Dropdowns, scatter plots, heatmaps, pivot tables |
| Storytelling | Sequential sections with narrative + visuals | Annotated charts, text blocks, step navigation |

### Grid System

- Use a 12-column grid for responsive layout
- KPI cards: full width or 3-4 per row
- Charts: 6-column (half width) or 12-column (full width)
- Tables: always full width
- Filters: sidebar (3-column) or top bar

## Step 4: Chart Selection Guide

| Data Relationship | Recommended Chart | When to Use |
|-------------------|-------------------|-------------|
| Trend over time | Line chart | Continuous time series |
| Comparison | Bar chart (horizontal for many categories) | Comparing discrete groups |
| Composition | Stacked bar or pie (< 6 slices) | Parts of a whole |
| Distribution | Histogram, box plot | Understanding spread |
| Correlation | Scatter plot | Relationship between two numerics |
| Geographic | Choropleth or bubble map | Location-based data |
| Ranking | Horizontal bar, sorted | Top-N or bottom-N |
| Flow | Sankey diagram | Movement between states |
| KPI single value | Scorecard with delta indicator | Current value vs target/prior |

## Step 5: Interactivity Patterns

Implement these interaction types as appropriate:

- **Filters**: Global filters affect all charts; local filters affect one
- **Cross-filtering**: Clicking a chart element filters other charts
- **Drill-down**: Click to navigate from summary to detail
- **Tooltips**: Hover for additional context without clutter
- **Date range picker**: Allow custom time window selection
- **Search/typeahead**: For high-cardinality dimensions
- **Export**: CSV download for underlying data tables

## Step 6: Technology Selection

| Framework | Best For | Interactivity | Complexity |
|-----------|----------|---------------|------------|
| Streamlit | Fast Python prototypes | Medium | Low |
| Dash (Plotly) | Production Python dashboards | High | Medium |
| Panel (HoloViz) | Data science dashboards | High | Medium |
| Gradio | ML model demos with data | Medium | Low |
| Observable / D3 | Custom web visualizations | Very High | High |
| React + Recharts | Production web apps | Very High | High |

## Step 7: Implementation Template

```python
# Streamlit dashboard skeleton
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard Title", layout="wide")

# --- Sidebar Filters ---
st.sidebar.header("Filters")
# Add filter widgets here

# --- KPI Row ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Metric 1", value, delta)
# ...

# --- Chart Row ---
left, right = st.columns(2)
with left:
    st.plotly_chart(fig1, use_container_width=True)
with right:
    st.plotly_chart(fig2, use_container_width=True)

# --- Detail Table ---
st.dataframe(filtered_df, use_container_width=True)
```

## Step 8: Design Best Practices

- **Color**: Use a consistent palette; reserve red/green for negative/positive
- **Typography**: Dashboard title 24px, section headers 18px, labels 12-14px
- **Whitespace**: Generous padding between widgets; avoid cramming
- **Alignment**: Left-align text, right-align numbers
- **Responsiveness**: Test at 1280px and 1920px widths minimum
- **Accessibility**: Ensure color-blind safe palettes, sufficient contrast (WCAG AA)
- **Loading states**: Show spinners or skeletons for slow-loading widgets

## Step 9: Performance Optimization

- Pre-aggregate data where possible; avoid computing on raw rows in the UI
- Cache expensive computations (`@st.cache_data`, `functools.lru_cache`)
- Limit default date ranges to recent data; let users expand
- Paginate large tables (show 25-50 rows, not thousands)
- Use efficient chart types (SVG for < 1000 points, WebGL/Canvas for more)

## Quality Checklist

- [ ] Dashboard loads in under 3 seconds
- [ ] All KPI cards show current value, comparison, and direction
- [ ] Filters work correctly and reset cleanly
- [ ] Charts have clear titles, axis labels, and legends
- [ ] Color palette is consistent and accessible
- [ ] Mobile/narrow viewport does not break layout
- [ ] Data refreshes without full page reload (if applicable)
- [ ] Export functionality works for key tables

## Edge Cases

- **No data**: Show "No data available" message, not a blank space or error
- **Single data point**: Show value without trend line; note insufficient data
- **Extreme outliers**: Consider log scale or capped axis with annotation
- **Slow queries**: Add loading indicators and consider pre-aggregation
- **Mixed time zones**: Normalize to one time zone and display it clearly
