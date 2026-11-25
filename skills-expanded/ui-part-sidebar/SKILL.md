---
name: ui-part-sidebar
description: "How to build an application sidebar and how it changes at each width (full, icon rail, drawer behind a Menu button): what goes in it and in what order, groups and nesting, the current item, item anatomy and measures, the workspace switcher and account block, collapsing, the content anchored beside it, keyboard and screen reader behaviour, and the drawer on phones. Read before building or reworking one."
---

# Sidebar

Generated application shells get the sidebar wrong in the same ways: it stays
open on a phone and squeezes the content to a sliver, every item has a
different coloured icon, the current page is a saturated block, three levels
of nesting hide the daily screens, a user card with an invented name sits at
the top, and the content floats centred in the space that is left. The
principles (direction, spacing, type, colour, icons, states, accessibility)
are in the `ui` skill; the shell it sits in, with its widths and a skeleton,
in `ui-layout` section 5.

## 1. When a sidebar

- For an application with more sections than a top bar holds (more than
  about five), where users move between them all day: admin tools,
  dashboards, editors, internal tools.
- Not for a marketing site, a docs page's own navigation
  (`ui-page-docs` has its tree), or an app with three screens (a top bar or
  a bottom tab bar on phones, `ui-part-navigation`).

## 2. What goes in it, top to bottom

1. The product name or logo (links to the home screen), and a workspace or
   organisation switcher when the product has several (a button opening a
   menu: the current name, its initials avatar, a chevron).
2. Optionally search or a command palette trigger ("Search ⌘K",
   `ui-part-command-palette`) for large apps.
3. The daily places, in the order of use, not alphabetical: Home or
   Overview, then the objects people work on (Orders, Customers,
   Products...).
4. Groups under short headings (12px, muted, sentence case) when there are
   more than about seven items: "Sales", "Catalogue", "Settings".
5. At the bottom: help, settings and the account (the signed-in person's
   real name and avatar, opening a menu with profile, theme and sign out).

At most two levels. A section with children expands in place (a disclosure
with `aria-expanded`); the parent is either a link or a toggle, not both.

## 3. Measures

- 224 to 256px wide, full window height, sticky (`position: sticky; top: 0;
  height: 100dvh`), with its own scroll when the list is long (the account
  block stays pinned at the bottom).
- Each item an icon and a label on one line, 36 to 40px high, 8 to 12px
  horizontal padding, 14px text, the icon 16 to 20px in one set and one
  colour (`currentColor`), 2 to 4px between items, 16 to 24px between
  groups.
- Background one step from the page (a surface token) or the same with a
  1px border; not a dark bar on a light app unless the direction says so.

## 4. The current item and states

- The current item marked with a tinted background or a bar at the start
  and bold or medium weight text, and `aria-current="page"`. A filled,
  saturated block for the current item only when the direction calls for
  it.
- Hover a surface step; focus-visible a 2px ring inside the item.
- Counts beside items only when they are real and actionable ("Inbox 3"),
  announced ("3 unread").
- Items the user cannot access are hidden, not disabled.

## 5. The content beside it

The content beside it starts at its edge plus the page padding (24 to 32px);
it does not float centred in the space that is left (`ui-layout` section
2b). Lists and tables use the full width; forms keep a readable column,
left-aligned.

```css
.shell { display: grid; grid-template-columns: 240px minmax(0, 1fr); min-height: 100dvh; }
.sidebar { position: sticky; top: 0; height: 100dvh; overflow-y: auto; }
.content { min-width: 0; padding: 24px 32px; }
@media (max-width: 1023px) {
  .shell { grid-template-columns: minmax(0, 1fr); }
  .sidebar { display: none; } /* the same navigation opens as a drawer */
}
```

## 6. At each width

| Width | Sidebar |
|---|---|
| 1280px and up | Full, 224 to 256px |
| 1024 to 1279px | Full, or a 64 to 72px rail of icons, each with a tooltip and an accessible name, and a control to expand it |
| Under 1024px | Gone from the page; a sticky top bar with a Menu button opens it as a drawer |

- Collapsing by choice on wide screens: a button at the top or bottom
  ("Collapse sidebar", `aria-expanded`), remembered per user; the rail keeps
  the current item marked and tooltips on hover and focus
  (`ui-part-tooltips`).
- Under 1024px it is gone from the page. A sticky top bar (56px) holds a
  labelled "Menu" button (the icon and the word) that opens the same
  navigation as a drawer from the left: a scrim behind it, focus moved in
  and kept there, `Esc` and a close button, closed after a link is chosen,
  focus back on the button (`ui-part-drawers`). The top bar also holds the
  screen's title and its primary action (`ui-part-page-header`).
- An app used on the phone all day may use a bottom tab bar of 3 to 5
  labelled items instead, with the rest behind "More".

## 7. Markup and accessibility

- A `nav` with `aria-label="Main"` (or "Primary"), a list of links; group
  headings as real headings or `aria-labelledby` on grouped lists.
- The drawer is a dialog (`role="dialog"`, `aria-modal`, labelled), built
  with the component library's sheet or dialog.
- Keyboard: Tab moves through items in order; disclosure groups open with
  Enter or Space; nothing depends on hover.
- The icon-only rail: every link has its label as an accessible name, not
  only a tooltip.

## 8. Themes and motion

A surface token per theme, the current item's tint and the icons visible in
both (`ui-themes`). Collapse and the drawer slide over 240 to 320ms, easing
out, nothing under reduced motion beyond a fade (`motion-interface`).

## Check it

- `preview` at 360, 768 and 1440px: no sidebar beside the content under
  1024px (`preview` reports an open sidebar), no empty band between the
  sidebar and the content on a wide screen (it reports floating content),
  the Menu button labelled.
- Open the drawer from the keyboard, move through it, close it with Escape:
  focus returns to the button.
- A short laptop screen (768px tall): the navigation scrolls and the
  account block does not push items out of reach.

## Avoid

A sidebar that stays open on a phone or tablet and squeezes the content; a
sidebar on a marketing site; every item a different coloured icon; a user
card with an invented name and avatar; nesting three levels; the account
block pushing the navigation off a short screen; a saturated block for the
current item by default; the content centred in the space beside the
sidebar; an icon rail without names; a hamburger icon with no word.
