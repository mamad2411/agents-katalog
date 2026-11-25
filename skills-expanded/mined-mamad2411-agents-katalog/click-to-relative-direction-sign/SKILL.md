---

name: click-to-relative-direction-sign
description: Derive a normalized movement vector from any clicked grid cell via `Math.sign(target-current)` on each axis — one click handler covers all 8 directions.
category: algorithms
triggers:
  - click to relative direction sign
tags: [algorithms, click, relative, direction, sign]
version: 1.0.0
---

# click-to-relative-direction-sign

From `18-velvet-cartographers-voyage/app.js` board click handler: `const dq=Math.sign(q-state.ship.q), dy=Math.sign(y-state.ship.y); if(dq===0&&dy===0) apply({type:"chart"}); else apply({type:"drift",dq,dy});`. A single handler on the `<svg>` board serves as both a "click own tile to chart" action and a "click any other tile to drift toward it" action, collapsing what would otherwise be 8 directional buttons + a chart button.

The idiom works because `Math.sign` clamps any delta to `{-1, 0, 1}`, which happens to be exactly the move-one-step-toward-target rule. Clicking a far-away hex doesn't teleport — the movement system still only advances one step, but the user gets an intuitive "nudge toward this" gesture. The same shape (`Math.sign(dx)`, `Math.sign(dy)`) works for square grids, hex grids, or any tile system with ≤ 8 neighbors, because every signed-axis combination maps to a valid neighbor.

Pair with an early-exit for self-click to bind a second action (inspect, interact, wait-in-place). Compared to per-direction buttons, this eliminates UI clutter and lets keyboard bindings stay orthogonal to click — both call the same `apply({type:"drift",dq,dy})` with different dq/dy sources.
