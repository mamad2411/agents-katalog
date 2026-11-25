---
title: W_SINGLE_FILE_SKILL
summary: Warning: the skill arrived as a single Markdown file that was treated as SKILL.md; it is accepted, but the canonical layout is a skill folder.
related: pages/publish, actions/publish/issue-help
---

## What it means

Warning: skill arrived as a single .md that was treated as SKILL.md (common for Reckon learned skills). Severity label: **Warning**. Issue codes are stable across API, UI, and import. On Publish, Blocking errors prevent a successful parse; Warnings annotate the result and should still be reviewed.

## Common causes

Uploading nutrition-migration.md instead of SKILL.md inside a folder. Confirm the selected artifact type and that paths match the canonical layout for skill (`skills/<name>/`), command (`commands/<name>.md`), agent (`agents/<name>.md`), and hook (`hooks/hooks.json`).

## How to fix

Optional: rename to SKILL.md under skills/<name>/ for the canonical layout. Re-run validation on the Publish page and confirm the issue disappears from the issue list (issue-help links back to this topic).

```
# accepted with warning
nutrition-migration.md
# canonical
skills/nutrition-migration/SKILL.md
```
