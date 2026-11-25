---
name: test-mocking-strategies
description: Picks the right test double for each dependency (real object, fake, stub or spy) so tests stay fast without mocking away the behavior they should verify.
---

# Test mocking strategies

Use the least fake double that keeps the test fast and deterministic.

## Decide per dependency

1. **Real object** when it is pure, in memory and cheap: value types, parsers, formatters. Never mock these.
2. **Fake** (a working simplified implementation) for stateful collaborators you own: an in-memory repository, a fake clock, a local queue. Share one fake across the suite and test it against the same contract as the real one.
3. **Stub** for a canned answer from something slow or external: an HTTP client returning a fixed response, including error and timeout cases.
4. **Spy or mock** only when the call itself is the behavior: an email sent, a payment charged, an event published. Assert the arguments that matter, not the call order.

## Rules

- Mock at the boundary you own, such as your own payment client wrapper, not the third-party SDK's internals.
- Assert outcomes (return value, stored state, emitted event) before interactions.
- Never mock the class under test, and never stub a private method.
- If a test needs more than three doubles, the unit has too many dependencies: say so and suggest the split.
- Keep stubs honest: build responses from recorded real payloads or the published schema.

## Report

For a review: each test with a smell, the double it uses, the better choice and why. For new tests: which doubles you chose and the reason for each.
