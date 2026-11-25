---
name: canon-responsive
description: Use when designing or auditing responsive behavior, breakpoints, fluid type, container queries, mobile-first CSS, or layouts that adapt to viewport sizes. Trigger when the user mentions mobile, tablet, desktop, breakpoint, fluid, responsive, viewport, or asks how something should behave at different sizes.
---

# CANON · Responsive Design

Mobile-first is non-negotiable. Container queries beat media queries for component-level responsiveness. Fluid type beats stepped breakpoints for headings.

## Quantified Rules

### Breakpoints

```css
/* Mobile-first: base styles target the smallest screen */
/* Default: < 640px */

@media (min-width: 640px)  { /* sm — large phone, small tablet */ }
@media (min-width: 768px)  { /* md — tablet portrait */ }
@media (min-width: 1024px) { /* lg — tablet landscape, small laptop */ }
@media (min-width: 1280px) { /* xl — laptop */ }
@media (min-width: 1536px) { /* 2xl — large desktop */ }
```

These match Tailwind defaults and align with common device widths. Don't invent breakpoints unless the design demands it.

**Use `min-width`, not `max-width`.** Mobile-first means base styles work everywhere, breakpoints add complexity at larger sizes.

### Container Widths

| Container | Mobile (<640) | Tablet (768) | Desktop (1280+) |
|---|---|---|---|
| Page horizontal padding | 16–24px | 32–48px | 48–80px |
| Prose max-width | 100% | 65ch | 65ch |
| Marketing max-width | 100% | 100% | 1200–1280px |
| App max-width | 100% | 100% | 1440–1600px |

### Fluid Type

Use `clamp()` for headings that scale smoothly between mobile and desktop:

```css
h1 {
  font-size: clamp(2rem, 5vw + 1rem, 4.5rem);
  /*           min,    preferred,    max */
}
```

| Heading | Fluid range |
|---|---|
| H1 (marketing) | `clamp(2rem, 5vw + 1rem, 4.5rem)` (32–72px) |
| H1 (app) | `clamp(1.75rem, 3vw + 0.5rem, 2.25rem)` (28–36px) |
| H2 | `clamp(1.5rem, 3vw + 0.5rem, 2.25rem)` (24–36px) |
| H3 | `clamp(1.25rem, 2vw + 0.5rem, 1.75rem)` (20–28px) |
| Body | 16px (don't scale body) |

**Rule: scale headings, not body text.** Body stays 16px across all sizes for reading consistency.

### Container Queries (preferred over media for components)

```css
.card-grid {
  container-type: inline-size;
}

.card {
  /* default: 1 column */
  display: block;
}

@container (min-width: 600px) {
  .card {
    display: grid;
    grid-template-columns: 200px 1fr;
  }
}
```

**Use container queries for component-level responsiveness.** Media queries are for page-level layout. A card should change layout based on its container width, not the viewport width.

### Viewport Units

| Unit | Use case | Caveat |
|---|---|---|
| `vw` | Fluid type via `clamp()` | Don't use alone (no max) |
| `vh` | Hero sections | Buggy on mobile (URL bar) |
| `dvh` (dynamic) | Mobile full-height | Modern, prefer this |
| `svh` / `lvh` | Smallest/largest viewport | Use for predictable behavior |

```css
.hero {
  min-height: 100dvh;  /* dynamic viewport height, accounts for browser chrome */
}
```

### Touch vs Pointer

```css
@media (hover: hover) and (pointer: fine) {
  /* Mouse: enable hover effects */
  .button:hover { background: var(--color-accent-hover); }
}

@media (hover: none) and (pointer: coarse) {
  /* Touch: increase tap targets, remove hover */
  .button { min-height: 44px; }
}
```

**Rule: hover effects only inside `(hover: hover)`.** This prevents touch devices from getting stuck hover states.

### Image Responsiveness

```html
<img
  src="image-800w.jpg"
  srcset="image-400w.jpg 400w, image-800w.jpg 800w, image-1200w.jpg 1200w"
  sizes="(min-width: 1024px) 50vw, 100vw"
  loading="lazy"
  decoding="async"
  width="800"
  height="600"
  alt="Description"
/>
```

| Attribute | Why |
|---|---|
| `srcset` + `sizes` | Browser picks correct resolution |
| `loading="lazy"` | Defer offscreen images |
| `decoding="async"` | Doesn't block rendering |
| `width`/`height` | Reserves space, prevents CLS |

For art direction (different crops at different sizes), use `<picture>` with `<source>`.

### Layout Patterns That Self-Adapt

#### Auto-Grid

```css
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--space-3);
}
```

No media queries needed. Grid wraps based on item width.

#### Sidebar That Stacks

```css
.layout {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-6);
}
.sidebar { flex: 1 1 240px; }
.main    { flex: 999 1 600px; }
```

Sidebar and main share row when there's space. Sidebar wraps below when there isn't. No breakpoints.

#### Switch Layout

```css
.switcher {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-3);
}
.switcher > * {
  flex-grow: 1;
  flex-basis: calc((40rem - 100%) * 999);
  /* When container > 40rem: fills row. Below: wraps to its own row. */
}
```

The Switcher pattern from Every Layout. Container width determines layout, no media queries.

## Mobile-First CSS Order

```css
/* 1. Base: smallest viewport */
.card {
  padding: 16px;
  font-size: 14px;
}

/* 2. Tablet up */
@media (min-width: 768px) {
  .card {
    padding: 24px;
    font-size: 15px;
  }
}

/* 3. Desktop up */
@media (min-width: 1280px) {
  .card {
    padding: 32px;
    font-size: 16px;
  }
}
```

**Never write desktop styles first then override for mobile.** That's desktop-first, which produces fragile cascades.

## Anti-Patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| `max-width: 768px` media queries | Desktop-first | Use `min-width` |
| Hardcoded `width: 1200px` | Doesn't fit smaller screens | Use `max-width` + horizontal padding |
| `100vh` on mobile | Cuts off below URL bar | Use `100dvh` |
| Hover effects without `(hover: hover)` | Stuck on touch | Wrap in feature query |
| Tiny tap targets on mobile | Below 44px | Increase via padding |
| Same font-size desktop and mobile | No fluid scaling for headings | Use `clamp()` |
| Body font scaling with viewport | Reading size shouldn't change | 16px body, period |
| Side-scrolling grids on mobile (uncontrolled) | Confuses users | Use scroll-snap or stack |
| Tables without horizontal scroll | Overflow breaks layout | Wrap in `overflow-x: auto` |
| Images without `width`/`height` | Cumulative Layout Shift | Always set both |
| Images without `srcset` | Loads full size on mobile | Use responsive images |
| Custom breakpoints (e.g., 743px) | Brittle, no system | Use the standard 5 |
| `display: none` for mobile content | Mobile users miss it | Show different content via flex/grid |
| Fixed-height heroes | Crops on small screens | Use `min-height` |

## Decision Tree

```
Designing a layout?
├─ Component-level (a card, a list) → container queries
├─ Page-level (header, sidebar, main) → media queries
├─ Heading sizes → fluid (clamp)
├─ Body text → static 16px
├─ Hero section → 100dvh, mobile-first
└─ Grid of items → auto-fit + minmax (no media queries)
```

## Audit Checklist

1. Open DevTools, switch to mobile (375px). Layout works without horizontal scroll?
2. Resize browser slowly from 320px to 1920px. Any awkward intermediate states?
3. Check headings. Use `clamp()`? Body stays 16px?
4. Check `100vh` usage. Replaced with `100dvh`?
5. Check hover effects. Wrapped in `(hover: hover)` where critical?
6. Check tap targets. All >= 44×44 on mobile?
7. Check images. `srcset` + `sizes` + `width` + `height`?
8. Check tables. Wrapped in `overflow-x: auto`?
9. Check breakpoint count. Using the standard 5?
10. Check media query direction. All `min-width`, not mixed?

## Citations

- Web.dev Responsive Images: https://web.dev/learn/design/responsive-images
- MDN Container Queries: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_queries
- Every Layout (Heydon Pickering, Andy Bell): https://every-layout.dev
- Utopia Fluid Typography: https://utopia.fyi
- Apple HIG Layout: https://developer.apple.com/design/human-interface-guidelines/layout
- Material Design Responsive Layout: https://m3.material.io/foundations/layout/applying-layout/window-size-classes
