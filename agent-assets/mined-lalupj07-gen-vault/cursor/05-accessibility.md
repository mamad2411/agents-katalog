---
description: Accessibility requirements targeting WCAG 2.2 AA
globs: "**/*.{tsx,jsx,vue,svelte,astro,html,css,scss,dart}"
alwaysApply: false
---

# Accessibility (WCAG 2.2 AA where practical)

Accessibility overrides visual preferences in `01-design-system.mdc` and `10-design-rules.mdc` when they conflict.

- **Semantics**: native elements first (`button`, `a`, `nav`, `main`, `label`, `table`). ARIA only when no native element fits. One `h1` per page, no skipped heading levels. Flutter: `Semantics` labels on custom widgets.
- **Keyboard**: everything operable by keyboard alone. Logical tab order matching visual order. No traps. Escape closes dialogs and menus; focus returns to the trigger.
- **Focus**: visible `:focus-visible` indicator with at least 3:1 contrast. Never remove outlines without a replacement. Focused elements not hidden behind sticky headers.
- **Labels**: every input has a visible label. Icon-only buttons have an accessible name. Meaningful `alt`, decorative images `alt=""`.
- **Screen readers**: announce async results with `aria-live="polite"`, errors with `role="alert"`. Provide a skip link on content sites.
- **Contrast**: text 4.5:1, large text and UI components 3:1, in every theme mode.
- **Touch targets**: at least 24x24px (WCAG 2.2 minimum), aim for 44x44px.
- **Motion**: honor `prefers-reduced-motion` (and platform equivalents) for every animation, parallax, smooth scroll and auto-moving content. Pause control for anything moving longer than 5 seconds.
- **Color**: never communicate status with color alone. Pair with text or an icon.
- **Forms**: errors identified in text, linked via `aria-describedby`, user input preserved.
- **Zoom and text scaling**: usable at 200% zoom, 320px width, and large system font sizes.
