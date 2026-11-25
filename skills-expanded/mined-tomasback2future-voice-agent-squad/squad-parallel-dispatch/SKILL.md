---
name: squad-parallel-dispatch
description: Default to parallel when items are independent. Children run scoped tests; the parent runs the full suite as the integration gate. Sequencing independent work out of habit wastes wall-clock time.
allowed-tools:
  - Task
  - Bash
disable-model-invocation: false
---

# Parallel dispatch: when, when-not, and the test-gate split

Two or more ready items in different subsystems with no shared state and no mutual dependency should be dispatched in parallel. Sequencing them out of habit wastes wall-clock time. The gain is real — three 2h items in parallel finish in 2h, not 6h.

## When to use this skill

Invoke this skill whenever you are about to start a second item in a session, or whenever the user asks you to do multiple things at once. Use it to decide between parallel dispatch and sequential execution, and to set up the dispatch correctly if parallel.

## When parallel is right

- Three unrelated bugs in three different subsystems.
- A research task plus an unrelated code task.
- Building a UI component plus writing the API endpoint behind it — but only if the contract is already in the item file. Otherwise the API contract IS the dependency, and you must sequence the API first.
- Code review of N completed items: use one repository-approved independent reviewer per item, respecting review single-flight and runtime capability.

## When parallel is wrong

- Items in the same file or directory. Merge conflicts.
- Items where one's findings might change another's approach. Work the first one first; let it inform the second.
- Exploratory work where you do not yet know what is broken. A single focused investigation is faster than three speculative dispatches.
- Items that share state (same database table, same config file, same in-memory singleton). Race conditions in your own work.

## The test-gate split (this matters)

Parent and child test gates are NOT symmetric:

- **Children** run only their package-scoped tests during TDD (`go test ./<pkg> -race`, scoped vitest, etc.). They MUST NOT run the full suite — wasted wall-clock and spurious failures from sibling worktrees.
- **Parent** is the integration gate. After cherry-picking all parallel diffs into `main`, the parent session runs the full suite (`go test ./... -race`, full vitest) BEFORE dispatching code review. This is what catches cross-package races, shared-state conflicts, and silent breakages no single child could see.

Violating either side causes real problems:

- Child running full suite → wasted minutes per child, spurious failures from uncommitted parallel work in sibling worktrees.
- Parent skipping the post-integration full-suite gate → a race like "new goroutine in package A reads a non-atomic field in package B's test harness" ships to main and only fires on CI.

## How to apply

1. Tick first. Subagents cannot see chat — bake whatever you just heard into the briefing.
2. Use the selected runtime's supported subagent mechanism and the briefing below. The `superpowers:dispatching-parallel-agents` helper is optional; do not require a Claude-specific tool name or launch a duplicate controller.
3. For each child, paste the standing constraints (commit conventions, no-PM-traces, comment discipline, TDD, scope-limited tests, return format) into the briefing. Do not paraphrase from memory.
4. Each child gets: context, files to look at (priority order), the specific task in one sentence, the item file path, the output format, and the constraints (read-only vs write code, no scope creep, no new docs).
5. Tell each child: "your test scope is your package; do NOT run the full suite."
6. After children return: read each diff yourself before reporting "done." Trust but verify — agent summaries describe intent, not always reality.
7. Cherry-pick / integrate diffs into the parent branch.
8. Parent runs full suite. Paste the green output.
9. Then dispatch parallel code review (one reviewer per item).

## Anti-patterns to avoid

- Sequencing two independent items because "I will just do them one at a time." Habit. Defaults to parallel.
- Dispatching parallel agents on related work and discovering the merge conflict at integration time. Pre-flight the file overlap.
- Letting children run the full suite. Burns wall-clock; gives spurious failures.
- Skipping the parent integration gate because "the children all passed." Cross-package interactions are exactly what the parent gate exists to catch.
- Trusting child summaries without reading their diffs. Sometimes the summary and the diff disagree.
