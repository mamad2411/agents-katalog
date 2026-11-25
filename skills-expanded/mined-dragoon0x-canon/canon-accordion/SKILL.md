---
name: canon-accordion
description: Use when designing, auditing, or refactoring accordion components, collapsible sections, disclosure widgets, FAQ sections, or expand/collapse patterns. Covers when accordions help versus hurt comprehension, single vs multi-expand behavior, icon conventions, keyboard behavior, semantic markup (`<details>` vs ARIA), animation, and accessibility. Trigger when the user mentions accordion, collapsible, expandable, disclosure, FAQ, or expand/collapse.
---

# CANON · Accordions

An accordion is a disclosure widget — a heading that toggles content visibility. Useful in moderation. Often overused to hide things that should just be visible.

## When to use an accordion

| Appropriate | Not appropriate |
|---|---|
| FAQ sections | Primary content users need to see |
| Optional settings users don't always expand | Forms (users miss fields they didn't open) |
| Long reference content organized into topics | Short content that fits on the page |
| Dense lists where each row has rich drill-down detail | Hiding critical errors or confirmations |

**Don't use accordions to hide information users actually need.** If the content matters, show it.

## Use `<details>` / `<summary>` when possible

Native HTML gives you keyboard, screen reader, toggle state, and animation primitives for free.

```html
<details>
  <summary>What's your return policy?</summary>
  <p>Returns accepted within 30 days of purchase. Items must be unused.</p>
</details>
```

- Enter / Space on `<summary>` toggles.
- Keyboard focus works natively.
- Screen readers announce expanded/collapsed.
- Default disclosure triangle can be styled or replaced.
- Use CSS `details[open]` to animate.

Reach for custom ARIA only when native doesn't fit — e.g., controlling multiple sections with complex behavior.

## Custom ARIA pattern

When `<details>` won't do:

```html
<h3>
  <button
    aria-expanded="false"
    aria-controls="panel-1"
    id="trigger-1"
  >
    What's your return policy?
    <svg aria-hidden="true">▼</svg>
  </button>
</h3>

<div
  id="panel-1"
  role="region"
  aria-labelledby="trigger-1"
  hidden
>
  <p>Returns accepted within 30 days.</p>
</div>
```

- Button wraps the heading text (not the heading itself).
- Heading element (`<h3>` etc.) wraps the button to preserve document outline.
- `aria-expanded` toggles true/false.
- `aria-controls` points to panel id.
- Panel has `role="region"` and `aria-labelledby`.
- Hide with `hidden` attribute (or `display: none`), not `visibility: hidden`.

## Single-expand vs multi-expand

| Pattern | Use |
|---|---|
| **Multi-expand** (default) | Users can have multiple sections open at once |
| Single-expand (accordion behavior strict) | Only one section open; opening another closes the previous |

Multi-expand is more forgiving. Use single-expand only when:
- Content is very long per section (auto-closing keeps the page manageable).
- Sections are mutually exclusive in context (one set of settings vs another).

Default to multi-expand unless you have a reason.

## Icon convention

| Icon | Meaning |
|---|---|
| Chevron right (▶) / down (▼) | Default. Rotates on expand. |
| Plus (+) / minus (−) | Acceptable. Changes on expand. |
| Caret up / down | Acceptable. |
| Custom icons | Risky — users need to learn them |

**Chevron is the convention.** Rotates 90° on expand. Transition: 150–200ms ease-out.

Icon position: right-aligned by default (label reads left, icon closes the row visually).

## Layout and sizing

```
┌─────────────────────────────────────────┐
│ Section heading                      ▼  │   ← trigger row
├─────────────────────────────────────────┤
│                                         │
│ Panel content when expanded.            │
│                                         │
└─────────────────────────────────────────┘
```

| Element | Spec |
|---|---|
| Trigger row height | 48–56px |
| Trigger padding | 16px horizontal, 12–16px vertical |
| Panel padding | Matches trigger horizontal; 16–24px vertical |
| Divider between items | 1px border, or just whitespace |
| Mobile tap target | ≥ 44px (trigger row usually clears this naturally) |

Whole trigger row is clickable, not just the icon or just the text.

## Hover, focus, active

- **Hover**: background tint or icon color shift.
- **Focus-visible**: outline on the trigger (the `<button>` or `<summary>`), not on the container.
- **Active (being pressed)**: subtle press feedback.
- **Expanded state**: visually distinct — often a slight background tint persists while open, or the bottom border of the trigger becomes invisible.

## Animation

Animating height from collapsed to expanded needs care.

### Simple CSS

```css
details[open] > summary + * {
  animation: reveal 200ms ease-out;
}

@keyframes reveal {
  from { opacity: 0; transform: translateY(-4px); }
  to { opacity: 1; transform: translateY(0); }
}
```

### Height animation (more involved)

Native `height: auto` can't be animated. Options:
- Use `grid-template-rows: 0fr → 1fr` (modern browsers).
- Use `max-height: 0 → max-height: calc(some-large-value)`.
- Measure actual height via JS and animate.

```css
.accordion-panel {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows 200ms ease-out;
}
.accordion-panel[aria-expanded="true"],
details[open] .accordion-panel {
  grid-template-rows: 1fr;
}
.accordion-panel > * {
  overflow: hidden;
}
```

Duration: 200–300ms. Easing: ease-out on expand, ease-in on collapse.

Honor `prefers-reduced-motion`:
```css
@media (prefers-reduced-motion: reduce) {
  .accordion-panel { transition: none; }
}
```

## FAQ patterns

FAQ is the canonical accordion use case.

Rules:
- **Most important questions first.**
- Multi-expand — users scan, open several, read.
- Include a "Expand all / Collapse all" button when there are 10+ items.
- Question is the trigger text. Full sentence, question form. Sentence case.
- Answer content can include links, lists, code — any rich content.
- Add schema.org FAQPage structured data for SEO if public.

## Scroll behavior

When a user expands an item near the bottom of the viewport, the panel content may open off-screen. Options:

- Scroll-into-view on expand (optional; can feel aggressive).
- Keep the trigger in view; let panel content push below.
- Sticky trigger when the panel is very long.

For most cases, do nothing. Let the user scroll naturally.

## Deep linking to sections

Useful for FAQ and documentation:

```
/faq#returns
```

- On load, if hash matches an accordion item id, expand it.
- Scroll it into view.
- Each item has a stable id slug.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Hiding form fields inside accordion | Users miss fields |
| Hiding critical status / errors | Content is invisible when collapsed |
| Non-standard icons without label context | Users don't learn the convention |
| No `aria-expanded` on custom triggers | Screen reader silent on state |
| Click target is only the icon | Trigger should be the whole row |
| No focus-visible | Keyboard users lost |
| Single-expand when multi-expand is natural | Frustrating; users want to compare open items |
| Heavy animations that take > 400ms | Feels slow, blocks reading |
| Nested accordions inside accordions | Information architecture failure |
| Accordion used to hide length when the fix is less content | Surface-level fix |
| `<div>` wrapping the trigger instead of `<button>` | Not keyboard-operable |

## Decision tree

```
Is the content critical/primary?
  ├─ Yes → Don't hide it; show it
  └─ No → Accordion may fit

Can you use <details>/<summary>?
  ├─ Yes → Use it (default path)
  └─ No → Custom ARIA pattern

Single-expand or multi-expand?
  ├─ Content is mutually exclusive → Single
  └─ Default → Multi-expand

Is this a form?
  ├─ Yes → Don't accordion the fields
  └─ No → Continue

Is this a FAQ or doc section?
  └─ Add deep linking by slug
```

## Audit checklist

- [ ] Uses `<details>`/`<summary>` or correct ARIA pattern
- [ ] `aria-expanded` on custom triggers
- [ ] `aria-controls` points to panel id
- [ ] Panel has `role="region"` and `aria-labelledby`
- [ ] Whole trigger row is clickable, not just the icon
- [ ] Focus-visible on the trigger
- [ ] Chevron/plus icon animates on expand
- [ ] Animation duration 200–300ms
- [ ] `prefers-reduced-motion` honored
- [ ] Mobile tap target ≥ 44px
- [ ] Multi-expand by default (unless justified otherwise)
- [ ] No form fields hidden inside
- [ ] No critical content hidden by default
- [ ] Deep-link support (hash → expand) for docs/FAQ

## Sources

- WAI-ARIA Authoring Practices · Accordion, Disclosure
- WCAG 2.2 · 2.1.1 Keyboard, 4.1.2 Name Role Value, 1.4.13 Content on Hover or Focus
- HTML Living Standard · `<details>`, `<summary>`
- Nielsen Norman · "Accordions and expandable content"
- Material Design 3 · List (expandable)
