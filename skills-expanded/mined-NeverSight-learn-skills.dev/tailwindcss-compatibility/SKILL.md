---
name: tailwindcss-compatibility
description: "Use this skill when checking Tailwind CSS v4 browser/tooling compatibility. Covers browser requirements (Safari 16.4+, Chrome 111+, Firefox 128+), modern CSS feature dependencies, when to stay on v3.4, Sass/Less/Stylus guidance, built-in import bundling/prefixing via Lightning CSS, CSS modules and component style blocks, `@reference`, and build-performance pitfalls. Triggers on: compatibility, browser support, Safari, Chrome, Firefox, Sass, Less, Stylus, CSS modules, Vue style block, Svelte style, Astro style, @reference, autoprefixer, postcss-import."
license: MIT
---

Tailwind CSS v4 is designed for modern browsers and is a full CSS build tool. It handles imports, vendor prefixing, nesting transforms, and many workflows that previously required extra preprocessors.

## Quick Start

Use v4 when browser support allows:

- Safari 16.4+
- Chrome 111+
- Firefox 128+

Stay on Tailwind CSS v3.4 when the product must support older browsers.

**Related skills:** `tailwindcss-installation`, `tailwindcss-upgrade-v4`, `tailwindcss-functions-directives`, `tailwindcss-custom-styles`.

## Core Guidance

### Browser support

Tailwind v4 depends on modern CSS features such as registered custom properties and `color-mix()` for core behavior. It also exposes utilities for newer platform features; only use those utilities if the target browsers support them.

Check feature-specific support in a browser database when using cutting-edge CSS like `field-sizing`, `@starting-style`, or `text-wrap: balance`.

### Sass, Less, and Stylus

Do not recommend Sass/Less/Stylus as part of a Tailwind v4 workflow. Tailwind is the CSS build tool:

- `@import` files are bundled by Tailwind.
- CSS variables replace preprocessor variables for runtime design tokens.
- Nested CSS is processed.
- Vendor prefixes are handled.
- Utility generation removes the need for preprocessor loops for class families.

Use plain CSS plus Tailwind directives unless the existing repository has a strong legacy reason.

### CSS modules

Tailwind can coexist with CSS modules, but it is usually better to style directly with utility classes. CSS modules make Tailwind process many CSS files separately, which can slow builds.

When `@apply` or custom theme values are needed inside a CSS module, import context with `@reference`:

```css
@reference "../app.css";

.button {
  @apply bg-blue-500 text-white;
}
```

Alternatively, use CSS variables directly:

```css
.button {
  background: var(--color-blue-500);
}
```

### Vue, Svelte, and Astro style blocks

Treat component `<style>` blocks like CSS modules. Prefer classes in markup. If style blocks need Tailwind context, add `@reference`.

## Common Mistakes

### [HIGH] Upgrading to v4 while supporting old browsers

If the browser matrix includes versions older than Safari 16.4, Chrome 111, or Firefox 128, stay on v3.4 unless the product explicitly accepts loss of support.

### [MEDIUM] Keeping `postcss-import` and `autoprefixer` by habit

Tailwind v4 handles imports and prefixing. Remove redundant tooling during migration unless the project has unrelated CSS that still needs it.

### [MEDIUM] Expecting `@apply` in CSS modules without context

Use `@reference` so theme variables, custom utilities, and variants are visible without duplicating output.

## API Reference

- Compatibility: `https://tailwindcss.com/docs/compatibility`
- Upgrade guide: `https://tailwindcss.com/docs/upgrade-guide`
- Functions and directives: `https://tailwindcss.com/docs/functions-and-directives#reference-directive`
