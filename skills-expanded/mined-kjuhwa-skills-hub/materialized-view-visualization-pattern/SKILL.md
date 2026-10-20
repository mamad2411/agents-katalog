---

name: materialized-view-visualization-pattern
description: Visual layout conventions for rendering materialized view lifecycle (base tables → MV → queries) with staleness indicators
category: design
triggers:
  - materialized view visualization pattern
tags: [design, materialized, view, visualization]
version: 1.0.0
---

# materialized-view-visualization-pattern

Materialized-view UIs benefit from a three-tier horizontal layout: base tables on the left (source-of-truth with write activity indicators), the materialized view node in the center (showing last-refresh timestamp, row count, and a staleness gauge), and dependent queries/consumers on the right. Use directed edges with animated dots during refresh events to make the ETL/incremental-merge flow visible; color the MV node by staleness state (green: fresh <TTL/3, amber: aging, red: stale beyond TTL, gray: refreshing-in-progress). A secondary lag strip under the MV node plots `now() - last_refresh_at` over time so users can see refresh cadence versus data drift at a glance.

For the staleness dashboard variant, pair the topology view with a companion panel showing three synchronized metrics: (1) row delta between base and MV, (2) refresh duration histogram, (3) query-hit-on-stale-data counter. When the planner variant is shown, overlay query plans with a boolean "used MV?" badge and a cost-delta vs. base-table plan so the MV's value is quantified per query. Keep all timestamps in a single timezone-aware format and render "X minutes ago" relative labels with a tooltip to the absolute timestamp to avoid the classic ambiguity bugs during DST transitions.

Avoid stacking multiple MVs vertically without grouping — if more than 3 MVs exist, use swim-lanes grouped by refresh strategy (on-commit, scheduled, manual) because mixing strategies in one column makes cadence patterns unreadable. Reserve the top-right corner for a global "refresh storm" indicator that lights up when >30% of MVs are refreshing concurrently, since this is the most common performance pathology users need to spot.
