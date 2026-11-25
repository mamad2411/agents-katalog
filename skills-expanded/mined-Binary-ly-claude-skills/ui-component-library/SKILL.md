---
name: ui-component-library
description: Best practices for building world-class CSS UI component libraries — highly organized, highly customizable, and very fast in performance. Grounded in MDN, CSS Working Group specs, browser engineering docs, and W3C ARIA Authoring Practices. Use this skill whenever the user is building, reviewing, styling, or debugging any CSS component, design system, UI library, accessible widget, or interactive HTML control. Also use when the user asks about ARIA patterns, keyboard accessibility, focus management, or WCAG compliance — even if they don't explicitly ask for "best practices."
metadata:
  tags: css, ui-library, design-system, custom-properties, performance, tailwind, tokens, aria, accessibility, wcag
---

## How to use

Read the relevant reference file based on what you're working on. Only read what you need — don't load everything at once.

### CSS Architecture — read when designing or structuring a component library

- [rules/token-architecture.md](rules/token-architecture.md) - Read when setting up CSS custom property layers or deciding public vs internal API
- [rules/at-property.md](rules/at-property.md) - Read when considering @property registration (contains a critical fallback chain trap)
- [rules/specificity.md](rules/specificity.md) - Read when encountering specificity wars or setting up :where() patterns
- [rules/naming.md](rules/naming.md) - Read when naming components, CSS variables, or shape modifiers
- [rules/file-organization.md](rules/file-organization.md) - Read when scaffolding a new library or reorganizing files
- [rules/themes.md](rules/themes.md) - Read when implementing theme switching or dark mode

### CSS Techniques — read when implementing specific visual/interactive features

- [rules/performance.md](rules/performance.md) - Read when using contain, content-visibility, will-change, clip-path, or filter
- [rules/color.md](rules/color.md) - Read when working with color-mix(), oklch, or perceptual color systems
- [rules/motion.md](rules/motion.md) - Read when adding hover/transition animations or directional easing
- [rules/accessibility.md](rules/accessibility.md) - Read when implementing focus styles, ARIA roles, or checking WCAG contrast
- [rules/mistakes.md](rules/mistakes.md) - Read when reviewing code for common pitfalls (10 patterns with fixes)

### Web Performance (from web.dev) — read when optimizing load time or runtime performance

- [rules/webdev-performance/core-metrics.md](rules/webdev-performance/core-metrics.md) - Read when measuring or targeting LCP, CLS, INP thresholds
- [rules/webdev-performance/rendering-pipeline.md](rules/webdev-performance/rendering-pipeline.md) - Read when debugging rendering bottlenecks or choosing compositor-only properties
- [rules/webdev-performance/layout-thrashing.md](rules/webdev-performance/layout-thrashing.md) - Read when diagnosing forced synchronous layout or batch read/write issues
- [rules/webdev-performance/long-tasks.md](rules/webdev-performance/long-tasks.md) - Read when breaking up long tasks or improving input responsiveness
- [rules/webdev-performance/lcp-cls-inp-optimization.md](rules/webdev-performance/lcp-cls-inp-optimization.md) - Read when you need the full optimization playbook for any Core Web Vital
- [rules/webdev-performance/fonts-and-assets.md](rules/webdev-performance/fonts-and-assets.md) - Read when optimizing font loading, resource hints, or image delivery

### ARIA Authoring Practices (from W3C APG) — read when building accessible interactive widgets

- [rules/aria-apg/keyboard-and-focus.md](rules/aria-apg/keyboard-and-focus.md) - Read when implementing keyboard navigation, focus management, or roving tabindex
- [rules/aria-apg/names-and-descriptions.md](rules/aria-apg/names-and-descriptions.md) - Read when labeling elements with aria-label, aria-labelledby, or aria-describedby
- [rules/aria-apg/landmarks-and-structure.md](rules/aria-apg/landmarks-and-structure.md) - Read when setting up page landmarks, structural roles, or using aria-hidden
- [rules/aria-apg/grid-table-range.md](rules/aria-apg/grid-table-range.md) - Read when building data grids, tables with ARIA, or range widgets (sliders, meters)
- [rules/aria-apg/form-controls.md](rules/aria-apg/form-controls.md) - Read when building buttons, checkboxes, radios, switches, comboboxes, listboxes, or sliders
- [rules/aria-apg/navigation-and-menus.md](rules/aria-apg/navigation-and-menus.md) - Read when building menubars, menu buttons, tabs, toolbars, or breadcrumbs
- [rules/aria-apg/dialogs-alerts-disclosure.md](rules/aria-apg/dialogs-alerts-disclosure.md) - Read when building modals, alerts, tooltips, accordions, or disclosure widgets
- [rules/aria-apg/data-display-widgets.md](rules/aria-apg/data-display-widgets.md) - Read when building data tables, grids, tree views, feeds, meters, or carousels
