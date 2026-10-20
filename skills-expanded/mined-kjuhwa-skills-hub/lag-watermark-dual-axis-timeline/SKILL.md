---

name: lag-watermark-dual-axis-timeline
description: Overlay consumer lag and watermark progression on a shared time axis with dual-scale Y to keep both readable during bursts.
category: frontend
triggers:
  - lag watermark dual axis timeline
tags: [frontend, lag, watermark, dual, axis, timeline]
version: 1.0.0
---

# lag-watermark-dual-axis-timeline

When visualizing message-queue consumer health, lag (messages behind) and watermark/offset position live on wildly different scales — lag spikes to millions while watermark advances linearly. Plotting both on one linear Y-axis hides the lag dynamics or flattens the watermark to a constant line. The reusable pattern is a dual-axis SVG/Canvas timeline where the left axis is log-scaled lag (with a `symlog` transform so zero and near-zero stay visible) and the right axis is a linear watermark offset counter, both sharing the X time axis and a synchronized cursor.

Implementation sketch: maintain two scale functions `yLag = symlog(domain=[0, maxLag], range=[h, 0])` and `yOffset = linear(domain=[minOff, maxOff], range=[h, 0])`, render lag as a filled area (alpha 0.3) and watermark as a crisp line on top, and emit a single `<g>` cursor group bound to pointer X that reads both series via bisector. Color lag warm (amber→red above SLA threshold) and watermark cool (cyan) so the eye instantly separates "health" from "progress." Add a secondary band at the bottom showing rebalance events as vertical ticks — these are the causal anchors explaining lag discontinuities.

This generalizes to any "backlog + progress" pairing: queue depth + throughput, replication lag + LSN, retry queue size + success rate. The key insight is that symlog on the backlog axis prevents the "always zero or always huge" failure mode, and overlaying event ticks on a third mini-band turns a chart into an incident timeline without adding a second chart.
