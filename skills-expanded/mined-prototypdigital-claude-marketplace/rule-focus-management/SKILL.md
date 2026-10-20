---
name: focus-management
description: Provide visible focus indicators; move focus intentionally on route change and dialog open/close
---

# Focus Management

Focus management is what separates keyboard navigation that works from keyboard navigation that feels broken. WCAG 2.4.3 (Focus Order) and 2.4.7 (Focus Visible) are Level AA; WCAG 2.4.11 (Focus Appearance) is Level AA in WCAG 2.2.

## Rules

- **Never use `outline: none` or `outline: 0` without a replacement focus style.** CSS resets commonly remove the default outline on all elements. Always provide a custom `:focus-visible` style that meets WCAG 2.4.11 (minimum 2px offset, 3:1 contrast against adjacent colors).
- **Prefer `:focus-visible` over `:focus`.** `:focus` fires on mouse click too, which causes focus rings to appear during normal pointer interaction. `:focus-visible` only shows when the browser determines keyboard navigation is likely.
- **Move focus to new content when it appears:**
  - **Dialog opens** → move focus to the dialog's first focusable element or the dialog container itself (`ref.current.focus()`).
  - **Dialog closes** → return focus to the element that triggered the dialog.
  - **Route changes (SPA)** → move focus to the `<h1>` or a designated skip-target so screen readers announce the new page.
- **Do not programmatically call `.focus()` on non-focusable elements** without first adding `tabIndex={-1}` (which makes the element focusable by script but not by Tab).
- **Focus must not become lost.** After removing a focused element (e.g. deleting a list item, closing a panel), explicitly move focus to a sensible next target.

## Examples

```css
/* BAD — removes focus visibility for all users including keyboard users */
* {
  outline: none;
}

/* GOOD — removes outline only for pointer/touch, replaces it for keyboard */
:focus:not(:focus-visible) {
  outline: none;
}
:focus-visible {
  outline: 2px solid #005fcc;
  outline-offset: 2px;
  border-radius: 2px;
}
```

```tsx
// BAD — dialog opens but focus stays behind the overlay
function Modal({ isOpen, children }) {
  return isOpen ? <div role="dialog">{children}</div> : null
}

// GOOD — focus moves into dialog on open; returns on close
function Modal({ isOpen, onClose, triggerRef, children }) {
  const dialogRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    if (isOpen) {
      dialogRef.current?.focus()
    } else {
      triggerRef.current?.focus()
    }
  }, [isOpen])

  return isOpen ? (
    <div
      ref={dialogRef}
      role="dialog"
      tabIndex={-1}
      onKeyDown={e => e.key === 'Escape' && onClose()}
    >
      {children}
    </div>
  ) : null
}
```

```tsx
// BAD — SPA route change; screen reader user has no signal the page changed
function App() {
  return <Routes>...</Routes>
}

// GOOD — announce the new page by moving focus to the heading
function PageLayout({ children }) {
  const location = useLocation()
  const headingRef = useRef<HTMLHeadingElement>(null)

  useEffect(() => {
    headingRef.current?.focus()
  }, [location.pathname])

  return (
    <>
      <h1 ref={headingRef} tabIndex={-1}>{pageTitle}</h1>
      {children}
    </>
  )
}
```

## Gotchas

- `tabIndex={-1}` makes an element programmatically focusable but does not add it to the natural Tab sequence. Use it for elements that receive focus only via script (dialog containers, route headings).
- Focus trapping inside dialogs should use a library (`focus-trap-react`, Radix, Headless UI) rather than manual `Tab` interception — edge cases (Shadow DOM, portals, dynamic children) are numerous.
- `autoFocus` on input fields inside dialogs works for the first render but is unreliable for conditionally rendered dialogs; prefer the `useEffect` pattern above.
- The "no `outline: none` without a replacement" invariant is best caught early in CI — flag bare `outline: none`/`outline: 0` with a stylelint rule (e.g. a `declaration-property-value-disallowed-list` entry) so the replacement style is a conscious choice, not an omission.
