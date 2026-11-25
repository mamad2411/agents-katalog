---
name: ui-part-badges
description: "Badges, tags and chips: status, count, category, removable and toggle chips, one colour per meaning with the word always there, sizes, contrast, how screen readers hear them, and when not to badge at all. Read before adding a badge, a tag, a count or a filter chip."
---

# Badges, tags and chips

The generated version: a green "Active" pill on every row, "New", "AI" and
"Beta" pills with a glowing dot on things that are not new, white text on
a bright yellow fill nobody can read, and one state in three colours on
three screens. A badge is a short label for a state or a category that
changes a decision; this is how to pick the kind, set one style per
meaning, and make it readable and heard. One part of an interface: the
principles (direction, spacing, type, colour, icons, states,
accessibility) are in the `ui` skill, the measures in `ui-layout`.

## 1. The kinds, and when to use each

| Kind | Says | Example | Element |
|---|---|---|---|
| Status | the state of a record | Paid, Overdue, Draft | `span` |
| Count | how many need attention | Inbox 3, 99+ | `span` inside the link or button |
| Tag or label | a category | Design, Bug, Vegetarian | `span`, or `a` when it filters |
| Removable chip | a filter in effect | Paid, with an × | a `button` that removes it |
| Toggle chip | a filter option | Open, Mine, This week | `button` with `aria-pressed` |

- Use them for real status or real categories, in a few colours with text.
- A status says the exception, not the norm (`ui-part-tables`): no badge
  when a product is simply active; "Inactive" or "Low stock · 3 left"
  where it applies. A badge on every row is noise, and the one that
  matters hides among them.
- Not a badge: a sentence ("Your trial ends in 3 days" is a banner,
  `ui-part-notifications`); an action (a status that changes on click is a
  button or a menu trigger that looks like one); decoration.

## 2. Measures

- 20 to 24px tall, 12px text (13px in a spacious layout), weight 500, 4 to
  8px of side padding, `line-height: 1`, `white-space: nowrap`.
- Radius 4 to 6px from the token set; fully round only for count discs, so
  a status never looks like a button.
- An icon or a 6px dot before the word is optional (12 to 14px icon, 4px
  gap); the word is not.
- Counts: `font-variant-numeric: tabular-nums`, a minimum width equal to
  the height so one digit makes a disc, capped at 99+ (9+ on a 16px dot).
- Long tag names truncate at a maximum width (160 to 200px) with the full
  name in a tooltip; a list of tags shows three, then "+N".
- In a table cell or a list row the badge sits on the text's line, never
  stretched to the row's height.

## 3. Colour: one style per meaning

- Five tones at most, as tokens: neutral, info, success, warning, danger.
  Each state of the domain maps to one tone once, in code, and every
  screen uses that map: Paid is the same green in the list, the detail and
  the email.
- Subtle by default: a tinted background (the tone at 10 to 15%) with the
  tone's strong shade as the text, 4.5:1 against the tint. A solid fill
  only for count discs and, at most, the one urgent state.
- Check the fill: white on a mid green, amber or yellow fails 4.5:1; those
  tones take dark text.
- Colour is never the only signal: the word is always there, and an icon
  (a clock for pending, an alert for overdue) helps where tones sit side
  by side.
- Tags whose colours users choose (labels on issues): compute the text
  colour from the background's luminance, dark or light, whichever passes
  4.5:1.
- Categories do not borrow status tones: a "Bug" tag in the danger red
  reads as an error.

## 4. States and behaviour

- Status, count and tag are static text: no hover, no focus, no pointer
  cursor. A tag that filters is a link (`href="?tag=design"`) with the
  link states (`ui-part-links`).
- Removable chip: the whole chip is one `button` with `aria-label="Remove
  filter: Paid"` (the name holds the words it shows) and an × icon
  (`aria-hidden="true"`). After removal, focus moves to the next chip, or
  to the filter button when none is left, never to the top of the page.
  Two or more chips get "Clear all" at the end.
- In a tag input or a multi-select, Backspace in the empty text field
  removes the last chip.
- Toggle chip: a `button` with `aria-pressed="true"` or `"false"`; the
  pressed one gets a check icon and a filled surface, not only a colour
  change. When exactly one may be on, they are radios styled as chips
  (`ui-part-choices`).
- Chips are controls: 32px tall on desktop, 44px tall on touch, 8px
  apart.
- An option with nothing behind it ("This week" with no items) is left out,
  or says why nearby.

## 5. Screen readers

- The badge's text is read where it sits, so write it to make sense
  there: "Invoice 1042, Overdue" reads well; a lone "3" does not.
- Counts carry their meaning: visually hidden text after the number
  ("3 unread"), or on an icon button `aria-label="Notifications, 3
  unread"` with the visible disc `aria-hidden="true"`.
- A dot with no number ("something new") still has words: the button's
  name says "Messages, new".
- A count that changes while the user watches is announced politely
  (`role="status"`), once, when it matters; not on every tick.

## 6. Words

- One or two words, sentence case (not caps with wide tracking), the same
  word for the same state everywhere: "Overdue", not "Late" on the next
  screen.
- "New" only when something is new to this user, and it goes away (once
  they open it, or after 30 days). "Beta" only when the feature is in
  beta, with what that means one click away. "Pro" or a lock says which
  plan unlocks it.
- Counts are real and live. Hide a zero; never show a number nobody
  counted.

## 7. Phones, themes, motion

- Badges do not wrap or shrink; tag lists wrap onto new lines with 6px
  gaps; a row of chips scrolls sideways in its own container, or folds into
  a "Filters" sheet with the active count on its button (`ui-layout` 9).
- Themes: each tone has a tint and a text value per theme; on dark the
  tint is deeper and the text lighter, still 4.5:1 (`ui-themes`).
- Motion: none. A count changes in place: no pulse, no bounce, no glowing
  dot (`motion-interface`).

## 8. A sketch

```ts
// One map, used by every screen, email and export.
export const INVOICE_STATUS = {
  draft: { label: "Draft", tone: "neutral" },
  sent: { label: "Sent", tone: "info" },
  paid: { label: "Paid", tone: "success" },
  due_soon: { label: "Due soon", tone: "warning" },
  overdue: { label: "Overdue", tone: "danger" },
} as const;
```

```css
.badge {
  display: inline-flex; align-items: center; gap: 4px;
  block-size: 22px; padding-inline: 8px;
  font-size: 12px; font-weight: 500; line-height: 1; white-space: nowrap;
  border-radius: var(--radius-sm);
  background: var(--tone-tint); color: var(--tone-text);
}
.badge[data-tone="neutral"] { --tone-tint: var(--surface-2); --tone-text: var(--text-muted); }
.badge[data-tone="success"] { --tone-tint: var(--success-tint); --tone-text: var(--success-text); }
.badge[data-tone="danger"] { --tone-tint: var(--danger-tint); --tone-text: var(--danger-text); }
.count {
  display: inline-grid; place-items: center;
  min-inline-size: 20px; block-size: 20px; padding-inline: 6px;
  border-radius: 999px; font-variant-numeric: tabular-nums;
}
```

```html
<a href="/inbox">Inbox <span class="count">3<span class="visually-hidden"> unread</span></span></a>

<div role="group" aria-label="Filters in effect" class="chips">
  <button type="button" class="chip" aria-label="Remove filter: Paid">
    Paid <svg aria-hidden="true" width="14" height="14"><use href="#icon-x" /></svg>
  </button>
</div>
```

## Check it

- `ui_check` reports glow, default gradients and caps with wide tracking;
  `preview` reports badge text below 4.5:1 in either theme and, at 360px,
  chips under 44px.
- List every place a state appears (list, detail, email, export): one word
  and one tone each.
- Count the badges on a screen: if most rows carry the same one, remove it
  and badge the exceptions.
- Keyboard: Tab to a removable chip, press Enter, and focus lands on the
  next chip; toggle chips are announced as pressed or not pressed.
- A screen reader reads counts with their meaning ("3 unread").

## Avoid

"New", "AI powered", "Beta" with no meaning, a badge on everything; a
green "Active" on every row; glowing or pulsing dots; white text on yellow
or light green; one state in two colours, or two states in one colour;
status tones on categories; caps with wide tracking; badges that look like
buttons, and buttons that look like badges; a "0" count; counts nobody
counted.
