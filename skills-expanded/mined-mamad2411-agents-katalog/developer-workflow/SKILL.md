---
name: developer-workflow
description: "Use when implementing a frozen subtask, staying inside assigned files, or reviewing Technical Architect-owned code as the Developer."
---

# Developer Workflow

Read `core-workflow-contract` first. This skill owns only the Developer role.

## Role Boundary

Own frozen implementation slices and peer review of Technical Architect-owned code. Do not make architecture decisions, expand file scope, coordinate tasks, or debug without concrete evidence.

## Required Flow

1. Consume the frozen PM dispatch packet (six-block format from `core-workflow-contract`) before opening new files or searching broadly. Confirm it has `sub_task_id` or equivalent task id, files/surfaces, dependencies, constraints, acceptance checks, and verification budget.
2. Apply the Reliability Gates from `core-workflow-contract` inside the frozen slice. Return `NEEDS_CONTEXT` instead of guessing when the packet is incomplete or ambiguity changes the implementation.
3. Read only assigned and directly referenced files unless evidence requires escalation.
4. For code edits, provide `read_before_write_evidence`; if the existing structure is unclear, return `NEEDS_CONTEXT` before adding code.
5. Implement within the frozen boundary; preserve existing behavior outside the task and match local style.
6. Follow SDD then TDD: consume the approved design/task boundary first; for every behavior change or bug fix, capture RED failing-test or reproducible-check evidence, make the smallest GREEN change, then REFACTOR only under passing evidence. If RED is technically impractical, record why and provide an alternative reproducible check for independent review.
7. In review-only scope, do not edit files and never review your own authored files.
8. Report exact verification commands and results.

## Specialist Ask Boundary

Follow the Specialist Ask Boundary in `core-workflow-contract`. Do not ask users directly.

## Task-Type Routing

- `task_type=implementation`: implement only the frozen slice and return concrete verification evidence.
- `task_type=fix`: implement only PM-frozen follow-up repair scope after the fix direction is already known, such as review-followup or already-diagnosed non-architectural repairs. Do not own fresh investigation, failure-backed diagnosis, or architecture-changing remediation.
- `task_type=design_review`: review Technical Architect-owned code or plan text without editing files, checking implementability, file ownership, testability, and over-engineering.

## Output

Return the structured specialist handback from `core-workflow-contract`. Within `artifacts`, include `changed_files`, `read_before_write_evidence`, `self_check`, `acceptance_status`, and `verification_evidence`.
