---
name: wp-divi-5-migration-readiness
description: Plans and reviews safe Divi 4 to Divi 5 migrations, including inventory, backup and staging evidence, Migrator compatibility analysis, legacy-module risk, rollback criteria, and post-migration verification.
---

# Divi 5 Migration Readiness

Use this skill before approving, running, or validating a Divi 4 to Divi 5 migration.

## Required Inputs

- Source and target environment.
- Installed WordPress, Divi, PHP, plugin, and child-theme versions.
- Backup and restore evidence.
- Staging fidelity.
- Third-party Divi module inventory and compatibility claims.
- Migrator compatibility report.
- Critical page, template, form, menu, search, archive, 404, and integration journeys.
- Maintenance window, owners, success criteria, and rollback criteria.

## Procedure

1. Run the filesystem inspector with `--help`, then inspect a local WordPress copy when available.
2. Run the export scanner with `--help` against a current read-only export when available.
3. Treat script output as inventory evidence, not as Migrator approval.
4. Confirm a full restorable backup and representative staging environment.
5. Update inventory and review third-party Divi 5 compatibility.
6. Install Divi 5 on staging without opening normal pages first.
7. Open the Divi 5 Migrator and review all report sections.
8. Record unsupported modules and every item expected to use backward-compatibility mode.
9. Apply the migration decision matrix.
10. Define success, stop, and rollback criteria before migration.
11. Follow the migration workflow.
12. Verify the logged-out frontend and Visual Builder after conversion.
13. Produce a migration record with versions, timestamps, findings, decisions, and remaining legacy work.

## Decision Rules

- Defer when backup recovery is unproven, staging is not representative, critical extensions are unsupported, or the legacy footprint exceeds the accepted threshold.
- Proceed with conditions when limited legacy content has owners, tests, and a replacement plan.
- Proceed when critical journeys are supported and the rollback window is viable.
- Never infer compatibility from the absence of filesystem markers alone.

## Workflow

Use [plan-and-run-divi-migration-workflow.md](workflows/plan-and-run-divi-migration-workflow.md).

## Resources

- [migration-readiness-checklist.md](resources/migration-readiness-checklist.md)
- [migration-decision-matrix.md](resources/migration-decision-matrix.md)
- [migration-runbook-example.md](examples/migration-runbook-example.md)

## Scripts

Run each script with `--help` first:

- `scripts/inspect-divi-installation.py`
- `scripts/scan-divi-content-export.py`

Both scripts are read-only and have documented blind spots.

## Output

Return:

- Readiness status: proceed, proceed with conditions, or defer.
- Evidence summary.
- Compatibility-mode inventory.
- Critical risks and owners.
- Staging test plan.
- Production promotion criteria.
- Rollback path and trigger.
- Remaining manual verification.
