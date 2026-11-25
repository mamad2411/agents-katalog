---
name: test-first
description: Drive a feature or bug fix with a failing test first. Use when implementing new logic or fixing a bug — never when only reading or refactoring without behavior change.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
disable-model-invocation: true
argument-hint: "<feature or bug description>"
---

# Test-first

Enforces TDD discipline: red → green → refactor. The test is the spec — write it first, watch it fail, then make it pass.

## Process

1. **Restate the requirement** in one sentence. If you can't, ask the user before proceeding.
2. **Find the right test file** (or create one in the project's test conventions). Look at neighboring tests for naming and style.
3. **Write a single failing test** that captures the requirement. Concrete inputs, exact expected outputs.
4. **Run the test and confirm it fails.** Show the failure output. If it doesn't fail for the right reason, the test is wrong — fix the test, not the code.
5. **Implement the smallest change** that makes the test pass. Resist scope creep.
6. **Run the test and confirm it passes.** Then run the broader suite to confirm nothing else broke.
7. **Commit** with a `test:` or `feat:` prefix mentioning the requirement.

## Anti-patterns to avoid

- Writing the implementation first and the test after ("trivially-passing-test syndrome").
- Tests that mock the very thing under test.
- Tests that check `function called` instead of `correct behavior`.
- Skipping the red step. If you didn't see it fail, you don't know it's testing the right thing.

## Quick test-runner reference

| Stack | Command |
|---|---|
| Python (pytest) | `pytest path/to/test_file.py::test_name -v` |
| Node (vitest)   | `npx vitest run path/to/test.spec.ts -t "name"` |
| Node (jest)     | `npx jest path/to/test.spec.ts -t "name"` |
| Go              | `go test -run TestName ./...` |
| Rust            | `cargo test test_name` |

For deeper guidance, read `knowledge/test-driven-development/SKILL.md`.
