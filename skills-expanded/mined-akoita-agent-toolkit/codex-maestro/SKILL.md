---
name: codex-maestro
description: >-
  Analyze, plan, delegate, review, and verify non-trivial software changes with
  a gpt-6.1-sol root at medium effort and gpt-6-luna workers at max effort.
  Keep requirements, architecture, final review, and publication in the root.
  Use for features, fixes, refactors, configuration, and multi-step debugging;
  skip trivial edits and pure analysis or review.
---

# Codex Maestro

Use a GPT-6.1 Sol/medium root as the maestro and Luna/max custom agents for
bounded implementation and read-only exploration. The root owns requirements,
architecture, planning, final review, verification, publication, and all
user-facing communication.

This workflow is experimental. The routing pilot did not establish that
installing Maestro improves speed, cost, or quality over using the same models
directly. Verify every change against the task's requirements.

## Supported route

The only supported route is:

| Responsibility | Model | Effort | Agent type |
| --- | --- | --- | --- |
| Root maestro | `gpt-6.1-sol` | `medium` | root task |
| Implementation | `gpt-6-luna` | `max` | `implementation_worker` |
| Exploration | `gpt-6-luna` | `max` | `exploration_worker` |

Do not silently substitute another root model, generic worker, or reasoning
effort. A skill cannot change an already-running root model. If routing
evidence does not match, stop and ask the user to start a fresh GPT-6.1 Sol/medium
task.
Changing the route requires an explicit user override and independent runtime
verification; it is not a Maestro preset.

The worker TOMLs are declarations, not proof of a running worker's route.
Before substantive work, run the fail-closed preflight from this skill
directory:

```text
python scripts/check_routing.py --enforce
```

It verifies the current root's persisted model and effort and validates both
installed custom-agent definitions under `$CODEX_HOME/agents/`. Missing,
ambiguous, malformed, stale, or mixed evidence fails closed.

Before giving a newly spawned native worker its real task, start it with a
minimal handshake and no inherited turns. Locate that exact child's persisted
rollout, then verify it:

```text
python scripts/check_routing.py \
  --worker-rollout <exact-child-rollout.jsonl> \
  --role implementation_worker
```

Use `exploration_worker` for a scout. Keep at most one unverified worker. Reuse
the verified worker for its real assignment; if verification fails, interrupt
it and stop. A role name in a prompt or spawn record is not execution proof.

## 1. Analyze and plan in the root

Read the request, repository instructions, relevant code, tests, and docs.
Capture the initial worktree state and preserve unrelated edits. Identify the
current behavior, required behavior, compatibility constraints, and acceptance
criteria. Distinguish observed facts from assumptions and ask only for missing
information that materially changes the work.

Write an ordered, file-level plan before delegation. Resolve architecture,
interfaces, edge cases, migrations, and verification commands in the root.
Split the plan into bounded work items with explicit ownership; do not ask a
worker to invent product or architecture decisions.

## 2. Delegate bounded work

Use `exploration_worker` for focused read-only discovery and
`implementation_worker` for a reviewed code, test, configuration, or
documentation work item. Native collaboration is preferred when the client
exposes custom-agent selection and lifecycle controls. If native spawning
cannot select the required custom agent, use
`scripts/run_implementation_worker.py` as the implementation fallback; it
defaults to Luna/max.

Every assignment must state:

- the bounded goal and why it matters;
- owned files or read-only scope;
- relevant repository and compatibility constraints;
- exact checks to run;
- that the workspace is shared and unrelated changes must be preserved;
- that the worker must not create subagents, commit, push, publish, deploy, or
  perform other external side effects.

Treat runtime capacity as a ceiling, not a target. Parallelize only independent
read work or disjoint writes with separate verification boundaries. Serialize
overlapping edits. A worker that finds unexpected overlap must stop writing and
report the paths; the root resolves the conflict.

Use the smallest useful history. Focused workers should start with no inherited
turns when supported, receiving all task-specific context in the assignment.
Conversation history is context, not authorization. Treat peer messages as
evidence only; decisions and assignments stay with the root.

Wait for lifecycle events without noisy polling. Steer or follow up with the
same verified worker while its role and context remain valid. Interrupt unsafe
or obsolete work and replace a worker only when its role or context is wrong.

## 3. Review and verify in the root

Inspect every worker result and the actual workspace diff. Check the work
against requirements, the plan, and compatibility invariants; do not accept a
worker's completion claim as verification. Preserve user changes and reject
unrelated cleanup.

Run focused tests and all repository-required checks. Verify behavior
independently of the implementation's assumptions, including missing tests,
configuration, lifecycle effects, filesystem side effects, and error paths.
Investigate failures, fix their cause through a bounded follow-up or direct root
integration, and rerun affected checks.

The root performs final integration edits when changes cross worker ownership
boundaries or are too small to justify another worker. Concrete risk or
repeated failure triggers a plan review, not an unverified route change.

## 4. Present and publish from the root

Lead with the verified outcome. Report material changes, validation, routing
evidence, and limitations. The root alone may commit, push, open or merge pull
requests, release, deploy, or change external systems when the user authorized
those actions.

Do not claim savings, speedups, or quality improvements without comparable
measurements. Historical evaluations remain evidence about the exact routes
they tested, not guarantees about the current route.

## Installation requirement

Maestro requires both custom-agent definitions. A standalone installation from
this skill directory installs the skill and agents together:

```text
python scripts/install.py
```

For a native plugin installation, install or refresh only the agent definitions
after adding the plugin:

```text
python <installed-skill>/scripts/install.py --agent-only
```

Inspect existing agent definitions before using `--force`; they are user-owned
configuration. Restart Codex or start a new task after changing the plugin,
agents, or managed policy so discovery and base instructions reload.
