---
name: wp-site-editor-source-control
description: Reconciles WordPress Site Editor database-saved templates and global styles with block-theme files and source control. Use before releases, migrations, reviews, or when file changes do not match the active frontend.
---

# wp-site-editor-source-control

Use this skill whenever Site Editor changes may exist outside the repository.

## Required Inputs

- Theme and child-theme paths.
- WordPress environment and database access owner.
- Current branch and clean working-tree state.
- List of edited templates, parts, global styles, navigation, and patterns.
- Distribution goal: site-only customization or reusable theme release.
- Backup and reset/rollback method.

## Principles

- Inspect before resetting.
- Preserve user-owned content.
- Do not assume export output is a clean source diff.
- Compare normalized block markup and JSON.
- Copy only intended distributable artifacts into source.
- Verify from a clean or reset-override state.
- Keep an explicit ledger.

## Workflow

Use [`workflows/synchronize-site-editor-workflow.md`](workflows/synchronize-site-editor-workflow.md).

## Resource

Use [`resources/source-of-truth-ledger-template.md`](resources/source-of-truth-ledger-template.md).

## Completion Evidence

Record:

- Database artifacts discovered.
- Backup/export location.
- Files updated.
- Artifacts intentionally left site-owned.
- Overrides reset or isolated.
- Clean-site verification result.
- User content preserved.
