---

name: lantern-visualization-pattern
description: Canvas-based lantern rendering with flicker, glow halos, and ember particle systems for atmospheric visualization
category: design
triggers:
  - lantern visualization pattern
tags: [design, lantern, visualization, canvas]
version: 1.0.0
---

# lantern-visualization-pattern

Lantern-themed visualizations share a layered rendering stack: a dark gradient backdrop (deep indigo to black) painted first, then per-lantern glow halos drawn as radial gradients with additive blend mode (`globalCompositeOperation = 'lighter'`), then the lantern body sprite/path, and finally ember particles emitted upward with buoyancy. Each lantern owns three animated scalars — `flickerPhase` (sinusoidal 0.85–1.15 intensity multiplier), `swayAngle` (pendulum using damped spring, ±0.08 rad), and `emberEmitRate` (Poisson-distributed spawn interval 40–120ms). Drive all three from a single `requestAnimationFrame` loop keyed off a shared `elapsed` timestamp so lanterns in a constellation stay phase-coherent but visually independent.

For the constellation/atlas variant, position lanterns on a 2D starfield and connect nearest neighbors with faint catenary curves (quadratic bezier with control point offset downward by `dist * 0.15`) rendered at 20–30% opacity. For the drifting/flight variant, apply a wind vector field (Perlin noise sampled at lantern position, scale 0.002) that perturbs velocity each frame with a drag coefficient around 0.96. For the composer variant, each lantern maps to a musical voice — flicker intensity drives amplitude envelope, sway angle drives stereo pan, and ember emission triggers note-on events — so visual and sonic behavior share state.

Keep the glow halo radius at roughly 4× the lantern body radius and cap total active embers per lantern at 60 to avoid overdraw tanking framerate on mid-tier GPUs. Use `willReadFrequently: false` on the 2D context and pre-bake the lantern body to an offscreen canvas once, then `drawImage` per frame rather than re-stroking paths.
