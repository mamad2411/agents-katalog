---
name: unit-test-writing
description: Writes focused unit tests for a function or class, covering boundaries and failures without testing mocks. Use it when code lacks tests or a bug needs one.
---

# Unit test writing

Test what the code promises, not how it does it.

## Steps

1. Find the test framework, file layout, naming and helpers already used (look at two existing test files) and copy their style. Do not add a new framework.
2. Read the target and list its observable behaviors: return values, thrown errors, state changes, calls to collaborators that matter.
3. Choose cases per behavior: one typical input, each boundary (0, 1, max, empty, null, whitespace, duplicate), each documented error, and one case per branch you can name. Skip cases that repeat another.
4. Write one test per behavior. Name it as a sentence ("returns the first match when two items tie"). Use arrange, act, assert with one logical assertion each. Prefer literal expected values over recomputing them with the same logic.
5. Fake only what crosses a process boundary: network, disk, clock, randomness. Use real objects for everything inside the module. Never assert that a mock was called when you can assert the result.
6. Prove each test can fail: change the code (flip a condition, drop a line), see red, then revert. Report any test that stayed green.
7. Run the file and the full suite.

## Rules

- No sleeps, no test order dependence, no shared mutable state, no snapshots of large objects.
- Do not edit the code under test, except to report that it is untestable.

## Report

Tests added with their names, behaviors left uncovered, and the mutations you tried.
