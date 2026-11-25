---
name: migrate-data
description: Make safe, reversible database schema and data changes. Use for migrations, DDL, backfills, seeds, and data rollout/rollback work.
---

# INPUTS
- Approved migration task, resolved database context, confirmed target database, schema contract, and rollout constraints.

# PRECONDITIONS
- Identify the actual target host/port or container; have a tested rollback; obtain explicit confirmation for destructive work.

# ACTIONS
- Plan expand, migrate, and contract phases.
- Implement up and down migrations, batch large changes, and document rollout and rollback.
- Validate against an identified non-production target.

# OUTPUTS
- Migration files, rollback path, target confirmation, and migration evidence.

# VALIDATION
- Run up/down checks and application compatibility checks; verify destructive-operation evidence when applicable.

# FORBIDDEN
- Do not run against an unconfirmed target, perform destructive operations without user confirmation, or mark delivery complete.
