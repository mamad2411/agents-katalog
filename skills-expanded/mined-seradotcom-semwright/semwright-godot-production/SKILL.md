---
name: semwright-godot-production
description: Use when an agent must create, modify, persist, inspect, validate, repair, playtest, or export a managed Godot project through Semwright's typed Godot authoring profile and first-party Godot driver.
---

# Godot production

Use the live `driver.godot.*` capability catalog. Do not reconstruct schemas, grants, refs, or project paths from memory.

## Production loop

1. **DISCOVER** the current Godot capability catalog. Confirm that the managed-authoring profile is advertised before planning a new project. Authoring capabilities appear only when the host has configured bounded output/private-state grants.
2. **INSPECT** with `driver.godot.composition.inspect`. Treat the returned managed-source state as source-level evidence. `IN_SYNC` does not by itself prove that Godot parsed, saved, reopened, played, or exported the project.
3. **INTENT**: express the project through the typed `GodotAuthoringSpec`: project settings, scenes, native node/component kinds, resources/assets, relationships, animations, and bounded Behavior IR. Expressions include typed arithmetic/comparison/logic/clamp and bounded lerp; use typed transform actions for position/rotation/scale and managed-node reparenting; physics/gravity uses the typed vector acceleration actions on managed bodies with an explicit max-speed bound; `keep_global` is explicit and invalid hierarchy/dimension changes fail validation. Do not put GDScript, shell, arbitrary property/method names, plugins, executable paths, or expression strings in the payload.
4. **PLAN** with `driver.godot.composition.plan`. Review the returned base state, intent digest, write set, effect-contract digest, and target revision. Planning must not create target project files.
5. **APPLY** only the issued `plan_id` through `driver.godot.composition.apply`. The plan is private, owner-bound, one-shot authority under the authenticated Driver Host session; it is not permission merely because its digest is known.
6. **MEASURE** fresh persisted state with `composition.measure`, then **VALIDATE** with `composition.validate`. Keep source readback, native engine readback, runtime evidence, and export evidence distinct.
7. **REPAIR** only when validation identifies a supported deterministic repair. Currently a missing managed source can be regenerated through `composition.repair.plan` and `composition.repair.apply`. A human-edited managed source is `DIVERGED`: stop and replan from an explicit user/model decision instead of overwriting it.
8. **VERIFY** with `composition.verify` after a completed apply. Preserve the typed verification report and Project Graph receipt. An incomplete dependency frontier or UNKNOWN native predicate remains incomplete/UNKNOWN.
9. **NATIVE READBACK / PLAYTEST / SAVE-REOPEN** through `driver.godot.composition.native.verify` when the task requires engine, runtime or persistence evidence. Prefer `driver.godot.composition.native.query` when the model needs one managed node by logical key or one persistent resource by `res://` path with a bounded property allowlist instead of the complete native projection. Use `driver.godot.composition.native.tracks.page` for bounded animation-track enumeration and `driver.godot.composition.native.keys.page` for keyframes of one exact track; follow each cursor until `next_cursor` is null and reacquire from page one if the managed source/projection changes. Use a fresh process for persistence claims; a ResourceLoader cache hit is not a reopen proof.
10. **EXPORT** through the registered `driver.godot.export.*` routes when available and authorized. Run the exported package without editor/Semwright dependencies for a production claim, and inspect the package for authoring tooling, private paths, broker tokens, or test hooks.
11. Re-inspect after external edits, generation changes, import/reimport, or process restart. Reacquire ephemeral refs; do not treat a logical ID, path, native ref, and content digest as interchangeable identity.

## Generated code and supplied code

Semwright may deterministically generate GDScript from the typed Behavior IR. That generated source is a backend artifact with fixed templates and provenance; it is not caller-supplied arbitrary code.

Assets declared under the configured input grant are supplied inputs. Existing human project files are external state unless explicitly managed. Never adopt an arbitrary non-empty directory, install an internet addon, execute a project callback to infer intent, or modify an unowned shared resource just to make validation pass.

## Limits and evidence

Behavior budgets bound authored event/timer/spawn behavior; they are not a sandbox for arbitrary third-party Godot code. Source hashes prove only the observed file scope. Native scene structure, imports, runtime physics, animation playback, save/reopen, and exports require their own native evidence.

Read the focused references when relevant:

- [semantic authoring](references/semantic-authoring.md)
- [native evidence](references/native-evidence.md)
- [security and repair](references/security-and-repair.md)
