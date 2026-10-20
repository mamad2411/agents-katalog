# Issue Disposition Workflow

This workflow is the single AI decision path for durable autonomy issues.

- Trigger from a new, reopened, or materially revised issue transition, or a
  bounded same-revision reconciliation attempt after the prior owner failed.
- Disposition application belongs to its typed action owner; the definition
  invokes it and retains routing, agent authorization, validation, and publication.
- Keep the agent read-only. Source implementation belongs to builder.
- Route task and owner-question proposals through the shared generated-work
  transaction using the issue key as stable proposal identity. Repository task
  changes stage in the writer; idempotent owner-question effects and issue
  disposition publish in the original run's shared success finalizer.
- Bind the staged disposition to the issue's owner fingerprint. Recheck that
  fingerprint against canonical scope state immediately before integrating
  task changes and before finalizing any follow-up owner effects.
- Repeated evidence enriches projection provenance without another review or
  attention item.
- Investigators receive cited run diagnostics and module logs through the shared
  scoped issue export in their agent directory. Missing or unsafe content stays
  explicitly unavailable; references do not authorize canonical host reads.
- Inspect the linked evidence, current owner, implementation, and related queue
  work before acting. Link relevant existing repair tasks through the disposition
  contract; publication rechecks the reviewed task body without changing its
  contract or runtime claim. Reconciliation follows that same issue/task link,
  retaining task lineage after a clear observation for recurrence review.
- Do not replay AI review without a new decision-request transition.
- `doctor.fix` is the sole deterministic recovery action. Its allowlist and
  idempotent settled-state verification target only the cited stale daemon
  control record through the doctor repair owner; general maintenance is a
  separate operator action. Source changes remain builder-owned tasks.
- Exhausted investigation retries publish the issue's durable `attention`
  disposition. A terminal run by itself is never an owner.
- Investigation backoff is a future-eligible durable improver run. Completion
  and one-shot workflow-runtime startup reconciliation admit that owner; idle
  polling does not own or re-drive issue investigation.
