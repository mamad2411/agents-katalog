# Security Story Review

## Purpose
Challenges acceptance criteria for missing security requirements and verifies auth assumptions are correctly stated.

## Role
Security Engineer

## Phase
Planning (Stage 2)

## Triggered By
`threat-modelling` complete.

## Inputs
- User Story AC
- `threat-modelling` findings

## Security AC Template
```
Given: {attack scenario or threat vector}
When: {attacker attempts action}
Then: {system must respond with specific defence}
```

## Process
1. Read all AC from User Story.
2. Check for missing security AC:
   - Is authentication requirement stated?
   - Is authorisation (what roles can do what) specified?
   - Are input validation requirements stated?
   - Are error response requirements stated (no sensitive data in errors)?
   - Are rate limiting requirements stated for public endpoints?
3. Check for incorrect auth assumptions:
   - Story assumes auth handled elsewhere when it shouldn't
   - Story exposes endpoint without stating auth requirement
4. Write missing security AC in Given/When/Then format.
5. Add security AC to User Story kanban card.
6. Apply sign-off label when complete:
   - `security: cleared` (no issues)
   - `security: conditional` (cleared with conditions noted)
   - `security: blocked` (cannot proceed)

Sign-off label REQUIRED before PM can set `status: ready` on any story.

## Outputs
Security AC added to story, sign-off label applied.

## Quality Gates
- [ ] All AC reviewed for security implications
- [ ] Missing security AC added in Given/When/Then format
- [ ] Sign-off label applied to story

## References
- `.claude/skills/security-engineer/threat-modelling/SKILL.md`
- `.claude/skills/pm/kanban-board-management/SKILL.md`
