---

name: chaos-engineering-visualization-pattern
description: Visualizing blast radius, failure propagation, and steady-state deviation in chaos experiments
category: design
triggers:
  - chaos engineering visualization pattern
tags: [design, chaos, engineering, visualization]
version: 1.0.0
---

# chaos-engineering-visualization-pattern

Chaos engineering UIs need three coordinated visual layers: a topology graph of services/nodes with health-tinted edges, a blast-radius overlay (concentric rings or shaded regions radiating from the injection point), and a steady-state metrics panel showing deviation bands above/below the baseline envelope. Use color not as status-only but as a gradient encoding severity of deviation (σ from baseline), so a partially-degraded node is visually distinct from a fully-failed one. The injection point itself should be a persistent, unambiguous marker (e.g., a pulsing core) separate from the downstream impact shading, because operators need to know "where did we break it" vs "where did it hurt."

For scenario runners (gameday-style) add a timeline scrubber that lets users replay the experiment tick-by-tick, with the topology re-rendering at each tick and a vertical marker on the metrics chart locked to the scrubber position. Dice/entropy-style apps should visualize the probability distribution of the next fault as a weighted histogram alongside the roll outcome — users trust randomness they can see. Always keep the "abort / halt" control pinned and visually loud (red, fixed position), because the whole UX premise is that the operator can stop the experiment at any moment.

Avoid dashboards that only show end-state. Chaos visualizations are fundamentally *temporal* — the story is the propagation, not the final failure count. Render transitions with easing (200–400ms) so cascading failures read as a wave, not a snap, which matches operator mental models of real outage propagation.
