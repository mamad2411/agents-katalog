---
name: keyboard-navigation
description: All interactive elements must be reachable and operable by keyboard alone; no keyboard traps
---

# Keyboard Navigation

Every action a mouse user can take must also be reachable and operable by keyboard. WCAG 2.1 SC 2.1.1 (Level A) and SC 2.1.2 (No Keyboard Trap) make this a baseline requirement, not a nice-to-have.

## Rules

- **All interactive elements must be focusable.** Native interactive elements (`<button>`, `<a href>`, `<input>`, `<select>`, `<textarea>`) are focusable by default. Custom elements must receive `tabIndex="0"`.
- **Never use `tabIndex` greater than 0.** `tabIndex={1}` creates a custom tab order that diverges from DOM order and confuses sighted keyboard users.
- **No keyboard traps.** If a user can tab into a component, they must be able to tab or Escape out of it without reloading the page. Dialogs trap intentionally — but must release focus on close.
- **Provide visible focus for all interactive elements** (covered in depth by the `focus-management` rule).
- **Support expected keyboard interactions for standard patterns:**

  | Pattern | Keys to support |
  |---|---|
  | Button | `Enter`, `Space` |
  | Link | `Enter` |
  | Checkbox / Radio | `Space` to toggle |
  | Listbox / Select | Arrow keys within options |
  | Dialog / Modal | `Escape` to close; Tab cycles within dialog |
  | Accordion | `Enter` / `Space` to expand; arrow keys optional |

- **Do not rely on hover-only interactions.** Tooltips, dropdowns, and contextual menus triggered only by hover are inaccessible to keyboard and touch users. Provide equivalent keyboard triggers.
- **Logical tab order follows visual reading order.** Avoid absolute positioning or CSS `order` that moves items visually without reordering the DOM, because tab focus follows DOM order.

## Examples

```tsx
// BAD — div is not in the tab sequence; Enter/Space do nothing
<div className="menu-item" onClick={handleSelect}>
  {label}
</div>

// GOOD — button is focusable and handles keyboard events natively
<button type="button" className="menu-item" onClick={handleSelect}>
  {label}
</button>
```

```tsx
// BAD — keyboard trap: focus enters the panel but Tab has no exit path
function Panel({ children }) {
  return (
    <div onKeyDown={e => e.stopPropagation()}>
      {children}
    </div>
  )
}

// GOOD — only prevent propagation for keys the component handles intentionally
function Panel({ children, onClose }) {
  return (
    <div
      role="dialog"
      onKeyDown={e => {
        if (e.key === 'Escape') onClose()
      }}
    >
      {children}
    </div>
  )
}
```

## Gotchas

- `pointer-events: none` hides an element from mouse but does not remove it from the tab sequence. Use `tabIndex={-1}` or `disabled` to also exclude it from keyboard navigation.
- CSS `visibility: hidden` removes from tab sequence; `opacity: 0` does not. Content hidden behind a closed drawer may still receive keyboard focus if it is only visually hidden via opacity or transform.
- The "no positive `tabIndex`" invariant is non-negotiable; enforce it in CI with the `jsx-a11y/tabindex-no-positive` lint rule rather than relying on review alone.
- Skip navigation links (`<a href="#main-content">Skip to main content</a>`) must be the first focusable element on every page. They may be visually hidden until focused.
