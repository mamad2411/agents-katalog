---
name: azure-blob-storage-12-layout-design
description: Designs Azure Blob Storage SDK v12 container and path layouts. Use for namespace separation, public/private boundaries, generated artifacts, exports, temp/cache/backup prefixes, lifecycle boundaries, and storage path policy reviews.
license: MIT
compatibility: Requires repository access. Optional Azure resource context can improve reviews but is not required.
---

# Azure Blob Storage 12 Layout Design Skill

Use this skill when designing or reviewing Blob Storage containers, prefixes, naming conventions, and access boundaries.

## When To Use

Use when a task involves:

- New containers or top-level prefixes.
- Public versus private storage separation.
- Generated artifacts or external downloads.
- Exports, imports, backups, temporary files, cache files, or diagnostics.
- Lifecycle, retention, immutability, or access policy differences.
- Multi-tenant or multi-workload storage layouts.

## Required First Steps

1. Read `resources/namespace-layout-matrix.md`.
2. If writing or changing path conventions, read `resources/path-policy-schema.md`.
3. If scanning files or proposed changes, run `scripts/azure-blob-storage-12-path-policy-check.py --help` first.
4. Do not introduce application-domain labels unless they already exist in the repository and are part of the user request.

## Workflows

- `workflows/design-storage-layout-workflow.md`: Use for container and prefix layout design.

## Resources

- `resources/namespace-layout-matrix.md`: Classification matrix for layout decisions.
- `resources/path-policy-schema.md`: Template for documenting path rules.

## Scripts

- `scripts/azure-blob-storage-12-path-policy-check.py`: Read-only scanner and hook for suspicious mixed path classifications.

## Examples

- `examples/container-path-layouts.md`: Domain-neutral layouts and anti-patterns.

## Layout Rules

- Prefer separate containers when access, retention, immutability, lifecycle, ownership, or data classification differs.
- Treat prefixes as organization and routing aids, not security boundaries.
- Keep public outputs isolated from internal and private data.
- Define path templates centrally.
- Avoid leaking tenant, user, principal, or internal IDs through public paths.
