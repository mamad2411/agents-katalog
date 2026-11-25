---
name: animejs-animate
description: "Comprehensive guide to using Anime.js v4 for JavaScript-driven web animations — timelines, SVG animations, scroll effects, draggable interactions, and stagger patterns."
metadata:
  openclaw:
    emoji: "🎌"
    source: "https://github.com/BowTiedSwan/animejs-skills"
---

# Anime.js v4 — Web Animation Skill

## When to use
- Lightweight JavaScript animations (smaller than GSAP)
- SVG path animations and morphing
- Timeline-based sequences
- Stagger effects on multiple elements
- Draggable interactions

## Key APIs

### Basic animation
```js
import anime from "animejs";

anime({
  targets: ".element",
  translateX: 250,
  opacity: [0, 1],
  duration: 800,
  easing: "easeOutExpo",
});
```

### Timeline
```js
const tl = anime.timeline({
  easing: "easeOutExpo",
  duration: 750,
});

tl.add({ targets: ".header", translateY: [-30, 0], opacity: [0, 1] })
  .add({ targets: ".content", translateY: [20, 0], opacity: [0, 1] }, "-=400")
  .add({ targets: ".cta", scale: [0.9, 1], opacity: [0, 1] }, "-=300");
```

### Stagger
```js
anime({
  targets: ".grid-item",
  scale: [0.5, 1],
  opacity: [0, 1],
  delay: anime.stagger(100, { grid: [4, 4], from: "center" }),
});
```

### SVG path animation
```js
anime({
  targets: "path",
  strokeDashoffset: [anime.setDashoffset, 0],
  duration: 2000,
  easing: "easeInOutSine",
});
```

## v4 changes from v3
- ES module support by default
- New `createTimeline()` API
- `createDraggable()` for drag interactions
- Scroll-linked animations with `createScope()`
- Improved TypeScript support

## Performance tips
- Animate `transform` and `opacity` only for 60fps
- Use `will-change: transform` on animated elements
- Batch DOM reads before animation starts
- Remove completed animations to free memory

## Common pitfalls
- Animating layout properties (width/height) → use transform instead
- Not cleaning up in SPAs → store and pause/remove references
- SVG animations not working → check `stroke-dasharray` is set

## Tips for AI Agents
- Ask if Anime.js is already installed or needs adding.
- Confirm animation style (entrance, scroll, interaction, SVG).
- Consider `prefers-reduced-motion` for accessibility.
