---
name: jest-engineering
description: Write and configure Jest tests. Use when working on a Jest test suite.
metadata:
  tags: jest, engineering
---

# Jest Engineering

## Use this skill when
- Configuring Jest for a project
- Writing mocks, spies, and timers correctly
- Speeding up and stabilizing suites

## Do not use this skill when
- Non-JS/TS projects
- Testing design (use unit-testing)

## Instructions
1. Configure transform, moduleNameMapper, and testMatch cleanly.
2. Use jest.spyOn + restoreMocks to avoid cross-test leaks.
3. Use fake timers for time-dependent code; advance them, avoid real waits.
4. Mock modules at the boundary, not everything.
5. Run in parallel with proper resource isolation.
6. Write snapshot tests sparingly; keep them small.
7. Use coverage thresholds that are meaningful.

## Checklist
- restoreMocks on
- No sleeps or real timers where fake works
- Suite runs in CI within budget

## Output Format
- Config | mocking strategy | perf fixes

## Common Mistakes
- Global mocks leaking state
- Spinning up servers instead of mocking at the edge
- Snapshot sprawl
