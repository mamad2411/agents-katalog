# Release Documentation

## Purpose
Publishes a version-specific release page to the docs site.

## Role
Technical Writer

## Phase
Release (after Release Manager produces release notes)

## Triggered By
Release Manager `release-notes-writing` complete.

## Inputs
- Release Manager's `release-notes-writing` output

## Process
Take Release Manager's `release-notes-writing` output. Add formatted `CHANGELOG.md` entry for this release. Publish version-specific release page in docs site.

Format: What's New, What's Fixed, Breaking Changes, Migration Guide.

## Outputs
Location: `apps/docs/src/content/internal/latest/releases/`

## Quality Gates
- [ ] Release notes incorporated accurately
- [ ] CHANGELOG.md entry formatted and included
- [ ] All four sections present
- [ ] Published to correct docs location

## References
- `.claude/skills/release-manager/release-notes-writing/SKILL.md`
- `.claude/skills/release-manager/changelog-aggregation/SKILL.md`
