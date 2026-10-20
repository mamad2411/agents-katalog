# Decomposer Workflow

Decomposer diagnoses failed builder scope after timeout or exhausted repair.
A coherent task may remain unchanged; replacement requires independently useful
outcomes and approval before any mutation.

- It triggers only from a failed builder completion and reads the canonical run
  metadata and immutable builder trigger contract from `.kota/runs/<run-id>`.
- The builder payload identifies one task and digest. Decomposer rechecks that
  contract against the current verified task snapshot; changed, terminal, or
  non-actionable work is superseding evidence and skips decomposition.
- Builder and decomposer bind the same `task:<taskId>` logical resource.
  `RunStateDatabase` owns exclusivity; there is no task-claim file or
  builder-specific lease.
- The workflow declares repository write access and task validation.
  `RunLifecycle` supplies the sandbox and `IntegrationQueue` publishes the
  result only after the failed builder's source task contract still matches
  the canonical snapshot used for the final rebase.
- Planning and review agents are read-only. Only replacement plans reach review, which compares them with the
  exact screened task markdown before mutation.
- `apply-decomposition` is the only semantic mutation path. It uses repo-tasks
  operations to create dependency-linked open tasks, annotate the original,
  and move it to `dropped`.
- Replacement retargets incoming active-task dependencies to the children in
  the same publication. It validates the full prospective queue and current
  held-task ownership before any sandbox writes; integration rechecks ownership.
  The immutable failed-builder digest remains bound to the original task.
- Tests cover source authentication, superseding task evidence, shared resource
  binding, approved mutations, and observable queue outcomes rather than claim
  artifacts or commit mechanics.
