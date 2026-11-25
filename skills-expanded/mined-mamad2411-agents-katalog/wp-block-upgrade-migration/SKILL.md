---
name: wp-block-upgrade-migration
description: Plans and reviews WordPress block upgrades, package alignment, API feature gates, deprecations, serialized-content migrations, and compatibility testing.
---

# WordPress Block Upgrade and Migration

Use this skill when raising WordPress support, changing Block API behavior, updating `@wordpress/*` packages, or repairing historical content.

## Procedure

1. Inventory Core, Gutenberg, PHP, Node.js, package, and browser versions.
2. Read `resources/compatibility-matrix.md` and `resources/deprecation-checklist.md`.
3. Identify every API, metadata property, support flag, package export, markup contract, and generated artifact affected.
4. Separate runtime compatibility changes from tooling-only changes.
5. Preserve historical content with deprecations or explicit migration planning.
6. Update packages as a coherent compatibility set, not arbitrary independent `latest` upgrades.
7. Test minimum and latest versions plus historical serialized fixtures.
8. Document changed requirements and rollback behavior.

## Workflow

Use `workflows/upgrade-block-workflow.md`.

## Resources

- `resources/compatibility-matrix.md`
- `resources/deprecation-checklist.md`

## Example

- `examples/deprecation-migration-example.md`
