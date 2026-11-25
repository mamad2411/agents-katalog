---
name: kanban-worker-operations
description: "Use when operating or debugging Hermes Kanban workers."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [hermes, kanban, workers, dispatch, troubleshooting, operations]
    related_skills: [hermes-agent, systematic-debugging]
---

# Hermes Kanban Worker Operations

## Overview

Hermes Kanban is a durable multi-worker queue. A card's column, a worker run's outcome, and the underlying provider/tool health are related but distinct signals. This skill provides a repeatable operating procedure for dispatch, incident diagnosis, guarded recovery, and end-to-end verification.

The central discipline is:

> **Classify the latest run before changing the card.**

Do not equate `blocked` with crashed, historical failures with current health, or a worker's final prose with a valid terminal Kanban transition.

For the compact red-to-green incident pattern that motivated this workflow, read `references/incident-recovery-pattern.md`.

## When to Use

Use this skill when:

- Kanban cards are `ready` but no worker starts.
- A dashboard or failure feed makes the queue look broadly broken.
- Workers exit without calling `kanban_complete` or `kanban_block`.
- A model, provider, profile, skill, credential, or launcher problem may be affecting workers.
- You need to retry failed workers without duplicating completed work.
- You need to determine whether a block is genuine HITL or a technical failure.
- Completing one card may promote or dispatch dependent cards.
- You are designing or validating an intake-to-worker queue.

Also load the domain skill attached to the cards: email, GitHub, finance, browser operations, and so on. This skill governs the worker runtime and queue, not the card's business policy.

Do not use this as a reason to bypass approvals or turn a genuine review requirement into an autonomous action.

## Mental Model

Treat a Kanban incident as five layers:

1. **Card state** — `todo`, `ready`, `running`, `blocked`, `done`, etc.
2. **Run state** — `completed`, `blocked`, `crashed`, `spawn_failed`, `timed_out`, or still running.
3. **Worker protocol** — the worker must finish with a terminal Kanban tool call.
4. **Execution configuration** — profile, provider/model override, attached skills, workspace, tools, and credentials.
5. **Dispatch control** — dependency promotion, claim locks, failure counters, cooldowns, and respawn guards.

A visible symptom at one layer may originate at another. For example, a provider error can occur before the first tool call, while the dispatcher only sees a clean process exit and reports a protocol violation. Read the worker log before accepting the wrapper error as root cause.

## Core Invariants

### Card status is not run outcome

- `blocked` with `outcome=blocked` and `error=null` is usually an intentional HITL or external-dependency result.
- `done` with `outcome=completed` and `error=null` is a successful terminal run even if older attempts crashed.
- `ready` does not guarantee spawnability; a guard may defer dispatch.
- A card can have many historical runs. Use the **latest** run for live health, then inspect history only to explain recurrence.

### Terminal protocol matters

A dispatched worker must call `kanban_complete` or `kanban_block`. A text-only final answer does not transition the card. If the worker exits without a terminal call, determine whether it:

- chose prose instead of the protocol;
- lost tools or task context;
- encountered a provider/model failure before tool use; or
- was terminated externally.

### Skills are explicit execution inputs

Kanban workers do not inherit the parent chat's loaded skills merely because the parent used them. Attach required skills to the card/task. A worker loads its pinned skills when the worker session starts; edits made after startup do not rewrite that running prompt.

### Recovery is scoped

Failure guards are generally scoped to a task/profile execution path. Fix the actual provider/profile/launcher issue first, then perform an explicit supported recovery action. Resetting state without fixing the cause only creates another failure loop.

### Completion can cascade

Completing a parent can promote a child, and a gateway dispatcher may claim that child immediately. Final verification must therefore include a second board-wide pass after every repaired card reaches a terminal outcome.

## Operating Procedure

### 1. Freeze queue growth and capture live state

Do not enqueue more work while the execution path is untrusted. Capture board health before mutating anything:

```bash
hermes kanban --board <board> stats
hermes kanban --board <board> diagnostics --json
hermes kanban --board <board> list --json --sort created-desc
```

Record:

- counts by card status;
- cards currently `ready` or `running`;
- diagnostics;
- assignees and model overrides;
- which cards belong to the workflow under investigation.

**Completion criterion:** the suspect population is bounded by task IDs or a deterministic metadata field such as `created_by`; unrelated cards are separated.

### 2. Reduce runs before reading logs

For each suspect card, inspect run history:

```bash
hermes kanban --board <board> runs <task-id> --json
```

Build a compact table with:

- task ID and title;
- current card status;
- latest run ID;
- latest run outcome and error;
- count of historical crashes/spawn failures;
- latest summary.

Classify each latest run:

| Latest evidence | Classification | Next action |
|---|---|---|
| `completed`, `error=null` | Success | Do not retry |
| `blocked`, `error=null` | Candidate HITL/external dependency | Read summary and policy |
| `crashed`, `spawn_failed`, `timed_out`, or non-null error | Technical | Investigate |
| `running` with recent heartbeat | Active | Monitor, do not duplicate |
| `running` without heartbeat / expired claim | Stale candidate | Use diagnostics/reclaim path |
| `ready`, but dry-run will not select it | Guarded/nonspawnable | Inspect dispatch controls |

Do not begin by searching every log for the word `error`; email bodies, source code, and old attempts create false positives.

**Completion criterion:** every suspect card is assigned exactly one live classification based on its latest run.

### 3. Build a tight dispatch repro

For `ready` cards, use dry-run as the red-capable feedback loop:

```bash
hermes kanban --board <board> dispatch --dry-run --max <n> --json
```

Interpret the result precisely:

- Expected task appears in `spawned`: the dispatch path is selectable.
- Task appears in a skip bucket: investigate that explicit reason.
- Task is `ready` but appears nowhere: inspect diagnostics, assignee/profile validity, claim state, and stored failure/guard state.

Do not run a real dispatch until the dry-run selects the exact intended cards and no unrelated card.

**Completion criterion:** one command reliably shows red before recovery and can show green afterward.

### 4. Trace the first real failure

Inspect the latest failed run and worker log:

```bash
hermes kanban --board <board> show <task-id> --json
hermes kanban --board <board> log <task-id>
hermes status --all
```

Trace from the earliest failure in the worker session, not the dispatcher's final wrapper. Check, in order:

1. Did the model/provider initialize?
2. Did the worker receive the task ID and board?
3. Did attached skills load?
4. Was the first Kanban tool call made?
5. Did the required domain tool initialize?
6. What was the last successful heartbeat/tool call?
7. Did the worker make a terminal Kanban call?

Compare a failed card with one recent successful card using the same profile. A known-good run proves more than a generic health command.

**Completion criterion:** the root cause is stated as a falsifiable execution difference between failed and working paths.

### 5. Fix the execution path before clearing the guard

Examples of root-cause fixes include selecting a supported model/provider pair, restoring a profile's auth, attaching the missing skill, or correcting the worker launcher configuration. Use live help and official Hermes docs because Kanban recovery verbs evolve:

```bash
hermes kanban --help
hermes kanban set-model --help
hermes kanban assign --help
hermes kanban unblock --help
```

If a task needs a model override:

```bash
hermes kanban --board <board> set-model <task-id> <model> --provider <provider>
```

Choose a model/provider pair proven by a recent successful worker, not merely one that appears configured.

**Completion criterion:** the broken dependency succeeds independently or matches a recent known-good worker configuration.

### 6. Perform a supported recovery transition

Prefer a dedicated reset/retry command if the installed Hermes version provides one.

For a `blocked` task, `unblock` is the normal deliberate retry boundary:

```bash
hermes kanban --board <board> unblock <task-id>
```

For a `ready` task held by stale task/profile failure state, a deliberate reassignment is the supported recovery pattern on Hermes versions where the guard is task/profile-scoped:

```bash
hermes kanban --board <board> assign <task-id> none
hermes kanban --board <board> assign <task-id> <known-good-profile>
```

Reassigning to the same profile without changing away first may preserve the failure state. Do not edit the Kanban SQLite database directly unless developing Hermes itself with a backup and regression test.

Immediately rerun the dry test:

```bash
hermes kanban --board <board> dispatch --dry-run --max <n> --json
```

**Completion criterion:** failure state is cleared, the intended task is selected, and the corrected profile/model is visible before real dispatch.

### 7. Dispatch narrowly and monitor to a terminal outcome

Dispatch only the repaired population:

```bash
hermes kanban --board <board> dispatch --max <n> --json
```

Monitor card state, latest run, heartbeat, and log. A long-running worker with current heartbeats is not crashed. Do not spawn a duplicate merely because it exceeds an informal estimate.

Valid terminal outcomes:

- `done` / `completed` / `error=null`;
- `blocked` / `blocked` / `error=null`, with a concrete business, approval, or external-dependency reason.

Invalid completion signals:

- prose says "done" while the card remains `running`;
- process exited but no terminal run outcome exists;
- task returns to `ready` with a new failure error;
- a technical dependency failure is presented as a business decision.

**Completion criterion:** every retried run has ended via the Kanban protocol or remains actively heartbeating with an explicit reason to continue waiting.

### 8. Follow the dependency cascade

After each terminal outcome, re-run:

```bash
hermes kanban --board <board> stats
hermes kanban --board <board> diagnostics --json
hermes kanban --board <board> list --json --sort created-desc
```

Look for newly promoted `ready` cards and newly claimed `running` cards. Monitor any auto-dispatched child to its own terminal outcome. A repaired parent is not the end of the incident if it unlocks downstream work.

**Completion criterion:** no unexpected `ready` or `running` cards remain, or each remaining active card is explicitly accounted for.

### 9. Report technical health separately from HITL

Give two independent summaries:

1. **Runtime health:** latest run errors, crashes, guarded tasks, diagnostics, and active workers.
2. **Business queue:** intentional blocks, decisions, approvals, and external dependencies.

Never inflate technical failure counts by including valid HITL blocks. Never hide a technical access/tool problem inside an HITL list.

A strong final proof includes:

- diagnostics result;
- `ready` and `running` counts;
- latest outcomes and `error` fields for repaired runs;
- domain-workflow counts filtered by deterministic metadata;
- any dependent card promoted during recovery.

## Common Failure Shapes

### Provider failure wrapped as protocol violation

**Shape:** worker log shows provider/model initialization failure, while the dispatcher reports a clean exit without a terminal Kanban call.

**Response:** treat the provider error as root cause, prove a working provider/model pair, update the execution configuration, clear stale guard state, then rerun the dry dispatch loop.

### Historical failures dominate the dashboard

**Shape:** many failed run records exist, but current cards are already `done` or intentionally `blocked`.

**Response:** aggregate by latest run per task and scope by workflow metadata. Historical runs remain useful audit evidence but are not live incident counts.

### Ready card silently omitted by dispatch

**Shape:** card status is `ready`; dry-run does not select it and may not list a normal skip reason.

**Response:** inspect diagnostics, assignee/profile validity, claim state, latest failure, and respawn guard state. Fix the execution path, perform a supported recovery transition, and require dry-run green before real dispatch.

### Technical failure mislabeled as HITL

**Shape:** worker could not access a required tool, model, skill, or credential and blocks as though the user owes a business decision.

**Response:** separate technical blockers from policy-required approvals. Repair and retry technical failures. Reserve HITL for decisions or actions that genuinely require the user.

### Parent succeeds and a child immediately runs

**Shape:** final board stats change after the repaired task completes.

**Response:** this is dependency promotion, not regression. Monitor the child and include its outcome in end-to-end verification.

## Common Pitfalls

1. **Delegating board mutation to a `delegate_task` child.** Hermes deliberately blocks Kanban initialization/mutation in delegated child contexts (the CLI may return `delegate_task child contexts cannot mutate Kanban tasks or boards`, including on commands that initialize the board connection). Perform board creation/reconciliation in the parent/orchestrator context or a dispatcher-spawned Kanban worker with the dedicated `kanban_*` toolset; do not bypass the guard through SQLite or an alternate API.
2. **Counting run records instead of affected tasks.** One card can contribute many crashes. Report both task count and run count.
3. **Treating every `blocked` card as broken.** Inspect `outcome`, `error`, summary, and governing policy.
4. **Reading all logs before reducing the population.** First group by latest run; then inspect only representative failed and successful logs.
5. **Resetting state before fixing the cause.** This creates a retry loop and destroys diagnostic clarity.
6. **Reassigning to the same profile and assuming it reset.** Use an explicit away-and-back transition when that is the installed version's supported recovery mechanism.
7. **Editing SQLite by hand for an operational incident.** Prefer CLI transitions that preserve events and invariants.
8. **Stopping after the original retries finish.** Parent completion may auto-dispatch children.
9. **Growing the queue during runtime uncertainty.** Freeze intake until the worker path has a verified terminal success.
10. **Claiming skill inheritance.** Required skills must be attached to the task; parent-chat skill state is not evidence.
11. **Declaring success from prose.** Verify the durable card state and latest run row.

## Verification Checklist

- [ ] The affected workflow is scoped by task IDs or deterministic metadata.
- [ ] Every suspect card is classified from its latest run, not dashboard appearance.
- [ ] A tight dry-run repro went red before recovery and green afterward.
- [ ] The first underlying worker error was identified; wrapper errors were not mistaken for root cause.
- [ ] A recent successful worker established a known-good profile/provider/model path.
- [ ] Required skills are explicitly attached to cards.
- [ ] Recovery used supported Kanban transitions, not direct production database edits.
- [ ] Retries ended with `completed` or intentional `blocked`, with `error=null`.
- [ ] Newly promoted or auto-dispatched children were monitored.
- [ ] Final diagnostics were run.
- [ ] Unexpected `ready` and `running` cards are zero or explicitly accounted for.
- [ ] Technical health and business HITL were reported separately.
