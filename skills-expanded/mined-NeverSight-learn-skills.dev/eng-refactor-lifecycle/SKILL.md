---
name: eng-refactor-lifecycle
description: Execute safe progressive refactoring automatically from hotspot analysis through behavior-preservation contracts, phased strangler planning, small-step execution with per-step regression validation, audit, and delivery. Use when modernizing legacy systems without changing observable behavior.
---

# Progressive Refactoring Lifecycle

Modernizes legacy code through strangler-style incremental steps where behavior preservation is contractually enforced and every step is regression-verified.

## 7-Stage Pipeline State Machine

```
Stage 1: eng-analyze-codebase (identify refactor hotspots & coupling)
           │
           ▼
Stage 2: eng-spec (behavior-preservation contract: golden tests, seams)
           │
           ▼
Stage 3: eng-plan (phased strangler roadmap) ──► [Gate: Human Plan Sign-off]
                                                        │
Stage 4: eng-execute (small-step refactor, ◄────────────┘
           │        per-step regression validation)
           ▼
Stage 5: eng-multidimensional-audit (post-refactor integrity scan)
           │
           ▼
Stage 6: eng-validate (full suite green)
           │
           ▼
Stage 7: eng-git-commit / eng-git-pr
```

---

## Autonomous Execution Protocol

1. **Execute `eng-analyze-codebase`**: Rank refactoring hotspots by coupling, churn, and risk. Produce evidence-backed targets.
2. **Execute `eng-spec`**: Freeze the behavior-preservation contract: observable inputs/outputs that must remain identical, characterization tests capturing current behavior, and allowed internal changes.
3. **Execute `eng-plan`** and present the phased strangler roadmap. **Gate (Human Sign-off)**: proceed only after explicit plan approval.
4. **Execute `eng-execute`**: Refactor in small steps. After every step, run the characterization tests plus affected suite subset; any behavioral drift halts and reverts the step immediately.
5. **Execute `eng-multidimensional-audit`**: Verify no coupling regressions, dead code residue, or consistency hazards were introduced.
6. **Execute `eng-validate`**: Full linters, types, tests, and build must pass with zero regressions.
7. **Execute `eng-git-commit` / `eng-git-pr`**: Deliver atomic commits per phase with a PR summarizing behavior-preservation evidence.

## State Persistence & Resumption

Record pipeline progress in `.agents/lifecycle-state.json`:

```
{
  "feature": "<refactor-slug>",
  "pipelineType": "progressive-refactor",
  "currentStage": 4,
  "stageName": "eng-execute",
  "completedStages": [
    "eng-analyze-codebase",
    "eng-spec",
    "eng-plan"
  ],
  "lastUpdated": "YYYY-MM-DDTHH:mm:ssZ"
}
```

## Checkable Completion Criteria

- [ ] Behavior-preservation contract frozen with characterization tests passing before any refactor.
- [ ] Phased plan approved by the user.
- [ ] Every executed step validated against characterization tests with zero behavioral drift.
- [ ] Post-refactor audit and full validation suite both green.
- [ ] Phase-level atomic commits delivered via PR.