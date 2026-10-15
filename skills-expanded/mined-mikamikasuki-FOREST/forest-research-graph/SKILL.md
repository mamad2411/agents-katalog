---
name: forest-research-graph
description: "Integrate or redesign FOREST's research graph, node editor, branch actions, and impact review while preserving revision guards, dependencies, provenance, and scheduling semantics. Use for graph UI or client changes, not scientific experiment design."
---

# FOREST research graph integration

Make graph editing understandable without changing the research execution contract.
Keep editable structure, scheduling, current results, and historical evidence distinct.

## Start with the affected contract

Read [repository-map.md](references/repository-map.md) for the affected operation,
its owner, source pointers, and regression scenarios before changing graph behavior.
The map records inspected HEAD `ff16c3f656f94d053d1bba65c6b3a07a5feaccde`;
confirm the target repository's current source rather than treating this snapshot
as a permanent API specification. All source paths in the map are FOREST-root relative.
Limit investigation to the changed operation and its consumers; expand only when
a concrete state or provenance question remains unresolved.

The canonical research skills under `research/agents/skills/` remain authoritative
for scientific execution. This frontend skill does not revise their policies,
research completion rules, protocols, acceptance conditions, or model instructions.

## Retain the real graph

- Preserve project/graph revision, node IDs/revisions, branches, typed edges,
  `input_mapping`, `inputs`, `outputs`, `context_overrides`, comments, and config.
- Keep fetched state and unsaved drafts separate. Store the graph/project revision
  originally loaded into a node editor or impact preview.
- Node `revision` identifies execution provenance; node PATCH uses the
  **project/graph** `expected_revision` and returns a graph-command result.
- Node types and execution/research/deliverable statuses are extensible strings.
  Render unknown values explicitly; do not replace them with a guessed enum.
- Preserve unknown configuration and metadata. Kernel node patches deep-merge;
  resource/run editors use other merge rules and cannot share that assumption.
- Paged graph edges may point outside the displayed page. Resolve external
  endpoints without deleting their edges or treating them as broken graph data.

## Use supported operations

At the inspected HEAD, the kernel supports:

```text
add_node edit_node delete_node add_dependency remove_dependency
fork_branch clone_subtree insert_before insert_after reparent_subtree
merge_branches split_node group_nodes prune_branch restore_branch
reopen_branch revise_goal set_main_branch apply_instruction_patch undo redo
```

Read the operation table in [repository-map.md](references/repository-map.md)
when implementing an action; parameters and batch eligibility are not uniform.
Do not derive an operation name from a visual label or add a UI-only mutation.
Use `requestApi()` with the generated `/api` contract for new JSON calls.

## Review, apply, and reconcile

1. Build one intended command with `request_id`, loaded `expected_revision`,
   operation, targets, params, and explicit `run` choice; default ordinary edits
   to `run:false` unless execution was requested.
2. When impact review is needed, preview that command. Preview returns impact
   only and changes neither graph nor workspace files.
3. Show changed/affected nodes, rerun/refresh nodes, reasons, conflicts, files,
   missing input bindings, and proposed external actions where returned.
4. Apply the reviewed intent against its original revision. Retain its identity
   through uncertain transport outcomes; changed intent needs a new ID.
5. Adopt the server graph/revision and inspect intervention effects and run IDs.
   A saved edit, queued run, or accepted control is not completed execution.
6. On 409, preserve the draft/preview, fetch current graph, expose the conflict,
   and merge or re-review before resubmitting. Never refresh only the guard.

Request receipts are endpoint-specific. Node PATCH generates its own request ID;
use graph commands when recovery with a client-controlled identity is required.
Do not automatically replay mutations after an error with a fresh UUID.

## Preserve scientific dependencies

`depends_on` and `consumes` order execution, with source before target. Inputs,
verification producer bindings, and required verifier nodes also create implicit
execution dependencies. Use existing `executionLinks()`/`hasCycle()` behavior
and server validation; a canvas-only cycle check is incomplete.
History, citation, evidence, and grouping relations have separate propagation
duties. Retain their relation rather than turning every arrow into a dependency.

Layout/title/group changes must not launch experiments. Semantic, statistical,
figure-style, paper-wording, and Goal edits have different server-computed impacts.
Do not invalidate all evidence or enqueue all descendants from a client heuristic.
Goal changes preserve completed computation and may require a new evidence-use decision.

## Explain branch and history effects

Prune stops future dispatch and holds queued work; it does not stop running work.
Restore/reopen does not resume held runs. A fork/merge can remain `materializing`
until its source-bound file receipt is confirmed; preserve that execution barrier.
Inherited results are inspectable history, not fresh/current execution.
Undo/redo restores editable structure and preserves monotonic identities/history;
it does not reverse completed commands, file writes, or external effects.

## Verify the changed behavior

Use the relevant local graph/API/browser cases in
[repository-map.md](references/repository-map.md), including stale drafts/previews,
implicit cycles, selective invalidation, branch holds, and inherited results.
Use existing unit fixtures for isolated logic. Integrated changes also require
an isolated real local backend/worker/artifact smoke workflow as guided by the
browser-testing skill; fixture data cannot substitute for those observed effects.
Do not start the user's existing research tasks or use an unauthorized paid
provider. Provider-free local execution and actual artifacts are permitted.
Report what was observed and what remains unexecuted; schema agreement alone
does not establish current-result correctness or scientific validity.
