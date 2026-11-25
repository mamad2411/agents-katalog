---
name: using-libriscoslib
description: Use the RISC_OSLib library from C-based RISC OS projects, including choosing the correct header include path and linking the exported library object in `Makefile,fe1`. Use when a task adds or reviews `#include "RISC_OSLib/..."` headers, `wimp_*`/other RISC_OSLib APIs, or `LIBS` entries for desktop applications and other RISC_OSLib-based code.
metadata:
  author: gerph@gerph.org
license: MIT
---
# Using the library RISC_OSLib

Use this skill when a C project depends on the `RISC_OSLib` library.

## Default workflow

1. Confirm that the project is a C-based RISC OS component using `RISC_OSLib` APIs such as `wimp_*`.
2. Read the relevant resource notes for the headers you are about to touch:
   * `resources/overview.md` for the header map and major caveats
   * `resources/wimp-ui.md` for Wimp, template, menu, dialogue, help, and transfer helpers
   * `resources/text-editing.md` for `txt*` and `txtedit*`
   * `resources/system-graphics.md` for OS, resources, fonts, sprites, Draw, printing, memory helpers, and utility wrappers
3. Include headers with the exported include form `#include "RISC_OSLib/<header>.h"`.
4. Ensure the makefile can resolve those headers through `INCLUDES`, which is normally `-IC:` by default in the standard project templates.
5. Link the exported library object explicitly in `Makefile,fe1` through `LIBS`.
6. For simple Wimp tasks, prefer the `wimpt_*` helper layer from `RISC_OSLib` rather than dropping straight to the lower-level `wimp_taskinit` path.
7. Rebuild after any header or link change to catch unresolved symbols immediately.

## Include guidance

Use the exported include path form:

* `#include "RISC_OSLib/wimp.h"`
* `#include "RISC_OSLib/wimpt.h"`
* `#include "RISC_OSLib/os.h"`

Do not include headers by their host filesystem paths.

When using `RISC_OSLib/template.h`, include `RISC_OSLib/wimp.h` first, because
the template header relies on `wimp_wind` already being defined.

## Makefile linkage

When a project uses `RISC_OSLib`, add the library to `LIBS` in
`Makefile,fe1` using the exported object name:

    LIBS       = C:RISC_OSLib.o.risc_oslib

For 32-bit application builds this resolves to the correct `-32` variant
through the build system. If other libraries are already present, append
`C:RISC_OSLib.o.risc_oslib` to the existing `LIBS` list rather than replacing
them.

## Wimp task startup through `RISC_OSLib`

For small desktop applications using `RISC_OSLib`, the practical startup path
is usually:

1. call `wimpt_wimpversion(<minimum_version>)`
2. register the required message list with `wimpt_messages(...)`
3. call `wimpt_init(<task_name>)`
4. read back the task handle with `wimpt_task()`
5. enter the event loop with `wimpt_poll(...)`

This keeps startup and polling aligned with the `RISC_OSLib` helper layer.

When using `wimpt_messages`, terminate the `wimp_msgaction` array with
`wimp_MCLOSEDOWN`, as documented by the `RISC_OSLib` header.
Do not assume that an unterminated list is acceptable just because the first
few entries appear to work.

`wimpt_init` returns the actual Wimp version. Check it against the minimum
version you requested before continuing into application setup.

## Template loading

`RISC_OSLib` exposes both:

* the higher-level `template.h` helper layer
* the lower-level `wimp_open_template`, `wimp_load_template`, and
  `wimp_close_template` calls from `wimp.h`

Be careful with the higher-level helper layer. The `template.h` comments
document an assumption that the template file is called `Templates` in the
application directory. If the real packaged path or lookup context matters,
prefer the explicit `wimp_open_template("<App$Dir>.Templates")` path instead
of assuming the helper's default lookup will resolve correctly.

For explicit template loading through `wimp.h`, a practical pattern is:

1. call `wimp_open_template(...)` with the full application-relative path
2. call `wimp_load_template(...)` once with `buf <= 0` to obtain the required
   template-buffer and indirected-workspace sizes
3. allocate persistent storage for both the template buffer and the indirected
   workspace
4. call `wimp_load_template(...)` again with the allocated pointers
5. call `wimp_close_template()` even on failure paths

Keep the template buffer and indirected workspace alive for as long as the
created window exists. Do not free or overwrite them immediately after
`wimp_create_wind()`.

If the template name is being matched by name, use a writable aligned name
buffer rather than a string literal.

## Structure-field usage

`RISC_OSLib` gives you C structures for Wimp objects, but many UI details are
still configured through explicit packed fields rather than high-level helper
functions.

In particular:

* menu title and work-area colours are set through the menu header fields such
  as `tit_fcol`, `tit_bcol`, `work_fcol`, and `work_bcol`
* menu item foreground and background colours come from the item's
  `iconflags`, not the menu header colours
* icon button types are encoded into the icon flags, for example with
  `(wimp_BCLICKDEBOUNCE << 12)`
* submenu dialogue windows are attached through the menu item's `submenu`
  field even though the field type is expressed as `wimp_menuptr`

Do not assume that a `RISC_OSLib` menu API will derive those values for you.
When a menu or icon renders or behaves incorrectly, inspect the populated
structure fields and packed flag values directly.

For Wimp colour numbers used through `RISC_OSLib` structures, remember that
the logical Wimp palette maps `0` to white and `7` to black.

## Open-window protocol

Even when a window came from a template or is only used as a menu submenu,
normal Wimp open-window handling still applies.

If the task receives `wimp_EOPEN`, pass the returned `wimp_openstr` back to
`wimp_open_wind()` promptly. If you omit that handler, otherwise moveable
windows will not behave correctly when the user drags or reopens them.

## Practical checks

When reviewing or repairing a `RISC_OSLib` project, check these first:

* headers included as host paths instead of `RISC_OSLib/...`
* calls to `wimp_*` or other `RISC_OSLib` APIs with no matching `LIBS` entry
* abstract or guessed library names such as `libRISC_OSLib` instead of the
  exported object `C:RISC_OSLib.o.risc_oslib`
* application skeletons that compile but fail to link because the library was
  never added
* `wimpt_messages` lists that are not terminated with `wimp_MCLOSEDOWN`
* applications using `wimpt_init` but never checking the returned Wimp version
* code including `template.h` before `wimp.h`
* template-loading code that relies on the `template.h` default `Templates`
  lookup when an explicit application-relative path is safer
* template buffers or indirected workspaces that are stack-allocated or freed
  too early
* menu or icon code that changes the wrong colour fields because it confuses
  menu-header colours with item `iconflags`
* moveable windows or menu subwindows that never handle `wimp_EOPEN`

## Related skills

Use `writing-c` for general C style and structure.
Use `riscos-wimp` or `riscos-wimp-app` when the `RISC_OSLib` usage is
specifically for desktop Wimp applications.

## Resource notes

The `resources/` directory in this skill contains source-backed notes on the
public `RISC_OSLib` headers and the behaviour that is easy to miss from the
header comments alone. Use those notes instead of relying on the local
implementation sources being available to the next agent.
