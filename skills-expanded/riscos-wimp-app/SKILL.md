---
name: riscos-wimp-app
description: Structure and package small RISC OS desktop Wimp applications, especially iconbar applications, without duplicating the raw Wimp protocol guidance from the riscos-wimp skill. Use when creating or restructuring a desktop application with Wimp startup, poll-loop dispatch, iconbar icons, packaged Resources files, or application naming changes.
license: MIT
---
# riscos-wimp-app

Use this skill when creating or restructuring a RISC OS desktop application.
Use `riscos-wimp` as well for the underlying Wimp protocol, SWI contracts,
event block layouts, and generic icon rules.
Use `riscos-wimp-templates` as well when the application needs to create or
revise `Templates,fec` content such as the baseline proginfo window.

## Read these references

Choose only the references needed for the task:

* `references/application-structure.md`: startup, shutdown, SWI-wrapper, and event-dispatch structure
* `references/baseline-iconbar-application.md`: the default behaviour and packaging for a new iconbar-based application
* `references/iconbar-icon-creation.md`: concrete application defaults for iconbar icons
* `references/naming-and-package-structure.md`: package naming, `!Run`/`!Boot`, and related application-structure updates
* `references/timed-events-with-pollidle.md`: regular timed callbacks driven from the main Wimp poll loop

For raw Wimp behaviour, also read the relevant `riscos-wimp` references rather
than duplicating them here. In particular:

* `riscos-wimp/references/icons.md`
* `riscos-wimp/references/interactions.md`
* `riscos-wimp/references/initialisation.md`

## Default workflow

1. Confirm whether the task is an ordinary desktop application, a module task, or another Wimp-integrated form.
2. Read `references/application-structure.md` first.
3. If the user is asking for a new ordinary iconbar application, also read `references/baseline-iconbar-application.md` unless they explicitly want a different shape.
4. If the application uses an iconbar icon, read `references/iconbar-icon-creation.md` and the matching `riscos-wimp` icon references.
5. If the application needs regular background work such as animation, status refresh, or network polling, read `references/timed-events-with-pollidle.md` before editing the poll loop.
6. If the application name or package layout is being changed, read `references/naming-and-package-structure.md` before editing.
7. Keep the application split into plumbing, business logic, and narrow SWI wrappers.
8. For packaged applications, check the built absolute size and keep `Resources/!Run` slot settings in sync with it, rounded to whole 4K pages with a minimum of 24K and at least 32K headroom over the built absolute.
9. Verify install-oriented applications with `riscos-amu install INSTDIR=install`.

## Review checklist

When reviewing a desktop application structure, check these first:

* iconbar icons using the wrong side or wrong text/sprite form for the intended application type
* iconbar bounding boxes using unsuitable vertical co-ordinates
* click handlers that do not filter by both source window and source icon
* button decoding that mixes up button-event values with generic bitfield masks
* timed background work implemented as busy polling instead of scheduling the next idle wake-up
* timeout callbacks doing too much work or calling blocking operations inside the poll loop
* `Resources/!Run` slot sizes left at skeleton defaults, not rounded to whole 4K pages, or left below the 24K minimum
* application renames that updated `COMPONENT` but missed `!Run`, `VersionNum`, help/messages, or task-name strings
* SWI calls leaking directly into business logic instead of being isolated behind helpers
* proginfo windows created from templates but not given open-window handling, so they cannot be moved correctly
* window work areas, side panels, status bars, or proginfo templates sized too narrowly for their contained text, causing text clipping or truncation against borders (ensure width >= max_text_width + margins)
* application main windows or canvas windows created with a close icon but missing the back icon (`wimp_WINDOW_BACK_ICON`)
* application windows using raw VDU 5 bitmap text for desktop UI or data display instead of the antialiased font system (`Wimp_PlotIcon` or Font Manager `Homerton.Medium`/`Corpus.Medium`)
