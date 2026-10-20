---
name: aria-only-when-needed
description: ARIA is a fallback for when native HTML falls short — never add redundant or conflicting roles
---

# ARIA Only When Needed

The first rule of ARIA is: do not use ARIA if a native HTML element already covers the requirement. ARIA modifies the accessibility tree — misuse creates incorrect announcements, conflicting roles, and broken keyboard behavior that native elements never have.

## Rules

- **No redundant ARIA.** Do not add `role`, `aria-*`, or `tabIndex` to an element that already has the correct semantics from its tag alone.
- **No conflicting roles.** The ARIA role must not contradict the element's native role. A `<button role="link">` is broken: the keyboard contract for links and buttons differs.
- **`aria-label` / `aria-labelledby` must be non-empty strings.** An empty `aria-label=""` removes the accessible name entirely.
- **Do not use `aria-hidden="true"` on focusable elements.** Hidden + focusable = keyboard trap: focus lands on an element the screen reader cannot describe.
- **`aria-live` regions must exist in the DOM before content is injected.** Inserting a live region and content at the same time causes announcements to be missed.
- **`aria-expanded`, `aria-selected`, `aria-checked` must reflect actual state**, updated synchronously when the UI changes.

## When ARIA IS appropriate

- Custom widgets with no native equivalent: combobox, tree, grid, slider, tab panel.
- Adding a descriptive name to an icon-only button: `<button aria-label="Close dialog">`.
- Connecting a visible label to a form control when `<label for>` cannot be used.
- Live regions for dynamic content (toasts, status messages, validation results).

## Examples

```html
<!-- BAD — redundant role and aria-disabled that duplicates the HTML disabled attribute -->
<button role="button" aria-disabled="true" disabled>Save</button>

<!-- GOOD -->
<button disabled>Save</button>
```

```tsx
// BAD — aria-hidden on a focusable interactive element
<button aria-hidden="true" onClick={close}>×</button>

// GOOD — visually hidden label, element is not aria-hidden
<button onClick={close}>
  <span aria-hidden="true">×</span>
  <span className="sr-only">Close dialog</span>
</button>
```

```tsx
// BAD — live region injected at the same time as the message
function showStatus(msg: string) {
  const el = document.createElement('div')
  el.setAttribute('role', 'status')
  el.textContent = msg
  document.body.appendChild(el) // screen reader misses this
}

// GOOD — region pre-exists; only content changes
// <div role="status" aria-live="polite" id="status-region"></div>
document.getElementById('status-region').textContent = msg
```

## Gotchas

- `role="presentation"` and `role="none"` strip all native semantics; applying them to interactive elements (`<a>`, `<button>`, `<input>`) violates the spec.
- `aria-labelledby` points to an element's `id`. If the referenced element is hidden with `display: none`, the label is lost.
- Adding ARIA to a component library component may conflict with ARIA the library already sets internally. Inspect the rendered DOM, not the JSX.
