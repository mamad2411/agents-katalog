# Acceptance Criteria Challenge

## Purpose
Challenges every AC for testability before planning proceeds, tightening vague or unautomatable criteria.

## Role
QA Engineer

## Phase
Planning (Stage 2)

## Triggered By
Stage 1 complete, PO has presented story.

## Inputs
- User Story AC
- Wireframe (secondary input, if available)

## Process
1. Read all AC from the User Story (primary input). Wireframe is secondary — used only for element discovery when available.
2. Challenge each AC for testability:
   - Is it specific?
   - Is it measurable?
   - Is it automatable?
   - Does it cover the unhappy path, not just the happy path?
3. Missing element visible in wireframe but absent from AC → flag to UI/UX during planning.
4. Vague AC → rewrite collaboratively with PO before planning proceeds.

## Outputs
Tightened, testable AC on the story kanban card.

## Quality Gates
- [ ] Every AC challenged for specificity, measurability, automatability
- [ ] Unhappy paths covered, not just happy path
- [ ] Vague AC rewritten collaboratively
- [ ] Wireframe/AC mismatches flagged to UI/UX

## References
- `.claude/skills/qa-engineer/test-strategy-definition/SKILL.md`
- `.claude/skills/ui-ux-designer/interaction-specification/SKILL.md`
