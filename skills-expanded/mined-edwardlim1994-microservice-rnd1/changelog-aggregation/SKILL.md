# Changelog Aggregation

## Purpose
Aggregates all Tech Lead story changelogs into the root CHANGELOG.md for the release.

## Role
Release Manager

## Phase
Release

## Triggered By
All stories in release have `story-changelog-writing` complete.

## Inputs
Reads all Tech Lead story changelogs from: `openspec/changes/*/CHANGELOG.md`

## Process
1. Read all story changelogs for the release.
2. Aggregate into root `CHANGELOG.md`.
3. Group by: Features, Bug Fixes, Breaking Changes, Migrations, Dependencies.
4. Never write original changelog entries — only aggregate existing ones.

Input to `release-notes-writing`.

## Outputs
Aggregated root `CHANGELOG.md` for the release.

## Quality Gates
- [ ] All story changelogs included
- [ ] Grouped correctly by category
- [ ] No original entries authored (aggregation only)
- [ ] Ready to feed release-notes-writing

## References
- `.claude/skills/tech-lead/story-changelog-writing/SKILL.md`
- `.claude/skills/release-manager/release-notes-writing/SKILL.md`
