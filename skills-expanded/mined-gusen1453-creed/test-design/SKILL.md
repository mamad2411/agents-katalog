---
name: test-design
description: Use when writing, reviewing, or modifying unit/integration tests, adding test cases, assertions, or mocks, or deciding whether a piece of code is worth testing — especially when tempted to add tests for coverage, over-mock dependencies, or write formalistic tests that just restate the implementation.
---

# Test Design

> **Output language:** answer and write artifacts in the user's own language (match their messages, not the repo's history).

## Overview

Answers **"what input should a test feed, what should it assert, and what should it mock"**. Does NOT cover the red-green-refactor rhythm (that is TDD).

**Core principle: tests protect a behavioral contract that users/callers can observe — not implementation details, and never a coverage number.**
A good test is a falsifiable spec of the contract; a bad test restates the code in another syntax.

**REQUIRED COMPANION:** for the write-test-first rhythm, see **tdd**. For module boundaries when mocks multiply, see **solid**. This skill only governs the *design quality* of cases and assertions.

## When to Use

- Adding or modifying unit/integration tests for a piece of code
- Reviewing someone's tests to judge whether they are effective or formalistic
- Deciding "is this code worth testing?" or "unit vs integration?"
- About to write a fake test under coverage pressure, deadline crunch, or sunk cost

**When NOT to use:** just running tests / reading failures → test-runner. Just following the test-first rhythm → **tdd**.

## The Iron Law (non-negotiable)

```
Break one line of production code and the test protecting it MUST turn red.
If it can't, the test is formalism — delete it and rewrite.
```

After writing each test, mentally (or actually) break the logic it guards and confirm it goes red.
**Violating the letter of the rule is violating the spirit** — "my coverage is fine" and "I follow the spirit" do not count.

## Workflow (when invoked)

Announce "Using test-design to …", then **create one todo per step**:

1. **Decide if it's worth testing** (§1): complexity in own logic → unit test; in dependency wiring → integration test. Not worth it → don't write.
2. **Write a behavior list** (§2): from the contract only — "when …, it should …", including things with no dedicated branch (e.g. "don't delete my legit content"). Each case carries its **goal / conditions / parameters** in reader-facing words (see §2).
3. **Pick representative points** (§3): equivalence classes / boundaries / decision table / state transitions / dirty input — one representative each, no homogeneous duplicates.
4. **Write assertions** (§4): assert return value / observable state / side-effect boundary only; narrow and hard; hand-write `expected`.
5. **Decide mocks** (§5): mock only the outside world; count ≤ 2-3; prefer Fake/Recording.
6. **Mutation check** (Iron Law): break production code, confirm each test goes red.
7. **Scan the rationalization table + red flags**; if any hit, stop and rethink.

## §1 Is it worth testing (ROI, not coverage)

Criterion: **is the complexity in the code's own logic, or in the interaction between dependencies?**

- Own logic (algorithms, pure computation, domain models/state machines, branch-heavy policy/validation/degradation) → **unit test**, highest ROI.
- Dependency wiring (CRUD, `A.get() → convert() → B.save()` glue) → **integration test**. The risk of such code lives exactly where mocks replace it (dependency returns null, times out, throws, transaction not committed); a unit test only proves "it runs when everything is fine" = worthless.

> Don't unit-test glue; don't integration-test algorithms.

## §2 Find cases from a behavior list

Write "when …, it should …" from the contract only. **Never count `if`s in the source.** The list MUST include items with no dedicated branch that users care about most.
If a case was "written while reading the source", delete and rewrite it — it protects the implementation, not the contract.

**Each case must be legible to someone who is not the author.** State three things in plain user/product words — before any code:

- **Goal** — what this case proves, in one sentence a non-author understands (the user-visible outcome, not the mechanism).
- **Conditions** — the state the case sets up (who / which data / what happened just before).
- **Parameters** — the concrete inputs and the expected observable result (values, and *why that value is the interesting one* — boundary, extreme, real case).

A case whose Goal is only readable by re-reading the source has failed this bar. Example:

```
Case: re-import with the same file twice
- Goal:      a re-run must not double-count rows (the bug users reported as "my totals doubled")
- Conditions: the file was already imported once; no other change
- Parameters: same file; expect the row count unchanged, and an idempotency marker set
```

## §3 Five techniques to pick representative points

1. **Equivalence partitioning**: one representative per behavior group (a second in the same group = duplicate).
2. **Boundary values**: for every threshold test `boundary-1 / boundary / boundary+1` (`>=4` must test "exactly 3" and "exactly 4" — that's the only way to catch `>` vs `>=`).
3. **Decision table**: enumerate combinations when output depends on multiple conditions; **must include "several hit at once"**; use pairwise when conditions are many.
4. **State transition**: legal path + illegal transition (use after close) + idempotency (close×2) + repetition.
5. **Dirty/malicious input**: empty, null, oversized, huge JSON, broken structure (missing closing tag, nesting), wrong type.

## §4 Assertions (positive recipe)

Assert only these three observable targets: ① return value / thrown error (type + message + code) ② observable state change ③ side-effect boundary (whether a request was sent, where to, argument shape).

- **Narrow and hard**: several precise small assertions > one big `toEqual(whole object)`.
- **Hand-written `expected`**: `expected = input.replace(sameRegex)` asserts "the regex equals itself" — always green.
- **Don't touch implementation details**: private call counts / internal branches, unless "count/order" is itself the contract (retries exactly 3 times, must not double-charge).

## §5 Mock rules

Only replace slow/flaky/side-effecting/expensive **external collaborators**. Not for bypassing hard-to-test design.

| Do Mock | Never Mock |
|---|---|
| Network/HTTP/3rd-party SDK/LLM, DB/FS/MQ, clock, RNG | The unit under test, pure functions, value objects, schemas, simple in-module collaborators |

Fidelity order: **Fake (in-memory) > Recording/contract replay > Spy > Mock framework**. Assert only contract shape:

```ts
// Good: assert the outward contract
expect(fetchMock).toHaveBeenCalledWith(
  expect.objectContaining({ method: "POST", url: expect.stringContaining("/nodes") }),
)
// Bad: lock implementation detail, red on any refactor
expect(buildPayload).toHaveBeenCalledTimes(1)
```

## §6 User perspective

Assert from the real consumer's view: end user sees results; upstream API/agent sees fields and error codes; ops sees whether logs/state can localize a problem.
Test name = **role + scenario + expectation** (forbid `case 1` / `should work`); enter through the **public entry point**, don't drill into private functions.

## §7 Shape selection

Logic-dense → **pyramid** (many unit tests at the base); business/CRUD → **diamond** (many integration tests in the middle, unit tests only for utils and core algorithms).
Integration tests catch what unit tests never can: transaction commit, dropped JSON fields, param validation, real dependency failures.

## Rationalization Table (how you lie to yourself before writing formalism)

| Excuse | Reality |
|--------|---------|
| "Just add a test to cover this branch" | Coverage isn't protection. Ask "what breaks for the user?"; no risk → don't test. |
| "Computing `expected` with a function is more accurate" | That tests "the impl equals itself" — always green. `expected` must be a hand-written literal. |
| "Mock a bit more for cleaner isolation" | Mocking a pile = split the code or go integration; you replaced the most bug-prone spot with a fake. |
| "Might as well test this glue/CRUD too" | Its risk is entirely in the mocked-out deps; use an integration test. |
| "Testing one boundary is enough" | Off-by-one is caught only at the boundary. |
| "Testing these few cases is more thorough" | Multiple cases in one equivalence class are homogeneous duplicates = formalism. |
| "Shipping soon, verifying the call is enough" | `verify(called once)` protects nothing. Short on time → write less, not fake. |
| "Snapshotting the whole object is easiest" | Any unrelated field change breaks it brittly, and hides which contract failed. |
| "This test is hard to write, mock around it" | Hard to test = hard to use — a design signal; fix the code. |
| "Looks professional / 80% is required" | 100 impl-copying tests protect nothing. Quality, not quantity. |

## Red Flags — stop immediately

- Adding a test just to light up a line/branch
- `expected` computed with production logic instead of hand-written
- A "unit test" mocking 3+ dependencies
- Assertions are all `verify(...)` / `toHaveBeenCalled`, none on return value/state
- Test names like `test1` / `should work` / `case 2`
- Testing getters/setters/DTO conversion/pure glue
- "Breaking the code probably wouldn't turn this test red"

**Any hit → stop, return to: "what user-visible bad outcome does this test prevent?" Can't answer → don't write it.**

## Worked Example (techniques strung together)

Under test: `strip(prompt)` removes evidence dumps and keeps short instructions; a paragraph with ≥4 `[n]` citations is dropped.

**Behavior list → cases (not branch-following):**

```ts
// role+scenario+expectation; narrow/hard assertions; hand-written expected
test("subagent receiving a prompt with task_result has the dump stripped but instructions kept", () => {
  const out = new HeuristicDumpStripper().strip(
    "Summarize in three sentences.\n<task_result>…huge dump…</task_result>\nPrefer the latest conclusion.",
  )
  expect(out).not.toContain("<task_result>")        // dump gone
  expect(out).toContain("Summarize in three sentences")  // leading instruction kept
  expect(out).toContain("Prefer the latest conclusion")  // trailing instruction kept
})

// Boundary values: threshold >=4, test "exactly 3 kept / exactly 4 dropped"
test("paragraph with exactly 3 citations is kept", () => {
  expect(strip("conclusion [1][2][3] still body")).toContain("still body")
})
test("paragraph with exactly 4 citations is dropped", () => {
  expect(strip("noise [1][2][3][4] should be removed")).not.toContain("should be removed")
})

// Dirty input + fallback: non-empty when everything is stripped
test("falls back to truncated original (non-empty) when stripping empties it", () => {
  expect(strip("<task_result>only dump</task_result>").length).toBeGreaterThan(0)
})
```

**Mutation check:** change `hits.length >= 4` to `>= 5`; "exactly 4 dropped" MUST go red. All green → the threshold isn't tested → rewrite.

## Checklist (run once per test)

- [ ] Worth testing? complex logic → unit; glue → integration
- [ ] Cases come from a behavior list, not copied from source branches
- [ ] One representative per equivalence class; boundary±1 per threshold; "several hit at once" covered
- [ ] One case each for empty/oversized/broken/malicious input
- [ ] Assert return value/observable state/side-effect only; narrow and hard; `expected` hand-written
- [ ] Mock only external IO/time/RNG; the unit's logic is real; mock count ≤ 2-3
- [ ] Test name = role+scenario+expectation; enter via public API
- [ ] Mutation check passes: break production code and this test goes red
