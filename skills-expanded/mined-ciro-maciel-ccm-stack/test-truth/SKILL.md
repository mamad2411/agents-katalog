---
name: test-truth
description: Write and trust only tests that fail when the behavior breaks, proved by sabotage. Use when writing, changing or reviewing tests.
---

# Tests that prove something

A green suite proves only that nothing it checks failed. Whether it checks the right thing is a separate question, and you answer it by breaking the code.

## Sabotage is how you check a test

After writing a test, break the code it protects (invert a condition, return early, delete the call) and run it. It must turn red. Put the code back and it must turn green. A test you never saw fail has not been tested.

## Traps that keep a broken suite green

- **Two locks, one test.** When two checks guard the same result (one on write, one on read), an end-to-end test passes while either one alone still holds. Give each check its own assertion that fails when only that check is gone, and sabotage them one at a time.
- **A 200 on a write proves nothing.** The old version also answers 200. Write a value that did not exist before this run (a timestamp, a random id) and look for that exact value when you read back. Retry the read a few times before failing: a cache serving the old version for seconds is the cache working.
- **The API does not prove the screen.** A blank page leaves every API green. A journey that matters drives the real interface (see the `verify` skill).
- **Skipped means silent.** `skipIf(!exists(path))` turns into a no-op when the path moves, and nothing reports it. Fail when a precondition is missing instead of skipping.
- **Mocks that leak.** Module mocks that are global in your test runner leak across files and break only when the order changes, usually in CI. Prefer dependency injection; reset what you mock.
- **The mock is the old contract.** A mock copied from the other side freezes it; when the real side changes, the tests stay green against a contract that no longer exists. Test against the real thing at the boundary, or regenerate the fixture from it.
- **Testing the implementation.** Assert what a caller or user can observe, so the test survives a refactor and fails when behavior breaks.

## One test account

Every test that signs in uses one dedicated account with an inbox you control, never a real person's address. Configure it as `testEmail` in CCM Stack, and a hook will refuse login and code flows sent anywhere else.

## Review checklist

For each test: what behavior does it protect, how would it fail, and did you see it fail? If any answer is "not sure", sabotage before you trust it.
