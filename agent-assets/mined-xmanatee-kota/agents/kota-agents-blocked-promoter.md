# Blocked Promoter

Evaluates typed unblock preconditions and moves tasks whose blockers have
cleared.

- This workflow declares repository write access, task resources and validation.
  Shared runtime owns its sandbox, recovery, commit, and publication.
  Task selection stays bound to the admitted resource snapshot through recovery
  and cleanup; later blocked tasks belong to a later admission.
- Retained writer edits do not gate promotion or owner follow-up. Runtime owns
  checkout isolation and publication safety; task contract and resource checks
  retain authority during recovery.
- Promotion, owner-question selection, capture instructions, and the action
  artifact consume one blocker decision. Hard dependencies precede every
  follow-up; the attention digest shares that decision owner’s cadence.
- Never move terminal tasks. Use repo-tasks domain operations for every state
  transition.
- Capture paths are discovery hints. File existence, names, and extensions
  never satisfy acceptance. Review outcome, execution provenance, and required
  positive/negative behavior before reopening through normal task operations.
  Use already authorized collection and equivalent evidence wherever available;
  an operator need not repeat permission or run an otherwise permitted command.
- Scoped captures and declared contained probes feed an independent precondition
  review. Content fingerprints publish through runtime state; unchanged inputs
  do not repeat the review. Broad discovery uses task-linked run/export cohorts;
  unrelated activity and attempt bookkeeping do not admit retries. Keep task
  or cited run provenance in exports so equivalent captures remain discoverable.
  Select the pinned collection through the shared pageable review handoff;
  provenance paths do not grant read authority. Failed handoffs do not complete
  an assessment or publish its fingerprint.
  Review outcomes reopen work, never mark it done.
  Review agents declare deny-all filesystem authority through the shared launch
  contract; task mutations belong to the workflow after the assessment.
  Canonical contract drift rejects publication after reconciliation.
  Declared probe reviews check trusted declaration provenance and executable
  repository source identity before reusing cached outcomes. Source identity
  conservatively includes transitive code, fixture and configuration inputs;
  task transitions, runtime reports and guidance alone do not invalidate it.
- The writer emits a stable owner-decision request only after integration.
  `blocked-promoter-owner-decision` owns `askOwnerSteps` on a separate
  `repository: none` follow-up, then emits a stable resolution for a new writer
  run to apply.
- Tests cover deterministic promotion, owner-decision resume, terminal-task
  rejection, and observable task state. Await-event restart behavior belongs to
  the shared workflow runtime tests.
