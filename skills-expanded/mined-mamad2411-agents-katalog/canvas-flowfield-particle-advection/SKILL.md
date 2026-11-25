---

name: canvas-flowfield-particle-advection
description: Render drifting "currents" by advecting particles through a cached noise-based vector field with trail fade.
category: algorithms
triggers:
  - canvas flowfield particle advection
tags: [algorithms, canvas, flowfield, particle, advection, cache]
version: 1.0.0
---

# canvas-flowfield-particle-advection

A bioluminescent-current or kelp-drift visual is really particles sampling a 2D vector field. Precompute the field once (grid of angles from layered sine or value-noise: `angle = noise(x*0.01, y*0.01, t*0.001) * TAU`), then each frame advance each particle by `(cos(angle), sin(angle)) * speed`. Wrap or respawn at edges. Instead of clearing the canvas, paint a semi-transparent rect over it (`fillStyle='rgba(0,10,20,0.08)'`) so particle trails fade into comet-like streaks — zero extra buffers needed.

```js
for (const p of particles) {
  const gx = (p.x / cell) | 0, gy = (p.y / cell) | 0;
  const a = field[gy * cols + gx];
  p.x += Math.cos(a) * p.v; p.y += Math.sin(a) * p.v;
  if (p.x < 0 || p.x > W) p.x = Math.random() * W;
  ctx.fillRect(p.x, p.y, 1.5, 1.5);
}
```

Key tunings: field cell size 8–16 px (coarser = smoother swirls), particle count 2–8k with single-pixel fills (DOM-free, GC-free), alpha-fade factor 0.05–0.12 (lower = longer trails but ghosting). Regenerate the field every few seconds with a time-offset noise seed for evolving weather. This pattern replaces any "animated flow" visual — wind maps, magnetic lines, traffic streams — without SVG, WebGL, or per-frame allocation.
