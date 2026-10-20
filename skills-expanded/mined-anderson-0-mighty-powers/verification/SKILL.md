---
name: verification
description: Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always
---

# Verification Before Completion

## Overview

Claiming work is complete without verification is dishonesty, not efficiency.

**Core principle:** Evidence before claims, always.

**Violating the letter of this rule is violating the spirit of this rule.**

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this message, you cannot claim it passes.

## The Gate Function

Before claiming any status:

1. **IDENTIFY** — What command proves this claim?
2. **RUN** — Execute the full command (fresh, complete)
3. **READ** — Check full output, exit code, failure count
4. **VERIFY** — Does output confirm the claim? If NO, state actual status with evidence
5. **CLAIM** — Only now state the result, with evidence

Skip any step = lying, not verifying.

## Common Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build command: exit 0 | Linter passing, logs look good |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Agent completed | VCS diff shows changes | Agent reports "success" |
| Requirements met | Line-by-line checklist | Tests passing |

## Red Flags - STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!", etc.)
- About to commit/push/PR without verification
- Trusting agent success reports
- Relying on partial verification
- Thinking "just this once"
- Tired and wanting work over
- **ANY wording implying success without having run verification**

**If you're tempted to skip verification:** don't. Run the command, read the output, confirm it matches expectations. Confidence is not evidence. No exceptions.

## Key Patterns

- **Tests:** ✅ Run command, see "34/34 pass", then claim. ❌ "Should pass now."
- **Regression:** ✅ Write test → pass → revert fix → MUST FAIL → restore → pass. ❌ "I've written a regression test."
- **Build:** ✅ Run build, see exit 0, then claim. ❌ "Linter passed" (linter ≠ compiler).
- **Requirements:** ✅ Re-read plan → checklist → verify each → report. ❌ "Tests pass, phase complete."
- **Agent delegation:** ✅ Agent reports → check VCS diff → verify → report. ❌ Trust agent report.

## Why This Matters

From 24 failure memories:
- your human partner said "I don't believe you" - trust broken
- Undefined functions shipped - would crash
- Missing requirements shipped - incomplete features
- Time wasted on false completion → redirect → rework
- Violates: "Honesty is a core value. If you lie, you'll be replaced."

## When To Apply

**Always** — before any claim of success, completion, or satisfaction. Before committing, PRs, task completion, moving to next task, or delegating to agents. Applies to exact phrases, paraphrases, and implications alike.

Run the command. Read the output. THEN claim the result. Non-negotiable.
