# Release Scope Management

## Purpose
Maintains Must Ship / Should Ship / Can Hold classification per Epic and Story for release scope decisions.

## Role
Project Manager

## Phase
Planning + Retrospective

## Triggered By
Sprint planning, retro improvement actions added to backlog.

## Inputs
- Story/Epic list with priority scores

## Process

### Classifications
- Must Ship: blocking release, cannot go without — story blocks the release
- Should Ship: high value, strong preference to include this release
- Can Hold: defer to next release if capacity exceeded — acceptable

### Steps
1. During planning: assign initial classification to each story.
2. During sprint: update if new information changes priority.
3. During retro: update based on delivery results and improvement actions.
4. Improvement actions always start as Backlog (never auto-assigned).

### Used By
- `sprint-planning` (capacity decisions)
- Release Manager: `go-no-go-assessment` (release scope decisions)

## Outputs
Classification recorded on each story kanban card.

## Quality Gates
- [ ] Every story has a classification
- [ ] Must Ship stories never deferred without Edward's explicit approval
- [ ] Classifications updated after each retro

## References
- `.claude/skills/pm/sprint-planning/SKILL.md`
- `.claude/skills/po/retrospective-conclusion/SKILL.md`
