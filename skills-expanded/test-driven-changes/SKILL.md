---
name: test-driven-changes
description: "Plans and implements behavior changes using focused tests, regression coverage, and incremental verification. Use when adding a feature, fixing a bug, changing business logic, or refactoring behavior-sensitive code."
license: MIT
metadata:
  author: OpenSelfHosting
  version: "1.0.0"
---

# Test-Driven Changes

## Goal
Turn the requested behavior into observable checks, implement the smallest change, and prove the intended behavior without overstating coverage.

## Workflow
1. Read project instructions and identify the existing testing conventions, framework, and nearest related tests.
2. Convert the request into explicit acceptance criteria. Include normal behavior, boundaries, invalid input, and failure modes that matter to the contract.
3. Choose the cheapest test level that gives meaningful confidence: unit, component, integration, contract, or end-to-end. Avoid excessive mocks when they would hide the behavior under test.
4. Add a focused test before implementation when practical. Confirm that it fails for the intended reason; a failure caused by broken setup does not validate the test.
5. Implement the smallest coherent change. Reuse established patterns and avoid unrelated refactors.
6. Run the focused test, inspect failures, and make the smallest necessary adjustments.
7. Add adjacent tests for important regressions, authorization boundaries, invalid states, error handling, and compatibility when relevant.
8. Run appropriate broader checks after focused tests: formatter, linter, type checker, relevant test suite, and build. Select checks proportionate to impact.
9. Review whether tests could pass while the defect remains. Verify assertions check results and side effects, not merely execution.
10. Inspect the final diff for scope creep, flaky timing, hard-coded environment assumptions, skipped tests, and accidental weakening of assertions.

## Test quality checklist
- The test name describes behavior, not implementation details.
- Arrange/act/assert or the project’s equivalent is easy to follow.
- Inputs include the condition that previously failed.
- Assertions would fail if the target behavior regressed.
- Cleanup is deterministic and external services are isolated appropriately.
- Test data contains no real secrets or personal data.

## Report
Summarize acceptance criteria, new/changed tests, exact checks executed, actual results, and any coverage or environment limits.

## Guardrails
- Never disable, skip, delete, or loosen a failing test solely to obtain a green run.
- Do not claim full coverage because tests pass.
- Do not run tests against production data or external systems with side effects without authorization.
- If the repository has no test harness, recommend a minimal practical approach and state that automated verification is limited.
