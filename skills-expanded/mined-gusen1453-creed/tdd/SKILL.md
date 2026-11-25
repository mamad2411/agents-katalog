---
name: tdd
description: "Use when implementing any feature, bug fix, refactor, or behavior change, before writing production code."
---

# TDD

> **Output language:** answer and write artifacts in the user's own language (match their messages, not the repo's history).

## Overview

**Write the test first. Watch it fail. Write the minimal code to pass. Refactor.**

**Core principle: if you didn't watch the test fail, you don't know it tests the right thing.**

**REQUIRED COMPANION:** use **test-design** for *what* to feed, assert, and mock. This skill is only the **rhythm**. Formalistic RED tests are still forbidden — a failing theater test proves nothing.

## When to Use

**Always:** new features, bug fixes, refactoring, behavior changes.

**Exceptions (ask the human first):** throwaway prototypes, generated code, pure config with no behavior.

Thinking "skip TDD just this once"? Stop — that's rationalization.

## The Iron Law (non-negotiable)

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Wrote code before the test? **Delete it. Start over.**

**No exceptions:**

- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete

**Violating the letter is violating the spirit.**

## Workflow (when invoked)

Announce "Using tdd to …", then **one todo per cycle step**:

1. **RED** — one failing behavior test (apply test-design: contract, narrow asserts, hand-written `expected`)
2. **Verify RED** — run it; confirm fail for the *right* reason (missing feature, not typo/error)
3. **GREEN** — minimal production code to pass
4. **Verify GREEN** — run it; all relevant tests pass; output pristine
5. **REFACTOR** — clean up; stay green; no new behavior
6. **Repeat** — next behavior → next RED

Bug found later? Write a failing reproduction test first, then the same cycle.

## Red → Green → Refactor

### RED — write one failing test

One behavior. Clear name (role + scenario + expectation). Real collaborators unless IO forces a Fake/Recording (see test-design).

```ts
test("retries failed operations 3 times", async () => {
  let attempts = 0
  const operation = () => {
    attempts++
    if (attempts < 3) throw new Error("fail")
    return "success"
  }
  expect(await retryOperation(operation)).toBe("success")
  expect(attempts).toBe(3)
})
```

Bad: vague name, asserts only on mock call counts, or `expected` computed with production logic.

### Verify RED — mandatory

Run the targeted test. Confirm:

- Fails (not errors out from typos/imports)
- Failure message matches the missing behavior
- If it **passes** immediately → you're testing existing behavior or asserting nothing real — fix the test
- If it **errors** → fix the harness, re-run until it fails correctly

### GREEN — minimal code

Simplest code that passes. No extra features, no drive-by refactors, no YAGNI options objects.

### Verify GREEN — mandatory

Run again. All related tests pass. No new warnings/errors ignored.

### REFACTOR

Only after green: names, duplication, helpers. Keep tests green. Don't add behavior (new behavior → new RED).

## Good vs bad tests (rhythm lens)

| | Good | Bad |
|--|------|-----|
| Size | One behavior; "and" in the name → split | Kitchen-sink test |
| Name | Describes observable behavior | `test1` / `works` |
| Proof | You saw RED for the right reason | Passed on first run |
| Depth | Asserts contract (test-design) | Only `toHaveBeenCalled` / coverage lighting |

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "I'll test after to verify" | Passes immediately prove nothing. You never saw it catch the bug. |
| "Tests after achieve the same goals" | After = "what does this do?" First = "what should this do?" |
| "Already manually tested" | Ad-hoc, no record, can't re-run. |
| "Too simple to test" | Simple code breaks. A focused test is cheap. |
| "Deleting X hours is wasteful" | Sunk cost. Unverified code is debt. Delete and restart. |
| "Keep as reference / adapt while testing" | That's testing after. Delete means delete. |
| "Need to explore first" | Explore, then **throw away** exploration; start TDD clean. |
| "TDD slows me down" | Debugging in prod is slower. Pragmatic = test-first. |
| "Hard to test" | Design smell. Simplify the interface (test-design § hard-to-test). |
| "Existing code has no tests" | You're changing it — add the failing test for the behavior you touch. |
| "Just this once / spirit not ritual" | Letter = spirit. No exceptions without the human. |

## Red Flags — delete code and restart

- Production code before a failing test
- Test written after implementation
- Test passes on first run
- Can't explain why RED failed
- `--no-verify` / skipping the test run "to save time"
- Keeping pre-test code as "reference"
- "Pragmatic shortcut" / "this is different because…"

**Any hit → delete the production code. Start over at RED.**

## Anti-patterns (quick)

- Testing mock behavior instead of the unit
- Test-only methods on production types
- Mocking a pile of neighbors (usually glue → prefer integration, or redesign — test-design §1/§5)

## Checklist (per behavior)

- [ ] Worth a real test? (test-design ROI) — else don't fake TDD on glue
- [ ] RED written from contract; watched fail for the right reason
- [ ] GREEN is minimal; verify pass
- [ ] REFACTOR stays green; no new behavior smuggled in
- [ ] Mocks only for external world; asserts are narrow and hard

## Hand-off

**Transition gate** — when a feature slice is done (or before leaving tdd), ask the user (one AskUserQuestion; never auto-advance):

```
A) Recommended: Proceed → review (then commit-and-push)
B) Review first — run **review** on the code slice (`references/code.md`; upstream = plan tasks / spec), then return to this gate
C) Adjust — back into a tdd RED→GREEN cycle for the issue, then return to this gate
D) Something else (I will type it)
```

- Case quality unclear → **test-design**
- Boundaries / mock piles → **solid**
- Feature shape unclear → **grill** → **write-spec** first, then TDD
- To ship → **review** then **commit-and-push**
