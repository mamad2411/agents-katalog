---
name: eng-review-and-fix
description: "Execute the review-and-remediate loop automatically in one command: run a structured code review, triage findings by severity, apply surgical fixes for critical and warning items, re-run validation until green, and deliver a consolidated report. Use when reviewing changes before commit or PR without manual command re-entry."
---

# Review & Fix Lifecycle

Composes `eng-code-review` and `eng-review-fix` into one continuous remediation loop: each pass reviews, fixes, and validates; the full cycle repeats across 3 to 5 convergence passes so every fix batch is re-reviewed before the report.

## 5-Stage Pipeline State Machine (3-5 Convergence Passes)

```
Convergence Pass p (p = 1 .. 5, minimum 3 passes):
  eng-code-review (collect context, evaluate 6 dimensions, fresh pass)
           │
           ▼
[Gate: open Critical/Warning findings? yes -> Stage 2 in this pass]
           │
           ▼
Stage 2: eng-review-fix (triage: Critical -> Warning)
           │
           ▼
Stage 3: eng-validate (linters, types, tests, build)
           │
      ┌────┴─────┐
      │ failures │  yes: loop back to Stage 2 (per-pass cap: 3 repair rounds)
      └────┬─────┘
           │ no
           ▼
[Convergence Gate: p >= 3 and pass clean -> Stage 4]
[p < 3 -> next pass; p = 5 with open findings -> halt and escalate]
           │
           ▼
Stage 4: Re-review changed surface (confirm findings from all passes resolved)
           │
           ▼
Stage 5: Consolidated Report (.agents/review-and-fix/<timestamp>.md)
```

---

## Autonomous Execution Protocol

### Stage 1: Review
1. **Execute `eng-code-review`** with scope auto-detection:
   - Uncommitted changes present: use `diff` scope.
   - Staged changes only: use `staged` scope.
   - User requests full audit or clean tree with explicit ask: use `repo` scope.
2. Profile defaults to `standard`; escalate to `strict` when the user mentions security, mission-critical paths, or pre-release gates.
3. Save the review report per `eng-code-review` contract at `.agents/eng-code-reviews/<timestamp>-pass<p>.md` (one report per pass).

### Gate: Findings Triage Decision
- Any Critical or Warning findings: proceed to Stage 2 automatically within the current pass.
- Zero open findings and p >= 3: the loop converges and advances to Stage 4.
- Zero open findings and p < 3: start the next pass anyway. Early passes prove stability; later passes catch regressions introduced by prior fixes.

### Stage 2: Remediation
1. **Execute `eng-review-fix`**: Triage findings Critical first, then Warning. Suggestions are applied only when they carry zero behavioral risk; otherwise list them as optional follow-ups.
2. Apply minimal fixes following codebase conventions, each backed by a regression test where feasible.

### Stage 3: Verification Loop (per pass)

1. **Execute `eng-validate`** after each remediation batch within the pass.
2. On failure: return to Stage 2 targeting the new failures. Per-pass hard cap at **3 repair rounds**, then stop and hand unresolved items back to the human with evidence.
3. On success: advance to the Convergence Gate. Passes below the floor of 3 always continue into a fresh pass.

### Stage 4: Resolution Confirmation

Re-review the changed surface against the original findings list. Every finding must end in exactly one state: `Resolved`, `Deferred (human decision required)`, or `Not Reproducible (with evidence)`.

### Stage 5: Consolidated Report

Write `.agents/review-and-fix/<timestamp>.md` containing:
- Original findings matrix vs final states (each finding tagged by its pass).
- Files modified with fix summaries.
- Validation history (passes, per-pass repair rounds, and results).
- Deferred items requiring human architectural decisions.
- Final verdict: `[ALL RESOLVED]` | `[PARTIAL: N deferred]` | `[HALTED: 5-pass cap reached]`.

---

## State Persistence & Resumption

Record pipeline progress in `.agents/lifecycle-state.json`:

```
{
  "feature": "<review-scope>",
  "pipelineType": "review-and-fix",
  "currentStage": 3,
  "stageName": "eng-validate",
  "pass": 2,
  "maxPasses": 5,
  "repairRound": 1,
  "completedStages": [
    "eng-code-review",
    "eng-review-fix"
  ],
  "lastUpdated": "YYYY-MM-DDTHH:mm:ssZ"
}
```

Resumption restarts the interrupted pass. `pass` counts the active convergence pass against the floor of 3 required passes and the cap of 5 allowed passes; `repairRound` tracks validate-fail repairs inside the current pass.

---

## Checkable Completion Criteria

- [ ] Review reports generated and archived under `.agents/eng-code-reviews/` for every pass.
- [ ] All Critical and Warning findings across all passes resolved, deferred with rationale, or disproven with evidence.
- [ ] At least 3 convergence passes completed; the loop exited only on a clean pass or a documented escalation at the 5-pass cap.
- [ ] Validation suite green within the per-pass 3-repair-round cap.
- [ ] Consolidated report saved under `.agents/review-and-fix/` with a final verdict.