---
name: superpowers-verify
agent_created: true
version: 1.0.0
description: Evidence-before-claims gate. Run verification commands and confirm output BEFORE making any completion claims. This skill should be used before committing, marking tasks done, or claiming any fix is complete.
---

# Verification Before Completion

## Overview

Claiming work is complete without verification is dishonesty, not efficiency.

**Core principle:** Evidence before claims, always.

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
| Linter clean | Linter output: 0 errors | Partial check |
| Build succeeds | Build command: exit 0 | Linter passing |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Agent completed | VCS diff shows changes | Agent reports "success" |

## Red Flags — STOP

Using "should", "probably", "seems to". Expressing satisfaction before verification ("Great!", "Done!"). About to commit without verification. Trusting agent success reports. Relying on partial verification. ANY wording implying success without having run verification.

## Key Patterns

**Tests:** Run the command, see the count, report the count. Never "should pass."
**Build:** Run build, see exit 0. Linter is not a compiler.
**Agent delegation:** Check VCS diff, verify changes, report actual state. Never trust agent reports.

## The Bottom Line

**No shortcuts for verification.** Run the command. Read the output. THEN claim the result. This is non-negotiable.
