---
name: dev-flow-execution
description: Use when Phase 3 has started and the agent must execute continuously, dynamically replan tasks, verify results, handle sub-agent settlement, and maintain runtime orchestration state.
---

# dev-flow-execution

Run approved phase work to settlement. The main agent coordinates; implementation and independent review remain isolated in sub-agent contexts. All user-facing replies and persisted Markdown artifacts are written in Chinese.

## Canonical State

Use the active OpenSpec task artifact as the only implementation task source, together with progress.md and actual repository evidence. Dependencies are inline `Depends on` references. A Phase has one writing task agent at a time; only the Loop controller may run separate Phase worktrees concurrently. Persist concise results in Markdown and raw output under `.dev-flow/runtime/<run-id>/`.

## Steps

1. **Reconstruct runtime truth.** Re-read actual state, OpenSpec tasks and dependencies, and progress.md; select the next eligible task in stable OpenSpec order.
   **Complete when:** eligible, running, blocked, and settled tasks agree with actual evidence.

2. **Dispatch eligible work.** All implementation tasks go to isolated sub-agents, but dispatch exactly one writing task at a time inside this Phase. Do not create task batches or nested task-level writer parallelism.
   **Complete when:** the next eligible task has one bounded scope, actor, verification contract, and final-signal requirement.

3. **Settle each task.** Follow `references/task-settlement-and-modes.md`. Require built-in TDD or an explicit exception, fresh proving checks, and an independent reviewer sub-agent returning a 0-100 score. Apply at most three fix rounds after the initial review.
   **Complete when:** each task is approved under the quality policy or stopped with remaining findings and a user decision.

4. **Replan material changes.** Follow `references/replanning-and-recovery.md`. Update only the affected OpenSpec artifacts/tasks and progress. Material task, dependency, acceptance, or writer-boundary changes re-enter combined planning.
   **Complete when:** affected downstream tasks are updated or execution stops at the correct gate.

5. **Aggregate and hand off.** After all OpenSpec tasks settle serially, run final Phase checks, update `progress.md`, and emit `execution_settled`. Acceptance reuses task reviewer evidence and adds only missing integration/system checks.
   **Complete when:** every task has a final status, reviewer score/findings, fix-round count, verification evidence, and Git state.

## Context Pointers

- `references/runtime-and-dispatch.md`: single-writer task cursor, execution modes, eligibility, and runtime state.
- `references/task-settlement-and-modes.md`: built-in verification, independent review, three fix rounds, and final signals.
- `references/replanning-and-recovery.md`: material changes, retry boundaries, and recovery.

Do not claim completion from an agent message alone. Actual files, fresh checks, and the independent reviewer verdict are required.
