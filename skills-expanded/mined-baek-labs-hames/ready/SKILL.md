---
name: ready
description: Prepare and present a bounded task contract for same-session approval by /go when the user invokes /ready.
---

# Ready

Read `references/intent.md` for the integrated intent-to-execution procedure. This is a Hames adaptation of DryForge, already included in this plugin.

Use the user's language. Ordinary file work does not require a contract or Git. Never initialize Git or install another DryForge plugin.

Turn the user's intent into a complete, readable Hames contract. Do not start execution.

Read `.hames/config.yaml` and load the selected workspace through the bundled `runtime/context.js`. Read common rules, its index and relevant registered root `docs/` only. Switch the session selection when the task moves to another workspace; ask only if the target is unclear. Never force-load all docs.

Use project evidence and choices already stated by the user before asking questions. Ask only about unresolved choices that would change the result.

Record the goal, targets, actions, allowed and denied scope, outputs, invariants, acceptance criteria, evidence, and risk. Also record deliverable locations, work steps and dependencies, review policy, and durable-knowledge destinations. Require independent review for behavior, API, permission, data-processing, external-state, or complex judgment-heavy work; use direct verification for simple reversible work.

For a new document, record, web resource, or external resource, use the location and name already stated by the user. Ask only for a missing `parent` or `planned_name`; do not ask again when both are known.

Require before, action, and after evidence for external changes unless the contract records a reason and explicit exception approval. Mark critical actions; `/ready` approval does not authorize executing them.

Keep spec, work plan, and handoff in one readable contract, backed by the existing machine specification. Put long-lived knowledge only in approved shared root `docs/` destinations. Automatic index bookkeeping for approved file writes is derived maintenance, not permission for other document edits.

Show goal, scope, outputs, work order, review policy, and acceptance criteria before the complete machine specification. Use `present` to tie the display to the project, session, task, revision, specification hash, and display digest, then move it to `READY` without recording approval.

Tell the user that `/go` in the same conversation approves and activates exactly this presented contract. Do not request a separate approval reply. A changed contract must be presented again.

Use the bundled `runtime/contract.js` `draft`, `amend`, and `present` commands. Retain `approve` only for compatible explicit-approval flows. Stage machine input only under ignored `.hames/state/` and include no secret values.
