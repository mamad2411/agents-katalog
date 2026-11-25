---
name: ui-anatomy
description: "The contract of each interface component, decided by structure and logic rather than by eye: its parts, variants and when each is used, sizes, every state, keyboard behaviour, content rules and the usual mistakes, for buttons, icon buttons, links, segmented controls, tabs, navigation, breadcrumbs, cards, stats, tables, form fields, selects, checkboxes, radios, switches, badges, alerts, toasts, dialogs, drawers, menus, tooltips, pagination, search, empty states, avatars and the theme toggle. Read before building any of them."
---

# Component anatomy

A component built by eye has whatever parts the moment suggested: a button
with no disabled state, a tab row whose selected tab differs only by a
shade, a toggle with a label in front, a stat with no period. Each
component below is a contract: what it is made of, which variant when,
which sizes, which states it must show, how the keyboard drives it, what
its words must be, and the mistakes to avoid. Build every instance to it.
The `ui-part-*` skills go deeper on each; `ui-structure` says where they go.

Shared rules for every interactive component:
- **States**: default, hover, focus-visible (a 2px ring in the accent with
  offset, never removed), active (pressed), disabled (not just faded: no
  pointer, `aria-disabled` or `disabled`), and where it applies selected,
  loading and error.
- **Sizes** come from one control-height scale: sm 32, md 40 (default),
  lg 48. Touch targets 44px on touch screens (padding may extend it).
- **Names**: every control has an accessible name; an icon-only control
  has `aria-label` (and a `title` tooltip).
- **Colour** never carries meaning alone: selected also has weight, a
  mark, a fill or an underline; an error also has text.

## Button

- **Parts**: label (verb first: "Save changes", "Create invoice"),
  optional leading icon, optional trailing icon for direction or menus.
- **Variants**: *primary* (filled accent; one per screen or per card in a
  set of choices), *secondary* (outline or tinted), *ghost* (text only, for
  low-weight actions in toolbars), *danger* (destructive, always confirmed),
  *link* (inline navigation that looks like a link). Use a link (`<a>`) to
  go somewhere and a button to do something.
- **Sizes**: sm 32 / md 40 / lg 48; horizontal padding about 1.5x the
  font size; a button next to an input shares its height.
- **States**: all shared states plus *loading* (spinner replaces the
  leading icon or sits before the label, width stays the same, disabled
  while loading).
- **Content**: 1 to 3 words; the same action has the same word everywhere;
  no "Click here", no "Submit" when you can say what is submitted.
- **Mistakes**: three primary buttons side by side; buttons of different
  heights in one row; an arrow on every button; a disabled button with no
  reason given nearby.

## Icon button

Square, the control height on each side, one icon at 16 to 20px, a
visible hover surface, `aria-label` and `title`. Used for well-known
actions only (close, menu, more, copy, theme). If people would not know
the icon, use a labelled button.

**Theme toggle** is an icon button: sun or moon, no visible text, its
`aria-label` says what it switches to ("Switch to dark theme"), updated on
each switch, placed in the header's right group.

## Link

Inline in text: underlined or clearly coloured, visited state where it
helps. Standalone: the destination as the words ("Pricing", "View all
invoices"). An external link says so (an icon with a label).

## Segmented control

A small set (2 to 5) of mutually exclusive options that switch a view in
place: a time range, Buy or Sell, List or Grid.

- **Parts**: a track (a filled or outlined container, the control
  height), segments of equal height, the selected segment as a raised or
  filled block with stronger text.
- **States**: selected is unmistakable (filled block plus weight), hover on
  the others, focus-visible on the segment, disabled segments greyed and
  skipped.
- **Keyboard**: a radio group: Tab into the selected one, arrows move and
  select. `role="radiogroup"`/`radio` or native radios.
- **Mistakes**: segments with no track so they read as loose words;
  selected shown by a slightly lighter grey; segments of different widths
  for no reason; used for navigation between pages (that is tabs or
  links).

## Tabs

Switch between views of the same object, content below.

- **Parts**: a tab list on one baseline, tabs with labels (and an optional
  count), an indicator under the selected tab (2px, accent), a divider
  under the list, the panel.
- **States**: selected (indicator plus text colour), hover, focus-visible,
  disabled.
- **Keyboard**: arrows move between tabs, Home/End, Tab enters the panel.
  `role="tablist"`, `tab`, `tabpanel`, `aria-selected`, `aria-controls`.
- **Behaviour**: on a phone, the list scrolls sideways inside itself; the
  page never does. Deep-linkable when a tab is a page section.
- **Mistakes**: tabs used as actions; more than 7 tabs; the selected tab
  differing by colour alone; the tab list wider than the screen with
  nothing to scroll it.

## Navigation

- **Top bar** (3 to 6 destinations): logo left, links centre or left
  after the logo, actions right; the current page marked (weight plus
  indicator, `aria-current="page"`). Below 768: a menu button that opens a
  full-height panel with the same links in the same order.
- **Sidebar** (5 to 9 sections, app screens): sections with icons and
  labels, grouped with small headings, the current item filled, collapsed
  to icons with tooltips on medium widths, a drawer on a phone. Account
  and settings at the bottom.
- **Mistakes**: dead links; a different order on mobile; the current page
  not marked; icon-only navigation without labels.

## Breadcrumbs

The path from a top level to the current page, for hierarchies three or
more deep. Parts: links for each ancestor, a separator (`/` or chevron,
`aria-hidden`), the current page as plain text with `aria-current="page"`,
inside `<nav aria-label="Breadcrumb">`. On a phone show the parent only
("< Projects"). Not on a homepage or a flat site.

## Card

A container for one thing (an item, a summary, a group of related
controls). Parts: optional media, title, supporting text or data, meta,
actions (one primary at most). Padding from the spacing scale (16 to 24),
one radius, either a border or a shadow, not both loud. Cards in one row
share height and inner alignment. A whole card is clickable only if it has
one destination, and then it is one link, not nested buttons.

## Stat (KPI)

Label (what it measures), value (large, tabular figures, unit), change
against a named period with direction ("+12.4% vs last week", coloured
and with an arrow), optional sparkline, optional link to the detail. The
value is the largest text in the card. Without a period, a change means
nothing; without a label, a number means nothing.

## Table

- **Parts**: header row (column labels, sortable ones with a sort
  indicator and `aria-sort`), rows, cells aligned by type (text left,
  numbers right with tabular figures, actions right), optional selection
  column, footer or pagination.
- **States**: row hover, selected, loading (skeleton rows), empty (a
  message in the table's place with an action).
- **Responsive**: below 768, either scroll inside its own container with
  the first column sticky, or become a list of rows with label: value
  pairs. The page never scrolls sideways.
- **Mistakes**: centred numbers; different decimals in one column; ten
  columns where four matter; action buttons in every row instead of a row
  menu.

## Form field

- **Parts**: label (always visible, above the input), the input, optional
  help text below, error text below in the danger colour with an icon,
  optional unit or prefix inside the input ("BTC", "$"), required or
  optional marked (mark the rarer one).
- **Input**: the control height, a placeholder that shows the format
  ("0.00"), never the label. Number inputs show their unit and step;
  amounts allow a "Max" shortcut when there is a ceiling.
- **States**: focus (ring), filled, error (border plus message, set after
  the user leaves the field or submits), disabled, read-only.
- **Behaviour**: validate on blur and submit, not on every keystroke; the
  submit button explains why it is disabled, or stays enabled and shows
  errors on submit.
- **Mistakes**: placeholder as label; error only in red; help text that
  repeats the label.

## Select and combobox

A closed control showing the current value and a chevron; opens a list
with the selected option marked (check) and keyboard support (arrows,
type to jump, Enter, Escape). A custom one (the native select looks
different on every OS) is built to the listbox pattern (`ui-part-choices`).
More than 10 options: a combobox with search.

## Checkbox, radio, switch

- **Checkbox**: independent yes/no choices, or many of a list; label to
  the right, the whole row clickable; indeterminate for "some".
- **Radio**: one of a few (2 to 5) shown all at once; a group label.
- **Switch**: a setting that takes effect immediately (on/off), label on
  the left, state readable without colour ("On"). Not for choices that
  need a Save button: that is a checkbox.

## Badge and tag

A short status or category: 1 to 2 words, small (20 to 24px tall),
semantic colour (neutral, info, success, warning, danger) from tokens,
with text that says the status ("Paid", "Overdue"). Not a button; a
removable tag has its own close button with a label.

## Alert, banner, toast

- **Alert** (inline, in the page): icon, title, text, optional action;
  semantic colour; stays until resolved.
- **Banner** (whole app, top): system-wide state (trial ends, outage);
  dismissible if not critical.
- **Toast** (temporary, corner): confirmation of an action the user took
  ("Invoice sent", with Undo); 4 to 6 seconds, paused on hover; errors that
  need action are not toasts.

## Dialog and drawer

A dialog asks for a decision or a short task: title, content, actions
right (primary last, or first by platform convention; consistent
everywhere), close button, Escape closes, focus moves in and is trapped,
returns to the trigger after. Destructive confirmation names the thing
("Delete 3 invoices?") and the button says the action ("Delete"). A drawer
is for longer tasks beside the page (details, filters).

## Menu (dropdown menu)

A list of actions from a trigger (the "more" icon button, an account
avatar): items with optional icons and shortcuts, groups with dividers,
destructive items last in the danger colour. Keyboard: arrows, Enter,
Escape, type-ahead. Not for navigation of the whole site.

## Tooltip

Short help on hover and focus for an icon button or an abbreviation; never
the only place important information lives; never on a disabled button
that cannot receive focus (put the reason beside it).

## Pagination

Previous and next with labels, page numbers with the current marked, the
total ("1-20 of 312"), page size where people need it. For feeds, "Load
more" or infinite scroll with a stable position.

## Search

An input with a search icon, a placeholder that says what it searches
("Search invoices"), a clear button when filled, `Cmd/Ctrl+K` for a global
one, results as you type for small sets, on Enter for large ones, and a
"no results" state that suggests what to do.

## Empty state

Where content will be: what goes here, why it is empty now, and the one
action that fills it ("No invoices yet. Create your first invoice.").
A simple illustration or icon only if it helps. Different from "no
results" (offer clearing filters) and from an error (offer retry).

## Avatar

A circle or rounded square of a fixed size scale (24, 32, 40), the
person's image or initials on a neutral or derived colour, an `alt` or a
name beside it, a status dot when presence matters.
