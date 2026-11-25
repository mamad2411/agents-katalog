---

name: distributed-tracing-visualization-pattern
description: Three complementary views (waterfall, service graph, latency heatmap) for reasoning about distributed traces
category: design
triggers:
  - distributed tracing visualization pattern
tags: [design, distributed, tracing, visualization]
version: 1.0.0
---

# distributed-tracing-visualization-pattern

Distributed tracing data is inherently multi-dimensional: each span has a parent-child relationship, a service/operation identity, a duration, a start offset, and a status. No single chart surfaces all of these, so effective tracing UIs compose three orthogonal visualizations. The **waterfall** encodes causality and critical path — spans rendered as horizontal bars indented by depth, positioned by startTime relative to trace root, width proportional to duration. The **service graph** collapses spans into a node-link topology where edges are weighted by call count and colored by error rate, exposing fan-out hotspots invisible in the waterfall. The **heatmap** bins spans by (operation, latency bucket) to reveal bimodal distributions and tail behavior that averages hide.

The shared contract across all three views is a normalized Span shape `{traceId, spanId, parentSpanId, service, operation, startTime, duration, status, tags}`. Build a single derivation layer that computes `depth`, `criticalPath`, `p50/p95/p99` per operation, and `edges[from→to]` once, then feed each view a slice. Cross-view linking is the payoff: hovering a span in the waterfall highlights its node in the graph and its bucket in the heatmap, which only works if every view agrees on `spanId` as the primary key and `service+operation` as the aggregation key.

Color encoding should stay consistent — reserve red for `status=ERROR`, a sequential scale (e.g., viridis) for latency in the heatmap, and categorical colors for service identity in the graph. Reusing hue for both latency and errors is the single most common source of misreading, so pick the axis early and stick to it across all three panels.
