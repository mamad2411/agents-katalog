---
name: audit-accessibility-wcag
description: Audits and fixes markup/JSX for WCAG 2.2 AA compliance — alt text, ARIA, heading order, contrast, keyboard nav, focus management; used before shipping UI or preparing an a11y review.
when_to_use: When the user wants an accessibility (a11y) check or fix, mentions WCAG, screen readers, ARIA, keyboard navigation, color contrast, or is preparing for an accessibility audit.
---

## When to Use

Trigger this skill when the task is to audit or fix UI for accessibility: WCAG 2.2 AA, screen readers, ARIA, keyboard nav, color contrast, focus management, or preparing an a11y review.

NOT this skill: pure visual/layout polish (no a11y intent), or security/XSS concerns — that is `security-review`. ARIA/role injection that touches `dangerouslySetInnerHTML` or user-controlled markup overlaps both; flag the a11y part here and hand the injection risk to `security-review`.

## Steps

Work in this order. Earlier rules outrank later ones — never reach for ARIA to patch a problem that semantic HTML already solves.

1. **Scope the surface.** Identify the files/components in the diff or named target. Grep for the smells that produce most findings: `rg -n 'role=|aria-|onClick=|<div|<span|tabindex|tabIndex|alt=|<img|placeholder='` across the target. Build a checklist; do not audit the whole repo unless asked.

2. **Semantic HTML first.** Replace `<div onClick>` / `<span onClick>` with a real `<button type="button">`. Use `<a href>` only for navigation (has a destination), `<button>` for actions (no navigation). Use `<nav>`, `<main>`, `<header>`, `<footer>`, `<ul>/<li>`, `<table>` over `<div role="...">`. One `<main>` per page. A native element is keyboard-operable and announced for free; a styled `div` is not.

3. **Images & icons.** Every `<img>` needs `alt`. Informative image → describe its meaning (`alt="Quarterly revenue up 12%"`), not the filename. Decorative/redundant image → `alt=""` (empty, not missing — missing alt makes SRs read the URL). Icon-only buttons need an accessible name via `aria-label` or visually-hidden text; an inline SVG that conveys meaning needs `role="img"` + `aria-label`, a decorative one needs `aria-hidden="true"`.

4. **Heading hierarchy.** Exactly one `<h1>`. No skipped levels (h2 → h4 is a fail; reflows the SR outline). Headings describe structure, not font size — never pick a level for its default styling. Don't fake headings with bold `<p>`/`<div>`.

5. **ARIA only where native fails.** First rule of ARIA: don't use ARIA. Apply it only for patterns HTML can't express (tabs, comboboxes, live regions, disclosure). When you do: every `role` must carry its required states (e.g. `role="tab"` needs `aria-selected` + `aria-controls`; `aria-expanded` on every disclosure/menu trigger; `role="dialog"` needs `aria-modal="true"` + `aria-labelledby`). Never put an interactive role on a non-interactive element without also making it focusable (`tabindex="0"`) and key-handled. Remove redundant roles (`role="button"` on a `<button>`).

6. **Forms.** Every input has a programmatic label: `<label for>` / `htmlFor`, wrapping `<label>`, or `aria-label`/`aria-labelledby`. Placeholder is NOT a label (vanishes on input, low contrast). Required → `required` + visible indicator. Errors: link the message with `aria-describedby` on the field, set `aria-invalid="true"`, and announce dynamic errors via an `aria-live="polite"` (or `role="alert"` for assertive) region. Group radios/related fields in `<fieldset>` + `<legend>`.

7. **Color contrast (WCAG 2.2 AA).** Body text ≥ 4.5:1; large text (≥ 24px, or ≥ 18.66px bold) ≥ 3:1; UI components, icons, and focus indicators ≥ 3:1 against adjacent colors. Compute ratios from the actual hex values (resolve CSS vars/Tailwind tokens to real colors first). Never rely on color alone to convey state — pair it with text/icon/shape. Check disabled, hover, and dark-mode states too.

8. **Keyboard.** Everything operable by mouse must work by keyboard. Tab order follows DOM order — fix with DOM/flexbox `order` reasoning, never positive `tabindex` (1+). `tabindex="-1"` = focusable by script only; `0` = in natural order. Every interactive element needs a visible focus indicator — do NOT `outline: none` without a replacement (`:focus-visible` ring). Add a "Skip to main content" link as the first focusable element. No keyboard traps (you can Tab out of every widget). Custom widgets implement expected keys (Esc closes, Arrow keys move within tabs/menus/listbox per ARIA APG).

9. **Focus management (dynamic UI).** On modal/dialog open: move focus into it, trap Tab within it, restore focus to the trigger on close, Esc closes. On client-side route change: move focus to the new page's `<h1>` or a focusable container so SR users aren't stranded. Toasts/async results → announce via live region, don't steal focus mid-task.

10. **Report.** Output a prioritized list grouped **Blocker → Major → Minor**, each entry = file:line, the WCAG criterion (e.g. 1.1.1, 2.4.7), the concrete problem, and a copy-pasteable fix (before → after). Blocker = blocks a user from completing a task (unlabeled control, keyboard trap, no focus on modal). Major = significant barrier (contrast fail, skipped heading). Minor = friction (redundant role, missing `lang`). Apply the fixes when asked; otherwise leave them as ready-to-paste diffs.

## Common Errors

- `alt=""` vs missing `alt` — empty is intentional "decorative, skip me"; missing makes SRs announce the file path. Not interchangeable.
- Placeholder used as the only label. Fails 1.3.1/4.1.2 and disappears once typing starts.
- `outline: none` / `outline: 0` in a CSS reset with no `:focus-visible` replacement — silently removes the focus ring for keyboard users. Single most common keyboard fail.
- Positive `tabindex` ("1", "2"…) to "fix" order — creates a brittle parallel tab sequence ahead of everything else. Fix DOM order instead.
- `aria-label` on a non-interactive, non-`role`'d element (plain `<div>`/`<span>`/`<p>`) — most SRs ignore it. The name needs an element that takes a name.
- `role="button"` on a `<div>` without `tabindex="0"` AND `onKeyDown` for Enter/Space — looks clickable, dead to keyboard. Just use `<button>`.
- Click handler only on the icon `<svg>`/`<i>` inside a control — enlarge the hit target and put the handler + name on the `<button>`.
- `aria-hidden="true"` on a focusable element (or an ancestor of one) — hides it from SRs while it stays in the tab order: a focusable ghost. Never wrap interactive content in `aria-hidden`.
- Live region added to the DOM at the same time as its message — SRs only announce changes to an *already-present* region. Render the empty `aria-live` container first, then inject text.
- Tailwind/utility color audit done on class names — `text-gray-400 on bg-white` is not a contrast value. Resolve to hex, then compute the ratio.
- Trusting the linter as "done" — `eslint-plugin-jsx-a11y`/axe catch static markup issues only. They cannot see contrast against rendered backgrounds, focus order, trap behavior, or whether a name actually makes sense. Keyboard/SR behavior needs manual or automated runtime checks.

## Verify

Static (always): `rg -n 'outline:\s*(none|0)|tabindex=["\x27][1-9]|aria-hidden=["\x27]true' <target>` returns no unjustified hits. If the project has it, run `npx eslint --no-eslintrc --plugin jsx-a11y` (or the existing a11y lint task) → zero errors. Confirm exactly one `<h1>` and no skipped heading levels.

Runtime (when a browser is available): load the page, run an axe-core scan (or `lighthouse` accessibility category) and capture the score + violations. Then keyboard-walk it: Tab from the top — every interactive element is reachable, in logical order, with a *visible* focus ring; the skip link appears first; open a modal and confirm focus enters it, Tab is trapped, Esc closes, and focus returns to the trigger.

Contrast: for each flagged pair, state the computed ratio and the threshold it must clear (4.5:1 / 3:1) — a fix isn't done until the number passes.

Report is complete only when every Blocker has a concrete code fix attached (not just a description) and each finding cites its WCAG success criterion.
