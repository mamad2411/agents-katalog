---
name: riscos-wimp
description: "Use when writing, reviewing, debugging, or porting RISC OS Wimp code: task initialisation and shutdown, template loading, window creation and opening, icon bar icons, icon state changes, mouse and key handling, menus, help messages, redraw/open/close event flow, or Wimp data structures and SWIs. Also use for module-specific Wimp integration such as Service_StartWimp, Desktop_ commands, or task lifecycle inside a module."
metadata:
  author: gerph@gerph.org
license: MIT
---
# Wimp applications and modules

Use this skill for Wimp-facing code in applications or modules.

# Public references

* Wimp PRM chapter: `http://www.riscos.com/support/developers/prm/wimp.html`
* Use the PRM when the skill needs more detail on a SWI contract, event protocol, or structure field than the local notes provide.

# Core rules

Keep the core Wimp rules straight:

* Respect SWI register contracts exactly. Many bugs come from passing a block where raw registers are required, or vice versa.
* Treat window, icon, and task handles as opaque 32-bit values returned by the Wimp.
* Distinguish Wimp-owned redraw/open protocols from your own UI logic. If the Wimp asks for a redraw or open operation, satisfy that protocol first. If redraw requests appear for windows that should be auto-redraw, treat that as a likely flag, layout, or corruption bug and investigate the cause as well.
* Do not assume template-loaded structures may be rewritten arbitrarily. Preserve the layout the Wimp expects.
* When you need to inspect the contents of a `Templates` file, prefer `riscos-ccres` over `riscos-dump`. Use `riscos-ccres <infile> <outfile>` to decode a Template or Resource file to text, for example `riscos-ccres Templates,fec Templates,txt`. Use `riscos-dump` only when you genuinely need the raw bytes or mixed hex/text view.
* When behaviour differs from an original assembler implementation, compare the event protocol and block layout before changing higher-level logic.
* Treat desktop availability as an environment constraint, not proof that the code is wrong. Some `riscos-build-run` sessions may build and run binaries successfully but still not provide a usable desktop for `Wimp_Initialise`.

# References

Read only the references needed for the task:

* `references/general.md`: general Wimp rules, event-loop invariants, handles, SWI usage.
* `references/initialisation.md`: `Wimp_Initialise`, message lists, task shutdown.
* `references/quit-protocol.md`: `Message_PreQuit`, `Message_Quit`, user prompting, shutdown restart, and the distinction between desktop shutdown and quitting a single task.
* `references/templates.md`: `Wimp_OpenTemplate`, `Wimp_LoadTemplate`, indirected data, writable name buffers.
* `references/windows.md`: `Wimp_CreateWindow`, static window definition layout, and basic open/close helpers.
* `references/redraw.md`: redraw requests, open-window requests, update rectangles, outlines, and redraw forcing.
* `references/icons.md`: icon bar icons, `Wimp_CreateIcon`, icon state changes, priorities and placement.
* `references/palette.md`: Wimp colour numbers, their conventional meanings, and the distinction between logical Wimp colours and the current palette values.
* `references/nested-wimp.md`: nested-window-manager extensions such as child windows, furniture windows, extended `Wimp_OpenWindow`, version 380 initialisation, and related flag changes.
* `references/plugin-protocol.md`: browser plug-in tasks embedded through nested child windows, including `Message_PlugIn_*`, focus transfer, reshape rules, stream messages, and parameter files.
* `references/extedit-protocol.md`: External Edit (`Message_Edit*`) client and editor protocols, including session handles, cursor messages, return/abort flows, and the use of `EditDataSave` with the normal data-transfer protocol.
* `references/taskwindow.md`: TaskWindow child-task protocol, including start-up matching, output handling, cooked versus raw data, and close-down tracking.
* `references/colour-picker.md`: ColourPicker dialogue types, block layout, Wimp message protocol, and menu/submenu integration.
* `references/interactions.md`: mouse clicks and key presses.
* `references/menus.md`: menu creation, opening, warnings, submenu handling, and selection decoding.
* `references/help.md`: `HelpRequest` and `HelpReply` handling.
* `references/user-messages.md`: non-file-transfer Wimp messages such as help replies, filer messages, and `AppControl` construction.
* `references/data-transfer.md`: `DataLoad`, `DataSave`, scrap-file flows, and file-type checks.
* `references/clipboard-protocol.md`: caret and selection ownership, `Message_ClaimEntity`, clipboard `DataRequest` and `DataSave` flow, paste probing, and clipboard-manager handover with `Message_ReleaseEntity`.
* `references/module-integration.md`: module-specific Wimp startup and service interactions. This includes such as `Service_StartWimp`, `Desktop_` commands, or task lifecycle inside a module. This is intentionally separate because it is less common.

# Default workflow

1. Identify whether the code is task-level Wimp code or module-integrated Wimp code.
2. Read `references/general.md` first for protocol constraints.
3. If the task can be quit from the icon bar, Task Manager, or a close-down path, read `references/quit-protocol.md` before changing shutdown handling.
4. If the task is a browser plug-in or another nested child-window client, read `references/nested-wimp.md` and `references/plugin-protocol.md` before changing event handling or open-window logic.
5. If the task implements either side of the External Edit protocol, read `references/extedit-protocol.md` together with `references/user-messages.md` and `references/data-transfer.md` before changing message handling.
6. If the task launches or tracks TaskWindows, read `references/taskwindow.md` before changing helper-task startup, output parsing, or close-down handling.
7. If the task implements cut, copy, paste, clipboard ownership, or selection persistence, read `references/clipboard-protocol.md` together with `references/data-transfer.md` and `references/user-messages.md` before changing message handling.
8. If the task opens or tracks a ColourPicker dialogue, read `references/colour-picker.md` and then the matching menu, help, or user-message reference if needed.
9. Read the one or two other area-specific references that match the task.
10. Validate structure layouts and register usage against the chosen SWIs before editing logic.
11. When diagnosing hangs, inspect the poll loop event sequence before assuming the high-level feature is wrong.
12. If live desktop verification is unavailable, move protocol-sensitive logic into pure helpers where possible and regression-test window geometry, menu selection decoding, clipboard message construction, ColourPicker message handling, and saved-file metadata separately from the live Wimp event loop.

# Review workflow

When reviewing code, check these first:

* wrong signedness or truncation for opaque handles
* block layouts that do not match the active header definitions
* incorrect `Wimp_CreateIcon` or `Wimp_CreateWindow` call conventions
* `Message_PreQuit` handlers that do not distinguish desktop shutdown from "quit just this task"
* tasks that try to ignore `Message_Quit`, or object there instead of during `Message_PreQuit`
* template name buffers passed as read-only strings to `Wimp_LoadTemplate`
* redraw/open/menu protocols being skipped or handled in the wrong order
* transient ColourPicker menu/submenu dialogues being treated like normal windows that must send a close request
* ColourPicker callbacks or generic key handling using the window handle when the dialogue handle is required, or vice versa
* nested-window paths mixing base and extended `Wimp_OpenWindow` or `Wimp_GetWindowState` forms
* plug-in message handlers confusing browser instance handles, plug-in instance handles, stream handles, or task handles
* TaskWindow integrations that do not distinguish clean exit, forced termination, and partial buffered output
* file transfer or clipboard paths that preserve the bytes but lose the intended RISC OS filetype
* application or canvas windows created with a close icon but omitting the back icon (`wimp_WINDOW_BACK_ICON`)
* custom redraw routines using raw VDU 5 bitmap text for desktop UI instead of antialiased fonts (`Wimp_PlotIcon` or `Font_Paint`)
* window work areas, panels, or redraw extents sized too narrowly, causing text to clip or truncate against window borders
