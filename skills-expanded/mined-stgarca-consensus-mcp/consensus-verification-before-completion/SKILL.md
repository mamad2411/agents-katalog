<!-- Vendored from Superpowers (c) 2025 Jesse Vincent, github.com/obra/superpowers, v5.1.0 @ f2cbfbe, MIT. Adapted for consensus-mcp. -->
---
name: consensus-verification-before-completion
description: "Consensus-adapted: Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands AND minting/verifying a consensus delivery-readiness token before any success claim; evidence before assertions always."
---

# Verification Before Completion

> Consensus has precedence at decision gates (see the consensus bootstrap / consensus-workflow).

## Overview

Claiming work is complete without verification is dishonesty, not efficiency.

**Core principle:** Evidence before claims, always.

**Violating the letter of this rule is violating the spirit of this rule.**

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this message, you cannot claim it passes.

## The Consensus Gate (delivery-readiness token)

In addition to the iron law above, the consensus gate adds a deterministic token check:

> **Before any completion claim, mint/verify a delivery-readiness token (`consensus_mcp/_delivery_readiness.py`) and run `gate_evaluate_production_with_scope_match`. This token is what the consensus Stop hook checks.**

Concretely:

1. Run the FULL verification commands (tests, build, lint) and read the output - this is the evidence the iron law requires.
2. **Mint/verify the delivery-readiness token** via `consensus_mcp/_delivery_readiness.py` for the modified source files. The token records that fresh verification evidence exists for the delivered scope.
3. **Run `gate_evaluate_production_with_scope_match`** to confirm the delivered changes match the approved scope and pass the production gate.
4. Only after the token verifies AND the gate passes may you claim completion.

The consensus Stop hook checks this delivery-readiness token: if a modified source file lacks a valid token, the Stop hook will surface a blocking directive naming the file. Minting the token here is what lets the Stop hook pass.

## The Gate Function

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: continue
5. TOKEN: Mint/verify the delivery-readiness token (_delivery_readiness.py)
          then run gate_evaluate_production_with_scope_match
6. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

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
| Ready to deliver | Delivery token verifies + gate passes | Tests passing alone |

## Red Flags - STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!", etc.)
- About to commit/push/PR without verification
- About to claim completion without a verified delivery-readiness token
- Trusting agent success reports
- Relying on partial verification
- Thinking "just this once"
- Tired and wanting work over
- **ANY wording implying success without having run verification**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence != evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter != compiler |
| "Agent said success" | Verify independently |
| "I'm tired" | Exhaustion != excuse |
| "Partial check is enough" | Partial proves nothing |
| "Different words so rule doesn't apply" | Spirit over letter |
| "Tests pass, no need for the token" | The Stop hook checks the token - mint it |

## Key Patterns

**Tests:**
```
[ok] [Run test command] [See: 34/34 pass] "All tests pass"
[x] "Should pass now" / "Looks correct"
```

**Regression tests (TDD Red-Green):**
```
[ok] Write -> Run (pass) -> Revert fix -> Run (MUST FAIL) -> Restore -> Run (pass)
[x] "I've written a regression test" (without red-green verification)
```

**Build:**
```
[ok] [Run build] [See: exit 0] "Build passes"
[x] "Linter passed" (linter doesn't check compilation)
```

**Requirements:**
```
[ok] Re-read plan -> Create checklist -> Verify each -> Report gaps or completion
[x] "Tests pass, phase complete"
```

**Agent delegation:**
```
[ok] Agent reports success -> Check VCS diff -> Verify changes -> Report actual state
[x] Trust agent report
```

**Delivery readiness (consensus gate):**
```
[ok] [Run verification] [Mint/verify _delivery_readiness token] [gate_evaluate_production_with_scope_match: PASS] "Ready to deliver"
[x] "Tests pass, shipping it" (no token = Stop hook will block)
```

## Why This Matters

From 24 failure memories:
- your human partner said "I don't believe you" - trust broken
- Undefined functions shipped - would crash
- Missing requirements shipped - incomplete features
- Time wasted on false completion -> redirect -> rework
- Violates: "Honesty is a core value. If you lie, you'll be replaced."

The consensus delivery-readiness token makes "I verified" a checkable artifact, not a self-report.

## When To Apply

**ALWAYS before:**
- ANY variation of success/completion claims
- ANY expression of satisfaction
- ANY positive statement about work state
- Committing, PR creation, task completion
- Moving to next task
- Delegating to agents

**Rule applies to:**
- Exact phrases
- Paraphrases and synonyms
- Implications of success
- ANY communication suggesting completion/correctness

## The Bottom Line

**No shortcuts for verification.**

Run the command. Read the output. Mint/verify the delivery-readiness token. Run the production gate. THEN claim the result.

This is non-negotiable.
