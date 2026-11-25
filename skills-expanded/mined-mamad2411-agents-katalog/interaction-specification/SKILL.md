# Interaction Specification

## Purpose
Specifies purely behavioural content and interaction of each screen — what is present and what it does, not how it looks.

## Role
UI/UX Designer

## Phase
Planning (Stage 4)

## Triggered By
`user-flow-definition` complete.

## Inputs
- `user-flow-definition` output
- Story AC (every AC must map to at least one interaction)

## Process
Per screen, document:
1. What elements are present (input field, button, table, etc.)
2. What each element does when interacted with
3. What feedback the user receives (success, error, loading, empty states)
4. What navigation/routing occurs

Explicitly excludes: visual layout, colours, spacing, animations.

## Outputs
Interaction specification consumed by:
- QA (element discovery for frontend interaction tests)
- Frontend/Mobile (knows what to build)

## Quality Gates
- [ ] Every AC maps to at least one interaction
- [ ] No visual/layout detail included
- [ ] Feedback states (success/error/loading/empty) specified per screen
- [ ] Navigation/routing specified

## References
- `.claude/skills/ui-ux-designer/user-flow-definition/SKILL.md`
- `.claude/skills/qa-engineer/frontend-interaction-test-design/SKILL.md`
