---
name: flaky-test-policy
description: Quarantine-then-fix flaky tests; a retried test is a tracked bug, not a pass
---

# Flaky Test Policy

A flaky test is a test that passes sometimes and fails sometimes without any change to the code. Retry-to-green hides flakiness behind an eventually-true signal and trains the team to ignore test failures. Once a CI pipeline is known to "just need a rerun," every real failure gets retried instead of investigated. The policy is: surface flakiness, quarantine it, fix the root cause, then restore.

## Rules

- **Do not add retries to silence a flaky test.** A `retry: 3` flag on a test means the test can fail twice in a row and still report green. This defeats the purpose of the test. Remove retries that exist solely to pass a known-flaky test.
- **Quarantine rather than delete.** When a test is flaky and cannot be fixed immediately, mark it `.skip` with a linked issue in a comment (`// TODO: unskip after #456 is resolved`). A skipped test with a tracking issue is visible; a deleted test is invisible.
- **Track every quarantined test as a bug.** Create a ticket the moment you skip a test. Flaky tests that are skipped-and-forgotten accumulate until the test suite has no value.
- **Fix the root cause, not the symptom.** Flakiness is almost always caused by: shared state leaking between tests, real timers, non-deterministic ordering (network, async), or missing `await`. Diagnose the cause; don't adjust assertion tolerances or add delays.
- **Restore quarantined tests within one sprint.** A test skipped for more than two weeks is a test that will never be restored. Set a due date on the tracking issue.

## Examples

```ts
// BAD — retry masks the flakiness, no visibility
it('syncs the feed', { retry: 5 }, async () => {
  await syncFeed()
  expect(feedStore.items).toHaveLength(10)
})

// BAD — deleted test, invisible loss of coverage
// (the test that was here was flaky so it was removed)

// GOOD — quarantined with a tracking issue
// TODO: unskip after https://github.com/org/repo/issues/456 is resolved
// Flaky due to race condition in feedStore — see issue for details
it.skip('syncs the feed', async () => {
  await syncFeed()
  expect(feedStore.items).toHaveLength(10)
})

// GOOD — root cause fixed (was missing await on async setup)
beforeEach(async () => {
  await feedStore.clear() // was: feedStore.clear() without await
})

it('syncs the feed', async () => {
  await syncFeed()
  expect(feedStore.items).toHaveLength(10)
})
```

## Enforcement

"No retry-to-green" is a non-negotiable invariant — enforce it in CI rather than trusting reviewers to spot a `retry:` flag: keep the global runner retry count at `0` and add a lint/grep gate that fails the build on per-test `retry`/`{ retry: n }` options. Track each quarantined test with a required linked issue so skipped-and-forgotten tests cannot accumulate.
