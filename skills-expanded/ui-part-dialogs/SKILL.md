---
name: ui-part-dialogs
description: "Dialogs (modals) and confirmations: when a dialog is right and when a page or a panel is, structure and sizes, wording that names the action and the object, the native dialog element and libraries, focus, Escape, backdrop and scroll lock, unsaved changes, and phones. Read before opening anything in a dialog."
---

# Dialogs (modals)

The generated version: a newsletter modal on page load, "Are you sure?"
with Yes and No, a long form squeezed into a box while the page scrolls
behind it, focus left on the page underneath, no way out but a tiny ×, and
a second dialog opened over the first. A dialog interrupts; this is when
the interruption is worth it, and how to build one that holds focus, says
exactly what will happen, and lets go cleanly. One part of an interface:
the principles (direction, spacing, type, colour, icons, states,
accessibility) are in the `ui` skill, the measures in `ui-layout`.

## 1. Dialog, panel or page

- A dialog for a decision that interrupts, or a short form tied to the
  current screen (rename, invite, confirm), up to about five fields.
- A page for long forms, for anything with steps, and for content that
  deserves a URL (a record, an article, an area of settings).
- A side panel when the list behind must stay visible, or the user moves
  from record to record (`ui-part-drawers`).
- A popover or a menu for a light choice beside its trigger
  (`ui-part-menus`); a toast or an inline message for news that needs no
  answer (`ui-part-notifications`).
- Never on page load: no newsletter or promotion modals, no cookie walls
  beyond what the law requires, no exit-intent pop-ups.

## 2. Structure and sizes

- Title: the question or the task, as an `h2`: "Delete the project
  [name]?", "Invite people to [workspace]".
- Body: what the user needs to decide, in a sentence or two, or the few
  fields.
- Footer: the actions, the primary at the right on desktop, Cancel beside
  it; stacked and full width on phones.
- A close button (×) at the top right of content and form dialogs, 32 to
  40px (44px on touch), `aria-label="Close"`; in a confirmation, Cancel is
  that control.
- 400 to 480px wide for a confirmation, 560 to 640px for a small form,
  never wider than the screen minus 32px. At most the screen's height
  minus 48px: the body scrolls while the title and the actions stay in
  view.
- Padding 24px (16px on phones); title 18 to 20px, weight 600; body 14 to
  16px; radius 12px; a shadow, since it sits above the page, and a hairline
  on dark; the backdrop a `--scrim` token at 40 to 60% black.

## 3. Words

- A destructive confirmation names the action, the object and what will
  be lost: "Delete 3 invoices? This cannot be undone." The button repeats
  the verb ("Delete invoices"), never "Yes" or "OK"; Cancel says "Cancel",
  or "Keep invoices" when that is clearer.
- One primary action. The destructive button in the danger colour, and not
  the default focus.
- For a large, permanent loss (a workspace and everything in it) the user
  types its name to confirm. For a frequent, reversible action there is no
  dialog: do it and offer Undo (`ui-part-buttons`).

## 4. Behaviour and ARIA

- The native `dialog` element, opened with `showModal()`: the page behind
  becomes inert, the dialog sits in the top layer (no z-index to fight),
  Escape closes it, focus returns to the opener. Or `role="dialog"` with
  `aria-modal="true"`, through a library that does all of that.
- Labelled by its title (`aria-labelledby`), described by its message
  (`aria-describedby`) when it has one. A confirmation that interrupts is
  `role="alertdialog"` (the APG alert dialog; the keys of both patterns are
  in `frontend-accessibility`).
- Focus moves into it when it opens, stays inside, and returns to what
  opened it when it closes. It lands on the first field of a form, on
  Cancel in a destructive confirmation, on the title (`tabindex="-1"`) when
  the body is long text: put `autofocus` on that element.
- Escape and a visible, labelled close button both close it. A click on the
  backdrop closes it too, unless the user has typed something: then it
  stays open, or asks first.
- The page behind does not scroll: `html:has(dialog:modal) { overflow:
  hidden; }`, with `scrollbar-gutter: stable` on `html` so nothing shifts.
- No dialogs opened from dialogs. A second question ("Discard your
  changes?") replaces the footer inside the same dialog: "Discard" and
  "Keep editing".
- Libraries: Radix Dialog and AlertDialog (shadcn's Dialog and
  AlertDialog; its AlertDialog focuses Cancel and ignores clicks outside),
  React Aria `Modal` with `Dialog`, Headless UI `Dialog`, Ark UI, Bits UI,
  Melt. In plain HTML, the native element.

## 5. States

- Submitting: the primary button shows its busy state and the dialog stays
  open until the work is done. Success closes it, and a toast says what
  happened; failure shows the error inside, above the footer, with the
  fields kept.
- Content loading into a dialog: a skeleton at the final size, so it does
  not grow under the reader.

## 6. Phones

- A form dialog becomes full screen: a top bar with the close control at
  the left, the title, and the primary action at the right, or at the
  bottom above the safe area.
- A confirmation or a short choice becomes a bottom sheet, its actions
  stacked full width with the primary on top (`ui-part-drawers`).
- Try it with the on-screen keyboard open: the focused field and the
  primary action stay reachable.

## 7. Themes and motion

- On dark the dialog is a lighter surface step with a hairline; the
  backdrop stays dark enough to set it apart (`ui-themes`).
- The backdrop fades; the panel fades and scales from 0.96, or rises 8px,
  over 240 to 320ms, and leaves faster; under reduced motion it only fades
  (`motion-interface` 4 has the `@starting-style` pattern).

## 8. A sketch

```html
<button type="button" class="btn btn--ghost" id="delete-open">Delete project</button>

<dialog id="delete-dialog" role="alertdialog"
  aria-labelledby="delete-title" aria-describedby="delete-desc">
  <form method="dialog" class="dialog">
    <h2 id="delete-title">Delete the project [name]?</h2>
    <p id="delete-desc">Its tasks and files are deleted with it. This cannot be undone.</p>
    <div class="dialog__actions">
      <button value="cancel" class="btn btn--secondary" autofocus>Cancel</button>
      <button value="delete" class="btn btn--danger">Delete project</button>
    </div>
  </form>
</dialog>
```

```js
const dialog = document.getElementById("delete-dialog");
document.getElementById("delete-open").addEventListener("click", () => {
  dialog.returnValue = ""; // Escape keeps the last value otherwise
  dialog.showModal();
});
dialog.addEventListener("close", () => {
  if (dialog.returnValue === "delete") deleteProject();
});
// A click on the backdrop lands on the dialog itself, which has no padding.
dialog.addEventListener("click", (event) => {
  if (event.target === dialog) dialog.close("cancel");
});
```

```css
dialog {
  padding: 0; border: 1px solid var(--border); border-radius: 12px;
  inline-size: min(480px, 100% - 32px); max-block-size: calc(100dvh - 48px);
  background: var(--surface); color: var(--text);
}
dialog::backdrop { background: var(--scrim); }
.dialog { display: grid; gap: 16px; padding: 24px; }
.dialog__actions { display: flex; justify-content: flex-end; gap: 8px; }
html { scrollbar-gutter: stable; }
html:has(dialog:modal) { overflow: hidden; }
@media (max-width: 480px) {
  .dialog__actions { flex-direction: column-reverse; } /* primary on top, full width */
}
```

## Check it

- Keyboard only: open it, and focus is inside; Tab cycles within it;
  Escape closes it; focus is back on the button that opened it.
- A screen reader announces the title and, for a confirmation, the message.
- Scroll with the dialog open: the page behind does not move.
- At 360px (the `preview` tool, with the dialog open): it fits with no
  overflow, the close control is 44px and named, the text passes 4.5:1 in
  both themes; with `motion: true` the reduced-motion pass only fades it.
- Submit with the network off: the error shows inside, nothing typed is
  lost.
- `ui_check` flags empty click handlers and "Submit" in its footer.

## Avoid

A dialog on page load (newsletter, cookie walls beyond what the law
requires, exit-intent pop-ups); dialogs opened from dialogs; "Are you
sure?" with Yes and No; long forms in a modal; the destructive button
focused by default; a page that scrolls behind the backdrop; focus left
behind the dialog, or lost when it closes; a close icon with no name; a
dialog that zooms from nothing; content that deserves a URL shut in a
modal.
