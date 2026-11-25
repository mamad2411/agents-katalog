---
name: ui-part-page-header
description: "How to build and place the page header inside an application: the title as the screen's h1, the one primary action, secondary actions and the More menu, breadcrumbs, counts and status beside the title, tabs under it, what a detail page's header holds, sticky behaviour, and what happens to all of it on a phone. Read before building or reworking one."
---

# Page header (inside an app)

The generated page header is a card with a big gradient title, a subtitle
that restates the title, and five equal buttons including "Refresh" and
"Export" that nobody asked for, wrapping onto two lines on a laptop and
running off the edge on a phone. Inside an application the page header does
two jobs: it says which screen this is, and it offers the one thing people
come here to do. The principles are in the `ui` skill; where it sits among
the rest, in `ui-layout` section 4.

## 1. Anatomy

```
Orders / #10482                                              breadcrumbs
Order #10482   Overdue · 2 days          [ Refund ] [⋯] [ Send reminder ]
Placed 12 Mar by Rina Pratama                                   one line, optional
Details   Items (3)   Payments   History                         tabs, when the record has them
─────────────────────────────────────────────────────────────────────────
first block of the page
```

- One row: the title (the page's `h1`, 20 to 28px) at the left, the primary
  action at the right, both vertically centred on the row. The action's
  right edge lines up with the right edge of the content below.
- Secondary actions to the left of the primary one, quieter (outline or
  ghost), or in a "More" menu past two (`ui-part-menus`), labelled "More
  actions". Refresh is not an action: data reloads itself after changes.
- Breadcrumbs above the title when the hierarchy is deeper than one level
  (`ui-part-breadcrumbs`).
- A count or status beside the title when it helps ("Products · 214",
  "Overdue · 2 days"), as text in a quieter weight or a status badge that
  says the exception (`ui-part-badges`).
- A description under the title only when a first-time user needs it, one
  line; never a sentence that restates the title.
- Tabs under the header for a record's sub-views, as links with their own
  URLs (`ui-part-tabs`).
- No card, border or background of its own: it sits on the page, 16 to
  24px above the first block.

## 2. The primary action

- One per screen, a filled button with a verb and object ("New order",
  "Send reminder", `ui-part-buttons`); the same place on every list screen.
- On a list screen it creates the object; on a detail screen it is the next
  step for that record (Send, Approve, Publish), which may change with its
  state.
- Destructive actions are never the primary one: they go in the More menu,
  at the end, in the danger colour, with a confirmation
  (`ui-part-dialogs`).
- When a form fills the screen, its Save belongs to the form (or a sticky
  save bar), not the header.

## 3. Detail pages

- The title is the record's name or number, not "Order details".
- Key facts beside or under the title (status, owner, dates) in one line,
  the rest in the page body.
- A back link to the list ("Orders") when there are no breadcrumbs, keeping
  the list's filters in its URL.
- Previous and next record controls only in review workflows.

## 4. Sticky or not

- The page header scrolls away on most screens; the top bar stays
  (`ui-part-header`).
- Long editing screens may keep a compact header (title and primary action)
  sticky under the top bar, with a solid background and a hairline when
  content passes under it.

## 5. On a phone

- The title and the primary action stay on one row (the action as a button
  with its word, shortened if needed: "Add"), or the action moves into the
  top bar; secondary actions go into a menu. Nothing wraps below or runs off
  the edge.
- The title truncates with an ellipsis after one or two lines, the full
  text in the document title.
- Breadcrumbs collapse to a back link to the parent.
- Tabs scroll sideways with the current one in view.

## 6. Accessibility

- The title is the page's only `h1`; the document `<title>` matches it
  ("Order #10482 · Orders · Acme").
- After navigation between screens in a single-page app, focus moves to the
  `h1` (or the main region) and the new title is announced.
- The More menu and icon buttons have names; the status beside the title is
  text, not only colour.

## 7. Themes and motion

Nothing of its own: text tokens and the buttons' own states hold in both
themes (`ui-themes`); no entrance animation on an app's page header
(`motion` dial 1 in tools).

## Check it

- `preview` at 360, 768 and 1440px: the title and the primary action on
  one row, nothing wrapping or overflowing, touch targets 44px.
- The primary action's right edge aligns with the content below on a wide
  screen.
- Tab order: breadcrumbs, title region, secondary actions, More, primary.

## Avoid

A row of five equal buttons; a title that repeats the navigation label with
nothing added; a subtitle under every title; a "Reload" button; a header
boxed in its own card; a gradient or oversized title in a tool; a
destructive action as the primary one; actions that wrap or run off the
edge on a phone; a detail page titled "Details".
