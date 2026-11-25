---
name: wp-block-theme-testing-release
description: Audits, tests, packages, updates, and prepares a WordPress block theme for release with structural inspection, clean-site verification, editor/frontend parity, accessibility, compatibility, and user-customization preservation. Use before delivery or publication.
---

# wp-block-theme-testing-release

Use this skill before client delivery, a theme update, WordPress.org submission, or a compatibility-range change.

## Required Inputs

- Theme path and release version.
- Minimum/tested WordPress and PHP versions.
- Distribution target.
- Dependency and asset licenses.
- Source-of-truth ledger.
- Representative content and test environments.
- Previous release for upgrade testing.

## Workflow

Use [`workflows/review-release-block-theme-workflow.md`](workflows/review-release-block-theme-workflow.md).

## Resource

Use [`resources/block-theme-release-checklist.md`](resources/block-theme-release-checklist.md).

## Script

Run [`scripts/inspect-block-theme.py`](scripts/inspect-block-theme.py) with `--help` first. It is read-only and cannot see database overrides or replace runtime/schema testing.

## Completion Evidence

Record:

- Inspector output.
- JSON/schema validation.
- Tested WordPress/PHP matrix.
- Clean-site and upgrade tests.
- Editor/frontend/accessibility results.
- Package inventory and license review.
- User-customization preservation result.
- Known limitations and rollback plan.
