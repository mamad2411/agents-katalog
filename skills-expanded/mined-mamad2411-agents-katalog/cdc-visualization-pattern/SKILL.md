---

name: cdc-visualization-pattern
description: Visualizing CDC event flow from source database through log capture to downstream consumers with row-level change granularity
category: design
triggers:
  - cdc visualization pattern
tags: [design, cdc, visualization]
version: 1.0.0
---

# cdc-visualization-pattern

CDC (Change Data Capture) visualizations must render three distinct layers simultaneously: the source database with its transaction log (WAL/binlog/redo), the CDC connector/capture process reading log positions (LSN/GTID/SCN), and downstream sinks (Kafka topics, search indexes, data lakes). Use horizontal swim lanes where each lane represents a stage, and animate discrete change events (INSERT/UPDATE/DELETE) as colored tokens flowing left-to-right. Color code by operation type: green for INSERT, amber for UPDATE, red for DELETE, and purple for schema changes (DDL). Always surface the log position cursor prominently — it is the single most important state in any CDC system.

For cdc-stream-monitor style real-time dashboards, show lag as the visual gap between the "current log tail" marker and the "last consumed position" marker per consumer. For cdc-replay-theater style time-travel UIs, render a scrubber timeline keyed to LSN/timestamp with event density histograms so users can see hot windows before seeking. For cdc-topology-weaver style graph views, draw source tables as nodes with edges representing subscription routes to sinks; overlay edges with throughput sparklines and a "last heartbeat" age badge so dead routes are instantly visible.

Always expose the before/after row image side-by-side for UPDATE events — a CDC tool that only shows the "after" state is half-blind. For DELETEs, preserve the tombstone marker visually (struck-through row with retention-until timestamp) rather than removing it from view, because downstream replay windows depend on tombstone visibility.
