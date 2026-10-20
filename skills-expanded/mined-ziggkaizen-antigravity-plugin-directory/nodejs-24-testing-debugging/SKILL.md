---
name: nodejs-24-testing-debugging
description: Writes, repairs, and debugs Node.js 24 tests and runtime failures using node:test, node:assert/strict, deterministic fixtures, resource cleanup, and built-in diagnostics. Use when tests fail, hang, flake, or need coverage.
license: MIT
compatibility: Requires Node.js 24.x for command execution examples.
---

# Node.js 24 Testing and Debugging

Use this skill for tests, runtime failures, flaky behavior, hanging processes, and debugging in Node.js 24 projects.

## Workflow

Use [test-repair-workflow](workflows/test-repair-workflow.md) when tests fail, hang, or need repair.

## Resources

Use [test-debugging-checklist](resources/test-debugging-checklist.md) for test and debugging checks.

## Example

Use [node-test-example](examples/node-test-example.test.mjs) as a reference for built-in test runner style.

## Instructions

1. Prefer `node:test` and `node:assert/strict` for base runtime tests unless the project already uses another framework.
2. Reproduce the failure before changing code.
3. Minimize the failing case.
4. Fix the root cause before changing assertions.
5. Clean up:
   - timers
   - HTTP servers
   - file handles
   - temporary directories
   - streams
   - workers
   - child processes
6. Avoid real network calls in tests unless they are explicit integration tests.
7. For filesystem tests, use temporary directories and remove them.
8. For TypeScript tests:
   - remember Node.js does not type-check while executing stripped TypeScript
   - run `npm run typecheck --if-present`
9. Use built-in diagnostics where useful:
   - `node --test`
   - `node --test --watch`
   - `node --trace-warnings`
   - `node --inspect`
10. Do not skip failing tests unless the skip is temporary, justified, and tracked.
