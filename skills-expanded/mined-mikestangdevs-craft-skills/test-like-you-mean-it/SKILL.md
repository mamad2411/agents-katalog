---
name: test-like-you-mean-it
description: "Use after building a feature, model, or fix that has to be trusted, before calling it done. Replaces smoke tests and tests written to pass with an adversarial wave — invariants, edge regimes, independent cross-checks, hostile inputs — where findings are expected and get fixed. Use when tests were written alongside the code they test, or a green suite still doesn't earn confidence."
---

# Test Like You Mean It

## The failure mode this fixes

Agents write tests the way a student grades their own exam. They built the code, they want the code to work, so they write tests that confirm the happy path and assert whatever the code currently returns. The suite goes green, everyone relaxes — and nothing was actually verified. A test written to pass is worse than no test: it's a green light bolted over a blind corner.

The tell: tests that mirror the implementation ("returns X when given Y" where X was copied from the function's output), no test that could conceivably fail, no edge regimes, no invariants. Smoke tests presented as verification.

This skill replaces that with an adversarial wave: after the build, you switch sides. You are no longer the author defending the code — you are the reviewer trying to break it. Finding a real defect is the *expected outcome*, not an embarrassment.

## When to Use This Skill

- A feature, calculation, model, or migration just landed and the next step would be "looks done"
- The only tests that exist were written in the same session as the code they test
- The suite passes but you couldn't say *what property of the system* it proves
- The domain has ground truth to check against — math identities, conservation laws, a reference implementation, a spec, known real-world values
- Someone (including you) is about to say "tests pass" as the reason to ship

**Don't use when:** the change is trivial plumbing with no behavior (a rename, a re-export), or you're in a genuine throwaway spike. Don't use it as a reason to write 100 shallow tests — ten tests that could fail beat a hundred that can't.

## Instructions

### 1. Switch sides

Before writing a single test, write down (briefly) how this code *could* be wrong in ways the existing tests wouldn't catch. You're drafting an attack plan, not a checklist of what it does. If you can't name a way it could be wrong, you don't understand it yet — go read it again.

### 2. Test properties, not outputs

The weakest test asserts the function's current output. The strongest asserts something that must be true *independent of the implementation*:

- **Invariants** — totals conserved, monotonicity, bounds (a percentage stays in [0,100], energy out ≤ energy in, a sorted list stays sorted)
- **Cross-checks** — compare against an independent route to the same answer: a closed-form solution, a reference library, a hand-computed case, the spec's worked example
- **Round trips** — serialize/deserialize, encode/decode, apply/invert
- **Known answers** — real-world values the output must reproduce (the documented rate, the published constant, last month's verified report)

### 3. Probe the regimes where things break

Happy-path inputs exercise the code; boundary inputs verify it. Zero, negative, empty, one, max, NaN-adjacent, timezone edges, unicode, concurrent access, the degenerate config where a denominator goes to zero. Pick the regimes that are *plausible in production*, not just exotic.

### 4. When a test fails, fix the code — almost always

A failing adversarial test is the skill working. The order of suspicion: (1) the code is wrong, (2) your test's expectation is wrong, (3) the spec is ambiguous. Only change the test when you can articulate *why reality disagrees with it* — never to make the run green. If you weaken an assertion or delete a check, say so out loud in the report and justify it; silently loosening a test is the exact failure mode this skill exists to kill.

### 5. Report findings, not just counts

"47 tests, all passing" says nothing. Report what was *attacked* and what was *found*: which invariants were checked, which regimes probed, what broke, what was fixed, and what residual risk remains untested (and why).

## Output format

```
Adversarial test wave: <component>
Attack plan: <the 3-6 ways this could plausibly be wrong>
Invariants tested: <list>
Regimes probed: <list>
Findings: <N real defects — each: what, root cause, fix>  ← finding 0 on first wave is suspicious
Expectations changed: <any test whose assertion was altered, with justification>
Not tested: <what remains unverified and why>
```

## Anti-Patterns

| Anti-Pattern | Why it defeats the skill |
|---|---|
| The mirror test | asserting whatever the implementation returns. That tests nothing but determinism. |
| Volume theater | 80 generated permutations of the same shallow assertion, presented as rigor. |
| Quiet loosening | widening a tolerance, deleting an assert, or skipping a case to get green, without flagging it. |
| "First wave found nothing, ship it" | a clean first adversarial pass usually means the attack plan was soft. Sharpen it once before believing it. |

## Mental Model

> You wrote the code as its advocate. Now prosecute it. A test suite is only worth what it could have caught — if no test in the wave *could* have failed, you didn't test, you decorated.
