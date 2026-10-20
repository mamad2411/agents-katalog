# Release Branch Management

## Purpose
Creates and manages the release branch for the sprint.

## Role
Release Manager

## Phase
Development + Release

## Triggered By
`/kickoff` command.

## Inputs
- Approved sprint plan

## Process
1. Create `release/v{X}.{Y}.{Z}` from `main` at `/kickoff`.
2. Monitor release branch for correct story merges.
3. After successful production merge: mark branch for deletion 30 days later.

## Rule
NEVER reuse a release branch — each sprint gets a new one.

## Outputs
Active release branch tracked through the sprint; retention marker after production merge.

## Quality Gates
- [ ] Release branch created only at /kickoff
- [ ] Only correct story branches merge into it
- [ ] 30-day retention marker applied after production merge
- [ ] No release branch ever reused

## References
- `.claude/skills/release-manager/versioning/SKILL.md`
- `.claude/skills/pm/milestone-management/SKILL.md`
