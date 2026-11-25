---
name: canon-menus
description: Use when designing, auditing, or refactoring menus, dropdowns, select menus, combobox, context menus, kebab menus, action menus, or any list of actions triggered by a button. Covers the WAI-ARIA menu pattern, when to use menu vs listbox vs combobox, keyboard behavior, positioning, nesting, and the most common menu-as-navigation anti-pattern. Trigger when the user mentions menu, dropdown, action menu, kebab, overflow menu, select, combobox, or context menu.
---

# CANON · Menus

The word "menu" is overloaded. Pick the right pattern and the accessibility falls into place.

## Menu vs listbox vs combobox vs dropdown-nav

| Pattern | What it is | Use when |
|---|---|---|
| **Menu (actions)** | List of actions | Rename, Delete, Duplicate. Kebab/overflow menus. |
| **Listbox** | List of options | Selecting one or more values. Native `<select>` is the default. |
| **Combobox** | Text input + list | Typing narrows choices (country picker, tag selector) |
| **Navigation dropdown** | Disclosure + links | Site nav with sub-sections |

Using the wrong role breaks screen readers. A menu of links is navigation, not a menu. A list of options to choose from is a listbox, not a menu.

## Actions menu (the common case)

Triggered by a button. Contains items that perform actions. Disappears on select.

```html
<button
  type="button"
  aria-haspopup="menu"
  aria-expanded="false"
  aria-controls="actions-menu"
  id="actions-trigger"
>
  Actions <svg aria-hidden="true">...</svg>
</button>

<div
  role="menu"
  id="actions-menu"
  aria-labelledby="actions-trigger"
  hidden
>
  <button role="menuitem">Edit</button>
  <button role="menuitem">Duplicate</button>
  <hr role="separator" aria-orientation="horizontal">
  <button role="menuitem" class="destructive">Delete</button>
</div>
```

## Required ARIA

| Element | Attribute | Value |
|---|---|---|
| Trigger button | `aria-haspopup` | `"menu"` |
| Trigger button | `aria-expanded` | `"true"` / `"false"` |
| Trigger button | `aria-controls` | id of the menu |
| Menu container | `role` | `"menu"` |
| Menu container | `aria-labelledby` | id of the trigger |
| Menu item | `role` | `"menuitem"`, `"menuitemcheckbox"`, or `"menuitemradio"` |
| Separator | `role` | `"separator"` |

## Keyboard — the WAI-ARIA menu pattern

| Key | Behavior |
|---|---|
| Enter / Space / ArrowDown (on trigger) | Opens menu, focuses first item |
| ArrowUp (on trigger) | Opens menu, focuses last item |
| ArrowDown / ArrowUp (in menu) | Move focus between items, wraps at ends |
| Home / End | First / last item |
| Enter / Space (on item) | Activate item |
| Escape | Close menu, return focus to trigger |
| Tab | Close menu, move focus to next page element |
| Typing a character | Jump to item starting with that letter |

Focus does **not** leave the menu via arrow keys — it cycles.

## Opening and closing

Opens on:
- Click on trigger
- Enter / Space / Arrow keys on focused trigger

Closes on:
- Item selection (usually)
- Click outside
- Escape
- Focus leaves the menu
- A scroll happens in the underlying page (optional; depends on positioning strategy)

Focus returns to the trigger on close — always.

## Positioning

Default: below the trigger, left-aligned with it.

Fallback order if there's no room:
1. Above (right-aligned stays consistent)
2. Right-aligned if overflowing the right edge of viewport
3. Left-aligned if overflowing the left

Offset: 4–8px between trigger and menu.

On mobile with a right-aligned trigger, open to the **left** by default — prevents overflow.

## Width

- **Match trigger width** when the menu is a form control (select-like).
- **Content-based width** for action menus. Min 120px, max 320px.
- Padding: 4–8px vertical, items get 8–12px horizontal padding.

## Menu item structure

```
┌──────────────────────────────────┐
│ [icon]  Item label        ⌘K    │
└──────────────────────────────────┘
```

Optional parts:
- **Leading icon** (16–20px), consistent set across items.
- **Label** (required), sentence case, verb for actions.
- **Trailing shortcut** hint (`⌘K`, 12px, muted).
- **Trailing chevron** only if the item opens a submenu.

Height: 32–40px per item (44px on mobile for hit target).

## Destructive items

- Visually separated from safe items (use a separator or place at the bottom).
- Red text color at high contrast (≥ 4.5:1).
- Label names the verb: "Delete" not "Yes".
- For permanent destruction, follow up with a confirmation (see `canon-modals`).

## Submenus — acceptable with care

One level of nesting is fine. Two levels is almost always a redesign signal.

| Rule | Reason |
|---|---|
| Submenu opens on hover + ArrowRight | Mouse and keyboard parity |
| Submenu closes on hover-leave with 150–300ms grace | Prevents flicker if cursor grazes diagonally |
| ArrowLeft closes submenu, returns focus to parent item | Keyboard back-path |
| Parent item shows a trailing chevron | Visual affordance |

Submenus inside action menus are rare and usually unnecessary. If you have a submenu, question it.

## Checkbox menus and radio menus

For "toggle one of these" or "select one of these" inside a menu, use the correct role:

```html
<button role="menuitemcheckbox" aria-checked="true">Show completed</button>
<button role="menuitemradio" aria-checked="false" name="sort">Name</button>
<button role="menuitemradio" aria-checked="true" name="sort">Date</button>
```

Selection state must be visible — checkmark on the left, or filled dot for radio.

## Search inside menu

If a menu has 10+ items, add a search input at the top. This turns a menu into a command palette, which is fine for power UX.

- Search input focused on open.
- Typing filters items live.
- Arrow keys navigate filtered items.
- Enter activates the focused item.

At this point the pattern is closer to combobox — consider the role change.

## Mobile

- Prefer **bottom sheet** for action menus on mobile. Bigger touch targets, easier to dismiss.
- Or fullscreen sheet for longer menus.
- Hover submenus don't work on touch — flatten the hierarchy.

## Animation

| Phase | Duration | Easing |
|---|---|---|
| Enter | 120–180ms | ease-out |
| Exit | 100–150ms | ease-in |
| Transform | opacity + subtle scale (0.96 → 1) | — |

Faster than modals because menus are lightweight.

## Semantic HTML for the common case

For a list of actions from a button click, use `<button>` + custom popup. For a single-select form value, use **native `<select>`** first:

```html
<label for="country">Country</label>
<select id="country" name="country">
  <option value="us">United States</option>
  <option value="ca">Canada</option>
</select>
```

Native `<select>` is accessible, keyboard-friendly, mobile-native, and free. Reach for a custom listbox only when the native one genuinely fails the need (searchable, multi-select with rich UI, custom option rendering).

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Using `role="menu"` for navigation links | Wrong pattern — screen reader says "menu" but it's nav |
| Custom select instead of native `<select>` | Usually buggier, almost never better |
| Menu items that are `<div>` with onclick | Keyboard-inaccessible |
| Opens on hover only | Broken for keyboard + touch |
| Missing `aria-expanded` on trigger | Screen readers don't know the menu is open |
| No Escape-to-close | Keyboard users trapped |
| Focus not returned to trigger on close | Disorienting |
| Submenu nesting > 2 levels | Information architecture is wrong |
| Destructive action mixed in with safe actions without separator | Misclick risk |
| Mobile hover submenu | Unreachable |
| Menu item label is a noun ("Deletion") | Violates canon-ux-writing — use verbs |

## Decision tree

```
User is picking one value from a list of options?
  ├─ Yes → <select> (default) or combobox if searchable
  └─ No → Continue

User is triggering an action from a list?
  ├─ Yes → Action menu with role="menu"
  └─ No → Continue

It's site navigation?
  ├─ Yes → Disclosure pattern with links, not role="menu"
  └─ No → Reconsider what you're building

Menu has 10+ items?
  └─ Add search input → combobox territory

Mobile?
  └─ Bottom sheet over dropdown
```

## Audit checklist

- [ ] Trigger has `aria-haspopup="menu"`, `aria-expanded`, `aria-controls`
- [ ] Menu has `role="menu"` and `aria-labelledby`
- [ ] Items have `role="menuitem"` (or checkbox/radio variants)
- [ ] Arrow keys cycle within menu
- [ ] Home / End / typing-to-jump work
- [ ] Escape closes, focus returns to trigger
- [ ] Menu items are `<button>` elements, not `<div>`
- [ ] Destructive items separated or styled distinctly
- [ ] Destructive label names the verb
- [ ] Submenus: 1 level max, ArrowRight/Left navigation
- [ ] Mobile hit target ≥ 44px
- [ ] Positioning falls back if clipped
- [ ] Animation honors `prefers-reduced-motion`
- [ ] Native `<select>` used where applicable

## Sources

- WAI-ARIA Authoring Practices · Menu, Menubar, Disclosure, Listbox, Combobox
- WCAG 2.2 · 2.1.1 Keyboard, 2.4.3 Focus Order, 4.1.2 Name, Role, Value
- HTML Living Standard · `<select>`
- Material Design 3 · Menus
- Apple HIG · Popover, Pull-down buttons, Pop-up buttons
