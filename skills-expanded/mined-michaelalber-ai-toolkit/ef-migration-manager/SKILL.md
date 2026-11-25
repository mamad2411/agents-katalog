---
name: ef-migration-manager
audience: team
description: >
  EF Core migration lifecycle with safety checks and rollback planning. Use when
  creating, reviewing, or applying database migrations in .NET projects.
  Do NOT use when the goal is initial schema design or ad-hoc SQL management;
  Do NOT use when the project uses Dapper or raw SQL without an EF Core DbContext.
---

# EF Core Migration Manager

> "Data is a precious thing and will last longer than the systems themselves."
> -- Tim Berners-Lee

## Core Philosophy

This skill manages the full Entity Framework Core migration lifecycle: **Plan → Create → Review SQL → Test Rollback → Apply**. Every migration is treated as a potentially destructive operation that demands verification before execution.

**Non-negotiable constraints:**
1. **Never apply a migration without reviewing the generated SQL** -- EF Core's migration builder abstracts the actual DDL; always inspect what will run.
2. **Every migration must have a verified rollback path** -- Confirm `Down()` correctly reverses all changes before applying `Up()`.
3. **Data preservation is paramount** -- Schema changes that risk data loss require a data migration plan and a backup strategy.
4. **Migrations must be idempotent-safe** -- Production scripts require `--idempotent`. Manual SQL requires existence checks.
5. **One concern per migration** -- Bundling unrelated changes makes rollback dangerous and review difficult.

## Workflow

The migration lifecycle flows: **PLAN → CREATE → REVIEW SQL → TEST ROLLBACK → APPLY**; on apply failure, emergency rollback returns to PLAN.

### Pre-Flight Checklist

Before creating any migration:
- [ ] All current migrations are applied (`dotnet ef migrations list`)
- [ ] Model snapshot is in sync with the database
- [ ] No pending changes from other developers
- [ ] Branch is up to date with main/develop
- [ ] Database backup exists (for staging/production)

### Data Loss Assessment

Before creating a migration, classify the change: column drop or table drop with data → **Critical**; type narrowing or NOT NULL addition on existing rows → **High**; widening type change or empty table removal → **Low**; additive change → **None**. See `references/data-loss-matrix.md` for full risk matrix.

### Step-by-Step Workflow

**Step 1: PLAN** — Identify the schema change. Consult the data loss matrix. Determine if a data migration step is needed. Decide single migration vs. multi-step.

**Step 2: CREATE**
```bash
dotnet ef migrations add <MigrationName> --project <DataProject> --startup-project <StartupProject>
```
Review the generated `Up()`, `Down()`, and updated `ModelSnapshot.cs`.

**Step 3: REVIEW SQL**
```bash
dotnet ef migrations script --idempotent --project <DataProject> --startup-project <StartupProject>
```
Inspect for: data loss operations, blocking locks, missing index recreations, constraint naming.

**Step 4: TEST ROLLBACK**
```bash
# Apply the migration
dotnet ef database update --project <DataProject> --startup-project <StartupProject>

# Roll back to the previous migration
dotnet ef database update <PreviousMigrationName> --project <DataProject> --startup-project <StartupProject>

# Re-apply to verify forward path
dotnet ef database update --project <DataProject> --startup-project <StartupProject>
```

**Step 5: APPLY** — Development: `dotnet ef database update`. Staging/production: generate an idempotent script or migration bundle.

**Load on demand — `references/operating-guide.md`:** Domain Principles, Knowledge Base Lookups (run them before the first phase), AI Discipline Rules, Anti-Patterns, Error Recovery.

## State Block

```
<ef-migration-state>
step: [PLAN | CREATE | REVIEW_SQL | TEST_ROLLBACK | APPLY | ROLLBACK | ERROR_RECOVERY]
migration_name: [descriptive name, e.g., AddUserEmailIndex]
data_loss_risk: [none | low | high | critical]
rollback_ready: [true | false]
sql_reviewed: [true | false]
last_action: [what was just done]
next_action: [what should happen next]
blockers: [any issues preventing progress]
</ef-migration-state>
```

**Example:**

```
<ef-migration-state>
step: PLAN
migration_name: SplitCustomerAddress
data_loss_risk: high
rollback_ready: false
sql_reviewed: false
last_action: Identified need to extract Address columns into separate table
next_action: Create migration with data copy logic
blockers: Must verify all existing customers have address data
</ef-migration-state>
```

## Output Templates

```markdown
## Migration Review: [MigrationName]
**Risk**: [none|low|high|critical] | **SQL Reviewed**: [yes|no] | **Rollback Tested**: [yes|no]

| Operation | Table/Column | Risk | Notes |
|-----------|-------------|------|-------|
| [ADD/ALTER/DROP] | [target] | [level] | [details] |

**Findings**: [any issues from SQL review]
**Rollback Command**: `dotnet ef database update [PreviousMigration] ...`
```

Full report templates (Creation Report, SQL Review Report, Apply Report): `references/migration-commands.md`.

## Integration with Other Skills

- **`dotnet-vertical-slice`** -- When creating a new vertical slice feature, use this skill to manage schema changes required by the feature's data layer. The migration should be part of the slice implementation.
- **`legacy-migration-analyzer`** -- When analyzing legacy systems, use this skill to plan the EF Core schema replacing the legacy database. Coordinate between legacy analysis findings and the new migration plan.
