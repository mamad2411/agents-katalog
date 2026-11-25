# Epic and Story Writing

## Purpose
Creates well-structured Epic and User Story kanban cards from confirmed requirements before the planning session begins.

## Role
Product Owner

## Phase
Planning (Stage 1, before session kickoff)

## Triggered By
Confirmed Problem Statement from `requirements-elicitation`.

## Inputs
- Confirmed Problem Statement

## Process
1. Create Epic kanban card:
   - Title: `[Epic] {Feature Name}`
   - Body:
     ```
     ## Problem Statement — {from requirements-elicitation}
     ## Business Value — {why this matters}
     ## Scope — {what is included}
     ## Out of Scope — {explicitly excluded}
     ## Acceptance Criteria — {high-level done definition}
     ## Dependencies — {other epics or services}
     ```
   - Labels: `type: epic`, `priority: TBD`

2. Break Epic into User Stories (one story = one user-facing capability, completable in one sprint):
   - Title: `[Story] {Short description}`
   - Body:
     ```
     ## User Story
     As a {user type}, I want to {action} so that {outcome}
     ## Acceptance Criteria
     - [ ] Given {context}, when {action}, then {result}
     ## Dependencies
     - Depends on: #{issue} — {reason}
     ## Notes
     {additional context for developers}
     ```
   - Labels: `type: story`, `priority: TBD`
   - Link: Part of #{epic card number}

3. Stories are platform-agnostic (platform decided during planning).
4. One story can span multiple services (Architect flags boundaries).
5. Link all stories to Epic in kanban.
6. Signal PM: stories ready for planning session kickoff.

## Outputs
Epic card (KAN-{N}), User Story cards (KAN-{N+1}...) in kanban.

## Quality Gates
- [ ] Every story has at least one Given/When/Then AC
- [ ] Stories are platform-agnostic
- [ ] All stories linked to parent Epic
- [ ] PM signalled that stories are ready

## References
- `.claude/skills/po/requirements-elicitation/SKILL.md`
- `.claude/skills/pm/planning-session-kickoff/SKILL.md`
- `.claude/skills/pm/kanban-board-management/SKILL.md`
