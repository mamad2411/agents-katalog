---
name: vite-env
description: "Check environment loading and exposure of server-only values. Use for build mode, environment loading and client exposure; vercel-env checks deployment scope metadata and security-secrets searches the repository and history for committed credentials."
---

# vite-env

Check environment loading and exposure of server-only values.

## Choose this workflow

Use for build mode, environment loading and client exposure; vercel-env checks deployment scope metadata and security-secrets searches the repository and history for committed credentials.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Vite methods](../../references/packs/vite.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; build mode, expected variable names, environment files, and exposure policy. Apply for a requested configuration fix without reading or printing secret values.

**Pack prerequisites:** Project manifests, lockfile, Vite/framework/plugin versions, and existing build scripts. Verify current version-specific documentation when changing configuration. Requested isolated verification may generate disposable build/cache artifacts; inspect their scripts first and preserve product files.

- **Infer from evidence:** Read manifests, lockfile, installed Vite/plugins, entry points, aliases, modes and current build scripts.
- **Reasonable default:** Preserve existing tooling and base-path conventions; in apply mode, make a local focused change when the brief identifies the behavior, and otherwise propose it.
- **Ask only when needed:** Ask if the intended serving subpath or deployment target cannot be inferred and would change generated URLs; do not ask for versions present in the lockfile.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Load precedence, prefixes, build-time replacement, and client/server separation.

Inspect/plan: inspect or propose; save requested artifacts only. Apply: edit the requested local implementation and perform relevant bounded checks while preserving unrelated work. Live data changes, remote actions and paid jobs require their resolved target and existing session authorization.

## Execute

1. Trace import.meta.env usage and the configured envPrefix, and inspect mode-specific files by names only.
2. Determine which mode supplies each name, separating build mode from NODE_ENV, and inspect existing generated bundles for exposure when available.
3. Recommend narrow corrections.

## Technical method

- **Inspect:** Inspect modes, envDir, public prefixes, define substitutions and client import paths using variable names.
- **Method:** Trace whether the value is compiled into client output or read only by server code; keep mode distinct from NODE_ENV.
- **Avoid misdiagnosis:** Prefixing a secret with VITE_ makes it public; booleans read from env may be strings with surprising truthiness.
- **Check the result:** Build with a synthetic sentinel and inspect intended exposure and parsing without placing real secret values in reports.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Vite worked example](../../references/examples/vite.md).
- The task depends on framework defaults, middleware, RLS, server/client or deployment behavior: [Framework-specific review branches](../../references/security/frameworks.md).

## Decision branches

- **When a required secret is referenced by client code:** Move the privileged operation behind a server boundary instead of adding a client-exposed prefix.

## Deliver and verify

- Redacted name/consumer/mode/exposure table with exposure and missing-value findings, and evidence from a controlled built artifact.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Server-only credentials are not moved into client-exposed prefixes; development and production modes resolve the intended public configuration.

## Stop and recover

- Never print secret values. Secret rotation is a separate authorized action; configuration edits use apply mode.

## Example requests

- **Normal (inspect):** Check whether server-only configuration is exposed in the client bundle.
- **Edge (inspect):** Diagnose a staging build made with a production NODE_ENV and a custom mode.
- **Blocked (inspect):** Inspect environment references without reading secret values or building output.
