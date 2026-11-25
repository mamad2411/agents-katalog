# Story Changelog Writing

## Purpose
Writes a conventional changelog per user story before the story PR merges to the release branch.

## Role
Tech Lead

## Phase
Development (before story-level PR merges)

## Triggered By
All tasks merged to story branch, story PR ready for review.

## Inputs
- All task PRs merged to the story branch
- Commit messages (conventional commits format)

## Process
1. Review all task PRs merged to this story branch.
2. Read commit messages (conventional commits format).
3. Categorise changes: features, fixes, breaking changes, migrations, dependencies.
4. Write changelog in the format below.
5. Commit to `openspec/changes/{slug}/CHANGELOG.md`.
6. Mark `story-changelog-writing` complete before story PR is reviewable.

This file is consumed by Release Manager's `changelog-aggregation` skill.

## Outputs
Location: `openspec/changes/{slug}/CHANGELOG.md`

```markdown
# Changelog — {Story Title} (KAN-{N})
# Sprint: v{X}.{Y}.{Z}
# Date: {date}

## Features
- {feature description} (KAN-{task-N})
- {feature description} (KAN-{task-N})

## Bug Fixes
- {fix description} (KAN-{bug-N})

## Breaking Changes
- {breaking change description} — Migration: {how to migrate}

## Database Migrations
- {migration description} — Files: {migration file names}

## Dependencies
- Updated {package} from {old-version} to {new-version}
- Added {package}@{version}
```

## Quality Gates
- [ ] All significant changes documented
- [ ] Breaking changes have migration instructions
- [ ] All database migrations listed with file names
- [ ] File committed to correct OpenSpec location

## References
- `.claude/skills/tech-lead/definition-of-done-enforcement/SKILL.md`
- Release Manager `changelog-aggregation`
