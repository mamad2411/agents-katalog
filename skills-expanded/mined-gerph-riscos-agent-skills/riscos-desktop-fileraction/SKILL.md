---
name: riscos-desktop-fileraction
description: Start interactive RISC OS Filer operations through the FilerSWIs/FilerAction module by sending the `FilerAction_SendSelectedDirectory`, `FilerAction_SendSelectedFile`, and `FilerAction_SendStartOperation` SWIs in the correct order. Use this skill when Codex needs to launch desktop copy, move, delete, access, set type, count, stamp, copy-local, or find operations via the Filer action window rather than performing filesystem changes directly.
metadata:
  author: gerph@gerph.org
license: MIT
---
# riscos-desktop-fileraction

Use the FilerAction SWIs to ask the desktop Filer to perform an interactive operation. This is for starting a Filer action window, not for silent filesystem updates.

## Workflow

1. Ensure the destination task is the Filer action task, typically after `*WimpTask Filer_Action`.
2. Call `FilerAction_SendSelectedDirectory` first.
   Pass `R0 = task handle`, `R1 -> nul-terminated source directory name`.
3. Call `FilerAction_SendSelectedFile` once for each selected object.
   Pass `R0 = task handle`, `R1 -> nul-terminated leaf name`.
4. Call `FilerAction_SendStartOperation` last.
   Pass `R0 = task handle`, `R1 = operation`, `R2 = option flags`, `R3 -> auxiliary data`, `R4 = auxiliary data length`.

Do not call `SendStartOperation` before the directory and file selections have been sent. The module buffers file names and flushes that buffer when the operation starts.

## Operations

Use these `R1` operation values for `FilerAction_SendStartOperation`:

* `0` copy
* `1` move (rename)
* `2` delete
* `3` set access
* `4` set type
* `5` count
* `6` move by copy-and-delete
* `7` copy local within directory
* `8` stamp
* `9` find

## Option bits

Set `R2` with any combination of:

* bit 0: verbose
* bit 1: confirm
* bit 2: force
* bit 3: newer
* bit 4: recurse

The original documentation lists only bits 0-4. Some headers define later flags for newer systems, but use them only if the target environment is known to support them.

## Auxiliary data by operation

For `R3` and `R4`:

* copy, move, move-by-copy-and-delete: `R3 -> nul-terminated destination directory`, `R4 = strlen(R3) + 1`
* delete: `R3` unused, `R4 = 0`
* set access: `R3 -> word containing the access specification`, `R4 = sizeof(int)`
* set type: `R3 -> word containing the file type in bits 0-11`, `R4 = sizeof(int)`
* count: `R3` unused, `R4 = 0`
* copy local: `R3 -> nul-terminated destination leaf name`, `R4 = strlen(R3) + 1`
* stamp: `R3` unused, `R4 = 0`
* find: `R3 -> nul-terminated object name to find`, `R4 = strlen(R3) + 1`

## String handling

Treat the SWI string inputs as control-terminated RISC OS strings:

* `SendSelectedDirectory` stops at space or any control character, so pass a clean directory path with no trailing parameters.
* `SendSelectedFile` accumulates leaf names separated by spaces.
* Directory and leaf names should be provided separately; do not send full paths through `SendSelectedFile`.

## Behavioural notes

* The module sends Wimp user messages `Message_FilerSelectionDirectory`, `Message_FilerAddSelection`, and `Message_FilerAction`.
* The file-selection buffer is limited to 256 bytes in the original implementation. Large selections may be split across multiple `Message_FilerAddSelection` messages automatically.
* `Service_WimpCloseDown` clears any buffered selection state. Do not assume partial state survives task shutdown.
* Use this skill when the user wants the interactive desktop experience. If they want direct non-interactive filesystem work, use normal filesystem interfaces instead.

## Implementation guidance

When writing code that uses these SWIs:

* keep the task handle explicit and thread it through all three calls
* build typed helper functions for each SWI rather than passing raw register blocks through the whole codebase
* preserve the exact ordering of calls
* compute `R4` from the actual auxiliary payload length, including the terminating nul for strings
