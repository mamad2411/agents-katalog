---
name: vite-config
description: "Audit aliases, plugins, build options, and environment handling. Use to inspect effective configuration; vite-hmr or vite-assets handles a known failure surface."
---

# vite-config

Audit aliases, plugins, build options, and environment handling.

## Choose this workflow

Use to inspect effective configuration; vite-hmr or vite-assets handles a known failure surface.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Vite methods](../../references/packs/vite.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; configuration files, intended behavior, and observed issue. Apply for a requested configuration fix.

**Pack prerequisites:** Project manifests, lockfile, Vite/framework/plugin versions, and existing build scripts. Verify current version-specific documentation when changing configuration. Requested isolated verification may generate disposable build/cache artifacts; inspect their scripts first and preserve product files.

- **Infer from evidence:** Read manifests, lockfile, installed Vite/plugins, entry points, aliases, modes and current build scripts.
- **Reasonable default:** Preserve existing tooling and base-path conventions; in apply mode, make a local focused change when the brief identifies the behavior, and otherwise propose it.
- **Ask only when needed:** Ask if the intended serving subpath or deployment target cannot be inferred and would change generated URLs; do not ask for versions present in the lockfile.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Aliases, plugins/order, build targets, server options, and environment handling.

Inspect/plan: inspect or propose; save requested artifacts only. Apply: edit the requested local implementation and perform relevant bounded checks while preserving unrelated work. Live data changes, remote actions and paid jobs require their resolved target and existing session authorization.

## Execute

1. Resolve command, mode, root, envDir, aliases and plugin order from the actual invoked script, and check version compatibility.
2. Trace conflicting options, compare development with production behavior and TypeScript with bundler resolution, and propose focused corrections.

## Technical method

- **Inspect:** Read effective command/mode, root/envDir, aliases, plugins, define replacements and server restrictions.
- **Method:** Trace each disputed option to its consuming tool; reconcile TypeScript paths with actual bundler resolution.
- **Avoid misdiagnosis:** A config file can execute arbitrary imports; read-only inspection should not evaluate it just to discover values.
- **Check the result:** Check the relevant dev and production resolution paths, including case-sensitive filenames and browser-exposed replacements.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Vite worked example](../../references/examples/vite.md).


## Decision branches

- **When a config function branches on command or mode:** Assess each relevant branch statically before executing potentially side-effecting configuration.

## Deliver and verify

- Effective configuration by invocation, unsupported or conflicting settings with reasoning and, in apply mode, a focused patch.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- A TypeScript-only alias missing at runtime is identified; a version-unsupported option is not recommended.

## Stop and recover

- Do not execute arbitrary config code during read-only inspection without considering its side effects. Missing build evidence remains unknown.

## Example requests

- **Normal (inspect):** Audit aliases and plugin order for the installed Vite version.
- **Edge (inspect):** Diagnose an alias that typechecks but fails in the production bundle.
- **Blocked (inspect):** Inspect config source with no build permission; do not execute arbitrary imports.
