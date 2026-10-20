---
name: ux-wcag-a11y
description: Use when building or auditing web UI for accessibility — WCAG 2.2 AA, keyboard, screen readers, semantic HTML, ARIA, contrast, focus management.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: domain
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-17"
  related: [ux-essentials, frontend-design-essentials]
---

# WCAG 2.2 AA Accessibility

**Iron Law: keyboard nav works for every interactive element. Color contrast meets AA. Semantic HTML before ARIA.**

Accessibility is correctness, not a feature. A site that breaks for keyboard users is broken — the same way a site that 500s for 10% of requests is broken. Target WCAG 2.2 Level AA (supersedes 2.1 as of Oct 2023; backward-compatible — meeting 2.2 satisfies 2.1). AAA is aspirational; AA is the legal floor in most jurisdictions.

## The five-minute test

Before any deep audit:

1. **Unplug your mouse.** Reach every interactive element with `Tab` / `Shift+Tab`. See the focus ring.
2. **OS screen reader on** (VoiceOver: `Cmd+F5`). Does it announce sensibly?
3. **Zoom to 200%.** Layout still works?
4. **Run axe-core / Lighthouse a11y.** Fix the criticals.

Four passes = ~80% of common failures gone.

## Semantic HTML first

ARIA is a patch over HTML's gaps. Use the right element and you need almost no ARIA.

| Need             | Use                                                       |
| ---------------- | --------------------------------------------------------- |
| Clickable action | `<button>` — **not** `<div onclick>`                      |
| Navigation       | `<a href>` — **not** `<span onclick>`                     |
| Checkbox         | `<input type="checkbox">`                                 |
| Form fields      | `<input>`, `<select>`, `<textarea>` with `<label>`        |
| Headings         | `<h1>`–`<h6>` in order, no skipping. One `<h1>` per page. |
| Landmarks        | `<nav>`, `<main>`, `<aside>`, `<footer>`                  |
| Tabular data     | `<table>` + `<th scope="col\|row">`                       |

Real form controls get keyboard, focus, labels, and screen-reader semantics for free.

## ARIA — sparingly

> The first rule of ARIA: don't use ARIA.

Use it when semantic HTML can't express the pattern (custom widgets, live regions, dynamic state).

| Need                          | Use                                                |
| ----------------------------- | -------------------------------------------------- |
| Announce dynamic changes      | `aria-live="polite"` (`assertive` only for urgent) |
| Label an icon-only button     | `aria-label="Close"`                               |
| Mark current page in nav      | `aria-current="page"`                              |
| Expanded/collapsed disclosure | `aria-expanded="true\|false"` on the trigger       |
| Connect control to label      | `aria-labelledby` / `aria-describedby`             |
| Hide decorative element       | `aria-hidden="true"` (truly decorative only)       |

**Don't** put `role="button"` on a `<div>` and call it done. You also need `tabindex="0"`, `Enter` + `Space` handlers, and focus styles. Use `<button>` and skip the headache.

### Decision tree

```
Is there a native HTML element for this? → use it. Done.
   └── No → Is the pattern in the WAI-ARIA Authoring Practices? → follow it exactly.
        └── No → reconsider the design. Custom widget = custom a11y debt.
```

## Keyboard

- Every interactive element reachable with `Tab`.
- Focus order matches visual order.
- Focus **visible** — never `outline: none` without a replacement. 2px ring, 3:1 contrast against background, minimum.
- Modals trap focus inside until dismissed; return focus to the trigger on close.
- `Esc` closes dialogs, menus, popovers.
- No keyboard traps (places where `Tab` won't get you out).

## Color and contrast

| Element                          | Minimum ratio |
| -------------------------------- | ------------- |
| Normal text vs background        | 4.5:1         |
| Large text (18pt+ or 14pt bold)  | 3:1           |
| UI components, graphical objects | 3:1           |
| Focus indicator vs background    | 3:1           |

**Don't rely on color alone.** Pair with shape, icon, or text. Red/green colorblindness is ~8% of men. Run any palette through a contrast checker — eyeballing it is a coin flip.

## Images and media

- Every `<img>` has `alt`. Decorative? `alt=""` (empty, **not** missing). Informative? Describe the _function_ ("Submit" not "blue rectangle").
- Complex images (charts, infographics) need a long description nearby.
- Video has captions; audio has a transcript.
- Auto-playing media has a pause control and ideally doesn't autoplay.

## Forms

- Every input has a `<label>`. **Placeholder is not a label.**
- Required fields marked in text (`*` + `aria-required="true"` + the word "required" in instructions).
- Errors associated via `aria-describedby`. Don't only color the border red — announce the error.
- Group radio buttons with `<fieldset>` + `<legend>`.

## Focus management in SPAs

Single-page apps break native focus. Put it back:

- **Route change:** focus the `<h1>` of the new page (or a skip-to-main link).
- **Modal open:** focus the first interactive element inside; trap until close.
- **Modal close:** return focus to the trigger element.
- **Dynamic insert (important):** announce with `aria-live`.

## Semantic equivalents — what to use instead

| Custom thing          | Native equivalent                                                                         |
| --------------------- | ----------------------------------------------------------------------------------------- |
| `<div onclick>`       | `<button>`                                                                                |
| `<span class="link">` | `<a href>`                                                                                |
| Custom checkbox div   | `<input type="checkbox">` + `<label>`                                                     |
| Custom dropdown div   | `<select>` (or full ARIA combobox if you must)                                            |
| Custom modal div      | `<dialog>` element (with polyfill if needed), or proven a11y library (Radix, Headless UI) |
| Tooltip span          | `<button>` + `aria-describedby` pointing to the tooltip                                   |

## Responsive and zoom

- Layout works at 200% zoom without horizontal scroll (tables/maps excepted).
- Touch targets ≥ 24×24 CSS px (WCAG 2.2 AA); aim for 44×44 (see `Skill(ux-essentials)` mobile-first).
- Text resizing doesn't break layout.

## Tools

- **axe DevTools** — best automated catch rate (~30-40% of issues).
- **Lighthouse a11y** — built into Chrome.
- **WAVE** — visual annotation.
- **VoiceOver / NVDA / JAWS** — actual screen-reader testing. No tool replaces this.
- **Keyboard only** — `Cmd/Ctrl+L`, then `Tab` through the page.

Automated tools catch ~30-40% of issues. The rest requires human testing.

## Common failures

| Symptom                            | Fix                                           |
| ---------------------------------- | --------------------------------------------- |
| `<div onclick>` everywhere         | Replace with `<button>`                       |
| `placeholder` used as label        | Add real `<label>`                            |
| Focus invisible                    | Remove `outline: none` or add custom ring     |
| Modal doesn't trap focus           | Use a proven a11y dialog (Radix, Headless UI) |
| Icon button with no label          | Add `aria-label`                              |
| Error only shown in red            | Add text + `aria-describedby`                 |
| Toast not announced                | Wrap in `aria-live="polite"` region           |
| Heading skip from `<h1>` to `<h4>` | Reorder; use CSS for size, not heading level  |

## Anti-patterns

- `role="button"` on a `<div>` (use `<button>`)
- `aria-label` to compensate for missing semantic HTML
- Removing focus outlines for "design reasons" without a replacement
- Color as the only signal of state
- Auto-focus inside modals onto an Esc-only-closeable element with no Cancel button
- `tabindex` values > 0 (forces order, breaks expectations)
- ARIA on `<button>` to "improve" it — `<button>` already announces

## Hand-off

For broader usability and mobile constraints: `Skill(ux-essentials)`. For component architecture that ships a11y by default + tokenized design systems with contrast-checked palettes: `Skill(frontend-design-essentials)`.
