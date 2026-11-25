---
name: test-orchestration
description: Use when coordinating multi-disciplinary test execution passes and collating evidence from Engineering, Architecture, Security, Performance, UX, and Support into a single release-ready verdict.
---

# Test Orchestration

## Specialization

Coordinate the execution of test passes across multiple disciplines, collect and normalise evidence from each pass, identify cross-discipline gaps, and produce a consolidated test summary with a release recommendation.

This skill does not perform the discipline-level test execution — that belongs to Engineering, Security, Performance, and UX domain skills. It coordinates sequencing, drives evidence collection, and produces the integrated verdict.

## Trigger Conditions

- A Test phase requires evidence from more than one discipline before a release decision can be made.
- Test passes have been run independently and their outputs need collation into a single verdict.
- A test plan exists with multi-discipline scope and execution needs sequencing.
- Evidence gaps across disciplines need identification before a release review can begin.

## Inputs

- Test plan or test scope document: disciplines in scope, coverage targets, and exit criteria.
- Available evidence artifacts: test run results, defect logs, coverage reports, security findings, performance results, accessibility reports, and support drill outcomes.
- Entry criteria: any preconditions that must be met before execution begins.
- Originating plan or workstream ID for traceability.

## Required Outputs

| Output | Description |
|---|---|
| Execution status grid | Per-discipline row showing: disciplines in scope, pass/not-yet-run/blocked status, and evidence artifact reference. |
| Evidence collation | Normalised summary of findings per discipline: finding count by severity, top issues, and any blocking items. |
| Cross-discipline gap log | Evidence or coverage gaps identified when viewing all discipline results together that are not visible within any single discipline. |
| Release recommendation | Explicit recommendation: `Ready` / `Ready with conditions` / `Not ready`. Conditions and blocking items listed. |
| Follow-up list | Non-blocking items from any discipline that need resolution post-release, each with owner and target date. |

## Workflow

1. Confirm all disciplines in scope and locate evidence artifacts for each.
2. Build the execution status grid: mark each discipline as Pass, In-progress, Not started, or Blocked.
3. For each completed discipline pass, normalise findings into a common severity format: Critical / Major / Minor / Advisory.
4. Collate findings: identify any cross-discipline patterns — for example, a security gap that also implies an engineering gap.
5. Populate the cross-discipline gap log with issues that emerge from the aggregate view.
6. Evaluate exit criteria: check whether all defined exit conditions are satisfied.
7. Write the release recommendation with explicit rationale.
8. Populate the follow-up list with non-blocking residual items.
9. Record the originating plan or workstream ID on the output artifact.

## Discipline Pass Sequence (default)

When sequencing is not prescribed by the plan, use this default order:

1. Engineering (unit, integration, system)
2. Architecture (resilience, boundary, failure mode)
3. Security (abuse cases, control verification)
4. Performance (load, benchmark, regression)
5. UX (accessibility, usability, journey)
6. Support (alert drills, escalation, runbook)
7. Analysis (traceability, failure analysis, requirement completeness)

Disciplines may run in parallel unless an earlier pass produces findings that invalidate a later pass.

## Done Criteria

- Execution status grid covers every in-scope discipline.
- Evidence collation exists for each completed pass.
- Cross-discipline gap log is present (may be empty if none found).
- Release recommendation is explicit with rationale.
- Follow-up list is present (may be empty).
- Originating plan or workstream ID is on the output.

## Guardrails

- Do not record a `Ready` recommendation when any Critical finding is open across any discipline.
- Do not synthesise a verdict from stale evidence — confirm evidence artifact dates before collating.
- Do not skip a discipline that is in scope; use `Blocked` status with a reason if evidence is unavailable.

## References

- Related skills: `test-design-review`, `release-readiness`, `acceptance-governance`, `security-research`, `performance-research`, `perf-benchmark`
