---
name: crm-dashboards
description: Build and maintain dashboards in the CRM (Twenty) — dashboards, tabs, and widgets (charts, counts, tables over CRM data). Use for "make me a dashboard", pipeline/activity reporting surfaces, or editing existing dashboard widgets.
---

# CRM Dashboards

Read the `crm` skill first. Dashboards are grids of widgets, organized in
tabs, each widget an aggregation or list over one object.

## Reading

- `List Dashboards` → `Get Dashboard` (tabs + widgets and their configs).
- `Search dashboards` / `Group dashboards` when hunting by name or owner.

## Building

1. Prefer `Create Complete Dashboard` for a new dashboard: name, tabs, and
   widgets in one call. Follow its input schema exactly.
2. Incremental edits: `Add Dashboard Tab`, `Add Dashboard Widget`,
   `Update Dashboard Widget`, `Delete Dashboard Widget`, `Delete dashboard`.
3. A widget config names the source object, an aggregation (count, sum, avg
   of a numeric/currency field), an optional group-by field, a filter (same
   DSL as search), and a display type. Validate every object and field name
   against `Get Object Metadata` first — a widget over a misspelled field
   renders empty.

## Design guidance

- Mirror the question, not the schema: "pipeline health" = sum of open
  opportunity/deal amount by stage, count closing this month, win rate trend;
  "activity" = tasks completed per member, notes logged per week.
- Currency aggregations run over `amount.amountMicros`; label widgets so
  readers know units, and keep one currency per widget.
- Reuse the filters users already trust: copy filter definitions from an
  existing view (`Get View Filters`) into widget filters.
- After building, offer a `Navigate App` deep link to the dashboard and ask
  whether to pin it to the navigation menu (`crm-admin`).
