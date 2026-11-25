---
name: e2e-testing-framework
description: Write and run end-to-end tests. Use when verifying complete user
  flows through the real app.
metadata:
  tags: e2e, testing, framework
---

# End-to-End Testing

## Use this skill when
- Verifying critical journeys end to end
- Running browser-level acceptance tests
- Building stable selectors and retry discipline

## Do not use this skill when
- Testing unit logic
- Replacing lower-level tests entirely

## Instructions
1. Keep E2E focused on user journeys; push edge logic to lower layers.
2. Use role/label/accessible selectors, not brittle CSS or snapshots.
3. Auto-wait and retry on actions; avoid forced sleeps.
4. Isolate data via seeded, resettable test accounts/environments.
5. Parallelize on CI with partitioned runs.
6. Handle flaky tests: diagnose root cause; never just retry-and-forget.
7. Track the fewest flows that cover the criticals.

## Checklist
- No sleeps; waits are condition-based
- Selectors are stable
- Tests run in CI

## Output Format
- Journey map | selector strategy | CI sharding | flake log

## Common Mistakes
- E2E as the only test layer
- Flaky tests ignored in CI
- Assertions on implementation details
