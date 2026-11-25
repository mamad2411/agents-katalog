---
name: ui-part-forms
description: "Forms and fields, their look and layout (the logic is in frontend-forms): labels, help and error text, one column and field widths, required and optional, input types, inputmode and autocomplete, every field state, long forms and the save bar, actions, phones and themes. Read before building or restyling a form."
---

# Forms and fields

The generated version: placeholders standing in for labels and vanishing
at the first keystroke, two columns of fields on a phone, a red border as
the only sign of an error, "Submit" beside a reset button, 14px inputs
that make iOS zoom, and every field as wide as the page whatever it holds.
This is how a form looks and is laid out so it is quick to fill and hard
to get wrong; its behaviour (when to validate, submitting, server errors,
unsaved changes) is in `frontend-forms`. One part of an interface: the
principles (direction, spacing, type, colour, icons, states,
accessibility) are in the `ui` skill, the measures in `ui-layout`, form
pages in `ui-page-form` and `ui-page-settings`.

## 1. Layout

- One column; related fields in a `fieldset` with a `legend` (an address,
  a card, a date of birth in three parts).
- A visible label above each field; the placeholder is an example, never
  the label.
- Field width follows the expected answer: a postcode 8 to 10 characters,
  a card's security code 5, a phone number 16 to 20, a name or an email
  the column's width (up to about 480px). Set it in `ch` (`max-inline-size:
  10ch`), so the width hints at the answer.
- Short related fields may pair on one row (city and postcode, expiry and
  security code); everything else stacks. One field for a full name,
  unless the system truly needs the parts.
- Spacing: 6 to 8px from label to field, 16 to 24px between fields, 32 to
  48px between sections.
- A long form gets section headings (`h2`) with a line on what each is
  for; past about three sections, consider steps or a page per part
  (`ui-page-form`).

## 2. Anatomy and measures

- Label 14px, weight 500 (16px on a page people read). Help text 13 to
  14px in the muted colour, between the label and the field so it is read
  first, tied to the field with `aria-describedby`.
- Input 40 to 44px tall (44px on touch), 12px side padding, the body
  font, a radius from the token set, and a 1px border at 3:1 against the
  background, since the border is how the field is seen.
- 16px text in inputs on phones, or iOS zooms the page on focus.
- Textarea: at least 3 rows, resizable vertically, or growing with its
  content (`field-sizing: content` where supported).
- Error text under the field, 13 to 14px, in the danger colour with an
  icon and words.

## 3. Required, optional, help

- Required fields marked in words, or with a mark that is explained. When
  most are required, mark the few optional ones "(optional)" instead; the
  `required` attribute on the input either way.
- Help text says what to enter and why, before the user gets it wrong:
  "We send the receipt here." Never a restatement of the label.
- Character counters only near a limit: shown from about 80% of it, in
  words ("20 characters left").
- No input masks that fight typing: accept spaces, dashes and pasting;
  show the format in the help text, or tidy it when the field is left.

## 4. Types, keyboards, autofill

| Field | `type` | `inputmode` | `autocomplete` |
|---|---|---|---|
| Email | `email` | | `email` |
| Phone | `tel` | | `tel` |
| Full name | `text` | | `name` |
| Street address | `text` | | `street-address`, or `address-line1` |
| Postcode of digits only | `text` | `numeric` | `postal-code` |
| One-time code | `text` | `numeric` | `one-time-code` |
| Amount of money | `text` | `decimal` | `transaction-amount` |
| Card number | `text` | `numeric` | `cc-number` |
| New password | `password` | | `new-password` |
| Current password | `password` | | `current-password` |
| Web address | `url` | | `url` |

- The right type, `inputmode` and `autocomplete` value, so phones show the
  right keyboard and browsers fill what they can. Never
  `autocomplete="off"` on a field the browser could fill.
- `type="number"` only for quantities: it accepts "e", changes with the
  scroll wheel in some browsers, and loses leading zeros once read as a
  number. Codes, card numbers, phones and postcodes are text.
- `enterkeyhint` ("next", "send", "search", "done") labels the phone's
  Enter key; `autocapitalize="off"` and `spellcheck="false"` on usernames
  and codes.

## 5. States

| State | Look |
|---|---|
| Default | the border at 3:1, the surface behind it |
| Hover | the border one step stronger |
| Focus | a 2px ring in `--focus` (text fields show it on click too), the border in the accent |
| Invalid | the border in the danger colour, the message under it with an icon, `aria-invalid="true"` |
| Disabled | not focusable, not sent; muted but legible, with the reason nearby |
| Read-only | focusable, selectable and sent; no border, or a quiet surface, so it reads as a value |
| Loading | a small spinner at the field's end while options or a check load |
| Valid | usually nothing; a check only where it answers a question ("Username available") |

- The error sits under its field, in words that say how to fix it ("Enter
  a date after today", not "Invalid input"), tied to it with
  `aria-describedby`; a long form also lists the errors at the top, each a
  link to its field.
- Check on submit and when a field is left, not on every keystroke
  (`frontend-forms` has the timing).
- Keep what the user typed after an error. Show that the form sent, and
  what happens next: "Message sent. We reply within [time]."
- Disabled is not read-only: a value the user may see and copy but not
  change is read-only.

## 6. Actions

- The submit button says what happens ("Create account", "Send message",
  "Book appointment"), never "Submit"; at the end of the form, aligned
  with the fields' left edge, Cancel beside it as a quieter button or a
  link (`ui-layout` 4).
- No reset button. A destructive action (deleting the account) stands
  apart at the end, in a "Danger zone" (`ui-page-settings`).
- A long edit form (settings, a record) gets a sticky save bar once
  something has changed: "Unsaved changes" with Discard and Save,
  `position: sticky; bottom: 0`, a solid background and a hairline above.
- While it sends, the button shows its busy state and keeps its width
  (`ui-part-buttons`); the fields stay filled.

## 7. Phones, themes, motion

- One column always; fields full width; paired fields stack below about
  480px; the submit button full width at the end, or in a bar fixed to the
  bottom of a long form.
- Themes: `color-scheme` per theme, so date pickers, autofill and
  scrollbars follow; the border at 3:1 and the focus ring visible in both;
  `caret-color` from a token. Autofill a field in each theme to see its
  tint (`ui-themes`).
- Motion: an error fades in over 160ms; no shake; success is a check that
  draws once, or the word "Saved"; no confetti (`motion-interface` 12).

## 8. A sketch

```html
<div class="field">
  <label for="email">Email</label>
  <p class="field__hint" id="email-hint">We send the receipt here.</p>
  <input id="email" name="email" type="email" autocomplete="email" required
    aria-describedby="email-hint email-error" aria-invalid="true">
  <p class="field__error" id="email-error">
    <svg aria-hidden="true" width="16" height="16"><use href="#icon-alert" /></svg>
    Enter an email address, like name@example.com
  </p>
</div>
```

```css
.field { display: grid; gap: 6px; max-inline-size: 30rem; }
.field label { font-size: 14px; font-weight: 500; }
.field__hint { margin: 0; font-size: 14px; color: var(--text-muted); }
.field input {
  block-size: 44px; padding-inline: 12px; font: inherit; font-size: 16px;
  color: var(--text); background: var(--surface);
  border: 1px solid var(--border-strong); border-radius: var(--radius-sm);
}
.field input:focus-visible {
  outline: 2px solid var(--focus); outline-offset: 1px; border-color: var(--accent);
}
.field input[aria-invalid="true"] { border-color: var(--danger); }
.field__error {
  display: flex; align-items: center; gap: 6px; margin: 0;
  font-size: 14px; color: var(--danger-text);
}
```

The error element exists only while there is an error, and its id joins
`aria-describedby` only then. With shadcn, its Form (react-hook-form and
zod) wires the same ids (`ui-stack-shadcn`).

## Check it

- Keyboard only: the Tab order follows the visual order; every field has a
  visible label; Enter in the last field submits.
- Submit it empty: each error sits under its field in words, focus goes to
  the first one (or the summary), and nothing typed is lost.
- `preview` at 360px: one column, no overflow, no input under 44px, no
  "controls without a name". On a real phone, each field brings up the
  right keyboard.
- Autofill a name, an email and an address: the browser fills them.
- `ui_check` flags "Submit" and focus outlines removed without a
  replacement.
- A screen reader reads each label, its help, "required", and the error
  when the field is invalid.

## Avoid

Placeholder-only fields, errors shown only as a red border, a reset
button, a submit that clears everything on failure; two columns on a
phone; every field full width whatever it holds; `type="number"` for
codes; 14px inputs on phones; input masks that fight typing; disabled
fields where read-only was meant; "Submit"; a counter on every field;
errors on the first keystroke.
