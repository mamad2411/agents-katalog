---
name: design
description: Check design-system and UI consistency for diffs that touch user-facing surfaces. Use for visual changes, design checks, or as the UI stage of $ship, including small component, style, copy, and layout changes.
---

# Design

Gate on the diff: if it does not touch components, styles, tokens, templates, markup, copy, or layout, report "no UI changes in diff" and stop.

1. **Load context** — Read the applicable `AGENTS.md` files and the design-system documentation they identify, including the component library, tokens, spacing, typography, breakpoints, and themes.
2. **Inspect statically** — Find hand-written values where tokens exist, reimplemented component variants, placeholder copy, and accessibility defects in semantics, labels, alt text, focus states, contrast, or keyboard access.
3. **Look at the UI** — Start the documented development environment or Storybook. Use `$agent-browser` for real interaction and screenshots unless the repository explicitly requires another tool; load its current core workflow before issuing browser commands. Check empty, loading, error, and populated states; hover, focus, active, and disabled states; long and minimal content; project breakpoints; and supported themes. Support every "looks correct" claim with a screenshot.
4. **Fix or flag** — Fix mechanical defects within scope, such as a wrong token, missing focus style, or broken breakpoint. Present tradeoffs before changes that involve visual judgment, intentional-looking behavior, or other screens.

Check at least one additional consumer when the diff changes a shared component. Preserve consistency rather than redesigning or adding unrequested aesthetic changes.
