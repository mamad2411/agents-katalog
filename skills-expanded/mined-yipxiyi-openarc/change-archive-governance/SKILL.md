---
name: change-archive-governance
description: Use when maintaining AI-assisted change memory, CHANGELOG_AI.md, docs/archive, historical context retention, archive indexes, or context-budget-aware repository reading in OpenArc repositories.
---

# Change Archive Governance

Use this skill when a repository needs AI change memory or archive policy.

## Goal

Keep recent AI-assisted changes visible while preserving older history outside the default context path.

## Files

Default files:

- `docs/CHANGELOG_AI.md`
- `docs/archive/`
- `docs/archive/README.md` or `docs/archive/ARCHIVE_INDEX.md`

Use `templates/CHANGELOG_AI.template.md` and `templates/ARCHIVE_INDEX.template.md` when creating new files.

## CHANGELOG_AI Rules

`docs/CHANGELOG_AI.md` contains only recent AI-assisted changes.

Recommended retention:

- Keep the last 10-20 entries visible.
- Move older entries to `docs/archive/`.
- Do not delete historical context.

Each entry should record:

- summary
- changed files
- key decisions
- verification
- remaining work

## Archive Rules

Archive old or completed historical context into `docs/archive/`.

Examples:

- `docs/archive/CHANGELOG_2026_Q2.md`
- `docs/archive/TASKS_2026_Q2.md`
- `docs/archive/DECISIONS_2026_Q2.md`
- `docs/archive/SPEC_editor_deprecated.md`

Archived files are not read by default. Load them only for regressions, architectural history, or prior AI decision investigation.

## Context Budget Rule

Use the smallest context required to safely complete the task.

Do not automatically load:

- archived changelogs
- old completed tasks
- deprecated specs
- outdated implementation notes
- unrelated source files

Only load archived context when the task explicitly requires historical investigation.

## Workflow

1. Check whether `docs/CHANGELOG_AI.md` and `docs/archive/` exist.
2. Create missing files from templates when the user asks for setup.
3. Add concise recent entries after implementation or documentation work.
4. When entries exceed the retention window, move older entries into archive files.
5. Update the archive index with path, date range, topic, and when to read.
6. Report what was kept visible and what was archived.

## Rules

- Do not replace `CHANGELOG.md`; it tracks project releases.
- Do not make `docs/archive/*` part of default reading.
- Prefer moving historical context over deleting it.
- Preserve existing repository structure and naming when it is coherent.
