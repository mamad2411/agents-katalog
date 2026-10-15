---
name: sapphire-design
description: "Approximate the Danske Bank Sapphire design system using plain CSS and HTML, without installing @danske/sapphire-* packages. Use this skill whenever the user asks to build UI that should look like Sapphire, match Danske Bank's design system, create Sapphire-styled components, or wants banking/fintech UI with a Scandinavian design language. Also trigger when the user mentions 'sapphire tokens', 'sapphire components', or wants to create UI prototypes that follow the Sapphire visual style. This skill is framework-agnostic and works with any frontend stack."
---

# Sapphire Design System (Lightweight Approximation)

This skill teaches you how to build UI that closely matches Danske Bank's Sapphire design system using only CSS custom properties and plain HTML/CSS patterns. No npm packages required.

The real Sapphire system uses `@danske/sapphire-react`, `@danske/sapphire-css`, `@danske/sapphire-design-tokens`, and `@danske/sapphire-icons`. This skill extracts the essential design tokens, component patterns, and icon catalog so you can replicate the look and feel in any framework (React, Vue, Svelte, plain HTML, etc.).

## Quick Start

Every Sapphire-styled page needs two things:

1. **A theme class on a root element** - Add `class="sapphire-theme-default"` to your `<body>` or root container
2. **The design tokens CSS** - Either link to the tokens stylesheet or inline the CSS custom properties

The tokens define everything: colors, spacing, typography, radii, shadows, and control sizes. Components are built by referencing these tokens, which means your entire UI stays consistent and theme-switchable.

```html
<body class="sapphire-theme-default">
  <!-- All Sapphire-styled content goes here -->
</body>
```

## How to Use This Skill

1. **Start with tokens**: Read `references/tokens.md` for the full set of CSS custom properties. Copy the `.sapphire-theme-default` block into your project's CSS.
2. **Build components**: Read only the component reference files you need (see table below). This keeps context lean — not every page needs every component.
3. **Add icons**: Read `references/icons.md` for the complete icon catalog (700+ icons). Icons are simple SVGs that you can inline or reference.

## Component References

Components are split into focused files. Read only what your task requires:

| File | Components | When to read |
|------|-----------|-------------|
| `references/core.md` | Surface, Text, Card, Separator, Layout (stack/row/container) | **Always** — needed for any Sapphire page |
| `references/buttons.md` | Button (7 variants × 3 sizes, states, icons) | When the UI has buttons or clickable actions |
| `references/forms.md` | Text Field, Checkbox, Radio, Switch, Select | When the UI has form inputs or settings |
| `references/feedback.md` | Badge, Alert, Tabs, Dialog/Modal, Avatar | When the UI shows status indicators, navigation tabs, modals, or user avatars |

For a typical page, start with `core.md` + `buttons.md`. Add `forms.md` if there are inputs, `feedback.md` if there are badges/alerts/tabs/dialogs.

## Design Principles

Sapphire follows these key principles that you should maintain:

- **Semantic color tokens**: Never hardcode colors. Use semantic tokens like `--sapphire-semantic-color-foreground-primary` instead of raw hex/hsl values. This ensures theme compatibility (light, dark, contrast modes).
- **Consistent spacing scale**: Use the spacing tokens (`--sapphire-semantic-size-spacing-*`) for all padding, margins, and gaps. The scale runs from `4xs` (0.125rem) to `6xl` (4.5rem).
- **Pill-shaped buttons**: Buttons use `border-radius` equal to their height, creating the signature pill shape.
- **Subtle interaction states**: Hover/active states use semi-transparent overlays via `color-mix()`, not distinct solid colors. This creates smooth, layered interactions.
- **Typography hierarchy**: Use the heading scale (`heading-2xl` down to `heading-xs`) and body scale (`body-lg` down to `body-xs`) with the Danske font family (falls back to system sans-serif).
- **Focus rings**: All interactive elements show a `2px solid blue-400` outline on keyboard focus, offset by 2px.
- **Disabled = 30% opacity**: Disabled elements use `opacity: 0.3` universally.

## Theme Variants

Sapphire has three surface levels plus a contrast (dark) mode. Each adjusts token values:

| Class | Background | Use Case |
|-------|-----------|----------|
| `.sapphire-theme-default` | White | Primary surface |
| `.sapphire-theme--secondary` | Sand-50 | Elevated sections |
| `.sapphire-theme--tertiary` | Sand-100 | Nested containers |
| `.sapphire-theme--contrast` | Gray-900 (dark) | Dark mode / hero sections |

Nest theme classes to create depth. A card on a secondary surface would have the secondary class on the section and the default class on the card itself.

## Font

Sapphire uses the proprietary "Danske" font. When approximating without the font files, use a system font stack that matches the geometric sans-serif style:

```css
font-family: 'Danske', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
```

## Accessibility

- All interactive elements must have visible focus indicators (the focus ring tokens handle this)
- Color is never the sole indicator of state - always pair with icons, text, or shape
- Minimum touch target size: `--sapphire-semantic-size-height-control-sm` (2rem / 32px)
- Use semantic HTML elements (`<button>`, `<input>`, `<nav>`) - the CSS classes layer on top
