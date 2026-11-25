---
name: test-generation
description: "Call when tests cover only the happy path, a bug was found without a case, or coverage is requested. Trigger words (RU+EN): покрой тестами, напиши тест, а если подать мусор, краевые случаи, тест на регрессию, что если пусто / cover with tests, write a test, what if we feed garbage, edge cases, a regression test, what if empty. GENERATES beyond the happy path: adversarial inputs, property/fuzz, golden snapshots, scenario matrices. Complements gate (coverage) and diagnosing (a loop for one bug)."
---

# Test generation (beyond the happy path)

Coverage 100% is a necessary floor but not a sufficient one: a covered happy path gives false
confidence. A test catches a bug only if it asserts what WILL BREAK. Generate tests by the types
below, not "called it and checked it did not crash".

## Types (roughly by the cost of the bug found)

1. **Adversarial inputs.** Not "a valid X" but a hostile one: empty/None, huge, negative,
   unicode/emoji, injection (`'; DROP`, `../../etc`), duplicates, out-of-order, concurrency.
   Rule: for every user INPUT — a hostile-input test (see the trigger in [[task-cycle]]).
2. **Property / fuzz.** Not examples but an INVARIANT: "for any input the property holds" (round-trip
   `decode(encode(x))==x`, monotonicity, sum preservation). 1000 random inputs → hunt a
   counterexample. Libraries: hypothesis (py). "Sometimes wrong" is debugged only this way (see
   [[diagnosing]]).
3. **Golden / snapshot.** A complex deterministic output (generated HTML, a schema, an API response)
   → a snapshot of the reference in a file, the test compares. The reference diff is visible in
   review. NOT for non-deterministic output.
4. **A scenario matrix.** A feature with axes (role × state × flag) → a table of cases, not one.
   Empty cells of the matrix = an uncovered path = value (like empty Process Brief cells).
5. **A regression for the bug.** Each fix → a test that REDDENS on the old code (otherwise it did not
   prove it fixed anything). The form reference is the kit `${CLAUDE_PLUGIN_ROOT}/presets/example-service/`:
   three classes (fail-open validation · an unhandled external call · a secret in a log), each with a
   fix and a bug version; one test is green on the fix and red on the bug. Copy the FORM, not the
   examples.

## The criterion of a good test

Asserts the EXACT symptom (not "did not crash"); is deterministic (seed the RNG, pin the time,
isolate FS/network); is fast (cache the setup). A 2-second deterministic test is a superpower; a
30-second flaky one is nearly useless ([[diagnosing]]).

## The case form (mandatory for every test)

The types above are about WHAT to cover; this section is about the form without which the covered is
not proven. In full, with examples and reasons — `${CLAUDE_PLUGIN_ROOT}/presets/python/tests.md`;
brought here is what is violated most often.

1. **A counter-case beside "it fired".** For each "the mechanism fired" test — a "and here it must
   not" test. → *Stop if* a mechanism that answers "yes" ALWAYS passes your suite green: the test
   proves only the fact of firing, not that the mechanism looks at the input. (Exactly how a guard
   that blocks everything and a validator that rejects any input pass green.)
2. **The case names the defect class it guards.** One line in the docstring: not "checks
   parse_date" but "a date with no year does not silently become the current year". → *Stop if* you
   cannot decide from the test whether it may be deleted: it is unclear what it held.
3. **The test name is a scenario, not a module name.** One module is covered by several tests:
   `test_expired_token_is_rejected`, not `test_auth`. → *Stop if* a red run names only the area, not
   the broken behavior.
4. **Idempotency — by a call in a loop.** "A repeated call breaks nothing" is a separate property,
   one call does not check it. → *Stop if* the operation creates/sends/charges and the test calls it
   once.
5. **A seam is checked by a real seam.** A test where both ends of the seam are substituted proves
   the mocks agreed with each other. → *Stop if* the suite is green but the system does not work at
   that seam: slicing "a test per function" covers the details and not the path they are called by
   in production.
6. **A mutant reddens.** Break the guarded mechanism (remove the check, return a constant, drop the
   condition) — the test must redden. → *Stop if* it is green on the broken code: the test guards
   not what is declared, and its green means nothing. Cheaper to delete than to keep: a suite with a
   false green is more dangerous than a missing one, because it is cited as proof.

## Mock antipatterns (mock hygiene, not coverage)

**First — is a substitution needed at all.** Dependencies are real by default; what is substituted
is the EXTERNAL process boundary: network, a queue, the clock, file storage, a call into a foreign
runtime. Your own code between your own modules is not substituted. A separate case is YOUR OWN
scenario the orchestrator touches: its double lives by different rules (see the form table in the
test layer), and the two cases must not be confused. The substitution form and its home are in
`${CLAUDE_PLUGIN_ROOT}/presets/python/tests.md`: the mechanics live in a typed boundary fixture, not
in the case body, and a double of an external system and an observer-double of your own scenario
have a DIFFERENT form (a real signature vs free arguments) — confusing them means rewriting all
doubles on every refactor.

Below is hygiene for when a substitution was unavoidable. Each item has a gate question "stop if…":

1. **Do not test the mock's behavior.** An assert on a value you returned from a `*-mock` yourself
   checks the mock, not the code. → *Stop if* the test fails only from a change to the mock, not the
   production code: test real behavior or do not mock that level.
2. **No test-only props in production.** A method in a production class living ONLY so a test can
   substitute or reset a dependency (`reset()`, a setter to inject a double) is dead risk in
   production. → *Stop if* the production method calls no production path: keep injecting/resetting a
   double in a fixture or a test utility (resetting the mock itself — item 5).
3. **Mock at the right level.** Understand the real method's side effects and whether the test
   depends on them; mock the LOWER layer (slow/external: network, disk, time; cf. the mock-layer
   trigger in [[task-cycle]]), not the high-level method whose logic the test checks. → *Stop if* the
   mock replaces exactly the function the test is written for.
4. **Mock the FULL response schema.** Mirror the WHOLE form of the real response, not only the fields
   needed now: a partial mock silently fails downstream when the code reaches a missing field. →
   *Stop if* the mock response is poorer in form than the real contract.
5. **Isolate the mock's state between tests.** A mock not reset between tests (call-count,
   `side_effect`, a response queue) leaks into a neighboring test → a false pass/fail. → *Stop if* a
   mock lives longer than one test without an explicit reset / fixture scope. (The polluter is caught
   by find-polluter in [[diagnosing]].)

## How much to run

Along the way there is a targeted run of the subject and a mutation probe of the edit — by them it is
judged whether the case guards what is declared. The full suite — once, on what leaves the machine
([[gate]]).

## When NOT to apply

A trivial pure getter/config with no branching — the happy path is enough, do not inflate.
Non-deterministic output (timestamps/order) — golden cannot be used, normalize first. Property where
there is no invariant — a waste.

Related: [[gate]] (coverage+N+1), [[diagnosing]] (a loop for a specific bug), [[task-cycle]] (the
"hostile input FIRST" trigger).
