---
name: phase-implement
description: Phase 3 of the software delivery workflow: execute an approved implementation plan using TDD, language-specific patterns, focused changes, build repair, and bounded retries.
origin: ECC automation-pack
---

# Phase Implement

Use this skill when the user asks for `/phase-implement`, implementation from a plan, TDD execution, or the coding stage of an automated software delivery flow.

## Purpose

Implement the approved plan with tests and tight feedback loops.

## Workflow

1. Load the latest relevant plan or ask for the target plan if none is obvious.
2. Split work into independently verifiable steps.
3. For each step:
   - write or update a failing test when practical
   - implement the smallest change
   - run the nearest verification
   - refactor only after behavior is protected
4. Use the project’s existing style, helpers, and architecture.
5. Use language-specific skills or reviewers when the project stack is clear.
6. If build or tests fail:
   - diagnose the first meaningful failure
   - fix incrementally
   - retry up to 3 times per distinct failure mode
7. Mark blocked work explicitly instead of hiding failures.

## Output

Include:

- implemented steps
- changed files
- tests or checks run
- failures fixed
- any blocked or deferred items

End with `PHASE_IMPLEMENT_DONE` when implementation is complete, or `PHASE_IMPLEMENT_BLOCKED` when it cannot safely continue.
