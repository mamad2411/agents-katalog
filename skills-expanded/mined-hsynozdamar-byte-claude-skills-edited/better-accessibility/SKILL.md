---
name: better-accessibility
description: "UI accessibility to WCAG 2.2 AA: focus, keyboard, ARIA, forms, live regions, target sizes. Use when building interactive UI or auditing a screen or component."
---

# Accessibility

Most accessibility is free if you use the platform: native elements bring keyboard support and roles, real labels announce themselves, and a focus ring is one CSS rule. When unsure, take the platform default over a custom rebuild, and remove ARIA rather than add it.

These are minimums, not style. Visual treatment (ring color, hit-area technique, motion) follows the project's design, but the floors below hold. Write fixes in the project's styling system and its existing primitives (Radix, Base UI, React Aria). Color measurement belongs to `better-colors`.

A review is two walks: keyboard only (every flow completes without a mouse), then screen reader (every control announces name, role and state).

## Floors

- **Contrast (WCAG AA):** text 4.5:1, large text (24px, or 18.5px bold) 3:1, UI components and focus indicators 3:1. Never color alone: pair status color with an icon, text or underline.
- **Targets:** 24×24 CSS px minimum (WCAG 2.5.8), or a spacing exception: a 24px circle centered on each small target touches no other target. Aim for 44×44 on touch, 40×40 on desktop when density allows.
- **Focus:** visible on every focusable element via `:focus-visible`. Prefer the browser ring plus `outline-offset: 2px`. A custom ring is at least a `2px` solid perimeter, checked against every color it crosses. Never `outline: none` without a verified replacement.
- **Zoom:** works at 200% and reflows at 320px wide without horizontal scroll (tables, maps, code scroll in their own box). Use `min-height`, not fixed `height`, on text containers. Never cap zoom in the viewport meta.
- **Names:** every control has an accessible name; visible label text is part of it (WCAG 2.5.3: a "Send" button can't be `aria-label="Submit message"`).

## Rules that are commonly wrong

- `<button>` for actions, `<a href>` for navigation (must support Cmd/Ctrl/middle-click). Never `<div onClick>`. A "button" that navigates is a styled `<a>`.
- `tabindex` is only `0` or `-1`; positive values break page order. Composite widgets (tabs, menus, toolbars, radio groups) are one Tab stop with roving tabindex; arrows move within, Tab moves between.
- A role is a promise of the full keyboard model. `role="menu"` on site nav is wrong; use `<nav>` with a list.
- Modals: prefer native `<dialog>` with `showModal()`. Otherwise `inert` on the background, `role="dialog"`, `aria-modal="true"`, `aria-labelledby`. Focus inside on open (least destructive action for confirms), Escape closes, focus returns to the trigger. `overscroll-behavior: contain`.
- `aria-hidden="true"` never on or above a focusable element. Decorative icons and layers get it; decorative layers over controls also need `pointer-events: none`.
- Inputs: a `<label>` (placeholder is never a label), meaningful `autocomplete`, correct `type`/`inputmode`. Never block paste. Label and control share one hit target.
- Errors: keep submit enabled and validate on submit. Failing field gets `aria-invalid="true"` and `aria-describedby` to inline error text; focus the first invalid field. While submitting, disable and show a spinner beside the original label.
- Disabled: native `disabled` when truly unavailable. A tooltip on a `disabled` control never shows; use visible text beside it or `aria-disabled="true"` (then block activation in code and style it). Never both.
- Announcements: if focus moves there, nothing extra. Field-specific: `aria-describedby`. Non-urgent (toasts, "Saved", counts): `role="status"`, rendered empty before text arrives. Urgent untied errors only: `role="alert"`. Never move focus to a toast.
- Alt by purpose: decorative `alt=""` (present, empty); informative describes meaning; functional describes the action (`alt="Search"`, not "magnifying glass"). Missing `alt` reads the file name.
- Structure: one visible `<main>`, headings in an outline, a "Skip to content" link first when chrome precedes main, `scroll-margin-top` on anchor targets. SPA route change: update `document.title`, focus the new `<h1>` (`tabindex="-1"`) or `<main>`.
- Motion: opt in with `@media (prefers-reduced-motion: no-preference)`. Under reduce, swap slides and scales for opacity, kill parallax and autoplay; keep spinners and instant state changes. Anything moving over 5 seconds needs a visible pause. Toasts with an action or error stay until dismissed.
- Touch: gate hover styles with `@media (hover: hover)` so they don't latch after a tap.

## References

- [references/keyboard-and-focus.md](references/keyboard-and-focus.md): load when building custom widgets, dialogs, focus rings or skip links (APG key table, roving tabindex, forced colors).
- [references/forms.md](references/forms.md): load when building forms (autocomplete tokens, inputmode table, error pattern).
- [references/aria-and-screen-readers.md](references/aria-and-screen-readers.md): load for naming, live regions, `sr-only`, SVG, alt text, disabled states and common ARIA mistakes.
- [references/touch-motion-zoom.md](references/touch-motion-zoom.md): load for hit-area expansion, touch-action, reduced motion details, autoplay and rem vs px.

## Reporting

Severity: `HIGH` blocks a task, hides content from assistive tech, or is systemic; `MEDIUM` makes an interaction meaningfully harder; `LOW` is polish. One row per root cause, ordered by severity:

| Severity | Location | Before | After | Why |
| --- | --- | --- | --- | --- |

Mark checks you could not run as `Not verified`. End with `Block` if any `HIGH` remains, otherwise `Approve`. With nothing to report, say "No actionable accessibility findings".
