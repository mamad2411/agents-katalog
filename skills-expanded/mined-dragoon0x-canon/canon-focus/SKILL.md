---
name: canon-focus
description: Use when designing or auditing focus indicators — visible focus rings, focus-visible vs focus, custom focus styles, contrast requirements, and focus management during route changes. Trigger when the user mentions focus ring, focus indicator, focus-visible, outline, focus style, or focus management.
---

# CANON · Focus

If a user can't see where focus is, the keyboard is useless. Focus indicators are not optional decoration; they're navigation infrastructure.

## The focus-visible rule

`:focus-visible` shows focus only on keyboard navigation, not on mouse clicks. This is the right default for most elements.

```css
:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}

:focus:not(:focus-visible) {
  outline: none;
}
```

## Visual spec

| Property | Value | Reason |
|---|---|---|
| Outline width | 2–3px | Visible at distance, scales with zoom |
| Outline offset | 2px | Separates from element edge, prevents clipping |
| Outline color | Brand color or high-contrast default | Must be visible against all backgrounds |
| Contrast ratio | ≥ 3:1 against adjacent colors | WCAG 2.4.11 Focus Appearance (AA) |
| Shape | Follows element border-radius | Looks intentional, not broken |

```css
:focus-visible {
  outline: 2px solid oklch(50% 0.2 250);
  outline-offset: 2px;
  border-radius: inherit;
}
```

## Focus must be visible in BOTH themes

A blue focus ring on a white background is fine. The same blue on a dark blue background is invisible. Define focus color per theme.

## Never `outline: none` without replacement

```css
/* NEVER */
*:focus { outline: none; }

/* ACCEPTABLE — only if custom indicator replaces it */
button:focus-visible {
  outline: none;
  box-shadow: 0 0 0 2px var(--color-bg), 0 0 0 4px var(--color-focus);
}
```

The box-shadow double-ring technique creates a "halo" that works on any background.

## Focus management during navigation

Single-page apps don't trigger browser's native focus reset on navigation. You must manage focus manually.

- On route change: move focus to the new page's `<h1>` or `<main>`.
- On modal open: move focus into the modal (see `canon-modals`).
- On modal close: return focus to the trigger.
- On accordion expand: keep focus on the trigger.
- On item delete from a list: move focus to the next item (or previous if last).

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| `* { outline: none }` in reset CSS | Removes all focus visibility |
| Focus ring only via `:focus` (not `:focus-visible`) | Shows on every mouse click, annoys mouse users |
| Focus color that matches the background | Invisible in one theme |
| Thin 1px outline at low contrast | Invisible at 100% zoom, worse at 200% |
| No focus management on SPA route change | Users land in limbo after navigation |
| Focus indicator hidden by overflow: hidden | Clipped, invisible |

## Audit checklist

- [ ] Every interactive element has a visible `:focus-visible` indicator
- [ ] Focus ring is ≥ 2px and ≥ 3:1 contrast against adjacent colors
- [ ] Focus visible in both light and dark themes
- [ ] No global `outline: none` without replacement
- [ ] Focus ring not clipped by `overflow: hidden`
- [ ] SPA route changes manage focus (move to `<h1>` or `<main>`)
- [ ] Modal focus managed per `canon-modals`
- [ ] Outline offset prevents overlap with element borders

## Sources

- WCAG 2.2 · 2.4.7 Focus Visible, 2.4.11 Focus Appearance, 2.4.12 Focus Not Obscured
- Sara Soueidan · "A guide to designing accessible focus indicators"
- MDN · :focus-visible pseudo-class
