---

name: circuit-breaker-visualization-pattern
description: Three-state circuit breaker visualization using color-coded state machine with real-time metrics dashboard
category: design
triggers:
  - circuit breaker visualization pattern
tags: [design, circuit, breaker, visualization, metrics, dashboard]
version: 1.0.0
---

# circuit-breaker-visualization-pattern

Circuit breaker UIs should render the three canonical states (CLOSED/OPEN/HALF_OPEN) as visually distinct zones with semantic colors: green for CLOSED (healthy passthrough), red for OPEN (tripped, rejecting), and amber/yellow for HALF_OPEN (probing recovery). Each state transition should animate along a directed graph showing the trip threshold (failure count ≥ N), the cooldown timer (OPEN → HALF_OPEN after T seconds), and the success probe path (HALF_OPEN → CLOSED after K consecutive successes, or back to OPEN on any failure). Place the current state badge prominently with a pulsing indicator when in HALF_OPEN to emphasize the fragile probing window.

The dashboard layout should split into three synchronized panels: (1) a live request stream showing individual call outcomes as green/red dots with fallback indicators, (2) a rolling failure-rate chart with the trip threshold line overlaid, and (3) a state-timeline Gantt-style bar showing how long the breaker spent in each state over the observation window. This triple view lets operators correlate cause (failure spikes), effect (state transitions), and impact (rejected traffic) at a glance.

For interactive simulators, expose sliders for failure threshold, cooldown duration, half-open probe count, and injected failure rate. Every parameter change should reset or smoothly update the visualization without losing the historical trace, so users can A/B tune thresholds against a reproducible load pattern.
