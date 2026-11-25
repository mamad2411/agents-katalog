---
name: four-question-validation
version: 1.0.0
description: |
  Post-implementation hallucination detection. Four questions to verify work
  is complete, correct, and evidence-based. 94% detection rate for AI errors.
  Inspired by SuperClaude Framework.
triggers:
  - "four question check"
  - "validate my work"
  - "hallucination check"
  - "verify implementation"
---

# Four-Question Validation

Run this check after ANY implementation before claiming work is done.

## The Four Questions

### Q1: All tests passing?

- Run the actual test suite. Do NOT assume tests pass.
- If no tests exist, write them first.
- Check: `npm test`, `npx vitest`, `npx playwright test`, or project-specific test command.
- FAIL if: any test fails, or no tests exist for new code.

### Q2: All requirements met?

- Go back to the original request or spec document.
- Check each requirement individually against the implementation.
- List each requirement with a checkmark or X.
- FAIL if: any requirement is unmet, partially met, or interpreted differently than intended.

### Q3: No assumptions without verification?

- List every assumption you made during implementation.
- For each assumption, note whether it was verified or just assumed.
- Common unverified assumptions:
  - "This API endpoint exists" (did you check?)
  - "This function returns the right type" (did you verify?)
  - "This file path is correct" (did you confirm?)
  - "This will work in production" (did you test it?)
- FAIL if: any critical assumption was not verified.

### Q4: Evidence for each claim?

- For every claim you make ("this works", "this is faster", "this handles the edge case"):
  - Show the evidence: test output, screenshot, log, or code reference.
  - If you can't show evidence, you can't make the claim.
- FAIL if: any claim lacks supporting evidence.

## Scorecard

| Question | Status | Evidence |
|----------|--------|----------|
| Q1: Tests passing | PASS/FAIL | _test output_ |
| Q2: Requirements met | PASS/FAIL | _checklist_ |
| Q3: No unverified assumptions | PASS/FAIL | _assumption list_ |
| Q4: Evidence for claims | PASS/FAIL | _evidence links_ |

**Overall: PASS** (all 4 green) or **FAIL** (any red → fix before done)

## Detection Rate

This pattern catches 94% of AI hallucinations and errors when applied rigorously. The most common catches:
- Tests that weren't actually run (Q1)
- Requirements that were subtly misinterpreted (Q2)
- API endpoints or functions that don't exist (Q3)
- Performance claims without benchmarks (Q4)

## Credit

Inspired by the SuperClaude Framework's four-question validation pattern.
