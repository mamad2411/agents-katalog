---
name: allinluna
description: Compile and execute a goal, existing plan, active run, or Research Routes packet through the vNext Coordinator, Task Lanes, WorkUnits, and Workflow Packs.
---

# All in Luna
All in Luna is one public entry point. Accept one of these inputs:

- an idea or one-sentence goal;
- an existing plan;
- an active run or legacy run snapshot;
- a Research Routes packet.
Compile the input to a typed `RunIntent`, select a registered Workflow Pack, and compile its `TaskGraph` containing contracts, dependencies, ownership, done-when conditions, WorkGraph templates, and resource defaults. Then call the vNext runtime/CLI to persist the graph, release ready Lanes, ingest real host receipts, and continue until the root result is complete or a concrete blocker is returned.
## Highest-priority exact Action Relay
Logical `LocalDispatchIntent` values are not HostActions. A HostAdapter first
resolves them to a `lane-direct-work/v1` plan or an exact `HostAction.tool` opcode:

1. Invoke that exact tool with `HostAction.arguments`.
2. Never translate, approximate, or substitute another capability.
3. A `top_level_task` may never fall back to a subagent, the current thread, or direct execution.
4. Ingest the raw receipt immediately, then tick again.
5. If no `HostAdapter` is bound, return `ACTION_RELAY_REQUIRED` and preserve the exact action.
6. Return `HOST_CAPABILITY_BLOCKED` only after capability discovery confirms
   that the exact tool is absent.

For local work, `native_preferred` uses an advertised native worker or a real Lane-direct plan;
`native_required` blocks when absent and `direct_only` never spawns. A direct receipt is not
completion: the Lane must execute the WorkUnit and produce a verified `work-handoff/v1`.

Receipts explicitly provide `action_contract_hash`, `actual_tool`, and `actual_capability`.
A wrong actual tool is `HOST_PROTOCOL_VIOLATION`, not evidence that a Task started.
## Lane bootstrap and persistent drivers

Every public `codex_app__create_thread` dispatch embeds a complete `lane-bootstrap/v1` object in its durable action and child prompt: identities, digests, Store and contract references, workspace, capabilities, and required handoff. A child Lane must reopen that Store; its prompt is never only prose.
`CoordinatorDriver` is the durable outer loop: schedule exact actions, ingest receipts, wait/read top-level threads, ingest typed Lane handoffs, reconcile, and immediately release newly-ready Tasks. `LaneDriver` performs the matching local WorkGraph loop, including snapshots, dynamic local expansion, worker handoffs, same-worker corrections, and lane handoff synthesis. A wave is only a UI grouping: dependency-ready work is released immediately.
## Runtime shape

```text
Conversation
  -> Global Coordinator
       -> independent Task Lane(s)
            -> bounded recursive WorkUnits
                 -> tools / skills / plugins / MCP
```
Keep raw tool output in the Artifact Store. Pass typed contracts, artifact
references, context slices, receipts, and handoffs upward. A child WorkUnit
must narrow its parent scope, authority, ownership, and resource envelope; a
cross-Lane request becomes a promotion request.
## Input and Pack routing

Use `SinglePublicSkillAPI.compile()` or `allinluna start`:

- plain goal -> `delivery` by default;
- existing plan -> read-only legacy import, then `delivery`;
- active run -> read-only run-state import and recovery-oriented compilation;
- Research Routes packet -> `research-routes-bridge`, preserving Claims,
  Evidence, unknowns, contradictions, failure regimes, HumanDecision, and
  experiment-authorization boundaries.

Use `gsd` when the user explicitly requests its workflow. Its executable Pack
provides clarify, specify, decompose, implement, verify, and integrate,
dynamic lane-local expansion, bounded WorkUnits, contract handoffs, and local
failure recovery. Do not add GSD phases to Core.

`--task-graph` accepts a canonical graph or compact outcome Tasks. Compile compact
input through the selected Pack so it owns contracts and Lane-local WorkGraphs.
For GSD, explicit expert decomposition defaults to compact six-phase roots;
use Pack config `granularity: full` only when the detailed recipe is useful.

## Resources and permissions

Resource choices follow this precedence: explicit user request, then a
Task/WorkUnit override, user preference, Pack capability, deployment/host
capability, and finally the current session/host default. Core is
vendor-neutral and does not hardcode a provider or concrete model route.
Preserve requested, resolved, and actual values separately. If the host cannot provide an actual model receipt, record
`actual: null` and `actual_state: unresolved`; never claim a fallback or
fabricate a receipt. A narrower scope may change compute resources but may not
expand permissions or ownership.
Host resource-route telemetry is optional adapter diagnostics, not an execution or result-completion requirement. A host route must resolve the required `model` before an executable `codex_app__create_thread` action is frozen; an unresolved route emits a non-executable resolution action. Without explicit model and reasoning telemetry, record `actual: null` and `actual_state: unresolved` while retaining the independent requested and resolved values. The persisted receipt exposes `resource_receipt.requested`, `resolved`, `actual`, and `actual_state`. When actual evidence is available, the adapter compares requested values with the persisted dispatch action and requires actual to match the reported resolved route; a receipt must never establish its own verification baseline. A route is not hard-locked unless policy says so; a locked route must match its receipt.

Request permissions just in time at the action boundary. Read-only compilation
does not request credentials, publication, deployment, push, destructive work,
or live external mutation. When such an action is reached, return a
`PermissionIntent` with `ask`, `allowed`, or `denied`; do not front-load a
questionnaire and do not silently perform the action.

## CLI and recovery

```text
allinluna --db ABSOLUTE_RUNTIME_DB start --goal "..." --repository-root REPOSITORY [--no-dispatch] [--supersedes-run OLD_RUN_ID]
allinluna capabilities
allinluna --db ABSOLUTE_RUNTIME_DB status RUN_ID [--invariants]
allinluna --db ABSOLUTE_RUNTIME_DB doctor RUN_ID
allinluna --db ABSOLUTE_RUNTIME_DB {preview-actions|dispatch|drive|pause|resume|retry|cancel|reconcile} RUN_ID
allinluna --db ABSOLUTE_RUNTIME_DB set-task-policy RUN_ID TASK_ID POLICY.json
allinluna --db ABSOLUTE_RUNTIME_DB request-permission RUN_ID --scope-type task --scope-id TASK_ID --action push
allinluna --db ABSOLUTE_RUNTIME_DB lane {start|status|tick|drive|next-actions|handoff|finalize|ingest-direct-result} RUN_ID TASK_ID
```

The runtime CLI exposes `start`, `status`, `preview-actions`, `dispatch`, `ingest-receipt`, `pause`, `resume`, `retry`, `cancel`, `set-policy`, `set-task-policy`,
`request-permission`, `capabilities`, and `reconcile`. Use the
public compatibility APIs for legacy plan/run import; they return host-neutral
actions for the host adapter and never treat a pending client id as an active
receipt.
`lane finalize` synthesizes and verifies the canonical handoff from persisted
WorkUnit results. A Task Lane must use the Desktop-observed worktree recorded on
its TaskAttempt; never substitute the control-plane repository root. A verified
WorkHandoff is normal completion input: `lane drive` materializes its concrete
file/directory/Git artifacts, carries its passing checks into done_when, and
projects the resulting checks, artifacts, exports, workspace, and changed paths
onto the LaneHandoff consumed by Coordinator. If `lane drive` returns
`LANE_DIRECT_EXECUTION_REQUIRED`, execute that bounded plan, use
`lane ingest-direct-result RUN_ID TASK_ID RESULT.json`, and resume `lane drive`.
Do not manually reconstruct a second LaneHandoff.

An explicit request for exactly one top-level Task, or for one cohesive output
directory plus one commit, is authoritative Task cardinality. Keep sections and
semantic domains as that Task's context rather than promoting them to sibling
Tasks. `doctor` and `status --invariants` are read-only diagnostics;
they do not add a completion approval layer. Recovery keeps immutable artifacts and re-computes ready actions after leases,
receipts, or context snapshots are reconciled.

Coordinator `preview-actions` is a non-relayable summary; only `dispatch` or `drive` returns a persisted Coordinator action. Coordinator `next-actions` is a deprecated one-RC alias and must not be relayed; Lane `next-actions` still materializes a relayable local action.

Resolve one absolute Runtime DB path when the Run starts and reuse that exact
path for every Coordinator and Lane command. For repository work, pass
`--repository-root`; a compact task graph's `metadata.workspace` is also
recognized when no explicit root is supplied. Do not silently fall back to a
projectless target for repository work. If the `allinluna` console executable
is not on `PATH`, use `python -m allinluna_runtime` with the same arguments and
the same absolute DB path; do not switch runtimes or create a second Store.

The registry/launcher is internal discoverability. Ordinary users enter through
this contextual Skill; experts may inspect Pack and manifest contracts.
