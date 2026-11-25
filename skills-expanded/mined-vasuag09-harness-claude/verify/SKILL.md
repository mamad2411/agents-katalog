---
name: verify
description: Confirm the change actually works by running the app/feature and observing real behavior — not just that tests pass. Use late in the Verify phase, before ship. Closes the loop between "tests green" and "it works."
---

# /verify — observe it actually working

Goal: prove the feature does what the spec said, in the running app — green tests are
necessary, not sufficient.

**Default to NEEDS WORK.** Assume the change is *not* done until the running system proves each
criterion with evidence. A clean first pass is suspicious, not reassuring — look harder before
you pass it; first attempts usually have a rough edge you haven't found yet.

## Do this
1. Load the criteria from `.claude/planning/<slug>/SPEC.md` (and `PLAN.md` for what each
   task claimed to cover), if present — verify against the recorded `AC-n`, not memory.
2. Launch the app/feature the way a user would (dev server in tmux, CLI invocation,
   the affected screen/endpoint).
3. Exercise each **acceptance criterion** against the running system. For web, drive
   the browser (Playwright/Chrome) and capture a screenshot of the working state.
4. Check the unhappy paths the spec named: invalid input, empty/error states, edge
   cases. Confirm errors are handled and messages are sane.
5. Note anything observed that tests missed → add a regression test (back to `/harness-claude:test`).

## Output — coverage matrix
Build a matrix mapping **every `AC-n`** to the evidence and a verdict, and write it to
`.claude/planning/<slug>/VERIFICATION.md` (present it in the reply too; for trivial work,
the reply is enough):

```
## Verification: <title>
| Criterion | Evidence (what you ran / observed) | Verdict |
|-----------|------------------------------------|---------|
| AC-1      | <command / screenshot / log>       | pass    |
| AC-2      | (could not exercise)               | FAIL    |
```

A criterion you could not actually exercise is **FAIL**, not blank — never pass on
assumption.

## Common rationalizations (don't accept these from yourself)

| Excuse | Reality |
|--------|---------|
| "Tests pass, so it works" | Tests prove the code does what the tests say — not what the spec says. This gate exists for the gap. |
| "I can see from the code that AC-3 holds" | Reading code is assumption, not evidence. Run it. A criterion you didn't exercise is FAIL, not blank. |
| "The happy path works; edge cases are covered by tests" | The spec's unhappy paths are acceptance criteria too. Drive them in the running system. |
| "Launching the app is expensive; the diff is low-risk" | The matrix needs evidence per AC-n. "Low-risk" is a prediction; verification is an observation. |

## Red flags — stop and re-check
- A verdict says `pass` but the Evidence cell is a claim, not a command/screenshot/log.
- Everything passed on the first run and you didn't try to break it.
- The matrix has fewer rows than the spec has `AC-n`s.

## State
Patch `.claude/STATE.md`: `phase: verify`, `status: done` (or `blocked`),
`next_skill: /ship`.

## Exit criterion
**Every `AC-n` has a `pass` verdict backed by evidence.** Any unaddressed or failing
criterion blocks the exit — the matrix names which `AC-n` and why. Then `/harness-claude:ship`.
