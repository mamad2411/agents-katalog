---
name: tailwindcss-typography
description: "Use this skill when styling text with Tailwind CSS v4. Covers font family/size/smoothing/style/weight/stretch, numeric variants, font-feature settings, letter spacing, line clamp, line height, lists, text alignment/color/decoration/transform/overflow/wrap/indent, tab size, vertical align, whitespace, word break, overflow-wrap, hyphens, and content utilities. Triggers on: typography, font, text, leading, tracking, line-clamp, list-disc, text color, underline, truncate, text-wrap, whitespace, word-break, overflow-wrap, hyphens, tab-size, content."
license: MIT
---

Typography utilities control text hierarchy, readability, decoration, wrapping, overflow, and generated content.

## Quick Start

```html
<article class="max-w-2xl text-gray-900">
  <p class="text-sm/6 font-medium text-sky-700">Release</p>
  <h1 class="mt-2 text-4xl font-bold tracking-tight text-gray-950">Tailwind CSS skills</h1>
  <p class="mt-4 text-base/7 text-gray-600">
    Compose readable interfaces with font, line-height, color, and wrapping utilities.
  </p>
</article>
```

**Related skills:** `tailwindcss-colors`, `tailwindcss-theme`, `tailwindcss-states-variants`, `tailwindcss-preflight`.

## Utility Map

| Need | Utilities |
|---|---|
| Font family | `font-sans`, `font-serif`, `font-mono`, custom `font-*` |
| Font size/line height | `text-sm`, `text-base/7`, `text-[22px]`, `leading-*` |
| Weight/style | `font-medium`, `font-semibold`, `italic`, `not-italic` |
| Letter spacing | `tracking-tight`, `tracking-wide` |
| Numeric features | `tabular-nums`, `lining-nums`, `oldstyle-nums` |
| Text color | `text-gray-950`, `text-white/80` |
| Decoration | `underline`, `decoration-*`, `underline-offset-*` |
| Overflow | `truncate`, `text-ellipsis`, `line-clamp-*` |
| Wrapping | `text-wrap`, `text-balance`, `whitespace-*`, `break-*`, `wrap-*`, `hyphens-*` |
| Lists | `list-disc`, `list-decimal`, `list-inside`, `list-image-*` |
| Tab width | `tab-*`, `tab-[12px]`, `tab-(--tab-size)` |
| Generated content | `before:content-*`, `after:content-*` |

## Core Patterns

### Font size with line height modifier

```html
<p class="text-sm/6 text-gray-600">Compact readable body copy.</p>
```

### Truncation

```html
<div class="min-w-0 truncate">A very long title that should not break the row</div>
```

For multiple lines:

```html
<p class="line-clamp-3 text-sm/6 text-gray-600">...</p>
```

### Balanced headings

```html
<h1 class="max-w-3xl text-5xl font-bold tracking-tight text-balance">
  Build interfaces without leaving your markup
</h1>
```

### Font feature utilities

Prefer high-level utilities such as `tabular-nums` before low-level OpenType feature utilities.

### Tab size

Tailwind CSS v4.3 adds `tab-*` utilities:

```html
<pre class="tab-4 whitespace-pre font-mono text-sm">...</pre>
```

## Common Mistakes

### [HIGH] Expecting headings to be styled by default

Preflight makes headings inherit font size and weight. Add utilities or base styles explicitly.

### [MEDIUM] Truncating flex children without `min-w-0`

The truncating child must be allowed to shrink:

```html
<div class="min-w-0 flex-1 truncate">Long label</div>
```

### [MEDIUM] Using low-level font-feature utilities when semantic utilities exist

Use `tabular-nums`, `ordinal`, etc. before `font-features-*` unless you specifically need raw OpenType features.

## API Reference

- Font size: `https://tailwindcss.com/docs/font-size`
- Font weight: `https://tailwindcss.com/docs/font-weight`
- Line height: `https://tailwindcss.com/docs/line-height`
- Text overflow: `https://tailwindcss.com/docs/text-overflow`
- Text wrap: `https://tailwindcss.com/docs/text-wrap`
- Tab size: `https://tailwindcss.com/docs/tab-size`
- Content: `https://tailwindcss.com/docs/content`
