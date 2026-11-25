---
name: using-libtoolbox
description: Use the installed Toolbox veneer headers and the public Toolbox manual to create, inspect, and understand RISC OS Toolbox applications, windows, menus, dialogues, and gadget extensions. Use when code includes headers from `/riscos-resources/Export/Lib/tboxlibs/h/`, when a task needs Toolbox object methods/events/types, or when an agent must choose the right calls for SaveAs, Window, Menu, Iconbar, or Toolbox gadget work.
metadata:
  author: Gerph
license: MIT
---
# using-libtoolbox

Use this skill when working with the installed Toolbox veneer headers and related Toolbox object modules.

Primary locations:

- Installed veneers: `/riscos-resources/Export/Lib/tboxlibs/h/`
- Core Toolbox header: `/riscos-resources/Export/Export/Lib/tboxlibs/h/toolbox`
- Public behavioural manual: `http://www.riscos.com/support/developers/toolbox/index.html`

## Workflow

1. Read [references/overview.md](references/overview.md).
2. Read [references/core-toolbox.md](references/core-toolbox.md) if the task involves application startup, object lifecycle, event flow, resource files, or generic Toolbox SWIs.
3. Read [references/simple-application.md](references/simple-application.md) if the task is a small Toolbox application or iconbar utility and you need an end-to-end structure to follow.
4. Read [references/application-structure.md](references/application-structure.md) if the task needs generic Toolbox application wiring such as object creation, event registration, iconbar/menu linkage, background null-event work, or runtime state updates.
5. Read [references/header-map.md](references/header-map.md) and then load only the per-header reference files that match the object classes, gadgets, or support headers used by the task.
6. If the task is about standard dialogues, iconbar objects, or menus, read [references/dialogues-and-menus.md](references/dialogues-and-menus.md).
7. If the task is about windows, toolbars, redraw, or gadget composition, read [references/windows-and-gadgets.md](references/windows-and-gadgets.md).
8. If the task uses non-core gadget or object modules such as `textarea`, `scrolllist`, `imagefilegadget`, `ToolAction`, or `optionswindow`, read [references/extensions.md](references/extensions.md) and then the specific generated header reference in `references/`.

## Rules

- Treat the installed headers as the concrete API reference for function names, types, constants, method numbers, and event structures.
- Treat the RISCOS.com Toolbox manual as the behavioural reference for how the standard Toolbox classes are intended to be used.
- Prefer object-level Toolbox methods and events over raw Wimp manipulation unless the code clearly needs the bridge points exposed by `window`, `gadgets`, or `wimp`.
- When reading existing code, expect a mixture of Toolbox and Wimp APIs. Confirm whether the code is operating on a Toolbox `ObjectId` or a raw Wimp handle before proposing changes.
- For SaveAs work, pay attention to the Toolbox-managed save protocol rather than assuming the application handles raw Wimp data-transfer messages itself.
- For composite gadgets such as `NumberRange` and `StringSet`, prefer the family API before reaching into child components.
- For extension headers that are not part of the classic Toolbox chapters, rely on the generated per-header references first; they are the primary source in this skill for those modules.

## Generated References

The per-header Markdown files in `references/` are generated from the installed headers by:

- `scripts/generate_header_refs.py`

Re-run that script if the installed header set changes and the per-header references need to be refreshed.
