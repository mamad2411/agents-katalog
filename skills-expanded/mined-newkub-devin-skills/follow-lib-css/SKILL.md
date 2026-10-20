---
name: follow-lib-css
description: Write CSS following modern best practices and Baseline features
argument-hint: "[scope]"
related:
  - follow-lib-unocss
  - follow-lib-animejs
  - follow-tool-formatter
  - follow-best-practice
  - follow-web-standard

---

## Goal

Write maintainable, performant, accessible CSS using modern CSS features per the 2025/2026 Baseline

## Scope

Applies to traditional CSS, CSS Modules, CSS-in-JS, and preprocessors detected in the project — CSS is a web platform standard, no package to install

Boundaries:
- Use this skill for raw CSS writing/review per modern standards and Baseline
- If the project uses a utility-first engine (UnoCSS/Tailwind) → use `/follow-lib-unocss` instead
- For JS-driven animation (timelines, staggers) → use `/follow-lib-animejs` instead; plain CSS transitions/animations are in this scope
- Markup semantics, native widgets, and Web-API-over-library choices beyond CSS → use `/follow-web-standard` instead

- References: [apis](references/apis.md) 
## Execute

### 1. Analyze CSS Setup

> Goal: analyze the current CSS setup

1. Check the CSS framework or utility-first engine in use (`Tailwind`, `UnoCSS`, `Bootstrap`, etc.)
2. Check the CSS-in-JS or scoped styles in use (`CSS Modules`, `styled-components`, etc.)
3. Check the CSS preprocessor (`Sass`, `Less`, `PostCSS`) and build tools
4. Identify the browser support target from `browserslist`, `package.json`, or project requirements
5. If there is no target, default to Baseline (`last 2 versions, >0.5%`)

### 2. Apply Modern Layout And Cascade

> Goal: use Baseline-ready modern CSS features

1. Use CSS custom properties (`--variable`) and `@property` for theming and typed variables
2. Use `:is()` and `:where()` to reduce specificity complexity
3. Use `:has()` for relational styling
4. Use native CSS Nesting instead of preprocessor nesting when the target supports it
5. Use `@layer` for cascade control (`reset`, `base`, `theme`, `components`, `utilities`)
6. Use Container Queries (`@container`) for component-level responsiveness
7. Use Flexbox, Grid, and Subgrid for layouts
8. Use logical properties (`margin-inline-start`, `inset`, etc.) for multi-locale
9. Use View Transitions (`::view-transition`, `view-transition-name`, `view-transition-class`) for page/state transitions (Baseline 2025)
10. Use the Popover API (`popover` attribute + `:popover-open`) instead of custom overlays where suitable (Baseline 2025)
11. Use `@starting-style` + `transition-behavior: allow-discrete` for entry/exit transitions on `display: none` elements
12. Use `scrollbar-color`/`scrollbar-width` for scrollbar styling (Baseline 2025)

### 3. Use Modern Color And Sizing

> Goal: use modern color spaces and fluid sizing

1. Use `oklch()`, `color-mix()`, and `light-dark()` for a modern color system
2. Use `clamp()`, `min()`, `max()` for fluid typography and spacing
3. Use relative units (`rem`, `em`, `%`, `cqw`, `cqi`) to respect user preferences
4. Use `aspect-ratio` for media containers
5. Use `gap` instead of `margin` in Flexbox/Grid
6. Use `text-wrap: balance` for headings and `text-wrap: pretty` for body copy (Baseline 2024)
7. Use `abs()`/`sign()` in `calc()` when math functions are needed (Baseline 2025)

### 4. Optimize Performance

> Goal: improve CSS performance

1. Use `content-visibility` for lazy rendering of off-screen content
2. Use the `contain` property to isolate layout/paint
3. Use `will-change` carefully and remove it after the animation ends
4. Use `transform` and `opacity` for animations to get GPU acceleration
5. Remove unused CSS with build tools (`PurgeCSS`, `UnoCSS`, `Lightning CSS`)
6. Minify CSS for production
7. Use `font-display: swap` for web fonts
8. Use `prefetch`/`preload` for critical assets appropriately

### 5. Ensure Accessibility

> Goal: verify CSS accessibility

1. Pair semantic HTML with CSS
2. Use `:focus-visible` for keyboard navigation
3. Use `prefers-reduced-motion` for motion sensitivity
4. Use `prefers-contrast` and `prefers-color-scheme` per context
5. Check color contrast per WCAG 2.1 (minimum 4.5:1 for text)
6. Use relative units (`rem`, `em`) for font and spacing

### 6. Browser Compatibility

> Goal: check and manage browser compatibility

1. Use `@supports` for feature detection
2. Check browser support on `caniuse.com` or `web.dev/baseline`
3. Use progressive enhancement with fallbacks for unsupported features
4. Use `Autoprefixer` or `Lightning CSS` only when the build pipeline needs vendor prefixes
5. Avoid non-Baseline features unless the project targets specific browsers

## Rules

### 1. CSS Architecture

- Structure CSS with `@layer` or utility-first/ITCSS
- Separate concerns: reset, base, theme, components, utilities
- Use CSS Modules or scoped styles for isolation
- Use barrel exports for imports where appropriate
- Order declarations by logical group (`layout`, `box model`, `typography`, `visual`)

### 2. Modern Features

- Prefer CSS custom properties over preprocessor variables
- Use `oklch()` or `hsl()` for colors to get perceptual uniformity
- Use `clamp()` for responsive typography
- Use `container`/`@container` for component-level responsiveness
- Use native CSS Nesting instead of Sass/Less nesting when the browser target supports it
- Use `@scope` when limiting cascade reach is needed

### 3. Responsive Design

- Use a mobile-first approach
- Use Container Queries for components reused in many contexts
- Use relative units (`rem`, `em`, `%`, `cq*`) and `min()`/`max()`/`clamp()`
- Test at the project's breakpoints

### 4. Performance

- Remove unused CSS with the project's build tool
- Use the `contain` property to isolate layout/paint
- Use `transform`/`opacity` for animations
- Reduce critical rendering path blockers
- Use `font-display: swap` for custom fonts
- Avoid overusing `will-change`

### 5. Accessibility

- Use `:focus-visible` instead of `:focus` for focus styles
- Provide a `prefers-reduced-motion` media query for motion
- Check contrast with tools such as Lighthouse
- Use relative units to respect user font scaling

### 6. Browser Compatibility

- Use `@supports` for feature queries
- Use `caniuse.com` and `web.dev/baseline` to check support
- Provide fallbacks for unsupported features

- Use `/follow-lib-unocss` if the project uses a utility-first engine
- Use `/follow-lib-animejs` for JS-driven animation
- Use `/follow-tool-formatter` if needed
- Use `/follow-best-practice` if needed

- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- CSS written per modern best practices and the 2025/2026 Baseline
- Better performance (less unused CSS, containment, GPU-friendly animations)
- Complete accessibility
- Maintainable CSS architecture
- Clear browser compatibility with fallbacks
