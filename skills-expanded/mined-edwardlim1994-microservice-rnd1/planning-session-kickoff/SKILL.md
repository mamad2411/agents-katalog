# Planning Session Kickoff

## Purpose
Loads all planning subagents with story context before Stage 1 begins, ensuring everyone starts informed.

## Role
Project Manager

## Phase
Planning (before Stage 1)

## Triggered By
`/start` command after PO creates Epic + Story cards.

## Inputs
- Story kanban cards for this planning session
- Previous sprint retro summary
- Current kanban board state
- Security knowledge base

## Process
1. Read all story kanban cards for this planning session.
2. Read previous sprint retro summary (`openspec/changes/retro-*/retro.md`).
3. Read current kanban board state (active risks, carry-over items).
4. Read security-knowledge-base for active CVEs.
5. Load all planning subagents with this context:
   - Story cards and their AC
   - Previous sprint learnings
   - Active risks and blockers
   - Architecture axioms (from CLAUDE.md)
6. Confirm all subagents loaded and ready.
7. Hand control to `planning-session-facilitation`.

## Outputs
All planning subagents context-loaded, ready for Stage 1.

## Quality Gates
- [ ] Previous retro summary read
- [ ] All story cards read
- [ ] Active risks loaded
- [ ] All 6 planning subagents confirmed ready

## References
- `.claude/skills/pm/planning-session-facilitation/SKILL.md`
- `.claude/skills/po/epic-and-story-writing/SKILL.md`
