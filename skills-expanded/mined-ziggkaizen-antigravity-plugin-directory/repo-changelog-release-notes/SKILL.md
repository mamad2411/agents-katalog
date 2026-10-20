---
name: repo-changelog-release-notes
description: Drafts and reviews changelogs, release notes, migration notes, and upgrade summaries from concrete repository changes. Use when summarizing changes for users, maintainers, operators, or downstream teams.
---

# Changelog and Release Notes

Use this skill to summarize repository changes accurately.

## Process

1. Identify actual changes from repository evidence.
2. Group by impact.
3. Call out breaking changes and required user action.
4. Include compatibility and migration notes when verified.
5. Avoid internal-only details unless the audience needs them.
6. Avoid claiming release status for unreleased changes.
7. Keep tone factual and concise.

## Workflows

- `workflows/changelog-drafting-workflow.md`
- `workflows/release-notes-review-workflow.md`

## Resources

- `resources/release-notes-template.md`
- `resources/changelog-quality-checklist.md`

## Examples

- `examples/release-notes-example.md`

## Scripts

This skill owns `scripts/changelog-structure-check.py`. Run it with `--help` before manual use.
