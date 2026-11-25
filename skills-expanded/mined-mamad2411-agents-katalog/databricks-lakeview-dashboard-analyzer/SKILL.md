---
name: databricks-lakeview-dashboard-analyzer
description: Analyze existing Databricks AI/BI (Lakeview) dashboards using the Lakeview REST API (default) or Chrome DevTools for visual inspection. Extracts datasets, queries, widgets, and page structure from dashboard definitions. Use when analyzing dashboards, extracting dashboard data, or when user shares a Databricks dashboard URL.
---

# Databricks Lakeview Dashboard Analyzer

Analyze Databricks AI/BI (Lakeview) dashboards — API-first, with optional browser-based visual analysis.

**Note:** This skill is for *analyzing existing dashboards*. To create dashboards programmatically, use `/databricks-lakeview-dashboard`.

## Prerequisites

**Required:**
- Databricks CLI installed and authenticated (`/databricks-authentication`)
- Dashboard URL or dashboard ID
- Read access to the dashboard

**Optional (for visual analysis only):**
- Chrome DevTools MCP Server (available in vibe by default)

## Quick Start — API Workflow (Default)

This is the **primary** approach. It returns the full dashboard definition in a single API call — no browser needed.

### 1. Parse the Dashboard URL

Extract the dashboard ID from the URL using the pattern `/dashboardsv3/([^/?]+)`:

| Platform | URL Pattern | Example |
|----------|-------------|---------|
| Azure | `https://adb-XXXXX.azuredatabricks.net/dashboardsv3/{ID}/published?o=ORGID` | ID = `01efb...` |
| AWS | `https://WORKSPACE.cloud.databricks.com/dashboardsv3/{ID}/published` | ID = `01efb...` |

The workspace host (everything before `/dashboardsv3/`) determines which CLI profile to use.

### 2. Determine the CLI Profile

Use the workspace host to find the matching Databricks CLI profile. Follow the patterns in `/databricks-authentication` to list profiles and match by host:

```bash
databricks auth profiles --output json
```

Match the workspace host from the URL to a profile's `host` field.

### 3. Fetch the Dashboard Definition

```bash
databricks api get /api/2.0/lakeview/dashboards/{DASHBOARD_ID} --profile {PROFILE}
```

This returns the full dashboard object including metadata and the serialized definition.

### 4. Double-Parse the Definition

The response contains a `serialized_dashboard` field that is a **JSON-encoded string** (not a nested object). You must parse it twice:

1. First parse: the API response JSON → gives you `serialized_dashboard` as a string
2. Second parse: `JSON.parse(serialized_dashboard)` → gives you the actual dashboard structure

The parsed dashboard definition contains:
- **`datasets`** — Named datasets with their SQL queries
- **`pages`** — Dashboard pages/tabs, each containing widgets
- **`widgets`** — Visualizations (charts, tables, counters, text, filters) with their configuration

### 5. Summarize the Dashboard

From the parsed definition, extract and present:

- **Datasets**: List each dataset name and its SQL query
- **Pages**: List each page/tab name
- **Widgets per page**: For each page, list widgets with their type (bar chart, table, counter, etc.) and which dataset they reference
- **Filters**: Any filter widgets and their configuration
- **Key metrics**: Identify counters and KPI widgets

## Visual Analysis — Chrome DevTools (Optional)

Use this approach **only** when the user explicitly asks for:
- Screenshots or visual appearance of the dashboard
- Chart color/styling analysis
- Interactive UI exploration (clicking filters, downloading CSVs)
- Visual trend interpretation from rendered charts

### Core Interaction Model

All interactions require **UIDs from snapshots** — you cannot use CSS selectors directly:

1. `take_snapshot` → Returns accessibility tree with element UIDs
2. Use UID with `click`, `fill`, `hover`

```bash
# Get UIDs
mcp__chrome-devtools__take_snapshot

# Use UID to interact
mcp__chrome-devtools__click '{"uid": "1_3"}'
```

### Two Analysis Tools

| Tool | Purpose | Use For |
|------|---------|---------|
| `take_screenshot` | Visual capture | Charts, colors, trends, layouts |
| `take_snapshot` | Text/structure extraction | Tables, labels, filter values, getting UIDs |

**WARNING:** Full page screenshots of complex dashboards can be 500KB-1MB+ and may disconnect the MCP server. Prefer viewport screenshots.

### Browser Workflow

#### 1. Navigate to Dashboard

```bash
mcp__chrome-devtools__navigate_page '{"type": "url", "url": "DASHBOARD_URL"}'
```

#### 2. Handle Authentication

If redirected to login, user authenticates manually (30-60 seconds). Check status:

```bash
mcp__chrome-devtools__evaluate_script '{"function": "() => ({ url: location.href, title: document.title })"}'
```

#### 3. Wait for Load

```bash
mcp__chrome-devtools__wait_for '{"text": "Dashboard Title", "timeout": 15000}'
```

#### 4. Capture and Analyze

```bash
# For text/structure (tables, filters, UIDs)
mcp__chrome-devtools__take_snapshot

# For visuals (charts, trends)
mcp__chrome-devtools__take_screenshot
```

### Key Techniques

#### URL Filter Manipulation (Fastest Method)

Change filters via URL instead of clicking through UI:

```
&f_PAGEID%7EFILTERID=VALUE
```

(`%7E` = URL-encoded `~`)

#### Container Scrolling

Dashboard content is in a scrollable div, NOT the window. Use `document.querySelector('[class*="dbsql-legacy-mfe-page"]').scrollBy(0, 600)` in `evaluate_script`. See [ELEMENT_INTERACTION.md](references/ELEMENT_INTERACTION.md#scrolling) for details.

#### Downloading Data via Ellipsis Menus

Every visualization has a ⋮ menu for downloading data:

1. **Hover** over chart heading to reveal ⋮ button
2. **Click** ellipsis button
3. **Keyboard navigate**: ArrowDown → ArrowRight (Download) → ArrowRight (Data) → Enter (CSV)
4. File downloads to `~/Downloads/{ChartName}-{YYYY-MM-DD}.csv`

Use keyboard navigation (ArrowDown/ArrowRight/Enter) instead of clicking — nested menus collapse easily.

#### React Controlled Inputs

For autocomplete filters that don't respond to normal `fill()`:

```javascript
const input = document.activeElement;
const setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;
setter.call(input, 'search term');
input.dispatchEvent(new Event('input', { bubbles: true }));
```

#### Navigating Dashboard Tabs

Look for `tab` elements in snapshots. Click to switch, or navigate via URL (tabs have page IDs like `/pages/abc123`).

### Best Practices

1. **Always take snapshot first** to get UIDs before interacting
2. **Prefer viewport screenshots** over full page (avoids MCP disconnection)
3. **Wait after actions** — use `wait_for` or brief delay after clicking filters
4. **Save progress frequently** — sessions can expire during long analysis
5. **Check Y-axis scales** when comparing charts across filter changes
6. **Combine methods** — screenshots for visuals, snapshots for precise values

### MCP Tools Reference

| Tool | Purpose | Key Parameters |
|------|---------|----------------|
| `navigate_page` | Go to URL | `type: "url"`, `url` |
| `wait_for` | Wait for text | `text`, `timeout` |
| `take_screenshot` | Visual capture | `fullPage`, `format` |
| `take_snapshot` | Text/structure | Returns UIDs |
| `evaluate_script` | Run JavaScript | `function: "() => { ... }"` |
| `click` | Click element | `uid`, `dblClick` |
| `fill` | Fill text field | `uid`, `value` |
| `hover` | Hover element | `uid` |
| `press_key` | Keyboard input | `key` |

## Reference Documentation

- **Element Interaction** (clicking, filling, dropdowns, tabs): See [ELEMENT_INTERACTION.md](references/ELEMENT_INTERACTION.md)
- **Data Extraction** (tables, downloads, JavaScript extraction): See [DATA_EXTRACTION.md](references/DATA_EXTRACTION.md)
- **Complete Workflows** (summary, filtering, time series, Q&A, multi-tab): See [WORKFLOWS.md](references/WORKFLOWS.md)
- **Chart Analysis** (interpreting visualizations): See [CHART_INTERPRETATION_GUIDE.md](references/CHART_INTERPRETATION_GUIDE.md)
- **Troubleshooting** (MCP disconnects, auth issues, session expiration): See [TROUBLESHOOTING.md](references/TROUBLESHOOTING.md)

## Related Skills

- `/databricks-authentication` - CLI-based authentication
- `/databricks-lakeview-dashboard` - Create dashboards programmatically
- `/databricks-query` - Run SQL queries directly
- `/databricks-warehouse-selector` - Select warehouse for queries
