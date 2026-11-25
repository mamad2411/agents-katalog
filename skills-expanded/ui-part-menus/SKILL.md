---
name: ui-part-menus
description: "Menus and dropdowns of actions: when to use one and what instead, the trigger and its name, item anatomy and groups, destructive and checkable items, the APG menu button keyboard pattern, placement that stays inside the window, context menus, bottom sheets on phones, and the libraries to use. Read before building a menu, a dropdown or a row's more-actions button."
---

# Menus and dropdowns

The generated version: a three-dot button with no name, opening on hover a
list of links and actions mixed together, clipped by the edge of the
screen, Delete in red at the top beside Edit, and nothing the keyboard can
reach. A menu is a short list of actions on one thing, opened by a button,
driven by the arrow keys, and placed where it fits. The principles are in
the `ui` skill, the measures in `ui-layout`, the motion in
`motion-interface` (section 2).

## 1. When a menu, and when not

- Use one for three or more secondary actions on one object (a row's
  "More actions", a file's options), for an account menu, and for toolbar
  actions that no longer fit.
- Not for:
  - the primary action, or one or two actions: show them as buttons. A
    menu with one item is a button hidden behind a click.
  - a site's navigation: a header dropdown is a disclosure of links, not
    `role="menu"` (`ui-part-navigation`).
  - choosing a value in a form: a select, radio group or combobox
    (`ui-part-choices`).
  - searching many commands: a command palette (`ui-part-command-palette`).
- An app's account menu may mix links (Profile, Settings) with actions
  (Sign out): render the links as menu items that are real `<a>` elements
  (Radix's `asChild`), so they open in a new tab like any link.

## 2. Anatomy and measures

- **Trigger**: a `button` with `aria-haspopup="menu"` and `aria-expanded`.
  Either a visible label with a chevron ("Actions", "Sort: Newest"), or an
  icon button (32 to 36px, 44px on touch) whose `aria-label` names the
  object: "Actions for invoice 0192".
- **Panel**: at least 180px or the trigger's width, at most 320px, 4 to 6px
  of padding, the overlay radius, `--surface` with a 1px border and a soft
  shadow (it sits above the page), 4 to 8px from the trigger.
- **Items**: 32 to 36px tall on desktop, 44px on touch; 8 to 12px of side
  padding; 14px text in sentence case; 16px icons at the start only when
  they speed up scanning, and then on every item of that group; shortcuts
  right-aligned in the muted colour, in `<kbd>`, only when they work; a
  chevron for a submenu.
- **Groups**: a separator (1px, 4px of margin) between groups; a small muted
  group label only when the grouping is not obvious.
- **Order**: the most used first; destructive items last, after a
  separator, in the danger colour, with a confirmation or an undo.
- Items that need more input before they act end with an ellipsis ("Move
  to…", "Delete…"); items that act at once do not.
- **Checkable items**: `menuitemcheckbox` with `aria-checked`, or
  `menuitemradio` in a group, with a check mark. Keep the menu open after
  a checkbox item when people usually toggle several.
- **Length**: the height of the space available with 8px to spare, the list
  scrolling inside; past about ten items, labelled groups, a filter field,
  or a different control.

## 3. States

- **Highlighted item**: a surface step (`--surface-2`), one at a time,
  following the pointer and the keyboard alike.
- **Focus**: the highlighted item holds focus; the trigger shows its ring
  when focus comes back.
- **Open trigger**: `aria-expanded="true"` and a pressed look.
- **Disabled item**: muted, `aria-disabled="true"`, with the reason when it
  is not obvious ("Archive (owners only)"); removed when it never applies
  here.
- **Loading**: the menu opens at once with what is known; an item waiting
  for data shows a small spinner. Never a menu that opens empty.

## 4. Keyboard and ARIA (the APG menu button)

- On the trigger: Enter, Space or Down Arrow opens the menu on the first
  item; Up Arrow opens it on the last.
- In the menu: Down and Up move (wrapping), Home and End jump to the ends,
  typing a letter moves to the next item starting with it, Enter or Space
  activates and closes, Escape closes and returns focus to the trigger, Tab
  closes it and moves on.
- Submenus: Right Arrow opens one on its first item, Left Arrow or Escape
  closes it back to its parent item.
- Markup: `role="menu"` on the list; `menuitem`, `menuitemcheckbox` or
  `menuitemradio` on items; `role="separator"`; `role="group"` with
  `aria-labelledby` for labelled groups; one Tab stop (roving `tabindex`).
- Pointer: a click or tap opens it, never hover alone; a click outside, an
  item chosen or Escape closes it. A submenu may open on hover after 100 to
  150ms, with a safe triangle toward it.
- Use a library that has done this: Radix `DropdownMenu` and `ContextMenu`
  (shadcn/ui), React Aria `MenuTrigger` and `Menu`, Headless UI `Menu`, Ark
  UI `Menu`, Bits UI or Melt UI in Svelte. In plain HTML the Popover API
  (`popover`, `popovertarget`) handles opening, light dismiss and the top
  layer but not the arrow keys: add them, or use Web Awesome's dropdown.
- A confirmation opened from an item is rendered outside the menu and
  opened from state set in the item's `onSelect`, so the menu closes first
  and focus returns to the trigger when the dialog closes.

## 5. Placement

- Below the trigger, aligned to its start edge; to its end edge when the
  trigger sits at the right of a row or a toolbar.
- The menu stays inside the window: it flips above when there is no room
  below, shifts sideways with 8px to spare, and never widens the page.
  Floating UI (`offset`, `flip`, `shift`, `size`, with `autoUpdate`), or
  the library's collision handling (Radix `collisionPadding`, and
  `--radix-dropdown-menu-content-available-height` for the max height).
  CSS anchor positioning (`position-anchor`, `position-try-fallbacks`)
  does the same where supported.
- In the top layer or a portal, so a parent with `overflow: hidden` or a
  table's scroll container cannot clip it; above the sticky header, below
  dialogs.

## 6. Context menus

- A right-click menu (a long press on touch, Shift+F10 or the Menu key from
  the keyboard) is a shortcut, never the only way: each action in it is
  also behind a visible "More actions" button or elsewhere on screen.
- The same items in the same order as the visible menu, so people learn
  one.

## 7. Phones and touch

- A short menu stays anchored to its trigger, with 44px items.
- A long one (more than about six items, or with submenus) opens as a
  bottom sheet (`ui-part-drawers`): the object's name as its title, 48px
  rows, a Cancel button, and submenus as a second screen with Back
  instead of flyouts.
- Nothing on hover only; the trigger is at least 44px.

## 8. Themes and motion

- The panel is one surface step above the page, with a hairline border on
  dark, where a shadow barely shows (`ui-themes`).
- In: a fade with `scale(0.96)` from the trigger's side, 160 to 240ms. Out:
  a fade, 120 to 160ms. The highlight moves instantly. A fade only under
  reduced motion (`motion-interface`, section 2).

## 9. A sketch (shadcn/ui, Radix underneath)

```tsx
const [confirming, setConfirming] = useState(false);

<DropdownMenu>
  <DropdownMenuTrigger asChild>
    <Button variant="ghost" size="icon" aria-label={`Actions for invoice ${invoice.number}`}>
      <DotsVerticalIcon aria-hidden />
    </Button>
  </DropdownMenuTrigger>
  <DropdownMenuContent align="end" collisionPadding={8}>
    <DropdownMenuItem onSelect={() => duplicateInvoice(invoice.id)}>Duplicate</DropdownMenuItem>
    <DropdownMenuItem asChild>
      <a href={`/invoices/${invoice.id}/pdf`}>Download PDF</a>
    </DropdownMenuItem>
    <DropdownMenuSeparator />
    <DropdownMenuItem className="text-destructive" onSelect={() => setConfirming(true)}>
      Delete…
    </DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>
<ConfirmDeleteDialog open={confirming} onOpenChange={setConfirming} invoice={invoice} />
```

## Check it

- Keyboard only: Tab to the trigger; Enter opens on the first item; the
  arrows, Home, End and a letter move; Escape closes with focus back on the
  trigger; Tab leaves.
- A screen reader announces the trigger's name and "menu button,
  collapsed", then the menu and each item's name and state.
- Open every menu at 360px near the right and bottom edges: it flips or
  shifts, nothing is clipped, the page never widens.
- `preview`: "controls without a name" catches unnamed icon triggers,
  "touch targets under 44px" small ones on phones. `ui_check`:
  `empty-handler` finds items that do nothing.

## Avoid

Menus that open on hover only; a menu with one item; a three-dot trigger
with no name; Delete first, or beside Edit without a separator;
destructive items that act without a confirmation or an undo;
`role="menu"` on site navigation; a menu clipped by a scroll container or
the window; icons on some items and not others; shortcuts that do not
work; a hand-built menu with no arrow keys; a context menu as the only way
to an action.
