---
name: Verification Before Completion
description: Guidance for verifying work with concrete evidence before reporting completion.
---

# Verification Before Completion

> No "done" without evidence. No "works" without proof. No "correct" without output.

## Triggers

- About to claim a task is complete, done, or finished
- About to assert code works, is correct, or functions properly
- About to say "should work", "looks good", "probably fine"
- End of any implementation, fix, or modification task

## HARD GATE: Evidence Required

**Before claiming completion**, you MUST:

1. **Identify the claim** you are about to make
2. **Execute verification** (run tests, run the code, check the output)
3. **Read the output** completely — do not skim
4. **Confirm match** between expected and actual behavior
5. **Assert with evidence** — quote the output that proves correctness

## Banned Phrases

These phrases are **never acceptable** without accompanying evidence:

| Banned Phrase | Required Replacement |
|---------------|---------------------|
| "should work" | "works — here's the output: [output]" |
| "probably fine" | "verified — test results: [results]" |
| "looks correct" | "confirmed correct — [evidence]" |
| "I believe this fixes" | "this fixes — reproduction no longer triggers: [output]" |
| "this should handle" | "handles correctly — tested with [input], got [output]" |
| "the tests should pass" | "tests pass: [test output]" |
| "I think we're done" | "done — all checks pass: [evidence]" |

## Verification Types

Match your verification to the claim:

| Claim Type | Required Verification |
|------------|----------------------|
| "Bug is fixed" | Show the bug no longer reproduces + tests pass |
| "Feature works" | Show test output covering happy path + edge cases |
| "Refactor is safe" | Show all existing tests still pass |
| "Build succeeds" | Show build output with zero errors |
| "No regressions" | Show full test suite output |
| "API works" | Show request/response with expected status codes |
| "Config is correct" | Show the system using the config successfully |

## 5-Step Protocol

```
Step 1: IDENTIFY  — What claim am I about to make?
Step 2: EXECUTE   — Run the verification (test, build, lint, etc.)
Step 3: READ      — Read the FULL output, not just the last line
Step 4: CONFIRM   — Does the output match the expected behavior?
Step 5: ASSERT    — State the claim WITH the evidence
```

## Integration

- Complements `confidence-check` (pre-work) — this is the **post-work** counterpart
- TDD's GREEN phase naturally produces verification evidence
- Debug's VERIFY step (Step 4) feeds into this skill
- Branch finishing requires verification before merge/PR

## What Counts as Evidence

**Acceptable evidence:**
- Test output showing pass/fail results
- Command output showing expected behavior
- Error-free build/lint/type-check output
- Screenshots or logs showing correct runtime behavior
- Git diff showing the change + test output showing it works

**NOT acceptable evidence:**
- "I read the code and it looks right" (code review is not runtime verification)
- "This pattern always works" (appeal to authority is not evidence)
- "I tested it mentally" (mental models miss runtime behavior)
