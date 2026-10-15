---
name: eng-defect-lifecycle
description: Run the complete defect resolution pipeline automatically from root cause analysis through surgical fix, regression validation, atomic commit, and retrospective reporting. Use when a reported bug needs end-to-end remediation without manual command re-entry.
---

# Defect Resolution Lifecycle

Orchestrates the full bug-fix loop as a continuous, state-tracked workflow. Advances automatically between stages and pauses only at the mandatory human RCA sign-off gate.

## 5-Stage Pipeline State Machine

```
Stage 1: eng-bugfix-rca ───────► [Gate: Human RCA Sign-off]
                                        │
Stage 2: eng-bugfix-implement ◄────────┘
           │
           ▼
Stage 3: eng-validate (full regression suite)
           │
           ▼
Stage 4: eng-git-commit (atomic conventional commit)
           │
           ▼
Stage 5: prod-execution-report (fix retrospective)
```

---

## Autonomous Execution Protocol

1. **Execute `eng-bugfix-rca`**: Reproduce the defect, isolate the root cause, and write `.agents/rca/rca-<bug-id>.md`.
2. **Gate (Human Sign-off)**: Present the RCA summary covering root cause, blast radius, and proposed fix strategy. Wait for explicit user approval.
3. **Execute `eng-bugfix-implement`**: Apply the minimal surgical patch plus the regression test derived from the repro loop.
4. **Execute `eng-validate`**: Run linters, type checks, unit tests, integration tests, and build verification. Any failure loops back to Stage 2 automatically.
5. **Execute `eng-git-commit`**: Create an atomic conventional commit referencing the bug id.
6. **Execute `prod-execution-report`**: Write the fix retrospective including divergence analysis and learnings.

## State Persistence & Resumption

Record pipeline progress in `.agents/lifecycle-state.json`:

```
{
  "feature": "<bug-id>",
  "pipelineType": "defect-resolution",
  "currentStage": 3,
  "stageName": "eng-validate",
  "completedStages": [
    "eng-bugfix-rca",
    "eng-bugfix-implement"
  ],
  "lastUpdated": "YYYY-MM-DDTHH:mm:ssZ"
}
```

If execution is interrupted, reading `.agents/lifecycle-state.json` resumes from the last incomplete stage.

## Checkable Completion Criteria

- [ ] RCA document written and approved by the user before any code change.
- [ ] Surgical patch applied with a regression test covering the defect.
- [ ] Full validation suite green with zero regressions.
- [ ] Atomic commit created referencing the bug id.
- [ ] Fix retrospective saved to `.agents/prod-execution-reports/`.