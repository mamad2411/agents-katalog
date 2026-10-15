---
name: tailwindcss-theme
description: "Use this skill when customizing Tailwind CSS v4 design tokens with `@theme`. Covers theme variables, token namespaces (`--color-*`, `--font-*`, `--text-*`, `--spacing-*`, `--breakpoint-*`, `--container-*`, shadows, radius, easing, animation), generated utilities, default theme extension/removal, CSS variable usage, and when to use `:root` instead of `@theme`. Triggers on: @theme, theme variables, design tokens, CSS variables, custom colors, custom font, custom breakpoint, spacing scale, default theme, token namespace."
license: MIT
---

Theme variables are special CSS variables declared with `@theme`. They both expose CSS variables and tell Tailwind which theme-backed utilities should exist.

## Quick Start

```css
@import "tailwindcss";

@theme {
  --font-display: Inter, ui-sans-serif, system-ui, sans-serif;
  --color-brand-500: oklch(0.68 0.18 245);
  --breakpoint-3xl: 120rem;
  --radius-card: 0.875rem;
}
```

```html
<section class="rounded-card bg-brand-500 font-display 3xl:max-w-7xl">
  <!-- ... -->
</section>
```

**Related skills:** `tailwindcss-colors`, `tailwindcss-responsive-design`, `tailwindcss-custom-styles`, `tailwindcss-functions-directives`.

For a namespace lookup table, read [references/theme-namespaces.md](references/theme-namespaces.md).

## Core Concepts

### Use `@theme` for utility-backed tokens

```css
@theme {
  --color-mint-500: oklch(0.72 0.11 178);
}
```

This creates utilities such as `bg-mint-500`, `text-mint-500`, `border-mint-500`, and related color utilities.

### Use `:root` for ordinary variables

Use `:root` when the variable is not meant to generate utilities:

```css
:root {
  --sidebar-width: 18rem;
}
```

Then reference it with arbitrary values:

```html
<aside class="w-[var(--sidebar-width)]">...</aside>
```

### Theme namespaces

Common namespaces include:

| Namespace | Creates utilities for |
|---|---|
| `--color-*` | color utilities such as `bg-*`, `text-*`, `border-*`, `fill-*`, `stroke-*` |
| `--font-*` | `font-*` family utilities |
| `--text-*` | font-size utilities |
| `--spacing-*` | spacing-driven utilities |
| `--breakpoint-*` | responsive variants |
| `--container-*` | container query variants and container sizes |
| `--radius-*` | border radius utilities |
| `--shadow-*` | shadow utilities |
| `--ease-*` | transition timing utilities |
| `--animate-*` | animation utilities |

Verify exact namespaces against the official theme docs when adding a new token family.

### Override, extend, or remove defaults

Add new tokens by defining new variables:

```css
@theme {
  --color-avocado-500: oklch(0.84 0.18 117.33);
}
```

Override a default token by redefining the same variable:

```css
@theme {
  --font-sans: Inter, ui-sans-serif, system-ui, sans-serif;
}
```

Remove a default token by setting it to `initial`:

```css
@theme {
  --breakpoint-2xl: initial;
}
```

Reset a namespace when intentionally replacing the scale:

```css
@theme {
  --breakpoint-*: initial;
  --breakpoint-tablet: 40rem;
  --breakpoint-desktop: 80rem;
}
```

## Common Mistakes

### [HIGH] Defining utility-backed tokens inside selectors

`@theme` variables must be top-level, not nested inside selectors or media queries.

### [HIGH] Expecting `:root --color-brand-500` to create utilities

Use `@theme` when `bg-brand-500` or similar utilities should exist. `:root` only defines a normal CSS variable.

### [MEDIUM] Adding many one-off tokens

Use arbitrary values for rare one-offs. Promote values to `@theme` only when they are part of the design system.

## API Reference

- Theme variables: `https://tailwindcss.com/docs/theme`
- Colors: `https://tailwindcss.com/docs/colors`
- Responsive custom breakpoints: `https://tailwindcss.com/docs/responsive-design#customizing-your-theme`
- Functions and directives: `https://tailwindcss.com/docs/functions-and-directives#theme-directive`
