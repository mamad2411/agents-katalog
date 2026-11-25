---
name: ui-part-buttons
description: "Buttons: hierarchy and variants, sizes and spacing, labels, icons and icon-only buttons, every state (hover, focus, pressed, toggled, loading, disabled), button or link, groups and split buttons, destructive actions, placement and phones. Read before building or restyling any button."
---

# Buttons

The generated version: every button a gradient pill with a glow and an
arrow, two filled buttons side by side, "Submit" and "Get started", a
spinner that makes the button shrink, a greyed-out button with no reason,
and a `div` with a click handler. A button is a promise of one action;
this is how to rank it, word it, size it and give it every state. One part
of an interface: the principles (direction, spacing, type, colour, icons,
states, accessibility) are in the `ui` skill, the measures in `ui-layout`.

## 1. Hierarchy

- One primary button per view (a screen, a dialog, a card with its own
  task): the action most people take next. Secondary and text buttons sit
  below it in weight. Never two primaries side by side.
- Primary: filled with the accent, `--on-accent` text at 4.5:1.
- Secondary: the surface with a 1px border that reaches 3:1, or a tinted
  surface, for the second most likely action.
- Tertiary (ghost): the text colour, no border, a surface on hover; for
  toolbars, table rows and dismissive actions. Cancel is ghost or
  secondary, never filled.
- Text button: looks like a link, is a `button`, for inline actions
  ("Undo", "Edit").
- Destructive: looks it, in the danger colour. The entry point is a quiet
  button or a menu item in danger text; the filled danger button appears
  in the confirming step.
- `preview` counts filled buttons: five or more in one saturated colour on
  a screen means rows carry primaries; make them quiet
  (`ui-page-dashboard`).

## 2. Sizes and anatomy

| Size | Height | Side padding | Text | Icon | Where |
|---|---|---|---|---|---|
| Compact | 32px | 12px | 13 to 14px | 16px | table rows, toolbars, dense panels |
| Default | 36 to 40px | 16px | 14 to 15px | 16 to 20px | application screens, forms, dialogs |
| Large | 44 to 48px | 20 to 24px | 16px | 20px | pages, the hero, phones |

- At least 44px tall to the touch: compact and default buttons grow to
  44px on phones (`preview` lists anything smaller at 360px).
- Padding from the spacing scale; 8px between icon and label; 8px between
  neighbouring buttons, 12px on touch.
- Weight 500 to 600, sentence case, one line (`white-space: nowrap`), a
  radius from the token set (4 to 8px). Fully round only when the design
  language is round everywhere, not as the default look.
- A minimum width (about 80px) so "Save" is not a stamp beside "Save and
  send".

## 3. Labels and icons

- The label is a verb and an object that says the outcome: "Create
  invoice", "Send reminder", "Book a first appointment". Not "Submit",
  "OK", "Yes", "Click here", "Get started" or "Learn more" (`ui_check`
  flags them), and never one word on two buttons that do different things.
- A confirming button repeats the verb of its question: "Delete project?"
  is answered by "Delete project", not "Yes" (`writing`).
- A trailing "…" when the action asks for more before it happens
  ("Rename…", "Export…"), the desktop convention; not on actions that
  complete at once.
- An icon beside the label when the product's set has a clear one for the
  action (plus, download, trash): leading, 16 to 20px, `currentColor`,
  `aria-hidden="true"`.
- A trailing chevron only on a button that opens a menu; a trailing arrow
  only on "Next" or a link that goes somewhere. Not an arrow on every
  button.
- Icon-only buttons in dense toolbars and rows: 36 to 40px square (44px on
  touch), an `aria-label` that names the action ("Delete invoice"), and a
  tooltip with the same name on hover and focus (`ui-part-tooltips`).

## 4. States

| State | Look | Behaviour |
|---|---|---|
| Hover | a background step of 4 to 8%, over 160ms | only under `(hover: hover)` |
| Focus-visible | a 2px ring in `--focus`, 2px offset, no transition | reached by Tab in visual order |
| Pressed | `scale(0.97)` for 100ms, or a darker step | none under reduced motion |
| Toggled | a filled surface and weight, `aria-pressed="true"` | the label stays the same |
| Loading | a spinner over the label, the width kept | `aria-busy="true"`, clicks ignored |
| Disabled | legible but clearly off, no hover | the reason stated nearby |

- Loading: `aria-busy` set after about 300ms of waiting, so quick work
  shows no spinner; the label stays in place under it (transparent), so
  the width and the accessible name hold; clicks are ignored from the
  first one, so the form is sent once; "Saving", then "Saved" or the
  error, announced through a `role="status"` region. Keep the button
  focusable: making the pressed button `disabled` drops the keyboard
  focus, and a screen reader loses its place.
- Disabled: say why near it ("Add a payment method to publish"), or leave
  it enabled and explain on click. A submit button stays enabled and the
  form shows what is missing (`frontend-forms`). Where it must look
  disabled, `aria-disabled="true"` keeps it focusable and readable, with
  the click stopped in script.
- After the action the result shows: the new row, or a toast ("Invoice
  sent", with Undo, `ui-part-notifications`). A button that reads "Saved"
  goes back to "Save" after 2 to 3 seconds or when the form changes.

## 5. Button or link

- `a href` navigates: to a page, a section, a file, another site. It opens
  in a new tab with a middle click, shows its URL, works before the script
  loads.
- A `button` element acts: saves, sends, opens a dialog or a menu,
  toggles. `type="button"` unless it submits: inside a `form` the default
  is submit, which sends the form by accident.
- The look follows the rank, the element follows the behaviour: "Book a
  session" leading to the booking page is a link that looks like a primary
  button. Never a `div` or `span` with a click handler.

## 6. Groups, split buttons, placement

- In footers and dialogs the primary sits at the end of the reading
  direction (the right on desktop, in left-to-right languages), Cancel
  beside it; the project's own convention wins (`ui-layout` 4).
- Past two secondary actions, the rest go into a "More" menu button
  (`aria-haspopup="menu"`, `aria-expanded`, `ui-part-menus`).
- A split button: the main action, and beside it a chevron button with
  `aria-label="More save options"` opening a menu ("Save as draft", "Save
  and send"). Both halves are real buttons.
- Segmented controls pick a view or a filter: they are choices, not
  buttons (`ui-part-choices`).
- Destructive actions stand apart from Save (a "Danger zone" at the end, or
  a menu). They confirm, in a dialog naming the object
  (`ui-part-dialogs`), when the loss is large and permanent; they offer
  Undo instead when the action is frequent and reversible.

## 7. Phones

- Full width only on phone forms and sheets: stacked, the primary on top,
  Cancel below it. Elsewhere buttons keep their width.
- The screen's primary action stays in reach: in the top bar with its
  word, at the end of the content, or in a bar fixed to the bottom above
  the safe area (`ui-layout` 9).
- Labels may shorten ("Add" for "Add product") but never become an
  unnamed icon. Rows of buttons wrap or fold into a menu; never off the
  edge.

## 8. Themes and motion

- The accent takes a lighter step on dark to keep 3:1 against the page and
  4.5:1 for its label; the focus ring shows in both themes (`ui-themes`).
- Hover, press and focus as in `motion-interface`: colour over 160ms,
  press at 100ms, no bounce, no shine sweeping across, no pulse.

## 9. A sketch

```css
.btn {
  display: inline-flex; align-items: center; justify-content: center; gap: 8px;
  min-block-size: 40px; min-inline-size: 80px; padding-inline: 16px;
  font: inherit; font-size: 14px; font-weight: 500; white-space: nowrap;
  border: 1px solid transparent; border-radius: var(--radius-sm); cursor: pointer;
  transition: background-color var(--m-fast) var(--m-ease-out),
    border-color var(--m-fast) var(--m-ease-out), transform var(--m-instant) var(--m-ease-out);
}
.btn:focus-visible { outline: 2px solid var(--focus); outline-offset: 2px; }
.btn--primary { background: var(--accent); color: var(--on-accent); }
.btn--secondary { background: var(--surface); color: var(--text); border-color: var(--border-strong); }
.btn--ghost { background: transparent; color: var(--text); }
.btn--danger { background: var(--danger); color: var(--on-danger); }
@media (hover: hover) {
  .btn--primary:hover { background: var(--accent-hover); }
  .btn--secondary:hover, .btn--ghost:hover { background: var(--surface-2); }
}
.btn:not([aria-disabled="true"], [aria-busy="true"]):active { transform: scale(0.97); }
.btn[aria-disabled="true"], .btn:disabled {
  background: var(--surface-2); color: var(--text-muted);
  border-color: var(--border); cursor: not-allowed;
}
.btn[aria-busy="true"] { position: relative; }
.btn[aria-busy="true"] > * { color: transparent; } /* keeps the width and the name */
.btn[aria-busy="true"]::after {
  content: ""; position: absolute; inset: 0; margin: auto;
  inline-size: 16px; block-size: 16px; border-radius: 50%;
  border: 2px solid currentColor; border-inline-end-color: transparent;
  animation: spin 0.9s linear infinite;
}
@keyframes spin { to { rotate: 1turn; } }
@media (max-width: 640px) { .btn { min-block-size: 44px; } }
@media (prefers-reduced-motion: reduce) { .btn:active { transform: none; } }
```

```html
<button class="btn btn--primary" type="submit" aria-busy="true">
  <span>Save changes</span>
</button>
<p class="visually-hidden" role="status">Saving changes</p>
```

With shadcn, the same variants live in the Button's `cva` definition
(`variant`, `size`), used by name (`ui-stack-shadcn`).

## Check it

- `preview` at 360px: no button in "touch targets under 44px" or
  "controls without a name"; no report of five or more filled buttons in
  one colour; labels at 4.5:1 in both themes.
- `ui_check`: generic actions, glow, default gradients, pills everywhere,
  empty click handlers and `href="#"`.
- Keyboard only: Tab reaches every button in visual order with a visible
  ring; Enter and Space act; after a submit, focus has not jumped away.
- Double-click a submit on a slow network: one request is sent.
- Search for `div` and `span` with click handlers, and `a` elements that
  act without navigating.

## Avoid

An arrow on every button; pill plus gradient plus glow as the default
look; "Submit", "Click here", "Get started"; two primaries side by side; a
primary on every row; a greyed-out button with no reason; a spinner that
changes the button's width; `disabled` on the button that was just
pressed; a `div` that acts as a button; a link that acts, or a button that
navigates; a destructive action next to Save; full-width buttons on wide
screens.
