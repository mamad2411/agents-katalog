---
name: phase-plan
description: Phase 2 of the software delivery workflow: convert research and requirements into a practical PRD, implementation plan, architecture notes, task list, and acceptance criteria before coding.
origin: ECC automation-pack
---

# Phase Plan

Use this skill when the user asks for `/phase-plan`, planning after research, PRD/PRP generation, implementation planning, or the second stage of an automated software delivery flow.

## Purpose

Create a plan that is specific enough to execute and small enough to verify.

## Workflow

1. Restate the requirement in concrete terms.
2. Summarize relevant findings from `phase-research` if available.
3. Define acceptance criteria and non-goals.
4. Check for over-design:
   - What is the simplest version?
   - What can be deleted before implementation?
   - Which abstractions are actually needed now?
5. Draft the implementation plan:
   - files or modules likely affected
   - ordered steps
   - tests per step
   - risk and rollback notes
6. Add a Mermaid diagram only when it clarifies multi-module behavior.
7. Save or present the plan in the project’s normal planning location when appropriate.

## Output

Include:

- requirement summary
- acceptance criteria
- phased implementation plan
- test plan
- risk list
- open questions

End with `PHASE_PLAN_DONE` when the plan is executable. If blocked, output `PHASE_PLAN_BLOCKED`.
