---
name: wp-divi-5-update-management
description: Plans and executes controlled Divi 5 minor-version updates with release-note review, staging, evidence capture, cache-aware verification, explicit rollback criteria, and production promotion gates.
---

# Divi 5 Update Management

Use this skill for a Divi 5 update, update-related regression review, or release-readiness decision.

## Required Inputs

- Current and target Divi versions.
- Current WordPress, PHP, child theme, extensions, and cache stack.
- Relevant Divi release notes.
- Backup and staging evidence.
- Critical journey list.
- Maintenance and rollback window.

## Procedure

1. Read the official Divi 5 changelog from the current version through the target version.
2. Classify entries affecting migration, rendering, Theme Builder, third-party modules, REST/security, cache, performance, and WooCommerce.
3. Snapshot versions, screenshots, logs, cache configuration, and known defects.
4. Confirm restorable backup and representative staging.
5. Run the included command guard with `--help` and test planned commands with `--check-command` when useful.
6. Update staging without bundling unrelated changes.
7. Verify before clearing caches, then clear one cache layer at a time and record the result.
8. Test critical logged-out frontend and Visual Builder journeys.
9. Test any area named in relevant release notes.
10. Promote only when acceptance checks pass and rollback remains viable.
11. Produce a change record.

## Safety Rules

- Do not bulk-update WordPress, Divi, and all plugins as one unreviewed mutation.
- Do not treat cache clearing as a harmless substitute for diagnosis; capture evidence first.
- Do not change multiple performance options at once.
- Do not overwrite the Divi theme or import/reset databases without explicit approval and recovery evidence.
- Stop when a critical journey fails or the migration/update state is uncertain.

## Workflow

Use [update-divi-5-workflow.md](workflows/update-divi-5-workflow.md).

## Resources

- [update-verification-checklist.md](resources/update-verification-checklist.md)
- [update-change-record-example.md](examples/update-change-record-example.md)

## Script

Run `scripts/divi-command-safety.py --help` before direct use. The script is also invoked by `hooks.json` as a fail-secure command gate.

## Output

Return:

- Update decision.
- Release-note impact summary.
- Backup/staging status.
- Planned commands and command-guard results.
- Acceptance and rollback criteria.
- Verification results.
- Remaining risk and owners.
