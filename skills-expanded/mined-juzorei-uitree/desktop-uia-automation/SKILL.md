---
name: desktop-uia-automation
description: Automate Windows desktop applications through the UI Automation tree instead of screenshots — inspect a window's elements, locate controls by AutomationId or name, verify state changes by re-reading the tree. Use whenever the user asks to automate, test, inspect or read a Windows desktop app (buttons, menus, dialogs, forms), says "click this button in app X", "read what the dialog says", "fill this form", "automate this desktop program", mentions pywinauto, UIA, "element tree", or a screenshot-based agent approach is failing on a desktop app. Not for games or apps with custom rendering that expose no UIA tree.
---

# Desktop UIA automation

Screenshot-driven agents guess; the UI Automation tree *knows*. Windows exposes every well-behaved app as a semantic tree — controls with types, names, AutomationIds, enabled states and values — like a DOM for the desktop. Acting on this tree survives theme changes, window moves and DPI differences that break pixel strategies.

Install the CLI (Windows; the `--fixtures` mode works anywhere):

```bash
pip install uitree
```

## 1. Inspect before acting

```bash
uitree windows                          # top-level windows: handle + title
uitree dump "Notepad"                   # full element tree (text view)
uitree dump "Notepad" --json            # machine-readable
uitree find "Notepad" --type Edit       # locate: name / --contains / --type / --automation-id
```

The tree is the ground truth. Read it before clicking anything: which button exists, what its AutomationId is, whether it's enabled. An element that doesn't appear in the tree doesn't exist for the app — a button hidden behind a collapsed menu won't be there until the menu is expanded.

**Match by AutomationId when one exists** (stable across themes and languages), else by exact name, else `--contains`. Coordinates are the last resort, not the first.

## 2. Act through the tree, verify through the tree

`uitree` reads; it doesn't click by design (read-only keeps it safe to run against any window). To act, use the found element's identity with pywinauto from the same tree:

```python
from pywinauto import Desktop
w = Desktop(backend="uia").window(handle=132016)
w.child_window(auto_id="CmdSave", control_type="Button").invoke()   # Invoke pattern
w.child_window(auto_id="15", control_type="Edit").set_edit_text("hello")
```

Then **verify by re-reading the tree**, not by assuming:

```bash
uitree watch "Notepad" --interval 1 --count 10
```

`watch` re-dumps on an interval and reports exactly what appeared, disappeared or changed value — a "Save As" dialog opening shows up as `+ appeared: Dialog "Save As"`, an edited document as `~ value: Edit "Text Editor": '' -> 'hello'`. This is the desktop equivalent of asserting on the DOM instead of a screenshot.

## 3. Dialogs and waiting

A dialog is a *new subtree* (sometimes a new top-level window — check `uitree windows` again). The failure mode is acting on a control before the dialog finishes building; `watch` until the expected element appears, with a deadline:

```bash
uitree find "Save As" --automation-id CmdSave || watch more...
```

Never sleep a fixed number of seconds when you can poll the tree with a deadline — the tree tells you the moment the control is really there.

## 4. When there is no tree

- **Electron apps** (VS Code, Discord): expose a limited Chromium tree; buttons usually visible, rich content may not be. Inspect first, don't assume.
- **Games, custom-rendered apps** (self-drawn UIs): no UIA tree at all — `dump` returns one bare Pane. Say so and switch strategy (accessibility APIs if the app has them, or screenshot tooling); don't invent elements that aren't in the dump.
- **Elevated (admin) windows** can't be read by a non-elevated process — the tree comes back empty or access-denied. Note it instead of retrying.

## 5. Scope

Read-only by contract: this tool reads trees and never injects input, so it's safe to point at any window. Acting on a window is the user's decision — respect applications' terms (don't automate things the vendor forbids) and never sit between a user and their production systems uninvited.
