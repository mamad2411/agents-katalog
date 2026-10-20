# Release Retrospective Handoff

## Purpose
Summarises the release for the retrospective session.

## Role
Release Manager

## Phase
Retrospective

## Triggered By
`/metrics` command before `/retro`.

## Inputs
- Release cycle data for the sprint (RC cycles, hotfixes, deployment durations, rollbacks)

## Process
Summarise:
- RC cycles needed this sprint
- Hotfixes this sprint
- Deployment duration
- Rollbacks (should be 0)
- Must Ship delivery rate
- Changelog completeness (all stories documented?)

## Outputs
Contributes to Section 6 of `retro-template.md`.

## Quality Gates
- [ ] All metrics are actual counts, not estimates
- [ ] Changelog completeness verified against all shipped stories
- [ ] Report ready before /retro session begins

## References
- `.claude/skills/pm/retrospective-facilitation/SKILL.md`
- `openspec/retro-template.md`
