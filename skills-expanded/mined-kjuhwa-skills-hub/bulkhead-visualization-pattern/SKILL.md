---

name: bulkhead-visualization-pattern
description: Visual layout conventions for rendering isolated resource pools side-by-side with saturation indicators
category: design
triggers:
  - bulkhead visualization pattern
tags: [design, bulkhead, visualization]
version: 1.0.0
---

# bulkhead-visualization-pattern

Bulkhead visualizations should present each partition as a distinct, bordered container arranged horizontally or in a grid, never merged into a single aggregate view. The core visual metaphor borrows from ship compartments: each pool gets its own "chamber" with a clear capacity ceiling (e.g., 10 slots rendered as 10 cells or a filled bar), and in-flight requests fill the chamber from the bottom up. Color-code by saturation thresholds — green (0-60%), amber (60-90%), red (90-100%) — so viewers instantly spot which partition is drowning without reading numbers.

Cross-partition comparison requires a shared y-axis scale across all bulkhead panels; otherwise a small pool at 9/10 looks identical to a large pool at 90/100 and the isolation benefit is invisible. Always render a "rejected/queued" overflow indicator outside the chamber boundary (e.g., stacked red dots spilling off the side) to show that back-pressure is kicking in on one partition while others remain healthy — this is the whole point of the pattern and must be the most prominent signal.

Include a timeline or sparkline strip beneath each chamber showing recent saturation history (last 30-60s). This makes it obvious when one bulkhead has been pegged while neighbors idle, which is the key insight the pattern teaches. Avoid aggregating metrics across bulkheads in headline numbers — show per-partition latency p50/p99 separately, because averaging defeats the isolation narrative.
