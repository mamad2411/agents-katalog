# Verification Before Completion

Claiming work is complete without verification is dishonesty, not efficiency.

Inspired by obra/superpowers (verification-before-completion). Generalized for
any stack and any AI coding tool.

## The Rule

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this response, you cannot claim
it passes. "Should work" is not evidence. "Looks correct" is not evidence.

## The Gate

Before claiming any success or expressing satisfaction:

1. **Identify**: What command proves this claim?
2. **Run**: Execute the full command (fresh, complete -- not a cached result)
3. **Read**: Full output, check exit code, count failures
4. **Verify**: Does the output actually confirm the claim?
   - If NO: State the actual status with evidence
   - If YES: State the claim with evidence
5. **Only then**: Make the claim

Skip any step and you're guessing, not verifying.

## What Requires Verification

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| "Tests pass" | Test command output showing 0 failures | Previous run, "should pass" |
| "Linter clean" | Linter output showing 0 errors | Partial check, extrapolation |
| "Build succeeds" | Build command with exit 0 | Linter passing, "logs look good" |
| "Bug fixed" | Test for the original symptom passes | "Code changed, should be fixed" |
| "Regression test works" | Red-green cycle verified | Test passes once |
| "Requirements met" | Line-by-line checklist against spec | "Tests passing" |

## Red Flags -- Stop Immediately

If you catch yourself doing any of these, stop and run the verification:

- Using "should", "probably", "seems to", "likely"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!")
- About to commit, push, or create a PR without running tests
- Relying on a previous run instead of a fresh one
- Trusting partial verification ("linter passed, so build is fine")
- Thinking "just this once I can skip it"
- Any wording implying success without having run the command

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "Should work now" | Run the verification |
| "I'm confident" | Confidence is not evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter is not the test suite |
| "I'm in a hurry" | Unverified claims waste more time later |
| "Partial check is enough" | Partial proves nothing about the whole |

## Verification Patterns

**Tests:**
```
RUN: pytest tests/ -v
SEE: 47/47 passed
CLAIM: "All tests pass"
```

**Regression tests (TDD red-green):**
```
Write test -> Run (PASS) -> Revert fix -> Run (MUST FAIL) -> Restore fix -> Run (PASS)
```

**Build:**
```
RUN: npm run build (or cargo check, tsc --noEmit, etc.)
SEE: exit code 0, no errors
CLAIM: "Build passes"
```

**Requirements:**
```
Re-read spec -> Create checklist -> Verify each item -> Report gaps or confirm completion
```

## After Verification

Once verification passes:

1. **State what you verified**: "Ran `pytest tests/ -v` -- 47/47 passed, 0 errors"
2. **Note any warnings**: Even if tests pass, surface warnings that matter
3. **Confirm scope**: "This covers the changes in `module_x` and `module_y`"

If verification fails:

1. **State what actually happened**: "3 tests failed in `test_auth.py`"
2. **Show the output**: Include the relevant error messages
3. **Diagnose before fixing**: Understand the failure before changing code
4. **Re-verify after fixing**: Run the full suite again, not just the failing tests

## The Bottom Line

Run the command. Read the output. Then claim the result. This is non-negotiable.
