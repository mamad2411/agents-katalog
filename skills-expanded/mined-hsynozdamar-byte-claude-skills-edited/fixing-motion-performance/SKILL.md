---
name: fixing-motion-performance
description: "Audit and fix animation performance: layout thrashing, compositor properties, scroll-linked motion, blur. Use when animations stutter or jank."
---

# Fixing motion performance

Fix animation jank within the project's existing animation stack (CSS, WAAPI, Motion, rAF, GSAP). Keep the library: migrate or mix animation APIs only when the user asks, and never half-migrate a component.

`/fixing-motion-performance` applies these rules to animation work in the conversation. `/fixing-motion-performance <file>` reviews a file and reports each violation as the quoted line, one sentence on why it matters, and a code-level fix.

Apply when adding or changing animations, refactoring janky interactions, building scroll-linked or reveal-on-scroll motion, animating layout, filters, masks, gradients or CSS variables, or reviewing `will-change`, transforms and measurement code.

## Cost ladder

Pick the cheapest rendering stage that matches the intent; state the constraint (surface size, duration, interaction need) behind any heavier choice.

- **Composite**: `transform`, `opacity`. The default for motion.
- **Paint**: color, borders, gradients, masks, images, filters. Fine on small, isolated elements.
- **Layout**: size, position, flow, grid, flex. Reserve for one-shot effects on small surfaces.

Downgrade the technique before removing the motion: opacity and translate first, blur last.

## Rules by priority

**1. Layout stays out of the frame loop (critical)**
- Batch DOM reads before writes; measure once, then animate via transform or opacity (FLIP for layout-like effects).
- Give every `requestAnimationFrame` loop a stop condition.
- Keep one animation system per element; two systems that each measure or mutate layout fight each other.

**2. Scroll (high)**
- Drive scroll-linked motion with Scroll or View Timelines (`animation-timeline: view()`), not `scrollTop`, `scrollY` or scroll events.
- Use IntersectionObserver for visibility, and pause or stop animations that are off-screen.
- Scroll-linked motion on large surfaces stays on the compositor.

**3. Paint and CSS variables (medium-high)**
- Large containers animate transform and opacity only.
- Animate transform, opacity and position directly, not through CSS variables. When a variable must animate, scope it to the element and keep it from inheriting, since an inherited animated variable invalidates every descendant.

**4. Layers (medium)**
- Compositor motion needs layer promotion; confirm it with devtools instead of assuming.
- Set `will-change` only while animating, on specific elements, and keep promoted layers few and small.

**5. Blur and filters (medium)**
- Blur animates at 8px or less, in short one-time effects, on small surfaces. Continuous blur and blur on large surfaces get replaced by opacity and translate.

**6. View transitions (low)**
- Use them for navigation-level changes. Interaction-heavy UI and anything that needs interruption or cancellation uses another mechanism. Treat size changes inside a transition as layout-triggering.

**7. JS-driven animation**
- Use it only when the interaction requires it (gestures, physics). One-shot effects are acceptable more often than continuous motion.

Before and after snippets (transform vs width, scroll-timeline vs scroll listener, FLIP): [references/fixes.md](references/fixes.md).

## Review

Report critical violations first (layout in the frame loop, mixed animation systems), then the rest in priority order. Give a concrete alternative for each note.
