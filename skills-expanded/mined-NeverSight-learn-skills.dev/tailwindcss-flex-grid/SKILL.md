---
name: tailwindcss-flex-grid
description: "Use this skill when building flexbox or grid layouts in Tailwind CSS v4. Covers flex direction/wrap/basis/grow/shrink/order, grid template columns/rows, grid column/row spans, auto flow, auto columns/rows, gap, justify/align/place utilities, responsive layout changes, and common card/list/sidebar patterns. Triggers on: flex, grid, flex-row, flex-col, flex-wrap, basis, grow, shrink, order, grid-cols, col-span, row-span, auto-cols, auto-rows, gap, justify, align, place, layout grid."
license: MIT
---

Use flexbox for one-dimensional alignment and distribution. Use grid for two-dimensional tracks, spans, and page/card layouts.

## Quick Start

```html
<div class="grid grid-cols-1 gap-4 md:grid-cols-3">
  <aside class="md:col-span-1">Filters</aside>
  <main class="md:col-span-2">Results</main>
</div>
```

```html
<div class="flex items-center justify-between gap-4">
  <div class="min-w-0 flex-1">Title</div>
  <button class="shrink-0">Save</button>
</div>
```

**Related skills:** `tailwindcss-responsive-design`, `tailwindcss-spacing-sizing`, `tailwindcss-layout`.

## Core Patterns

### Flex rows

```html
<div class="flex items-center gap-3">
  <img class="size-10 shrink-0 rounded-full" alt="" />
  <div class="min-w-0 flex-1">
    <p class="truncate font-medium">Ada Lovelace</p>
    <p class="truncate text-sm text-gray-500">Product engineering</p>
  </div>
</div>
```

Use `min-w-0` on flex children that need text truncation.

### Responsive stacks

```html
<div class="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
  <!-- ... -->
</div>
```

### Grid tracks

```html
<div class="grid grid-cols-[16rem_1fr] gap-6">
  <nav>Sidebar</nav>
  <main>Main</main>
</div>
```

Use arbitrary track values for layout-specific grids; promote repeated grids to component abstractions.

### Auto-fit style grids

```html
<div class="grid grid-cols-[repeat(auto-fit,minmax(16rem,1fr))] gap-4">
  <!-- cards -->
</div>
```

### Alignment

| Need | Utilities |
|---|---|
| Main axis distribution | `justify-start`, `justify-between`, `justify-center`, `justify-end` |
| Cross axis alignment | `items-start`, `items-center`, `items-end`, `items-stretch` |
| Per-item override | `self-start`, `self-center`, `justify-self-end`, `place-self-center` |
| Grid content alignment | `content-*`, `place-content-*`, `place-items-*` |

## Common Mistakes

### [HIGH] Forgetting `min-w-0` in flex layouts

Long text inside a flex item may overflow unless the flexible child can shrink:

```html
<div class="min-w-0 flex-1 truncate">Long title</div>
```

### [MEDIUM] Using flex when grid tracks are the real model

If rows and columns both matter, use grid. If only one axis matters, flex is usually simpler.

### [MEDIUM] Recreating spacing with child margins

Prefer `gap-*` for flex/grid spacing unless a margin is semantically needed.

## API Reference

- Flex: `https://tailwindcss.com/docs/flex`
- Flex direction: `https://tailwindcss.com/docs/flex-direction`
- Grid template columns: `https://tailwindcss.com/docs/grid-template-columns`
- Grid column: `https://tailwindcss.com/docs/grid-column`
- Gap: `https://tailwindcss.com/docs/gap`
- Align items: `https://tailwindcss.com/docs/align-items`
- Justify content: `https://tailwindcss.com/docs/justify-content`
