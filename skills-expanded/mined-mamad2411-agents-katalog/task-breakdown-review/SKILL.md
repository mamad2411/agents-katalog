# Task Breakdown Review

## Purpose
Quality gate verifying OpenSpec-generated tasks are correctly scoped, labelled, and linked before kanban card creation.

## Role
Project Manager

## Phase
Planning (Stage 6)

## Triggered By
`openspec-proposal` completes.

## Inputs
- `tasks.md` from OpenSpec change folder

## Process
1. Read `tasks.md` from OpenSpec change folder.
2. For each task, verify:
   - Has clear acceptance criteria (not just a description)
   - Has correct area label (backend/frontend/mobile/devops/qa/api/security)
   - Has dependency links to blocking tasks
   - Sized for one PR (if multi-day, needs further breakdown)
   - References correct `contracts/` schema files
3. Request task revision from Architect if tasks are too large or missing info.
4. Only proceed to `issue-management` when all tasks pass review.

## Outputs
Verified task list ready for kanban card creation.

## Quality Gates
- [ ] Every task has AC
- [ ] Every task has area label
- [ ] Dependencies documented
- [ ] No tasks requiring multi-PR to complete (unless intentionally split)

## References
- `.claude/skills/pm/openspec-proposal/SKILL.md`
- `.claude/skills/pm/kanban-board-management/SKILL.md`
