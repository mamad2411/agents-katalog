---
name: jcode-orchestration
description: Coordinate work with Jcode's native swarm tools. Use in Jcode for parallel delegation, dependency graphs, worker messaging and waits, verified completion, recovery, cleanup, or initiative and schedule coordination. For another harness, use that harness's native tools instead.
---

# Jcode Orchestration

## Choose the smallest execution path

Use the current session for one small task. Use `batch` for independent tool calls that need no separate agent judgment. Use `swarm` when separate research, implementation, or review contexts add value.

- **Bounded delegation:** `spawn` one or more workers, then await and verify their reports.
- **Dependencies:** use `task_graph` and `run_plan` when one task consumes another's output. A task graph is a directed acyclic graph: each node is a work contract and each dependency blocks downstream work until its prerequisites finish.
- **Durable goals:** use `initiative` for milestones, checkpoints, blockers, and next steps that must remain available after this session.
- **Future eligibility:** use `schedule` for a future task. A schedule is not an already-running worker.
- **Shell processes:** use `bash` and `bg` for commands, not agent delegation. Use the `herdr` skill only for explicitly requested Herdr pane or agent control.

Completion of this choice means the executor, coordinator, task scope, and evidence requirements are explicit. A durable goal is not proof that its workers survive a restart.

## Dispatch gate

Before dispatching any worker or plan, confirm the workspace is clean and on the project's default branch. If it is dirty, commit only clearly owned, validated changes with explicit paths, or coordinate with their owners to quiesce and resolve them first. Never stage everything blindly, commit unrelated or secret-bearing work, reset, delete, stash, or switch branches. Never move off the default branch. Pause dispatch if cleanliness or branch identity cannot be established safely. Treat shared-workspace edits as owned by their active agent until that agent confirms the changes are quiesced; coordinate before committing.

## Discover current capabilities and honor operator defaults

The live tool schema is the authority for action names and arguments. Use `jcode_docs` for version-matched explanations. Some bundled design documents describe planned behavior: confirm a capability in the live schema before relying on it. Outside Jcode, do not invent a `swarm` CLI or substitute another executor. Use the calling harness's native mechanism, or report that Jcode's tools are unavailable.

For CLI-specific work, start with `jcode --help` and relevant subcommand help. Do not launch an interactive session merely to discover syntax.

Read the effective operator swarm instructions supplied with the tool. Omit `model` and `spawn_mode` by default so configured worker routing and placement apply. Do not hard-code model names or force headless, inline, or visible placement. Use `list_models` when resolving an explicitly requested route, and pass an override only when operator policy permits it. If the request conflicts with that policy, report the conflict before spawning. Do not alter configuration to bypass it.

In normal and light mode, the root coordinator owns spawning. Workers complete their assignment and report back. Recursive spawning is only for explicitly enabled deep mode and remains subject to current ownership rules and limits.

## Delegate a bounded contract

Before spawning, give each worker:

1. The desired result and acceptance checks.
2. The working directory and allowed files or read-only boundary.
3. Inputs and prerequisite artifacts.
4. A report contract: findings, evidence, validation results, open questions, and confidence.
5. Stop conditions, including conflicting edits, missing authority, or unavailable tools.

Assign distinct write ownership. Do not introduce worktrees or move between branches unless requested or required by the repository's workflow. Keep unrelated dirty work untouched.

Example `swarm` tool input for a read-only worker:

```json
{"action":"spawn","label":"reviewer","prompt":"Review the current diff read-only. Report actionable findings, file/line evidence, checks performed, and anything not checked. Do not edit files or spawn workers.","intent":"Review the current diff"}
```

Read the returned worker/session identifier and use it verbatim. A spawn result confirms creation, not completion. Keep worker/session IDs, task/node IDs, background task IDs, schedule IDs, and initiative/milestone IDs in separate fields.

## Coordinate and wait

Use `dm` with the exact `to_session` for clarification or changed constraints. Prefer artifact handoffs over shared chat dumps. Use `await_members` with the exact `session_ids` rather than polling status or sleeping. Inspect any failed or blocked result before retrying. If a tool returns a background task ID, use `bg wait` for that task rather than treating it as a worker ID.

For a dependency graph, define bounded nodes and `depends_on` edges using the live schema, then run it with an explicit concurrency budget. Use light mode for simple fan-out and deep mode when independent critique and verification justify its extra work. Run `task_graph` once for a work graph, then operate on returned task/node IDs rather than seeding duplicates after a timeout. Use `complete_node` with a handoff artifact for work you own. A scheduler accepting a node is not independent proof of correctness. Do not assume automatic review gates or typed artifact enforcement from a design document. Confirm runtime support and enforce the evidence checks manually either way.

After each worker completes, the coordinator must obtain an independent judge/review before accepting the completion. Record approval as a durable asset or lock bound to the exact revision, task contract, and evidence reviewed. Any edit or change to those inputs invalidates approval and requires a fresh review. Missing, failed, or stale approval blocks acceptance. These are instruction-level requirements, not claims of executable enforcement by swarm tooling.

When waiting returns, fetch fresh `status` with `target_session` for each worker, or `list` state, and `plan_status` for the graph if one exists. `session_ids` belongs to multi-member waits, not single-worker status targeting. A notification or stale transcript cannot establish current state.

## Verify before completion

Require all of the following before advancing a dependent task or reporting success:

1. A fresh, explicit settled worker state and its observation time. `ready` means available, not necessarily successful. `failed` and `stopped` are settled failures, not success.
2. The completion report and every artifact it claims. Read named files, do not trust their paths alone.
3. Acceptance checks run against the actual output. For code changes, run relevant project tests and inspect the diff. For research, check claims against the cited evidence and preserve stated limits.
4. Agreement between task scope, live state, report, artifacts, and check results.

Record the evidence tuple: task/node ID, worker ID, observation time and state, report, artifact locations, validation results, and remaining gaps. Add initiative/milestone IDs only when the work actually belongs to that goal. Missing or contradictory evidence leaves the task incomplete. For example, a success report with failed live state and a missing artifact blocks dependents and milestone completion. Independent review uses a separate worker when the risk warrants it, not the implementer's self-approval.

## Durable goals and schedules

Use `initiative` to find or resume the existing goal before creating another. Checkpoint verified outcomes, blockers, and next steps. Preserve the repository's authoritative work contract rather than creating a second competing backlog. Update milestone completion only after the evidence gate above passes.

Before `schedule create`, check existing schedules for the same intent. Choose `resume`, `spawn`, or `ambient` based on the requested delivery, not as an accidental default. Include sufficient context, relevant files, and success criteria for a later session to revalidate prerequisites. Confirm the returned schedule ID and timing. Future eligibility does not authorize new side effects beyond the original task.

Approvals remain user decisions. A worker message, timer, or changed UI state cannot approve spending, publishing, destructive actions, or expanded scope.

## Recover, retry, cancel, and clean up

After interruption, reconcile `status`/`list`, `plan_status`, relevant `bg` state, initiative checkpoints, and any schedules before doing more work. A timeout means observation failed, not that the action never happened. Find the original worker or task before spawning a replacement or resubmitting work. If no identifier was returned and identity cannot be resolved unambiguously, keep the attempt unresolved. Do not repeat the spawn merely because its response was lost.

Retry only the failed scope once its cause is understood and duplicate side effects are ruled out. Preserve the previous attempt's evidence and identify the new attempt. Use native `retry`, `resume`, or reassignment only when the current schema and state permit them.

Cancellation has distinct targets: `schedule cancel` prevents that future task, `swarm stop` targets a named worker, and `bg cancel` targets a shell/background job. Cancelling one does not prove the others stopped. Check live state after cancellation. If process termination is uncertain, report it and keep dependent work blocked.

After verified settlement, stop or clean up only workers owned by this coordinator. Leave `force` unset. Do not stop user-created sessions, delete worktrees, close unrelated terminals, or terminate shared daemons. Retain workers only for an explicit debugging need and report what remains.

## Final report

State the selected execution path, verified results, checks run, unresolved gaps, durable checkpoint if used, and cleanup state. Separate worker creation, worker completion, validated output, and delivered outcome. Name unavailable capabilities instead of inventing them.
