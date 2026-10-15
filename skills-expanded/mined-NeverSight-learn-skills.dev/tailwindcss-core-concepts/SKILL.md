---
name: tailwindcss-core-concepts
description: "Use this skill when explaining or applying Tailwind CSS v4's core model: utility-first styling, static CSS generation, zero runtime, class composition, generated CSS, design-token constraints, CSS-first configuration, variants, responsive prefixes, and when to use utilities instead of inline styles or custom CSS. Triggers on: utility-first, utility classes, generated CSS, zero runtime, className, why Tailwind, inline styles, design tokens, class composition, v4 model, CSS-first."
license: MIT
---

Tailwind CSS works by scanning source files for class names, generating the CSS for the classes it recognizes, and writing static CSS. There is no Tailwind runtime in the browser for normal builds.

## Quick Start

```html
<article class="mx-auto max-w-2xl rounded-xl bg-white p-6 shadow-lg ring-1 ring-gray-950/5 dark:bg-gray-900 dark:ring-white/10">
  <h2 class="text-xl font-semibold text-gray-950 dark:text-white">Release notes</h2>
  <p class="mt-2 text-sm/6 text-gray-600 dark:text-gray-300">
    Utility classes compose layout, color, spacing, typography, and state in markup.
  </p>
</article>
```

Use utilities directly for local presentational decisions. Move to theme variables, custom utilities, or custom CSS when a pattern needs a named token or repeated API.

**Related skills:** `tailwindcss-theme`, `tailwindcss-states-variants`, `tailwindcss-responsive-design`, `tailwindcss-custom-styles`, `tailwindcss-source-detection`.

## Core model

### Utility classes are the styling API

Tailwind classes usually map to one CSS property or a small, predictable declaration set. Compose them in markup:

```html
<button class="rounded-lg bg-sky-600 px-4 py-2 text-sm font-medium text-white hover:bg-sky-700">
  Save
</button>
```

This keeps styling local to the element and avoids inventing selectors for one-off presentation.

### Theme variables provide constraints

Use values from the design system instead of magic numbers:

```html
<div class="space-y-4 text-gray-700">
  <h1 class="text-3xl font-bold text-gray-950">Dashboard</h1>
  <p class="text-sm/6">The spacing and color choices come from theme tokens.</p>
</div>
```

Use arbitrary values only when the value is genuinely one-off and should not become part of the theme.

### Variants express conditions

Prefix a utility with a condition:

```html
<a class="text-gray-600 hover:text-gray-950 focus-visible:outline-2 md:text-sm dark:text-gray-300">
  Docs
</a>
```

Variants stack from left to right and can combine state, media, feature, dark mode, group/peer, data, aria, and arbitrary selectors.

### CSS-first v4 configuration

Tailwind v4 customization belongs in CSS for most projects:

```css
@import "tailwindcss";

@theme {
  --color-brand-500: oklch(0.68 0.18 245);
  --font-display: Inter, ui-sans-serif, system-ui, sans-serif;
}
```

This creates utilities such as `bg-brand-500` and `font-display`.

## Decision guide

| Need | Use |
|---|---|
| Local layout, spacing, color, state | Utility classes |
| Reusable design token | `@theme` variable |
| One-off value | Arbitrary value like `top-[117px]` |
| CSS property with no built-in utility | Arbitrary property like `[mask-type:luminance]` |
| Project-specific reusable utility | `@utility` |
| Third-party component override | Custom CSS or `@apply` where needed |

## Common Mistakes

### [HIGH] Dynamically constructing class names

Wrong:

```jsx
<button className={`bg-${color}-600 hover:bg-${color}-500`} />
```

Correct:

```jsx
const variants = {
  blue: "bg-blue-600 hover:bg-blue-500",
  red: "bg-red-600 hover:bg-red-500",
};

<button className={variants[color]} />;
```

Tailwind scans files as text and needs complete class names present in the source.

### [MEDIUM] Replacing every repeated class list with `@apply`

Prefer component extraction in the host framework for reusable UI. Reach for `@apply` mainly when styling third-party markup, CSS modules, or framework style blocks that cannot carry classes directly.

### [MEDIUM] Treating `sm:` as mobile

Unprefixed utilities target mobile and all sizes. `sm:` applies at the small breakpoint and above. See `tailwindcss-responsive-design`.

## API Reference

- Styling with utility classes: `https://tailwindcss.com/docs/styling-with-utility-classes`
- Theme variables: `https://tailwindcss.com/docs/theme`
- Detecting classes: `https://tailwindcss.com/docs/detecting-classes-in-source-files`
- Functions and directives: `https://tailwindcss.com/docs/functions-and-directives`
