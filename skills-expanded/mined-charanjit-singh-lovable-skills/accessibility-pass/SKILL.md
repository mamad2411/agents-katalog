---
name: accessibility-pass
description: >-
  Use when reviewing or fixing accessibility: keyboard navigation, focus order,
  labels, color contrast, screen reader support, or ARIA attributes. Not for
  SEO-only or performance-only audits.
---

# Accessibility pass

Report findings as: **critical** (blocks users), **serious**, **minor**.

## Keyboard and focus

- All interactive elements reachable by Tab; visible focus ring.
- Modals trap focus; Escape closes.
- No `tabIndex={0}` on non-interactive divs for click hacks — use `<button>`.

## Labels and semantics

- Every input has `<Label htmlFor>` or `aria-label`.
- Icon-only buttons have `aria-label`.
- Images: `alt` descriptive or `alt=""` if decorative.
- Use `<button>` for actions, `<a href>` for navigation.

## Forms

- Errors linked with `aria-describedby` / `FormMessage`.
- Required fields indicated in label or `aria-required`.

## Color and motion

- Text contrast ≥ 4.5:1 (normal), 3:1 large text.
- Do not rely on color alone for state (add icon/text).
- Respect `prefers-reduced-motion` for large animations.

## Tables and dynamic content

- `<th scope="col">` on data tables.
- `aria-live="polite"` for toast/alert regions when appropriate.

## Avoid

- `div onClick` without role/keyboard support.
- Auto-playing media with sound.
- Removing focus outlines without replacement.

## Deliverable

Checklist table: issue | location | fix | severity.
