---

name: backpressure-visualization-pattern
description: Visualize producer/consumer rate mismatch with buffer fill gauges, drop counters, and upstream signal arrows
category: design
triggers:
  - backpressure visualization pattern
tags: [design, backpressure, visualization, visualize]
version: 1.0.0
---

# backpressure-visualization-pattern

Backpressure demos need three synchronized visual layers to be legible. The first is a **flow lane** showing items as discrete tokens traveling producer → buffer → consumer, with token color encoding lifecycle state (in-flight, queued, processing, dropped, NACK'd). The second is a **buffer gauge** rendered as a stacked bar or ring with explicit watermarks — low (resume), high (pause), and hard cap (drop/block) — because backpressure is fundamentally about threshold crossings, not absolute fill. The third is a **signal lane** showing the upstream control channel (PAUSE, RESUME, WINDOW_UPDATE, credit grants) as arrows flowing opposite to the data direction; without this reverse-arrow visualization, users cannot distinguish backpressure from simple throttling.

Overlay a live rate chart with two lines (producer offered rate vs. consumer drain rate) and shade the delta region — the shaded area *is* the backpressure signal. Color convention across pipeline-pressure-lab, reactive-stream-juggler, and tcp-window-sim: green (flowing), amber (paused/blocked upstream), red (dropped/overflow), blue (credit/window token). Always label the **strategy** currently active (drop-oldest, drop-newest, block, buffer-unbounded, NACK) in the gauge header because the same fill level means different things under different strategies.

Interactivity must let the user drag producer rate, consumer rate, and buffer size independently while the sim runs — static sliders that require restart hide the most important lesson, which is the *transient* behavior when parameters change mid-flight. Expose a "burst" button that injects N items instantly to show overflow edges.
