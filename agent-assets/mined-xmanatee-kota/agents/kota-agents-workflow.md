# Workflow Runtime

Owns workflow definitions, validation, durable run state, execution, repair,
and publication.

## Run Ownership

- Definitions declare repository access (`none`, `read`, or `write`); writers
  also declare integration validation. Logical resources express domain
  exclusivity without workflow-specific locks.
- `RunStateDatabase` owns durable admission, attempts, resources, processes,
  external effects, and terminal publications. Scope state uses its revisioned
  SQLite API; staged compare-and-set mutations commit atomically with success.
  Project dispatch pause and scope agent backoff live there, with sibling scopes
  isolated. `WorkflowRunStore` and artifacts are evidence, never a second queue
  or shared state store. Only daemon database composition migrates schema and
  removes obsolete operational files; offline readers are explicit and read-only.
- `RunCoordinator` owns capacity, admission pause, cancellation, and child waits.
  Waiting parents release capacity and reacquire it before continuing. Retained
  recovery assessments inherit coordinator cancellation and join its scope and
  shutdown drains without taking execution capacity.
- `RunLifecycle` owns sandbox creation/adoption, resource allocation, execution,
  writer finalization, restart reconciliation, and cleanup.
  Automatic recovery preserves ambiguous missing sandboxes. Explicit cancellation
  may release a missing checkout with no remaining branch or Git registration,
  preserving residual runtime files with the run artifacts; it never completes the task.
- `IntegrationQueue` alone publishes writers: rebase onto canonical head,
  validate, acquire the integration resource, run domain invariants against
  that exact snapshot with fresh scope-state and scope-filtered ownership
  readers, recheck both trees, then fast-forward. Rejection retains the writer.
  Canonical ignored files are operator-owned too; publication must not overwrite
  them when a writer introduces a tracked path at the same location.
- Trusted project preparation runs after reconciliation in the actual writer.
  Setup failures retain that run outside agent source repair. The integration
  journal owns dependency-output promotion and rollback; blocking workers drain
  before canonical dependencies and source change. Project policy owns package
  managers, readiness checks, frozen inputs, relocatable outputs and setup egress.
  Dependency recovery is a Node-builtin-only startup boundary shared with live
  recovery. CLI entrypoints run it before loading packages; it reads the same
  installation-local SQLite run journal without migrations, refuses live publication
  owners, validates outputs against trusted preparation policy and Git, and
  leaves acknowledgement and cleanup to RunLifecycle.
- Conflict and validator repair use bounded AI continuation with screened
  diagnostics, conflict-path write scope, Git mutation denial, cancellation,
  and no-progress fingerprints. Runtime owns staging, commits, rebase, and
  publication. Each repair invocation retains distinct timestamped evidence
  under its original run. Stream only when supported; always retain returned
  results, verification summaries, and measured usage, including on errors or
  cancellation. Agent success still requires validation and publication.
- Workflow owners supply repair continuation's domain contract and judgment.
  Failed continuation judgments propagate through runtime incident/recovery
  handling; only a completed judgment can request an owner decision.
  Core observes semantic boundaries, check evidence, queue revisions, and
  same-scope workspace changes, then owns durable yield/resume. One judgment
  covers a boundary until unresolved attempts grow geometrically, failures
  strictly expand, or diff scope materially expands; volatile churn alone
  never creates a reviewer cadence. Resumable harnesses establish their session
  before checkpoint polling. Preserved runs retain workspaces and resources,
  release capacity, and defer to actually runnable higher-priority work. Blocked,
  deferred or stale work does not become a hard completion dependency. Before
  resuming a yield, loaded definitions resolve fresh resource-bound supply through
  ordinary trigger admission, including after restart; SQLite does not interpret tasks.
- Nested critic, semantic-gate, and continuation judges are filesystem
  read-only; they inspect unpublished work without becoming mutation owners.
  The step context snapshots runtime-selected artifact roots into the existing
  run store and grants bounded files containing only verified selected projections,
  never a directory containing unselected evidence. Disposable compiled trees
  belong in run temp; review roots retain the selected verification outputs.
  Large workflow-selected packets use directly granted, content-addressed
  projections so reviewers can page through them; smaller projections share
  bounded review bundles. Explicit current-run file selections must have
  readable projections before launching a reviewer; failed delivery is not a
  substantive verdict.
  Linked snapshots require
  explicit selection and a same-scope run observation. Originals keep exact
  hashes; redacted or unavailable projections never stand in for original bytes.
  Cleanup atomically moves private runtime originals into the existing run store;
  review projection limits or unprojectable test files do not prevent cleanup.
  Failed retention preserves the sandbox. Restart reconciles partial Git cleanup
  against the same retained allocation, without rerunning integrated work.
  Repository publication rejects new or changed run packets; artifacts belong
  under the runtime-provided agent and artifact directories. Historical copies
  may be retired only after their retained replacement has been verified.
- Decomposition terminally classifies the writer through its failed-run
  consumer. The domain module reviews and changes work; core never creates
  child tasks from free-form text.
- `WorkflowQueueManager` adapts triggers to durable admission. Do not add
  parallel queues, task-claim files, workflow-owned worktrees, merge gates,
  process registries, port leases, or recovery side channels.
- Suspended runs retain exclusive resources. Reconciliation and resumption
  enter through their recovery owner; ordinary mutators cannot revise their
  contract. Definitions may assess relevant changes before retained execution;
  runtime atomically reconciles trigger, recovery revision, and dispatch
  identity while preserving resources. Publication journals resume integration
  recovery instead of restarting business execution.
- Discovery-based resource resolvers select work at admission and reuse that
  admitted snapshot on restoration. Queue changes, including the writer's own
  publication, cannot strand publication or cleanup recovery.
- A persisted sandbox that disappears keeps its ownership until Git-backed
  cleanup reconciliation or the runtime publication journal establishes its
  disposition. Missing files and empty historical diffs are not cleanup evidence.
- Completed-outcome observers select artifact candidates against a coherent
  durable run/publication snapshot before reading metadata. Startup and retained
  publication evidence belongs to recovery; historical metadata still needs
  explicit completion after its durable row expires.
- `ctx.runEvidence` provides immutable, scope-filtered observations. Investigators
  receive redacted exports and unavailable diagnostics; database handles and
  host control authority stay in runtime.
- Daemon startup may repair malformed authority-critical or recovered metadata
  only when durable run, `workflow.json`, and `trigger.json` agree. Preserve the
  malformed source; disagreement fails closed. Other terminal history remains
  quarantinable. Dead-letter disposition needs run-specific repair evidence and
  a later successful consumer. Standalone and inspection paths stay read-only.
- Native writer authorization rechecks run, attempt, daemon epoch, and workspace
  per mutation. Sandboxed commands receive fresh boolean responses, never raw
  databases. Request/reply files are transient invocation transport, not durable
  state or reusable approvals.

@step-contract.md
