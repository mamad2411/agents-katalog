---
name: wp-plugin-development-plan-and-scaffold
description: Plans and scaffolds a compatibility-aware WordPress plugin with clear boundaries, lifecycle, dependencies, storage, tests, and release constraints. Use when starting a new plugin or restructuring an unsafe bootstrap.
---

# WordPress Plugin Planning and Scaffolding

Use this skill before writing a new plugin or when an existing plugin has unclear ownership, bootstrap, lifecycle, dependency, or compatibility behavior.

## Inputs to collect

- User-visible goal and explicit non-goals.
- Distribution channel: private, commercial, WordPress.org, must-use, or bundled.
- Minimum and tested WordPress versions.
- Minimum and tested PHP versions.
- Required or optional plugin dependencies.
- Multisite and network-activation expectations.
- Data ownership, retention, privacy, export, erasure, and uninstall policy.
- Admin, frontend, REST, Ajax, cron, webhook, CLI, or external-service entry points.
- Build, test, packaging, deployment, and rollback process.

Do not invent missing compatibility or data-retention decisions. Record them as blockers.

## Method

1. Use the [plugin boundary and architecture matrix](resources/plugin-boundary-and-architecture-matrix.md) to confirm that the requested behavior belongs in a plugin.
2. Inventory the target project's WordPress, PHP, database, dependency, Multisite, and distribution constraints.
3. Define a unique slug, PHP namespace, global prefix, text domain, REST namespace, option prefix, cron prefix, and script/style handle prefix.
4. Separate the bootstrap, feature modules, integrations, administration, public rendering, data access, migrations, and tests according to actual complexity.
5. Define activation, deactivation, uninstall, schema-version, dependency-failure, and interrupted-upgrade behavior before coding.
6. Decide which WordPress APIs own each data type and entry point.
7. Apply the [plugin architecture checklist](resources/plugin-architecture-checklist.md).
8. Use the [minimal plugin bootstrap](examples/minimal-plugin-bootstrap.md) only as a conservative reference; replace its example compatibility values with tested project values.
9. Run the [plan and scaffold workflow](workflows/plan-and-scaffold-plugin-workflow.md).

## Required output

Produce:

- a one-paragraph plugin boundary statement
- explicit in-scope and out-of-scope lists
- compatibility contract
- component and file tree
- identifier/prefix map
- entry-point and authorization map
- data ownership and lifecycle plan
- dependency behavior
- test matrix
- packaging and release plan
- unresolved decisions and stop conditions

## Design rules

- Keep the main plugin file small and deterministic.
- Prefer one clear runtime bootstrap over many files with load-time side effects.
- Add layers only when they isolate real responsibilities or testing boundaries.
- Do not create a custom table when options, metadata, taxonomies, or custom post types fit the access pattern.
- Do not put persistent feature functionality in a theme.
- Do not hide destructive data deletion in deactivation.
- Do not claim support for a version that is absent from the test plan.
- Do not include secrets or production credentials in scaffolds or examples.
