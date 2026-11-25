# Security Priority Scoring

## Purpose
Contributes Security Risk score to `shared/priority-scoring-model` for each story in the planning session.

## Role
Security Engineer

## Phase
Planning (Stage 6)

## Triggered By
`task-prioritisation` begins.

## Inputs
- `threat-modelling` findings per story
- `shared/priority-scoring-model` (Security Risk dimension)

## Process
1. For each story, assign Security Risk score 1-5 using the scale below.
2. Justify score with one sentence referencing `threat-modelling` findings.
3. Submit score to PM for `task-prioritisation`.
4. Note: score affects sprint priority but DOES NOT affect compliance requirements (compliance is always Must Ship regardless of score).

### Scale (from priority-scoring-model)
- 5 = auth, PII, payment, public-facing sensitive data endpoint
- 4 = modifies existing security controls or adds new external integration
- 3 = internal service with user data
- 2 = internal service with non-sensitive data
- 1 = read-only, no user data, fully internal

## Outputs
Security Risk score per story, submitted to PM.

## Quality Gates
- [ ] Score assigned for every story in sprint
- [ ] Score justified with reference to threat findings
- [ ] Compliance stories separately marked Must Ship

## References
- `.claude/skills/shared/priority-scoring-model/SKILL.md`
- `.claude/skills/pm/task-prioritisation/SKILL.md`
- `.claude/skills/security-engineer/threat-modelling/SKILL.md`
