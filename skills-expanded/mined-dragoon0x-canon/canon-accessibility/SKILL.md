---
name: canon-accessibility
description: Use when designing or auditing accessibility, ARIA, semantic HTML, screen reader support, keyboard navigation, color contrast, motion preferences, or WCAG compliance. Trigger when the user mentions a11y, accessibility, ARIA, screen reader, WCAG, keyboard, focus, or asks to make something accessible.
---

# CANON · Accessibility

Accessibility is not a layer applied at the end. It is the substrate. Every other design decision either supports it or undermines it. WCAG 2.2 AA is the floor.

## The Four POUR Principles

WCAG organizes everything around four principles:

| Principle | Means |
|---|---|
| **Perceivable** | Information must be presentable in ways users can perceive (text, alt text, captions, contrast) |
| **Operable** | UI components must be operable by all users (keyboard, time, no seizure triggers) |
| **Understandable** | Information and operation must be understandable (predictable, error prevention) |
| **Robust** | Content must work with current and future assistive tech (semantic HTML, valid markup) |

## Semantic HTML First, ARIA Second

| Need | Use this | Not this |
|---|---|---|
| Clickable action | `<button>` | `<div onclick>` |
| Navigation to URL | `<a href>` | `<button>` or `<div>` |
| Form input | `<input>`, `<textarea>`, `<select>` | custom div with contenteditable |
| Heading | `<h1>`–`<h6>` | `<div class="heading">` |
| List | `<ul>`, `<ol>`, `<li>` | `<div>` collection |
| Section | `<section>`, `<article>`, `<nav>`, `<aside>`, `<main>`, `<header>`, `<footer>` | `<div>` |
| Table of data | `<table>`, `<thead>`, `<tbody>`, `<th scope>` | `<div>` grid |

**The first rule of ARIA: don't use ARIA.** If a native element does the job, use it. ARIA is for what HTML can't express.

## Required Page Structure

```html
<!DOCTYPE html>
<html lang="en">  <!-- lang is mandatory -->
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Page-Specific Title</title>
</head>
<body>
  <a href="#main" class="sr-only-focusable">Skip to main content</a>
  <header>
    <nav aria-label="Primary"> ... </nav>
  </header>
  <main id="main">
    <h1>One H1 per page</h1>
    ...
  </main>
  <footer> ... </footer>
</body>
</html>
```

| Element | Why |
|---|---|
| `lang` attribute | Screen reader pronunciation |
| Skip link | Keyboard users bypass nav |
| One `<h1>` per page | Document outline |
| `<main>` landmark | Screen reader jump-to |
| `<nav aria-label>` | Distinguish multiple navs |

## Heading Hierarchy

```
H1 → H2 → H3 → H4 → H5 → H6
```

**Rules:**
- One H1 per page (page title)
- Don't skip levels (H1 → H3 is wrong)
- Use level for semantic depth, not visual size
- Style independently of level (H2 can look smaller than H3 if hierarchy demands)

Screen readers navigate by heading level. Skipping levels breaks the document outline.

## Color Contrast (recap)

| Text size | Minimum | Source |
|---|---|---|
| Normal (< 18.66px regular, < 14px bold) | 4.5:1 | WCAG 1.4.3 |
| Large (≥ 18.66px regular, ≥ 14px bold) | 3:1 | WCAG 1.4.3 |
| UI components, focus rings, icons | 3:1 | WCAG 1.4.11 |

See **canon-color** for full color guidance.

## Focus Management

```css
:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}
```

| Rule | Why |
|---|---|
| Use `:focus-visible`, not `:focus` | Keyboard users see ring; mouse users don't |
| Never `outline: none` without replacement | WCAG 2.4.7 violation |
| Focus ring contrast >= 3:1 against adjacent | WCAG 1.4.11 |
| Focus must be visible after every action | WCAG 2.4.7 |
| Tab order = DOM order | Don't use positive tabindex |
| Focus trapped in modals | WAI-ARIA modal pattern |
| Focus restored on modal close | Standard expectation |

See **canon-interaction** for full focus and keyboard guidance.

## Forms

```html
<label for="email">Email address</label>
<input
  id="email"
  type="email"
  required
  aria-describedby="email-hint email-error"
  aria-invalid="false"
  autocomplete="email"
/>
<span id="email-hint">We'll never share your email.</span>
<span id="email-error" aria-live="polite"></span>
```

| Pattern | Why |
|---|---|
| `<label for>` linked to input | Click label focuses input; SR reads label |
| `aria-describedby` | Hints and errors announced |
| `aria-invalid="true"` on error | SR announces error state |
| `aria-live="polite"` on error message | SR reads error when it appears |
| `autocomplete` | Browser fills correctly; SR uses for purpose |
| `required` attribute | Native validation, no JS needed |
| Error messages text, not color alone | WCAG 1.4.1 |

See **canon-forms** for complete form guidance.

## Images and Media

| Image type | Alt text |
|---|---|
| Informative (conveys info) | Describe the info: "Bar chart showing Q3 revenue up 12%" |
| Decorative | `alt=""` (empty) — screen readers skip |
| Functional (button, link) | Describe the action: "Search" not "magnifying glass" |
| Complex (chart, diagram) | Short alt + long description nearby |

```html
<!-- Informative -->
<img src="chart.png" alt="Q3 revenue grew 12% over Q2, with strong gains in enterprise sales.">

<!-- Decorative -->
<img src="divider.png" alt="">

<!-- Functional -->
<button><img src="search.svg" alt="Search"></button>

<!-- Complex -->
<img src="org-chart.png" alt="Organizational chart" aria-describedby="chart-desc">
<div id="chart-desc">CEO at top, with 4 VPs reporting...</div>
```

**Video/audio:** captions for video, transcripts for audio. WCAG 1.2.

## ARIA: When to Use

ARIA roles and properties exist for what HTML can't express:

| Need | ARIA |
|---|---|
| Custom button (use `<button>` instead) | `role="button"` (last resort) |
| Custom checkbox | `role="checkbox"` + `aria-checked` |
| Custom tab interface | `role="tablist"` + `role="tab"` + `aria-selected` |
| Disclosure widget | `aria-expanded` on the trigger |
| Live updates | `aria-live="polite"` or `"assertive"` |
| Hidden from SR (decorative) | `aria-hidden="true"` |
| Label that isn't visible | `aria-label="..."` |
| Label provided by another element | `aria-labelledby="id"` |
| Description for complex content | `aria-describedby="id"` |

**Don't combine ARIA with native semantics.** `<button role="button">` is redundant. `<a href role="link">` is wrong.

## Keyboard Navigation

| Component | Required keys |
|---|---|
| Modal | Esc closes, Tab traps inside, focus restored on close |
| Tabs | Arrow Left/Right between tabs, Tab into panel |
| Menu | Arrow Up/Down between items, Esc closes, Tab leaves |
| Combobox | Arrow Down opens, type filters, Enter selects |
| Dialog | Esc closes, focus trapped |
| Slider | Arrow keys adjust, Home/End jump to min/max, Page Up/Down for larger jumps |
| Carousel | Arrow keys navigate, Pause/Play button required if auto-rotates |

See WAI-ARIA Authoring Practices for the canonical pattern of each.

## Motion Preferences

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

**Mandatory in every project.** WCAG 2.3.3.

## Color Preferences

```css
@media (prefers-color-scheme: dark) {
  /* dark theme */
}

@media (forced-colors: active) {
  /* Windows High Contrast Mode */
  /* Don't override user color choices */
}
```

## Touch Target Size

| Standard | Size |
|---|---|
| WCAG 2.5.8 (AA) | 24 × 24 px |
| WCAG 2.5.5 (AAA) | 44 × 44 px |
| Apple HIG | 44 × 44 pt |
| Material 3 | 48 × 48 dp |

**Use 44 × 44 as the floor.** See **canon-spatial** and **canon-interaction**.

## Common WCAG 2.2 Success Criteria (the most-failed)

| SC | Name | Failure |
|---|---|---|
| 1.1.1 | Non-text Content | Missing alt text |
| 1.3.1 | Info and Relationships | Visual headings without `<h>` tags |
| 1.4.3 | Contrast (Minimum) | Body text < 4.5:1 |
| 1.4.10 | Reflow | Horizontal scroll at 320px |
| 1.4.11 | Non-text Contrast | Focus rings, icons < 3:1 |
| 2.1.1 | Keyboard | Mouse-only interactions |
| 2.4.4 | Link Purpose | "Click here", "Read more" |
| 2.4.7 | Focus Visible | `outline: none` without replacement |
| 2.5.8 | Target Size (Minimum) | Tap targets < 24×24 |
| 3.3.2 | Labels or Instructions | Inputs without labels |
| 4.1.2 | Name, Role, Value | Custom widgets without ARIA |

## Anti-Patterns

| Anti-pattern | WCAG violation | Fix |
|---|---|---|
| `<div onclick>` for buttons | 2.1.1, 4.1.2 | Use `<button>` |
| `outline: none` | 2.4.7 | Use `:focus-visible` with custom ring |
| Placeholder as label | 3.3.2 | Use `<label>` |
| "Click here" link text | 2.4.4 | Describe the destination |
| Color as only signal | 1.4.1 | Add icon, weight, or label |
| Auto-playing video with sound | 1.4.2 | Mute by default; provide control |
| Carousel auto-rotates without pause | 2.2.2 | Add pause; default to no auto-rotate |
| Time-limited forms | 2.2.1 | Provide extension |
| Modal focus escapes | WAI-ARIA modal | Implement focus trap |
| Empty alt on informative image | 1.1.1 | Add descriptive alt |
| Long alt on decorative image | 1.1.1 | Use `alt=""` |
| Multiple H1s | 1.3.1 | One per page |
| Skipping heading levels | 1.3.1 | Don't skip |
| Form errors that disappear | 3.3.1 | Persistent error message |

## Audit Checklist

1. Run **axe DevTools** or **Lighthouse Accessibility audit**. Score should be 95+.
2. Tab through every interactive element. Visible focus ring? Logical order?
3. Use a screen reader for 5 minutes (VoiceOver on Mac, NVDA on Windows). Pages make sense?
4. Zoom to 200%. Layout still works? No content cut off?
5. Check every form. Labels associated? Errors descriptive? `aria-describedby` linked?
6. Check every image. Alt text present? Decorative images empty alt?
7. Check heading hierarchy. One H1? No skipped levels?
8. Check color contrast for every text/bg pair. >= 4.5:1?
9. Check `prefers-reduced-motion` media query exists.
10. Check skip link present and works.

## Citations

- WCAG 2.2: https://www.w3.org/TR/WCAG22/
- WCAG 2.2 Quick Reference: https://www.w3.org/WAI/WCAG22/quickref/
- WAI-ARIA Authoring Practices Guide (APG): https://www.w3.org/WAI/ARIA/apg/
- MDN Accessibility: https://developer.mozilla.org/en-US/docs/Web/Accessibility
- Inclusive Components by Heydon Pickering: https://inclusive-components.design
- A11y Project: https://www.a11yproject.com
- axe DevTools: https://www.deque.com/axe/
