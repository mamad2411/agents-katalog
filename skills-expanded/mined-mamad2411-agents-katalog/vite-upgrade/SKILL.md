---
name: vite-upgrade
description: "Upgrade Vite and plugins with compatibility and build checks. Use for a requested Vite version transition; deps handles general dependency selection."
---

# vite-upgrade

Upgrade Vite and plugins with compatibility and build checks.

## Choose this workflow

Use for a requested Vite version transition; deps handles general dependency selection.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Vite methods](../../references/packs/vite.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **apply**. Apply for a requested upgrade; source/target version, framework/plugins, and runtime constraints.

**Pack prerequisites:** Project manifests, lockfile, Vite/framework/plugin versions, and existing build scripts. Verify current version-specific documentation when changing configuration. Requested isolated verification may generate disposable build/cache artifacts; inspect their scripts first and preserve product files.

- **Infer from evidence:** Read manifests, lockfile, installed Vite/plugins, entry points, aliases, modes and current build scripts.
- **Reasonable default:** Preserve existing tooling and base-path conventions; in apply mode, make a local focused change when the brief identifies the behavior, and otherwise propose it.
- **Ask only when needed:** Ask if the intended serving subpath or deployment target cannot be inferred and would change generated URLs; do not ask for versions present in the lockfile.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Compatible Vite/toolchain upgrade and necessary config changes.

Apply: only the requested local changes and relevant isolated verification. Inspect/plan requests remain inspection/planning. External actions require their exact action and target in session authorization.

## Execute

1. Read the target version's migration notes and check framework-plugin and Node compatibility.
2. Update only the required dependency graph and lockfile, and adjust deprecated behavior.
3. Compare dev refresh, production output and preview behavior with the previous version.

## Technical method

- **Inspect:** Read current/target migration notes, Node support, framework plugin peer ranges and config differences.
- **Method:** Upgrade a coherent toolchain with the project's lockfile; remove obsolete options only after mapping their replacement behavior.
- **Avoid misdiagnosis:** A passing install with ignored peer conflicts does not establish refresh or production compatibility.
- **Check the result:** Verify dev refresh, build, preview and relevant SSR/test integration; report a plugin blocker instead of forcing an unsupported combination.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Vite worked example](../../references/examples/vite.md).


## Decision branches

- **When a required plugin has no compatible version:** Stop at that compatibility boundary and propose a supported intermediate target.

## Deliver and verify

- Upgrade patch with a version/peer matrix, configuration changes, dev/build/runtime checks and rollback steps.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Framework refresh and build both work; incompatible plugins are resolved or explicitly block the target version.

## Stop and recover

- No unrelated major upgrades. If a required peer is unsupported, stop before presenting a broken combination as complete.

## Example requests

- **Normal (apply):** Upgrade to the specified Vite version and verify framework-plugin compatibility.
- **Edge (apply):** Upgrade Vite while retaining an older framework plugin until a supported replacement exists.
- **Blocked (inspect):** Plan an upgrade with unavailable release-note access; do not guess removed options.
