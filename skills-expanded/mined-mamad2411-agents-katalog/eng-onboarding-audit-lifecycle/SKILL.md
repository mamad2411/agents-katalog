---
name: eng-onboarding-audit-lifecycle
description: Perform a one-shot read-only codebase health inspection combining context priming, topology analysis, multi-dimensional audit, and baseline validation. Use when taking over an unfamiliar repository or running periodic architecture health checks.
---

# Codebase Onboarding & Health Audit Lifecycle

Runs the entire onboarding and audit pipeline in one pass. Fully read-only: no source code is modified at any stage, so no human gates are required until the final report review.

## 5-Stage Pipeline State Machine

```
Stage 1: eng-prime-context (tech stack, conventions, entry points)
           │
           ▼
Stage 2: eng-analyze-codebase (topology, circular deps, patterns)
           │
           ▼
Stage 3: eng-multidimensional-audit (spatial, solid, reverse 3D scan)
           │
           ▼
Stage 4: eng-adversarial-audit (optional deep security scan)
           │
           ▼
Stage 5: eng-validate (baseline lint, types, tests, build status)
           │
           ▼
Output: Consolidated Codebase Health Report
```

---

## Autonomous Execution Protocol

1. **Execute `eng-prime-context`**: Map tech stack, directory layout, conventions, and key entry points.
2. **Execute `eng-analyze-codebase`**: Build the dependency graph, detect circular dependencies, and catalog design patterns.
3. **Execute `eng-multidimensional-audit`**: Run the spatial, solid, and reverse thinking scans producing prioritized findings.
4. **Execute `eng-adversarial-audit`** (optional): Include this stage when the user requests deep security analysis or the system is mission-critical.
5. **Execute `eng-validate`**: Record the current health baseline covering what passes and what fails today.
6. **Consolidate Findings**: Merge all outputs into a single report saved to `.agents/audit-reports/codebase-health-<repo-name>.md` containing the architecture overview, risk heatmap, prioritized remediation backlog, and baseline health status.

## State Persistence & Resumption

Record pipeline progress in `.agents/lifecycle-state.json`:

```
{
  "feature": "<repo-name>",
  "pipelineType": "onboarding-audit",
  "currentStage": 4,
  "stageName": "eng-adversarial-audit",
  "completedStages": [
    "eng-prime-context",
    "eng-analyze-codebase",
    "eng-multidimensional-audit"
  ],
  "lastUpdated": "YYYY-MM-DDTHH:mm:ssZ"
}
```

If execution is interrupted, reading `.agents/lifecycle-state.json` resumes from the last incomplete stage.

## Checkable Completion Criteria

- [ ] All executed stages produced their standard artifacts.
- [ ] Every finding references concrete file paths and line evidence.
- [ ] Consolidated health report saved to `.agents/audit-reports/`.
- [ ] Zero source modifications made during the audit.