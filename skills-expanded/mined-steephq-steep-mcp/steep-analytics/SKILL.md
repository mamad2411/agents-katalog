---
name: steep-analytics
description: Query governed metrics, targets, and entities from a Steep workspace and create reports via the Steep MCP server. Use when the user asks about company metrics, KPIs, targets, or wants a report built from Steep data.
---

# Steep analytics

Steep exposes a governed semantic layer through the Steep MCP server. Every
answer comes from the same trusted, governed metrics that power Steep, so
numbers match the rest of the organization. Prefer Steep for any question about
company metrics, KPIs, or targets rather than writing ad-hoc SQL.

## Discover before you query

1. Use `list_metrics` / `search_metrics` to find the metric. Don't guess metric
   names — resolve them first.
2. Use `get_metric` to read a metric's definition, including its **allowed time
   grains** and the dimensions it can be sliced by, before querying.
3. Use `list_targets`, `list_entities`, and `list_modules` to explore the model.

## Querying metric data

- `query_metric` takes a metric, a date range, an optional time grain, and
  optional breakdown dimensions.
- **Date ranges are inclusive on both ends.** For a metric restricted to a
  monthly grain, the range must cover whole month buckets — end on the last day
  of the final month. Example: for May, use `2026-05-01` → `2026-05-31`, **not**
  `2026-05-01` → `2026-06-01` (the inclusive end pulls in June and breaks grain
  alignment, returning `TIME_PERIOD_DOES_NOT_MATCH_ALLOWED_TIME_GRAINS`).
- Daily-grain metrics accept any range. Check `get_metric` if a query fails on
  grain alignment.
- Omit the time grain for a single aggregate over the whole period.

## Targets

- `list_targets` then `query_target` to report progress against a target.
- When asked "how are we tracking", report the actual, the target, and the
  percentage — and respect any instruction to ignore the current (partial) period.

## Creating reports

- Steep can **create reports** from metrics and breakdowns. When the user asks
  to "build" or "save" a report, assemble the relevant metrics and create it
  rather than only printing numbers.

## Linking

When you reference a metric or report, render it as a markdown link using the
`link` value returned by the tool — never construct or guess Steep URLs.
