---
name: eng-enterprise-lifecycle
description: Execute the end-to-end enterprise production development pipeline sequentially in an automated workflow. Orchestrates briefing, spec freezing, context priming, optional PRD, planning with change-scope whitelist, execution, validation gates, first-pass multi-angle review, remediation loop, independent fix verification, completion verdict, and authorization-gated push without requiring manual command re-entry.
---

# Enterprise Production Lifecycle Pipeline

Orchestrates the complete enterprise development lifecycle as a continuous, state-tracked execution engine. Design principles hardened against known lifecycle defects:

- **First review is multi-angle**: pass 1 covers all six quality dimensions at once; later convergence passes re-scan the evolving surface without adding dedicated stages.
- **Convergence by repetition**: Stages 8-9 run 3 to 5 full review-fix-validate passes; a single green pass never advances to the verdict.
- **Single-purpose fix verification**: after remediation, one focused review verifies the fix diff only.
- **Verdict before push**: the completion gate runs before any remote delivery; pushing an unverified state is structurally impossible.
- **Push requires explicit authorization**: default mode produces a readiness report only.
- **Smallest sufficient pipeline**: small tasks skip PRD and heavy spec stages via the fast-path rule below.

---

## 13-Stage Pipeline State Machine

```
Stage 1: prod-briefing-loop ──────► [Gate: Human Brief Sign-off]
                                            │
Stage 2: eng-prime-context ◄────────────────┘
           │        (+ eng-analyze-codebase)
           ▼
Stage 3: prod-create-prd (OPTIONAL: new features only)
           │
           ▼
Stage 4: eng-spec (SDD freeze: requirements, contracts)
           │
           ▼
Stage 5: eng-plan ───────────────► [Gate: Human Plan Sign-off]
           │        (+ change-scope-funnel whitelist)   │
           ▼                                           │
Stage 6: eng-execute ◄────────────────────────────────┘
           │        (whitelist-bounded edits)
           ▼
Stage 7: eng-validate (linters, types, tests, build)
           │        (NEVER review untested code)
           ▼
Stage 8: First-Pass Multi-Angle Review
           │        (eng-multidimensional-audit + eng-hardening-review)
           ▼
Stage 9: eng-review-fix convergence ─► re-review ➔ fix ➔ eng-validate
           │        (passes 2-5: floor 3 clean-pass convergence, cap 5)
           ▼
Stage 10: Second Independent Review (fix diff only)
           │        (root cause verified, no weakened tests)
           ▼
Stage 11: eng-completion-gate (DONE / DONE-WITH-ACCEPTED-RISKS / BLOCKED)
           │        (BLOCKED halts before any remote action)
           ▼
Stage 12: eng-git-commit + eng-git-pr readiness report
           │        ───► [Gate: Explicit Push Authorization]
           ▼                                              │
Stage 13: prod-execution-report ◄───────────────────────┘
```

---

## Fast-Path Rule (Smallest Sufficient Pipeline)

| Task Type | Skipped Stages | Minimum Chain |
|---|---|---|
| Typo, comment, rename | 3, 4 | 1 → 2 → 5(light) → 6 → 7 → 11 → 12 |
| Single bug fix | 3 | 1(light) → 2 → 4(thin RCA contract) → 5 → 6 → 7 → 9 → 10 → 11 → 12 |
| Small feature (under 3 files) | 3 | full chain minus PRD |
| New feature / service | none | full chain |

The agent proposes the path classification at Gate 1 alongside the Brief; the user confirms or overrides it.

---

## Autonomous Execution Protocol

### Checkpoint 1: Alignment & Grounding (Stages 1-4)
1. **Execute `prod-briefing-loop`**: Ask 3 to 5 blocker questions, synthesize the Playback Brief, and propose the fast-path classification.
2. **Gate 1**: User confirms the Brief and task-size classification.
3. **Execute `eng-prime-context`** plus `eng-analyze-codebase` for non-trivial tasks: map conventions and integration seams.
4. **Execute `prod-create-prd`** only when Stage 3 applies: formalize business requirements.
5. **Execute `eng-spec`**: freeze requirements into `specs/<feature-name>/{requirements.md, design.md, checklist.md}`.

### Checkpoint 2: Scoped Planning & Implementation (Stages 5-6)
6. **Execute `eng-plan`** grounded by `eng-change-scope-funnel`: the plan's file list becomes the whitelist contract.
7. **Gate 2**: present the plan summary plus the whitelist table; await approval.
8. **Execute `eng-execute`**: whitelist-bounded implementation; any out-of-whitelist need halts and re-funnels with user visibility.

### Checkpoint 3: Quality Gauntlet (Stages 7-10)
9. **Execute `eng-validate`**: automated gates run before any human-style review; never review untested code.
10. **First-Pass Multi-Angle Review**: run `eng-multidimensional-audit` (spatial, solid, reverse) plus `eng-hardening-review` (data integrity plus six failure surfaces) as one comprehensive pass. No separate post-fix rescan stage exists because coverage is complete here.
11. **Execute `eng-review-fix`** inside a 3-5 pass convergence loop: Stage 8 counts as pass 1; every further pass re-reviews the current surface, fixes open findings Critical then Warning, and re-runs `eng-validate` per batch. A clean pass at a total count of 3 or more converges; the cap of 5 total passes escalates with evidence.
12. **Second Independent Review**: re-review ONLY the accumulated fix diff against the union of findings from all passes: root cause addressed, no weakened assertions, no new issues introduced.

### Checkpoint 4: Verdict-Gated Delivery (Stages 11-13)
13. **Execute `eng-completion-gate`**: evidence audit of every criterion. A BLOCKED verdict halts here; nothing remote has happened yet.
14. **Execute `eng-git-commit`**: atomic conventional commits passing the readiness checklist.
15. **Execute `eng-git-pr`** in readiness-only mode: produce the PR text and readiness report without pushing.
16. **Gate 3**: present the readiness report; push or submit happens solely on explicit user instruction.
17. **Execute `prod-execution-report`**: archive the retrospective with Gap Review at `.agents/prod-execution-reports/<feature-name>.md`.

---

## State Persistence & Resumption

Record pipeline progress in `.agents/lifecycle-state.json`:
```
{
  "feature": "<feature-name>",
  "pipelineType": "enterprise-production",
  "currentStage": 6,
  "stageName": "eng-execute",
  "fastPath": false,
  "completedStages": [
    "prod-briefing-loop",
    "eng-prime-context",
    "eng-spec",
    "eng-plan",
    "change-scope-funnel"
  ],
  "lastUpdated": "YYYY-MM-DDTHH:mm:ssZ"
}
```

If execution is interrupted, reading `.agents/lifecycle-state.json` resumes from the last incomplete stage.

---

## Checkable Completion Criteria

- [ ] Brief confirmed with explicit fast-path classification at Gate 1.
- [ ] Requirements frozen into `specs/<feature-name>/` (or thin RCA contract on fast path).
- [ ] Plan approved together with the change-scope whitelist at Gate 2.
- [ ] All edits stayed inside the whitelist; escapes triggered documented re-funnels.
- [ ] `eng-validate` green BEFORE review began (never reviewing untested code).
- [ ] One comprehensive multi-angle pass completed; no duplicate post-fix rescan stage.
- [ ] Review-fix-validate ran 3 to 5 convergence passes with a clean exit or documented escalation at the cap.
- [ ] Second independent review verified the accumulated fix diff only.
- [ ] Completion gate verdict recorded BEFORE any push; BLOCKED never reached remote.
- [ ] Push executed solely after explicit user authorization at Gate 3.
- [ ] Retrospective archived at `.agents/prod-execution-reports/<feature-name>.md`.