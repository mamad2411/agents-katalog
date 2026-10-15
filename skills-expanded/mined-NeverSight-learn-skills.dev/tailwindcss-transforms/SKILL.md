---
name: tailwindcss-transforms
description: "Use this skill when transforming elements in Tailwind CSS v4. Covers rotate, scale, skew, translate, transform, transform origin, transform style, perspective, perspective origin, backface visibility, 3D transforms, arbitrary transform values, responsive/state transforms, and `zoom-*` utilities added in v4.3. Triggers on: transform, rotate, scale, skew, translate, origin, perspective, transform-style, backface, 3D, zoom, zoom-75, hover:scale, group-hover:translate."
license: MIT
---

Transform utilities move, rotate, scale, skew, and project elements without changing normal document flow. They are commonly paired with transitions and variants.

## Quick Start

```html
<button class="transition-transform duration-150 hover:-translate-y-0.5 hover:scale-[1.02] active:translate-y-0 active:scale-100">
  Open
</button>
```

**Related skills:** `tailwindcss-transitions-animation`, `tailwindcss-states-variants`, `tailwindcss-effects-filters`, `tailwindcss-layout`.

## Utility Map

| Need | Utilities |
|---|---|
| Translate | `translate-x-*`, `translate-y-*`, `translate-*`, `-translate-y-*` |
| Rotate | `rotate-*`, `-rotate-*`, `rotate-x-*`, `rotate-y-*`, `rotate-z-*` |
| Scale | `scale-*`, `scale-x-*`, `scale-y-*`, `scale-z-*` |
| Skew | `skew-x-*`, `skew-y-*` |
| Origin | `origin-center`, `origin-top`, `origin-bottom-right`, arbitrary origins |
| 3D | `perspective-*`, `perspective-origin-*`, `transform-3d`, `transform-flat`, `backface-hidden` |
| Zoom | `zoom-*`, `zoom-[1.1]`, `zoom-(--preview-zoom)` |

## Core Patterns

### Hover lift

```html
<article class="transition duration-200 hover:-translate-y-1 hover:shadow-lg motion-reduce:hover:translate-y-0">
  <!-- ... -->
</article>
```

### Off-canvas panel

```html
<aside class="translate-x-full transition-transform data-[open=true]:translate-x-0">
  <!-- ... -->
</aside>
```

### 3D scene card

```html
<div class="perspective-distant">
  <div class="transform-3d rotate-x-6 rotate-y-12 backface-hidden">
    <!-- ... -->
  </div>
</div>
```

Verify exact 3D utility support and browser behavior against the docs for production work.

### Zoom utilities

Tailwind CSS v4.3 adds `zoom-*`:

```html
<div class="zoom-75 md:zoom-100"></div>
<div class="zoom-[1.1]"></div>
<div class="zoom-(--preview-zoom)"></div>
```

Use `zoom` for cases where CSS zoom semantics are desired; use transform scale for ordinary visual scaling.

## Common Mistakes

### [HIGH] Expecting transforms to affect document flow

Transforms move pixels visually but do not reserve new layout space. Use margin, padding, or layout utilities when flow must change.

### [MEDIUM] Creating motion without reduced-motion fallback

Pair transform motion with `motion-reduce:` or `motion-safe:` for larger movement.

### [MEDIUM] Using `zoom` as a replacement for responsive design

`zoom` scales rendering. Use responsive layout utilities for adaptive UI.

## API Reference

- Transform: `https://tailwindcss.com/docs/transform`
- Translate: `https://tailwindcss.com/docs/translate`
- Rotate: `https://tailwindcss.com/docs/rotate`
- Scale: `https://tailwindcss.com/docs/scale`
- Perspective: `https://tailwindcss.com/docs/perspective`
- Backface visibility: `https://tailwindcss.com/docs/backface-visibility`
- Zoom: `https://tailwindcss.com/docs/zoom`
