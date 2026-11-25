---
name: verification-before-completion
description: Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always.
aliases:
  - verification-before-completion
  - verify-before-completion
  - verification-gate
  - pre-completion-check
category: "05 - Security & Code Quality"
tags:
  - agent-skill
  - verification
  - quality-assurance
  - stage-5
---

# Verification Before Completion

## Overview

**Core principle:** Evidence before claims, always.

**Violating the letter of this rule is violating the spirit of this rule.**

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this message, you cannot claim it passes.

## Pre-Execution Mental Simulation (Cognitive Sandbox)

Before executing multi-file mutations, schema changes, or destructive shell operations:
1. **Blast Radius Analysis**: Trace upstream callers and downstream consumers. Which modules break if this signature changes?
2. **Failure Mode Hypothesis**: Formulate concrete failure scenarios (null inputs, timeouts, concurrency collisions).
3. **Reversibility Guarantee**: Ensure every operation has a clean rollback path (git worktree, backup, down migration).

## Enterprise Scale & Zero-Anomaly Gates

When working on large-scale codebases, monorepos, or high-throughput services:

1. **Monorepo Downstream Ripple Gate**:
   - Never verify only the local package when editing shared libraries, schemas, or utilities.
   - Run dependency impact builds and downstream tests (`pnpm --filter ...`, `npm run build --workspaces`, or `turbo run test`).
2. **Flake-Resistance Multi-Sampling**:
   - For asynchronous, concurrent, or network-bound logic, a single pass does not prove correctness.
   - Run critical regression tests 3 consecutive times (`for i in {1..3}; do <test>; done`) to prove zero flakiness and race immunity.
3. **Hermetic Environment & Stale Artifact Purge**:
   - Before final verification, remove cached artifacts (`dist/`, `.next/`, `build/`, `__pycache__`) to prevent false-green passes on stale bytecode.
4. **Zero-Pollution Quarantine**:
   - Audit `git status --porcelain` and diff to ensure zero uncommitted debug flags, temporary dumps, or secret leakage.

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

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter ≠ compiler |
| "Agent said success" | Verify independently |
| "I'm tired" | Exhaustion ≠ excuse |
| "Partial check is enough" | Partial proves nothing |
| "Different words so rule doesn't apply" | Spirit over letter |

## Key Patterns

**Tests:**
```
✅ [Run test command] [See: 34/34 pass] "All tests pass"
❌ "Should pass now" / "Looks correct"
```

**Regression tests (TDD Red-Green):**
```
✅ Write → Run (pass) → Revert fix → Run (MUST FAIL) → Restore → Run (pass)
❌ "I've written a regression test" (without red-green verification)
```

**Build:**
```
✅ [Run build] [See: exit 0] "Build passes"
❌ "Linter passed" (linter doesn't check compilation)
```

**Requirements:**
```
✅ Re-read plan → Create checklist → Verify each → Report gaps or completion
❌ "Tests pass, phase complete"
```

**Agent delegation:**
```
✅ Agent reports success → Check VCS diff → Verify changes → Report actual state
❌ Trust agent report
```

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

---
## 🔗 Connected Skills (ทักษะที่เกี่ยวข้อง)
- [[Skills/tdd-workflow/SKILL|tdd-workflow]] — รันการทดสอบ Unit/Integration ให้ผ่านครบถ้วน
- [[Skills/review/SKILL|review]] — ตรวจสอบ Code Quality และ Diff ก่อนส่งมอบงาน
- [[Skills/systematic-debugging/SKILL|systematic-debugging]] — หากการทดสอบล้มเหลว ย้อนกลับไปวินิจฉัยหาสาเหตุรากเหง้า
- [[Skills/finishing-a-development-branch/SKILL|finishing-a-development-branch]] — ปิดและรวม Branch หลังจากผ่านการ Verify แล้ว

<!-- v1.1.0 synchronized: 2026-09-29 -->
