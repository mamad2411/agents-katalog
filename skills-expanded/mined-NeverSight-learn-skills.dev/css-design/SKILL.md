---
name: css-design
description: Expert-level CSS development covering modern layout (flexbox, grid, subgrid, container queries), CSS nesting, pseudo-classes and pseudo-elements, transforms, translations, keyframe animations, complex animation sequencing, WCAG-compliant accessible styling, design tokens, modern color functions, and striking visual design strategies. Use when asked to (1) write, debug, or architect CSS, (2) implement layouts with flexbox, grid, subgrid, or container queries, (3) create animations, transitions, transforms, or animation sequences, (4) apply CSS nesting or modern selectors, (5) ensure WCAG-compliant styling and accessible visual design, (6) implement responsive or fluid design, (7) create visual effects like gradients, glassmorphism, textures, or layered compositions, or when phrases like "style", "CSS", "stylesheet", "design", "layout", "animation", "transform", "keyframe", "nesting", "pseudo", "accessible", "WCAG" appear.
---

# Expert CSS Development

Write modern, performant, maintainable, and accessible CSS following current best practices with deep knowledge of the CSS specification, browser compatibility, WCAG guidelines, and visual design craft.

## Documentation Lookup with context7

**IMPORTANT**: When you need to look up CSS properties, syntax, browser compatibility, or spec details, use the context7 MCP tool to query MDN and other documentation sources.

### How to use context7 for CSS

```bash
# Look up CSS properties
context7 "CSS flexbox properties"
context7 "CSS grid-template-areas syntax"
context7 "CSS custom properties inheritance"

# Check browser compatibility
context7 "CSS container queries browser support"
context7 "CSS :has() selector compatibility"

# Find best practices
context7 "CSS performance optimization"
context7 "CSS naming conventions BEM"

# Explore modern features
context7 "CSS cascade layers @layer"
context7 "CSS subgrid"
context7 "CSS color-mix function"
```

**Use context7 whenever**:
- You're unsure about exact syntax or property values
- You need to verify browser support for a feature
- You want to find the most current best practices
- You're working with cutting-edge CSS features
- You need to understand spec details or edge cases

## Core Principles

1. **Accessible by default** — Every visual decision must meet WCAG AA. Contrast, focus, motion, and readability are not afterthoughts — they are constraints that shape the design.
2. **Mobile-first responsive design** — Start with mobile layout with fluid scaling, enhance for larger viewports.
3. **Progressive enhancement** — Core functionality works everywhere; layer modern features with `@supports`.
4. **Cascade and specificity mastery** — Understand and leverage `@layer`, `:where()`, `:is()`, and nesting — don't fight the cascade.
5. **Performance-driven** — Only animate composite properties (`transform`, `opacity`). Use `contain`, `content-visibility`, and `will-change` deliberately.
6. **Intentional visual craft** — Every value has a reason. No default-looking output. Design tokens, cohesive color systems, and purposeful typography.

## Modern Layout Techniques

### Flexbox for One-Dimensional Layouts

```css
/* Common flex patterns */
.container {
  display: flex;
  gap: 1rem; /* Prefer gap over margins for spacing */
}

/* Center content */
.centered {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Responsive flex wrapping */
.flex-wrap {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.flex-wrap > * {
  flex: 1 1 300px; /* Grow, shrink, basis */
}

/* Common flex utilities */
.flex-1 { flex: 1; }
.flex-none { flex: none; }
.flex-auto { flex: auto; }
```

### Grid for Two-Dimensional Layouts

```css
/* Responsive grid with auto-fit */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

/* Named grid areas for semantic layouts */
.layout {
  display: grid;
  grid-template-areas:
    "header header"
    "sidebar main"
    "footer footer";
  grid-template-columns: 250px 1fr;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
}

.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main { grid-area: main; }
.footer { grid-area: footer; }

/* Dense packing for masonry-like layouts */
.masonry {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  grid-auto-flow: dense;
  gap: 1rem;
}
```

### Subgrid — Inherited Track Sizing

Subgrid lets children align to a parent grid's tracks, solving the "cards with different height content" problem:

```css
/* Parent defines the column tracks */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

/* Each card inherits parent row tracks — all titles, bodies, and footers align */
.card {
  display: grid;
  grid-row: span 3;  /* Occupy 3 row tracks */
  grid-template-rows: subgrid;
  gap: 0;
}

/* Subgrid for sidebar + content alignment */
.layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  grid-template-rows: auto 1fr auto;
}

.sidebar {
  grid-row: 1 / -1;
  display: grid;
  grid-template-rows: subgrid; /* Sidebar rows match main rows */
}
```

### Advanced Flexbox Patterns

```css
/* Holy Grail — sticky footer without min-height hacks */
body {
  display: flex;
  flex-direction: column;
  min-height: 100dvh; /* Dynamic viewport height for mobile browsers */
}

main {
  flex: 1; /* Grows to fill available space, footer stays at bottom */
}

/* Intrinsic sizing — let content decide */
.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;

  & > * {
    flex: 0 1 auto; /* Don't grow, shrink if needed, size to content */
  }
}

/* Equal-height columns regardless of content */
.features {
  display: flex;
  gap: 2rem;

  & > * {
    flex: 1;           /* Equal widths */
    display: flex;
    flex-direction: column;
  }

  & > * > :last-child {
    margin-top: auto;  /* Push last element (e.g., CTA) to bottom */
  }
}
```

### Container Queries (Modern Alternative to Media Queries)

```css
/* Container query setup */
.card-container {
  container-type: inline-size;
  container-name: card;
}

/* Query the container, not the viewport */
@container card (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 150px 1fr;
  }
}

@container card (min-width: 600px) {
  .card {
    grid-template-columns: 200px 1fr;
  }
}
```

## Modern CSS Features

### Custom Properties (CSS Variables)

```css
:root {
  /* Color system */
  --color-primary: #0066cc;
  --color-primary-dark: #004499;
  --color-surface: #ffffff;
  --color-text: #1a1a1a;
  
  /* Spacing scale */
  --space-xs: 0.25rem;
  --space-sm: 0.5rem;
  --space-md: 1rem;
  --space-lg: 2rem;
  --space-xl: 4rem;
  
  /* Typography */
  --font-sans: system-ui, -apple-system, sans-serif;
  --font-mono: 'Fira Code', monospace;
  
  /* Dark mode using data attribute */
  --bg: var(--color-surface);
  --fg: var(--color-text);
}

[data-theme="dark"] {
  --color-surface: #1a1a1a;
  --color-text: #e5e5e5;
}

/* Using custom properties */
.button {
  background: var(--color-primary);
  padding: var(--space-sm) var(--space-md);
  font-family: var(--font-sans);
}
```

### Cascade Layers (@layer)

```css
/* Define layer order - lowest specificity first */
@layer reset, base, components, utilities;

@layer reset {
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
}

@layer base {
  body {
    font-family: system-ui, sans-serif;
    line-height: 1.5;
  }
}

@layer components {
  .button {
    padding: 0.5rem 1rem;
    border-radius: 0.25rem;
  }
}

@layer utilities {
  .text-center { text-align: center; }
  .hidden { display: none; }
}
```

### Modern Selectors

```css
/* :is() for grouping (no specificity increase) */
:is(h1, h2, h3) {
  font-weight: 700;
  line-height: 1.2;
}

/* :where() for zero specificity */
:where(.card, .panel) > :where(h2, h3) {
  margin-top: 0;
}

/* :has() for parent selection */
.card:has(img) {
  display: grid;
  grid-template-columns: 200px 1fr;
}

.form:has(:invalid) .submit-button {
  opacity: 0.5;
  pointer-events: none;
}

/* Logical properties for internationalization */
.element {
  margin-inline-start: 1rem; /* Instead of margin-left */
  padding-block: 2rem; /* Instead of padding-top and padding-bottom */
  border-inline-end: 1px solid; /* Instead of border-right */
}
```

## Native CSS Nesting

Use native nesting for component-scoped styles. Nesting reduces repetition and makes the cascade explicit.

### Basic Nesting with `&`

```css
.card {
  background: var(--color-surface);
  border-radius: var(--radius-md);
  overflow: hidden;

  /* Nested element — compiles to .card .card__header */
  & .card__header {
    padding: var(--space-4) var(--space-6);
    border-bottom: 1px solid var(--color-border);
  }

  & .card__body {
    padding: var(--space-6);
  }

  /* Modifier — compiles to .card.card--featured */
  &.card--featured {
    border: 2px solid var(--color-accent);
    box-shadow: var(--shadow-lg);
  }

  /* State — compiles to .card:hover */
  &:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
  }

  /* Media query nesting */
  @media (min-width: 768px) {
    display: grid;
    grid-template-columns: 240px 1fr;

    & .card__header {
      grid-column: 1 / -1;
    }
  }
}
```

### Nesting Pseudo-elements and States

```css
.button {
  position: relative;
  padding: var(--space-3) var(--space-6);
  background: var(--color-primary);
  color: var(--color-on-primary);
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  overflow: hidden;

  /* Hover */
  &:hover {
    background: var(--color-primary-dark);
  }

  /* Focus — WCAG 2.4.12 compliant */
  &:focus-visible {
    outline: 3px solid var(--color-focus);
    outline-offset: 2px;
  }

  /* Active press effect */
  &:active {
    transform: scale(0.97);
  }

  /* Disabled state */
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    pointer-events: none;
  }

  /* Ripple pseudo-element */
  &::after {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(circle, rgba(255,255,255,0.3) 10%, transparent 10%);
    background-size: 200% 200%;
    background-position: center;
    opacity: 0;
    transition: opacity 0.3s;
  }

  &:active::after {
    opacity: 1;
    background-size: 100% 100%;
  }
}
```

### Deep Nesting with Container Queries

```css
.product-card {
  container-type: inline-size;
  container-name: product;

  & .product-card__image {
    aspect-ratio: 1;
    object-fit: cover;
  }

  & .product-card__details {
    padding: var(--space-4);

    & h3 {
      font-size: var(--text-lg);
      margin-bottom: var(--space-2);
    }

    & .price {
      font-weight: 700;
      color: var(--color-accent);
    }
  }

  @container product (min-width: 400px) {
    display: grid;
    grid-template-columns: 180px 1fr;

    & .product-card__image {
      aspect-ratio: 3 / 4;
    }
  }
}
```

## Modern Pseudo-classes & Pseudo-elements

### Structural Pseudo-classes

```css
/* Select items without class-based overrides */
.list > li {
  border-bottom: 1px solid var(--color-border);

  &:last-child {
    border-bottom: none;
  }

  /* Alternating backgrounds */
  &:nth-child(even) {
    background: var(--color-surface-alt);
  }

  /* First N items (e.g., top 3 results) */
  &:nth-child(-n + 3) {
    font-weight: 600;
  }

  /* Every 3rd item starting at 2nd */
  &:nth-child(3n + 2) {
    accent-color: var(--color-accent);
  }

  /* Only child — no siblings */
  &:only-child {
    text-align: center;
    border-bottom: none;
  }

  /* Empty elements */
  &:empty {
    display: none;
  }
}
```

### Functional Pseudo-classes

```css
/* :is() — matches any in the list, takes highest specificity of the list */
:is(h1, h2, h3, h4) {
  font-family: var(--font-display);
  line-height: var(--leading-tight);
  text-wrap: balance;
}

/* :where() — same as :is() but zero specificity (easy to override) */
:where(article, section, aside) > :where(h2, h3) {
  margin-top: 0;
}

/* :has() — parent selector (the most powerful modern pseudo-class) */
.card:has(img) {
  display: grid;
  grid-template-columns: 200px 1fr;
}

.form-group:has(:invalid) {
  --border-color: var(--color-error);

  & .form-group__message {
    color: var(--color-error);
    display: block;
  }
}

/* :has() for layout control — sidebar detection */
main:has(+ aside) {
  grid-template-columns: 1fr 300px;
}

main:not(:has(+ aside)) {
  grid-template-columns: 1fr;
}

/* :not() — exclusion selectors */
.nav-link:not([aria-current="page"]) {
  opacity: 0.8;
}

button:not(:disabled):hover {
  background: var(--color-primary-dark);
}
```

### Form Pseudo-classes

```css
.input {
  border: 2px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: var(--space-3);
  transition: border-color 0.2s ease;

  &:focus-visible {
    outline: 3px solid var(--color-focus);
    outline-offset: 2px;
    border-color: var(--color-primary);
  }

  &:valid {
    border-color: var(--color-success);
  }

  &:invalid:not(:placeholder-shown) {
    /* Only show error after user interaction */
    border-color: var(--color-error);
  }

  &::placeholder {
    color: var(--color-text-muted);
    opacity: 1; /* Firefox fix */
  }

  &:required::after {
    content: " *";
    color: var(--color-error);
  }

  &:read-only {
    background: var(--color-surface-alt);
    cursor: default;
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
}
```

### Pseudo-elements for Visual Decoration

```css
/* Decorative line accent */
.section-title {
  position: relative;
  display: inline-block;

  &::after {
    content: "";
    position: absolute;
    bottom: -4px;
    left: 0;
    width: 60%;
    height: 3px;
    background: var(--color-accent);
    border-radius: 2px;
  }
}

/* Custom bullet points */
.features li {
  list-style: none;
  padding-left: var(--space-6);
  position: relative;

  &::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0.5em;
    width: 8px;
    height: 8px;
    background: var(--color-accent);
    border-radius: 50%;
  }
}

/* Overlay for hover effects */
.media-card {
  position: relative;

  &::before {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(to top, rgba(0,0,0,0.7) 0%, transparent 50%);
    opacity: 0;
    transition: opacity 0.3s ease;
    z-index: 1;
  }

  &:hover::before {
    opacity: 1;
  }
}
```

## Transforms, Animations & Motion Design

For comprehensive animation theory, sequencing strategies, and advanced techniques,
  see the animation-specialist skill. This section covers CSS animation mechanics;
  animation-specialist provides deeper choreography and motion design principles.

### CSS Transforms — The Foundation

Transforms are GPU-accelerated and don't trigger layout or paint. They are the primary tool for performant visual motion.

```css
/* 2D Transforms — translate, rotate, scale, skew */
.element {
  /* Individual transform properties (modern — easier to animate independently) */
  translate: 0 -8px;
  rotate: 3deg;
  scale: 1.05;
}

/* Combined transform function (wide support) */
.element-classic {
  transform: translateY(-8px) rotate(3deg) scale(1.05);
}

/* Transform origin controls the pivot point */
.door {
  transform-origin: left center;
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);

  &:hover {
    transform: perspective(800px) rotateY(-25deg);
  }
}

/* 3D Transforms */
.scene {
  perspective: 1000px;           /* Creates depth for child elements */
  perspective-origin: center;
}

.card-3d {
  transform-style: preserve-3d;  /* Children exist in 3D space */
  transition: transform 0.6s ease;

  &:hover {
    transform: rotateY(15deg) rotateX(-5deg);
  }

  /* Card back face */
  & .back {
    transform: rotateY(180deg);
    backface-visibility: hidden;
    position: absolute;
    inset: 0;
  }
}
```

### Transitions — State-to-State Motion

```css
/* Transition only compositor-friendly properties for 60fps */
.button {
  background: var(--color-primary);
  color: var(--color-on-primary);
  border-radius: var(--radius-sm);
  
  /* ✅ Only transform + opacity — GPU optimized */
  transition:
    transform 0.2s cubic-bezier(0.4, 0, 0.2, 1),
    opacity 0.2s ease,
    box-shadow 0.2s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
  }

  &:active {
    transform: translateY(0) scale(0.97);
    transition-duration: 0.1s;  /* Faster snap on press */
  }
}

/* Staggered transitions on child elements */
.nav-list > li {
  opacity: 0;
  transform: translateX(-12px);
  transition:
    opacity 0.3s ease,
    transform 0.3s ease;

  /* Each item delays slightly more than the last */
  &:nth-child(1) { transition-delay: 0.05s; }
  &:nth-child(2) { transition-delay: 0.10s; }
  &:nth-child(3) { transition-delay: 0.15s; }
  &:nth-child(4) { transition-delay: 0.20s; }
  &:nth-child(5) { transition-delay: 0.25s; }
}

.nav-list.is-open > li {
  opacity: 1;
  transform: translateX(0);
}
```

### Easing Functions — The Key to Natural Motion

```css
:root {
  /* Named easings for consistent motion language */
  --ease-out: cubic-bezier(0.0, 0.0, 0.2, 1);        /* Decelerating — entering */
  --ease-in: cubic-bezier(0.4, 0.0, 1, 1);            /* Accelerating — exiting */
  --ease-in-out: cubic-bezier(0.4, 0.0, 0.2, 1);      /* Standard — moving */
  --ease-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);   /* Overshoot — playful */
  --ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275); /* Spring — elastic snap */
  --ease-smooth: cubic-bezier(0.45, 0, 0.55, 1);      /* Smooth sine — subtle */

  /* Duration scale */
  --duration-instant: 100ms;
  --duration-fast: 200ms;
  --duration-normal: 300ms;
  --duration-slow: 500ms;
  --duration-slower: 800ms;
}

/* Use ease-out for enter, ease-in for exit */
.modal {
  &.entering {
    animation: fadeScaleIn 0.3s var(--ease-out) both;
  }

  &.exiting {
    animation: fadeScaleOut 0.2s var(--ease-in) both;
  }
}

/* Spring easing for interactive feedback */
.toggle {
  transition: transform 0.4s var(--ease-spring);

  &:active {
    transform: scale(0.9);
  }
}
```

### Keyframe Animations — Complex Motion

```css
/* Multi-step entrance with personality */
@keyframes slideUpFadeIn {
  0% {
    opacity: 0;
    transform: translateY(30px) scale(0.96);
    filter: blur(4px);
  }
  60% {
    opacity: 1;
    filter: blur(0px);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
    filter: blur(0px);
  }
}

/* Breathing glow — subtle ambient motion */
@keyframes breathe {
  0%, 100% {
    box-shadow: 0 0 20px rgba(59, 91, 219, 0.15);
  }
  50% {
    box-shadow: 0 0 40px rgba(59, 91, 219, 0.35);
  }
}

/* Typewriter cursor blink */
@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

.cursor {
  animation: blink 1s step-end infinite;
}

/* Skeleton loading shimmer */
@keyframes shimmer {
  0% {
    background-position: -200% 0;
  }
  100% {
    background-position: 200% 0;
  }
}

.skeleton {
  background: linear-gradient(
    90deg,
    var(--color-surface-alt) 25%,
    var(--color-surface) 37%,
    var(--color-surface-alt) 63%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s ease-in-out infinite;
  border-radius: var(--radius-sm);
}

/* Elastic bounce entrance */
@keyframes bounceIn {
  0% {
    opacity: 0;
    transform: scale(0.3);
  }
  50% {
    opacity: 1;
    transform: scale(1.05);
  }
  70% {
    transform: scale(0.95);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}
```

### Complex Animation Sequences — Orchestration

Coordinate multiple animations to create choreographed motion:

```css
/* Staggered card entrance — each card enters in sequence */
.card-grid > .card {
  opacity: 0;
  animation: slideUpFadeIn 0.5s var(--ease-out) both;

  /* CSS custom properties for dynamic stagger */
  animation-delay: calc(var(--i, 0) * 80ms);
}

/* Set stagger index via inline style: style="--i: 0", style="--i: 1", etc. */
/* Or with nth-child for static grids: */
.card-grid > .card:nth-child(1) { --i: 0; }
.card-grid > .card:nth-child(2) { --i: 1; }
.card-grid > .card:nth-child(3) { --i: 2; }
.card-grid > .card:nth-child(4) { --i: 3; }
.card-grid > .card:nth-child(5) { --i: 4; }
.card-grid > .card:nth-child(6) { --i: 5; }

/* Hero section — sequenced entrance of multiple elements */
@keyframes heroTitle {
  from { opacity: 0; transform: translateY(40px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes heroSubtitle {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes heroCTA {
  from { opacity: 0; transform: translateY(16px) scale(0.95); }
  to   { opacity: 1; transform: translateY(0) scale(1); }
}

@keyframes heroDivider {
  from { transform: scaleX(0); }
  to   { transform: scaleX(1); }
}

.hero {
  & h1 {
    opacity: 0;
    animation: heroTitle 0.7s var(--ease-out) 0.1s both;
  }

  & .divider {
    transform-origin: left;
    animation: heroDivider 0.5s var(--ease-out) 0.4s both;
  }

  & p {
    opacity: 0;
    animation: heroSubtitle 0.5s var(--ease-out) 0.6s both;
  }

  & .cta {
    opacity: 0;
    animation: heroCTA 0.5s var(--ease-spring) 0.9s both;
  }
}

/* Sequenced list reveal with stagger */
@keyframes listItemIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.feature-list > li {
  animation: listItemIn 0.4s var(--ease-out) both;
  animation-delay: calc(0.15s + var(--i, 0) * 0.08s);
}
```

### Scroll-Driven Animations

```css
/* Scroll progress indicator */
@keyframes scrollProgress {
  from { transform: scaleX(0); }
  to   { transform: scaleX(1); }
}

.progress-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--color-accent);
  transform-origin: left;
  animation: scrollProgress linear;
  animation-timeline: scroll(root);
}

/* Fade in as element enters viewport */
@keyframes scrollFadeIn {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.scroll-reveal {
  animation: scrollFadeIn ease-out both;
  animation-timeline: view();
  animation-range: entry 10% cover 40%;
}

/* Parallax effect via scroll timeline */
@keyframes parallax {
  from { transform: translateY(-50px); }
  to   { transform: translateY(50px); }
}

.parallax-bg {
  animation: parallax linear;
  animation-timeline: scroll();
}
```

### View Transitions API

```css
/* Smooth page transitions */
::view-transition-old(root),
::view-transition-new(root) {
  animation-duration: 0.3s;
}

/* Named element transitions — shared element animation */
.hero-image {
  view-transition-name: hero;
}

::view-transition-old(hero) {
  animation: fadeOut 0.3s var(--ease-in) both;
}

::view-transition-new(hero) {
  animation: fadeIn 0.3s var(--ease-out) both;
}
```

### Animation Performance Rules

1. **Only animate `transform` and `opacity`** — these are compositor-only properties (no layout/paint)
2. **Use `will-change` sparingly** — only on elements about to animate, remove after
3. **Prefer `animation-fill-mode: both`** — holds initial and final states
4. **Use `contain: layout style paint`** on animated containers to limit browser work
5. **Always wrap in `prefers-reduced-motion: no-preference`** — animations are enhancement, not content

## Responsive Design Patterns

### Modern Media Query Strategy

```css
/* Mobile-first approach */
.component {
  /* Base mobile styles */
  padding: 1rem;
}

/* Tablet */
@media (min-width: 768px) {
  .component {
    padding: 2rem;
  }
}

/* Desktop */
@media (min-width: 1024px) {
  .component {
    padding: 3rem;
  }
}

/* Wide desktop */
@media (min-width: 1440px) {
  .component {
    padding: 4rem;
  }
}

/* Prefer reduced motion */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* Dark mode preference */
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #1a1a1a;
    --fg: #e5e5e5;
  }
}
```

### Fluid Typography

```css
/* Clamp for responsive font sizes */
h1 {
  font-size: clamp(2rem, 4vw + 1rem, 4rem);
}

body {
  font-size: clamp(1rem, 0.5vw + 0.875rem, 1.125rem);
}

/* Or using custom properties */
:root {
  --fluid-min-width: 320;
  --fluid-max-width: 1140;
  --fluid-min-size: 16;
  --fluid-max-size: 20;
  
  --fluid-size: calc(
    (var(--fluid-min-size) * 1px) +
    (var(--fluid-max-size) - var(--fluid-min-size)) *
    ((100vw - (var(--fluid-min-width) * 1px)) /
    (var(--fluid-max-width) - var(--fluid-min-width)))
  );
}

body {
  font-size: clamp(
    var(--fluid-min-size) * 1px,
    var(--fluid-size),
    var(--fluid-max-size) * 1px
  );
}
```

## Performance Optimization

### Critical Performance Rules

```css
/* 1. Avoid expensive properties */
.avoid {
  box-shadow: ...; /* OK, GPU accelerated */
  filter: ...; /* Expensive, use sparingly */
}

/* 2. Use containment for isolated components */
.card {
  contain: layout style paint;
  /* Tells browser this element's styles won't affect others */
}

.isolated-component {
  content-visibility: auto; /* Skip rendering offscreen elements */
}

/* 3. Optimize selectors - specificity vs performance */
/* Fast ✅ */
.button { }
.nav-item { }

/* Slower ❌ */
div.container ul li a.link { }
[class*="btn-"] { }
```

### CSS Loading Strategies

```html
<!-- Critical CSS inline in <head> -->
<style>
  /* Above-the-fold styles */
</style>

<!-- Non-critical CSS with media query trick -->
<link rel="stylesheet" href="styles.css" media="print" onload="this.media='all'">

<!-- Preload for faster loading -->
<link rel="preload" href="fonts.woff2" as="font" type="font/woff2" crossorigin>
```

## Problem Solving & Debugging

Three techniques that resolve the most common CSS headaches:

**Stacking context confusion** — instead of hacking `z-index`, create an isolated stacking context:
```css
.modal-wrapper {
  isolation: isolate; /* New stacking context — z-index battles stay contained inside */
}
```

**Specificity wars** — use `@layer` to define explicit priority groups rather than escalating specificity:
```css
@layer reset, base, components, utilities;

/* Anything in `utilities` always wins, regardless of selector specificity */
@layer utilities {
  .hidden { display: none; }
}
```

**Layout overflow** — when something is breaking the viewport width, find it fast:
```css
* { outline: 1px solid red; }
```
This outlines every element without affecting layout (unlike `border`). Scan visually for the element that bleeds past the edge, then remove the rule.

## Naming Conventions and Organization

### BEM (Block Element Modifier)

```css
/* Block */
.card { }

/* Element - part of block */
.card__title { }
.card__body { }
.card__footer { }

/* Modifier - variation of block */
.card--featured { }
.card--large { }
.card__title--primary { }
```

### Utility-First (Tailwind-style)

```css
/* Spacing utilities */
.p-4 { padding: 1rem; }
.px-4 { padding-left: 1rem; padding-right: 1rem; }
.mt-2 { margin-top: 0.5rem; }

/* Layout utilities */
.flex { display: flex; }
.grid { display: grid; }
.hidden { display: none; }

/* Typography utilities */
.text-lg { font-size: 1.125rem; }
.font-bold { font-weight: 700; }
.text-center { text-align: center; }
```

### File Organization

```
styles/
├── base/
│   ├── reset.css
│   ├── typography.css
│   └── utilities.css
├── components/
│   ├── button.css
│   ├── card.css
│   └── nav.css
├── layout/
│   ├── grid.css
│   ├── header.css
│   └── footer.css
├── themes/
│   ├── light.css
│   └── dark.css
└── main.css (imports all)
```

## Modern Color Functions

```css
:root {
  /* Modern color functions */
  --primary: oklch(60% 0.2 250); /* Perceptually uniform */
  --surface: color-mix(in oklch, var(--primary) 10%, white);
  
  /* Relative colors */
  --primary-light: oklch(from var(--primary) calc(l + 20%) c h);
  --primary-dark: oklch(from var(--primary) calc(l - 20%) c h);
  
  /* Color contrast for accessibility */
  --text-color: color-contrast(
    var(--surface) vs black, white
  );
}
```

## SVG Styling

Use CSS to style and animate inline SVGs and SVG elements embedded in HTML. Targeting SVG segments via classes gives you hover states, drawn stroke animations, and filter effects — all without JavaScript.

```css
/* currentColor — makes icons theme-aware by inheriting the text color */
.icon {
  fill: currentColor;
  width: 1.5em;
  height: 1.5em;
}

/* Target individual SVG paths/shapes by class */
.logo-mark .primary-path {
  fill: var(--color-primary);
  transition: fill 0.3s ease;
}

.logo-mark:hover .primary-path {
  fill: var(--color-primary-dark);
}

/* Stroke draw animation — set pathLength="1" in HTML to normalize distances */
@keyframes drawStroke {
  from { stroke-dashoffset: 1; }
  to   { stroke-dashoffset: 0; }
}

.animated-path {
  stroke: currentColor;
  fill: none;
  stroke-width: 2;
  stroke-dasharray: 1;
  stroke-dashoffset: 1;
  vector-effect: non-scaling-stroke; /* consistent stroke width at any scale */
  animation: drawStroke 1s var(--ease-out) forwards;
}

/* drop-shadow respects SVG alpha channel — box-shadow does not */
.icon:hover {
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
}

/* Interactive SVG button — CSS nesting + custom property for timing */
.btn {
  --icon-speed: 0.3s;
  display: flex;
  align-items: center;
  gap: 0.5rem;

  & svg {
    transition: transform var(--icon-speed) ease;
    fill: currentColor;
  }

  &:hover svg {
    transform: rotate(15deg) scale(1.1);
  }
}
```

**Key patterns:**
- Use `currentColor` for fills that automatically follow the element's `color` — no extra variables needed
- Avoid inline `fill` attributes on SVG shapes — CSS can't override them without `!important`
- Use `vector-effect: non-scaling-stroke` to keep stroke widths consistent when the SVG scales
- Use `filter: drop-shadow()` rather than `box-shadow` on SVGs — it follows the shape's alpha channel
- Set `pathLength="1"` on SVG `<path>` elements to normalize `stroke-dasharray` distances to 0–1

## Browser Compatibility Strategies

### Feature Queries (@supports)

```css
/* Fallback for older browsers */
.grid {
  display: flex;
  flex-wrap: wrap;
}

/* Enhanced for modern browsers */
@supports (display: grid) {
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  }
}

/* Progressive enhancement */
.button {
  background: blue;
}

@supports (backdrop-filter: blur(10px)) {
  .button {
    background: rgba(0, 0, 255, 0.8);
    backdrop-filter: blur(10px);
  }
}
```

## Visual Design Strategies

Modern CSS enables striking visual presentations without images or JavaScript. Use these techniques deliberately — every effect should reinforce the design, not decorate it.

### Gradient Compositions

```css
/* Multi-stop gradient with intentional color stops */
.hero-gradient {
  background:
    linear-gradient(
      135deg,
      oklch(25% 0.05 260) 0%,
      oklch(30% 0.12 280) 35%,
      oklch(20% 0.08 310) 100%
    );
  color: white;
}

/* Mesh-like gradient using radial layers */
.mesh-bg {
  background:
    radial-gradient(ellipse at 20% 50%, oklch(60% 0.2 250 / 0.4), transparent 50%),
    radial-gradient(ellipse at 80% 20%, oklch(65% 0.18 330 / 0.3), transparent 50%),
    radial-gradient(ellipse at 50% 80%, oklch(55% 0.15 150 / 0.3), transparent 50%),
    oklch(15% 0.02 260);
}

/* Gradient text */
.gradient-text {
  background: linear-gradient(135deg, var(--color-primary), var(--color-accent));
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
}

/* Animated gradient border */
@property --angle {
  syntax: "<angle>";
  initial-value: 0deg;
  inherits: false;
}

.gradient-border {
  border: 2px solid transparent;
  background:
    linear-gradient(var(--color-surface), var(--color-surface)) padding-box,
    conic-gradient(from var(--angle), var(--color-primary), var(--color-accent), var(--color-primary)) border-box;
  animation: rotateBorder 3s linear infinite;
}

@keyframes rotateBorder {
  to { --angle: 360deg; }
}
```

### Glassmorphism & Frosted Effects

```css
.glass-panel {
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(16px) saturate(180%);
  -webkit-backdrop-filter: blur(16px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: var(--radius-lg);
  box-shadow:
    0 8px 32px rgba(0, 0, 0, 0.12),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

/* Dark glassmorphism */
.glass-dark {
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(20px) saturate(150%);
  border: 1px solid rgba(255, 255, 255, 0.06);
}
```

### Layered Shadows & Depth

```css
:root {
  /* Shadow elevation scale — each level increases perceived depth */
  --shadow-xs: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.08), 0 1px 2px rgba(0, 0, 0, 0.06);
  --shadow-md:
    0 4px 6px rgba(0, 0, 0, 0.05),
    0 2px 4px rgba(0, 0, 0, 0.06);
  --shadow-lg:
    0 10px 25px rgba(0, 0, 0, 0.07),
    0 6px 10px rgba(0, 0, 0, 0.05),
    0 2px 4px rgba(0, 0, 0, 0.04);
  --shadow-xl:
    0 20px 50px rgba(0, 0, 0, 0.08),
    0 12px 24px rgba(0, 0, 0, 0.06),
    0 4px 8px rgba(0, 0, 0, 0.04);
}

/* Pop-out effect on hover — layered shadow + transform */
.card {
  box-shadow: var(--shadow-sm);
  transition:
    box-shadow 0.3s ease,
    transform 0.3s var(--ease-out);

  &:hover {
    box-shadow: var(--shadow-lg);
    transform: translateY(-4px);
  }
}
```

### Texture & Surface Treatment

```css
/* Subtle noise texture via SVG data URI */
.textured-surface {
  background-color: var(--color-surface);
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
}

/* Dot grid pattern */
.dot-grid {
  background-image: radial-gradient(circle, var(--color-border) 1px, transparent 1px);
  background-size: 24px 24px;
}

/* Subtle line grid */
.line-grid {
  background-image:
    linear-gradient(to right, var(--color-border) 1px, transparent 1px),
    linear-gradient(to bottom, var(--color-border) 1px, transparent 1px);
  background-size: 48px 48px;
}
```

### Clipping, Masking & Shape Effects

```css
/* Diagonal section divider */
.diagonal-section {
  clip-path: polygon(0 0, 100% 4%, 100% 100%, 0 96%);
  padding-block: 6rem;
}

/* Circular image mask */
.avatar-blob {
  clip-path: polygon(50% 0%, 80% 10%, 100% 40%, 95% 75%, 70% 100%, 30% 100%, 5% 75%, 0% 40%, 20% 10%);
}

/* Reveal on scroll with clip-path animation */
@keyframes clipReveal {
  from { clip-path: inset(0 100% 0 0); }
  to   { clip-path: inset(0 0 0 0); }
}

.reveal-line {
  animation: clipReveal 0.8s var(--ease-out) both;
  animation-timeline: view();
  animation-range: entry 20% cover 50%;
}
```

### Typography as Design

```css
/* Large display type with visual weight */
.display-heading {
  font-family: var(--font-display);
  font-size: clamp(3rem, 8vw + 1rem, 8rem);
  font-weight: 800;
  line-height: 0.95;
  letter-spacing: -0.03em;
  text-wrap: balance;
}

/* Outlined / stroke text */
.outlined-text {
  -webkit-text-stroke: 2px var(--color-text);
  color: transparent;
}

/* Mixed weight for editorial feel */
.editorial-heading {
  font-family: var(--font-display);
  font-weight: 300;

  & strong {
    font-weight: 800;
    font-style: italic;
  }
}
```

## Common Patterns and Solutions

### Aspect Ratio

```css
/* Modern way */
.video {
  aspect-ratio: 16 / 9;
}

/* For images */
img {
  aspect-ratio: 16 / 9;
  object-fit: cover;
}
```

### Truncation

```css
/* Single line */
.truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Multiple lines */
.line-clamp {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
```

### Smooth Scrolling

```css
html {
  scroll-behavior: smooth;
}

/* Scroll snapping */
.carousel {
  scroll-snap-type: x mandatory;
  overflow-x: auto;
}

.carousel > * {
  scroll-snap-align: start;
}
```

## WCAG-Compliant Accessible Styling

Accessibility is a **design constraint**, not an afterthought. Every CSS decision must satisfy WCAG 2.2 AA as a minimum.

### Color Contrast (WCAG 1.4.3 / 1.4.6 / 1.4.11)

```css
:root {
  /* Annotate every pairing with its contrast ratio */
  --color-text: #1a1a1a;        /* On white: 16.75:1 — AAA ✅ */
  --color-text-muted: #595959;  /* On white: 7.01:1  — AAA ✅ */
  --color-link: #0053a0;        /* On white: 7.21:1  — AAA ✅ */
  --color-error: #c32b2b;       /* On white: 5.64:1  — AA  ✅ */
  --color-border: #767676;      /* On white: 4.54:1  — AA for non-text (1.4.11) ✅ */
}

/* Non-text contrast — UI components and graphical objects need ≥ 3:1 */
.input {
  border: 2px solid var(--color-border); /* 4.54:1 against white background ✅ */
}

.input:focus {
  outline: 3px solid var(--color-link);  /* 7.21:1 ✅ */
  outline-offset: 2px;
}
```

**Contrast rules:**
| Element | WCAG Level | Minimum Ratio |
|---------|-----------|---------------|
| Normal text (< 18pt) | AA | 4.5:1 |
| Large text (≥ 18pt or ≥ 14pt bold) | AA | 3:1 |
| Normal text | AAA | 7:1 |
| Non-text UI (borders, icons, controls) | AA (1.4.11) | 3:1 |

### Focus Indicators (WCAG 2.4.7 / 2.4.11 / 2.4.12)

```css
/* Global focus style — WCAG 2.4.12 requires ≥ 2px solid outline */
:focus-visible {
  outline: 3px solid var(--color-focus, #0053a0);
  outline-offset: 2px;
  border-radius: 2px;
}

/* Never remove focus outlines — style them instead */
/* ❌ NEVER: *:focus { outline: none; } */

/* Dark backgrounds need inverted focus rings */
.dark-section :focus-visible {
  outline-color: #ffffff;
  box-shadow: 0 0 0 2px #000000; /* Double ring for contrast on any bg */
}

/* Enhanced focus for interactive cards */
.card-link:focus-visible {
  outline: 3px solid var(--color-focus);
  outline-offset: 4px;
  box-shadow: 0 0 0 6px rgba(0, 83, 160, 0.15);
}
```

### Motion & Animation Safety (WCAG 2.3.3 / 2.3.1)

```css
/* Always provide a reduced-motion alternative */
@media (prefers-reduced-motion: no-preference) {
  .animate-in {
    animation: slideInFade 0.4s ease-out both;
  }

  .smooth-hover {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }
}

/* Reduced motion — instant state changes only */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}

/* WCAG 2.3.1 — no flashing content faster than 3Hz */
/* Never create animations that flash more than 3 times per second */
```

### Don't Rely on Color Alone (WCAG 1.4.1)

```css
/* ❌ Color only — fails WCAG 1.4.1 */
.error { color: red; }
.success { color: green; }

/* ✅ Color + shape/icon/text — passes */
.error {
  color: var(--color-error);
  border-left: 4px solid var(--color-error);
  padding-left: var(--space-4);

  &::before {
    content: "⚠ ";  /* Visual indicator beyond color */
  }
}
```

### Touch Targets (WCAG 2.5.8)

```css
/* Minimum 24×24px (AA), prefer 44×44px for comfortable tapping */
.button,
a,
[role="button"],
input,
select {
  min-height: 44px;
  min-width: 44px;
}

/* Inline links in text — use adequate padding instead */
p a {
  padding-block: 0.25em;
  min-width: unset; /* Let text flow naturally */
}
```

### Screen Reader Utilities

```css
/* Hide visually, keep in accessibility tree */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

/* Reveal on focus — for skip links and keyboard-only shortcuts */
.sr-only:focus,
.sr-only:focus-within {
  position: static;
  width: auto;
  height: auto;
  margin: 0;
  overflow: visible;
  clip: auto;
  white-space: normal;
}
```

### High Contrast & User Preferences

```css
/* Forced colors mode — Windows High Contrast */
@media (forced-colors: active) {
  .button {
    border: 2px solid ButtonText;
    /* ButtonText, Canvas, CanvasText, LinkText — forced color keywords */
  }

  /* Ensure custom focus styles survive forced colors */
  :focus-visible {
    outline: 3px solid Highlight;
  }
}

/* High contrast preference */
@media (prefers-contrast: more) {
  :root {
    --color-border: #000000;
    --color-text-muted: #1a1a1a; /* Promote to full contrast */
  }

  .button {
    border: 2px solid currentColor;
    font-weight: 700;
  }
}

/* Typography accessibility minimums */
body {
  font-size: clamp(1rem, 0.5vw + 0.875rem, 1.125rem); /* Never below 16px */
  line-height: 1.5;                                     /* WCAG 1.4.12 */
  letter-spacing: 0.012em;                               /* Adequate spacing */
}

p {
  max-width: 75ch; /* ~75 characters per line for readability */
}
```

## Safety & Anti-Patterns

Avoid these patterns — they cause bugs, maintainability problems, or performance issues:

| Anti-pattern | Problem | Do instead |
|---|---|---|
| `!important` on arbitrary rules | Breaks the cascade; creates escalating specificity debt | Use `@layer` to control priority |
| Fixed heights on containers with text (`height: 200px`) | Text overflows at larger font sizes or zoom levels | Use `min-height` or let content define height |
| `:focus { outline: none; }` globally | Removes keyboard navigation visibility; WCAG failure | Style `:focus-visible` instead |
| Heavy `filter: blur()` or `backdrop-filter` over large mobile areas | Triggers expensive repaint on every frame; kills 60fps on mid-range devices | Limit blurred area size; test on actual mobile hardware |
| Relying on `:visited` for sensitive state | Browsers restrict `:visited` styles to color-only (prevents history sniffing) | Only use color changes; never change layout or content |
| Animating `width`, `height`, `top`, `left`, `margin` | Triggers layout recalculation on every frame | Animate `transform` and `opacity` instead |
| Deep descendant selectors (`div.container ul li a.link`) | Slow matching; tightly coupled to HTML structure | Use single class selectors |

## CSS Reset / Normalize

```css
/* Modern CSS reset */
*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
}

html {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  min-height: 100vh;
  line-height: 1.5;
}

img,
picture,
video,
canvas,
svg {
  display: block;
  max-width: 100%;
}

input,
button,
textarea,
select {
  font: inherit;
}

p,
h1,
h2,
h3,
h4,
h5,
h6 {
  overflow-wrap: break-word;
}
```

## Quick Reference

Key topics covered in this skill:
- Modern layout (flexbox, grid, subgrid, container queries)
- Native CSS nesting and modern pseudo-classes (`:has()`, `:is()`, `:where()`)
- Transforms (2D, 3D, perspective, transform-origin)
- Keyframe animations and complex choreographed sequences
- Scroll-driven animations and view transitions
- Easing functions and motion design tokens
- WCAG-compliant styling (contrast, focus, motion, touch targets, forced colors)
- Visual design strategies (gradients, glassmorphism, textures, clipping, typography)
- Performance optimization (containment, `content-visibility`, compositor-only animations)
- Responsive design (mobile-first, fluid typography, container queries)
- Modern color functions (oklch, color-mix, relative colors)
- SVG styling (currentColor, stroke animations, drop-shadow, targeting paths by class)
- Problem solving & debugging (isolation, @layer, overflow outlining)
- Safety & anti-patterns

## Workflow

1. **Start with context7** — Look up unfamiliar properties or modern features
2. **Accessibility first** — Define focus styles, contrast ratios, and motion preferences before visual polish
3. **Mobile-first** — Design and code for mobile, enhance for larger screens
4. **Use native nesting** — Scope styles to components; avoid flat class hierarchies
5. **Animate deliberately** — Only `transform` and `opacity`; respect `prefers-reduced-motion`
6. **Use feature queries** — Progressive enhancement with `@supports`
7. **Test across browsers** — Verify in Chrome, Firefox, Safari, Edge
8. **Validate** — Check WCAG contrast, keyboard navigation, and screen reader output
9. **Optimize** — Minimize reflows, use `contain`, leverage GPU acceleration

## Related Skills

This skill focuses on CSS as a declarative styling and animation tool. For deeper expertise in complementary areas, see:

- **animation-specialist** — Advanced animation theory, choreography, timing strategies, and motion design principles that go beyond CSS keyframes
- **svg-graphics** — SVG markup, path creation, filters, clipping paths, and advanced vector techniques for interactive graphics
- **gsap** — GreenSock Animation Platform for imperative, high-performance animations beyond CSS capabilities
- **gsap-scrolltrigger** — Scroll-linked animations and timeline control with GSAP; often paired with CSS for complex scroll sequences
- **smil** — Synchronized Multimedia Integration Language for native SVG animations (deprecated but still relevant for legacy systems)
- **frontend-design** — Design systems, visual hierarchy, typography systems, accessibility-first design, and design token architecture
- **art-theory** — Principles of composition, color theory, typography, and visual storytelling that inform effective design decisions
- **accessibility-patterns** — In-depth patterns and techniques for creating inclusive, WCAG-compliant web experiences across a wide range of disabilities and user needs
- **web-components** — Custom elements, Shadow DOM, and encapsulated styling that can be used in conjunction with CSS for reusable, self-contained UI components

**When to reach for each tool:**
- **CSS animations** — State changes, transitions, entrance/exit effects, and performant scroll-driven animations
- **animation-specialist** — Complex choreography, staggered sequences, and motion design strategy
- **GSAP** — Imperative control, non-linear timelines, morphing, and pixel-perfect animations where CSS falls short
- **SVG graphics** — Vector shapes, paths, filters, and interactive graphic elements
- **GSAP + ScrollTrigger** — Advanced scroll-linked animations with precise control and timeline scrubbing
- **Frontend design** — Design system tokens, component architecture, and accessibility from the ground up
- **Art theory** — Foundational design principles that guide effective visual communication
- **Accessibility patterns** — Specialized techniques for addressing specific accessibility challenges and user needs
- **Web components** — Encapsulated, reusable UI elements that can be styled with CSS and used across projects

## Tools and Resources

- **context7** - Primary documentation lookup tool
- **MDN Web Docs** - Comprehensive CSS reference (via context7)
- **Can I Use** - Browser compatibility data (via context7)
- **CSS Specifications** - W3C specs for detailed behavior (via context7)
- **PostCSS** - Transform CSS with JavaScript plugins
- **CSS Modules** - Scoped CSS for components
- **Sass/SCSS** - CSS preprocessor with variables, nesting, mixins
- **Lightning CSS** - Fast CSS parser, transformer, and minifier
- **CSS DB** (`cssdb.org`) - Track the stage of every CSS spec proposal; useful for knowing what's safe to use
- **Can I Use** (`caniuse.com`) - Browser compatibility tables — always check before deploying Subgrid, Scroll-Timeline, or other newer features to legacy-heavy audiences

---

**Remember**: When in doubt about any CSS feature, syntax, or browser support, use context7 to look it up in real-time documentation.
