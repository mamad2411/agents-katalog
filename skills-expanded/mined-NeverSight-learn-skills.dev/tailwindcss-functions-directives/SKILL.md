---
name: tailwindcss-functions-directives
description: "Use this skill when writing Tailwind CSS v4 directives and functions in CSS. Covers `@import`, `@theme`, `@source`, `@utility`, `@variant`, `@custom-variant`, `@apply`, `@reference`, legacy `@config` and `@plugin`, subpath imports, `theme()`, `--spacing()`, `--alpha()`, `--value()`, `--modifier()`, and `--default()`. Triggers on: @import, @theme, @source, @utility, @variant, @custom-variant, @apply, @reference, @config, @plugin, theme(), --spacing(), --alpha(), --value(), --modifier(), --default()."
license: MIT
---

Tailwind CSS v4 exposes CSS directives and functions for configuration, custom utilities, variants, source scanning, and legacy interop.

## Quick Start

```css
@import "tailwindcss";

@theme {
  --color-brand-500: oklch(0.68 0.18 245);
}

@custom-variant dark (&:where(.dark, .dark *));

@utility content-auto {
  content-visibility: auto;
}
```

**Related skills:** `tailwindcss-theme`, `tailwindcss-source-detection`, `tailwindcss-custom-styles`, `tailwindcss-dark-mode`, `tailwindcss-upgrade-v4`.

For a compact directive/function lookup table, read [references/directives-and-functions.md](references/directives-and-functions.md).

## Directive Reference

### `@import`

Import Tailwind and other CSS:

```css
@import "tailwindcss";
@import "./typography.css";
```

### `@theme`

Define design tokens that generate utilities:

```css
@theme {
  --font-display: Inter, sans-serif;
  --color-brand-500: oklch(0.68 0.18 245);
}
```

### `@source`

Register, safelist, or exclude source paths/classes:

```css
@source "../node_modules/@acmecorp/ui-lib";
@source inline("{hover:,focus:,}underline");
@source not "../src/legacy";
```

### `@utility`

Register a utility:

```css
@utility content-auto {
  content-visibility: auto;
}
```

Functional utility:

```css
@utility tab-* {
  tab-size: --value(integer, --default(4));
}
```

### `@variant`

Apply variants in CSS:

```css
.button {
  background: var(--color-sky-600);

  @variant hover, focus {
    background: var(--color-sky-700);
  }
}
```

### `@custom-variant`

Define custom selector variants:

```css
@custom-variant theme-midnight (&:where([data-theme="midnight"], [data-theme="midnight"] *));
```

### `@apply`

Inline existing utility classes in custom CSS:

```css
.select2-dropdown {
  @apply rounded-b-lg shadow-md;
}
```

Use it when CSS is necessary. Prefer utility classes in markup for normal components.

### `@reference`

Import theme variables, custom utilities, and custom variants into CSS modules or component style blocks without duplicating emitted CSS:

```css
@reference "../app.css";

.button {
  @apply bg-blue-500 text-white;
}
```

If using only the default theme:

```css
@reference "tailwindcss";
```

### `@config` and `@plugin`

Use these for legacy JavaScript config/plugins during migration:

```css
@config "../../tailwind.config.js";
@plugin "@tailwindcss/typography";
```

CSS-defined theme, utilities, and variants take precedence where they overlap.

## Function Reference

### `theme()`

Use dot-notation access when you specifically need it:

```css
.card {
  margin: theme(spacing.12);
}
```

Prefer CSS variables such as `var(--spacing-12)` when available.

### `--spacing()`

Use the spacing scale in custom utilities:

```css
@utility inset-* {
  inset: --spacing(--value(integer));
}
```

### `--value()`, `--modifier()`, and `--default()`

Use these to define functional utilities:

```css
@utility opacity-* {
  opacity: calc(--value(integer) * 1%);
  opacity: --value([percentage]);
  opacity: --value(--opacity-*);
}
```

```css
@utility tab-* {
  tab-size: --value(integer, --default(4));
  line-height: --modifier(integer, --default(1));
}
```

## Common Mistakes

### [HIGH] Using `@apply` in CSS modules without `@reference`

CSS modules and component style blocks are processed separately. Import the main stylesheet as reference first.

### [MEDIUM] Keeping legacy `@config` forever

Use `@config` for incremental migration only. Move tokens and utilities to CSS when practical.

### [MEDIUM] Using `@plugin` for behavior already expressible in CSS

In v4, many project plugins can be replaced by `@theme`, `@utility`, and `@custom-variant`.

## API Reference

- Functions and directives: `https://tailwindcss.com/docs/functions-and-directives`
- Adding custom styles: `https://tailwindcss.com/docs/adding-custom-styles`
- Source detection: `https://tailwindcss.com/docs/detecting-classes-in-source-files`
