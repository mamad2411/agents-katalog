---
name: design-test-cases
description: >-
  Load this skill when deciding which inputs and scenarios a test should cover, not how to wire the
  runner: partitions, boundaries, state transitions, properties, fuzzing, failing dependencies.
  Trigger on "what should I test", "cover the edge cases", or a test file with only a happy path.
disable-model-invocation: false
user-invocable: false
license: Apache-2.0
---

# Design Test Cases

The runner, fixtures, and mocking library belong to your stack's testing skill
(`ceh-python-service:write-pytest-service-tests`, `ceh-python-library:write-pytest-library-tests`,
`ceh-web-frontend:write-vitest-playwright-tests`). This skill answers the question those do not: **which inputs,
and which scenarios.**

The task is done when every rung has its tests or a stated skip, and no test lacks a nameable
`fails_when`.

## Two failure modes, not one

- **Too few:** one happy path plus a null check. Passes on code that is wrong in every way a real
  caller will discover.
- **Too many:** thirty variations of the same equivalence class, a reference implementation written
  in the test file to check the function against, a performance budget nobody asked for. Volume
  reads as diligence and is not — it is the same coverage at several times the maintenance cost,
  and each redundant test is another thing that breaks on a legitimate change.

The second is the one you are more likely to produce. The ladder below exists as much to tell you
**where to stop** as where to start.

## Procedure

Walk the ladder in order. **Each rung has a trigger; if the trigger is absent, skip the rung and say so.**
Most functions need 1, 2, and 6 — reaching rung 7 or 9 on a pure helper is over-testing, not thoroughness.

| Rung                 | Trigger — reach for it only when                    |
| -------------------- | --------------------------------------------------- |
| 1 Partitions         | always                                              |
| 2 Boundaries         | always                                              |
| 3 Decision table     | two or more flags/enums combine to pick the outcome |
| 4 State transitions  | the thing has a lifecycle                           |
| 5 Pairwise           | the config grid exceeds ~8 live rows                |
| 6 Properties         | the function is pure and total                      |
| 7 Metamorphic        | no expected output can be written down              |
| 8 Fuzzing            | the input is attacker- or user-controlled           |
| 9 Dependency failure | the code calls something that can fail              |

### 1. Partition the input space

Group inputs into classes where every member takes the same path. **One test per class, not per
value.** Three tests for `5`, `7`, and `12` are one test wearing three hats — delete two.

For `discount(order_total, customer_tier)` the classes are tier values × {below, at, above
threshold} — not a list of amounts.

Write the classes down before the tests. If you cannot name a class's expected behavior in a
sentence, you do not yet understand the requirement.

### 2. Boundaries — where the bugs actually are

Test **the boundary and one step either side**, never the middle of a range. Run this checklist
against every parameter, and take only the rows that apply:

| Kind       | Cases                                                                                                                         |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Numeric    | `0`, `1`, `-1`, min, min−1, max, max+1, the exact threshold and threshold±1                                                   |
| Collection | empty, exactly one, exactly two, at the size limit, over the limit, duplicates, unsorted                                      |
| String     | `""`, whitespace-only, single char, at max length, over max length, unicode + emoji, embedded newline, leading/trailing space |
| Optional   | absent, present-but-null, present-but-empty — these are three different inputs                                                |
| Time       | epoch, DST transition, month/year end, leap day, expiry exactly now, timezone-naive vs aware                                  |
| Pagination | page 0, page 1, last page, page past the end, limit 0, limit above max                                                        |

"At the limit" and "one over the limit" are the two highest-yield cases in the table. Include them
whenever a limit exists; a row whose kind is not in the signature is not a gap.

### 3. Decision tables — when flags interact

Enumerate the grid, strike the impossible rows, test what remains:

| `is_member` | `has_coupon` | `cart ≥ $50` | Expected                    |
| ----------- | ------------ | ------------ | --------------------------- |
| F           | F            | F            | no discount                 |
| F           | F            | T            | free shipping               |
| F           | T            | F            | coupon only                 |
| T           | F            | T            | member rate + free shipping |
| …           |              |              |                             |

This is how you find the combination nobody implemented — the highest-yield rung against real
feature code, and the one least likely to be reached without being prompted. If the grid exceeds
~8 live rows, go to rung 5.

### 4. State transitions — including the illegal ones

Anything with a lifecycle (order, session, job, connection, feature flag). Test the legal path
once, then spend your effort on:

- **Invalid transitions** — cancel an already-shipped order, pay a refunded invoice, close a closed
  connection. These are where real systems corrupt data.
- **Repeat transitions** — fire the same valid transition twice. Idempotent, or a duplicate charge?
- **Terminal states** — every operation attempted after the terminal state.

### 5. Pairwise — when the config space explodes

Six independent booleans is 64 combinations; nobody writes 64 tests, so most people write two.
Covering all _pairs_ catches the large majority of interaction bugs in a fraction of the cases.
Generate the set (`allpairspy` in Python, a table in TS) rather than picking by hand — hand-picked
sets cluster around the defaults, which is exactly where bugs are not.

### 6. Properties — rules that hold for every input

When you can state a rule that must always be true, assert the **rule** instead of guessing inputs
(`hypothesis` in Python, `fast-check` in TS). The generator picks inputs your imagination would not,
and shrinks a failure to a minimal case.

| Shape       | Assertion                                                                  |
| ----------- | -------------------------------------------------------------------------- |
| Round-trip  | `decode(encode(x)) == x`, parse∘format, serialize∘deserialize              |
| Invariant   | output always sorted / length preserved / total unchanged / never negative |
| Idempotence | `f(f(x)) == f(x)` — normalizers, migrations, retries, upserts              |
| Oracle      | matches a slow-but-obviously-correct reference, or the old implementation  |

Reach for this whenever a function is pure and total: parsers, formatters, serializers, sorting,
money and date arithmetic, sanitizers, diffing, pagination math.

One property replaces a dozen example tests — delete the examples it subsumes, keeping only the
boundary cases from rung 2. Write an oracle only against a genuinely independent reference that
already exists, because a re-implementation in the test file shares your misreading of the spec and
doubles what has to change when the spec moves.

Record any failing case the generator finds as its own explicit test — generators are not
guaranteed to produce it again.

### 7. Metamorphic relations — when there is no expected output

Rung 6 needs you to know what the answer should be. Search ranking, recommendations, LLM output,
pricing engines with a hundred rules, image and audio processing, simulations, aggregation
pipelines — for these nobody can write the expected value down, so they end up tested with one
snapshot and a hope.

Assert instead how the output must **change when the input changes**. You never need to know the
answer, only the relationship:

| Relation                       | Example                                                                                                             |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------- |
| Permutation invariance         | reordering the query terms must not change the result set                                                           |
| Monotonicity                   | adding a matching document must not lower an existing document's rank; adding an item must not lower the cart total |
| Scaling / units                | prices in cents and in dollars must produce the same ordering; a resized image must classify the same               |
| Additivity                     | `total(a + b) == total(a) + total(b)` for a linear fee                                                              |
| Irrelevant-input insensitivity | appending whitespace, a trailing newline, or an unused field must not change the output                             |
| Consistency between paths      | the batch endpoint and N single calls must agree                                                                    |

These are the highest-value tests available for any component whose output you cannot predict, and
usually the only ones that survive a model or ruleset being swapped out.

### 8. Fuzz whatever parses untrusted input

Rung 6 asserts a rule; fuzzing asserts only that the code **does not crash, hang, or corrupt state**
on input nobody would think to write. That weak oracle is enough when the input is attacker- or
user-controlled: file uploads, request bodies, query strings, cookies, webhook payloads, config
files, protocol frames, anything `pickle`/`yaml.load`/`eval` touches.

Same generators as rung 6, with the widest strategy available (`st.binary()`, `st.text()`) and a
`try`/`except` that passes on the one error type callers handle and fails on everything else —
`MemoryError`, `IndexError`, a hang. Assert the failure **mode**, not just the absence of failure:
a rejected input must leave no partial write, no unbounded allocation, and no unclosed handle.

Sustained fuzzing of a native or long-lived parser is `atheris` / `libFuzzer` territory — a decision
to raise, not to make silently.

### 9. Force every dependency to fail

Mocks that only ever return success leave every `except` / `catch` branch unexecuted. This is the
most under-tested region of agent-written code, and it is skipped far more often than it is
overdone.

For each external dependency, make it fail once: raises the library's real exception type (not bare
`Exception`), times out, returns a malformed / empty / partial payload, returns success with a field
missing, and fails **after** a partial write. In every case assert the state left behind, not only
that the call raised — `order.status == "pending"` is the assertion that catches the real bug.

## Rules

### Before the first test

- **Name the seam.** State where the test enters (the public function, endpoint, or command a
  caller uses) and what it fakes (only what is slow, paid, or outside the process). Settle this
  before writing, with the user when one is in the loop, because a seam picked mid-test drifts
  inward to whatever is easiest to call.
- **Call the code the way users do.** Go through the public entry point, not a private helper. A
  test of the helper passes while the caller's wiring is broken.
- **See it fail first** when the behavior is new or a bug is being fixed: run the test before the
  code exists and confirm it fails for the expected reason. A test never seen red may test nothing.
- **No tautological tests.** A test that mocks the unit under test, or asserts a mock returned what
  it was told to return, passes whatever the code does. Delete it rather than count it.

### Assertion rules

- **Assert the value, not its existence.** `assert result is not None` and
  `expect(x).toBeDefined()` pass on almost every bug. Assert the actual expected value.
- **Use a literal expected value.** If the test computes the expectation with the same logic as the
  code, it will agree with the code no matter how wrong both are. Write `timedelta(minutes=90)`,
  not `parse_duration_reference("1h30m")`.
- **One behavior per test.** The failure message should name the bug without a debugger.
- **Assert the state change too**, not only the return value — what got written, what got emitted.

### How many tests is enough

Not a coverage percentage. Coverage tells you which lines ran, never whether an assertion would
have noticed them being wrong.

The suite is sufficient when: **every partition once, every boundary once, every live decision-table
row once, every invalid transition once, every dependency-failure path once.** Anything short of
that is a gap you can name. Anything past it is duplication — and duplication is a defect, not a
safety margin, so cut it before you hand the suite over.

Say which rungs you skipped and why. A test file that states "no lifecycle, so no rung 4; grid is
2 rows, so no pairwise" is reviewable; one that silently covers everything is not.

Give each new test a value line in the hand-over, not in the test file:
`<test> — protects: <behavior>; fails_when: <the defect it catches>; why_new: <what no existing
test covers>`. A test with no nameable `fails_when` or `why_new` is the duplication above: cut it.

To find out whether those tests would actually catch a defect, use `ceh-testing:audit-test-suite`.
