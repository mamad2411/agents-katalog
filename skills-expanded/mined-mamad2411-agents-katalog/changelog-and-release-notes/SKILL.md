---
name: changelog-and-release-notes
description: Write and review changelogs, release notes, app-store update notes, launch notes, migration notes, breaking-change notices, and customer-facing product update communication for SaaS, apps, games, developer tools, desktop software, and marketplaces. Use when a release needs clear user value, risk communication, upgrade guidance, or support-aware wording.
---

# Changelog And Release Notes

Use this skill to communicate product change clearly without dumping commits.

## Workflow

1. Identify audience, release type, risk level, channels, and required actions.
2. Read `references/changelog-release-notes-patterns.md`.
3. Convert raw changes into user impact, action needed, compatibility, support, and rollout notes.
4. Separate public notes, technical changelog, store notes, and internal support notes.
5. Produce final notes and validation checklist.

## Guardrails

- Do not hide breaking changes, migrations, data changes, or pricing/support impacts.
- Do not expose secrets, internal incident details, or security exploit instructions.
- Do not write vague notes like bug fixes and improvements when users need specifics.

## Output format

```text
Release type:
Audience:
Risk:

Public notes:
- <user-facing change>

Technical/support notes:
- <compatibility, migration, known issue, support macro>

Validation:
- <check>
```
