# Progress Reviewer Workflow

This workflow owns cross-run systemic operational and product learning.

- Collect structured evidence first, then let the reviewer assess it.
- Automatic reviews consume a pinned, coalesced evidence window. Changed outcomes
  and owner feedback need not wait for an empty builder queue; delivery-only
  reflection uses spare capacity. Compare delivery, repair and review outcomes; source
  growth and elapsed time alone do not justify work. The agent decides evidence
  sufficiency for the proposed decision and can choose no action.
- Retain baseline/current outcome summaries with scoped raw references. Follow
  generated interventions through canonical task state, integrated changes and
  later outcomes that may disprove the original hypothesis. The default compact
  packet prioritizes the pinned comparison summary over individual raw references.
- Select current outcomes and prior interventions together, reserving manifest
  coverage across runs before diagnostic files. Canonical state details travel
  through redacted review projections, never agent access to operational stores.
- Publish cited architecture/guidance handoffs through the existing semantic
  publication transaction, preserving the shared improvement topic key. The
  receiving owner applies its own evidence and authority rules. Handoff evidence
  identity excludes admission revisions and citation order; scoped file content
  is pinned at collection. Carry that identity to the receiver independently of
  the shared topic and run-artifact provenance. While the topic's task is open
  or blocked, retain the handoff and its references as pending across task
  updates and unrelated reviews. A newer resolution or owner-question
  disposition cancels the topic's pending handoff; publication reconciles
  remaining handoffs against task completion before consuming them. Dispatcher
  invokes the same reconciliation on idle, so release does not require a new
  review. Both owners stage receipts with delivery in the runtime transaction.
- Consume each automatic semantic input revision once. Automatic requests use
  their own latest-only event slot, while the explicit request event is
  lossless, so owner/system requests cannot replace or be replaced by a
  superseded automatic revision.
- Reject consumed automatic revisions through the workflow's canonical
  `triggerAdmission` watermark before durable run admission. The watermark is
  one runtime state row; `RunStateDatabase` owns queued work and
  delivery-attempt keys own replay dedupe.
- Treat the complete current open queue, anchors, dependencies, durable issues,
  durable run state, and owner decisions as canonical state. Recent terminal
  task history can add context but must not stand in for queue truth.
- Bind runtime-authored evidence to its pre-agent digest. The reviewer receives
  a machine-enforced per-run `agent-output/` directory while sibling evidence,
  step state, and run metadata remain runtime-owned inputs rather than
  agent-authored authority. Its project write scope is `deny-all`.
- Keep the reviewer evaluative: it may create normal follow-up tasks or owner
  questions, but it must not directly mutate product code.
- Every review artifact must state its scope, trigger kind, evidence window,
  included evidence, excluded evidence, and applied actions.
- Dedupe before creating tasks or owner questions so recurring reviews do not
  spam the queue. Publication records explicit source runs independently of
  the automatic watermark. Per-topic observations preserve newer dispositions
  while allowing out-of-order explicit requests about unrelated topics.
- Validate citations against the collected evidence inside the agent contract.
  Exhausted output correction retains a typed rejection and finishes with
  warnings, without actions or proposal publication. It consumes the rejected
  automatic revision through runtime compare-and-set so changed evidence can
  open a later window without replaying exhausted correction. Runtime and evidence
  integrity failures remain terminal.
- Reconcile generated tasks and owner questions through the shared proposal
  lifecycle when canonical state disproves their premise.
- Stage task changes and semantic publication evidence in the writer run.
  Owner-question reconciliation and the consumed semantic watermark publish
  in the original run's shared success finalizer, using compare-and-set against
  the latest runtime state row. A failed finalizer retains the original run for
  recovery without repeating agent work.
- A consumed review watermark does not cancel paired owner effects for an
  integrated task change. Publication reconciles against canonical task state
  and the retirement disposition recorded in archived tasks, so delayed effects
  complete without undoing a later disposition.
