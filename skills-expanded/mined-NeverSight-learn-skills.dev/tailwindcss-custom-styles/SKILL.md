---
name: tailwindcss-custom-styles
description: "Use this skill when adding custom styling in Tailwind CSS v4 beyond built-in utilities. Covers arbitrary values (`top-[117px]`), arbitrary properties (`[mask-type:luminance]`), arbitrary variants, whitespace and type hints, custom CSS, `@layer base/components`, `@utility`, functional utilities with `--value()`, `--modifier()`, `--default()`, and when to prefer components over `@apply`. Triggers on: arbitrary value, arbitrary property, arbitrary variant, custom CSS, @layer, @utility, @apply, --value, --modifier, --default, component class."
license: MIT
---

Tailwind is extensible. Start with built-in utilities and theme variables, use arbitrary syntax for true one-offs, and add custom utilities or CSS only when the pattern deserves a reusable API.

## Quick Start

```html
<div class="top-[117px] grid-cols-[1fr_500px_2fr] [mask-type:luminance] lg:top-[344px]">
  <!-- ... -->
</div>
```

```css
@utility content-auto {
  content-visibility: auto;
}
```

```html
<section class="content-auto">
  <!-- ... -->
</section>
```

**Related skills:** `tailwindcss-theme`, `tailwindcss-functions-directives`, `tailwindcss-source-detection`, `tailwindcss-states-variants`.

## Core Patterns

### Arbitrary values

Use square brackets for one-off values:

```html
<div class="top-[117px] bg-[#bada55] text-[22px] before:content-['New']">
  <!-- ... -->
</div>
```

Use CSS variable shorthand when referencing custom properties:

```html
<div class="fill-(--brand-icon-color)"></div>
```

This is shorthand for a `var(...)` arbitrary value.

### Arbitrary properties

```html
<div class="[mask-type:luminance] hover:[mask-type:alpha] [--scroll-offset:56px] lg:[--scroll-offset:44px]">
  <!-- ... -->
</div>
```

### Whitespace and ambiguity

Use underscores for spaces inside arbitrary values:

```html
<div class="grid-cols-[1fr_500px_2fr]"></div>
```

When a namespace is ambiguous, include a CSS data type hint:

```html
<div class="text-(length:--body-size) text-(color:--body-color)"></div>
```

### Arbitrary variants

```html
<ul class="lg:[&>li:nth-child(-n+3)]:font-semibold">
  <!-- ... -->
</ul>
```

Promote repeated selector patterns to `@custom-variant`.

### Custom base styles

Use the base layer for element defaults:

```css
@layer base {
  h1 {
    font-size: var(--text-2xl);
    font-weight: var(--font-weight-semibold);
  }
}
```

### Component classes

Use component classes sparingly, mainly when custom CSS must remain overridable by utilities:

```css
@layer components {
  .card {
    border-radius: var(--radius-lg);
    background: var(--color-white);
    box-shadow: var(--shadow-sm);
  }
}
```

In React/Vue/Svelte/etc., often prefer extracting a component with utility classes over creating `.btn` and `.card` CSS.

### Custom utilities

Simple utility:

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

Use `--modifier()` when supporting slash modifiers:

```css
@utility text-* {
  font-size: --value(--text-*, [length]);
  line-height: --modifier(--leading-*, [length], [*]);
}
```

## Common Mistakes

### [HIGH] Turning one-off values into theme tokens too early

If a value is only needed once, use an arbitrary value. Add `@theme` tokens when the value is part of the design system.

### [MEDIUM] Using `@apply` as the default reuse mechanism

Prefer framework components for reusable markup. Use `@apply` for third-party markup, CSS modules/style blocks, or unavoidable CSS contexts.

### [MEDIUM] Leaving ambiguous arbitrary variables untyped

If `text-(--my-var)` could mean font size or color, use `text-(length:--my-var)` or `text-(color:--my-var)`.

## API Reference

- Adding custom styles: `https://tailwindcss.com/docs/adding-custom-styles`
- Functions and directives: `https://tailwindcss.com/docs/functions-and-directives`
- Theme variables: `https://tailwindcss.com/docs/theme`
