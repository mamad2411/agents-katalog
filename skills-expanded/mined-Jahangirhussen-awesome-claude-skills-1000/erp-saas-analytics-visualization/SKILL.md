---
name: erp-saas-analytics-visualization
description: Use automatically for ERP, SaaS, POS, CRM or e-commerce analytics - dashboards, KPIs, charts, graphs, reports and metrics (MRR, ARR, churn, NRR, LTV, CAC, cohort, funnel, sales, inventory, finance, HR, CRM, subscription, forecasting). Chooses KPIs, chart types, filters, roles and data for the business question, defines calculations, and validates numbers. Does not build the surrounding app (database, backend, UI come from other skills) and is not for SEO ranking reports (use seo-master).
---

# ERP + SaaS Analytics Visualization

## Purpose
Turn a business question into the right KPI, data definition, chart, dashboard layout, interactions and permissions for ERP/SaaS products.

## When to use
Dashboard, report, chart, KPI or metric requests for ERP modules (sales, inventory, finance, HR, CRM, manufacturing, projects, logistics, assets), SaaS (MRR/ARR, subscriptions, cohorts, funnels, product, support, marketing, infrastructure), or POS/e-commerce analytics.

## When NOT to use
- Building the database/backend/UI of the app (other skills; this skill specifies analytics only).
- SEO traffic/ranking dashboards -> `seo-master` (analytics child).
- One-off statistical analysis of a dataset -> data analysis skills.

## Inputs
Project/modules, roles, available tables/fields, time grain and filters; infer from repo and schema when present.

## Core workflow
1. Detect modules from the request and repo ("SaaS ERP" = both); use only modules whose data exists.
2. Open `DASHBOARD-REGISTRY.md` for the role dashboard; open `GRAPH-REGISTRY.md` rows by module code (e.g. ERP-SALES, SAAS-CORE).
3. Open only the matching `references/*.md` (charts by module, `subscription-metrics.md` formulas, `cohort-analysis.md`, `funnel-analysis.md`).
4. Pick each chart by the business question using `CHART-SELECTION-MATRIX.md`; separate KPI, trend, comparison, composition, diagnostic.
5. Define per chart: source, fields, aggregation, grouping, time dimension, calculation, filters, refresh, permission.
6. Implement with the project's existing chart library; aggregate server-side; enforce role access on the server.
7. Validate against source totals, then test filters, empty/error states, responsiveness, accessibility.

## Decision rules
- 8-12 widgets per dashboard; choose by role, module, data availability, decision value.
- Never choose a chart for looks; if the registry default does not fit the data shape, override and note why.
- Keep metric definitions consistent (period, currency, timezone, refund/discount/failed-payment handling).

## Edge cases and failure handling
- Missing data fields -> propose the minimal schema addition or a proxy metric, mark it as approximate.
- Sparse cohorts / partial periods -> grey out incomplete cells and show cohort size.
- Mixed currencies/timezones -> normalize before aggregating.
- Sensitive metrics (salary, finance) -> hide from unauthorized roles server-side.

## Validation
Reconcile each KPI with a direct query on source data; verify filters change results correctly; test mobile layout; confirm accessible summary and table view exist; check refresh cadence and query cost.

## Output requirements
Dashboard spec or implementation: widgets with chart type, question answered, query/aggregation, filters, drill-down, role access; short `DONE` with open data gaps.

## Example
"SaaS dashboard" -> KPI cards (MRR, ARR, customers, churn, NRR, LTV:CAC) -> MRR trend + MRR movements -> revenue by plan -> retention cohort heatmap -> trial-to-paid funnel; roles: founder/admin; filters: date, plan, country; MRR = sum of normalized monthly recurring revenue of active subscriptions.

## Related / dependencies
`GRAPH-REGISTRY.md` (344 graphs), `DASHBOARD-REGISTRY.md` (14 dashboards), `CHART-SELECTION-MATRIX.md`, `references/`; database, backend, UI/UX, security, testing skills for the surrounding system.

## References
`references/subscription-metrics.md` (formulas), `cohort-analysis.md`, `funnel-analysis.md`, `chart-selection.md`, `dashboard-patterns.md`, `accessibility.md`, module chart files.
