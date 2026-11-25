---
name: canon-tooltips
description: Use when designing, auditing, or refactoring tooltips, hover hints, help text, or any supplementary info surfaced on hover/focus. Covers when a tooltip is appropriate vs a label vs a popover, delay timing, positioning, keyboard access, mobile behavior, and the rules that keep tooltips from becoming accessibility traps. Trigger when the user mentions tooltip, hover hint, help text, title attribute, or popover hint.
---

# CANON · Tooltips

A tooltip is a band-aid. If you need one, the interface usually failed first. Use them, but earn them.

## When a tooltip is appropriate

| Appropriate | Not appropriate |
|---|---|
| Naming an icon-only button | Explaining what a button labeled "Save" does |
| Showing full text of a truncated cell | Critical info users must see to proceed |
| Showing the exact value of a chart data point | Error messages |
| Shortcut hints ("⌘K") | Instructions needed by everyone |
| Disambiguating a date ("Posted 3d ago" → exact timestamp) | Form field labels |
| Advanced-use details secondary to the label | Primary call-to-action copy |

**Critical info is never tooltip-only.** If users need the info to succeed, put it in the interface.

## Tooltip vs label vs popover

| Pattern | Trigger | Dismiss | Content |
|---|---|---|---|
| Tooltip | Hover, focus | Auto on mouseleave/blur | Short text, 1–2 lines max |
| Label | Always visible | N/A | Primary name of the control |
| Popover | Click, tap | Explicit dismiss | Longer content, interactive (buttons, links) |
| Disclosure | Click, tap | Toggle | Expand/collapse structured content |

Tooltips have **no interactive content**. No buttons. No links. If users need to click inside it, it's a popover.

## Timing

| Event | Delay |
|---|---|
| Show on hover | **500–700ms delay** before showing |
| Show on focus | **0ms delay** — immediate |
| Hide on mouseleave | **0ms** (or 50ms to allow cursor slip) |
| Hide on blur | **0ms** |
| Show delay for adjacent tooltip | 0ms (if another tooltip was recently shown) |

The hover delay is critical — tooltips appearing instantly trigger every time the cursor passes by, creating visual noise. Material spec says 500ms; most modern systems use 500–700ms.

## Positioning

Default: above the trigger, centered horizontally.

Fallback order when above doesn't fit:
1. Below
2. Right
3. Left

Every tooltip needs an offset: **4–8px** between tooltip edge and trigger.

Never let a tooltip cover its own trigger — users lose the context.

Arrow/caret on the tooltip is optional but helps connect to the trigger. 6–8px arrow size.

## Keyboard access — required

- Tooltip appears on `focus` of its trigger. Not only on hover.
- Escape dismisses the tooltip without moving focus.
- Tab to the next element dismisses the tooltip.

This is where most tooltip implementations fail — hover-only tooltips are inaccessible.

## Mobile — reconsider

Hover doesn't exist on touch. Mobile tooltip strategies:

- **Tap-to-show, tap-outside-to-hide** — works, but users don't expect it.
- **Convert tooltip to popover with close button.**
- **Surface the info inline on small screens** — usually the best answer.

If an icon needs a tooltip on desktop, on mobile it probably needs a label.

## Semantic markup

```html
<button aria-describedby="save-hint" type="submit">
  <svg aria-hidden="true">...</svg>
  Save
</button>

<div role="tooltip" id="save-hint">Ctrl+S</div>
```

- `role="tooltip"` on the tooltip element.
- `aria-describedby` on the trigger, pointing to the tooltip id.
- Don't use the native `title` attribute — inconsistent across browsers, not touch-accessible, awkward timing.

## Content

- **1 line ideal, 2 lines max.** If it's longer, it belongs in a popover or help panel.
- Sentence case. Period optional (single sentence without period is fine).
- No instructions requiring multiple steps.
- No links inside. If you need a link, it's a popover.

## Styling

- Background: high-contrast against surroundings. Dark-on-light tooltips (near-black bg, white text) are the traditional default and work in both light and dark themes.
- Font size: 12–13px (smaller than body by one step).
- Padding: 6–10px horizontal, 4–6px vertical.
- Border radius: 4–6px.
- Max width: 240–320px. Text wraps.
- Shadow: subtle, elevation 2 from `canon-depth`.
- Animation: 120–180ms fade + subtle scale (0.96 → 1) on enter. Skip scale under `prefers-reduced-motion`.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Tooltip on hover only (no focus) | Keyboard users blocked |
| Using native `title` attribute for critical info | No timing control, no keyboard behavior, no mobile |
| Tooltip with buttons or links inside | Users can't move cursor to it before it closes |
| Critical info tooltip-only | Inaccessible to touch + screen reader |
| 3+ line tooltips | Should be a popover |
| Instant-show hover tooltips | Visual noise, chases cursor |
| Tooltip covering the trigger | Context lost |
| Tooltip without arrow and far from trigger | Ambiguous attribution |
| Tooltip on a plain text label ("Save") | Redundant |
| Disappearing before users can read (< 1 second) | Race condition |

## Edge cases

- **Tooltips on disabled buttons**: disabled buttons don't fire pointer events in most browsers. Solutions: (1) wrap disabled button in a span that receives hover, (2) use `aria-disabled="true"` and prevent click in JS, not the native `disabled` attribute.
- **Truncated text tooltips**: only show tooltip when content is actually truncated (check `scrollWidth > clientWidth`), not on every hover.
- **Tooltip inside a scrollable container**: reposition on scroll, or hide on scroll.
- **Tooltip from a modal trigger**: z-index must exceed modal; render in a portal to `<body>`.

## Decision tree

```
Is the info critical to using the product?
  ├─ Yes → Put it in the interface, not in a tooltip
  └─ No → Tooltip may be appropriate

Does the content include buttons, links, or structured content?
  ├─ Yes → Popover, not tooltip
  └─ No → Tooltip OK

Is there a focusable element to attach to?
  ├─ No → Add one or use a different pattern
  └─ Yes → Attach with aria-describedby

Mobile?
  └─ Plan the mobile alternative: inline label, popover, or omit.
```

## Audit checklist

- [ ] Tooltip appears on both hover and focus
- [ ] Uses `role="tooltip"` + `aria-describedby`, not native `title`
- [ ] 500–700ms delay on hover
- [ ] 0ms on focus
- [ ] Escape dismisses
- [ ] Doesn't cover its trigger
- [ ] Content is 1–2 lines max
- [ ] No interactive content inside
- [ ] Not used for critical info
- [ ] Mobile alternative planned
- [ ] Honors `prefers-reduced-motion`
- [ ] Contrast ≥ 4.5:1 text-to-background
- [ ] Works inside modals (z-index / portal)

## Sources

- WCAG 2.2 · 1.4.13 Content on Hover or Focus, 2.1.1 Keyboard
- WAI-ARIA Authoring Practices · Tooltip pattern
- Material Design 3 · Tooltip (500ms show delay)
- Apple HIG · Help (tooltip equivalent, hover delay guidance)
- Floating UI · positioning reference implementation
