---
name: vite-hmr
description: "Diagnose broken, slow, or inconsistent hot-module updates. Use for broken development updates; react-effects handles lifecycle bugs visible during refresh."
---

# vite-hmr

Diagnose broken, slow, or inconsistent hot-module updates.

## Choose this workflow

Use for broken development updates; react-effects handles lifecycle bugs visible during refresh.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Vite methods](../../references/packs/vite.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; affected file/component, development environment, and HMR logs or reproduction. Apply for a requested fix.

**Pack prerequisites:** Project manifests, lockfile, Vite/framework/plugin versions, and existing build scripts. Verify current version-specific documentation when changing configuration. Requested isolated verification may generate disposable build/cache artifacts; inspect their scripts first and preserve product files.

- **Infer from evidence:** Read manifests, lockfile, installed Vite/plugins, entry points, aliases, modes and current build scripts.
- **Reasonable default:** Preserve existing tooling and base-path conventions; in apply mode, make a local focused change when the brief identifies the behavior, and otherwise propose it.
- **Ask only when needed:** Ask if the intended serving subpath or deployment target cannot be inferred and would change generated URLs; do not ask for versions present in the lockfile.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Watcher events, module invalidation, framework refresh, and proxy/network transport.

Inspect/plan: inspect or propose; save requested artifacts only. Apply: edit the requested local implementation and perform relevant bounded checks while preserving unrelated work. Live data changes, remote actions and paid jobs require their resolved target and existing session authorization.

## Execute

1. Follow the file change from watcher to module graph to HMR connection and framework boundary, inspecting plugin boundaries and duplicate modules.
2. Localize the failure, distinguishing transport loss, invalidation and a deliberate full reload from hot replacement.

## Technical method

- **Inspect:** Observe filesystem watcher, module invalidation, websocket transport and framework refresh boundary.
- **Method:** Identify the first missing event and repair that layer; inspect proxy and container paths before changing host restrictions.
- **Avoid misdiagnosis:** Full page reload and preserved hot state are different outcomes; disabling host checks is not a generic websocket repair.
- **Check the result:** In apply mode or an owned copy, edit a leaf and a shared dependency, verify the expected refresh behavior, and check reconnection after an ordinary dev restart.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Vite worked example](../../references/examples/vite.md).


## Decision branches

- **When updates fail only through a proxy or container:** Inspect websocket origin/port and mounted-path watching before relaxing host/filesystem protections.

## Deliver and verify

- Reproduction steps, the failing HMR boundary and a focused fix proposal; in apply mode, the applied fix with update and state-preservation checks.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- A changed module updates correctly after remediation; unrelated state is preserved when the framework supports it.

## Stop and recover

- Running the project's dev server is bounded local execution. Do not disable host protections or broadly relax filesystem access as a default fix.

## Example requests

- **Normal (inspect):** Investigate why changes trigger full reloads and lose form state.
- **Edge (inspect):** Diagnose refresh failing behind a reverse proxy while direct localhost works.
- **Blocked (inspect):** Inspect HMR configuration without starting a dev server; identify needed browser evidence.
