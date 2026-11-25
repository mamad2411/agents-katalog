---
name: tdd
description: "Design black-box tests at the program's edge by default, rare unit tests, failing-before regressions and verification of critical properties; use for test design, TDD, pruning suites, model checking and verification drift, with explicit evidence limits."
---

# TDD

Follow the consuming project's instructions and requested scope; use the
[portable defaults](../orbyn-workflow/references/project-policy.md) only where guidance is missing.

Respect tests excluded by the current user, session or consumer policy; this skill
grants no production or live-provider authority.

## Choose the test: black box first

Test what the program does, not how. Unit tests are the exception. The repository's
own test policy, or its `verification.test_layer` in the harness, comes first where
it says otherwise.

1. **Default: a black-box case at the program's edge.** Feed a real input to the CLI,
   endpoint, job, screen or, for a library, its public API and compare what comes out with an expected file: output,
   exit code, error, and the effects someone can see (rows written, files changed,
   requests sent to outside systems). One case per behaviour a user or caller relies
   on, failures included. How to build the harness: [golden cases](references/golden-cases.md).
2. **A unit test only when all three hold:**
   - a silent break would be costly: money, deleting or moving files, secrets,
     permission checks, stored-data formats;
   - the behaviour cannot be reached or checked cheaply from the edge;
   - the logic has many edge cases (parsing, rounding, date math), where a table of
     inputs is clearer than many whole-program runs.

   Otherwise write no unit test.
3. **Never** test private helpers or internal call order, and never mock our own
   code. Fake only systems outside ours, such as a payment provider.

Agent behaviour and whole outcomes get an [answer-key](../orbyn-workflow/references/answer-key.md)
check or an eval. Skill text, docs, thin glue and one-off scripts get no test; UI gets
a visual check. Record the choice in one line in the task record or PR, for example
`Tests: black-box, 3 cases`, `Tests: unit, rounding table unreachable from the API` or
`Tests: none, docs only`.

## Method

1. **Freeze the observed defect,** expected invariant and the smallest observable contract at a practical authorized test boundary. Use the [reproduction contract](../how/references/reproduction.md) for baseline, fixture and runner discovery.
2. **Write one regression** at the owning boundary (a black-box case at the edge unless a unit test meets the three conditions above, [cover each behavior once](references/test-strategy.md#cover-each-behavior-once)), exercising the actual production path rather than a copy of the implementation. Assert state or externally meaningful behavior rather than private helper calls; [two-edit check](references/test-strategy.md#judge-a-test-by-two-edits). Keep mocks on unavailable effects at real effect/adaptor boundaries, away from private helper choreography.
3. **Run it against the unchanged candidate first.** Confirm the intended test actually ran; zero selected tests, an unrelated setup error or a skipped mode is not regression proof. Check that it fails for the reported contract violation, not a missing dependency or broken fixture. Retain failing attempts. Report which red you saw: an assertion failing on the violation is the strongest; a compile error because the new field or route does not exist yet shows the test needs the change, not that its assertion catches the defect; a test that also passes against a no-op is a pin, not red evidence. A test that expects a 404 passes when the route itself is missing, so assert that the handler answered.
4. **Make the smallest coherent production correction,** then rerun the same case, directly affected controls and relevant adjacent cases. Never weaken assertions to obtain green. Adding the regression to the existing test file is expected; a key that restores protected tests judges the fix by the original tests.
5. **Extend one failing contract at a time** from observed behavior. Confirm the first signal catches the defect before writing more, rather than a speculative batch.
6. **Refactor only after the meaningful signal is green.** Internal reorganization should preserve useful behavior tests, so keep contract tests rather than coupling them to the new implementation.

For a stale version write, place the regression at the API/version boundary. Arrange an existing record and newer version, send the stale mutation, and assert both rejection and unchanged persisted data. A snapshot of the error string alone misses a write that succeeds before returning an error. Include a legitimate current-version control when it distinguishes an overbroad rejection. Add a UI check only when the changed user flow needs separate evidence and that check is authorized.

A model that reviews its own code repeats the blind spot that produced it, so its
"looks correct" is not evidence. Give every fixed bug an automated test, and make
it cover every path that can reach the bug, including the alternate ones (sandbox
and production, flag on and off, cached and fresh). Synthetic example: a field was
added to the production query but not the sandbox one; a test run over both modes
fails at once.

## When the ideal test is out of reach

- Baseline execution unavailable: record that limit. A passing new test without a demonstrated baseline failure is weaker regression evidence, so state that distinction and do not call it failing-before evidence.
- The practical test requires unrelated harness churn or unrealistic mocks: explain the limitation and use the closest authorized executable check: a targeted script, a reproduction command, browser automation, a snapshot comparison, a log assertion or a focused integration check. Keep it on the bug, without broad fixture churn.
- No production databases or unapproved live-provider calls. Production databases and paid providers require their own applicable authority. Read [development](../orbyn-workflow/references/project-policy.md#development-resources) for guarded database and package prerequisites.

## Read when needed

- A repair that retains a previously ignored value: the [propagated-value method](references/propagated-values.md).
- A critical invariant, event-order race, explicit formal verification request or stale verification model: [property verification](references/formal-verification.md) and its [drift review](references/verification-drift.md). Choose tools from the property and real code, agree the intent both ways, list what the proof trusts, plant a failing control per clause, and distinguish model results from implementation evidence. Skip the formal model for ordinary small UI edits.
- Code with no tests that is about to be rewritten or ported: record the original's behaviour as its characterization suite ([rewrite parity](../figure-it-out/references/rewrite-parity.md)).
- A request to review, prune or speed up an existing suite, or one grown by generated tests: [suite audit](references/suite-audit.md). It classifies weak tests, moves behaviour to black-box cases before deleting unit tests, keeps those tied to a named risk and records what is given up.
- Requested test design: [test strategy](references/test-strategy.md) to select the real boundary, fixtures, failure controls and execution scope. A plan can be the requested output; this skill does not turn every test request into mandatory production edits.
- Model-powered application quality: pair deterministic permission/state tests with [task evaluations](../orbyn-ai-application/references/evaluations.md). A correct schema or one expected answer is not a reliability estimate; preserve held-out cases, repeated-trial failures and critical slices. Ordinary deterministic changes do not require live model calls.
- Clocks, async cleanup, readiness, module identity or runner legs that can hide the assertion: [test reliability](references/test-reliability.md). Preserve actual production/fixture boundaries and first-attempt evidence.
- Actual Expo/RN requested-screen, binary/device and native evidence: [mobile verification](references/mobile-verification.md). Deterministic fixtures and screenshots do not close missing platforms or paid-service cells.
