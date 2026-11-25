---
name: dev-flow-master
description: Use as the primary entrypoint for dev-flow development requests, including features, debugging, UI/UX, review, requirement changes, recovery, governed routing, phase gates, execution coordination, Git boundaries, and acceptance.
---

# dev-flow-master

Dispatch governed dev-flow work. Master owns route and gate decisions; focused skills own their stages. It coordinates implementation but does not implement, perform Git side effects, or replace OpenSpec/opsx.

All user-facing replies and persisted Markdown artifacts are written in Chinese.

## Canonical State

Markdown artifacts are the single workflow state. Recover actual repository state, OpenSpec/opsx, `dev-flow-state.md`, and `progress.md`; always load implementation tasks from the active OpenSpec task artifact. Chat memory is never completion evidence.

## Steps

1. **Recover evidence.** Inspect actual Git/filesystem state and persisted OpenSpec/dev-flow artifacts.
   **Complete when:** state paths, current blockers, approvals, and evidence are known without relying on chat memory.

2. **Classify and route.** Load `dev-flow-intent` for every new or ambiguous entry, check existing change/spec context, classify complexity, and persist `routing_decided`. A loop-authorized phase enters planning with its confirmed baseline and envelope.
   **Complete when:** one owner, one implementation path, required protocols, risks, and the next gate are explicit.

   Loop admission requires approved `loop_start_ready` carrying the four-file content baseline (`requirements.md`, `design.md`, `test-plan.md`, `test-cases.xlsx`), Loop Phase DAG, and envelope.

   Resolve the Phase from the Loop controller's Ready Phase Set and matching phase index entry in `phase-artifacts.md` or `opsx-index.md`. The Loop controller, not dev-flow, owns concurrent Phase dispatch.

3. **Drive phase planning.** Explicit implementation intent authorizes necessary planning artifacts. Use OpenSpec tasks as the only task source, express dependencies inline only where needed, declare the Phase write scope, then run one combined planning checker and one Phase Planning Gate. For Loop work, validate the isolation and Git policy inherited from the Loop Start Gate without asking again.
   **Complete when:** the combined plan is approved or has a concrete blocker and recovery owner.

4. **Coordinate execution.** After the Phase Planning Gate, load `dev-flow-execution`. The current Phase's OpenSpec tasks execute with one writer at a time in stable eligible order. Requirement, material task, dependency, or declared write-scope changes return to planning.
   **Complete when:** all in-scope tasks have reviewed outcomes, verification evidence, and permitted Git integration states.

5. **Authorize completion.** Load `dev-flow-acceptance` to aggregate task reviewer results and fresh integration/system evidence. Do not launch another checker over unchanged task evidence; loop `phase_eval` reuses the same acceptance result.
   **Complete when:** `acceptance_ready` supports `ready-to-report`, or the result is explicitly `not-ready`/`ready-for-review` with owner, reason, and next action.

## Context Pointers

- `references/routing-and-complexity.md`: owner selection, complexity, OpenSpec/opsx, and loop-authorized entry.
- `references/state-and-gates.md`: Markdown state, signals, approvals, quality policy, and completion evidence.
- `references/flow-and-recovery.md`: stage order, recovery, continuation, and hard stops.

OpenSpec/opsx remains the requirements, design, and only phase-task source. Loop owns the cross-phase DAG, Ready Phase Set, Phase worktrees, and serial Phase integration; dev-flow owns one Phase's serial task execution and acceptance.
