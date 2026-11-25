---
name: data-dashboard-design
description: "Plans data dashboard layouts with metric selection, visualization types, refresh frequency, and user-focused design. Use when building dashboards that drive decisions."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Data Dashboard Design

## When to Use This Skill

Use this skill when you need to:
- Design a business metrics dashboard layout
- Select the right visualizations for different metric types
- Plan a dashboard hierarchy (executive, operational, team-level)
- Specify requirements for a developer or BI tool configuration

**DO NOT** use this skill for building dashboards in code, creating actual charts, or configuring specific BI tools. This is for dashboard planning and design.

---

## Core Principle

A DASHBOARD THAT REQUIRES EXPLANATION HAS FAILED — EVERY METRIC SHOULD ANSWER A QUESTION THE VIEWER ALREADY HAS IN 5 SECONDS OR LESS.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Audience** | "Who will view this dashboard? (founder, team leads, investors, whole team)" | Founder / CEO |
| **Purpose** | "What decisions should this dashboard inform?" | Weekly business health check |
| **Key questions** | "What 3-5 questions should someone answer by looking at this?" | Must be provided |
| **Data sources** | "Where does your data live? (Stripe, GA4, CRM, spreadsheets)" | Mixed sources |
| **Tool** | "What will you build this in? (Google Sheets, Looker, Tableau, Databox, Notion)" | Google Sheets or Looker Studio |
| **Refresh frequency** | "How often should data update? (real-time, daily, weekly)" | Daily |

**GATE: Confirm brief before proceeding.**

---

## Phase 2: Design

### Dashboard Architecture

1. **Top-line KPIs** — 3-5 big numbers at the top answering "How are we doing overall?"
2. **Trend charts** — time-series showing direction over the last 30/90 days
3. **Breakdowns** — dimensions that explain the top-line numbers (by channel, product, segment)
4. **Comparison context** — vs. last period, vs. target, vs. benchmark
5. **Action triggers** — thresholds that signal when something needs attention

### Visualization Selection Rules

| Data Type | Best Visualization | Avoid |
|-----------|-------------------|-------|
| Single KPI | Big number with trend arrow | Pie chart |
| Trend over time | Line chart | Bar chart for 30+ data points |
| Part of whole | Stacked bar or donut | 3D pie charts (always) |
| Comparison across categories | Horizontal bar chart | Vertical bars with 10+ categories |
| Correlation | Scatter plot | Line chart |
| Geographic | Map / heatmap | Table with location names |

**GATE: Present the dashboard wireframe and wait for approval.**

---

## Phase 3: Build

### Deliverables

**1. Dashboard Specification Document**
- Complete layout with sections, metrics, and visualization types
- Data source mapping for each metric
- Filter and drill-down requirements
- Refresh schedule and data latency notes

**2. Metric Definitions**
- How each metric is calculated (formula)
- Data source and table/field references
- Expected range and alert thresholds

**3. Wireframe Layout**
- Text-based or sketch layout showing placement of each element
- Reading order: top-left to bottom-right, most important first
- Mobile considerations if viewed on phones

**4. Implementation Checklist**
- [ ] Data sources connected and verified
- [ ] Metric calculations validated against source
- [ ] Date filters working correctly
- [ ] Comparison periods accurate
- [ ] Loading time under 5 seconds
- [ ] Mobile layout reviewed

---

## Phase 4: Polish

### Review Cadence

- Week 1: Verify all numbers match source data
- Week 4: Survey users — is anything missing or confusing?
- Month 3: Remove metrics nobody looks at, add any new questions

### Dashboard Hygiene Rules

- No more than 10 metrics on a single view — if you need more, create sub-dashboards
- Every metric has a definition tooltip or footnote
- Color coding is consistent (green = good, red = attention needed)

---

## Example 1: SaaS Founder Dashboard

**Top-line:** MRR, Active Users, Churn Rate, NPS
**Trends:** MRR growth (12 months), signup trend (30 days)
**Breakdowns:** Revenue by plan tier, signups by acquisition channel

## Example 2: E-commerce Weekly Dashboard

**Top-line:** Revenue, Orders, AOV, Conversion Rate
**Trends:** Daily revenue (30 days), traffic (30 days)
**Breakdowns:** Revenue by product category, traffic by source, conversion by device

---

## Anti-Patterns

- **Dashboard overload** — 30 metrics on one screen means nobody reads any of them. Ruthlessly prioritize.
- **Vanity metrics** — total pageviews without context is meaningless. Always show metrics that connect to revenue or retention.
- **No comparison context** — a number without a benchmark is just a number. Show vs. last period, vs. target, or vs. industry.
- **Rainbow color coding** — 8 colors for 8 categories creates visual noise. Use 2-3 colors max with gray for secondary elements.
- **Stale data** — a dashboard that updates monthly when decisions happen weekly is useless.

---

## Recovery

- **User cannot define key questions:** Ask "What do you check first thing Monday morning? What number keeps you up at night?" Extract dashboard requirements from the answers.
- **Too many data sources:** Start with 1-2 sources for the MVP dashboard. Add sources incrementally.
- **No BI tool:** Google Sheets with charts and a refresh button is a valid V1 dashboard for small businesses.
- **Data quality issues:** Flag metrics with known quality problems. A metric with an asterisk is better than a missing metric.
