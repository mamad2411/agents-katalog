# analyze-dashboards

## Description
Browses the Strategy Cloud library, inventories all dashboards, opens each one, and detects anomalies, threshold breaches, and trends using the detection patterns defined in `references/finding-patterns.json`.

## Trigger
This skill is invoked automatically when a compliance or strategy review needs dashboard analysis, or when orchestrated by user-invoked commands.

## Instructions

### Query Guidelines

- **Use natural language, not SQL.** Both Strategy AI agents and the MCP USL accept natural language queries. Write questions the way you would ask a colleague (e.g., "Show me dashboards with declining revenue trends").
- **Only use tables in the playground schema.** All queries should target the playground schema exclusively. Do not reference tables outside of it.
- **Default environment and dashboard.** For dashboard viewing and analysis (this skill), use `demo.microstrategy.com` as the default environment and the **Office Royale Sales** dashboard unless otherwise specified. For all other analysis (data queries, reporting, etc.), use the Strategy USL and Strategy Agent MCPs directly.
- **Tool routing fallback.** If no specific project or assignee is configured for an enterprise tool, discover the best-fit project or workspace in that tool automatically rather than skipping the routing.
- **Missing MCP servers.** If an enterprise tool's MCP server is not connected, skip that tool's routing step. Dashboard analysis should always run regardless — only the downstream enterprise routing is skipped.

### 1. Discover — Browse the Strategy Library

Use the Strategy MCP server to access the Strategy Cloud library:

- Navigate the library folder structure (typically organized by LOB: Sales/, Marketing/, Finance/, Operations/, HR/, etc.)
- Inventory every dashboard: capture **name**, **folder path**, **last modified date**, and **dashboard URL**
- Aim for **100% coverage** — do not sample; analyze every dashboard

### 2. Analyze — Open Each Dashboard

For each inventoried dashboard:

- Open/query the dashboard to retrieve its visualizations and data
- Review systematically: left-to-right, top-to-bottom across all visualizations
- Apply the detection patterns from `references/finding-patterns.json`:

**Anomaly Detection:**
- **Spikes**: Value increase >20% vs prior period
- **Drops**: Value decrease >15% vs prior period
- **Outliers**: Data points beyond 2 standard deviations from mean
- **Gaps**: Missing data periods (null or absent values)

**Threshold Breaches:**
- Red/critical status indicators
- Yellow/warning indicators approaching threshold
- Target misses with negative variance (>10% for warning, >20% for critical)
- Declining trend arrows

**Trend Patterns:**
- 3+ consecutive periods moving in the same direction
- Acceleration (rate of change increasing)
- Reversal (direction change after established trend)

**Comparisons:**
- Year-over-year variance >15%
- Actual vs budget/forecast variance >10%
- Regional or product peer variance >20%

### 3. Document Findings

For each detected finding, capture:

```json
{
  "dashboard_name": "...",
  "dashboard_url": "...",
  "dashboard_folder": "...",
  "finding_type": "anomaly|threshold_breach|trend|comparison",
  "severity": "critical|warning|informational",
  "metric": "Name of the affected metric",
  "current_value": "Current metric value",
  "comparison_value": "Prior period / target / peer value",
  "variance_percent": 0.0,
  "details": "Human-readable description of what was found",
  "visualization_source": "Name/position of the chart or table"
}
```

### 4. Return Results

Return a JSON object:

```json
{
  "analyzed_at": "ISO-8601 timestamp",
  "dashboards_inventoried": 0,
  "dashboards_analyzed": 0,
  "coverage_percent": 100,
  "total_findings": 0,
  "findings_by_severity": {
    "critical": 0,
    "warning": 0,
    "informational": 0
  },
  "findings": [ ... ]
}
```

## Error Handling
- If a dashboard fails to load, log the error and continue with remaining dashboards
- Report coverage percentage based on successfully analyzed dashboards
- Note any inaccessible dashboards in the output
