---

name: health-check-visualization-pattern
description: Dashboard layout pattern for rendering heterogeneous health-check signals into a single at-a-glance status surface
category: design
triggers:
  - health check visualization pattern
tags: [design, health, check, visualization, dashboard]
version: 1.0.0
---

# health-check-visualization-pattern

Health-check UIs (service-pulse-monitor, vital-signs-checkup, network-health-radar) converge on a three-zone layout: a top aggregate banner showing overall system verdict (healthy / degraded / down) driven by the worst-state child, a middle grid of per-probe cards (HTTP endpoint, TCP port, DNS, TLS expiry, disk, memory), and a bottom timeline strip showing the last N probe results as a sparkline of colored ticks. Each card exposes four fixed fields regardless of probe type: name, last-checked timestamp, latency, and status pill — this uniformity is what lets a radar-style grid, a medical-chart-style checkup view, and a pulse/heartbeat view all share the same underlying component.

Color semantics must be decoupled from the probe type. Use a single status enum (`up`, `degraded`, `down`, `unknown`) with a central color map, and let each probe translate its raw output (HTTP 2xx, ping RTT threshold, cert days-remaining) into that enum at the edge. This keeps the visualization layer probe-agnostic and makes adding a new probe (e.g. Kafka broker reachability) a matter of writing a translator, not touching the renderer. Reserve `unknown` (gray) for "probe hasn't run yet" — conflating it with `down` (red) causes false-alarm fatigue on cold start.

For the timeline strip, render fixed-width ticks rather than time-proportional bars: a missed probe is visually identical in width to a successful one, which makes gaps in collection obvious and prevents a single slow probe from visually dominating the history. Always anchor the rightmost tick as "now" and scroll left as new samples arrive.
