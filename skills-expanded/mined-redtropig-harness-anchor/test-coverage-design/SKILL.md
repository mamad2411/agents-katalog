---
name: test-coverage-design
description: Use when deciding what to test, reviewing whether a feature is adequately covered before calling it done, or when tests pass but you're unsure they exercise the real risks. Derives coverage obligations from code + spec, finds gaps (including paths outside the test runner's scope), and designs a minimal, edge-case-first test set. Dispatches the coverage-analyst subagent. Generic (language-agnostic).
---

# Test Coverage Design

A passing test suite proves only that *the tests you wrote* pass — not that they exercise what the
feature actually requires or where the code is actually risky. This skill is the **post-implementation**
discipline for closing that gap: derive what *must* be tested, check it against what the suite runs, and
design the smallest test set that covers it.

## Altitude — where this sits vs. superpowers TDD

| Phase | Owner | What |
|---|---|---|
| **Pre-implementation** (spec-driven, test-first) | superpowers `test-driven-development` | Red-green-refactor; write the failing test *before* the code. Deliberately **code-blind**. |
| **Post-implementation** (code-aware) | **this skill + `coverage-analyst`** | Read the actual code for risk; confirm the spec's obligations are met **and actually run**. |

Do **not** reimplement TDD's process here. Use TDD first for the spec-driven cases; use this *after* the
code exists for the cases TDD structurally can't see (its discipline forbids looking at the
implementation). The design techniques in `coverage-reference.md` serve **both** phases.

## Two failure modes this prevents

1. **Obligation gap** — a behaviour / edge case / risky construct the feature needs is never tested
   (e.g. nothing checks `checksum()` on large input, so a fixed-width-accumulator overflow ships).
2. **Run-scope gap** — a test or binary that *would* exercise the risk exists but the project's runner
   never executes it (e.g. a binary built with `add_executable` but never `add_test`-registered, so
   `/sanitize` + `/verify` silently skip it and report "clean").

These are classic confident-wrong traps, and a line-coverage tool misses them: the line can run under a
small input yet never at the magnitude / in the scope where the bug bites.

## Method (gray-box, post-implementation)

1. **Black-box obligations from the spec** — `feature_list.json` description + `done_criteria`,
   `AGENTS.md`, any `docs/superpowers/specs|plans/*`. List behaviours incl. malformed / empty /
   boundary inputs the spec implies.
2. **White-box / risk obligations from the code** — scan the implementation against the risk-construct
   checklist in `coverage-reference.md`. These are the ones the spec never names but the code reveals.
3. **Check both against the suite AND the run scope** — for each obligation, is there a test the runner
   *actually executes* that exercises it? An unexercised obligation, or one exercised only by a binary
   outside the runner's scope, is a gap.
4. **Design the minimal closing set** — equivalence-partitioning + boundary-value + pairwise for fewest
   cases, widest coverage (see `coverage-reference.md`).

## Reliability — because code AND tests are both LLM-generated

A different agent writing the tests decorrelates *context* bias, not *shared model priors*: the model
that wrote `int h` may also not think to test for overflow. So prefer defenses that don't depend on the
model's judgement:

- **Oracle-independent tests first** — metamorphic ("compute it a second, wider / independent way and
  compare"), differential (vs. a trivially-correct reference), property / invariant. Their correctness
  comes from the *relation*, so they catch the bug **even if the test author shares the blind spot** —
  the reliable way to test oracle-free code like a checksum.
- **Scan the risk checklist** — externalises known traps so you don't rely on recalling them.
- **Escalate, never fabricate** — if a requirement is ambiguous or you can't derive an oracle, ask the
  user. A guessed "expected value" just re-encodes the blind spot.

## Dispatch the coverage-analyst (fresh context)

For anything past a glance — risk constructs, large-data / numeric paths, "is this really covered before
I mark it done" — dispatch the **`coverage-analyst`** subagent (fresh context = it didn't write the
code, so it reads adversarially). Run **`/test-plan`**, or dispatch it directly via the `Task` tool. It
returns obligations + run-scope gaps + a minimal oracle-independent-first test set, persisted to
`.harness-anchor/coverage-<ts>.md`. It is **read-only** — it recommends; you write the tests, then
`/verify` + (for C/C++) `/sanitize`.

## The gate

**A green suite that skips the risk path is a false pass.** Before flipping `feature_list.json` to
`pass`, the spec / code obligations must be exercised by tests the run actually executes — record the
`coverage-<ts>.md` report as evidence. See `anti-hallucination-gates` (the "Coverage obligations"
criterion).

## Related

- `anti-hallucination-gates` — the Default-FAIL evidence gate this feeds
- superpowers `test-driven-development` — the pre-implementation, spec-driven counterpart
- `/verify` + `verification-runner` — runs the registered suite (this finds what's *missing* from it)
- `cpp-sanitizers` — for C/C++, the run-scope caveat + `ub-failure-patterns.md` (the C/C++ risk arm)
- `docs-lookup` — for unfamiliar test frameworks / coverage tools (don't guess)
- `coverage-reference.md` (sibling) — design-technique catalog + risk-construct checklist
