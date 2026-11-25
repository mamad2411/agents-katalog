---

name: canvas-svg-dual-layer-hit-dispatch
description: Composite scene from an animated `<canvas>` plus an overlaid `<svg>`, routing pointer events to the layer that owns each element class.
category: frontend
triggers:
  - canvas svg dual layer hit dispatch
tags: [frontend, canvas, svg, dual, layer, hit]
version: 1.0.0
---

# canvas-svg-dual-layer-hit-dispatch

Used in `17-inkwell-whale-atlas/app.js`/`index.html`: `<canvas id="sea">` renders continuously-animated paper bands, whales, and lantern halos via `requestAnimationFrame`, while `<svg id="stars">` holds the small population of pickable stars with `pointer-events:none` on the SVG except target elements. Canvas click handler (`cv.addEventListener("click",...)`) normalizes coords via `getBoundingClientRect()` scaling (`(clientX-r.left)*(W/r.width)`) and runs manual hit-tests (`Math.abs(dx)<w.len*.5 && ...` for whales, squared-distance for lanterns). SVG click handler uses `e.target.getAttribute("data-id")` — cheap DOM-native picking for the tiny star set.

The trick is the split: canvas gives you dozens of animated primitives at 60fps, SVG gives you free hit-testing + accessibility for the handful of clickable items. Stars get `<line>` constellation edges drawn into SVG too, so they layer visually under lanterns because SVG sits under canvas in the DOM but above visually via `pointer-events:none` + explicit `data-id`. Both dispatch into a single `show(title, body)` panel, keeping inspect UX identical regardless of which layer the element lives on.

Apply when you have a scene with a many-cheap-animated-things layer and a few-interactive-things layer — pushing all picking into canvas forces manual AABB/circle tests for every click, and pushing everything into SVG tanks framerate past ~100 nodes. Split by cardinality and interactivity, not by visual role.
