---
name: web-ui
description: Modern web design systems, Component-Level Container Queries (@container), CSS View Transitions API, OKLCH perceptual color spaces, fluid clamp() typography curves, and single-zenith sub-pixel lighting craftsmanship.
---

# Modern Web Design Systems & Responsive Engineering

The `web-ui` skill establishes modern engineering standards for responsive, fluid, and visually pristine web applications. It replaces outdated viewport-only media queries, abrupt DOM redraws, and inconsistent sRGB/HSL color calculations with Component-Level Container Queries, the CSS View Transitions API, mathematically uniform OKLCH palettes, and fluid `clamp()` spatial scaling.

---

## 1. Quick Navigation & Progressive Disclosure

| Resource Type | Document | Description |
| :--- | :--- | :--- |
| **Reference** | [references/container-queries-guide.md](references/container-queries-guide.md) | Component container context declarations, `@container` queries, Tailwind v4 `@container`. |
| **Reference** | [references/oklch-and-fluid-typography.md](references/oklch-and-fluid-typography.md) | Human perceptual OKLCH color spaces, fluid clamp() typography and spacing curves. |
| **Utility** | [scripts/verify_web_ui_hygiene.py](scripts/verify_web_ui_hygiene.py) | Audits web stylesheets for viewport-only media query reliance, stepped fonts, and sRGB/HSL clashing. |

---

## 2. Component-Level Container Queries (`@container`)

Decouple component styling from the global viewport. A component must adapt based on the size of its immediate parent container (e.g. sidebar, grid column, modal pane), not the browser window:

```css
/* Container Context Declaration */
.card-wrapper {
  container-type: inline-size;
  container-name: feed-card;
}

/* Component Rules Anchored to Container */
@container feed-card (min-width: 480px) {
  .card {
    display: grid;
    grid-template-columns: 180px 1fr;
    gap: 1.5rem;
    padding: 1.5rem;
  }
}

@container feed-card (max-width: 479px) {
  .card {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
  }
}
```

### Prohibited Anti-Pattern
- **Viewport Rigidity**: Never hardcode card internal layouts to `@media (min-width: 768px)` when the card is placed inside dynamic columns or resizable sidebars.

---

## 2. CSS View Transitions API (`startViewTransition`)

Eliminate harsh layout jumps and flash-of-unstyled-content during route or state transitions:

```typescript
// Progressive Enhancement View Transition Handler
export function navigateWithTransition(updateDomFn: () => void | Promise<void>) {
  if (!document.startViewTransition) {
    updateDomFn();
    return;
  }

  document.startViewTransition(async () => {
    await updateDomFn();
  });
}
```

### Named Transition Elements
```css
/* Morph specific persistent elements (heroes, active tabs, avatars) */
.hero-image {
  view-transition-name: active-hero-image;
}

::view-transition-old(active-hero-image),
::view-transition-new(active-hero-image) {
  animation-duration: 280ms;
  animation-timing-function: cubic-bezier(0.16, 1, 0.3, 1); /* Apple-like exponential decay */
}
```

---

## 3. OKLCH Perceptual Color Spaces

Traditional `rgb()` and `hsl()` distort perceptual brightness: yellow at lightness 50% appears blindingly bright while blue at lightness 50% appears dark. SkillBuilder mandates the **OKLCH** color space for all semantic color tokens:

```css
:root {
  /* OKLCH: oklch(Lightness Chroma Hue / Alpha) */
  --color-canvas-base: oklch(0.14 0.01 260);
  --color-surface-subtle: oklch(0.18 0.015 260);
  --color-surface-elevated: oklch(0.24 0.02 260);
  --color-accent: oklch(0.68 0.18 245);
  --color-accent-subtle: oklch(0.68 0.18 245 / 0.12);
  --color-text-primary: oklch(0.96 0.005 260);
  --color-text-secondary: oklch(0.72 0.01 260);
  --color-border-subtle: oklch(0.32 0.01 260 / 0.4);
}
```

### Dynamic Tints via `color-mix()`
Derive state overlays predictably without guessing arbitrary hex codes:
```css
.card:hover {
  background-color: color-mix(in oklch, var(--color-surface-elevated), white 4%);
}
```

---

## 4. Fluid Typography & Spatial Layout with `clamp()`

Prohibit step-ladder media queries that abruptly jump text sizes across viewport breakpoints. Use smooth mathematical scaling curves:

```css
:root {
  /* Fluid Typography: clamp(MIN, PREFERRED, MAX) */
  --font-fluid-sm: clamp(0.8125rem, 0.78rem + 0.16vw, 0.875rem);
  --font-fluid-base: clamp(0.9375rem, 0.88rem + 0.28vw, 1.0625rem);
  --font-fluid-lg: clamp(1.125rem, 1.02rem + 0.52vw, 1.375rem);
  --font-fluid-xl: clamp(1.5rem, 1.25rem + 1.25vw, 2.25rem);
  --font-fluid-hero: clamp(2.25rem, 1.6rem + 3.25vw, 4.5rem);

  /* Fluid Spacing */
  --space-gutter: clamp(1rem, 0.8rem + 1vw, 2.5rem);
}
```

---

## 5. Single-Zenith Sub-Pixel Lighting & Depth

Render UI cards with physical depth and optical grounding:
- **Top Specular Hairline**: A subtle top inset border representing natural overhead directional light.
- **Dual-Layer Shadows**: Separate ambient atmospheric occlusion from directional key light.

```css
.elevated-card {
  background: var(--color-surface-elevated);
  border: 1px solid var(--color-border-subtle);
  border-radius: 16px;
  box-shadow:
    inset 0 1px 0 0 rgba(255, 255, 255, 0.08), /* Single-zenith top specular hairline */
    0 1px 2px 0 rgba(0, 0, 0, 0.24),           /* Ambient contact shadow */
    0 8px 24px -4px rgba(0, 0, 0, 0.42);        /* Key directional shadow */
}
```

---

## 6. Accessible Focus States & Tap Target Budget

- **Accessible Focus Rings**: Never suppress outline without an explicit replacement:
  ```css
  :focus-visible {
    outline: 2px solid var(--color-accent);
    outline-offset: 2px;
  }
  ```
- **Minimum Interactive Bounds**: Minimum `44x44px` clickable bounding box on all touch and pointer controls.
