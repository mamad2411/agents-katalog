---

name: copper-patina-gradient-shader
description: Simulate aged copper map surfaces using layered radial gradients and noise-perturbed hue shifts on canvas.
category: frontend
triggers:
  - copper patina gradient shader
tags: [frontend, copper, patina, gradient, shader, canvas]
version: 1.0.0
---

# copper-patina-gradient-shader

Across all three desert-themed apps, the "copper map" aesthetic needed a reusable treatment that reads as metal rather than flat orange. The trick is a three-layer composite: (1) a base radial gradient from `#8b4513` core to `#2a1208` edge, (2) a multiplicative noise layer with hue jittered between `hsl(20..35, 60%, L)` where L is sampled from a low-octave simplex, and (3) a sparse specular pass painting 2-4% of pixels at `rgba(255, 220, 180, 0.3)` to mimic polished highlights.

```js
function paintCopper(ctx, w, h, noise) {
  const g = ctx.createRadialGradient(w/2, h/2, 0, w/2, h/2, Math.hypot(w,h)/2);
  g.addColorStop(0, '#8b4513'); g.addColorStop(1, '#2a1208');
  ctx.fillStyle = g; ctx.fillRect(0,0,w,h);
  const img = ctx.getImageData(0,0,w,h);
  for (let i = 0; i < img.data.length; i += 4) {
    const n = noise((i/4)%w * 0.01, Math.floor((i/4)/w) * 0.01);
    const shift = (n - 0.5) * 30;
    img.data[i]   = clamp(img.data[i]   + shift);
    img.data[i+1] = clamp(img.data[i+1] + shift*0.6);
    img.data[i+2] = clamp(img.data[i+2] + shift*0.2);
  }
  ctx.putImageData(img, 0, 0);
}
```

Reusable for any "aged metal", "weathered parchment", or "oxidized surface" visualization. The key insight: flat fills look digital; radial + noise + sparse specular reads as physical. Pre-bake to an offscreen canvas once — recomputing per frame is wasteful since the texture is static while foreground elements animate on top.
