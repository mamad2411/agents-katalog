---
name: ada-accessibility
description: The team's authoritative build-time accessibility standard for Shopify Dawn-fork themes — WCAG 2.1 AA basics, semantic HTML, ARIA (aria-label/labelledby, roles), keyboard navigation, focus management, screen-reader compatibility, forms, image alt text, and interactive elements (sliders, drawers, modals). Use this skill whenever building or editing interactive elements, forms, images, sliders, accordions, drawers, or modals, and whenever the user mentions accessibility, ADA, WCAG, ARIA, screen readers, keyboard navigation, or focus. BUILD-TIME guidance so code arrives accessible; the qa agent runs the deep axe/keyboard audit against this same file. By project decision, color contrast is settled at the token/color-scheme level and is NOT re-checked per section.
---

# Accessibility Standard (Shopify Dawn-fork)

Single source of truth for accessibility. Build to it so sections arrive clean; the `qa` agent audits the rendered DOM against it. The rendered DOM is the truth for what a screen reader gets.

## Images & media

- Every `<img>` / `image_tag` has an `alt`. Informative images: `alt` describes the content (`alt="Christian Norgaard training kit"`, not the filename). Decorative images: `alt=""` (present but empty) so they're skipped.
- `<svg>` icons that convey meaning have an accessible name (`aria-label` or `<title>`); purely decorative SVGs get `aria-hidden="true"`.

## Headings

- Logical order, no skipped levels (no `h2 → h4`). A section usually starts at `h2`, not a second `h1` (see `seo` skill).
- No empty headings; no text styled to _look_ like a heading that isn't a heading tag.

## ARIA — use sparingly, correctly

- Icon-only buttons/links have an accessible name via `aria-label`.
- Every `aria-labelledby` / `aria-describedby` points to an `id` that exists in the rendered DOM (broken references are a common bug).
- No redundant/conflicting roles (`role="button"` on a real `<button>`), no invalid ARIA values.
- Don't invent ARIA where a native element does the job — a real `<button>`/`<a>` beats a div with `role`.

## Links & buttons

- Links have discernible text; no empty `<a>`, no context-free "click here" / "read more".
- Right element for the job: navigation → `<a href>`, action → `<button>`. Never clickable divs.
- External / new-tab links signal it and use `rel` appropriately.

## Forms & inputs

- Every input has an associated `<label>` (via `for`/`id`) or an `aria-label`. Placeholder text is not a label.
- Error messages are programmatically associated and announced.

## Keyboard & interaction

- All interactive elements are keyboard reachable and operable; logical tab order; no traps; visible focus preserved (never remove outlines without a `:focus-visible` replacement).
- Sliders (Swiper 11): keyboard module enabled, aria-labels on prev/next, accessible pagination, `prefers-reduced-motion` respected (no forced autoplay under it).
- Drawers/modals: focus trapped while open, restored on close, Escape closes, `aria-expanded`/`aria-controls` on triggers.

## Dawn regression guard

Never let a section strip Dawn's built-in `aria-*`, `role`, or `focus-visible` attributes (repo rule). Flag any that were removed.

## Explicitly out of scope

- **Color contrast.** Project decision: settled at the design-token / color-scheme level during intake, not re-litigated per section. The qa agent disables axe's `color-contrast` rule.

## Audit method (used by the qa agent)

Static grep pass for quick wins, then a live axe pass scoped to the section:

```js
// npm i -D @axe-core/playwright
import { chromium } from "playwright";
import { AxeBuilder } from "@axe-core/playwright";
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto("http://127.0.0.1:9292/<page-with-section>");
const results = await new AxeBuilder({ page })
  .include("#shopify-section-<section-id>")
  .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
  .disableRules(["color-contrast"])
  .analyze();
console.log(JSON.stringify(results.violations, null, 2));
await browser.close();
```

axe catches mechanical failures (missing alt, empty buttons, invalid ARIA, heading order). Human judgment adds what axe can't: is the alt _meaningful_, is the link text _descriptive_, does the heading make sense in context.

## Severity (for the qa gate)

- **critical** — blocks a core interaction for assistive tech (icon-only control with no name, unlabeled form field, broken `aria-labelledby`, keyboard trap).
- **serious** — real barrier (missing alt on informative image, skipped heading level, empty link, focus not restored on modal close).
- **moderate** — should fix (decorative image missing `alt=""`, redundant role). Warnings, don't block.

## Honest limit

Automated checks plus review catch the common errors, not all of WCAG. A clean result means "no known common ADA errors," not "fully compliant." Full keyboard walkthroughs and screen-reader reading-order checks still need a human — say so.
