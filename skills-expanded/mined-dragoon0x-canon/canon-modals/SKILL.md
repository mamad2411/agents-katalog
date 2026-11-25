---
name: canon-modals
description: Use when designing, auditing, or refactoring modal dialogs, alert dialogs, confirmation dialogs, drawers, popovers, sheets, or any overlay pattern. Covers when to use a modal vs page vs inline, focus trap, escape behavior, scroll locking, sizing, the dialog element, and modal stacking. Trigger when the user mentions modal, dialog, popup, drawer, sheet, overlay, or confirm.
---

# CANON · Modals

A modal interrupts the user. Every modal should justify the interruption. Most shouldn't exist.

## When to use a modal

| Use modal | Don't use modal |
|---|---|
| Confirming a destructive action with no undo | Confirming a reversible action (use Undo toast) |
| Focused task that requires full attention (image edit, payment) | Editing a field (inline edit) |
| Error or warning blocking progress | Informational messages (toast/banner) |
| Critical form that must complete before continuing | Forms that can live on a page |
| Collecting user input for current flow only | Secondary workflows (new tab/page) |

**Undo beats confirm.** A toast with "Item deleted. [Undo]" is almost always better than "Are you sure?"

## Modal vs drawer vs popover vs sheet

| Pattern | Overlay | Blocks page | Anchored | Use |
|---|---|---|---|---|
| Modal dialog | Full | Yes | Center | Critical decisions, focused tasks |
| Drawer (side) | Partial | Yes | Edge | Settings panels, filters, nav |
| Popover | None | No | Element | Supplemental info, small forms |
| Bottom sheet (mobile) | Partial | Yes | Bottom | Mobile primary pattern for drawers |
| Fullscreen sheet (mobile) | Full | Yes | Full | Complex mobile tasks |

## Use the `<dialog>` element

Native `<dialog>` handles focus trap, ESC, backdrop, and scroll lock for free. Stop reinventing it.

```html
<dialog id="confirm-delete">
  <h2>Delete project?</h2>
  <p>This permanently removes the project and all 47 files.</p>
  <div class="actions">
    <button value="cancel">Cancel</button>
    <button value="confirm" class="destructive">Delete project</button>
  </div>
</dialog>

<script>
  const dialog = document.getElementById('confirm-delete');
  dialog.showModal(); // Modal with backdrop + focus trap
  // dialog.show();  // Non-modal
</script>
```

If you must build without `<dialog>`, the requirements below are non-negotiable.

## Required behaviors

1. **Focus moves into the dialog on open.** The first focusable element, or the most useful (e.g., the primary action).
2. **Focus trapped inside.** Tab and Shift+Tab cycle within. Nothing outside is reachable.
3. **Focus returns to trigger on close.** The element that opened the modal gets focus back.
4. **Escape closes.** Unless explicitly forbidden (rare).
5. **Click outside closes.** For non-critical modals. For critical confirmations, require explicit button press.
6. **Scroll locked on body.** No scrolling behind the modal. `overflow: hidden` on `<html>`, not `<body>` — that loses scroll position on mobile Safari.
7. **Backdrop visible.** 40–60% opacity black or tinted dark with blur for modern feel.
8. **`role="dialog"` or `role="alertdialog"`.** Alertdialog for critical confirmations.
9. **`aria-labelledby` pointing to the heading.** Or `aria-label` if no visible heading.

## Sizing

| Size | Width | Use |
|---|---|---|
| Small | 320–400px | Confirmations, quick messages |
| Medium | 480–560px | **Default.** Forms, standard content |
| Large | 640–800px | Complex forms, settings |
| XL | 900–1120px | Data-heavy edit screens |
| Fullscreen | 100% | Mobile, image editors, complex flows |

Max height: `min(90vh, 720px)`. Content scrolls inside the modal, header and footer stay sticky.

Padding: 24px on medium+ desktop, 16px on mobile.

## Mobile — bottom sheet by default

On mobile, centered modals are awkward. Bottom sheets feel native.

- Slide from bottom with 250–300ms ease-out.
- Drag handle at top (4×40px pill).
- Swipe down to dismiss.
- Fills 60–90% of viewport height, scrolls inside.

Reserve centered modals on mobile for true alert dialogs.

## Stacking modals — avoid, but if you must

At most 2 modals stacked. Beyond that, the flow is wrong.

- Second modal has higher z-index.
- Closing the second restores focus to the first.
- Escape closes one at a time, not all.
- **If stacking happens often, redesign the flow.**

## Animation

| Phase | Duration | Easing |
|---|---|---|
| Enter | 200–250ms | ease-out |
| Exit | 150–200ms | ease-in |
| Backdrop fade | same as modal | same |

Avoid scale animations beyond 0.96–1.0 (too bouncy reads childish).

Honor `prefers-reduced-motion` with opacity-only fallback.

## Copy

- **Title** is a statement, not a question. "Delete project" or "Deleting project" beats "Are you sure?"
- **Body** explains consequences, specific. "This permanently removes the project and all 47 files" beats "This cannot be undone."
- **Primary button** names the action. "Delete project" not "Yes". "Save changes" not "OK".
- **Secondary button** is usually "Cancel". Plain. Not "No" (pairs poorly with verb-primaries).

## Destructive confirmations — the extra step

Type-to-confirm is appropriate for truly irreversible actions.

```
Type "delete" to confirm.
[______________]
[Delete permanently]
```

Reserve for: account deletion, workspace deletion, database drops. Overused, it becomes ignored.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Confirmation modal for every save | Alert fatigue, users stop reading |
| "Are you sure?" as the title | Not informative |
| "OK" / "Cancel" as button labels | Violates canon-ux-writing; buttons should be verbs |
| Modal without focus trap | Keyboard users escape into the background |
| Modal without Escape close | Keyboard users trapped |
| Focus not returned to trigger on close | Disorienting |
| Autofocus on destructive primary button | Accidental confirmation on Enter |
| Three or more modals stacked | Flow is wrong |
| Modal for a settings form that fits on a page | Wasted interruption |
| No backdrop click-to-close on non-critical modals | Forces explicit close |
| Backdrop click closes critical destructive modal | Accidental dismissal = accidental action (wait, reverse this — backdrop close on destructive is actually risky. Require explicit Cancel.) |

## Focus-on-open strategy

| Modal type | Autofocus |
|---|---|
| Form modal | First input |
| Confirmation (safe) | Primary button |
| Confirmation (destructive) | **Cancel button** — not the destructive action |
| Alert (info only) | Primary / OK button |
| Empty modal / message | Close button |

## Decision tree

```
Does the user need to make a decision that blocks everything else?
  ├─ No → Don't use a modal (use toast, banner, inline, or new page)
  └─ Yes →
     Is the action reversible?
       ├─ Yes → Prefer Undo toast over confirmation
       └─ No → Proceed with modal
          Is this a critical destructive action?
            ├─ Yes → role="alertdialog", default focus on Cancel, require explicit confirm
            └─ No → role="dialog", default focus on primary or first input
```

## Audit checklist

- [ ] Modal uses `<dialog>` or has `role="dialog"` / `"alertdialog"`
- [ ] `aria-labelledby` points to the heading
- [ ] Focus moves into the modal on open
- [ ] Focus is trapped inside
- [ ] Focus returns to trigger on close
- [ ] Escape closes (unless explicitly forbidden for alert dialogs)
- [ ] Background scroll locked
- [ ] Title is a statement, not "Are you sure?"
- [ ] Primary button names the action (verb)
- [ ] Destructive confirms default focus on Cancel
- [ ] Mobile uses bottom sheet pattern where appropriate
- [ ] prefers-reduced-motion honored
- [ ] Max height prevents overflow on short viewports
- [ ] Backdrop has visible contrast (not invisible)

## Sources

- WAI-ARIA Authoring Practices · Dialog (Modal), Alert Dialog
- WCAG 2.2 · 2.1.2 No Keyboard Trap, 2.4.3 Focus Order, 1.3.1 Info and Relationships
- HTML Living Standard · The `<dialog>` element
- Apple HIG · Sheets, Alerts
- Material Design 3 · Dialog
- Refactoring UI · "Use fewer borders" (applied to modal chrome)
