---
name: flutter-accessibility
description: Audit and improve Flutter accessibility, inclusive interaction, localization safety, and RTL behavior. Use for screen-reader semantics, focus and keyboard navigation, text scaling, contrast, touch targets, reduced motion, form errors, RTL, localization, or accessibility acceptance checks.
---

# Flutter Accessibility

Treat accessibility failures that block core tasks as release blockers.

## Audit

1. Identify core journeys and the assistive modes relevant to supported platforms.
2. Inspect semantics, labels, values, hints, grouping, headings, live updates, and decorative exclusions.
3. Traverse with keyboard, switch-like focus, and screen reader where available.
4. Test system text scaling up to the supported maximum without clipping or hiding critical actions.
5. Verify contrast, non-color cues, touch targets, error association, disabled-state clarity, and motion preferences.
6. Test long translations, pluralization, bidirectional content, mirrored navigation, and directional icon correctness.
7. Read `references/accessibility-and-localization.md` and relevant platform guidance already present in the project.
   For multi-domain dashboards, read `references/connected-product-workflows.md` and align semantic order with cross-domain visual priority.

## Implement

- Prefer semantic native Flutter controls before custom gesture surfaces.
- Merge or exclude semantics intentionally; do not create duplicate announcements.
- Keep focus order aligned with visual and task order.
- Announce asynchronous errors and important state changes without excessive chatter.
- Use logical direction APIs (`start`/`end`) when layout should mirror.
- Do not disable text scaling to protect a fragile layout.
- Provide reduced-motion behavior without removing necessary feedback.

## Verify and Report

State tools, platforms, text scales, locales, directions, themes, and journeys tested. Distinguish automated checks from manual assistive-technology verification and identify gaps.
