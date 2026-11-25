---
name: testing-on-the-toilet
description: >-
  Apply Google Testing on the Toilet (TotT) rules when writing tests, reviewing
  a test diff, choosing mocks vs fakes, diagnosing brittle or change-detector
  tests, DAMP vs DRY test structure, SMURF/pyramid layer choice, or flaky
  time/sleep/shared-fixture tests. Instructs what a good test asserts and what
  to refuse. Not a Vitest/runner cookbook and not an E2E authoring workflow.
---

# Testing on the Toilet

Distilled from Google's [Testing on the Toilet](https://testing.googleblog.com/search/label/TotT) episodes (2007–2026). Episode index: [`references/episodes.md`](references/episodes.md).

Run this loop on every new test and every test you review. Completion: each test that ships would fail on a real behavior bug and would survive a behavior-preserving refactor.

## 1. Change-detector gate

A **change-detector** restates production structure (especially ordered `verify` of every collaborator call) without checking an observable result. Correct and incorrect implementations pass equally; any rename/extract/reorder fails the suite.

Rewrite it to assert **state, return value, rendered output, or persisted data**. If you cannot name the user-visible contract, **delete the test** and say why. Do not "fix" a refactor by mechanically updating fifty mirrors.

Interaction `verify` is allowed only when the call itself is the contract (send mail once, do not double-charge, presenter tells the view to show X). If unsure, rewrite to a state/return assertion; if that is impossible, **stop and ask** which observable outcome the test protects.

## 2. Pick the cheapest layer that still has fidelity

Name the bug/risk first. Pick the **topmost** row in the table that can catch it. Escalate a row only when a cheaper layer would miss that risk (state the miss). **SMURF** (Speed, Maintainability, Utilization/cost, Reliability, Fidelity) is the tradeoff language when two rows could both catch it: prefer the cheaper/faster/more reliable one.

| Risk | Layer |
| --- | --- |
| Pure logic, parsing, validation, reducers | Fast unit through the **public API** |
| Collaborators you own, in-process | Real objects or an owner-maintained **fake** |
| Service/HTTP contract | Owner fake or hermetic server — not a handwritten request mock |
| UI wiring (disabled, unbound, hidden) | Drive the **rendered control** (click/type), not the handler |
| Cross-system critical path | Tiny e2e set: one path per use case plus key error classes; assert system outcomes, not copy/layout |

Brainstorm **key risks** before stacking layers. Coverage meters find gaps; they do not certify quality. Cover both sides of a branch (the implicit `else` counts). Skip exhaustive combinatorics; extract predicates and cover each independently.

Prefer testing through the **public API**. Exhaustive tests of private helpers for inputs callers never pass are change-detectors in disguise.

## 3. Choose the double

Order: **real → fake → stub → mock**. Mock last.

- **Real** when it is fast, deterministic, in-process.
- **Fake**: simplified working impl of a type you (or the library owner) maintain. Keep it narrow. Contract-test fake vs real when the fake is shared.
- **Stub**: canned returns for queries. Do not `verify` getters.
- **Mock**: verify side-effecting calls whose interaction *is* the spec.

Hard rules:

- Do **not mock types you don't own**. Wrap the third-party API; mock the wrapper; test the wrapper against the real library.
- Mocking more than one or two collaborators, or a long `when`/`verify` chain, is a **seam** smell — extract a narrower port and fake that.
- Inject long-lived collaborators in the constructor; pass per-call work as method arguments. No hidden singletons, unmockable statics, or `now()` inside the logic under test.

## 4. Author the test (DAMP)

**DAMP** (descriptive and meaningful phrases) beats DRY in tests. Tests have no tests — a reader must see cause next to effect in the method body.

- **One behavior per test.** Name `unit_scenario_expectedOutcome` (or the project's equivalent). `testFoo` is not a name.
- **Arrange–act–assert** in one block. Shared `@Before` soup that lives far from the assertion is how wrong expected values sneak in.
- Helpers hide **irrelevant** construction. Scenario-relevant fields stay **visible** in the test. Builder/factory with defaults is good; silently asserting a helper default is not.
- **Literal** inputs and expected outputs. Do not compute the expectation with loops/conditionals that can share a bug with production. If a helper must contain logic, unit-test the helper.
- **Narrow assertions**: the fields under test, not the whole object/screenshot/hash order. One full-equality check for the common happy object is enough.
- **Distinct non-default values** per input (`0`, `""`, first enum can match uninitialized state and fake a pass).
- **Actionable failures**: precise matchers (`containsEntry`, `isOk` with error text) over `assertTrue(result.ok())`. Independent checks should continue (`EXPECT`) unless later asserts are meaningless (`ASSERT` file opened).
- Floats: **tolerance**, never exact equality.
- UI locators: stable test IDs, not copy or brittle XPath.

## 5. Hermetic and deterministic

No real clock, no `sleep` as synchronization, no live network/disk in unit tests, no shared files/rows assumed empty.

- Inject a clock; **tick** it.
- Wait on latches/events with a timeout, or advance a fake scheduler.
- Unique temp paths / isolated fixtures per test.
- Force rare failures (timeouts, thrown errors) through the double — live infra cannot.

## 6. Prove the test can fail

When writing or editing locally: run green, then break production (or invert the assertion) and confirm **red**. When reviewing and you cannot run: write the one concrete behavior bug this assertion would catch; if you cannot, treat it as a change-detector and do not approve.

When **refactoring tests**, put production in a known-broken state first so dropped assertions show up; then restore production. Never green-to-green "cleanup" of tests without that check.

If the only remaining test is a tautology, a mock-script of the implementation, or wiring with no logic: **do not add it**. Report the missing seam or the layer that should own the risk instead.

If project conventions conflict with a hard rule here (required mock-all-collaborators, sleep-based waits, tests of private helpers only): **stop and cite the conflict**. Do not silently follow the weaker convention.

## Review checklist

A test you would merge:

- [ ] Would fail on a real behavior bug, not only on a rename/extract
- [ ] Asserts a result/state, not a call script (unless the call is the contract)
- [ ] Public API / user-facing path, not an unreachable helper
- [ ] Cause and effect visible; name states the outcome
- [ ] Deterministic (clock/IO/uniqueness handled)
- [ ] Failure message would start the fix without extra logging
