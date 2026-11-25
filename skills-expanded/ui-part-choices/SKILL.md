---
name: ui-part-choices
description: "Choices: radios, checkboxes, switches, selects, comboboxes, segmented controls and choice cards; which to use when, labels and hit areas, groups and legends, defaults, states, the keyboard and ARIA patterns, libraries and phones. Read before asking a user to pick anything."
---

# Choices: select, radio, checkbox, switch

The generated version: a dropdown with two options, a switch inside a form
that only applies on Save, custom checkboxes the keyboard cannot reach, a
16px box that is the only clickable part, "Select an option" as the only
label, and a consent box ticked by default. Each kind of choice has a
control that fits it; this is the table to pick from, and how to build
each one so it is clicked, tapped and heard correctly. One part of an
interface: the principles (direction, spacing, type, colour, icons,
states, accessibility) are in the `ui` skill, the measures in `ui-layout`,
the form around them in `ui-part-forms`.

## 1. Which control

| The choice | Control |
|---|---|
| One of 2 to 6, worth seeing all at once | radio group |
| One of 7 to about 15 known options | custom select (button and listbox, section 7) |
| One of many (people, products, countries), found by typing | combobox with search |
| Any number of a few | checkboxes |
| Any number of many | multi-select combobox with chips, or checkboxes in a searchable list |
| On or off, applied immediately | switch |
| On or off inside a form saved later; an agreement | one checkbox |
| A view mode or a quick filter, 2 to 5 short options | segmented control |
| A visual pick: a plan, a theme, a layout | choice cards, radios underneath |

- In short: radios for one choice from up to five or six, visible at once;
  a custom select for a longer list; a searchable combobox for long
  lists; checkboxes for any number of choices; a switch only for a setting
  that applies immediately.
- A dropdown with two options is a pair of radios or a segmented control. A
  yes or no question that must be answered is two radios, not a checkbox,
  so "not answered" differs from "no".
- A number the user knows (a quantity, a year) is typed, not picked from a
  list of a hundred.

## 2. Anatomy and hit areas

- Each has a label that toggles it when clicked: the input inside its
  `label`, or `for` and `id`. The whole row is the hit area, 44px tall on
  touch (padding on the label), 32 to 36px in dense desktop settings.
- Box and circle 16 to 20px, 8 to 12px from the label's text; the label at
  body size; a description under it, 13 to 14px in the muted colour, tied
  with `aria-describedby`.
- A group has a legend: `fieldset` and `legend` holding the question ("How
  should we deliver it?"), options stacked 8 to 12px apart; side by side
  only for two or three short ones.
- The borders of unchecked boxes and circles reach 3:1 against the
  background: they are how the control is seen.
- Native controls styled first: `accent-color: var(--accent)` colours a
  checked box, circle and range, and `color-scheme` matches them to the
  theme. Build custom ones only for what that cannot do, on the real input
  with `appearance: none`, or with a headless library.

## 3. States

- Checked, unchecked, and indeterminate for a "Select all" when some are
  chosen: `input.indeterminate = true` in script, `aria-checked="mixed"` on
  a custom one.
- Hover: the border one step stronger. Focus-visible: a 2px ring round the
  box, or round the whole card for choice cards.
- Disabled options say why beside them ("Express: not available for this
  address"), or are left out when the user never needs to know.
- Error: on the group, under the legend ("Choose a delivery option"), with
  the message tied to the group and `aria-invalid` on its inputs.
- Options loading (a combobox searching): a "Searching…" row in the list,
  not an empty list.

## 4. Behaviour and keyboard

- The keys for each pattern are in `frontend-accessibility`; prefer a
  headless library (React Aria, Radix, Headless UI, Ark UI, Bits UI, Melt)
  to a hand-built widget.
- Radios (APG radio group): Tab enters the group at the checked one, the
  arrow keys move and select, Tab leaves. Native radios sharing a `name`
  do all of it.
- Checkboxes: Space toggles; each is its own Tab stop.
- Switch: a `button role="switch"` with `aria-checked`, or `<input
  type="checkbox" role="switch">`; Space toggles (Enter too on a button).
  The label names the setting ("Email me when an invoice is paid") and
  does not change with the state. It applies at once, shows that it saved,
  and turns back with a message when saving fails. Never inside a form
  that applies on submit.
- Select: a custom one, not the native `select`, whose open list is drawn
  by the OS and differs on every system and browser. A button showing the
  current value and a chevron opens a listbox under it; section 7 has the
  keyboard, ARIA and code. Use the stack's component when there is one.
  The native `select` stays only where phones are the main audience (their
  own picker is right there), styled closed to match the other fields.
- Combobox (APG combobox with a listbox): Down opens and moves, Up moves,
  Enter picks, Escape closes then clears, typing filters; the input keeps
  focus and `aria-activedescendant` points at the highlighted option.
  Server search after 1 or 2 characters, debounced 150 to 300ms, "No
  results for [query]" when empty, the typed text kept. Libraries: React
  Aria `ComboBox`, Headless UI `Combobox`, Ark UI, Bits UI, Melt,
  Downshift's `useCombobox`; shadcn's combobox is its Popover with Command
  (cmdk).
- Multi-select: the chosen items as removable chips in the field
  (`ui-part-badges`), Backspace removing the last; or checkboxes in a
  popover, with a summary on the trigger ("3 selected").
- Segmented control: a radio group in markup and keys (arrows move and
  select); tabs only when it switches panels of content (`ui-part-tabs`).
  The selected segment gets a filled surface and weight.
- Choice cards: the card is the `label` of a visually hidden radio; the
  checked card gets a 2px accent border and a check icon
  (`:has(:checked)`), the focused one a ring (`:has(:focus-visible)`).

## 5. Defaults and words

- A default when most people choose it and it is safe (standard delivery,
  monthly billing); none when the answer deserves thought; never a
  pre-ticked box for consent or marketing, which is not consent under the
  GDPR.
- Options short, parallel and mutually exclusive, in a meaningful order:
  natural (S, M, L; dates), by frequency, or alphabetical for long lists
  with the likely one first (the user's own country). "Other" with a text
  field, or "None", when the list cannot be complete.
- A select's empty first option says what to do ("Choose a country"); a
  required choice without a default is checked on submit.

## 6. Phones, themes, motion

- Options stack; rows 44px tall; a segmented control fits the width or
  becomes a select; a long list opens as a full-height sheet with the
  search at the top (`ui-part-drawers`).
- Themes: `color-scheme` per theme so native controls follow; unchecked
  borders at 3:1 in both (`ui-themes`).
- Motion: a switch's thumb slides in 160 to 240ms, a check appears at once
  or within 100ms, a segmented indicator slides; none of it under reduced
  motion (`motion-interface`).

## 7. A sketch

```html
<fieldset class="choice-group">
  <legend>How should we deliver it?</legend>
  <label class="choice">
    <input type="radio" name="delivery" value="standard" checked aria-describedby="standard-note">
    <span>Standard delivery</span>
    <small id="standard-note">[Delivery time and price]</small>
  </label>
  <label class="choice">
    <input type="radio" name="delivery" value="express" disabled aria-describedby="express-note">
    <span>Express delivery</span>
    <small id="express-note">Not available for this address</small>
  </label>
</fieldset>
```

```css
.choice-group { display: grid; gap: 8px; margin: 0; padding: 0; border: 0; }
.choice-group legend { margin-block-end: 8px; font-weight: 600; }
.choice {
  display: grid; grid-template-columns: 20px 1fr; column-gap: 12px;
  align-items: center; min-block-size: 44px; cursor: pointer;
}
.choice input { inline-size: 20px; block-size: 20px; margin: 0; accent-color: var(--accent); }
.choice input:focus-visible { outline: 2px solid var(--focus); outline-offset: 2px; }
.choice small { grid-column: 2; font-size: 14px; color: var(--text-muted); }
.choice:has(input:disabled) { cursor: not-allowed; color: var(--text-muted); }
```

## Check it

- Keyboard only: Tab reaches each group once; arrows move through radios
  and segments; Space toggles checkboxes and switches; a combobox opens,
  filters, picks and closes with Escape.
- Click the label text: it toggles. Measure the radio and checkbox rows at
  360px (44px); `preview` lists selects, switches and segment buttons under
  44px, and controls without a name.
- A screen reader reads the legend with each option, the description, and
  the checked, mixed or pressed state.
- Toggle a switch with the network off: it turns back and says why.
- Search the code for `div`s with click handlers or `role="checkbox"`
  where a native input would do.

## Avoid

A dropdown with two options; a switch inside a form that only applies on
submit; a pre-ticked consent box; only the tiny box clickable; checkboxes
built from `div`s; a radio group with no legend; a hand-rolled combobox
without its keyboard pattern; options disabled with no reason; "Select an
option" as the only label; a segmented control used as tabs, or tabs used
as a filter.

## 7. A custom select

Built when the stack has no select component. Same height, border, radius
and padding as the text fields beside it; the open list is a surface one
step up, as wide as the button (or wider for long labels), 8px from it,
with at most about 8 options shown before it scrolls.

```html
<div class="select" data-select>
  <span class="select__label" id="size-label">Size</span>
  <button type="button" class="select__button" aria-haspopup="listbox"
          aria-expanded="false" aria-labelledby="size-label size-value">
    <span id="size-value">Medium</span>
    <svg class="select__chevron" aria-hidden="true" viewBox="0 0 16 16"><path d="M4 6l4 4 4-4" /></svg>
  </button>
  <ul class="select__list" role="listbox" aria-labelledby="size-label" tabindex="-1" hidden>
    <li role="option" id="size-s" aria-selected="false">Small</li>
    <li role="option" id="size-m" aria-selected="true">Medium</li>
    <li role="option" id="size-l" aria-selected="false">Large</li>
  </ul>
</div>
```

```css
.select { position: relative; display: grid; gap: 6px; }
.select__button {
  display: flex; align-items: center; justify-content: space-between; gap: 8px;
  height: var(--control-h, 40px); padding: 0 12px; width: 100%;
  border: 1px solid var(--border); border-radius: var(--radius-sm);
  background: var(--surface); color: var(--text); font: inherit; text-align: left;
}
.select__button:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
.select__chevron { width: 16px; height: 16px; fill: none; stroke: currentColor; stroke-width: 1.5; }
.select__list {
  position: absolute; top: calc(100% + 8px); left: 0; right: 0; z-index: 20;
  max-height: calc(8 * 36px); overflow-y: auto; margin: 0; padding: 4px; list-style: none;
  border: 1px solid var(--border); border-radius: var(--radius-sm);
  background: var(--surface-raised); box-shadow: var(--shadow-sm);
}
.select__list [role="option"] { display: flex; align-items: center; min-height: 36px; padding: 0 8px; border-radius: 4px; cursor: pointer; }
.select__list [role="option"].is-active { background: var(--surface-hover); }
.select__list [aria-selected="true"] { font-weight: 600; }
```

```js
for (const root of document.querySelectorAll("[data-select]")) {
  const button = root.querySelector("button");
  const list = root.querySelector("[role=listbox]");
  const options = [...list.querySelectorAll("[role=option]")];
  const value = root.querySelector("#" + button.getAttribute("aria-labelledby").split(" ")[1]);
  let active = Math.max(0, options.findIndex((o) => o.getAttribute("aria-selected") === "true"));
  const show = (i) => {
    options.forEach((o, k) => o.classList.toggle("is-active", k === i));
    list.setAttribute("aria-activedescendant", options[i].id);
    options[i].scrollIntoView({ block: "nearest" });
    active = i;
  };
  const open = () => { list.hidden = false; button.setAttribute("aria-expanded", "true"); list.focus(); show(active); };
  const close = (focus = true) => { list.hidden = true; button.setAttribute("aria-expanded", "false"); if (focus) button.focus(); };
  const pick = (i) => {
    options.forEach((o, k) => o.setAttribute("aria-selected", String(k === i)));
    value.textContent = options[i].textContent;
    root.dispatchEvent(new CustomEvent("change", { detail: options[i].textContent }));
    close();
  };
  button.addEventListener("click", () => (list.hidden ? open() : close()));
  button.addEventListener("keydown", (e) => { if (["ArrowDown", "ArrowUp", "Enter", " "].includes(e.key)) { e.preventDefault(); open(); } });
  list.addEventListener("keydown", (e) => {
    if (e.key === "ArrowDown") { e.preventDefault(); show(Math.min(active + 1, options.length - 1)); }
    else if (e.key === "ArrowUp") { e.preventDefault(); show(Math.max(active - 1, 0)); }
    else if (e.key === "Home") { e.preventDefault(); show(0); }
    else if (e.key === "End") { e.preventDefault(); show(options.length - 1); }
    else if (e.key === "Enter" || e.key === " ") { e.preventDefault(); pick(active); }
    else if (e.key === "Escape") { e.preventDefault(); close(); }
    else if (e.key === "Tab") { close(false); }
    else if (e.key.length === 1) {
      const i = options.findIndex((o) => o.textContent.trim().toLowerCase().startsWith(e.key.toLowerCase()));
      if (i >= 0) show(i);
    }
  });
  options.forEach((o, i) => { o.addEventListener("click", () => pick(i)); o.addEventListener("mousemove", () => show(i)); });
  document.addEventListener("pointerdown", (e) => { if (!root.contains(e.target) && !list.hidden) close(false); });
}
```

- Keyboard (APG select-only combobox): Down, Up, Enter or Space open it;
  in the list the arrows move, Home and End jump, a letter jumps to the
  first match, Enter or Space picks, Escape closes and returns focus, Tab
  closes and moves on. A click outside closes it.
- The list opens upward when there is no room below it; on a phone it can
  open as a bottom sheet with the same options.
- In a form, a hidden `input` with the field's `name` carries the value, so
  the form submits it like any other field.

