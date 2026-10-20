---

name: read-replica-visualization-pattern
description: Canvas-based topology visualization for primary-replica clusters with lag indicators and routing flows
category: design
triggers:
  - read replica visualization pattern
tags: [design, read, replica, visualization, canvas]
version: 1.0.0
---

# read-replica-visualization-pattern

Read-replica systems need a visualization that makes three things legible at a glance: the primary node, the set of replicas, and the replication lag between them. The recommended pattern places the primary at the center (or left) with replicas radiating outward, connected by directed edges whose thickness or color encodes current lag (green <100ms, amber 100-1000ms, red >1s). Each replica node should display its role (sync/async), lag in milliseconds, and current query load as a small inline badge, so operators can correlate routing decisions with replica health without hovering.

Query routing should be animated as discrete particles traveling along edges: writes always flow to the primary (solid line, distinct color like blue), reads flow to the selected replica (dashed or lighter line, green). When a read hits a stale replica, flash the particle red at the destination to make consistency violations visible. For the lag-monitor variant, add a stacked time-series panel below the topology showing lag-per-replica over the last 60 seconds, with threshold lines for the app's consistency SLO. For the router-playground variant, overlay the current routing strategy (round-robin, least-lag, weighted, primary-fallback) as a label on the primary, and let users swap strategies to see the particle distribution shift in real time.

Keep the rendering stack lightweight: SVG for the topology (easy to label, animate via CSS/requestAnimationFrame), Canvas only if replica count exceeds ~50 nodes. Expose a speed-control slider (0.25x–4x) because replication phenomena at real-world timescales are either too slow to observe or too fast to trace — users need to scrub through scenarios. Always pause on hover over a node to freeze the lag readout; otherwise ticking numbers are unreadable.
