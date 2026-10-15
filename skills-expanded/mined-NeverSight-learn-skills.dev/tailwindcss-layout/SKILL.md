---
name: tailwindcss-layout
description: "Use this skill when controlling general layout in Tailwind CSS v4. Covers aspect ratio, columns, break-before/after/inside, box decoration and box sizing, display, float/clear, isolation, object-fit/object-position, overflow and overscroll behavior, position, inset/top/right/bottom/left including logical inset utilities, visibility, and z-index. Triggers on: layout, display, hidden, block, inline, flex display, grid display, position, absolute, fixed, sticky, inset, z-index, overflow, object-fit, aspect-ratio, columns, float, clear, isolation, visibility."
license: MIT
---

Layout utilities control element participation in document flow, positioning, overflow, object behavior, and stacking. Use this skill before reaching for custom CSS for common CSS layout properties.

## Quick Start

```html
<section class="relative isolate overflow-hidden rounded-xl">
  <img class="absolute inset-0 -z-10 size-full object-cover" src="/hero.jpg" alt="" />
  <div class="mx-auto max-w-3xl px-6 py-24">
    <h1 class="text-4xl font-bold text-white">Launch faster</h1>
  </div>
</section>
```

**Related skills:** `tailwindcss-flex-grid`, `tailwindcss-spacing-sizing`, `tailwindcss-responsive-design`, `tailwindcss-backgrounds-borders`.

## Utility Map

| Need | Utilities |
|---|---|
| Display | `block`, `inline`, `inline-block`, `flex`, `inline-flex`, `grid`, `inline-grid`, `contents`, `hidden`, `flow-root` |
| Positioning | `static`, `relative`, `absolute`, `fixed`, `sticky` |
| Insets | `inset-*`, `top-*`, `right-*`, `bottom-*`, `left-*`, logical `inset-s-*`, `inset-e-*` |
| Overflow | `overflow-*`, `overflow-x-*`, `overflow-y-*` |
| Overscroll | `overscroll-*`, `overscroll-x-*`, `overscroll-y-*` |
| Object media | `object-cover`, `object-contain`, `object-center`, `object-top`, `object-[...]` |
| Aspect ratio | `aspect-square`, `aspect-video`, `aspect-[4/3]` |
| Z-index | `z-*`, `z-auto`, `z-[...]` |
| Visibility | `visible`, `invisible`, `collapse` |
| Columns | `columns-*`, `break-*` |
| Box behavior | `box-border`, `box-content`, `box-decoration-slice`, `box-decoration-clone` |

## Core Patterns

### Full-cover media

```html
<div class="relative aspect-video overflow-hidden rounded-lg">
  <img class="absolute inset-0 size-full object-cover" src="/cover.jpg" alt="" />
</div>
```

### Sticky header inside a scrolling region

```html
<div class="max-h-96 overflow-y-auto">
  <header class="sticky top-0 z-10 bg-white/90 backdrop-blur">Filters</header>
  <!-- content -->
</div>
```

### Visually hidden vs removed

Use `hidden` to remove from layout. Use `invisible` to preserve layout space. For screen-reader-only content, use the official `sr-only` utility from accessibility docs when applicable.

### Logical positioning

Use logical inset utilities for bidirectional layouts:

```html
<button class="absolute inset-e-3 top-3">Close</button>
```

## Common Mistakes

### [HIGH] Using `invisible` when content must not affect layout

`invisible` hides visually but keeps space. Use `hidden` when the element should not participate in layout.

### [MEDIUM] Forgetting `relative` on positioned parents

Absolutely positioned children need a positioned ancestor when they should be anchored locally.

### [MEDIUM] Fighting z-index without understanding stacking contexts

Utilities like `isolate`, opacity, transforms, filters, and positioned elements can create stacking contexts. Add `isolate` deliberately when a component should contain its stacking.

## API Reference

- Display: `https://tailwindcss.com/docs/display`
- Position: `https://tailwindcss.com/docs/position`
- Top/right/bottom/left: `https://tailwindcss.com/docs/top-right-bottom-left`
- Overflow: `https://tailwindcss.com/docs/overflow`
- Z-index: `https://tailwindcss.com/docs/z-index`
- Object fit: `https://tailwindcss.com/docs/object-fit`
