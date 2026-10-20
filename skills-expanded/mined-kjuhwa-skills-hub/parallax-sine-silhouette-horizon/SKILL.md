---

name: parallax-sine-silhouette-horizon
description: Multi-layer animated horizon backdrop built from 3-N sine-displaced silhouette polygons with decreasing opacity and rising baselines for cheap parallax depth.
category: design
triggers:
  - parallax sine silhouette horizon
tags: [design, parallax, sine, silhouette, horizon]
version: 1.0.0
---

# parallax-sine-silhouette-horizon

Build an atmospheric background (dusk fields, mountain ranges, ocean waves, city skylines) on a single 2D canvas by drawing N layered closed polygons, each a horizon line perturbed by a sine sum. Each layer is parameterized only by its index: baseline rises with layer, color alpha drops with layer, amplitude grows with layer, and phase offset separates them. A `time` term in the sine argument creates gentle animation without any per-frame allocation. The effect reads as "depth + motion" for under 30 lines.

```js
for(let layer=0; layer<LAYERS; layer++){
  ctx.fillStyle = `rgba(${R-layer*dR}, ${G-layer*dG}, ${B-layer*dB}, ${A0 - layer*dA})`;
  ctx.beginPath();
  ctx.moveTo(0, H);
  for(let x=0; x<=W; x+=STEP){
    const y = H - (BASE + layer*LIFT)
            - Math.sin(x*FREQ + layer*PHASE + time*DRIFT) * (AMP + layer*dAMP);
    ctx.lineTo(x, y);
  }
  ctx.lineTo(W, H); ctx.closePath(); ctx.fill();
}
```

Tuning knobs: increase `STEP` (4→16px) to trade smoothness for speed on low-power displays; use multiple incommensurate sines per layer (`sin(x*f1) + sin(x*f2)`) when the single-frequency ripple looks too regular; pair with a vertical gradient sky (top→bottom color interpolation driven by a "dusk" slider) to make the whole background reactive. The baseline-rise-per-layer is load-bearing — without it the silhouettes stack on top of each other and the depth illusion collapses.
