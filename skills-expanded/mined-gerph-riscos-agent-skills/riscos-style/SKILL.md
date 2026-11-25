---
name: riscos-style
description: Apply the official Acorn RISC OS Style Guide when designing, reviewing, or implementing RISC OS desktop applications. Use when Codex must check or propose classic RISC OS behaviour for desktop integration, startup and shutdown, windows, menus, dialogue boxes, icons, colour, sound, keyboard and mouse handling, selection, configuration, internationalisation, or application resource layout.
metadata:
  author: gerph@gerph.org
license: MIT
---
# RISC OS Style

Use this skill to keep a RISC OS application aligned with the official Acorn desktop style.

## Work from the style-guide priorities

- Preserve desktop consistency before novelty.
- Prefer standard operations, menu structures, dialogue patterns, and terminology.
- Protect user data and make destructive actions explicit.
- Respect multi-tasking, user configuration, screen mode changes, palette changes, and filing-system differences.
- Use legal OS interfaces and standard printer, filer, and Wimp behaviour rather than bypassing the system.
- Treat 3D dialogue and window styling as the expected visual direction of the guide.

Treat `must` rules in the references as default requirements. Treat `should` rules as strong conventions unless the user or repository deliberately wants a different policy.

## Use the references selectively

Read only the sections that match the task:

- For overall application design, terminology, and desktop behaviour, read [references/planning.md](references/planning.md).
- For startup, shutdown, editor behaviour, application directories, saved choices, shared resources, or media/network concerns, read [references/application-structure.md](references/application-structure.md).
- For window titles, iconising, closing, scrolling, dragging, or screen takeover, read [references/windows.md](references/windows.md).
- For menu trees, standard menu names, icon bar menus, ellipses, submenu arrows, and Adjust semantics, read [references/menus.md](references/menus.md).
- For persistent or transient dialogue boxes, default actions, wording, control choices, or standard save/print/find dialogues, read [references/dialogue-boxes.md](references/dialogue-boxes.md).
- For caret behaviour, keyboard shortcuts, mouse usage, selection, drag and drop, or clipboard-style operations, read [references/input-selection.md](references/input-selection.md).
- For icon appearance, colour use, sound use, sprite expectations, typography, and visual harmony on the desktop, read [references/visual-design.md](references/visual-design.md).
- For legal implementation techniques, redraw responsiveness, OS-unit measurements, sprite sizes, menu sizing, and dialogue geometry, read [references/implementation.md](references/implementation.md).
- For translated text, character sets, and locale-sensitive formats, read [references/internationalisation.md](references/internationalisation.md).

## Apply the skill

1. Identify which part of the UI or application lifecycle is being designed, reviewed, or implemented.
2. Read only the matching reference files.
3. Extract the hard requirements first, then the preferred conventions.
4. When reviewing code or UX, call out mismatches in terms of user-facing behaviour, not just implementation detail.
5. If the current application intentionally diverges from the Acorn guide, state that the result is a deliberate departure from classic RISC OS style.

## Keep the scope clear

- Use this skill for classic RISC OS desktop style, not for arbitrary modern UI taste.
- Prefer the guide's terminology when wording UI text or review comments.
- Treat the reference files as the authoritative material for this skill; do not assume that any external Acorn style-guide source is available at runtime.
