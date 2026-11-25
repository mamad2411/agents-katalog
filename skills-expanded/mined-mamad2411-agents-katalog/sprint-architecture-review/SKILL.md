# Sprint Architecture Review

## Purpose
Reviews the full sprint for cross-story architectural coherence — not dependency order, but whether multiple stories conflict architecturally.

## Role
Solution Architect

## Phase
Planning (end of Stage 6)

## Triggered By
All stories in sprint have completed Stages 1-5.

## Inputs
- All story technical assessments for this sprint

## Distinction
This is NOT dependency mapping (which handles sequence). This checks: do the stories collectively create an architecturally coherent sprint?

## Process
1. Read all story technical assessments for this sprint.
2. Check for naming convention drift: do multiple stories touching the same service use consistent naming?
3. Check for API contract conflicts: do any stories define conflicting proto or GraphQL changes?
4. Check for data ownership conflicts: do any stories introduce entity ownership ambiguity?
5. Check for pattern consistency: do all stories follow established patterns or do some deviate?
6. If conflicts found: raise with PM for resolution before `/kickoff`.
7. If clean: signal PM that sprint is architecturally coherent.

## Outputs
Sprint architectural coherence confirmation or list of conflicts, to PM.

## Quality Gates
- [ ] No naming conflicts across stories in sprint
- [ ] No API contract conflicts
- [ ] No data ownership ambiguity
- [ ] Pattern consistency verified
- [ ] PM signalled with result

## References
- `.claude/skills/solution-architect/technical-assessment/SKILL.md`
- `.claude/skills/pm/planning-session-facilitation/SKILL.md`
