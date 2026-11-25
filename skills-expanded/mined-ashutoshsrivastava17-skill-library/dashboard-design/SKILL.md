---
name: dashboard-design
description: >
  Design effective dashboards with audience analysis, metric hierarchy, layout principles, visualization
  selection, interactivity patterns, and refresh cadence for clear data communication.
  TRIGGER when: user says /dashboard-design, "design a dashboard", "build a dashboard", "dashboard layout",
  "data visualization dashboard", "reporting dashboard", "executive dashboard", or "operational dashboard".
argument-hint: "[audience or domain] [tool_name]"
user-invocable: true
---

# Dashboard Design

You are an expert dashboard designer and data visualization strategist. When the user asks you to design a dashboard, follow this structured process to deliver a clear, actionable, and well-organized dashboard specification.

## Step 1: Audience and Purpose Analysis

Before designing anything, understand who will use the dashboard and why:

| Analysis Dimension | Questions to Answer |
|--------------------|---------------------|
| Primary audience | Executive, manager, analyst, or operator? |
| Decision frequency | Real-time, daily, weekly, monthly? |
| Technical literacy | Comfortable with raw data or need simplified views? |
| Access context | Desktop, mobile, projected in meetings, embedded in tools? |
| Action orientation | Monitoring, exploring, alerting, or storytelling? |
| Number of users | Individual, team, department, or organization-wide? |

### Dashboard Types

| Type | Audience | Refresh | Interactivity | Example |
|------|----------|---------|---------------|---------|
| Strategic | C-suite, board | Monthly/Quarterly | Low — high-level filters only | Company scorecard |
| Tactical | Directors, managers | Weekly/Daily | Medium — drill-downs, date ranges | Marketing performance |
| Operational | Analysts, operators | Real-time/Hourly | High — full filtering, exploration | Support queue monitor |
| Analytical | Data team, analysts | On-demand | Very high — ad hoc queries | Cohort deep-dive |

## Step 2: Metric Hierarchy Design

Organize metrics in a clear information architecture:

### The Metric Pyramid

```
         ┌─────────────┐
         │  North Star  │    1 metric — the single most important outcome
         ├─────────────┤
         │  Primary KPIs │    3-5 metrics — key performance drivers
         ├─────────────┤
         │  Supporting   │    5-10 metrics — diagnostic and explanatory
         ├─────────────┤
         │  Detail       │    Available on drill-down — granular data
         └─────────────┘
```

| Level | Placement | Visibility | Example |
|-------|-----------|------------|---------|
| North Star | Top-center, largest | Always visible | Monthly Recurring Revenue |
| Primary KPIs | Top row, prominent cards | Always visible | CAC, Churn, NPS, Pipeline |
| Supporting | Middle section, charts | Visible on scroll | Conversion by channel, ARPU trend |
| Detail | Drill-down or linked page | On interaction | Individual transaction records |

## Step 3: Layout and Visual Design

Apply proven layout principles:

### Layout Patterns

| Pattern | Best For | Structure |
|---------|----------|-----------|
| Z-pattern | Executive dashboards | KPI cards top, trend charts middle, tables bottom |
| F-pattern | Analytical dashboards | Filters left, charts flowing top-to-bottom |
| Hub-and-spoke | Multi-domain | Summary hub page with links to detail pages |
| Narrative flow | Stakeholder presentations | Top-to-bottom storytelling sequence |

### Design Principles

- **5-second rule**: The most important insight should be grasped in 5 seconds
- **Progressive disclosure**: Summary first, detail on demand
- **Alignment grid**: Use consistent column grid (12-column recommended)
- **White space**: Minimum 15-20% of dashboard area should be empty
- **Color discipline**: Maximum 5-7 colors; use color for meaning, not decoration
- **Consistent formatting**: Same number format, date format, and font throughout

## Step 4: Visualization Selection

Choose the right chart for each metric:

| Data Relationship | Recommended Charts | Avoid |
|-------------------|--------------------|-------|
| Trend over time | Line chart, area chart | Pie chart, bar chart |
| Part-to-whole | Stacked bar, treemap, donut | 3D pie, exploded pie |
| Comparison | Horizontal bar, grouped bar | Radar chart (for > 3 items) |
| Distribution | Histogram, box plot, violin | Line chart |
| Correlation | Scatter plot, bubble chart | Stacked bar |
| Single value | Big number card, gauge, bullet | Table (for single value) |
| Geographic | Choropleth map, bubble map | Bar chart by region |
| Ranking | Sorted horizontal bar, table | Unsorted bar chart |
| Composition change | Stacked area, 100% stacked bar | Multiple pie charts |

### Visualization Best Practices

- Start Y-axis at zero for bar charts
- Use consistent time axis across all temporal charts
- Label data directly when possible (avoid legend-hunting)
- Limit pie/donut charts to 5 segments maximum
- Use sparklines for compact trend indication in tables
- Apply conditional formatting for status indicators (red/yellow/green)

## Step 5: Interactivity Design

Define user interaction patterns:

| Interaction | Purpose | Implementation |
|-------------|---------|----------------|
| Global filters | Scope all visuals to a segment | Date range, region, product line |
| Cross-filtering | Click one chart to filter others | Highlight/filter linked visuals |
| Drill-down | Move from summary to detail | Click bar segment to see records |
| Tooltips | Show detail on hover | Additional metrics, explanations |
| Bookmarks/Views | Save filter combinations | Named views for common analyses |
| Alerts | Notify on threshold breach | Email, Slack, in-app notification |
| Export | Share data externally | PDF, CSV, scheduled email |

### Interaction Guidelines

- Every filter must have a clear "reset" option
- Show active filter state prominently
- Limit drill-down depth to 3 levels maximum
- Tooltips should add information, not repeat what is visible
- Mobile views should disable complex interactions

## Step 6: Refresh Cadence and Performance

Plan data freshness and dashboard performance:

| Dashboard Type | Data Freshness | Acceptable Load Time | Cache Strategy |
|----------------|---------------|---------------------|----------------|
| Strategic | Daily or weekly | < 5 seconds | Aggressive — pre-compute |
| Tactical | Daily | < 3 seconds | Moderate — daily refresh |
| Operational | Real-time / 5-min | < 2 seconds | Light — streaming or frequent refresh |
| Analytical | On-demand | < 10 seconds | Query-time with result caching |

### Performance Optimization

- Pre-aggregate data for high-level views
- Use materialized views or summary tables
- Limit default date range (last 30 days, not all time)
- Paginate large tables (show top 20, load more on scroll)
- Use incremental refresh where supported
- Monitor query execution time per visual

## Output Format

Present the dashboard design as:

1. **Design Brief** (audience, purpose, type, key decisions supported)
2. **Metric Inventory** (table of all metrics with hierarchy level, source, chart type)
3. **Wireframe Layout** (ASCII or description of section placement)
4. **Visualization Specifications** (chart type, axes, colors, interactions per visual)
5. **Filter and Interactivity Plan** (global filters, cross-filters, drill-downs)
6. **Data Requirements** (sources, transformations, refresh schedule)
7. **Style Guide** (colors, fonts, number formatting, conditional rules)
8. **Implementation Notes** (tool-specific guidance, performance considerations)

## Quality Checklist

Before delivering the dashboard design, verify:

- [ ] Dashboard has a clear title and purpose statement
- [ ] Audience is identified and design matches their literacy level
- [ ] Metric hierarchy follows the pyramid (North Star > Primary > Supporting > Detail)
- [ ] Layout follows a recognized pattern (Z, F, hub-spoke, or narrative)
- [ ] Chart types are appropriate for the data relationships
- [ ] Color palette is consistent and accessible (colorblind-safe)
- [ ] Interactivity is purposeful, not gratuitous
- [ ] Refresh cadence matches decision frequency
- [ ] Mobile or alternative views are considered

## Edge Cases

- **No clear North Star metric**: Facilitate a stakeholder alignment session before designing; present 2-3 candidates with trade-offs
- **Too many stakeholders**: Create a hub page with role-based linked dashboards rather than one overloaded view
- **Real-time requirements on batch data**: Set clear expectations on latency; use "last updated" timestamps prominently
- **Legacy tools with limited interactivity**: Design for static consumption; use conditional formatting and summary tables
- **Highly regulated data**: Add access control layer; redact or aggregate sensitive fields; log dashboard access
- **Dashboard fatigue**: Audit existing dashboards before creating new ones; consolidate or retire unused reports
