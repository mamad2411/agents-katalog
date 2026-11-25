---
name: web-experience-audit
description: "Use after frontend page, component, style, route, form, or interaction changes to verify browser behavior and visual quality with real evidence."
---

# Web Experience Audit

## Checks

- Page loads without console errors relevant to the change.
- Primary workflow works.
- Desktop and mobile layouts fit without overlap or clipped controls.
- Loading, empty, error, and disabled states are coherent when applicable.
- Text is readable and does not overflow.
- Network calls match expected endpoints and do not leak sensitive data.
- Component library usage is coherent with the repository's design system; Ant Design-based apps should use Ant primitives/tokens instead of visually incompatible custom controls.
- Visual hierarchy, spacing, typography, color, motion, and feedback pass a concise craft review.
- Tests or browser evidence cover the user's actual workflow, at least one edge state, and the smallest relevant responsive breakpoint set.

## Evidence

Use Playwright, browser tools, screenshots, console/network output, accessibility checks, or the closest available runtime evidence. For rich UI changes, prefer one desktop and one mobile screenshot plus console/network notes. If browser verification is unavailable, state the blocker and provide static fallback checks.
