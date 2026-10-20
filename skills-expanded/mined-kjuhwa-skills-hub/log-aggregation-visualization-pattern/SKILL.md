---

name: log-aggregation-visualization-pattern
description: Visual patterns for rendering streaming logs, heatmap density, and query-filtered timelines in log aggregation UIs
category: design
triggers:
  - log aggregation visualization pattern
tags: [design, log, aggregation, visualization, streaming]
version: 1.0.0
---

# log-aggregation-visualization-pattern

Log aggregation visualizations share three archetypes that map directly to operator mental models. A **stream river** renders a continuously scrolling vertical or horizontal lane per source (host/service/pod), with each log line as a colored tick whose hue encodes severity (trace/debug/info/warn/error/fatal) and whose width encodes burst intensity. Tail-follow mode auto-scrolls but pauses on hover to prevent the "rubber band" problem where operators can never click a line. A **density heatmap** buckets logs into a 2D grid of `time_bucket × source` (or `time_bucket × log_level`) with cell opacity proportional to `log(count+1)` — plain linear scaling collapses because error spikes are 100-1000× baseline. A **query console timeline** overlays a histogram strip above the result table so filter changes visibly reshape the time distribution, giving operators feedback that their regex/lucene query is actually narrowing the set.

Severity color must be consistent across all three views and must survive colorblind rendering — use the convention `trace=gray, debug=blue, info=green, warn=amber, error=red, fatal=magenta/purple` rather than red-green-only scales. Time axis should support both wallclock and relative ("5m ago") modes, and brushing a range in the heatmap should filter both the stream river and the query results — this cross-filtering is the entire reason to co-locate the three panels. Always show a "gap indicator" (dashed cell, striped lane) when a source stops emitting, because in log aggregation the *absence* of logs is itself a signal (crashed agent, network partition, log rotation bug).
