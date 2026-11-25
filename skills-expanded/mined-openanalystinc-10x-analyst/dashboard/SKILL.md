---
name: dashboard
description: "Build a standalone interactive HTML dashboard with Chart.js from any dataset"
argument-hint: "[dataset-name]"
risk: "safe"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Write, Bash, Glob, Grep
model: claude-sonnet-4-6
context: fork
agent: general-purpose
---

# 10x Analyst — Dashboard Builder

Build a standalone, interactive HTML dashboard from any dataset.

## Overview

Generates a single `dashboard.html` file with KPI cards, interactive Chart.js charts, and data tables. Reads from `input/<dataset>/`, writes to `output/<dataset>/dashboard.html`. Fully self-contained — open in any browser, no server needed.

## When to Use

- User asks for a "dashboard", "interactive view", "HTML report", or "visual summary"
- User wants something they can open in a browser and share
- User needs interactive charts with hover tooltips and toggleable legends

## Path Resolution

Parse `$ARGUMENTS` to get dataset name.
- **Input:** `input/<dataset-name>/`
- **Output:** `output/<dataset-name>/dashboard.html`

## Instructions

### Step 1: Data Loading
1. Find and load all data files at `input/<dataset>/`
2. Clean and prepare data (same cleaning steps as `:clean`)
3. Join related tables if multiple files present

### Step 2: Metrics Computation
4. Compute KPIs based on data domain:

**E-Commerce:**
- Total revenue, total orders, total customers, AOV
- Revenue growth (MoM), top product, top category
- Repeat customer rate

**General:**
- Record count, column count, date range
- Key numeric aggregates (sum, mean, max for important columns)

5. Compute chart data:
- Trend data (time series aggregations)
- Top-N data (category rankings)
- Segment data (group breakdowns)
- Correlation data (numeric column correlations)

### Step 3: Dashboard Generation
6. Create output directory: `mkdir -p output/<dataset>`
7. Write `output/<dataset>/dashboard.html` using a Python script that:
   - Loads data from `input/<dataset>/`
   - Computes KPIs and chart data
   - Generates standalone HTML with:
     - Chart.js from CDN (`https://cdn.jsdelivr.net/npm/chart.js`)
     - KPI cards row at top with delta indicators
     - 2x2 chart grid (trend line, top-N bar, segment donut, heatmap)
     - Summary data table
     - 10x.in branding: `#FF6B35` primary, `#004E89` secondary, `#F5EDE0` background
     - Responsive CSS grid (stacks on mobile)
     - All data embedded as inline JavaScript objects

8. Tell the user how to open it: `start output/<dataset>/dashboard.html`

## Examples

```bash
/10x-analyst:dashboard shopify-data
```

## Limitations

- Requires internet for Chart.js CDN (first load)
- Single page — no multi-page navigation
- Data embedded inline — very large datasets may produce large HTML files
- Static snapshot — does not auto-update when source data changes

---
*Developed by [10x.in](https://10x.in) | 10x-Analyst v1.0.0*
