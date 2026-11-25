# Planning Session Facilitation

## Purpose
Moderates all 7 stages of the planning session in order, controls the floor per role, synthesises between stages.

## Role
Project Manager

## Phase
Planning

## Triggered By
`planning-session-kickoff` completes.

## Inputs
- Context-loaded planning subagents

## Process

### Stage 1 — Story Presentation (PO leads)
PO presents the user story. All other roles listen only.
Output: shared understanding of what user needs.

### Stage 2 — Challenge Round (QA + Security)
- QA: `acceptance-criteria-challenge`, `test-strategy-definition`
- Security: `threat-modelling`, `security-story-review`, `compliance-assessment`
- PO responds and refines AC based on challenges.
Output: tightened testable AC, security requirements surfaced.

### Stage 3 — Technical Assessment (Architect leads)
Architect: `technical-assessment`, `system-architecture-diagram`, `service-boundary-definition`, `dependency-mapping`, `story-diagram-design`, `proto-contract-design` (if needed), `graphql-schema-design` (if needed), `architecture-decision-record` (if significant decision made).
Output: affected services, dependency map, diagrams, ADRs.

### Stage 4 — UX Elaboration (UI/UX Designer leads)
- UI/UX: `user-flow-definition`, `interaction-specification`, `component-requirements`, `accessibility-requirements`, `design-prompt-writing`.
- QA: `frontend-interaction-test-design` (parallel with UI/UX).
Output: interaction spec, component requirements, design prompt.

### Stage 5 — PRD Drafting (PM leads)
- PM: `prd-writing` (synthesises Stages 1-4 into PRD)
- QA: `test-data-strategy`, `qa-priority-scoring`
- Security: `security-requirements-writing`, `security-priority-scoring`
- All roles review and sign off.
Output: PRD committed to `openspec/changes/{slug}/prd.md`.

### Stage 6 — Prioritisation + OpenSpec (PM leads)
- PM: `task-prioritisation` (references `shared/priority-scoring-model`)
- PM: `openspec-proposal` (`/opsx:propose` with PRD as input)
- Architect elaborates `design.md` in OpenSpec change folder
- QA: `integration-test-case-design`, `e2e-test-case-design`
- PM: `task-breakdown-review`, `issue-management` (creates kanban tasks)
Output: OpenSpec change folder, kanban task cards.

### Stage 7 — Escalation + Sprint Planning (PM leads)
All roles surface unresolved decisions as one consolidated list.
- PM: triggers `shared/escalation-to-owner` → Edward reviews.
- PM: `sprint-planning`, `milestone-management` (after Edward approves).
Output: Sprint finalised, awaiting `/kickoff` from Edward.

### Steps
1. Proceed through stages 1-7 in strict order.
2. Decide when each stage is complete enough to move forward.
3. Synthesise outputs between stages.
4. Surface escalations at Stage 7 only (not piecemeal).
5. Do not begin Stage N+1 until Stage N is complete.

## Outputs
Sprint finalised, awaiting Edward's `/kickoff`.

## Quality Gates
- [ ] All 7 stages completed in order
- [ ] No stage skipped
- [ ] All escalations deferred to Stage 7
- [ ] Sprint plan ready for Edward's /kickoff

## References
- `.claude/skills/pm/planning-session-kickoff/SKILL.md`
- `.claude/skills/pm/prd-writing/SKILL.md`
- `.claude/skills/pm/openspec-proposal/SKILL.md`
- `.claude/skills/pm/task-breakdown-review/SKILL.md`
- `.claude/skills/pm/task-prioritisation/SKILL.md`
- `.claude/skills/pm/sprint-planning/SKILL.md`
- `.claude/skills/pm/milestone-management/SKILL.md`
- `.claude/skills/shared/escalation-to-owner/SKILL.md`
