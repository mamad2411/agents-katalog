---
name: flaky-test-triage
description: Diagnose intermittently failing tests by isolating ordering, timing and shared-state causes, then propose the smallest fix. Use when a test suite passes locally but fails unpredictably in continuous integration.
license: MIT
allowed-tools: Read Bash Grep
metadata:
  category: software-engineering
---

# Flaky test triage

A flaky test is a defect in the test, the code under test, or the boundary
between them. Find which before changing anything.

## Isolating the cause

Run the failing test alone. If it passes, the cause is shared state or
ordering. If it still fails intermittently, the cause is timing or a real race.

## Common causes

- Tests that share a database row, temporary file or module-level cache.
- Assertions on wall-clock time or on unordered collections.
- Fixtures that are not torn down when a test fails early.
- Real network or filesystem calls that were meant to be stubbed.

## The fix

Prefer removing the shared state over adding a retry. A retry hides the defect
and keeps the signal noisy.
