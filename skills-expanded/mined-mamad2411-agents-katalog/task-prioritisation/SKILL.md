# Task Prioritisation

## Purpose
Facilitates cross-role priority scoring session using `shared/priority-scoring-model`, producing ranked sprint priority order.

## Role
Project Manager

## Phase
Planning (Stage 6)

## Triggered By
`task-breakdown-review` completes.

## Inputs
- Verified task/story list
- `shared/priority-scoring-model` (MUST read before executing)

## Process
1. Read `shared/priority-scoring-model` for scoring dimensions and weights.
2. Request scores from each role for their dimension(s):
   - PO: Business Value + User Impact scores
   - Security Engineer: Security Risk score
   - Solution Architect: Dependency Blocking + Technical Complexity scores
   - QA Engineer: Testability Risk score
3. Calculate weighted total per story.
4. Apply Must Ship / Should Ship / Can Hold classification.
5. Apply OVERRIDE: compliance stories → Must Ship regardless of score.
6. Produce ranked priority table.
7. Commit table to `openspec/changes/sprint-{N}-priority/priority-table.md`.

## Outputs
Ranked priority table in OpenSpec.

## Quality Gates
- [ ] All roles submitted scores
- [ ] Weights applied correctly per shared/priority-scoring-model
- [ ] Compliance stories marked Must Ship
- [ ] Priority table committed

## References
- `.claude/skills/shared/priority-scoring-model/SKILL.md`
- `.claude/skills/pm/sprint-planning/SKILL.md`
