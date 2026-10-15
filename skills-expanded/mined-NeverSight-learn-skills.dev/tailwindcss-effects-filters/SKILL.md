---
name: tailwindcss-effects-filters
description: "Use this skill when applying visual effects in Tailwind CSS v4. Covers box shadow, text shadow, opacity, mix/background blend modes, masks, filter and backdrop-filter groups, blur/brightness/contrast/drop-shadow/grayscale/hue-rotate/invert/saturate/sepia, scrollbar styling utilities, dark-mode effects, and performance considerations. Triggers on: shadow, text-shadow, opacity, blend mode, mix-blend, background-blend, mask, filter, backdrop-filter, blur, drop-shadow, grayscale, scrollbar, scrollbar-thin, scrollbar-color."
license: MIT
---

Effects utilities control depth, translucency, compositing, masks, filters, and scrollbars. Use them deliberately because many create new compositing work in the browser.

## Quick Start

```html
<div class="rounded-xl bg-white/80 p-6 shadow-xl shadow-sky-950/10 ring-1 ring-black/5 backdrop-blur dark:bg-gray-900/80 dark:shadow-black/40 dark:ring-white/10">
  <!-- ... -->
</div>
```

**Related skills:** `tailwindcss-backgrounds-borders`, `tailwindcss-colors`, `tailwindcss-transitions-animation`, `tailwindcss-interactivity`.

## Utility Map

| Need | Utilities |
|---|---|
| Box shadow | `shadow-xs`, `shadow-sm`, `shadow-lg`, `shadow-color/opacity` |
| Text shadow | `text-shadow-*` |
| Opacity | `opacity-*` |
| Blend modes | `mix-blend-*`, `bg-blend-*` |
| Filters | `filter`, `blur-*`, `brightness-*`, `contrast-*`, `drop-shadow-*`, `grayscale`, `hue-rotate-*`, `invert`, `saturate-*`, `sepia` |
| Backdrop filters | `backdrop-filter`, `backdrop-blur-*`, `backdrop-brightness-*`, etc. |
| Masks | `mask-[...]`, `mask-none`, `mask-cover`, `mask-center`, `mask-no-repeat`, `mask-add`, `mask-intersect`, `mask-b-from-*` |
| Scrollbars | `scrollbar-auto`, `scrollbar-thin`, `scrollbar-none`, `scrollbar-thumb-*`, `scrollbar-track-*` |

## Core Patterns

### Glass surface

```html
<div class="bg-white/70 backdrop-blur-md ring-1 ring-white/40 supports-[backdrop-filter]:bg-white/60">
  <!-- ... -->
</div>
```

Include a reasonable fallback background for browsers/environments where the effect is not available.

### Text shadow

Tailwind CSS v4.1 added text shadow utilities:

```html
<h1 class="text-shadow-lg text-white">Over image</h1>
```

### Scrollbar styling

Tailwind CSS v4.3 adds first-party scrollbar styling:

```html
<div class="overflow-auto scrollbar-thin scrollbar-thumb-sky-700 scrollbar-track-sky-100">
  <!-- ... -->
</div>
```

### Masks

Use masks for fades and image effects:

```html
<div class="mask-b-from-80% mask-b-to-100%">
  <!-- ... -->
</div>
```

Verify exact mask utility syntax in the docs; the mask API is broad.

## Common Mistakes

### [HIGH] Using effects to solve contrast problems

Text shadow and backdrop blur are not substitutes for sufficient color contrast. Test foreground/background contrast.

### [MEDIUM] Animating expensive filters everywhere

Filters and backdrop filters can be expensive. Limit animated filters to small regions and test runtime behavior.

### [MEDIUM] Using old v3 shadow/blur scale assumptions after upgrade

Some shadow, blur, radius, and drop-shadow scale names changed in v4. Load `tailwindcss-upgrade-v4` for migrations.

## API Reference

- Box shadow: `https://tailwindcss.com/docs/box-shadow`
- Text shadow: `https://tailwindcss.com/docs/text-shadow`
- Opacity: `https://tailwindcss.com/docs/opacity`
- Filter: `https://tailwindcss.com/docs/filter`
- Backdrop filter: `https://tailwindcss.com/docs/backdrop-filter`
- Mask image: `https://tailwindcss.com/docs/mask-image`
- Scrollbar width: `https://tailwindcss.com/docs/scrollbar-width`
- Scrollbar color: `https://tailwindcss.com/docs/scrollbar-color`
