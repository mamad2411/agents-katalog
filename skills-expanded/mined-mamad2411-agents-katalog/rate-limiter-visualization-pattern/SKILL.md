---

name: rate-limiter-visualization-pattern
description: Visual patterns for rendering token buckets, sliding windows, and quota consumption in real-time dashboards
category: design
triggers:
  - rate limiter visualization pattern
tags: [design, rate, limiter, visualization, dashboard]
version: 1.0.0
---

# rate-limiter-visualization-pattern

Rate limiter visualizations share three core visual primitives: a **capacity meter** (bucket fill level, window occupancy, quota remaining), a **request timeline** (accepted vs. rejected events plotted against time), and a **refill/decay indicator** (token drip animation, window slide, quota reset countdown). For token-bucket-visualizer, render the bucket as a vertical gauge with animated token drops at the refill rate; color-code requests green (accepted, token consumed) or red (rejected, bucket empty). For sliding-window-lab, overlay two translucent time windows (previous + current) with a weighted interpolation bar showing the effective count — this makes the "smoothing" behavior of sliding-window-log vs. sliding-window-counter visually distinct.

Use a shared x-axis time scale across all three panels so operators can correlate cause (burst traffic) and effect (rejection spike). Reserve the top-right for a **live KPI strip**: current rate (req/s), rejection ratio (%), and time-to-reset. For api-quota-dashboard, add a horizontal stacked bar per API key/tenant showing daily/hourly/burst quota tiers — hitting any tier triggers a border-flash animation rather than a modal, so the view stays scannable during incidents.

Critical: always render **both limits and current usage on the same axis**. A gauge showing "847" means nothing without "/ 1000" visible. Use log scale only when burst capacity exceeds sustained rate by >10x (common for token buckets), otherwise linear scale preserves intuition about proximity to the limit.
