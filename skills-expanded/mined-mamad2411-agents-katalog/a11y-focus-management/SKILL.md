---
name: a11y-focus-management
description: Use when building a modal, dialog, or any UI that changes what's focused programmatically — moving focus in on open and restoring it on close. Use whenever a component conditionally renders/removes focusable content based on state (isOpen, route change).
metadata:
  origin: community (decomposed from frontend-a11y)
allowed-tools: Read, Edit, Grep, Glob
---

# Focus management

Focus must move logically whenever the visible/interactive surface changes — most commonly
modals, but also route transitions and any "reveal new interactive content" state change.

## Modal: move focus in, restore focus out

```tsx
export function Modal({ isOpen, onClose, title, children }: { isOpen: boolean; onClose: () => void; title: string; children: React.ReactNode }) {
  const modalRef = useRef<HTMLDivElement>(null);
  const previousFocusRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (isOpen) {
      previousFocusRef.current = document.activeElement as HTMLElement;
      modalRef.current?.focus();
    } else {
      previousFocusRef.current?.focus();
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div ref={modalRef} role="dialog" aria-modal="true" aria-labelledby="modal-title" tabIndex={-1} onKeyDown={(e) => e.key === 'Escape' && onClose()}>
      <h2 id="modal-title">{title}</h2>
      {children}
      <button onClick={onClose}>Close</button>
    </div>
  );
}
```

This covers **initial focus** and **restoration** only. It does not trap Tab/Shift+Tab inside the
modal — without a trap, Tab can escape to page content behind the modal. For a real focus trap
(handles nested portals, dynamically-added content), use a library like `focus-trap-react` rather
than hand-rolling the Tab-cycling logic.

## Checklist for any focus-moving component

- [ ] Save `document.activeElement` before moving focus away from it
- [ ] Move focus to a sensible target on open (the dialog container, or its first field — not left
      on `<body>`)
- [ ] Restore focus to the saved element on close, not just to `<body>`
- [ ] `role="dialog"` + `aria-modal="true"` + `aria-labelledby` pointing at the visible title
- [ ] Escape closes it
- [ ] Tab is trapped inside while open (use a library for this part)

## Related

- `a11y-semantics-aria` — `aria-expanded`/`aria-controls` for non-modal disclosure widgets that
  don't need focus trapping, just the ARIA state.
- `a11y-keyboard-nav` — keyboard handling for widgets that live *inside* the modal (a listbox,
  combobox, etc.), on top of the modal's own focus trap.
