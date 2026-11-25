---
name: migration-platform
version: 1.0.0
min_mindforge_version: 10.7.0
status: stable
triggers: migration platform design, schema migration orchestration, data migration tooling, zero-downtime migration automation, migration validation, migration rollback platform, database migration service, migration state machine, migration dry-run, migration scheduling, migration dependency graph, migration progress tracking
compose: migration-strategies
---

# Skill — Migration Platform

## When this skill activates

This skill activates when the user is designing or implementing a migration platform. This includes schema migration orchestration, data migration tooling, zero-downtime migration automation, migration validation, rollback capabilities, database migration services, migration state machines, dry-run testing, migration scheduling, dependency graph management, and progress tracking.

## Mandatory actions when this skill is active

### Before writing any code

1. Inventory all systems requiring migration: databases, APIs, services, data pipelines, infrastructure. Quantify: data volume, traffic volume, number of tables/services.
2. Define migration success criteria: zero downtime, data consistency, performance impact under 10%, rollback time under 5 minutes.
3. Identify dependencies: which services depend on the system being migrated. Build dependency graph to determine migration order.
4. Assess risk: classify migrations by risk (low, medium, high, critical). High-risk migrations require dry-run, shadow traffic, and manual approval gates.
5. Establish rollback strategy: forward-compatible schema changes, dual-write period, automated rollback triggers (error rate > 5%).

### During implementation

- **Migration State Machine:** Define states: pending → dry-run → scheduled → in-progress → validating → completed / failed / rolled-back. Track state per migration in database. Expose state via API and dashboard.
- **Schema Migration Orchestration:** Use tools like Liquibase, Flyway, or Alembic. Migrations should be: idempotent, forward-compatible, backward-compatible during rollout. Apply migrations in stages: additive changes → data migration → breaking changes.
- **Zero-Downtime Patterns:**
  - **Expand-Contract:** Add new column/table (expand), dual-write to old and new (transition), switch reads to new (cutover), remove old (contract).
  - **Blue-Green:** Deploy new version alongside old, switch traffic atomically, keep old version for quick rollback.
  - **Shadow Traffic:** Mirror production traffic to new system, compare results, cutover when validation passes.
- **Data Migration Tooling:** Build ETL pipelines for bulk data migration. Include: checkpointing (resume from failure), batching (avoid overwhelming target), validation (row counts, checksums), rate limiting (avoid impacting production). Migrations should be resumable and idempotent.
- **Migration Validation:** Automated validation checks: data integrity (row counts, checksums), functional correctness (run test suite against new system), performance (latency, throughput within 10% of baseline). Fail migration if any check fails.
- **Migration Rollback:** Automate rollback when error rate exceeds threshold (5% or 1% for critical systems). Rollback should: revert traffic to old system, preserve data written during migration (dual-write), alert on-call team. Rollback time target: under 5 minutes.
- **Dry-Run Testing:** Run migrations in staging environment first. Use production-like data volume and traffic patterns. Validate performance, correctness, and rollback. Dry-run should be mandatory for high-risk migrations.
- **Migration Scheduling:** Schedule migrations during low-traffic windows. Provide manual approval gates for critical migrations. Include: notification to stakeholders, runbook link, on-call team assignment.
- **Dependency Graph Management:** Build migration dependency graph (service A depends on service B). Enforce migration order: migrate dependencies first, then dependents. Detect circular dependencies and fail early.
- **Progress Tracking:** Real-time dashboard showing: migration state, percentage complete, error rate, performance metrics, estimated time remaining. Include logs and alerts for anomalies.

### After implementation

- Verify migration state machine tracks all migrations with state transitions logged.
- Confirm schema migrations are idempotent, forward-compatible, and backward-compatible during rollout.
- Validate zero-downtime patterns (expand-contract, blue-green, shadow traffic) are implemented.
- Ensure data migration tooling includes checkpointing, batching, validation, and rate limiting.
- Check that migration rollback is automated with under 5-minute rollback time.

## Self-check before task completion

- [ ] Migration state machine tracks pending, in-progress, completed, failed, rolled-back states.
- [ ] Schema migrations are idempotent, forward-compatible, and backward-compatible.
- [ ] Zero-downtime patterns (expand-contract, blue-green, shadow traffic) are implemented.
- [ ] Data migration tooling is resumable, idempotent, and includes validation.
- [ ] Migration validation checks data integrity, functional correctness, and performance.
- [ ] Migration rollback is automated and completes in under 5 minutes.
- [ ] Dry-run testing is mandatory for high-risk migrations in production-like staging.
- [ ] Migration scheduling supports manual approval gates and stakeholder notifications.
- [ ] Dependency graph enforces migration order and detects circular dependencies.
- [ ] Progress tracking dashboard shows real-time state, percentage complete, and error rate.
