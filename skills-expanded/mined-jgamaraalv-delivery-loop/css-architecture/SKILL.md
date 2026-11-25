---
name: css-architecture
description: Organize CSS using BEM, SMACSS, and CSS-in-JS patterns. Use when building scalable, maintainable styling systems with proper naming conventions.
---

# CSS Architecture

## Overview

Build maintainable CSS systems using methodologies like BEM (Block Element Modifier), SMACSS, and CSS-in-JS patterns with proper organization and conventions.

## Quick Start

Minimal working example:

```css
/* Block - standalone component */
.button {
  display: inline-block;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: all 0.3s ease;
}

/* Element - component part */
.button__icon {
  margin-right: 8px;
  vertical-align: middle;
}

/* Modifier - variant */
.button--primary {
  background-color: #007bff;
  color: white;
}

.button--primary:hover {
  background-color: #0056b3;
// ... (see reference guides for full implementation)
```

## References

Each file is loaded on demand — read one only when the task needs that depth (progressive disclosure).

- `references/bem-block-element-modifier-pattern.md` — the BEM (Block · Element · Modifier) naming methodology and conventions · read when establishing class-naming rules or component-scoped CSS.
- `references/smacss-scalable-and-modular-architecture-for-css.md` — the SMACSS category split (base, layout, module, state, theme) · read when organizing a large stylesheet into scalable layers.
- `references/css-in-js-with-styled-components.md` — CSS-in-JS with styled-components: themed, co-located, component-scoped styles · read when styling in a JS/React runtime rather than static CSS.
- `references/css-variables-custom-properties.md` — CSS custom properties for design tokens, theming, and runtime theme switching · read when building a token system or dark/light theming.
- `references/utility-first-css-tailwind-pattern.md` — the utility-first (Tailwind) approach and when to extract components · read when adopting or reviewing utility-class styling.

A starter component lives at `templates/component-template.tsx` · copy it when scaffolding a new styled component.

## Best Practices

### ✅ DO

- Follow established patterns and conventions
- Write clean, maintainable code
- Add appropriate documentation
- Test thoroughly before deploying

### ❌ DON'T

- Skip testing or validation
- Ignore error handling
- Hard-code configuration values
