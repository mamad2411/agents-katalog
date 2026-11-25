---
name: build-dashboard
description: Build an interactive, self-contained HTML dashboard with multiple charts, KPI cards, filters, and sortable tables in a single file. Use when the user asks for a "dashboard", "executive overview", "monitoring view", "ops snapshot", or wants several charts plus filters in one shareable HTML page. Covers cybersecurity ops dashboards (incidents, compliance, vendor risk, customer trust, SLA/uptime). Do NOT use for a single chart (data:create-viz), pure data analysis with no UI (data:analyze), generic UI styling (ckmui-styling), data profiling (data:explore-data), GAAP financial statements (finance:financial-statements), narrative status reports (operations:status-report), or compliance program tracking that doesn't need a visual dashboard (operations:compliance-tracking).
argument-hint: "<description> [data source]"
---

# build-dashboard - Interactive HTML Dashboards

Build a single self-contained HTML file with KPI cards, multiple Chart.js charts, dropdown / date filters that update everything in sync, and a sortable detail table. Opens in any browser, no server, no build step.

## When to use this skill (vs. siblings)

| Signal | Use this | Use instead |
|---|---|---|
| "Build a dashboard" / "monitoring view" / "executive overview" | build-dashboard | - |
| "Make a chart of X" (single viz) | - | data:create-viz |
| "Why did X drop?" / pure analysis | - | data:analyze |
| "Style this component" / general UI | - | ckmui-styling |
| "Profile this dataset" / null rates | - | data:explore-data |
| "Generate a P&L / balance sheet" | - | finance:financial-statements |
| "Write a weekly status update" (prose) | - | operations:status-report |
| "Track our SOC 2 controls" (no viz) | - | operations:compliance-tracking |
| "Multiple charts + filters + KPIs in one HTML file" | build-dashboard | - |

If the user wants a security incident dashboard, compliance program dashboard, vendor risk dashboard, customer trust / SLA dashboard, or ops dashboard, use this skill and load `references/cybersec-dashboards.md`.

## Workflow

1. **Clarify scope** - Purpose (exec / ops / deep-dive), audience, key metrics, slice dimensions, data source (live query, paste, CSV, sample).
2. **Gather data** - Query if a warehouse is connected; otherwise parse pasted data or generate realistic sample data and note the assumption.
3. **Pick layout** - Header + filters / KPI row (2-4 cards) / chart row (1-3 charts) / detail table. Adapt to content.
4. **Load the relevant references** (see routing table below) and assemble the HTML.
5. **Save** as `<name>_dashboard.html`, open in browser, confirm rendering, give update instructions.

## Reference routing - load only what the task needs

All working code lives in `references/`. Read them with the Read tool when the task hits the trigger.

| You need | Load |
|---|---|
| HTML skeleton, Chart.js CDN tags, Dashboard class shell | `references/base-template.md` |
| Line / bar / doughnut / stacked / mixed charts, color palette, filter-triggered chart updates | `references/chart-patterns.md` |
| Dropdown filters, date-range filters, combined filter logic, sortable tables, pagination | `references/filter-patterns.md` |
| CSS variables, layout grid, KPI card styles, chart container, table styles, responsive + print | `references/styling-system.md` |
| Datasets >1k rows, pre-aggregation, downsampling, animation tuning | `references/performance.md` |
| Worked cybersecurity dashboards (incidents, compliance, vendor risk, trust, ops) | `references/cybersec-dashboards.md` |

**Minimum viable load** for any new dashboard: `base-template.md` + `styling-system.md` + the chart types you need from `chart-patterns.md`. Add `filter-patterns.md` if there are >0 filters, `performance.md` if data >1k rows, `cybersec-dashboards.md` if the topic is security / compliance / vendor / trust / on-call.

## Cybersecurity dashboard patterns (high-value defaults)

For solo / small-team security operators, the five recurring dashboards are:

1. **Security incident dashboard** - alert volume by severity, MTTR trend, top-alerting sources, open vs. closed.
2. **Compliance program dashboard** - control freshness heatmap, audit-cycle gantt, evidence age, framework cross-mapping (SOC 2 / ISO 27001 / HIPAA / PR Act 111).
3. **Vendor risk dashboard** - vendor risk scores, paperwork gaps (DPA / SOC 2 / insurance), expirations in next 90 days, sub-processor changes.
4. **Customer trust dashboard** - uptime SLA vs. target, security questionnaire turnaround, SOC 2 audit status, transparency-report metrics.
5. **Operations dashboard** - ticket volume by priority, P1 count, on-call load distribution, runbook freshness.

Each is fully specified (KPIs, charts, filters, table, sample schema) in `references/cybersec-dashboards.md`. When the user describes any of these, open that file first, copy the spec, then assemble using the other references.

## Output requirements

Every dashboard you produce must:

- Be a single `.html` file with no external assets except the Chart.js CDN scripts (use the SRI hashes in `base-template.md`).
- Embed data as JSON in a `const DATA = ...` block.
- Use the `:root` CSS variable system from `styling-system.md` (no inline color literals in JS chart configs - reference the `COLORS` array).
- Wrap state in a `Dashboard` class with `init / applyFilters / renderKPIs / renderCharts / updateCharts / renderTable` methods (skeleton in `base-template.md`).
- Be responsive (mobile breakpoint at 768px) and print-friendly (rules in `styling-system.md`).
- Note in the footer "Data as of: <date>" - even sample dashboards need this so it's clear what the snapshot represents.

## Data-source decisions

- **Warehouse connected** - Query, then embed results as JSON.
- **Pasted / CSV** - Parse, clean, embed.
- **No data** - Generate realistic sample data matching the described schema, label the dashboard "Sample data", give clear swap-in instructions in a comment block at the top of the script.
- **>10k rows** - Pre-aggregate before embedding (see `references/performance.md`).

## Examples

```
/build-dashboard Security incident dashboard for last 90 days - alert volume by severity, MTTR trend, top sources, open vs closed.
```
-> Load `cybersec-dashboards.md` (example 1) + base + styling + chart-patterns (line + stacked bar + horizontal bar + doughnut) + filter-patterns (date range + severity dropdown).

```
/build-dashboard Vendor risk overview for our 40 SaaS vendors - risk score, missing paperwork, expirations next 90 days.
```
-> Load `cybersec-dashboards.md` (example 3) + base + styling + chart-patterns (bar + doughnut) + filter-patterns (dropdown + sortable table).

```
/build-dashboard Monthly sales dashboard from the orders table - revenue trend, top products, regional breakdown.
```
-> Load base + styling + chart-patterns (line + bar + doughnut) + filter-patterns (region + date).

## Tips

- Self-contained HTML files are shareable - email or attach. Good for board updates and customer trust pages.
- For live / streaming dashboards point to a BI tool instead - this skill makes point-in-time snapshots.
- User can ask for "dark mode", "presentation mode", or a specific brand palette - swap the CSS variables in `:root`.
- For Puerto Rico cybersec context: PR Act 111 (data breach notification) belongs on the compliance dashboard alongside SOC 2 / ISO 27001 / HIPAA.
