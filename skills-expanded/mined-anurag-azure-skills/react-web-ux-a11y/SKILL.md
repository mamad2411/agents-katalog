---
name: "react-web-ux-a11y"
description: "React web UX + accessibility (WCAG 2.1 AA): semantic HTML, labels, focus management, keyboard nav, live regions, loading/empty/error states, color-not-alone. Use when building or reviewing React web UI for accessibility and UX quality."
version: 1
created: "2026-07-10"
updated: "2026-07-10"
---

# React Web UX & Accessibility (WCAG 2.1 AA)

## Semantics & structure
- Landmarks: `header`, `nav`, `main`, `footer`. One `h1` per page; logical heading order.
- Native elements over ARIA: `button` for actions, `a` for navigation, real `input`/`select`/`textarea`.

## Forms
- Every input has a visible `<label htmlFor>`; group with `fieldset`/`legend` where relevant.
- Errors linked via `aria-describedby`; announce via `aria-live="polite"` (assertive for blocking errors).
- Disable submit while pending; show inline field errors; never validate by color alone.

## State (never blank)
- Every async surface renders loading / empty / error / loaded — no `return null` for a state.
- Skeletons for loading; `EmptyState` with a CTA; inline error with retry; toasts (`aria-live`) for non-blocking notices.

## Color & indicators
- Never convey status/priority by color alone — always pair color with a text label.
- Contrast: 4.5:1 body text, 3:1 large text / UI components.

## Keyboard & focus
- All interactive elements reachable via Tab in logical order; visible focus ring on every one.
- Dialogs/menus: trap focus while open, restore focus to the trigger on close; `Esc` closes.
- Skip-to-main-content as the first focusable element.

## Motion & media
- Respect `prefers-reduced-motion`; keep essential motion under ~400ms.
- Images have `alt`; decorative images `alt=""`; icon-only buttons have `aria-label`.

## Quality gates
- Automated a11y checks (axe / jest-axe) on key screens; no critical violations.
- Manual: keyboard-only pass and screen-reader labels on all controls.
