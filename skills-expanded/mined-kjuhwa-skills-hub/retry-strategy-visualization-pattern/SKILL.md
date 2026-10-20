---

name: retry-strategy-visualization-pattern
description: Visualize retry attempts as timeline tracks with backoff intervals, jitter bands, and terminal outcome markers
category: design
triggers:
  - retry strategy visualization pattern
tags: [design, retry, strategy, visualization, visualize]
version: 1.0.0
---

# retry-strategy-visualization-pattern

Render each in-flight request as a horizontal track on a time axis, with attempt markers (circles) placed at t₀, t₀+delay₁, t₀+delay₂, ... where delay_n follows the chosen backoff policy (fixed, linear, exponential, decorrelated jitter). Color-code each attempt by outcome: green for success, amber for retryable failure (429/503/timeout), red for terminal failure (4xx non-retryable), and gray for attempts suppressed by budget or circuit breaker. Overlay the computed backoff interval as a translucent band between markers so viewers can distinguish wait time from actual request latency.

For exponential-backoff strategies, draw the theoretical delay curve (base · 2^n) as a dashed reference line behind the actual attempt markers; jittered delays then visibly scatter around that curve, making the jitter distribution legible at a glance. Add a secondary panel showing aggregate metrics updated per tick: success rate, p50/p99 attempts-to-success, total retries issued, and budget consumption (retries / total_requests). A small legend should map every attempt-state color and annotate the active strategy parameters (base delay, max attempts, jitter mode, budget cap).

Keep the canvas scrolling horizontally in a fixed time window (e.g., last 30 seconds) so long-running simulations don't compress into unreadable density. Sticky the y-axis labels (request IDs) and let users hover any attempt marker to see exact delay, HTTP status, and retry-after header value. This pattern scales from single-request debugging (one track, zoomed-in) to storm analysis (hundreds of tracks, zoomed-out heatmap view).
