---
name: tailwindcss-preflight
description: "Use this skill when working with Tailwind CSS v4 base styles and reset behavior. Covers Preflight, modern-normalize, automatic base layer injection, removed default margins, border reset, unstyled headings/lists, block-level responsive images, hidden attribute behavior, extending `@layer base`, disabling Preflight by importing theme/utilities separately, and third-party library conflicts. Triggers on: Preflight, reset, base styles, headings unstyled, lists no bullets, border reset, image block, max-width image, @layer base, disable preflight."
license: MIT
---

Preflight is Tailwind's opinionated base style layer. It is included automatically by `@import "tailwindcss";` and smooths browser inconsistencies while enforcing design-system constraints.

## Quick Start

Add base styles on top of Preflight with `@layer base`:

```css
@layer base {
  h1 {
    font-size: var(--text-2xl);
    font-weight: var(--font-weight-semibold);
  }

  a {
    color: var(--color-blue-600);
    text-decoration-line: underline;
  }
}
```

**Related skills:** `tailwindcss-custom-styles`, `tailwindcss-functions-directives`, `tailwindcss-compatibility`, `tailwindcss-typography`.

## What Preflight changes

### Margins and padding are reset

Default margins on headings, paragraphs, lists, blockquotes, and other elements are removed. Add spacing intentionally with utilities like `mt-*`, `space-y-*`, `gap-*`, or custom base styles.

### Borders are reset

Elements default to `border: 0 solid`, which makes the `border` utility produce a consistent solid 1px border using current color. This can affect third-party widgets.

Override third-party regions locally:

```css
@layer base {
  .google-map * {
    border-style: none;
  }
}
```

### Headings are unstyled

Heading elements inherit font size and weight. Style headings with utilities or base styles:

```html
<h1 class="text-3xl font-bold tracking-tight">Settings</h1>
```

### Lists are unstyled

Use list utilities when visual bullets/numbers are desired:

```html
<ul class="list-inside list-disc">
  <li>One</li>
  <li>Two</li>
</ul>
```

If a semantic list remains visually unstyled, add `role="list"` where needed for VoiceOver announcement behavior.

### Images and replaced elements

Images, SVG, video, canvas, audio, iframe, embed, and object elements are block-level by default. Images/videos are constrained with `max-width: 100%` and `height: auto`.

Use utilities to opt out:

```html
<img class="inline max-w-none" src="..." alt="" />
```

### Hidden attribute

Elements with `hidden` remain hidden. Remove the attribute when showing an element rather than only adding display utilities.

## Disabling Preflight

Import Tailwind's layers separately and omit Preflight:

```css
@layer theme, base, components, utilities;

@import "tailwindcss/theme.css" layer(theme);
@import "tailwindcss/utilities.css" layer(utilities);
```

When importing pieces individually, put import options on the layer they affect:

```css
@import "tailwindcss/utilities.css" layer(utilities) source(none);
@import "tailwindcss/utilities.css" layer(utilities) important;
@import "tailwindcss/theme.css" layer(theme) theme(static);
```

Use `prefix(tw)` on both theme and utilities imports because it affects variables and utilities.

## Common Mistakes

### [HIGH] Assuming browser default headings/lists still apply

Preflight removes those defaults. Add explicit utilities or base styles.

### [MEDIUM] Globally undoing Preflight for one widget

Scope overrides to the third-party widget container. Do not remove Preflight for the whole app unless integrating into an existing system that cannot tolerate it.

### [MEDIUM] Forgetting accessibility on unstyled lists

If the content is semantically a list but visually unstyled, consider `role="list"` for VoiceOver support.

## API Reference

- Preflight: `https://tailwindcss.com/docs/preflight`
- Adding base styles: `https://tailwindcss.com/docs/adding-custom-styles#adding-base-styles`
- Compatibility: `https://tailwindcss.com/docs/compatibility`
