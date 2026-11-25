---
name: work-revit
description: Create, edit, move, copy, type-change, pin, delete, or automate Revit 2024 model elements through Revit MCP Next on Windows 11. Use for walls, grids, floors, rooms, family placement, parameters, model changes, or any request that mutates the active Revit document.
---

# Work in Revit

Use discovery-first, preview/apply automation:

Require native Windows 11 and a local Revit 2024 process. Do not attempt this
workflow from macOS, Linux, WSL, containers, or a remote non-Windows host.

1. Call `revit.read_bundle`; record document fingerprint and generation while
   collecting the bounded model context needed for the change.
2. Use at most one additional focused discovery call for exact levels,
   elements, types, symbols, hosts, or writable parameters. Never guess IDs.
3. Include `expectedUniqueId` or `expectedHostUniqueId` when prior reads provide
   them.
4. Call `revit.preview_change_set` with a small, named transaction.
5. Inspect every change, warning, dependent delete, and risk flag. Never apply a
   blocked preview.
6. Call `revit.apply_change_set` with the exact operations and returned
   `previewId`, `baseGeneration`, `changeSetHash`, `expiresAt`, and `confirm=true`.
7. Verify with focused read-only calls.

The normal target is four MCP round trips: bundled context, preview, apply, and
focused verification. Add a discovery call only when the bundle cannot supply
an exact ID or parameter contract. Never run installer or doctor commands in a
healthy write workflow.

Preview tokens are single-use and short-lived. If the model generation changes,
refresh reads and preview again. After a timeout or unknown commit state, do not
retry a non-idempotent change before read-only verification.

Ask before destructive deletion, dependent deletion, overwriting files, or
changes whose target/scope is ambiguous. Use a disposable model for setup and
write smoke tests.

Read `../../references/write-safety.md` for the supported operation map and
recovery rules.
