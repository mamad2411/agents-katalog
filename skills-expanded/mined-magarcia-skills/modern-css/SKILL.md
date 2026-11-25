---
name: modern-css
description: >
  Modern CSS best practices and patterns. Use when writing, editing, or reviewing
  CSS, SCSS, styled-components, or any task that produces CSS output. Provides
  modern alternatives to legacy hacks, JavaScript workarounds, and library
  dependencies.
---

# Modern CSS

When writing or reviewing CSS, prefer modern CSS features over legacy hacks, JavaScript workarounds, or library dependencies.

## How to Use

Read individual rule files in the `rules/` directory for detailed before/after code examples:

```
rules/layout-inset.md
rules/color-oklch.md
rules/selector-has.md
```

Each rule file contains a before/after comparison and browser support percentage. See `rules/_sections.md` for category definitions and ordering.

Treat bundled support percentages as snapshots, not current compatibility guarantees. Check the project's Browserslist or supported-browser policy first. For newly available or experimental features, verify current support in primary browser documentation before recommending production use.

## Rule Categories

| Priority | Category | Prefix | Support |
|----------|----------|--------|---------|
| 1 | Layout & Positioning | `layout-` | 90%+ |
| 2 | Colors & Theming | `color-` | 83-96% |
| 3 | Typography & Fonts | `typography-` | 79-96% |
| 4 | Selectors & Specificity | `selector-` | 84-96% |
| 5 | Transitions & Animation | `animation-` | 69-92% |
| 6 | Interactive Components | `component-` | 72-96% |
| 7 | Performance & Rendering | `performance-` | 90-96% |
| 8 | Forms | `form-` | 73-93% |
| 9 | Experimental | `experimental-` | < 70% |

## Core Principles

1. **CSS over JS** — If a CSS property can replace JavaScript (scroll spy, sticky detection, height animation, IntersectionObserver), use it.
2. **Native over libraries** — Prefer native `<dialog>`, `popover`, `anchor-name`, scroll-snap over Popper.js, Floating UI, Swiper, etc.
3. **Logical properties** — Use `margin-inline-start`, `padding-block-end`, `inset` instead of directional properties (left/right/top/bottom).
4. **oklch for color** — Use `oklch()` for perceptually uniform colors. Use `oklch(from ...)` for tint/shade variants instead of Sass `lighten()`/`darken()`.
5. **Layers for specificity** — Use `@layer` to control specificity instead of `!important` escalation.
6. **Container queries over media queries** — Use `@container` for component-level responsiveness.

## Quick Reference — Use These (90%+ Support)

| Instead of... | Use |
|---|---|
| `position: absolute; top:0; right:0; bottom:0; left:0` | `inset: 0` |
| `display:grid; justify:center; align:center` (verbose) | `place-items: center` |
| `calc(100% - padding)` width hacks | `width: stretch` |
| Padding-top aspect ratio hack | `aspect-ratio: 16/9` |
| JS scroll listeners for sticky | `position: sticky; top: 0` |
| Margin + `:last-child` override | `gap: 16px` |
| Sass `$variables` | `var(--custom-property)` |
| Media query breakpoint ladder | `clamp(1rem, 2.5vw, 2rem)` |
| Manual `<br>` for headline wrapping | `text-wrap: balance` |
| Sass nesting (build step) | Native CSS nesting `& a { }` |
| `:focus` (shows on click) | `:focus-visible` |
| Complex selectors for resets | `:where()` (zero specificity) |
| Repeating selectors | `:is(h1, h2, h3)` grouping |
| `.parent.has-child` class toggle | `:has()` parent selector |
| Background-image cover hack | `object-fit: cover` |
| `overflow-y: scroll` for shift | `scrollbar-gutter: stable` |
| JS `preventDefault` on scroll | `overscroll-behavior: contain` |
| JS IntersectionObserver for lazy | `content-visibility: auto` |
| Separate `@font-face` per weight | Variable font `font-weight: 100 900` |
| JS for dark mode form controls | `color-scheme: light dark` |
| Duplicated dark mode variables | `light-dark(#111, #eee)` |
| `appearance: none` + custom styles | `accent-color: #7c3aed` |
| Separate transform shorthand rewrite | `translate`, `rotate`, `scale` individually |
| JS `classList.toggle` for display | `transition-behavior: allow-discrete` + `@starting-style` |
| Sass `mix()` | `color-mix(in oklch, color1, color2)` |

## Support Tiers

### Widely Available (90%+) — Use freely
oklch colors, backdrop-filter, scrollbar-gutter, overscroll-behavior, object-fit,
inset, content-visibility, accent-color, aspect-ratio, sticky, gap, clamp(),
:is(), :where(), :has(), :focus-visible, CSS variables, native nesting,
@container, color-scheme, font-display, variable fonts, grid-template-areas,
dialog element, scroll-snap, line-clamp, initial-letter, independent transforms,
@property, @layer, logical properties, place-items, stretch, customizable select

### Newly Available (80-89%) — Use with confidence
light-dark(), color-mix(), text-wrap: balance, subgrid, @starting-style,
transition-behavior: allow-discrete, view transitions, :user-invalid/:user-valid,
popover, anchor positioning, @scope, scroll-linked animations

### Limited Support (< 80%) — Use progressively or check project targets
field-sizing, interpolate-size, scroll-state(), attr() typed, if() conditions,
CSS functions, corner-shape, sibling-index(), scroll-button/scroll-marker, text-box
