---
name: kicad-agent
description: Inspect and modify KiCad schematics and PCB layouts, run ERC/DRC, and prepare traceable fabrication exports using the installed version's CLI or documented APIs. Use for board edits, library and footprint issues, stale checks after edits, copper-zone refill, Gerber/drill/BOM exports, and saved-state verification.
---

# KiCad Agent

Keep the edited board, its checks, and its exports on the same revision.

## Inspect the project and tools

Identify the schematic, PCB, project settings, library references and desired change. Confirm electrical requirements, board dimensions, layer stack, clearances, current paths and manufacturing constraints where they affect the task. Use a copy or a tracked project revision for edits.

Check the KiCad version and available CLI, IPC, or Python interface. Read matching official help and the exact tool schema before making calls. CLI export/checking, a running editor's IPC API, and legacy Python bindings are different access routes with different capabilities. Do not assume that a connected MCP server exposes every KiCad operation.

Use [references/automation.md](references/automation.md) for route selection. A command-line export route does not imply a headless schematic or PCB editing API.

## Make the intended change

Inspect affected symbols, footprints, pin-to-pad mapping, net connectivity and design rules before editing. Preserve UUIDs, references, net names and unrelated geometry when updating a project. Avoid blind string replacements in structured KiCad files.

Use documented editor/API operations where supported. If file-level changes are necessary, use a format-aware method and verify that the native application can reopen the project. Do not claim native round-trip validation when it was not run.

## Check the actual saved state

After changes affecting copper, recompute zone fills through an available documented operation and wait for completion. Save the affected project/board and wait for acknowledgement. Confirm the file used for checking is that saved revision. Run these dependent operations sequentially; do not batch save and DRC as independent calls.

Run applicable schematic ERC and PCB DRC with the installed version's documented options. Retain the full reports and identify intentional exclusions. Do not change rules, exclude violations or suppress warnings merely to produce a clean report.

Use [references/validation.md](references/validation.md) to interpret the result. If refill or save confirmation is unavailable, state that the DRC evidence is incomplete and give the exact missing native step. Never call a stale report clean evidence for the new board.

## Export a reviewable package

Export Gerber, drill, placement and BOM files as requested from the checked revision into a new output directory. Record the source revision/hash, KiCad version, export options and report paths. Any later design change invalidates that association until checks and exports are repeated.

Inspect requested layers, board outline, holes, origin, rotation and top/bottom conventions. For assembly outputs, distinguish BOM references, quantities, DNP components, part numbers and placement files. Do not upload or order boards unless that action is within the user's authorization.

Deliver editable sources, requested exports, native reports and the unresolved findings. A DRC pass does not prove electrical function, EMC performance or manufacturing success. If KiCad cannot run here, label generated instructions or files as unexecuted and state the checks still needed.

See [references/example.md](references/example.md) for an edit-to-export task.
