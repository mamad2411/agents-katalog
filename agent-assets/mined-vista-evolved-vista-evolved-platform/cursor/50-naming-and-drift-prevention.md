# Naming and Drift Prevention

## Canonical Names

These are the official names. Do NOT use old names in new code, comments, UI text, or documentation.

| Component | Official Name | Old Names (do not use) |
|-----------|--------------|----------------------|
| `apps/control-plane/` | Platform Operations Console | Operator Console, Control Panel |
| `apps/control-plane-api/` | Platform Operations API | Control Plane API |
| `apps/tenant-admin/` | Site Administration Console | Tenant Admin, Practice Admin |
| Platform PostgreSQL | Platform DB (`ve-platform-db`) | Control Plane DB |

## Drift Prevention Rules

1. **No stale references.** When renaming a component, update ALL references: HTML titles, JS comments, CSS class names, documentation, E2E tests, README files.
2. **No orphan documentation.** When a feature is removed, remove its documentation entry from `mkdocs.yml` and the corresponding file.
3. **No orphan CSS.** When a UI component is removed, remove its CSS rules.
4. **No orphan routes.** When a backend route is removed, remove its proxy in the console server and its entry in the OpenAPI spec.
5. **Source of truth alignment.** After any change, verify `docs/reference/source-of-truth-index.md` still accurately reflects canonical file locations.

## Contract Alignment

After adding or modifying API routes:
1. Update the OpenAPI spec in `packages/contracts/openapi/`
2. Verify the `mkdocs.yml` nav includes any new docs
3. Verify `docs/reference/port-registry.md` if ports changed
