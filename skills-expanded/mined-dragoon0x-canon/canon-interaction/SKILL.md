---
name: canon-interaction
description: Use when designing or auditing interactive states (hover, focus, active, disabled, loading), focus management, keyboard navigation, click targets, drag-and-drop, or any user input handling. Trigger when the user mentions states, focus, hover, keyboard, interaction, click, tap, or fixing how something responds.
---

# CANON · Interaction Design

Every interactive element has 6 visual states. Most AI-generated UIs ship 1 or 2. The states below are the contract between the user and the interface.

## The Six States

Every button, link, input, and control must have:

| State | Trigger | Visual change |
|---|---|---|
| **Default** | Idle | Base appearance |
| **Hover** | Pointer over (desktop only) | Slight elevation, color shift, or underline |
| **Focus** | Keyboard tab or click | Ring (2–3px) outside the element |
| **Active** | Pressed but not released | Slight scale-down or color darken |
| **Disabled** | Cannot interact | 50% opacity OR muted color, no pointer events |
| **Loading** | In-flight | Spinner, skeleton, or progress |

For inputs, add a 7th: **Error**. For toggles, add **Selected**.

## Focus Rings (WCAG 2.4.7, 2.4.13)

```css
:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}

/* Never remove focus without replacement */
:focus { outline: none; }              /* alone: WCAG violation */
:focus-visible { outline: 2px solid; } /* together: OK */
```

| Property | Value | Source |
|---|---|---|
| Ring width | 2–3px | Visible at all zoom levels |
| Ring offset | 2px | Separates ring from element |
| Ring color | Brand accent or `--color-focus` | Must hit 3:1 against adjacent surface |
| Ring style | `solid` | `dotted`/`dashed` are harder to see |

**Use `:focus-visible`, not `:focus`.** This shows the ring for keyboard users but suppresses it for mouse clicks, which feels right.

## Hover

| Element | Hover treatment |
|---|---|
| Button | Background color one step darker (-4 to -8% L) |
| Link (text) | Underline appears OR color one step darker |
| Card (clickable) | Subtle elevation (shadow + 1–2px translateY) |
| Icon button | Background appears (transparent → 8% surface) |
| Input | Border color one step darker |
| Row in table/list | Background appears (transparent → 4% surface) |

**Never** make hover the only signal of interactivity. Touch users have no hover. Cursor and color shift together.

## Active (Pressed)

```css
button:active {
  transform: scale(0.98);
  transition: transform 100ms var(--ease-out);
}
```

A 2% scale-down for 100ms feels like a real button press. Pair with a slight color darken.

For larger surfaces (cards, tiles), use a faster opacity dip instead of scale.

## Disabled

```css
button:disabled,
button[aria-disabled="true"] {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}
```

| Approach | When |
|---|---|
| `disabled` attribute | Form controls (button, input) |
| `aria-disabled="true"` | Custom controls; allows focus for screen readers |
| `opacity: 0.5` | Visual signal |
| `cursor: not-allowed` | Affordance |

**Anti-pattern: hiding disabled instead of disabling.** Users need to see the action exists but isn't available, plus a hint why.

## Loading

| Wait time | Pattern |
|---|---|
| < 400ms | Show nothing (perceived as instant) |
| 400ms–1s | Spinner appears at 400ms |
| 1s–10s | Determinate progress bar |
| > 10s | Progress bar + status message + estimated time |

**Inline loading** (within the button that triggered it) keeps focus context. Replace label with spinner; keep button width fixed to prevent layout shift.

```html
<button disabled>
  <span class="spinner" aria-hidden="true"></span>
  <span class="sr-only">Saving...</span>
</button>
```

## Keyboard Navigation

### Required Bindings

| Key | Action | Source |
|---|---|---|
| `Tab` | Next focusable element | Browser default |
| `Shift+Tab` | Previous focusable element | Browser default |
| `Enter` | Activate button, submit form | WAI-ARIA |
| `Space` | Activate button, toggle checkbox | WAI-ARIA |
| `Esc` | Close modal, dismiss popover | WAI-ARIA Modal pattern |
| `Arrow keys` | Navigate within composite widgets (menu, tabs, listbox, slider) | WAI-ARIA |
| `Home`/`End` | First/last in a list | WAI-ARIA |

### Tab Order

Tab order follows DOM order. If tab order needs to differ from visual order, the design is wrong (re-order DOM, don't use `tabindex` to fix).

| `tabindex` value | Use |
|---|---|
| `0` | Insert into natural tab order |
| `-1` | Make focusable programmatically (e.g., for a focus trap) |
| Positive numbers | Never. Anti-pattern. |

### Focus Trap

Modals trap focus inside the modal. Tabbing past the last element loops to the first. Esc closes the modal and restores focus to the trigger.

## Click Targets

| Context | Minimum |
|---|---|
| Mobile (touch) | 44 × 44 px (WCAG 2.5.5 AAA) |
| Mobile (touch, AA floor) | 24 × 24 px (WCAG 2.5.8) |
| Desktop (mouse) | 24 × 24 px |
| Spacing between adjacent targets | 8px minimum |

**Rule: visual size can be smaller, but the tappable area must meet the floor.** Use padding or absolute-positioned `::before` to extend.

```css
.icon-button {
  width: 24px;
  height: 24px;
  position: relative;
}
.icon-button::before {
  content: "";
  position: absolute;
  inset: -10px;  /* extends tap area to 44x44 */
}
```

## Cursor

| Element | Cursor |
|---|---|
| Button, link | `pointer` |
| Input (text) | `text` (default) |
| Disabled | `not-allowed` |
| Drag handle | `grab` / `grabbing` |
| Resize handle | `ns-resize`, `ew-resize`, etc |
| Loading | `wait` or `progress` |
| Help available | `help` |

**Don't add `cursor: pointer` to non-interactive elements.** It signals interactivity that isn't there.

## Drag and Drop

If you implement drag-and-drop, you must also implement keyboard alternatives. Pure DnD is an accessibility failure.

```html
<!-- Each draggable item has keyboard controls -->
<li role="listitem" tabindex="0" aria-grabbed="false">
  <button aria-label="Move up">↑</button>
  <button aria-label="Move down">↓</button>
</li>
```

## Long-Press, Right-Click, Hover-Reveal

These are **enhancements**, never the only path. Every action available via long-press, right-click, or hover must also be available via a visible button or menu.

## Anti-Patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| `outline: none` without replacement | Keyboard users can't see focus | Use `:focus-visible` with custom ring |
| Hover as only interactivity signal | Touch users get nothing | Add color/cursor change |
| Disabled state with no explanation | User stuck | Add tooltip or message |
| Hidden disabled buttons | User can't see what's possible | Show as disabled |
| 16×16 close button on mobile | Below touch target | Pad to 44×44 |
| `cursor: pointer` on non-interactive divs | Lies about interactivity | Remove |
| Loading spinner appears at 0ms | Perceived as slow | Delay 400ms |
| No keyboard equivalent for drag-drop | Accessibility failure | Add buttons or arrow-key nav |
| Modal that doesn't trap focus | Tab escapes the modal | Implement focus trap |
| Modal that doesn't return focus | User loses position | Restore focus to trigger on close |
| `tabindex="5"` | Breaks natural order | Use `tabindex="0"` and re-order DOM |
| Right-click as only path | Mobile users locked out | Add visible menu button |
| Tooltips on hover only | Mobile and keyboard users miss them | Show on focus too |

## Decision Tree

```
Adding interactive element?
├─ Define all 6 states (default, hover, focus, active, disabled, loading)
├─ Tappable area >= 44px? If visual is smaller, extend with padding.
├─ Keyboard accessible? Tab reaches it, Enter/Space activates it.
├─ Focus ring uses :focus-visible, 2-3px solid, 2px offset, 3:1 contrast?
├─ Hover changes both color AND cursor?
├─ Disabled visible (not hidden) with explanation?
└─ Loading delayed 400ms? Acknowledged on completion?
```

## Audit Checklist

1. Click every button without a mouse. Tab through the page. Every focusable element shows a visible ring.
2. Search for `outline: none`. Each occurrence paired with `:focus-visible`?
3. Hover every interactive element. Color, cursor, or position changes?
4. Press every button. Active state visible?
5. Find every disabled state. Visible? Explained? Not hidden?
6. Find every loading state. Delayed 400ms? Acknowledged?
7. Open every modal. Focus trapped? Esc closes? Focus restored on close?
8. Check tap targets on mobile. All >= 44×44?
9. Find every drag-drop. Keyboard alternative present?
10. Find every hover-only tooltip. Also shows on focus?

## Citations

- WCAG 2.2 Focus Visible: https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html
- WCAG 2.2 Focus Not Obscured: https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html
- WCAG 2.2 Target Size: https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
- WAI-ARIA Authoring Practices: https://www.w3.org/WAI/ARIA/apg/
- Apple HIG Inputs: https://developer.apple.com/design/human-interface-guidelines/inputs
- Material Design States: https://m3.material.io/foundations/interaction/states/overview
