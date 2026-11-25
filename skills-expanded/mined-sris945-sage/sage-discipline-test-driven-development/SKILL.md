---
name: sage-discipline-test-driven-development
description: SAGE — use before implementation code. Tests first; minimal code to pass; refactor with green tests.
---

# SAGE discipline — Test-driven development

## Purpose

You are operating inside **SAGE** (Self-improving Autonomous Generation Engine). For features, bugfixes, and refactors: **write a failing test first**, observe the failure, then write the smallest change that makes it pass.

**Core rule:** If you did not see the test fail for the right reason, you do not know the test matches the behavior.

## Iron law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

If you wrote implementation first, delete it and restart from the test.

## Red — green — refactor

1. **Red:** One minimal test expressing the desired behavior; run it — must fail for the expected reason.
2. **Green:** Smallest implementation that makes the test pass.
3. **Refactor:** Clean up with all tests still green.

## When this applies

- New behavior, bugfixes, refactors, API or contract changes.
- Skip only for throwaway spikes or generated/config-only artifacts (and say so explicitly).

## Anti-patterns

- “I’ll add tests after” — no.
- Mocking away the behavior under test — you are not testing reality.
- Copy-paste implementation into tests — tests should describe outcomes, not mirror bugs.

## Cross-links

- Pair with **sage:discipline:verification-before-completion** before claiming done.
- Pair with **sage:discipline:systematic-debugging** when failures are unclear.
