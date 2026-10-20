---
name: postgres-analyze-migration
description: Analyze migrations to Azure Database for PostgreSQL Flexible Server from PostgreSQL or other supported sources, including Azure migration tooling, compatibility, extensions, schema/data movement, validation, cutover, and rollback. Use for cloud migration planning.
---

# Analyze Migration

1. Inventory source engine/version, size, schemas, extensions, users, workload, and downtime constraints.
2. Identify the currently supported Azure migration path/tooling for the source and target.
3. Assess PostgreSQL compatibility, unsupported extensions/features, networking, and identity.
4. Define data validation, synchronization/lag checks, application cutover, and rollback.
5. For heterogeneous migrations, separate automated conversion from manual semantic remediation.
6. Do not execute production cutover without explicit authorization.

## Output
- Source/Target Profile
- Compatibility Gaps
- Migration/Cutover Plan
- Validation/Rollback
- Recommended Sequence
