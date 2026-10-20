---
name: vite-chunks
description: "Investigate loading boundaries, duplicated modules, and chunks. Use to change lazy-loading/cache boundaries; vite-bundle first identifies heavy contributors."
---

# vite-chunks

Investigate loading boundaries, duplicated modules, and chunks.

## Choose this workflow

Use to change lazy-loading/cache boundaries; vite-bundle first identifies heavy contributors.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Vite methods](../../references/packs/vite.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect for analysis; apply for a requested split or loading-boundary change. Requires route/loading behavior, build artifacts, and chunk configuration.

**Pack prerequisites:** Project manifests, lockfile, Vite/framework/plugin versions, and existing build scripts. Verify current version-specific documentation when changing configuration. Requested isolated verification may generate disposable build/cache artifacts; inspect their scripts first and preserve product files.

- **Infer from evidence:** Read manifests, lockfile, installed Vite/plugins, entry points, aliases, modes and current build scripts.
- **Reasonable default:** Preserve existing tooling and base-path conventions; in apply mode, make a local focused change when the brief identifies the behavior, and otherwise propose it.
- **Ask only when needed:** Ask if the intended serving subpath or deployment target cannot be inferred and would change generated URLs; do not ask for versions present in the lockfile.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Dynamic imports, shared chunks, duplicate modules, and loading boundaries.

Inspect/plan: inspect or propose; save requested artifacts only. Apply: edit the requested local implementation and perform relevant bounded checks while preserving unrelated work. Live data changes, remote actions and paid jobs require their resolved target and existing session authorization.

## Execute

1. Map entry points, dynamic imports and shared chunks to representative navigation waterfalls.
2. Examine dependency duplication, circular dependencies and cache invalidation against initial-load cost, and propose focused splitting changes.

## Technical method

- **Inspect:** Inspect dynamic imports, shared dependencies, manual chunk rules and module side effects.
- **Method:** Split at meaningful usage boundaries and check initialization order and caching across releases.
- **Avoid misdiagnosis:** A smaller entry chunk can add serial requests or cause a stale HTML document to reference a deleted old chunk.
- **Check the result:** Test cold navigation, lazy routes and an older open page during deployment; define reload/recovery for missing chunks.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Vite worked example](../../references/examples/vite.md).


## Decision branches

- **When manual splitting changes execution order or creates a waterfall:** Verify module side effects and route transitions before accepting byte reductions.

## Deliver and verify

- Chunk and dependency map with the request waterfall, and an optimization plan or, in apply mode, a patch with loading evidence and navigation checks.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- A split reduces the intended initial work; deep-link and lazy-load paths still resolve all required modules.

## Stop and recover

- Avoid arbitrary manual chunk rules without evidence. Report missing network traces rather than inventing loading improvements.

## Example requests

- **Normal (inspect):** Find duplicated dependencies and loading-boundary issues in these build artifacts.
- **Edge (apply):** Split a heavy dashboard while preserving direct deep links and shared vendor initialization.
- **Blocked (inspect):** Plan chunks without network traces; report loading benefits as hypotheses.
