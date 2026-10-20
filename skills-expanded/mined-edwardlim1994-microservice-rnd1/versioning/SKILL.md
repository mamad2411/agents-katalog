# Versioning

## Purpose
Decides semantic version bumps and manages RC/final tags for the release.

## Role
Release Manager

## Phase
Release

## Triggered By
Release branch created; each UAT cycle; final release.

## Inputs
- Nature of changes in the release (features, fixes, breaking changes)
- Architect input on breaking changes

## Process

### Semantic Versioning Decision (jointly with Architect)
- Patch (`x.x.1`): bug fixes only
- Minor (`x.1.0`): new features, backward compatible
- Major (`1.0.0`): breaking changes

### Tagging
- RC tags: `v{X}.{Y}.{Z}-rc{N}` on release branch per UAT cycle.
- Final tag: `v{X}.{Y}.{Z}` after UAT passes.
- Same tag applied on `main` after successful merge.

## Outputs
Version number decided; RC and final tags applied.

## Quality Gates
- [ ] Version bump type agreed with Architect
- [ ] RC tag created per UAT cycle
- [ ] Final tag matches RC that passed staging (no rebuild)
- [ ] Same tag applied to main after merge

## References
- `.claude/skills/release-manager/release-branch-management/SKILL.md`
- `.claude/skills/solution-architect/api-deprecation-management/SKILL.md`
