---
name: follow-lib-animejs
description: Use Anime.js v4 for DOM/CSS animations, timelines, staggers, and utilities in web apps
argument-hint: "[scope]"
related:
  - follow-lib-css
  - follow-lib-react

---

## Goal

Use Anime.js v4 (latest v4.5.0) in projects with the ESM-first API to build fast, efficient, and maintainable animations

## Scope

Used for:
- DOM/CSS animations with `animate()`
- Sequence control with `createTimeline()`
- Staggered animations with `stagger()`
- Utilities (`utils.set`, `utils.get`, `lerp`, `damp`, `engine`)
- Scroll (`onScroll`), drag (`createDraggable`), scope (`createScope`), SVG, text, WAAPI integrations
- Working with React, Vue, Svelte, and plain JS

Boundaries:
- Use this skill for JS-driven animation (timelines, staggers, scroll/drag triggers, SVG morph)
- For plain CSS transitions/animations or styling → use `/follow-lib-css` instead

- Latest: `animejs@4.5.0` (verified 2026-09-13)
- v5 beta: `animejs@beta` (`5.0.0-beta.2`) has breaking changes — fixed transform render order (`perspective`>`translate`>`rotate`>`scale`>`skew`), the 3rd callback arg of function-based values changes from `total` (Number) to `targets` (Array), the stagger `use` signature changes accordingly, `matrix`/`matrix3d` cannot be animated directly
- References: [apis](references/apis.md) 
## Execute

### 1. Install And Setup

> Goal: install `animejs` and pick the import style that fits the bundle

1. `bun add animejs` (runtime dependency)
2. Imports for v4:

```javascript
import { animate, createTimeline, stagger } from 'animejs';

// or subpath imports for tree-shaking
import { animate } from 'animejs/animation';
import { createTimeline } from 'animejs/timeline';
import { createScope } from 'animejs/scope';
import { createDraggable } from 'animejs/draggable';
import { onScroll } from 'animejs/events';
import { createSpring } from 'animejs/spring';
```

3. Check the version: `bun pm ls animejs` or look at `package.json`

### 2. Learn Core API

> Goal: understand `animate()`, `createTimeline()`, and the basic `utils`

```javascript
// create an animation
animate('.box', {
  x: 250,
  rotate: { from: -180 },
  duration: 1200,
  delay: stagger(80, { from: 'center' }),
  ease: 'inOutQuint',
});

// timeline
const tl = createTimeline({
  defaults: { duration: 800, ease: 'outQuad' },
});
tl.add('.a', { x: 100 })
  .add('.b', { y: -50 }, '-=400');

// utilities
import { utils } from 'animejs';
utils.set('.box', { opacity: 0.5 });
```

### 3. Key Concepts

> Goal: know targets, tween parameters, callbacks, and stagger options

- `targets`: CSS selector, DOM elements, JS objects, array
- Animatable properties: CSS, transforms, CSS variables, SVG attributes, HTML attributes, JS object properties
- Tween parameters: `from`, `to`, `delay`, `duration`, `ease`, `composition` (`replace` | `blend` | `none`), `modifier`
- Playback: `loop`, `alternate`, `reversed`, `autoplay`, `frameRate`, `playbackRate`, `playbackEase`
- Keyframes: tween-value, tween-parameter, duration-based, percentage-based
- Callbacks: `onBegin`, `onBeforeUpdate`, `onUpdate`, `onRender`, `onLoop`, `onComplete`, `onPause`, `then()`
- Timeline: `add()`, `set()`, `call()`, `sync()`, `label()`, `remove()`, `seek()`, `stretch()`
- `stagger` options: `from`, `grid`, `axis`, `reversed`, `ease`, `jitter`, `seed`

### 4. Apply Patterns And Best Practices

> Goal: write animations that are performant, accessible, and cleaned up correctly

- Prefer `transform` (translate/scale/rotate) and `opacity`
- Avoid animating layout-triggering properties (width, height, top, left)
- Set `will-change` on elements about to animate, then remove it after finishing
- Use `stagger()` for group animations
- Set `composition: 'blend'` when combining animations
- Use `revert()` or `cancel()` for cleanup
- Honor `prefers-reduced-motion` to disable or reduce animation
- Use subpath imports (`animejs/easings`, `animejs/svg`, `animejs/text`) when only specific modules are needed
- v4.2+ deprecations: use `splitText()` instead of `text.split()`, `spring()` instead of `createSpring()`, `lerp()`/`damp()` instead of `interpolate()` (removed); easings `linear()`/`irregular()`/`steps()`/`cubicBezier()` must be imported separately from core

### 5. Integrate With Frameworks

> Goal: use `createScope()` for lifecycle/cleanup in React, Vue, Svelte

React: use `createScope()` (official pattern) — the scope cleans up every animation inside it

```jsx
import { useEffect, useRef } from 'react';
import { animate, createScope } from 'animejs';

function Box() {
  const root = useRef(null);
  useEffect(() => {
    const scope = createScope({ root }).add(() => {
      animate('.box', { x: 100 });
    });
    return () => scope.revert();
  }, []);
  return <div ref={root}><div className="box" /></div>;
}
```

Vue/Svelte: call `animate()` or `createScope()` in a lifecycle hook and clean up with `revert()` in `onUnmounted`/`onDestroy`

### 6. Reference And Troubleshoot

> Goal: use official docs, changelog, and the migration guide when stuck

- official docs: https://animejs.com/documentation
- releases/changelog: https://github.com/juliangarnier/anime/releases
- v3 to v4 migration: https://github.com/juliangarnier/anime/wiki/Migrating-from-v3-to-v4

## Rules

- Use `bun add animejs` for installation
- Import ESM: `import { animate, createTimeline, stagger } from 'animejs'`
- Do not use the v3 global `anime()`
- Use `ease` instead of `easing`
- Use `createTimeline()` instead of `anime.timeline()`
- Use `stagger()` instead of the old v3 stagger syntax
- Use `transform` and `opacity` where possible
- Use `will-change` carefully
- Honor `prefers-reduced-motion`
- Clean up animations with `revert()` or `cancel()`
- Use animations to enhance UX, not as a distraction
- Use /follow-lib-css if needed
- Use /follow-lib-react if integrating with React

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- Fast, efficient animations
- Maintainable, consistent code
- Good, accessible UX
- Optimized performance
