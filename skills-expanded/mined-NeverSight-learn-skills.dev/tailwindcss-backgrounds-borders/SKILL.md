---
name: tailwindcss-backgrounds-borders
description: "Use this skill when styling backgrounds, gradients, borders, and outlines in Tailwind CSS v4. Covers background attachment/clip/color/image/origin/position/repeat/size, gradients and arbitrary images, border radius/width/color/style, logical border utilities, outline width/color/style/offset, focus rings vs outlines, and dark-mode surface styling. Triggers on: background, bg-*, gradient, bg-gradient, border, rounded, outline, ring, border color, border width, border style, background image, bg-cover, bg-center."
license: MIT
---

Background, border, and outline utilities define surfaces, emphasis, focus affordances, and media presentation. Use them with color and spacing utilities to create complete component shells.

## Quick Start

```html
<div class="rounded-xl border border-gray-950/10 bg-white bg-linear-to-b from-white to-gray-50 p-6 shadow-sm dark:border-white/10 dark:bg-gray-900 dark:from-gray-900 dark:to-gray-950">
  <!-- ... -->
</div>
```

**Related skills:** `tailwindcss-colors`, `tailwindcss-effects-filters`, `tailwindcss-states-variants`, `tailwindcss-dark-mode`.

## Utility Map

| Need | Utilities |
|---|---|
| Background color | `bg-white`, `bg-gray-950`, `bg-sky-500/10` |
| Background image | `bg-[url(...)]`, gradient utilities |
| Background sizing | `bg-cover`, `bg-contain`, `bg-auto` |
| Background position | `bg-center`, `bg-top`, `bg-[position:...]` |
| Background repeat | `bg-no-repeat`, `bg-repeat-x` |
| Radius | `rounded-*`, `rounded-t-*`, logical corner utilities |
| Border width | `border`, `border-2`, `border-x`, `border-s`, `border-e` |
| Border color | `border-gray-200`, `border-white/10` |
| Border style | `border-solid`, `border-dashed`, `border-none` |
| Outline | `outline-*`, `outline-offset-*`, `outline-hidden`, `outline-none` |

## Core Patterns

### Focus outlines

```html
<button class="rounded-lg bg-sky-600 px-4 py-2 text-white focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-sky-600">
  Save
</button>
```

Use `focus-visible:` for keyboard-focused outlines.

### Media backgrounds

```html
<section class="bg-[url('/img/noise.png')] bg-cover bg-center bg-no-repeat">
  <!-- ... -->
</section>
```

### Gradient surfaces

```html
<div class="bg-linear-to-br from-sky-500 via-blue-600 to-indigo-700"></div>
```

Verify gradient utility names in the official docs when generating complex gradient syntax.

### Subtle borders in dark mode

```html
<div class="border border-gray-950/10 dark:border-white/10">
  <!-- ... -->
</div>
```

Opacity modifiers are often better than choosing separate grays for divider lines.

## Common Mistakes

### [HIGH] Removing accessible focus outlines

Do not use `outline-none` unless you provide an equivalent visible focus style. If you need the old invisible forced-colors behavior during v4 migration, use `outline-hidden`.

### [MEDIUM] Using `border` without an intentional color

Preflight makes borders solid, but `border` uses current color unless a border color is set. Add `border-gray-*` or opacity-modified colors for predictable UI.

### [MEDIUM] Using background images for meaningful content

If the image conveys content, use an `<img>` with alt text rather than a CSS background.

## API Reference

- Background color: `https://tailwindcss.com/docs/background-color`
- Background image: `https://tailwindcss.com/docs/background-image`
- Background size: `https://tailwindcss.com/docs/background-size`
- Border radius: `https://tailwindcss.com/docs/border-radius`
- Border width: `https://tailwindcss.com/docs/border-width`
- Outline width: `https://tailwindcss.com/docs/outline-width`
