---
name: a11y
description: Accessibility conventions — semantic HTML, keyboard support, focus management, ARIA, testing. Use when building UI components, forms, dialogs, navigation, or fixing a11y violations. 日本語の依頼例:「アクセシビリティ対応して」「キーボード操作できるように」「フォーカス管理」「スクリーンリーダー対応」「コントラスト」。
---

# Accessibility

Target: WCAG 2.2 AA. A11y is a build-time concern, not an audit-time patch.

## Semantic HTML first

- Use the element that does the job: `<button>` for actions, `<a href>` for navigation, `<label>`+input for forms, `<nav>/<main>/<header>` landmarks, real heading hierarchy (one `<h1>`, no level skipping).
- A `<div onClick>` is never acceptable for an action — it has no keyboard support, no role, no focus. If a design demands a non-button look, style a `<button>`.
- First rule of ARIA: don't use ARIA when an HTML element provides the semantics. ARIA adds promises (keyboard behavior) that you must then implement by hand.

## Keyboard

- Everything operable by mouse is operable by keyboard: Tab reaches it, Enter/Space activates it, Escape dismisses overlays, arrow keys move within composite widgets (menus, tabs, listboxes).
- Visible focus indicator always — never `outline: none` without an equal-or-better `:focus-visible` style (use a token, see `css-modules`).
- DOM order = visual order = tab order. Don't fix layout problems with `tabindex` > 0 (banned).

## Focus management (SPAs & overlays)

- Dialogs/drawers: focus moves in on open, is trapped while open, returns to the trigger on close. Prefer native `<dialog>` or a headless library (React Aria, Radix) over hand-rolling — focus traps are notoriously buggy.
- Client-side route change: move focus to the new page's heading (or announce via live region) — silent navigation strands screen-reader users.
- Content removal: if the focused element disappears, move focus somewhere sensible, not `<body>`.

## Forms

- Every input has a programmatic label (`<label htmlFor>`); placeholder is not a label.
- Errors: associate with the field via `aria-describedby`, set `aria-invalid`, and on submit failure move focus to the first error or an error summary. Error text says how to fix, not just "invalid".
- Don't disable the submit button as the only validation feedback — disabled buttons explain nothing.

## Content & visuals

- Contrast: text ≥ 4.5:1 (3:1 for large text), UI component boundaries ≥ 3:1. Check tokens once in `tokens.css`, inherit everywhere.
- Color never the sole signal — pair with text/icon (error = red AND icon + message).
- Meaningful images need `alt` describing function; decorative ones `alt=""`. Icon-only buttons need `aria-label`.
- Async updates (toasts, validation, loading→loaded) announce via `aria-live="polite"` regions that exist in the DOM before the update.
- Respect `prefers-reduced-motion` for any significant animation.

## Testing

- Automated catches ~30–40%: axe in Storybook (a11y addon, failing) + `@axe-core/playwright` on key pages. Zero serious/critical violations.
- The rest is manual: keyboard-walk every new interactive component (Tab/Enter/Escape/arrows) as part of done.
- Writing tests with `getByRole(…, { name })` (per `testing-vitest`) doubles as an a11y check — if the role query can't find it, assistive tech can't either.
