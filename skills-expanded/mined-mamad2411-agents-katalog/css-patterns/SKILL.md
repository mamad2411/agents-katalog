---
name: css-patterns
description: "When to activate: CSS Grid, Flexbox, custom properties, container queries, cascade layers, logical properties, :has selector, modern CSS"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: frontend
  language: web
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# CSS Patterns

## CSS Grid

```css
/* Named grid areas */
.layout {
  display: grid;
  grid-template-areas:
    "header header"
    "sidebar main"
    "footer footer";
  grid-template-columns: 250px 1fr;
  grid-template-rows: auto 1fr auto;
  min-height: 100dvh;
}
.header  { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main    { grid-area: main; }
.footer  { grid-area: footer; }

/* Auto-fill responsive grid without media queries */
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 300px), 1fr));
  gap: 1.5rem;
}

/* Subgrid for aligned card internals */
.card {
  display: grid;
  grid-row: span 3;
  grid-template-rows: subgrid;
}
```

## Flexbox

```css
/* Center anything */
.center { display: flex; place-items: center; }

/* Space-between with wrap fallback */
.nav {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  align-items: center;
  justify-content: space-between;
}

/* Equal-height cards with footer pinned to bottom */
.card {
  display: flex;
  flex-direction: column;
}
.card__body { flex: 1; }
.card__footer { margin-top: auto; }
```

## CSS Custom Properties

```css
:root {
  /* Primitive tokens */
  --color-blue-500: oklch(55% 0.22 260);
  --space-4: 1rem;
  --radius-md: 0.5rem;

  /* Semantic tokens */
  --color-primary: var(--color-blue-500);
  --surface-1: oklch(98% 0 0);
  --text-1: oklch(15% 0 0);
}

@media (prefers-color-scheme: dark) {
  :root {
    --surface-1: oklch(12% 0 0);
    --text-1: oklch(95% 0 0);
  }
}

/* Component-scoped variables */
.button {
  --btn-bg: var(--color-primary);
  --btn-radius: var(--radius-md);
  background: var(--btn-bg);
  border-radius: var(--btn-radius);
}
.button--danger { --btn-bg: oklch(55% 0.22 25); }
```

## Container Queries

```css
/* Define a containment context */
.card-wrapper {
  container-type: inline-size;
  container-name: card;
}

/* Style based on container width, not viewport */
@container card (min-width: 400px) {
  .card { flex-direction: row; }
  .card__image { width: 40%; }
}

/* Style query (experimental) */
@container style(--variant: featured) {
  .card { border: 2px solid var(--color-primary); }
}
```

## Cascade Layers

```css
/* Declare layer order first — later = higher priority */
@layer reset, base, components, utilities;

@layer reset {
  *, *::before, *::after { box-sizing: border-box; }
  body { margin: 0; }
}

@layer base {
  a { color: var(--color-primary); }
}

@layer components {
  .button { padding: 0.5em 1em; border-radius: var(--radius-md); }
}

@layer utilities {
  .sr-only {
    position: absolute; width: 1px; height: 1px;
    overflow: hidden; clip: rect(0,0,0,0);
  }
}
```

## Logical Properties

```css
/* Instead of margin-left/right (breaks RTL) */
.container {
  margin-inline: auto;
  padding-inline: 1rem;
  padding-block: 2rem;
  border-inline-start: 3px solid var(--color-primary); /* left in LTR, right in RTL */
}
```

## :has() Selector

```css
/* Parent selector: style form when it contains an invalid input */
.form:has(input:invalid) .submit-btn { opacity: 0.5; pointer-events: none; }

/* Card with image vs without */
.card:has(img) { grid-template-rows: auto 1fr; }

/* Navigation with open dropdown */
.nav-item:has(.dropdown[open]) > .nav-link { color: var(--color-primary); }
```

## Fluid Typography

```css
/* clamp(min, preferred, max) — no media queries needed */
:root {
  --text-sm:   clamp(0.875rem, 0.8rem + 0.3vw, 1rem);
  --text-base: clamp(1rem, 0.9rem + 0.4vw, 1.125rem);
  --text-xl:   clamp(1.25rem, 1rem + 1vw, 2rem);
  --text-hero: clamp(2.5rem, 1rem + 6vw, 6rem);
}
```
