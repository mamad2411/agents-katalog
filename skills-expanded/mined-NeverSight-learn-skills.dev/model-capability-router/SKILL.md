---
name: model-capability-router
description: Use when routing Codex work by topology, model, reasoning effort, role, lifecycle, or proof bar across the current task, native subagents and fleets, delegated user-owned subtasks, independent parallel user-owned tasks, and reusable Terra field coordinators. Covers master orchestration, Sol High planning, Luna fleets, task versus subtask decisions, overrides, reuse, steering, waiting, fallback, and Max/Ultra gates.
---

# Model Capability Router

Choose the smallest topology and cheapest compute that can meet the proof bar.
The preset is operator policy; current channel metadata is preflight; a successful
native call is runtime truth. UI badges are never routing evidence.

## Route

1. Locate the nearest operator-approved schema 3 preset. In the operator's
   installation, bundled `assets/vitor-opinionated.toml` is the coherent
   baseline. Treat any external copy as a compatibility mirror only when its
   schema and checksum match. Other bundled presets remain examples until adopted.
2. Classify topology before selecting compute:
   - `single`: keep the work in the user-facing master task;
   - `direct_subagent`: delegate one bounded contract to one native child;
   - `direct_fleet`: let the current master command independent native workers;
   - `field_coordinator`: create or reuse a Terra coordinator for a project or ticket;
   - `field_fleet`: let that coordinator command independent native workers;
   - `delegated_subtask`: create or reuse a user-owned task that works for a
     named master or coordinator;
   - `parallel_task`: create or reuse an independent user-owned task in the same project;
   - `max_single`: one operator-authorized, unusually hard non-parallel problem;
   - `ultra_auto`: operator-authorized automatic multi-agent execution.
   A delegated or parallel user-owned task may be `ephemeral` or `reusable`;
   field coordinators remain reusable. Lifecycle does not determine whether a
   task is logically delegated or independent.
3. Keep platform relationship separate from logical relationship:
   - native subagents and Fleet workers are real children;
   - every `create_thread` result is a platform peer and user-owned;
   - in the operator's nomenclature, a platform peer working for another task
     is a `subtask`; an autonomous peer in the same project is a normal `task`.
4. Select role and compute independently. The preset supplies defaults, not
   immutable bindings:
   - Spark for tiny deterministic work when the channel exposes it;
   - Luna Medium for bounded volume and exploration;
   - Luna High for bounded logic, synthesis, and mechanical debugging;
   - Luna XHigh for bounded coding or deep batches;
   - Terra Medium for persistent field coordination;
   - Sol Light (`low` in TOML) for difficult root-cause debugging;
   - Sol Medium for the master loop, difficult implementation, and substantial planning;
   - Sol High for the `planner`, review, audit, security, and release gates.

   Start lower and increase only after fresh evidence shows the proof bar is not
   being met. Prefer vanilla selection when no role, proof, cost, or lifecycle
   requirement justifies pinning. Do not turn changing benchmark scores into
   durable routing law; use current vendor evidence for benchmark-sensitive decisions.
5. Inventory the exact channels used by the selected topology:
   `current_task`, `spawn_agent`, and/or `create_thread`. Inventory current
   native controls, relevant skills, and custom role files. Role templates under
   `assets/agents/` intentionally omit model and effort so explicit route
   selection can use any model/effort the runtime supports. A role file that
   pins either field must agree with the route.
6. Resolve with Python 3.11 or newer. On Windows use `scripts\route.cmd`.

Planner:

```bash
python3 scripts/route.py resolve \
  --preset <preset.toml> \
  --route direct_subagent \
  --role planner \
  --channel-model spawn_agent=gpt-5.6-sol \
  --available-tool spawn_agent \
  --available-tool followup_task \
  --available-tool send_message \
  --available-tool wait_agent \
  --available-tool list_agents \
  --available-tool interrupt_agent \
  --agent-root <codex-home>/agents
```

Sol-managed Luna Fleet:

```bash
python3 scripts/route.py resolve \
  --preset <preset.toml> \
  --route direct_fleet \
  --fanout 3 \
  --runtime-capacity 8 \
  --active-subagents <live-count> \
  --channel-model current_task=gpt-5.6-sol \
  --channel-model spawn_agent=gpt-5.6-luna \
  --available-tool spawn_agent \
  --available-tool followup_task \
  --available-tool send_message \
  --available-tool wait_agent \
  --available-tool list_agents \
  --available-tool interrupt_agent \
  --agent-root <codex-home>/agents
```

Pass every required control actually exposed by the session. For a user-owned
task also pass `create_thread=<model>` and the task controls. Pass
`--existing-task-id <id>` only after live inspection proves project, purpose,
ownership, logical relationship, parent when delegated, and lifecycle match.
Then pass `--reuse-verified`. Every delegated user-owned route also requires
`--logical-parent-id <id>`; an independent `parallel_task` must not receive one.
Use `--model`, `--effort`, `--worker-model`, or `--worker-effort` only when the
current channel inventory proves the override.

For `field_fleet`, first create or reconcile the reusable Terra task with
`field_coordinator`. Resolve `field_fleet` only as a second stage, passing its
verified task ID, `--reuse-verified`, its logical parent ID, and a fresh
`--coordinator-receipt <json>` produced from live task readback. The receipt
binds the Terra identity, role, worker role, controls, models, capacity, active
children, parent, lifecycle, verification method, and observation time. The
master's inventory and free slots do not prove the coordinator's Fleet capability.
The preset owns the maximum receipt age; callers may request a smaller window
but cannot enlarge it. The receipt is a structured caller-supplied attestation,
not a platform signature, so `proof_state` remains `not_started`.

7. Follow the resolver result:
   - `preflight_ready`: routing inputs are coherent, but `proof_state` remains
     `not_started`; execute once and collect the required native/runtime proof;
   - `needs_authorization`: stop at the named current-user gate;
   - `blocked`: do not silently substitute a channel, relationship, role, model, or task.
8. Attach owned scope, expected output, proof, and stop condition to every
   delegation. Reconcile required results before reporting closure.

Read [orchestration-contract.md](references/orchestration-contract.md) before
creating, reusing, steering, waiting on, or ending a Fleet, field coordinator,
delegated subtask, or parallel task.

Before replacing a schema 2 installation, follow
[schema-3-migration.md](references/schema-3-migration.md). Do not update the
resolver, preset mirror, routing caller, or role assets as unrelated independent
changes.

When a gstack skill owns the workflow, also read
[gstack-compatibility.md](references/gstack-compatibility.md). Preserve gstack's
phase order, artifacts, dual-voice degradation labels, STOP points, and human
gates; use this router only to choose compute and topology for a bounded phase.

gstack is an optional overlay. Native routing is the default and never requires
gstack. Select `--workflow-owner gstack --workflow-phase <phase>` only when a
gstack skill owns the current workflow; then inventory `gstack` and pass the
required plan, repository, revision, scope, test, or target artifacts with
`--context-artifact KEY=VALUE`. The resolver enforces the phase/topology/role
matrix. An independent parallel task may run its own gstack loop, but remains
outside its creator's gstack hierarchy.

## Fleet Rules

- Use only independent workstreams with explicit ownership and proof.
- Start with two or three workers. The approved ceiling is eight spawned
  subagent threads, excluding the primary task; capacity is not a target.
- Before each expansion, reconcile the live runtime ceiling and active spawned
  children. Effective fan-out is the smallest of requested fan-out, the
  approved ceiling, and currently free slots. Zero free slots blocks the route.
- Keep workers as direct children. They never spawn further agents.
- Prefer `fork_turns="none"` or a small bounded positive value. Do not clone
  the full conversation into every worker.
- Reuse an idle native child with `followup_task` during the current lifecycle;
  otherwise spawn only the missing workstream.
- Wait for required workers, reconcile conflicts, and interrupt unnecessary work.
- Escalate only the failed or ambiguous workstream to Terra or Sol; do not
  upgrade the whole Fleet automatically.

## Authority Gates

`create_thread` creates a user-owned platform peer. Use it only when the user
explicitly asks for a new task in the current request. Delegation by itself does
not authorize task creation. Archival also requires current user authorization.

`fork_thread` is excluded. It copies task history and is not routing,
delegation, retry, reuse, or coordination. `handoff_thread` is outside the
router and is only for an explicitly requested relocation of an existing task
and its associated Git state.

`max` and `ultra` require explicit operator authorization for the bounded work
in the current task. Neither changes permissions, targets, credentials,
mutation authority, or delegation depth.

## Output Contract

Return the topology, execution channel, technical and logical relationships,
task lifecycle and reuse action, role, model, effort, Fleet fan-out and ceiling,
capability chain, missing controls or skills, authorization gates, proof bar,
stop condition, runtime rejection evidence, binding evidence, preset version,
preflight state, proof requirement versus proof state, evidence classification,
and excluded operations. Never present caller-supplied gstack context strings as
verified artifacts or a proof-bearing route as completed work.
