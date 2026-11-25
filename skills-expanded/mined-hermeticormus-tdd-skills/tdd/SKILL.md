---
name: tdd
description: Test-driven development discipline. Write the failing test first, then Red-Green-Refactor, one test at a time, minimal code to pass, test behavior not implementation. Use when implementing a feature or fixing a bug test-first in JavaScript/TypeScript or Python.
license: MIT
---

# TDD

Write the failing test first, then the minimal code to pass it, then refactor. One test at a time. Test behavior, not implementation.

**Tradeoff**: TDD biases toward design clarity and coverage over raw speed. For trivial or throwaway code, use judgment.

## 1. Write the failing test first

Before any implementation code exists, write one test that describes the behavior you want. Run it; it must fail. A passing test before the code exists is testing nothing.

## 2. Red, Green, Refactor

- Red: write one failing test for the simplest unhandled case.
- Green: write the minimal code that makes it pass.
- Refactor: improve the code without changing behavior; tests stay green.

Then repeat for the next case. The order is the discipline.

## 3. One test at a time

One test, one implementation, then the next. Do not write a batch of tests up front and chase them.

## 4. Minimal code to pass

Write only what the current failing test requires. No abstraction it did not ask for. The next failing test pulls the design forward.

## 5. Test behavior, not implementation

Assert on inputs and outputs, observable state changes, and side effects. Do not assert that an internal helper was called or that a private field holds a value. Mock external dependencies only; let internal modules run real code.

## When to use TDD

New features, complex logic, bug fixes (write a failing test that reproduces the bug), refactoring (tests first to prove behavior is unchanged), and APIs where the contract is the product. Overkill for throwaway proofs-of-concept, pure UI layout tweaks, trivial CRUD, and generated code.

## Anti-patterns

- Writing all tests first, then all code.
- Asserting on implementation details instead of behavior.
- Over-mocking, so you test mocks instead of real code.
- Skipping Red, so the test never proved anything.

---

See full content, the worked OAuth walkthrough, and common patterns at https://github.com/HermeticOrmus/tdd-skills.
