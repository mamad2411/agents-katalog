---
name: comfyui-core-runtime
description: Use when changing or diagnosing ComfyUI core execution, server behavior, backend APIs, model loading, caching, scheduling, node execution internals, filesystem handling, or other code owned by the ComfyUI runtime rather than a third-party custom-node pack.
metadata:
  version: "00.01.11"
---
# ComfyUI Core Runtime

If the `comfyui-development` router skill is installed, follow its shared authority/freshness policy. This specialist remains usable on its own.

## Primary sources

- target/version-matched `Comfy-Org/ComfyUI`;
- matching/current `Comfy-Org/docs`;
- tests in the core repository;
- RFCs only for proposal/history context.

## Procedure

1. Establish the compatibility target and exact checkout/commit.
2. Reproduce or locate the owning subsystem before editing.
3. Search for the behavior and its tests rather than assuming old module paths.
4. Trace call sites across the execution path.
5. Check for feature flags, version guards, compatibility shims, or deprecations.
6. Make the smallest behaviorally complete change.
7. Run the narrowest relevant tests, then broader tests if feasible.
8. For server/API changes, verify the actual route/payload behavior on a running target when practical.
9. For node-facing changes, inspect resulting live node definitions or representative workflows.

## Do not

- hardcode an internal path merely because it existed in a previous release;
- infer an API contract from an internal helper alone;
- use an RFC as proof that code has shipped;
- refactor unrelated code as part of a bug fix;
- update the user's checkout to upstream without permission.

## Evidence for completion

At least one of these should exist before claiming the change works:

- relevant automated tests pass;
- a minimal runtime reproduction passes;
- a server/API probe confirms the behavior;
- a representative workflow exercises the changed path.

## Acceptance gate

Before calling the change complete:

- record or identify the target ComfyUI commit/version;
- show that the change addresses the owning execution path;
- pass a focused test or minimal runtime reproduction;
- verify public route, node, or workflow behavior when the change affects one;
- update public documentation when the supported contract changed.

