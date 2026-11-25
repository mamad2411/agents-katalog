---
name: skiff-keys
description: Skiff's keyboard shortcuts, kept in step across the keymap, the F1 sheet, the menu bar, the palette and the wiki. Use when you add, change, remove or rebind a key or a key-driven behavior in apps/desktop/src (keys.ts, keyboard.ts, actions.ts, commands.ts, infoDialogs.ts, menus, settings, modes), or when you review such a change.
---

# Skiff keys

Read the `skiff-design` skill first. Its interaction rules apply: Ctrl+Shift for the app, keys act on what is highlighted, keyboard and mouse call the same code.

## One source

`apps/desktop/src/app/keys.ts` is the keymap. Everything else reads from it.

| What | Where | Reads |
| --- | --- | --- |
| Action names and default keys | `keys.ts`: `Action`, `DEFAULTS` | — |
| User overrides | `[keys]` in `projects.toml` → `setKeymap()` | `DEFAULTS` |
| What each action does | `keys.ts`: `DESCRIBE` (section); `i18n/en.ts`: `key.<action>` (words) | — |
| What an action runs | `app/actions.ts`: `runAction()` | — |
| F1 sheet | `ui/infoDialogs.ts`: `showShortcuts()` | `DESCRIBE` + `FIXED_SHORTCUTS` |
| Menu bar and palette | `app/commands.ts` | `keyLabel()`, `menuAccel()` |
| Menu hint keys | `ui/menu.ts`: `hintKey()` | `eventLabel()` |
| Global dispatch | `app/keyboard.ts`: window keydown | `actionFor()` |

Keys that are not actions live where they are handled. Their F1 rows are in `FIXED_SHORTCUTS`:

- List keys (Enter, Space, arrows, F2, Delete, Menu): the `$("sidebar-scroll")` handler in `keyboard.ts`.
- Ctrl+Shift+1…9: `projectKey()` in `keyboard.ts`.
- Menus, palette, find bar, start-session menu, empty pane: their own files.

Screens that hold the keys reuse action keys with a local meaning. Settings (`appearance/settings.ts`) is one: `modalOpen()` stops global dispatch, and the screen reads `actionFor(e)` itself. Up/Down step sections. Left goes to the tabs. Right goes into the section. Focus mode and maximize (`app/modes.ts`) also give Up/Down a local meaning. Mission control (`workspace/missionControl.ts`) holds the keys as a dialog does. `runAction()` drops every action but these: its own key (close), maximize (the lit session), the palette key (search the board), the focus mode key (Running / All), the list keys (step the screens), Next waiting, Settings, the Skiff agent's key and quit. The board's `onKey()` reads plain arrows, Enter and Esc itself, and the same action keys, so they work on the board and in its search.

## Rules

- Never hardcode a key label in UI text. Use `keyLabel(action)`. A key in a note, such as "Ctrl+Shift+Up/Down" in a `key.*` line, is the only exception. Check those notes when a default changes.
- A local handler matches action keys with `actionFor(e)`, not raw `e.key` checks. Then `[keys]` overrides work there too.
- An action with a menu bar item (`commands.ts`) has a native accelerator. The menu takes that key before the page sees a keydown, and calls `runAction()`. A screen that gives such a key a local meaning must also catch it in `runAction()`, as Settings does with `settings.runKey()`.
- A new action needs all of these: an `Action` member, a `DEFAULTS` key, a `DESCRIBE` row, a `key.<action>` line in `i18n/en.ts`, a `runAction()` case, and a `commands.ts` entry where a menu item fits. The typecheck fails while the `key.<action>` line is missing.
- A new fixed key needs a `FIXED_SHORTCUTS` row in the right section, and its `fixed.*` line in `i18n/en.ts`.
- A local meaning for an action key goes at the end of its `key.<action>` line: "In Settings, the next section".
- Before you take a key, check `DEFAULTS` for a clash. Check that the terminal does not need it (bare Ctrl), and that GNOME, KDE or macOS do not take it.
- The `key.*` and `fixed.*` lines are user copy. Follow the Words rules in `skiff-design`.

## Wiki

F1 is the full list. It reads the live keymap, so it is never out of date. The wiki does not copy it.

- [Design](https://github.com/solutionscay/skiff/wiki/Design) holds the rules: Ctrl+Shift for the app, keys act on the highlighted target, `[keys]` and F1.
- [Glossary](https://github.com/solutionscay/skiff/wiki/Glossary), section "The current keybinding scheme", holds the navigation model only: Ctrl+Shift+Up/Down, Ctrl+Shift+Left/Right, Ctrl+Shift+Home, F6, F1, Ctrl+Shift+P, Ctrl+Shift+M, Ctrl+Shift+A, Ctrl+Shift+Alt+Arrow. Each line names its action id. It sends the reader to F1 for the rest.
- [Mission control](https://github.com/solutionscay/skiff/wiki/Mission-control) lists the board's keys: Ctrl+Shift+A opens and closes it; in it, arrows move between cards, Enter goes to the session, Esc closes, Ctrl+Shift+E switches Running / All, Ctrl+Shift+P searches. Update it when a key in `onKey()` or the mission branch of `runAction()` changes.

Update the wiki only when one of those keys or rules changes. The wiki is a separate repo: `git clone https://github.com/solutionscay/skiff.wiki.git`. Ask the operator before you push it.

## Before you finish

- `npx tsc --noEmit -p apps/desktop` passes.
- `DEFAULTS`, `DESCRIBE`, `runAction()` and `commands.ts` agree on the action.
- F1 shows the change in the right section.
- If you changed a navigation key or a rule, the wiki says so.
