# Workflows

Autonomy workflows and their co-located prompts live here.

## Definition Contract

- Keep each workflow cohesive, typed, and role-focused. `workflow.ts` is the
  source of truth and the autonomy module is the only registry.
- Declare repository access on every workflow. Writers also declare integration
  validation; use logical resources for semantic exclusivity such as one task.
  When canonical domain identity must remain unchanged from admission through
  publication, declare a pure `integration.postReconcile` invariant. The shared
  integration rail runs it after rebase under publication serialization.
- Definitions describe semantic work. `RunStateDatabase`, `RunCoordinator`,
  `RunLifecycle`, and `IntegrationQueue` own queueing, capacity, isolation,
  resources, processes, recovery, commit, validation, and publication.
- Retained changes in a run-owned sandbox are unfinished work, not a reason
  to skip the workflow. Canonical cleanliness and safe publication belong to
  the shared runtime; do not duplicate those gates inside domain steps.
- Do not add workflow-specific claims, worktrees, branches, staging helpers,
  merge gates, port leases, or synthetic recovery triggers. Local completion
  bookkeeping uses the shared synchronous success hook.
- Shared cadence and watermark values use the runtime state API. Workflows read
  a revision and stage compare-and-set; they do not write canonical state files
  or publish dependent events before run success.
- Every agent step declares autonomy explicitly or inherits
  `defaultAutonomyMode`. Agent write scope is enforced inside the run sandbox;
  prompts should describe the role, not restate runtime rails.
- Agents write declared evidence under `$KOTA_RUN_DIR` and
  `$KOTA_RUN_ARTIFACT_DIR`. They do not stage, commit, rebase, or publish Git
  changes.

## Routing

Only `dispatcher` listens to `runtime.idle`. Other workflows trigger on typed
events describing domain state. A `workflow.completed` trigger must exclude its
own completion; validation rejects self-trigger loops.
Batch and watch trigger positions are persisted. Preserve existing positions
when adding triggers, and verify queued work survives definition updates.

Dispatcher emits queue-shape events rather than a fixed workflow graph:

- `autonomy.queue.available` identifies one dependency-clear `open` task. Its
  immutable digest and `taskId` bind builder to `task:<taskId>`.
- `autonomy.queue.empty` means no unclaimed runnable task or inbox work exists;
  explorer may look for independent work even while dependencies wait.
- `autonomy.queue.thin` reports available independent supply at or below the runtime
  capacity reserve, excluding queued, running, retained, and dependency-waiting tasks.
- `autonomy.blocked-research.attemptable` identifies blocked research that the
  current runtime can retry.

Blocked tasks remain active in `data/tasks/`; the blocked promoter changes a
satisfied task back to `open` before dispatcher can emit a builder event.

## Repair And Tests

- Repair checks validate without editing or staging. Use typed code checks for
  objective invariants and agent judgment for architecture or intent.
- Give each decision one owning test layer. Workflow tests cover semantic
  routing, predicates, resource binding, and outcomes; shared runtime tests own
  durable admission, capacity, sandbox, process/effect recovery, integration,
  and publication behavior.
- Do not freeze config catalogs, helper call order, filenames, private phases,
  or retired concurrency/recovery mechanics in tests.
- Resource observations compare workflow bindings; allocation, contention, and
  cross-scope isolation stay with the core resource owner. Agent and subprocess
  ports may be controlled, while task mutations and owner-question resolution
  use their production owners.
