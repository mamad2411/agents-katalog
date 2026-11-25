---
name: tomtom-traffic-analytics
description: |
  Analyses historical and aggregated traffic using TomTom MOVE Traffic Analytics. Use when the user
  asks about traffic "trends", "patterns", "over the past week/month", "rush hour", "average delay",
  "junction analysis", "route monitoring", "busiest times", or compares traffic between areas/periods.
  This is for historical/statistical analysis, NOT the live picture (use tomtom-live-traffic for now).
  Requires the optional TomTom Traffic Analytics (MOVE) connector to be enabled.
license: Apache-2.0
metadata:
  author: ABS
  version: "1.0"
---

# TomTom Traffic Analytics (MOVE)

## What this skill does

Answers **historical and aggregated** traffic questions — trends over time, rush-hour patterns,
average delays, junction performance, and route-corridor monitoring — using the TomTom MOVE
Traffic Analytics service.

> **Availability:** this skill needs the **optional** TomTom Traffic Analytics connector (a separate
> MOVE-Portal-backed MCP server). If those tools are not available in this session, tell the user the
> analytics connector isn't enabled and offer the live picture via the `tomtom-live-traffic` skill.

## Tools (provided by the optional analytics connector)

- `tomtom-area-analytics-stats` — traffic statistics for a custom geographic area.
- `tomtom-junction-search` → `tomtom-junction-live-data` / `tomtom-junction-archive` — find a
  junction, then read live or historical metrics.
- `tomtom-route-search` → `tomtom-route-monitoring-details` — find a monitored route, then read
  segment-level analysis.
- `tomtom-traffic-flow-segment`, `tomtom-traffic-incidents` — flow/incidents for a point or area.

**All analytics tools require a `sql_queries` parameter** that filters/aggregates the data
server-side (DuckDB) so results fit the conversation. See `references/sql-recipes.md`.

## Workflow

1. **Confirm availability.** If the analytics tools aren't present, stop and explain (offer
   `tomtom-live-traffic`). Otherwise continue.
2. **Find the subject.** Use `tomtom-junction-search` or `tomtom-route-search` (with a `sql_queries`
   filter by name/status) to get the junction/route IDs, or geocode an area with the
   `tomtom-location-search` skill.
3. **Pull the metrics.** Call the matching analytics tool (`*-live-data`, `*-archive`,
   `*-monitoring-details`, or `*-analytics-stats`) with a focused `sql_queries` that selects and
   aggregates only what's needed (top delays, hourly averages, period comparison).
4. **Interpret.** Summarise the finding in plain language (peak times, average vs worst delay, trend
   direction). Quote concrete numbers.
5. **Visualise where useful.** For area/junction context, hand coordinates to the
   `tomtom-live-map` skill to pin the location; analytics tables stand alone for time-series.

## Output format

- A short narrative answer (the headline insight).
- A compact results table from the `sql_queries` projection, e.g.:

  | Hour | Avg delay (s) | Samples |
  |------|---------------|---------|
  | 08:00 | 142 | 1,204 |

- Optional location pin via `tomtom-live-map`.

## Tips & disambiguation

- This is **historical/aggregated** analysis. For "what's happening right now", use
  `tomtom-live-traffic`.
- Always constrain `sql_queries` (e.g. `... ORDER BY delay_sec DESC LIMIT 10`) to avoid huge results.
- Junction/route searches return IDs — keep them to chain into the detail tools.

## Additional resources

- **`references/sql-recipes.md`** — ready-to-adapt `sql_queries` snippets for common questions.
