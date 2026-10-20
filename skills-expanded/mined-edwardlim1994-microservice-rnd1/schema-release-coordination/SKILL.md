# Schema Release Coordination

## Purpose
Coordinates the signal that generated types are ready so Backend and Frontend developers can begin implementation.

## Role
Data Engineer

## Phase
Development

## Triggered By
`api-type-generation` complete and committed.

## Inputs
- Confirmation of successful `api-type-generation`

This skill is about communication and unblocking — the technical work is done in `api-type-generation`. This wraps it up and unblocks the team.

## Process
1. Confirm `api-type-generation` completed successfully.
2. Confirm generated files committed and pushed.
3. Update kanban `api/` card: move to Done.
4. Update kanban card description with:
   - Which packages were generated
   - Which backend task cards are now unblocked
   - Which frontend/mobile task cards will be unblocked after backend merges
5. Signal PM that typing is ready.
6. If schema deviates from Architect's `design.md`: flag to Architect immediately.

## Outputs
Unblocked task cards, PM signalled.

## Quality Gates
- [ ] Generated types confirmed committed and pushed
- [ ] Kanban api/ card moved to Done
- [ ] All blocked task cards explicitly listed as unblocked
- [ ] PM signalled

## References
- `.claude/skills/data-engineer/api-type-generation/SKILL.md`
- `.claude/skills/pm/kanban-board-management/SKILL.md`
