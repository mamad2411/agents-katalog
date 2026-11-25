---
name: structure-first
description: "Use for code generation, feature work, bug fixes, refactoring, and code review when a change creates or reshapes a multi-step flow, state lifecycle, side-effect or decision ownership, cross-unit composition, or boundary contract. Also use it when an existing structural problem makes those elements hard to trace or verify. Structural change is optional. Mechanical edits, throwaway experiments, and coherent local changes stay with their current owner and focused verification."
---

# Structure First

Find the owner. Trace the flow. Change the smallest responsible unit. Verify the contract.

## Runtime Contract

For broad bug reviews across several owners, follow [Reviewing Across Owners](references/reviewing.md). Use the first allocation for contract-counterexample investigation and focused checks, then checkpoint and load the deferred challenge. Complete both phases and integration within this invocation and the original budget. Do not preload the challenge or depend on another message or agent to switch phases.

1. Choose the smallest **current unit** that owns the behavior or rule, not merely its symptom or output. State the intent and minimum observable completion condition. For a bug, establish the observable failure before restructuring.
2. Scope the trace by the affected contract, not merely the current branch. Identify which supported entries and outputs that contract covers, and compare their guards and input or state dependencies with its required preconditions. Trace the needed path from a supported entry through its guards and source state to a state change, external effect, or public result, including read-only results and the conditions that suppress them. Include types, tests, docs, and config only when leaving them unchanged would break the behavior, contract, or meaningful verification.

3. Before implementing, use that trace to locate the actual callers and owners of the affected decisions, state changes, effects, and completion. Name the structural demand and choose where the new behavior belongs. A large file or object is a signal to inspect these responsibilities, not a reason to split by size.
4. Prefer focused local clarification. Change structure only when it removes total complexity or isolates an independently changeable responsibility; a shorter top level is not better when helpers, wrappers, context, state, errors, or lifecycle merely hide the complexity.
5. Give each decision, writer, effect, and completion rule one discoverable, non-competing resolution path. As implementation adds a branch, helper, or lifecycle, check its callers and dependencies against the chosen owner; resolve competing interpretations or mixed lifetimes before building on them. Remove an old equivalent path in the same change; otherwise name the migration owner and exit condition.
6. Verify observable behavior at the most stable responsible unit, not helper internals. Separately confirm that the changed call path keeps decisions and lifecycle coordination with their responsible owners; passing behavior tests alone does not establish this. Reopen only the smallest implicated unit when evidence shows that another unit owns part of the contract.

Keeping, inlining, merging, deleting, reordering, extracting, and making no structural change are all valid outcomes. Do not add future-use options, configuration, dependencies, wrappers, or abstractions.

For performance work, measure input scale, repeated operations, materialization, and phase timings in the existing reproduction. Remove the dominant avoidable work at its owner, then compare the same reproduction and observable behavior.

## Required Detail

Read [Structural Boundaries](references/structural-boundaries.md) before changing public I/O; decision, writer, effect, or completion ownership; async/state lifecycle; representation meaning; or migration paths.

Read [Verification](references/verification.md) when a material claim crosses identity, authoritative data, representations, external writes, or runtime/async boundaries, or when a bug, refactor, or feature needs boundary evidence.

Report the current unit, structural demand, chosen outcome, ownership or migration status, and verification only when they help the task. Do not force a template onto planning or simple local work.
