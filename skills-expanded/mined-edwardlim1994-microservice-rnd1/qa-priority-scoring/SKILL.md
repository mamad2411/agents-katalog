# QA Priority Scoring

## Purpose
Contributes Testability Risk score to `shared/priority-scoring-model` for each story.

## Role
QA Engineer

## Phase
Planning (Stage 6)

## Triggered By
`task-prioritisation` begins.

## Inputs
- `shared/priority-scoring-model` (Testability Risk dimension)

## Process
1. For each story, assign Testability Risk score 1-5:
   - 5 = complex/hard to automate/high regression risk
   - 1 = trivial/minimal tests
2. Submit score to PM for `task-prioritisation`.

## Outputs
Testability Risk score per story, submitted to PM.

## Quality Gates
- [ ] Score assigned for every story in sprint
- [ ] Score reflects actual test design complexity from test-strategy-definition

## References
- `.claude/skills/shared/priority-scoring-model/SKILL.md`
- `.claude/skills/pm/task-prioritisation/SKILL.md`
