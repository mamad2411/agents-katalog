# PR Kanban Sync Pipeline

## Purpose
Keeps kanban card status synchronised with PR lifecycle events automatically.

## Role
DevOps Engineer

## Phase
Development

## Triggered By
Any PR event (opened, merged, closed).

## Inputs
- PR branch name (`{type}/{KAN-N}-{description}`)

## Process
GitHub Actions triggered on any PR event.
1. Extract `KAN-{N}` from branch name pattern: `{type}/{KAN-N}-{description}`.
2. Actions per event:
   - PR opened → kanban card: In Review
   - PR merged → kanban card: Done
   - PR closed (no merge) → kanban card: Blocked
3. Install kanban-cli in the GitHub Actions workflow.
4. Read/write `.kanban/boards.json` via kanban-cli commands.
5. Commit updated `boards.json` back to repo.

## Outputs
Kanban card status kept in sync with PR state automatically.

## Quality Gates
- [ ] KAN-{N} correctly extracted from branch name
- [ ] Card status transitions match PR event
- [ ] boards.json committed back after every sync

## References
- `.claude/skills/pm/kanban-board-management/SKILL.md`
