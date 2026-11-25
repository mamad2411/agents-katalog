---
name: ui-part-drawers
description: "Drawers, side panels and bottom sheets: detail and editing beside a list, modal or not, the open record in the URL, structure and widths, focus and closing, sheets with a handle and snap points, filters on phones, unsaved changes and stacking order. Read before building a panel or a sheet that slides in."
---

# Drawers and sheets

The generated version: a drawer that covers the list the user was working
through, a drawer opened from a drawer, a bottom sheet you can only close
by dragging, a footer that scrolls away with the content, and a record
that vanishes on reload because it was never in the URL. A drawer keeps
the current view in place while a detail or a secondary task sits beside
it; this is how to size it, wire it and close it. One part of an
interface: the principles (direction, spacing, type, colour, icons,
states, accessibility) are in the `ui` skill, the measures in `ui-layout`.

## 1. Which one

| Need | Use |
|---|---|
| Read or edit a record while the list stays visible | a side panel from the right, 400 to 560px |
| Go through records one after another on a wide screen | a split view: the list and a detail pane |
| Filters, sorting and short choices on a phone | a bottom sheet |
| The application's navigation under 1024px | a drawer from the left (`ui-part-sidebar`) |
| A decision that must be answered now | a dialog (`ui-part-dialogs`) |
| A long task, or a record that needs the whole screen | its own page |

- Use them for details or a secondary task beside the current view; not
  for the screen's main task, and not for content that needs the full
  width to be compared.

## 2. Modal or not

- Modal (a scrim, the page inert, focus kept inside): for editing, and
  under about 1024px, where the panel covers most of the page anyway.
- Non-modal (no scrim, the list narrows or the panel sits beside it, both
  usable): for inspecting records one by one on a wide screen. It is a
  region (`aside` with an `aria-label`), not a dialog: no focus trap, but
  Escape still closes it and focus returns to the row.
- The open record lives in the URL (`?invoice=INV-0042`, or a nested
  route), so a reload, the back button and a shared link all open it
  again. Opening adds a history entry; Back closes the panel before it
  leaves the page.

## 3. Structure and measures

- Side panel: full height, from the right, 400 to 560px wide (`inline-size:
  min(480px, 100vw)`), 640 to 720px for a wide editor, full screen on a
  phone: a width that leaves the page visible on wide screens.
- Header, 56 to 64px: the title (an `h2`, the record's name) and the close
  button at the right (40px, 44px on touch, `aria-label="Close"`); for
  records, previous and next buttons beside it.
- Body: scrolls on its own (`overflow-y: auto`) with
  `overscroll-behavior: contain`, so reaching its end does not scroll the
  page behind; padding 16 to 24px.
- Footer: fixed to the panel's bottom, with the actions (primary at the
  right, Cancel beside it), a hairline above and the safe area below
  (`env(safe-area-inset-bottom)`).
- A hairline on the open edge; a shadow only on the modal kind.

## 4. Bottom sheets

- For filters, sorting and short choices on phones: from the bottom edge,
  12 to 16px radius on the top corners, at most 90% of the screen's height
  (`max-block-size: 90dvh`).
- A drag handle 32 to 40px wide and 4 to 5px tall, centred, 8px from the
  top, to drag it closed; never the only way: a close or "Done" button and
  Escape do it too. A drag starts from the handle or the header, so
  scrolling the content does not close the sheet.
- Snap points (half and nearly full) only when the content gains from
  them: a map with results, a long list. A short sheet is as tall as its
  content.
- A filter sheet: the filters, then a footer with "Clear all" and a
  primary that says what it will show ("Show 24 results", counted live);
  the filters apply when it is pressed. The button that opened it shows
  how many are active ("Filters · 2", `ui-layout` 9).

## 5. Behaviour and keyboard

- The same focus and closing rules as a dialog: focus moves in on open
  (the title with `tabindex="-1"`, or the first field when editing), stays
  inside a modal drawer, and returns to the trigger or the row on close;
  Escape, the close button and the scrim close it.
- Do not open a drawer from a drawer. A related record replaces the
  panel's content, with a back button in its header, or opens its own
  page.
- Unsaved changes: closing an edited form (Escape, scrim, close, Back) asks
  in place, in the footer: "Discard changes?" with "Discard" and "Keep
  editing". Or it saves as the user types (`frontend-forms`).
- The navigation drawer closes when a link is chosen, and focus goes to
  the new page's heading (`ui-part-sidebar`).
- Libraries: a side panel is a dialog placed at an edge: Radix Dialog
  (shadcn's Sheet), React Aria `Modal`, Headless UI `Dialog`, Ark UI, Bits
  UI; the native `dialog` in plain HTML. Sheets with dragging and snap
  points: shadcn's Drawer (Vaul underneath) or react-modal-sheet.
- One stacking order, as tokens: the sticky header, then drawers, then
  dialogs, then toasts, so a confirmation never opens under a drawer. The
  native `dialog` and `popover` sit in the top layer and need none.

## 6. Themes and motion

- The panel is a surface step with a hairline; the scrim has a value per
  theme (`ui-themes`).
- It slides from its edge with a transform, 320ms in and 200ms out; a
  sheet follows the finger one to one and settles by distance and speed;
  under reduced motion a short fade or nothing. Never animate `left` or
  `width` (`motion-interface` 5).

## 7. A sketch

React with Radix Dialog as a panel, its open record in the URL (React
Router):

```tsx
import * as Dialog from "@radix-ui/react-dialog";
import { useSearchParams } from "react-router";

export function InvoicePanel() {
  const [params, setParams] = useSearchParams();
  const id = params.get("invoice");
  const close = () => setParams((p) => { p.delete("invoice"); return p; });
  return (
    <Dialog.Root open={id !== null} onOpenChange={(open) => { if (!open) close(); }}>
      <Dialog.Portal>
        <Dialog.Overlay className="scrim" />
        <Dialog.Content className="panel" aria-describedby={undefined}>
          <div className="panel__head">
            <Dialog.Title>Invoice {id}</Dialog.Title>
            <Dialog.Close className="icon-btn" aria-label="Close">
              <XIcon aria-hidden="true" />
            </Dialog.Close>
          </div>
          <div className="panel__body">{id && <InvoiceDetail id={id} />}</div>
          <div className="panel__foot">{/* Cancel, then Save */}</div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
```

```css
.panel {
  position: fixed; inset-block: 0; inset-inline-end: 0;
  inline-size: min(480px, 100vw);
  display: flex; flex-direction: column;
  background: var(--surface); border-inline-start: 1px solid var(--border);
}
.panel__head {
  display: flex; align-items: center; justify-content: space-between; gap: 12px;
  min-block-size: 56px; padding-inline: 24px;
}
.panel__body { flex: 1; overflow-y: auto; overscroll-behavior: contain; padding: 24px; }
.panel__foot {
  display: flex; justify-content: flex-end; gap: 8px;
  padding: 16px 24px calc(16px + env(safe-area-inset-bottom));
  border-block-start: 1px solid var(--border);
}
```

## Check it

- Open a record and reload: it is still open. Press Back: the panel
  closes, the list is where it was, focus is on the row.
- Keyboard only: focus lands in the panel; Tab stays inside the modal
  kind; Escape closes it; focus returns to the trigger.
- Scroll the panel to its end: the page behind does not move, and the
  footer stays in view.
- At 360px (`preview`): the panel is full screen, nothing overflows, the
  close button is 44px and named, a sheet's actions sit above the safe
  area.
- Edit something, then press Escape: the discard question appears.

## Avoid

A drawer from a drawer; a drawer covering the list the user works through
on a wide screen; a sheet closed only by dragging; a footer that scrolls
away; an open record that is not in the URL; a page that scrolls under the
panel; animating `left` or `width`; the screen's main task in a drawer; a
filter sheet whose button does not say what it will show.
