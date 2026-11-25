---
name: architecture-designer
description: Use for architecture and implementation planning before large changes: module boundaries, state ownership, data flow, APIs, migrations, rollout, and validation across Swift, Kotlin/Android, Flutter, Tauri, Rust, and frontend code.
---

# Architecture Designer

## Use when
- the user asks for architecture, design, implementation planning, module boundaries, ownership, or migration strategy
- the change touches multiple modules, contracts, persistence, bridge boundaries, or risky state flow
- coding should be preceded by a small but explicit design decision

## Do not use when
- the task is a narrow local edit that can be implemented safely without architectural work
- the user mainly wants a code review, bug triage, or test-only change

## Working rules
- Start from the existing repo, constraints, and failure modes, not a greenfield ideal.
- Prefer the smallest architecture that makes the next change correct, testable, and maintainable.
- Keep UI as a projection of state and isolate side effects, IO, and async ownership.
- Compare options only when the tradeoff materially affects correctness, release risk, or maintenance cost.
- Keep the user-facing answer compact; do not turn design work into a long essay unless asked.

## Workflow
1. Restate the goal, constraints, and non-goals in a few bullets.
2. Map current modules, state owners, async flows, persistence, bridge/API boundaries, and test seams.
3. Identify the minimum architecture change that solves the requirement.
4. Compare alternatives only where a real tradeoff exists.
5. Recommend one target shape, file/module plan, and migration order.
6. Call out validation, rollout, rollback, and compatibility needs before implementation starts.

## Quality bar
- Domain logic should be testable without UI code.
- Contracts and ownership should be explicit.
- Async work should have clear lifecycle and cancellation semantics.
- Persistence, transport, and bridge layers should not bleed across the app.
- Release concerns such as observability, migrations, versioning, and failure containment should be designed deliberately.

## Reference routing
- Read `references/architecture-checklists.md` for architecture and tradeoff checklists.
- Read `references/release-quality-gates.md` when the change affects contracts, storage, permissions, rollout, or rollback.
- Read `references/official-docs.md` only for platform or framework rules that change the design.

## Output contract
Provide:
- current-state summary
- recommended target architecture
- module or file plan
- state and data-flow ownership
- validation and migration steps
- real risks and mitigations
