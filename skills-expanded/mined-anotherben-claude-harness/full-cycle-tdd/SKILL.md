---
name: full-cycle-tdd
description: TDD-first development workflow. Agent Harness + Superpowers TDD discipline. Every task starts with a failing test. No code without a test first. Use for bug fixes, features where correctness is critical, or when you want maximum test coverage. Invoked with /full-cycle-tdd followed by a description.
---

# Full Cycle TDD — Test-Driven Development Workflow

Agent Harness execution with Superpowers TDD baked into every task.

## Philosophy

```
RED → GREEN → REFACTOR — for every task, no exceptions.
```

Every task produces a failing test before any implementation code is written.
The test defines "done". The code exists only to make the test pass.

## Prerequisites

1. Agent Harness (`.claude/AGENT_HARNESS.md`)
2. Superpowers TDD skill (`superpowers:test-driven-development`)
3. Memory/knowledge MCP servers (if configured)
4. Test framework configured (jest/vitest/playwright per project)

---

## PLANNING MODE (Interactive)

### Phase 1: Define + Research

1. Load Agent Harness Phase 0 — query knowledge graph for prior context
2. Invoke `superpowers:brainstorming` — push for acceptance criteria and edge cases
3. Save design to `.claude/designs/[feature-name].md`

### Phase 2: Create Test-First Plan

Invoke `superpowers:writing-plans`. Each task MUST include:
- **Test assertions first** — what the test checks, exact expected values
- Files to create/modify
- The test file path
- Git commit message (two commits per task: test commit + implementation commit)

Format:
```
- [ ] Task 1: Validate order total calculation
  Test: tests/services/orderTotal.test.js
    - returns 0 for empty cart
    - sums line items correctly
    - applies discount percentage
    - rounds to 2 decimal places
  Files: src/services/orderTotal.js
  Commits:
    1. "test: add order total calculation tests"
    2. "feat: implement order total calculation"
```

Save to `.claude/plans/[feature-name]-plan.md`

### >>> SINGLE CHECKPOINT <<<

Show plan. Wait for "go". Only pause.

---

## EXECUTION MODE (Autonomous)

For each task, follow this exact sequence. No shortcuts.

### TDD Loop (per task)

```
1. READ the task's test assertions from the plan
2. WRITE the test file — make it fail for the right reason
3. RUN tests — confirm RED (failing with expected error, not import error)
4. COMMIT the failing test: "test: [description]"
5. WRITE the minimum code to make the test pass
6. RUN tests — confirm GREEN (all pass)
7. REFACTOR if needed (tests must stay green)
8. COMMIT the implementation: "feat/fix: [description]"
9. Mark [x] in plan, continue to next task
```

### Rules

- **Never write implementation before the test.** If you catch yourself coding first, stop, delete it, write the test.
- **The test must fail for the RIGHT reason.** A test that fails because of a missing import is not a valid failing test. It must fail because the behavior doesn't exist yet.
- **Minimum code to pass.** Don't write extra code "while you're there". The test defines the scope.
- **Two commits per task.** Test commit first, implementation commit second. This proves the test actually catches regressions.
- **Run the full suite after each task.** Not just the new test — the full suite. Catch regressions immediately.

### When tests are hard to write first

Some things (UI rendering, integration with external services) are genuinely hard to test-first. For these:
- Write the test with the expected behavior described in comments
- Implement the code
- Go back and make the test assertions concrete
- This is the exception, not the rule — document why you deviated

### After All Tasks

1. Run full test suite
2. Run `superpowers:verification-before-completion`
3. Invoke `superpowers:requesting-code-review`
4. Compound learnings to knowledge graph
5. Output completion summary per Agent Harness Phase 4

---

## QUICK REFERENCE

```
/full-cycle-tdd fix the order total rounding bug
```
→ Brainstorm → Test-first plan → "go" → RED/GREEN/REFACTOR for each task

```
/full-cycle-tdd add email validation to signup
```
→ Define edge cases → Write test plan → "go" → Failing tests first, then implement
