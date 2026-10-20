# Builder Workflow

Builder is a business workflow, not a private execution runtime.

- One `autonomy.queue.available` event identifies one dependency-clear `open`
  task with an immutable digest. One event admits one run.
- The definition declares `repository: "write"` and resource
  `task:<taskId>`. Shared runtime owns task-resource exclusivity, sandbox,
  process, ports, commit, integration, recovery, and cleanup.
- Builder validates the admitted task against canonical source state, so its
  own retained task notes do not invalidate recovery, then checks harness
  readiness and runs one build agent. Universal
  repair checks protect target-task authority and independent critic review;
  the agent selects behavior-specific proof.
- Publication composes installed task validation with the selected scope's
  `workflow.validationCommand` from trusted configuration. Configure the command
  in `.kota/config.json` using argv, for example `["python3", "-m", "pytest"]`.
  Missing configuration requires setup; declared failures use runtime integration
  repair. The shared sandbox executes project checks in the reconciled writer.
- A continuation `decompose` decision terminally classifies the builder so the
  existing decomposer can review the immutable task contract, deduplicate child
  identities, and apply task mutations through repo-task operations.
- Its integration policy rechecks the admitted source task against the exact
  canonical snapshot used for the final rebase. Contract drift preserves the
  writer for attention instead of publishing stale work. Publication also
  requires a successful build (including repair checks) and a terminal target
  task in the reconciled writer; skipped builds cannot publish retained diffs.
- Recovery observes task-linked scoped execution and capability exports alongside
  contract and review changes. Collection timestamps, unrelated exports and the
  retained writer's own artifacts do not authorize another attempt. Routine reports
  and copies at new paths are not new evidence; each execution/capability record
  must itself be attributable. Collection uses the shared asynchronous worker
  boundary so retained admission cannot block daemon control. Select scoped
  task-linked run identities and explicit run/export citations before reading
  evidence through the shared anchored batch reader. Recheck canonical task
  intent after collection; non-actionable targets skip evidence export.
- Retained recovery compares the admitted task, critic policy, and linked issue
  revisions with the failed attempt. Automatic retries retain unchanged inputs;
  an explicit retry can reattempt repaired environments without editing task intent.
  Both paths still require an actionable target and compatible ownership. The shared
  runtime reconciles a changed canonical contract under the same resource and
  run identity before fresh execution. The exported `admitted-task.md` is the
  current admitted source; preserve retained task notes and corrections while
  reconciling them against that source.
- Builder never chooses another task and never implements claims, worktrees,
  branches, merge gates, port leases, recovery triggers, or terminal cleanup.
- The task remains `open` while runtime resource ownership marks the active
  builder run. Its terminal transition is part of the isolated change set.
- Tests cover targeted dispatch, resource binding, and build gating. Runtime
  isolation, integration, and recovery are tested by the shared runtime that
  owns those behaviors.
- Builder contributes its immutable task contract, canonical queue revision,
  and priority ordering to the universal continuation boundary. The runtime
  owns decision deduplication and preserve-yield checkpoints; resumed builder
  attempts reuse the same run, sandbox, task resource, evidence lineage, and
  exact next action. Harnesses without managed session resume start a fresh
  agent call against that preserved state.

The agent writes its proposed commit message to
`$KOTA_RUN_DIR/commit-message.txt`. Runtime owns durable run evidence and
publication; builder does not maintain a parallel evidence manifest.
