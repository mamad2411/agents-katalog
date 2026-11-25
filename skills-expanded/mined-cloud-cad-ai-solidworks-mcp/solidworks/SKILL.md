---
name: solidworks
description: Drive the open SolidWorks model with named tools. Lengths are meters. Angles are radians. When memory_* tools are listed and this is a new part or assembly, save it, then follow the engineering-memory skill's New project section.
---

The SolidWorks MCP server does the work. This skill has no session state. Read the latest tool result.

When `memory_*` tools are listed and this is a new part or assembly, save it, then follow the engineering-memory skill's New project section.

Prefer a named tool when one matches. Lengths are meters (mm/1000, 800 mm is 0.8; cm/100; m unchanged; in*0.0254; ft*0.3048). Angles are radians. `holes_on_flange` diameter stays in millimeters.

Pack every allowed step whose arguments you can write now into `batch`. `$n` is the handle from step n, including a quoted `$n` inside an invoke arguments JSON array or object. At most 32 steps. Nested `batch` is refused.

Stop the batch before a step whose tool is not allowed, or whose arguments need a returned value that is not a handle. Allowed: `invoke`, `get_property`, `set_property`, `get_object`, `release_object`, `active_document`, `get_enum`, `open_or_activate_document`, `create_sketch`, `add_sketch_entity`, `extrude`, `edge_feature`, `pattern`, `mass_properties`, `save`, `rebuild`, `hole`, `shell`, `dimension`, `relation`, `extract_part_data`, `feature_errors`, `whats_wrong`.

Do not put `CloseDoc` and `NewDocument` in the same steps array. That pair has crashed SolidWorks. `CloseDoc` is the next call after you accept the batch result, so a wrong result still has the document open. `NewDocument` is its own call. `set_units` is its own call. `save_as` is refused inside a batch; `save` takes a full path as a step. One `OpenDoc` per call.

Read the one batch result. Continue from the failing step. A refusal or `confirmation_required` did not run.

To change an existing dimension, feature, mate, or material, call `model`. `change` writes one SolidWorks name (`D1@Sketch1`, or `D1@Sketch1@Bracket-1@Asm` in an assembly) and returns only the read-back. It does not rebuild. Call `check`, `mass_properties`, or `whats_wrong` when the body needs judging. Use `invoke` only to create geometry that has no id yet. `dimension` creates a sketch dimension; `model` changes one that already has a name.

Call `capture_view` once per answer, after a major feature. Quote feature names and mass numbers from the tool result. Do not recap the JSON.

`assembly_parts` and `assembly_structure` return a capped component list (name, path, resolved, quantity). A large `extract_bom` result may be truncated.
