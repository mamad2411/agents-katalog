---
name: orchid
description: Coordinates Orchid spec leases, bud work, and branch-local goal cycles. Use for dispatch, validation, staging, cleanup, or orchid goal runs.
---

# Orchid

Use `orchid` as the control plane from the repository root. Orchid owns leases,
packets, reports, touched-file attribution, staging plans, branch-local goal
state, and `.orchid` runtime state. For spec and bud orchestration, follow JSON
ACKs from the CLI instead of parsing generated Markdown or Git porcelain. For
goal loops, follow the Markdown prompt printed by `orchid goal`; that command is
Markdown-first by design.

At the start of an orchestration run, call `orchid capabilities` once. Follow
the compact `recommended_action` and `argv` returned by `next` and
`report-check`; use `--explain` only when a mayor must interpret an exception.

## Mayor Loop

Think in this loop:

`Observe -> Select -> Lease -> Dispatch -> Ingest -> Verify -> Stage -> Commit/Review -> Close -> Continue/Stop`

Start by observing only the user-authorized scope:

```sh
orchid next --spec SPEC_ID
```

Use `--all-open` only when the user explicitly authorizes work across open
specs. If the authorized queue drains, or `next` returns `blocked` or `done`,
stop and report. Do not broaden scope on your own.

Phase guide:

- `dispatch`: use `next --explain` only when worker-routing detail is needed,
  then spawn the correctly sized worker and create the packet.
- `wait`: wait for the worker or validator to return. Do not poll or ask for
  routine progress while the agent wait is active. If no completion event
  arrives after 15 minutes, run one quiet `orchid status --spec SPEC_ID`;
  return to waiting for another 15 minutes when it remains healthy.
- `validate`: check the report, touched files, and task-specific evidence.
- `repair`: regenerate the worker packet from the failed validator report, then
  dispatch the focused repair worker.
- `stage`: ask Orchid for the staging plan, then stage only returned pathspecs.
- `cleanup`: close completed leases after durable commit/review state exists.
- `recover`: inspect stale leases, release or continue them, or report the blocker.

When runtime state itself is unclear, use the read-only health surfaces before
choosing a mutation:

```sh
orchid doctor
orchid inspect --lease LEASE_ID
```

Treat a `completion-recover` recommendation as an attempt to reconcile a
durable intent, not a guarantee that Orchid can override later task edits. Do
not invent a resource-claim protocol: Orchid leases are the coordination
primitive.

## Command Flow

Inspect before spawning. Use `next --explain` or `ready --explain` only when
the candidate's worker routing is not already known. Normal ACKs are compact;
do not turn routine observation into a diagnostic command chain.

After spawning the worker with those settings, lease and create the packet:

```sh
orchid lease SPEC_ID TASK_ID --owner worker:AGENT_ID --agent-id AGENT_ID --serial
orchid packet --lease LEASE_ID --role worker
```

For a scoped ephemeral delegation without durable spec files, choose the worker
effort before spawning, then pass the same metadata to `bud`:

```sh
orchid bud \
  --title "SHORT TITLE" \
  --scope PATH \
  --instructions PROMPT.md \
  --worker-reasoning-effort medium \
  --agent-id AGENT_ID \
  --serial
```

If the agent id becomes known after lease creation, attach it from the
coordinator and then continue with the lease id returned by status:

```sh
orchid lease-attach-agent --lease LEASE_ID --agent-id AGENT_ID
orchid status --agent-id AGENT_ID
```

Use `agent_id` only for discovery/recovery. Operational commands stay
lease-based.

Do not wait until packet handoff to discover worker effort. `next` and `ready`
are the place to decide which agent to spawn; lease and packet ACKs repeat the
metadata so you can validate the handoff. Spawned agents should receive only the
packet path and report path from Orchid's JSON output, plus
`worker_reasoning_effort` and non-empty `worker_model` when the ACK includes
them. Default absent worker effort to `medium`; raise it before spawning when
the task has architecture, security, migration, concurrency, or
unclear-invariant risk, but do not lower explicit task or user-requested effort.
Tell workers they are not alone in the worktree and may only work or review.
They must not stage files, commit, edit task state, close leases, or take over
final handoff.

Default to `--serial` in a shared worktree. Use `--allow-parallel` only after
checking active leases and confirming the scopes and likely behavior do not
overlap. File-scope disjointness alone is not enough if tasks share generated
state, global config, migrations, or test fixtures.

When a worker returns, ingest the report and verify the claim:

```sh
orchid report-check REPORT_PATH
orchid git-touched --lease LEASE_ID
```

Treat worker reports as claims until validation passes. The mayor owns
attribution judgment: when Git reports an ambiguous path already inside the
frozen scope, inspect `git-touched --explain`, the worker/validator evidence,
and the exact path. If that evidence resolves ownership, complete with
`--accept-attribution <path> --reason "..."`; Orchid binds that decision to the
current content, so a later edit becomes unsafe again. Do not dispatch a
reconciliation worker or build a manifest. Out-of-scope paths,
changed-after-release paths, missing snapshots, and unrecoverable evidence remain hard stops. If validation
fails within scope, regenerate the worker packet with the validator report as
its source so the repair starts from the exact failed criterion.

Use a role-specific packet when delegating validation or review. Pass a
canonical worker report with `--source-report` when the role needs that claim;
do not fabricate a validator handoff from a reviewer or loop-runner report.
Packets and reports are bound to the lease's frozen context revision, so do not
replace them with a newly edited task file during an active lease.

After green validation, complete the lease and ask for the staging plan:

```sh
orchid complete --lease LEASE_ID --verified-by VALIDATOR_OR_MAYOR
orchid git-stage-plan --lease LEASE_ID
```

The coordinator stages only returned pathspecs. Never use `git add .` in a
shared worktree. Follow repo conventions for validation, branch state, commit
messages, signing/signoff, and review. Make the intentional commit yourself,
then run an independent auto-review against the original request, the spec, and
the resulting diff before final handoff.

After commit/review state is durable, close runtime files:

```sh
orchid close --lease LEASE_ID
orchid cleanup --completed
```

### Mayor recovery rule

Do not create a recovery-only worker or validator. The mayor classifies the
existing evidence:

- `preexisting_dirty` only: informational; it must not block an otherwise safe close.
- in-scope `ambiguous`: mayor may accept exact paths with a reason after worker and validator evidence.
- `out_of_scope`, `changed_after_release`, missing snapshots, corrupt runtime state: stop and repair/escalate.
- validator `needs_fix`: regenerate a worker packet with that validator report as source; no new lease is needed.

## Goal Loop

Use `orchid goal` for one measurable, branch-local improvement target where a
repeatable evaluator decides whether to keep, discard, block, or finish each
cycle. Do not model this as a spec lease or legacy `loops/<id>` artifact unless
the user explicitly asks for that shape.

Initialize from the repository root with a metric, direction, minimum delta,
budget, and first hypothesis:

```sh
orchid goal init \
  --goal "SHORT GOAL" \
  --metric METRIC_NAME \
  --direction lower-is-better \
  --min-delta 5 \
  --hypothesis "FIRST HYPOTHESIS" \
  --max-iterations 10 \
  --max-duration 10h
```

Use `--evaluator` when the repo does not use the default `just goal-eval`. The
evaluator must print one JSON object with `status`, `recommendation`, `metric`,
`baseline`, `candidate`, `delta`, and `reason`. Use repeatable
`--protected-surface PATH` for evaluator, fixture, or policy files that should
block automatic keep/discard if changed. Use repeatable `--scope PATH` for
advisory work surfaces.

Run `orchid goal` to advance the loop. If it prints `# Goal Setup`, fix the
evaluator and run `orchid goal` again. If it prints `# Goal Ready` or
`# Goal Running`, implement one focused attempt inside the stated scope, then
write the requested report under `.orchid/goals/<goal-id>/reports/C###.md`:

```md
+++
cycle = "C001"
status = "ready_for_evaluation"
next_hypothesis = "next idea to try"
+++

## Summary

What changed and what evidence was collected.
```

Use `status = "blocked"` when the attempt cannot be evaluated safely. After the
report exists, run `orchid goal` again. Orchid runs the evaluator, appends
measurement/result traces, commits kept candidates as
`goal(<goal-id>): keep <cycle>`, or discards failed candidates by restoring the
baseline while preserving `.orchid/`. Use `orchid goal status` for read-only
state and `orchid goal finish` to stop without creating a pull request.

## Guardrails

- Stay inside the scope the user authorized.
- Clarify scope, dispatch order, review expectations, or final handoff before
  leasing when they are unclear.
- Do not hand-edit `.orchid` runtime files or task state during routine work.
- Do not read generated packets during normal orchestration; packets are
  worker/validator input, and ACKs carry the coordinator details, including
  worker execution metadata.
- Workers and validators may read packets, repo code, and reports, but they
  must not stage, commit, edit task state, close leases, or own final handoff.
- Goal attempts may be implemented directly by the coordinator or delegated as
  scoped work, but only `orchid goal` owns the keep/discard/done/block decision.
- Account for active leases before dispatching, staging, or cleaning up.
- Inactive spec folders are not dispatchable: `DRAFT-*`, `TBD-*`, `MANUAL-*`,
  `DONE-*`, or exact `DRAFT`, `TBD`, `MANUAL`, `DONE`.
- Keep `.orchid` ephemeral. Close or clean completed runtime files once commit
  and review status are recorded.
- Ignore unrelated dirty worktree changes and never revert user work.

## Done

Stop when the authorized queue is done or blocked, all validated work has been
completed through Orchid, approved pathspecs are staged and committed by the
coordinator, independent review has run, and completed runtime files are closed
or cleaned.
