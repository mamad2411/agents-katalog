---
name: eng-verification
description: Mandatory checklist before claiming work is complete—run the evidence-producing command, inspect output, and only then state a result.
---

# Verification Before Completion

## Overview
Claiming success without evidence is dishonesty, not efficiency. Every status report, “done,” or “tests pass” statement requires fresh verification.

**Iron Law**
```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you didn’t run the verifying command in this message, you cannot claim it passes.

## Gate Function
```
1. IDENTIFY: Which command proves the claim?
2. RUN: Execute the full command now (fresh run).
3. READ: Inspect entire output & exit code.
4. VERIFY: Does output prove the claim?
   - If NO → report actual status with evidence
   - If YES → state claim WITH evidence (command + summary)
5. ONLY THEN: Make the claim

Skipping any step = lying.
```

## Common Claims & Required Evidence
| Claim | Required | Not Enough |
|-------|----------|------------|
| “Tests pass” | Latest test command output showing 0 failures | Previous run, “should pass” |
| “Lint clean” | Linter command exit 0 now | Partial subset, inference |
| “Build works” | Build command exit 0 | Linter pass |
| “Bug fixed” | Reproduction test now passes | Code diff only |
| “Regression test exists” | Red→Green verified cycle | Test created but never failed |
| “Agent succeeded” | Inspect VCS diff + verify outputs | Agent success message |

## Red Flags – STOP
- Saying “should/probably/seems”
- Expressing satisfaction before running verification
- Planning to commit/push/PR without a fresh run
- Trusting agent reports without checking
- Partial verification (“just ran affected tests”)
- “Just this once” or “I’m tired” rationalizations

## Rationalization Rebuttals
| Excuse | Reality |
|--------|---------|
| “Should work now” | Run the command |
| “I’m confident” | Confidence ≠ evidence |
| “Just this once” | No exceptions |
| “Agent said success” | Verify independently |
| “Partial check is fine” | Partial proves nothing |
| “I’m exhausted” | Exhaustion isn’t evidence |

## Patterns
- Tests: run and show `X/Y passing` output.
- Regression tests: demonstrate fail (red), apply fix, pass (green), revert to confirm failure if necessary.
- Requirements: re-read spec, create checklist, tick items with evidence.
- Agent work: inspect actual diff, run verification yourself.

## When to Apply
Always before:
- Claiming completion/success
- Expressing satisfaction (“Great! Done!”)
- Moving to next task
- Committing, pushing, or filing PRs
- Delegating completion to others/agents

## Bottom Line
Evidence precedes claims. Run the command, read the output, then speak. Anything else breaks trust.
