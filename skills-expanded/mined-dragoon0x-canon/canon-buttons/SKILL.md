---
name: canon-buttons
description: Use when designing, auditing, or refactoring buttons, CTAs, icon buttons, split buttons, or any clickable action affordance. Covers hierarchy, sizing, states, disabled-state handling, loading behavior, keyboard behavior, and button vs link distinction. Trigger when the user mentions button, CTA, action, click, submit, or primary/secondary/tertiary.
---

# CANON · Buttons

A button is a verb. If the element navigates, it's a link. This distinction is not cosmetic — screen readers announce them differently, middle-click behaves differently, right-click behaves differently.

## The button vs link rule

| Task | Element |
|---|---|
| Submits form, triggers action, toggles state, opens modal, plays media | `<button>` |
| Navigates to a URL, scrolls to an anchor, opens new tab | `<a href>` |

Styling doesn't change semantics. A `<div onclick>` is never correct.

## Hierarchy — one primary per screen

| Level | Appearance | Rule |
|---|---|---|
| Primary | Filled, brand color | **One per screen**. The single most important action. |
| Secondary | Outlined or tonal fill | Alternative action. Cancel, back, alt-submit. |
| Tertiary / Ghost | Text only, no border | Low-priority. Breadcrumb actions, dismiss. |
| Destructive | Red filled or red outlined | Delete, revoke. Appears only when the action is available. |

If you feel you need two primaries, one of them isn't primary.

## Sizing

| Size | Height | Padding-X | Font size | Use |
|---|---|---|---|---|
| XS | 24px | 8px | 12px | Inline table actions only |
| SM | 32px | 12px | 13px | Toolbars, dense UIs |
| MD | 40px | 16px | 14px | **Default.** |
| LG | 48px | 20px | 16px | Hero CTAs, mobile-primary |
| XL | 56px | 24px | 18px | Marketing only |

**Mobile floor: 44×44px hit target.** Below that, violates Apple HIG and fails WCAG 2.5.5.

## Required states

A button must look visibly different in all six states. Missing any = incomplete.

1. **Default** — resting
2. **Hover** — `cursor: pointer`, subtle elevation or fill change
3. **Active** — press feedback (transform: scale(0.98) or filter darken)
4. **Focus-visible** — 2–3px outline offset 2px, contrast 3:1 minimum
5. **Disabled** — 40–50% opacity, `cursor: not-allowed`, no hover change
6. **Loading** — spinner replaces label OR sits beside it, button stays the same width

## Loading state

```html
<button disabled aria-busy="true">
  <span class="spinner" aria-hidden="true"></span>
  <span>Saving…</span>
</button>
```

Width must not change during loading. Pre-measure the "Saving…" width or use `min-width`.

## Disabled — preserve the "why"

A disabled button with no explanation is a trap. Do one of:
- Don't render it at all. Render it when conditions are met.
- Render it disabled with a tooltip on hover explaining why.
- Render it enabled; on click, show an inline error.

Never leave disabled buttons unexplained.

## Icon buttons

| Context | Rule |
|---|---|
| Icon-only button | Requires `aria-label` describing the action |
| Icon-only button | Requires 44×44px hit area |
| Icon + text | Icon is decorative; `aria-hidden="true"` on SVG |
| Icon position | Leading for start-actions (Save), trailing for flow-actions (Continue →) |

## Keyboard

- `<button>` natively handles Enter and Space.
- `<a>` natively handles Enter (not Space).
- If you used a `<div>` with role="button", you must manually handle both Enter and Space, prevent default, and add `tabindex="0"`. Don't use a div.

## Label copy

Buttons are **verbs**. Sentence case by default.

| Bad | Good |
|---|---|
| OK | Save changes |
| Submit | Create account |
| Yes | Delete permanently |
| Continue | Continue to payment |
| Click here | [link inline in sentence] |

Destructive buttons name the action. "Yes" is never the label for a destructive confirmation.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Two or more primary buttons side by side | Competing hierarchy, paralyzes choice |
| All buttons same color | No visual priority |
| Button shrinks on hover | Hit target violation mid-interaction |
| No focus-visible state | Keyboard users blocked |
| Disabled without explanation | Dead-end UX |
| `<div role="button">` | Reinventing accessibility, usually badly |
| Button label changes width during loading | Layout thrash |
| Destructive action not separated from safe actions | Misclick risk |
| Tooltip on button explaining what the button does | The button label should be clear. If you need a tooltip, your label failed. |

## Decision tree

```
Is it an action or a navigation?
  ├─ Action → <button>
  └─ Navigation → <a href>

Is it the most important action on the screen?
  ├─ Yes → Primary (one per screen)
  └─ No → Secondary or tertiary

Is it destructive?
  ├─ Yes → Destructive style, name the action in the label
  └─ No → Standard hierarchy

Is it icon-only?
  ├─ Yes → Must have aria-label + 44px hit area
  └─ No → Standard label rules
```

## Audit checklist

- [ ] Every button is a `<button>` or `<a>`, not a `<div>`
- [ ] One primary per screen
- [ ] All 6 states visible and distinct
- [ ] Mobile hit target ≥ 44×44px
- [ ] Focus-visible ring ≥ 2px with 3:1 contrast
- [ ] Disabled state has explanation if non-obvious
- [ ] Loading state preserves width
- [ ] Icon-only buttons have `aria-label`
- [ ] Labels are verbs, sentence case
- [ ] Destructive actions name the verb ("Delete" not "Yes")

## Sources

- WCAG 2.2 · 2.4.7 Focus Visible, 2.5.5 Target Size, 1.3.1 Info and Relationships
- Material Design 3 · Button component
- Apple HIG · Buttons
- Refactoring UI · "Don't use gray text on colored backgrounds"
- Nielsen Norman · "Primary vs. Secondary Buttons"
