---

name: connection-pool-visualization-pattern
description: Visual conventions for rendering connection pool state, connection lifecycles, and waiter queues in real-time dashboards
category: design
triggers:
  - connection pool visualization pattern
tags: [design, connection, pool, visualization, dashboard]
version: 1.0.0
---

# connection-pool-visualization-pattern

Connection pool visualizations should render the pool as a fixed-width slot grid where each slot represents one physical connection, color-coded by lifecycle state: idle (muted green/grey), active/checked-out (saturated blue), validating (yellow pulse), stale/evicted (orange fading), and broken (red). Overlay each slot with a thin progress bar showing either time-since-checkout (for active) or time-until-idle-timeout (for idle), so users can instantly spot long-running queries and connections about to be reaped. Place a separate "waiter queue" column to the right, stacking pending acquisition requests with their wait-time counters; this makes pool exhaustion visceral rather than an abstract metric.

Pair the slot grid with a stacked time-series chart (last 60s sliding window) of four key series: active count, idle count, waiters count, and acquisition latency p95. Use the same color language across the grid and the chart so correlation is obvious - a red spike in waiters should visually tie to a fully-blue grid. For config-tuning scenarios, render min/max/overflow thresholds as horizontal reference lines on the active-count series, and shade the "overflow zone" (between max and hard-cap) in a warning tint so users see when they are burning through the burst budget.

Always include a "connection age histogram" as a secondary panel - buckets of 0-30s, 30s-5min, 5min-30min, 30min+ - since connection reuse distribution is the single most diagnostic view for pool health that raw counts cannot convey. Avoid pie charts for state breakdown; they hide the capacity context that the slot-grid provides naturally.
