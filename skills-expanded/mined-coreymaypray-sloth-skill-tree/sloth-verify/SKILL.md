---
name: sloth-verify
description: "Use when about to claim a Maycrest deliverable is complete, fixed, or passing — before committing, opening a PR, or telling the client, requiring fresh verification evidence first."
---

# Sloth Verify — Evidence Before Claims 🦥

## Overview

Telling a client work is done without verifying it is dishonesty, not efficiency. At Maycrest
the deliverable is trust as much as code — a false "it works" costs us the relationship.

**Core principle:** Evidence before claims, always.

**Violating the letter of this rule is violating the spirit of this rule.**

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this message, you cannot claim it passes.

## The Gate Function

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

## Common Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build command: exit 0 | Linter passing, logs look good |
| `tsc` clean | `tsc --noEmit`: 0 errors | Editor squiggles gone |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Subagent completed | Git diff shows the changes | Agent reports "success" |
| Requirements met | Line-by-line checklist vs. spec | Tests passing |

## Forbidden Phrases — STOP

Never ship these unless you've just run the verification:

- "should work now", "probably", "seems to"
- Expressing satisfaction before evidence ("Great!", "Perfect!", "Done!")
- About to commit/push/PR without verification
- Trusting a subagent's success report
- Relying on partial verification
- "just this once" / "I'm tired, ship it"
- **ANY wording implying success without having run verification**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter ≠ compiler |
| "The client's waiting" | A false claim costs more than 30 seconds |
| "Subagent said success" | Verify independently via the diff |
| "I'm tired" | Exhaustion ≠ excuse |
| "Different words so the rule doesn't apply" | Spirit over letter |

## Key Patterns

**Tests:**
```
✅ [Run test command] [See: 165/165 pass] "All tests pass"
❌ "Should pass now" / "Looks correct"
```

**Regression tests (TDD red-green):**
```
✅ Write → Run (pass) → Revert fix → Run (MUST FAIL) → Restore → Run (pass)
❌ "I've written a regression test" (without red-green verification)
```

**Build:**
```
✅ [Run npm run build] [See: exit 0] "Build passes"
❌ "Linter passed" (linter doesn't check compilation)
```

**Requirements:**
```
✅ Re-read spec → Build checklist → Verify each → Report gaps or completion
❌ "Tests pass, phase complete"
```

**Subagent delegation:**
```
✅ Agent reports success → Check git diff → Verify changes exist → Report actual state
❌ Trust the agent's report
```

## Why This Matters

- Corey says "I don't believe you" — trust broken, and that's the whole business.
- Undefined functions shipped to a client — the app crashes on their device.
- Missing requirements shipped — incomplete deliverable, awkward redo on the call.
- Time wasted on a false completion → client redirect → rework on our dime.

## When To Apply

**ALWAYS before:**
- ANY variation of a success/completion claim
- ANY expression of satisfaction
- Committing, opening a PR, marking a task done
- Moving to the next task
- Handing a build to the client or to `maycrest-ops:reality-checker`

**Rule applies to:** exact phrases, paraphrases, synonyms, implications of success — ANY
communication suggesting completion or correctness.

## Example: AOS Sober Living booking app

About to tell Corey the van-booking fix is done. The gate:

1. **Identify** — `npx vitest run src/booking.test.ts` proves the double-booking guard.
2. **Run** — fresh, full command.
3. **Read** — `Test Files 1 passed, Tests 4 passed (4)`, exit 0.
4. **Verify** — output confirms the claim, including the original-symptom test.
5. **Claim** — "Double-booking is fixed: 4/4 booking tests pass, build exits 0." Evidence attached.

Without step 2-3, the only honest statement is "I changed the code but haven't verified it."

## Integration with the Maycrest roster

- Runs on every task inside [sloth-build](../sloth-build/SKILL.md) and after [sloth-tdd](../sloth-tdd/SKILL.md) green.
- Re-check the plan from [sloth-blueprint](../sloth-blueprint/SKILL.md) line-by-line for requirements coverage.
- For the production-readiness verdict, hand the verified build to `maycrest-ops:reality-checker` —
  it defaults to NEEDS WORK and demands the same evidence.

## The Bottom Line

**No shortcuts for verification.** Run the command. Read the output. THEN claim the result.
This is non-negotiable.

---
*Adapted from the MIT-licensed [obra/superpowers](https://github.com/obra/superpowers) project (© 2025 Jesse Vincent). See [NOTICE](../../NOTICE).*
