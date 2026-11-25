---
name: d3-motion
description: Data-viz animations with D3 + GSAP — animated SVG, trig-based distortion (sin/cos/tan), morphing paths.
---

# d3-motion

## Purpose
Combine D3's data-binding and scale machinery with GSAP's animation engine to produce expressive, performant data visualizations — animated charts, morphing SVG paths, and trig-based organic motion.

## Capabilities
- D3 enter/update/exit joins animated via GSAP tweens
- SVG path morphing (via `MorphSVGPlugin` when available, or interpolated `d` attr)
- Trig-based distortion — wave, ripple, lissajous using `Math.sin`, `Math.cos`, `Math.tan`
- Animated scales (`d3.scaleLinear`, `scaleTime`) driving GSAP timelines
- Force-directed layouts with animated transitions
- Canvas + SVG hybrid rendering for large datasets

## Instructions
1. Install: `npm i d3 gsap`. Import selectively (`import { select, scaleLinear } from "d3"`) to keep bundle small.
2. Use D3 for data joins and scales; use GSAP for *motion timing* instead of `d3.transition()` when you need timeline control.
3. For trig motion, drive a parameter `t` from 0→1 via GSAP, then compute positions: `y = amp * Math.sin(freq * x + t * Math.PI * 2)`.
4. Animate SVG attributes with GSAP using attribute plugin form: `gsap.to(circle, { attr: { r: 20, cx: 100 } })`.
5. For thousands of nodes, render to `<canvas>` and tween a shared `state` object, redrawing on `onUpdate`.
6. Respect `prefers-reduced-motion` — skip non-essential motion.

## Usage Examples

**Animated bar chart (enter):**
```js
const x = d3.scaleBand().domain(data.map(d => d.label)).range([0, width]).padding(0.1);
const y = d3.scaleLinear().domain([0, d3.max(data, d => d.value)]).range([height, 0]);

const bars = svg.selectAll("rect").data(data).join("rect")
  .attr("x", d => x(d.label)).attr("width", x.bandwidth())
  .attr("y", height).attr("height", 0);

gsap.to(bars.nodes(), {
  attr: { y: (i) => y(data[i].value), height: (i) => height - y(data[i].value) },
  duration: 0.8, stagger: 0.05, ease: "power3.out"
});
```

**Sine-wave distortion on a path:**
```js
const state = { t: 0 };
const path = d3.select("path.wave");
const points = d3.range(0, 400, 4);

gsap.to(state, {
  t: Math.PI * 2, duration: 4, repeat: -1, ease: "none",
  onUpdate: () => {
    const d = "M" + points.map(x => {
      const y = 50 + 20 * Math.sin(0.04 * x + state.t);
      return `${x},${y}`;
    }).join("L");
    path.attr("d", d);
  }
});
```

**Tan-based exaggerated easing (use sparingly — blows up near π/2):**
```js
// clamp input domain to avoid asymptote
const distort = t => Math.tan(Math.min(t, 0.49) * Math.PI) * 0.3;
```
