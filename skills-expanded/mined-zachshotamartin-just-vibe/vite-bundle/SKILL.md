---
name: vite-bundle
description: "Analyze bundle composition and measured size reductions. Use for bundle composition and size; vite-chunks focuses on loading boundaries."
---

# vite-bundle

Analyze bundle composition and measured size reductions.

## Choose this workflow

Use for bundle composition and size; vite-chunks focuses on loading boundaries.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Vite methods](../../references/packs/vite.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect for analysis; apply for a requested size change. Requires saved build stats/artifacts and a size/performance goal; a comparison build is bounded local execution with output in an owned temporary directory.

**Pack prerequisites:** Project manifests, lockfile, Vite/framework/plugin versions, and existing build scripts. Verify current version-specific documentation when changing configuration. Requested isolated verification may generate disposable build/cache artifacts; inspect their scripts first and preserve product files.

- **Infer from evidence:** Read manifests, lockfile, installed Vite/plugins, entry points, aliases, modes and current build scripts.
- **Reasonable default:** Preserve existing tooling and base-path conventions; in apply mode, make a local focused change when the brief identifies the behavior, and otherwise propose it.
- **Ask only when needed:** Ask if the intended serving subpath or deployment target cannot be inferred and would change generated URLs; do not ask for versions present in the lockfile.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Bundle composition and measured reductions, not arbitrary dependency removal.

Inspect/plan: inspect or propose; save requested artifacts only. Apply: edit the requested local implementation and perform relevant bounded checks while preserving unrelated work. Live data changes, remote actions and paid jobs require their resolved target and existing session authorization.

## Execute

1. Record the installed versions, command, mode, route and baseline artifact. Separate raw output, compressed size and actual transferred bytes; compare equivalent build and cache conditions.
2. Trace a large or duplicate module to imports and the user journey that loads it. Distinguish startup cost from total application cost and verify whether an existing lazy boundary is defeated by an eager import.
3. Choose a focused change based on the observed cost. Splitting a module can add a waterfall or alter side-effect order; avoid generic manual-chunk rules or removing dependencies solely because they are large.
4. Build and exercise affected entry/lazy routes, direct navigation and failure recovery. Report comparable before/after measurements plus functional checks; a smaller output file alone does not prove faster interaction.

## Technical method

- **Inspect:** Read production stats or source maps, entry imports and real route loading with identical build conditions.
- **Method:** Attribute large modules to reachable imports and compare raw, compressed and transferred sizes separately.
- **Avoid misdiagnosis:** Removing a named import or counting source file sizes does not prove tree-shaking or network improvement.
- **Check the result:** Rebuild and exercise representative routes; record comparable bytes and loading behavior, including any new lazy-load waterfall.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Vite worked example](../../references/examples/vite.md).


## Decision branches

- **When a dependency is large but loaded only after an optional interaction:** Measure its contribution to that interaction rather than attributing it to initial load.

## Deliver and verify

- Size breakdown, cause, changes made in apply mode, and comparable before/after results.
- Import path, size metric, loaded route and before/after build conditions.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Measurements share build/mode/version assumptions, and affected initial and lazy routes still load correctly. Raw bytes are not mislabeled as transfer size or user-perceived performance.

## Stop and recover

- Do not equate smaller bytes with faster UX without timing evidence. Missing stats limit numerical conclusions.

## Example requests

- **Normal (inspect):** Analyze the supplied production bundle statistics and prioritize size reductions.
- **Edge (apply):** Reduce initial bytes without breaking a lazily loaded editor.
- **Blocked (inspect):** Review available bundle stats without installing an analyzer or inventing timing gains.
