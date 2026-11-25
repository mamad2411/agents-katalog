---
name: web-accessibility
description: Builds and audits web UIs to WCAG 2.2 level AA - semantic HTML, correct ARIA, keyboard and focus handling, accessible forms and errors, alt text, color contrast, target size, dialogs, live regions and motion - and tests with automated tools plus keyboard and screen reader checks. Use when building or reviewing UI components, forms, modals, menus or pages, fixing axe or Lighthouse accessibility issues, or preparing for an accessibility audit or a compliance requirement such as ADA, Section 508, EN 301 549 or the European Accessibility Act.
license: MIT
---

# Web Accessibility

Use native HTML elements first: they bring keyboard support, focus and screen reader semantics for free. ARIA only fills gaps that HTML cannot, and wrong ARIA is worse than none. Automated tools find only part of the problems, so every change also gets a keyboard pass.

## When to use

- Building or reviewing any interactive UI: forms, buttons, menus, tabs, dialogs, tables, carousels.
- Fixing issues reported by axe, Lighthouse, a user, or an audit.
- Teams with a legal or contractual accessibility target (usually WCAG 2.1 or 2.2 AA).

## Workflow

1. **Automated scan.** Run axe (browser extension, `@axe-core/playwright`, `jest-axe`) or Lighthouse on each changed page or component state (open menus, error states, modals). Fix every violation.
2. **Keyboard-only pass.** Unplug the mouse. Tab through everything: is every action reachable, is the order logical, is focus always visible, can you escape every widget, does Esc close overlays, does focus return to a sensible place?
3. **Zoom and reflow.** Zoom to 200% and to a 320 CSS px wide viewport (about 400% zoom on desktop). Content must still work with no horizontal scrolling for text.
4. **Screen reader smoke test** of the main flow: NVDA with Firefox or Chrome on Windows, VoiceOver with Safari on macOS or iOS, TalkBack on Android. Check that names, roles, states and announcements make sense.
5. **Contrast check** of text, icons, focus indicators and form borders.
6. **Add an automated a11y test** for the component or page to CI, so the fix stays fixed.

## Semantic HTML first

| Need | Use | Not |
|---|---|---|
| Action on the page | `<button type="button">` | `<div onclick>`, `<a href="#">` |
| Navigation to a URL | `<a href="/path">` | `<button>` that calls `router.push` with no link |
| Page regions | `<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>` | Generic `<div>`s only |
| Headings | `<h1>`–`<h6>` in order, one `<h1>` per page | Bold text styled as a heading |
| Lists | `<ul>`, `<ol>`, `<li>` | Divs with bullets drawn in CSS |
| Data table | `<table>`, `<th scope>`, `<caption>` | CSS grid of divs for tabular data |
| On/off choice | `<input type="checkbox">` | Clickable `<div>` with an icon |
| Modal dialog | `<dialog>` with `showModal()` | Hand-built overlay without focus handling |
| Expand/collapse | `<details>`/`<summary>`, or a button with `aria-expanded` | Clickable heading with no state |

## Rules of ARIA

1. If a native element does the job, use it instead of ARIA.
2. Don't change native semantics (`<h2 role="button">`); wrap instead.
3. Every interactive ARIA control must work with the keyboard. `role="button"` needs `tabindex="0"` and Enter and Space handling, which is why `<button>` is better.
4. Never put `aria-hidden="true"` on a focusable element or its ancestor.
5. Every interactive element needs an accessible name (visible label, `aria-label` or `aria-labelledby`). The visible label text must be part of the accessible name.

For widgets HTML lacks (tabs, combobox, menu button, tree), follow the WAI-ARIA Authoring Practices patterns in [references/component-patterns.md](references/component-patterns.md).

## Keyboard and focus

- Everything that works with a mouse works with a keyboard. No keyboard traps.
- Focus order follows the visual and reading order. Don't use `tabindex` greater than 0.
- Focus is always visible. Never remove `outline` without a replacement; prefer `:focus-visible` styling with at least 3:1 contrast against the background.
- Focus is not hidden behind sticky headers, footers or cookie banners (WCAG 2.2). Use `scroll-padding-top` equal to the sticky header height.
- Provide a "Skip to main content" link as the first focusable element on pages with repeated navigation.
- In single-page apps, on route change: update `document.title` and move focus to the new page's `<h1>` (with `tabindex="-1"`) or announce the change.

## Forms

- Every input has a visible `<label for>` (or wraps the input). Placeholder text is not a label.
- Group related radios and checkboxes in `<fieldset>` with a `<legend>`.
- Mark required fields with the `required` attribute and a visible indicator explained once.
- Errors: show text next to the field (not color alone), set `aria-invalid="true"`, link the message with `aria-describedby`, and on submit move focus to the first invalid field or to an error summary that links to each field.
- Use `autocomplete` tokens for personal data (`name`, `email`, `tel`, `street-address`, `postal-code`, `current-password`, `new-password`, `one-time-code`).
- Don't block paste or password managers, and don't require puzzles or memorizing to log in (WCAG 2.2 Accessible Authentication).
- Don't make users re-enter information they already gave in the same flow (WCAG 2.2 Redundant Entry).

```html
<label for="email">Email address</label>
<input id="email" name="email" type="email" autocomplete="email" required
       aria-invalid="true" aria-describedby="email-error">
<p id="email-error">Enter an email address like name@example.com</p>
```

## Images and alt text

| Image | `alt` |
|---|---|
| Informative (photo, illustration that adds meaning) | Describe what matters in context, briefly |
| Functional (the only content of a link or button) | Describe the action or destination ("Search", "Home") |
| Decorative | `alt=""` (empty, not missing) |
| Complex (chart, diagram) | Short `alt` plus the data or a full description nearby |
| Image of text | The same text (and prefer real text) |

Don't start with "image of". Icon-only buttons need an accessible name: `<button aria-label="Close">` with the SVG marked `aria-hidden="true"`.

## Color, contrast and size

- Text contrast at least **4.5:1**; large text (24 px regular, or about 18.7 px bold, and up) at least **3:1**.
- Non-text contrast at least **3:1** for UI component boundaries, focus indicators, icons and chart elements that convey meaning.
- Never use color alone to convey information (errors, required fields, chart series). Add text, icons or patterns.
- Pointer targets at least **24 × 24 CSS px**, or with enough spacing that a 24 px circle around each doesn't overlap another (WCAG 2.2 Target Size Minimum).
- Text must survive the WCAG text-spacing overrides and 200% zoom without clipping.

## Dynamic content

- Status messages (saved, 3 results found, added to cart) go in a live region that exists in the DOM before the update: `<div role="status">`. Use `role="alert"` only for urgent errors.
- Don't announce everything; announcement spam is as bad as silence.
- Loading states: set `aria-busy="true"` on the region being updated, and announce completion if it is not obvious.

## Dialogs

```html
<button type="button" id="delete-btn">Delete project</button>
<dialog id="confirm-delete" aria-labelledby="confirm-title">
  <h2 id="confirm-title">Delete this project?</h2>
  <p>This cannot be undone.</p>
  <form method="dialog">
    <button value="cancel">Cancel</button>
    <button value="delete">Delete</button>
  </form>
</dialog>
<script>
  const dialog = document.getElementById("confirm-delete");
  const opener = document.getElementById("delete-btn");
  opener.addEventListener("click", () => dialog.showModal());
  dialog.addEventListener("close", () => opener.focus());
</script>
```

`showModal()` makes the rest of the page inert, closes on Esc and moves focus into the dialog. Browser behavior for returning focus on close varies, so restore it to the opener explicitly as above; check the target browsers if relying on the default. For custom overlays, use the `inert` attribute on the background instead of hand-written focus traps.

## Motion and media

- Respect `prefers-reduced-motion`: disable or reduce parallax, auto-scrolling and large animations.
- Anything that moves, blinks or auto-updates for more than 5 seconds needs a pause control. Nothing flashes more than 3 times per second.
- Video has captions; audio-only content has a transcript. Don't auto-play audio.

## Testing in CI

```ts
import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test("checkout page has no detectable WCAG A/AA violations", async ({ page }) => {
  await page.goto("/checkout");
  const results = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"])
    .analyze();
  expect(results.violations).toEqual([]);
});
```

Also useful: `jest-axe` or `vitest-axe` for component tests, `eslint-plugin-jsx-a11y` for JSX, and Testing Library `getByRole` queries (they fail when names and roles are wrong). Passing automated checks does not mean the UI is accessible; keep the keyboard and screen reader steps.

## Anti-patterns

- **Clickable `div`s and `span`s** instead of buttons and links.
- **`outline: none`** with no visible replacement.
- **Positive `tabindex`** to "fix" order. Fix the DOM order instead.
- **Redundant or conflicting ARIA** (`<button role="button">`, `aria-label` that differs from the visible label).
- **Placeholder as the only label.**
- **Color-only status** (red border with no text).
- **`role="menu"` for site navigation.** Use a list of links, with disclosure buttons for submenus.
- **Accessibility overlay widgets** as a fix; they don't repair the underlying markup.
- **Custom controls that ignore Space, Enter, Esc or arrow keys** that users expect from the pattern.
- **Hiding content with `display: none` and expecting screen readers to read it.** Use a visually-hidden utility class for screen-reader-only text.

## Done when

- axe reports no violations for every changed page and component state.
- The full flow works with keyboard only, with visible focus that is never obscured.
- Contrast, target size and zoom/reflow checks pass.
- A screen reader announces correct names, roles, states and status messages for the main flow.
- An automated accessibility test covers the change in CI.

## References

- [references/component-patterns.md](references/component-patterns.md) — read when building or reviewing a custom widget (tabs, menu button, combobox, accordion, disclosure, tooltip, toast, carousel, dialog) to get the roles, states and keyboard behavior right.
