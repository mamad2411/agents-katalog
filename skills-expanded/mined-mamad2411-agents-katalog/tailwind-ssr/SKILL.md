---
name: tailwind-ssr
description: TailwindCSS v4 and SSR expert. Use when configuring TailwindCSS, implementing SSR strategies, optimizing critical CSS, or solving styling performance issues.
---

# TailwindCSS v4 & SSR Expert

Expert assistant for TailwindCSS v4 configuration, SSR/SSG styling strategies, critical CSS optimization, and frontend performance.

## Thinking Process

When activated, follow this structured thinking approach to solve TailwindCSS and SSR styling problems:

### Step 1: Version and Context Identification

**Goal:** Understand the exact TailwindCSS and framework context.

**Key Questions to Ask:**
- What TailwindCSS version? (v3 vs v4 have major differences)
- What frontend framework? (SvelteKit, Next.js, Nuxt, etc.)
- What rendering mode? (SSR, SSG, SPA, hybrid)
- What build tool? (Vite, Webpack, Turbopack)

**Actions:**
1. Check `package.json` for tailwindcss version
2. Review build configuration (vite.config, next.config)
3. Identify CSS entry point and import style

**Version Decision Matrix:**

| If | Then Use |
|----|----------|
| New project | TailwindCSS v4 (CSS-first) |
| Existing v3 project | Consider migration or stay on v3 |
| Legacy browser support needed | TailwindCSS v3 |

**Decision Point:** Document:
- "TailwindCSS version: [X]"
- "Framework: [Y] with [Z] rendering"

### Step 2: Problem Classification

**Goal:** Understand what type of styling challenge this is.

**Key Questions to Ask:**
- Is this a configuration problem? (setup, plugins, theme)
- Is this an SSR problem? (FOUC, hydration, critical CSS)
- Is this a performance problem? (bundle size, render blocking)
- Is this a design system problem? (tokens, variants, customization)

**Decision Point:** Classify to select appropriate solutions:
- Configuration → Check tailwind.config or CSS imports
- SSR → Analyze render timing and CSS delivery
- Performance → Review bundle and critical CSS strategy
- Design System → Design theme and variant structure

### Step 3: Configuration Analysis (v3 vs v4)

**Goal:** Ensure correct configuration for the version.

**TailwindCSS v4 (CSS-first):**
```css
/* app.css */
@import "tailwindcss";

@theme {
  --color-primary: oklch(0.7 0.15 200);
  --font-display: "Inter", sans-serif;
}
```

**TailwindCSS v3 (JS-based):**
```javascript
// tailwind.config.js
module.exports = {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      colors: {
        primary: '#3b82f6',
      },
    },
  },
}
```

**Migration Considerations:**
- v4 auto-detects content (no config needed)
- v4 uses CSS variables for theming
- v4 has new color functions (oklch)
- v4 requires modern browsers

### Step 4: SSR Styling Strategy

**Goal:** Ensure styles load correctly in SSR context.

**Thinking Framework:**
- "What CSS is needed for first paint?"
- "When is the stylesheet loaded?"
- "What causes Flash of Unstyled Content (FOUC)?"

**SSR Styling Timeline:**
```
Server Render → HTML with inline/critical CSS → Browser parses HTML
    → Download full CSS → Hydration → Interactive
```

**SSR Checklist:**
- [ ] CSS imported in layout/root component
- [ ] Critical CSS inlined or preloaded
- [ ] No style-dependent JavaScript before CSS loads
- [ ] Consistent class generation server/client

**Framework-Specific Patterns:**

| Framework | CSS Import Location |
|-----------|---------------------|
| SvelteKit | +layout.svelte or app.css |
| Next.js | app/layout.tsx or globals.css |
| Nuxt | nuxt.config.ts css array |

### Step 5: FOUC Prevention

**Goal:** Eliminate Flash of Unstyled Content.

**Thinking Framework:**
- "Is CSS render-blocking or async?"
- "What is the first meaningful paint showing?"
- "Is there content shift during hydration?"

**FOUC Causes and Solutions:**

| Cause | Solution |
|-------|----------|
| CSS loads async | Make critical CSS render-blocking |
| Dynamic classes | Ensure SSR includes all needed classes |
| Font loading | Use font-display: swap with preload |
| Theme switching | Inline theme detection script |

**Anti-FOUC Pattern:**
```html
<html class="no-js">
<head>
  <!-- Inline critical CSS -->
  <style>/* critical styles */</style>

  <!-- Theme detection before render -->
  <script>
    const theme = localStorage.getItem('theme') || 'light';
    document.documentElement.classList.add(theme);
    document.documentElement.classList.remove('no-js');
  </script>

  <!-- Full CSS with preload -->
  <link rel="preload" href="/styles.css" as="style">
  <link rel="stylesheet" href="/styles.css">
</head>
```

### Step 6: Performance Optimization

**Goal:** Minimize CSS impact on performance.

**Thinking Framework:**
- "How large is the CSS bundle?"
- "What CSS is unused?"
- "What is render-blocking?"

**Performance Checklist:**
- [ ] PurgeCSS/content detection configured correctly
- [ ] No unused Tailwind plugins loaded
- [ ] Critical CSS extracted and inlined
- [ ] Non-critical CSS deferred
- [ ] Fonts optimized (subset, preload, swap)

**Bundle Analysis:** build with `--minify` and check the emitted CSS size; in v4 the output is driven by detected content, so unused utilities never ship.

**Optimization Strategies:**

| Strategy | When to Use |
|----------|-------------|
| Disable unused core plugins | Reduce base size |
| Use specific content globs | Faster builds, smaller output |
| Extract critical CSS | Improve FCP |
| Lazy load below-fold styles | Reduce initial CSS |

### Step 7: Theme and Design Token Strategy

**Goal:** Design a maintainable theming system.

**Thinking Framework:**
- "What needs to be customizable?"
- "How do we handle dark mode?"
- "What are the design system tokens?"

**Theme Architecture (v4):**
```css
@theme {
  /* Color tokens */
  --color-primary: oklch(0.6 0.2 250);
  --color-secondary: oklch(0.7 0.15 180);

  /* Semantic tokens */
  --color-background: var(--color-gray-50);
  --color-foreground: var(--color-gray-900);

  /* Spacing scale */
  --spacing-page: 2rem;
}

/* Dark mode overrides */
@media (prefers-color-scheme: dark) {
  :root {
    --color-background: var(--color-gray-900);
    --color-foreground: var(--color-gray-50);
  }
}
```

**Dark Mode Strategies:**

| Strategy | Implementation |
|----------|----------------|
| System preference | @media (prefers-color-scheme) |
| Class-based | Toggle .dark on html element |
| Hybrid | System default + user override |

### Step 8: Troubleshooting Framework

**Goal:** Systematically debug styling issues.

**Debugging Checklist:**

| Symptom | Check |
|---------|-------|
| Classes not applying | Content detection paths |
| FOUC on navigation | CSS import in layout |
| Hydration mismatch | Dynamic classes in SSR |
| Build too slow | Glob pattern specificity |
| Bundle too large | Unused plugins, content paths |

**Debug Commands:** `DEBUG=tailwindcss:content` to trace content detection; pass `--verbose` to the CLI to inspect the build; confirm dynamic classes literally appear in source (v4 detects whole class strings, not interpolated fragments).

## Documentation Resources

**Context7 Library IDs:**
- TailwindCSS v4: `/websites/tailwindcss` (2333 snippets)
- TailwindCSS v3: `/websites/v3_tailwindcss` (2691 snippets, Score: 85.9)

**Official Documentation:**
- Docs: `https://tailwindcss.com/docs`
- Blog (release notes): `https://tailwindcss.com/blog`
- Upgrade Guide: `https://tailwindcss.com/docs/upgrade-guide`

## Install & Tooling

Always install `tailwindcss@latest` alongside the matching first-party loader for
your build tool — keep the two versions in sync.

```bash
# Vite (recommended for SvelteKit / Vite apps)
npm i -D tailwindcss@latest @tailwindcss/vite@latest

# PostCSS
npm i -D tailwindcss@latest @tailwindcss/postcss@latest

# CLI
npm i -D tailwindcss@latest @tailwindcss/cli@latest

# Webpack / Next.js (Turbopack) — first-party loader, 2x+ faster than the PostCSS path
npm i -D tailwindcss@latest @tailwindcss/webpack@latest
```

| Build tool | Loader | Notes |
|------------|--------|-------|
| Vite | `@tailwindcss/vite` | Canonical path for SvelteKit; add to `vite.config` plugins |
| Webpack / Next.js | `@tailwindcss/webpack` | First-party loader (v4.2+); faster than `@tailwindcss/postcss` |
| PostCSS | `@tailwindcss/postcss` | Framework-agnostic fallback |

## TailwindCSS v4 Key Changes

### CSS-First Configuration (v4.0)

```css
/* v4 uses CSS @import instead of @tailwind directives */
@import "tailwindcss";

/* Design tokens as CSS variables */
@theme {
  --color-primary: oklch(0.7 0.15 200);
  --font-display: "Inter", sans-serif;
  --breakpoint-3xl: 1920px;
}
```

### Automatic Content Detection (v4.0)

```css
/* v4 auto-detects content, no config needed */
/* Manual override if needed: */
@source "../components/**/*.tsx";
```

### Core v4.0 Features

```css
/* Container queries */
@container (min-width: 400px) {
  .card { /* styles */ }
}

/* 3D transforms */
.element {
  @apply rotate-x-45 perspective-500;
}

/* Modern color functions */
.button {
  background: oklch(0.7 0.15 200);
}
```

## What's New Since v4.0 (Changelog)

Track the point releases — the skill must reflect the current feature set, not just v4.0.

### v4.1
- **`text-shadow-*`** utilities (`text-shadow-sm` … `text-shadow-lg`, color + opacity).
- **`mask-*`** utilities: `mask-image`, mask composites, and gradient masks
  (`mask-t-from-*`, `mask-radial-*`, etc.).

### v4.2
- **New palettes:** `mauve`, `olive`, `mist`, `taupe` (neutral-leaning ramps).
- **`@tailwindcss/webpack`** first-party loader — 2x+ faster than the PostCSS path
  (benefits Next.js / Turbopack).
- **Expanded logical properties:** `pbs-*`/`pbe-*`, `mbs-*`/`mbe-*`,
  `scroll-pbs-*`/`scroll-mbs-*`, `border-bs`/`border-be-*`, logical sizing
  (`block-*`, `inline-*`, `min-block-*`, `max-inline-*`), and logical inset
  (`inset-s-*`, `inset-e-*`, `inset-bs-*`, `inset-be-*`).
- **Deprecation:** `start-*` / `end-*` → use `inset-s-*` / `inset-e-*`.
- **`font-features-*`** for raw `font-feature-settings` (prefer high-level
  utilities like `tabular-nums` first).

### v4.3
- **Scrollbar utilities:** `scrollbar-auto` / `scrollbar-thin` / `scrollbar-none`
  (scrollbar-width); `scrollbar-thumb-*` / `scrollbar-track-*` (scrollbar-color,
  support `/opacity`); `scrollbar-gutter-auto` / `-stable` / `-both`.
- **`@container-size`:** creates a *size* container exposing block-axis query units
  (`cqb`/`cqh`), unlike `@container` which only creates an inline-size container;
  nameable via `@container-size/{name}`.
- **`zoom-*`** utilities (`zoom-75`/`-100`/`-125`, arbitrary `zoom-[1.1]`, `zoom-(--var)`).
- **`tab-*`** utilities for `tab-size` (`tab-2`/`tab-8`, arbitrary, var).
- **Stacked + compound `@variant` in CSS:** `@variant hover:focus {}` and
  `@variant hover, focus {}`.
- **Default values for functional utilities** via `--default(…)` inside
  `--value(…)`/`--modifier(…)`:
  ```css
  @utility tab-* {
    tab-size: --value(integer, --default(4)); /* bare `tab` now works */
  }
  ```

## SSR Performance Checklist

### Critical CSS
- [ ] Inline above-the-fold CSS
- [ ] Defer non-critical stylesheets
- [ ] Use `<link rel="preload">` for fonts

### Hydration
- [ ] Avoid layout shifts during hydration
- [ ] Match server and client class generation
- [ ] Test with JavaScript disabled

### FOUC Prevention
```html
<!-- Add loading state -->
<html class="no-js">
<head>
  <script>document.documentElement.classList.remove('no-js')</script>
  <style>.no-js .lazy-load { visibility: hidden; }</style>
</head>
```

## Framework Integration

### SvelteKit

Canonical path: add the `@tailwindcss/vite` plugin, then `@import "tailwindcss"`
in `app.css` and import it once in the root layout.

```ts
// vite.config.ts
import { sveltekit } from '@sveltejs/kit/vite';
import tailwindcss from '@tailwindcss/vite';
import { defineConfig } from 'vite';

export default defineConfig({ plugins: [tailwindcss(), sveltekit()] });
```

```svelte
<!-- +layout.svelte -->
<script>
  import '../app.css';
</script>
```

```css
/* app.css */
@import "tailwindcss";
```

### Next.js

```tsx
// app/layout.tsx
import './globals.css';
```

```css
/* globals.css */
@import "tailwindcss";
```

## Performance Optimization

### PurgeCSS (Production)
```css
/* v4 handles this automatically */
/* Ensure all dynamic classes are detectable */
```

### Custom Variants
```css
@variant hocus (&:hover, &:focus);
@variant group-hocus (:merge(.group):hover &, :merge(.group):focus &);
```

### Reduce Bundle Size
```css
/* Disable unused core plugins */
@import "tailwindcss" layer(utilities);
@import "tailwindcss/preflight" layer(base);
```

## Mindset

- **Components over CSS abstractions.** Prefer real, reusable components styled
  with utilities over hiding utilities behind `@variant`/`@apply` in CSS.
- **High-level utility before escape hatch.** Reach for `tabular-nums`,
  logical `inset-s-*`, scrollbar/container utilities before arbitrary values or
  raw `font-features-*`.
- **CSS-first config stays the default.** Theme via `@theme` tokens; let v4
  auto-detect content.
- **Logical properties by default** for i18n/RTL-ready layouts
  (`inset-s-*`/`pbs-*`), not the deprecated `start-*`/`end-*`.

## Browser Compatibility

**TailwindCSS v4 targets a modern baseline** (verify current minimums against the
upgrade guide, and note that newer utilities such as `mask-*`/scrollbar-color may
have stricter per-feature support):
- Safari 16.4+
- Chrome 111+
- Firefox 128+
- Edge 111+

## Present Results to User

When providing TailwindCSS solutions:
- Specify v3 vs v4 syntax differences
- Provide copy-paste ready configuration
- Consider SSR framework-specific integration
- Note browser compatibility requirements
- Include performance implications

## Troubleshooting

**"Styles not applying"**
- Check content detection paths
- Verify CSS import is correct
- Clear build cache

**"FOUC (Flash of Unstyled Content)"**
- Inline critical CSS
- Add proper preload hints
- Check hydration timing

**"Build too slow"**
- Reduce content glob patterns
- Use specific file extensions
- Enable caching in build tool
