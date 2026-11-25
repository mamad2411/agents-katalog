---
name: repo-issue-intake
description: Converts vague reports, support notes, QA findings, logs, and user requests into structured actionable issues. Use when drafting or reviewing bug reports, feature requests, reproduction steps, expected versus actual behavior, acceptance criteria, or issue evidence.
---

# Repo Issue Intake

Use this skill when turning raw information into a high-quality issue draft.

## Intake Requirements

Capture:

- concise searchable title
- issue type: bug, feature, task, incident follow-up, technical debt, question, or maintenance
- summary
- evidence
- reproduction or triggering conditions
- expected behavior
- actual behavior
- impact
- affected environment
- workaround if known
- acceptance criteria
- privacy and redaction notes
- open questions

## Behavior

- Mark unknowns explicitly.
- Do not fabricate evidence.
- Redact secrets and private data.
- Prefer a local draft before creating a tracker item.
- Search for duplicates when tracker access exists.
- Ask before posting to customer-visible or external trackers.

## Workflow

Use `workflows/issue-intake-workflow.md` for drafting a new issue or improving a weak issue report.

## Resources

- `resources/issue-quality-checklist.md`
- `resources/issue-template.md`

## Examples

- `examples/example-triage-report.md`

## Scripts

This skill owns:

```text
scripts/check-issue-draft.py
```

Run scripts with `--help` before manual use.
