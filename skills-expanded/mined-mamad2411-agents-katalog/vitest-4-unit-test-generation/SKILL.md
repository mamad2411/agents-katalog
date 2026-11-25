---
name: vitest-4-unit-test-generation
description: Generates targeted Vitest 4 unit tests for JavaScript and TypeScript functions, classes, modules, adapters, and edge cases. Use when adding or improving isolated unit tests, mocking dependencies, or covering critical logic without external services.
license: MIT
compatibility: Vitest 4.x, Node.js 20+, and Vite 6+ when Vite integration is used.
---

# Vitest 4 Unit Test Generation

Use this skill when the task is to create or improve focused unit tests with Vitest 4.

## Version Boundary

- Target Vitest 4.x only.
- Do not introduce Vitest 5 beta APIs.
- Use Vitest 4.1 tags only after confirming the installed Vitest version is at least 4.1.

## Workflow

- `workflows/unit-test-generation-workflow.md`: Use when creating or refactoring targeted unit tests.

## Resource

- `resources/unit-test-generation-checklist.md`: Use as a checklist for test inputs, edge cases, mocks, timers, cleanup, and assertions.

## Example

- `examples/targeted-unit-test-example.md`: Reference example for deterministic unit tests and dependency injection.

## Unit Test Principles

- Test behavior through public or stable module boundaries.
- Prefer explicit imports from `vitest`.
- Keep tests deterministic and isolated.
- Avoid external network, real databases, production queues, shared caches, and cloud services.
- Mock at dependency boundaries, not inside the unit under test.
- Cover success paths, representative failure paths, and important edge cases.
- Keep snapshots small and intentional.
- Do not weaken assertions to make a test pass.
