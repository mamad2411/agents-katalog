---
applyTo: "**/tests/**,**/test/**,**/*.test.*,**/*.spec.*,**/*Tests.cs"
description: Automated test authoring standards.
---

# Test Instructions

- Name tests for the behavior under test and its expected outcome, not for the method name.
- One logical assertion per test. Arrange, act, assert, in that order, with no branching.
- Tests are deterministic: no real clocks, random values, network calls, or shared mutable state. Inject them.
- No sleeps. Await deterministic signals.
- Every bug fix begins with a test that fails for the stated reason, then passes after the fix.
- Cover the success path and the primary failure path of each new code path.
- Test observable behavior through public entry points. Do not assert on private internals.
- Fixtures and temporary directories are created per test and removed in teardown.
- Never place real credentials or production data in a fixture.
- A skipped or quarantined test requires a linked issue and an owner.
