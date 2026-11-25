# Kanban Board Management

## Purpose
Primary sprint tracking tool. All execution state lives in the kanban board. Uses kanban-cli MCP tools.

## Role
Project Manager

## Phase
All phases

## Triggered By
Sprint start, task updates, status changes.

## Inputs
- kanban-cli MCP tool access
- Current sprint task list

## Process

### Card Type Convention
`type: epic | story | feature | task | api | qa | security | devops | bug-feature | bug-story | bug-release | hotfix | tech-debt | risk | knowledge-update`

### Daily Responsibilities
- Scan for blocked cards (`status: blocked`)
- Dependency health check: are all blocking relations still valid?
- Surface broken dependency chains to Tech Lead immediately
- Update card descriptions with latest status

### Card Creation Rules
- Epic → `us/` branch mapping
- Story → `us/` branch
- Feature → `feat/` branch
- Task → `task/` branch
- API → `api/` branch (Data Engineer)
- QA → `qa/` branch (QA Engineer)
- Security → `security/` branch
- DevOps → `devops/` branch
- Bug-feature → `bugfix/` from `feat/`
- Bug-story → `bugfix/` from `us/`
- Bug-release → `bugfix/` from `release/`

## Outputs
Kanban board reflects current sprint state accurately.

## Quality Gates
- [ ] All cards have correct type label
- [ ] All cards linked to their branch
- [ ] Blocked cards have escalation path
- [ ] Dependency chains verified daily

## References
- Branch hierarchy convention (CLAUDE.md)
- `.claude/skills/shared/status-reporting/SKILL.md`
- `.claude/skills/shared/risk-logging/SKILL.md`
