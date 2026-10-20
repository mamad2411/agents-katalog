# Repo-Tasks Module

Owns KOTA's task-queue domain: task states, path-safe reads and mutations,
actionability, validation, CLI/control operations, and task status/search
projections.

- The domain is the source of truth for state names and for the difference
  between active, actionable, and dispatchable work. Consumers use its typed
  snapshot fields rather than recomputing actionability from raw counts.
  File actionability expresses intent only. Work supply joins that intent with
  canonical runtime resource reservations and distinguishes available, running,
  queued, and retained work. Missing runtime evidence means availability is
  unknown. The final claim remains an atomic runtime operation.
- Active task files live directly under `data/tasks/`; terminal files live in
  `data/tasks/archive/`. In-progress state is a transient projection of active
  builder workflow runs and is never persisted in task frontmatter or paths.
- Task and inbox Markdown are authored directly, including multi-file changes.
  Domain operations are conveniences for deterministic callers and remote UI,
  not an authoring protocol. The shared task integration policy runs the installed
  task validator (additional checks cannot replace it) and checks changed task identities against current runtime
  ownership at publication. Workflows compose their own semantic invariants;
  task-editing agents may use the same validator for repair feedback.
- Task enumeration and reads use the same descriptor-anchored boundary. It
  rejects linked parents and non-regular entries and returns verified content
  snapshots for semantic dispatch and mutation rechecks.
- Workflow callers operate inside the run-provided repository sandbox. The
  workflow runtime owns run admission, logical resources, final index staging,
  commit, integration, and recovery; repo-tasks does not create task claims,
  workflow leases, worktrees, or merge gates.
- Remote client mutations enter through
  `repo-task-mutation-boundary.ts`. They always dispatch the ordinary
  `repo-task-mutation` writer workflow and fail closed when daemon workflow
  authority is unavailable. Direct domain mutation is limited to a writer
  workspace that the existing run-sandbox manager positively reconciles as
  active for the supplied run and canonical scope. The shared runtime supplies
  its sandbox, logical resources, validation, integration, and recovery; the
  module does not create a task claim, lease, worktree, or second lock table.
  Local editors do not need this adapter. Native agents edit their supplied
  writer sandbox; the runtime publishes the complete run, not each file edit.
- The domain mechanically owns identity, safe paths, lifecycle states,
  dependencies, and submitted-content validation. Whether a task outcome is good,
  complete, or supported by proportionate evidence is an agent review decision,
  not a growing set of task-class and artifact-shape gates.
- Tests exercise distinct path-safety, state-transition, authorization, and
  public-projection behavior without pinning source scans, helper order,
  staging mechanics, evidence filenames, or literal catalogs.
- `/api/tasks` and task search are module-owned surfaces. Visual clients and the
  CLI use the shared control/client contract; native agents may inspect and
  edit the underlying Markdown directly.
- `repo-tasks-operations.ts` owns the normalized list collection, dependency
  waiting projection, keyword/semantic search selection, semantic-unavailable
  result, and reindex result. Routes and local clients share those operations;
  routine daemon list/search/reindex transport is generated. The visual
  `/api/tasks` status projection and mutation transforms remain explicit.
- The default search provider ranks verified task content. `tasks-semantic`
  overrides ranking and declares `semanticSearchCapability` when an embedding
  provider is configured; the base provider has no placeholder reindex method.

Directory selection delegates to the shared daemon scope selector. Registered
search providers stay bound to their construction workspace as the live default
changes. Filesystem anchoring is shared infrastructure, not a task protocol.
