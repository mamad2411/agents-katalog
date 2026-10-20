---
name: migration
last_reviewed: 2026-09-06
group: Migrate and modernise
description: >-
  Map the debt, plan a strangler migration, and execute the zero-downtime cutover. Use when
  migrating legacy systems, databases, or frameworks safely.
---

# Migration

Executes complex system migrations — databases, cloud platforms, architectures, and frameworks — with zero-downtime strategies and rollback guarantees.

## Phased Workflow

### Phase 1: Migration Assessment & Risk Mapping
1. Inventory all affected systems, data stores, integrations, and downstream consumers.
2. Classify migration complexity: Simple (config change), Medium (schema change), Complex (architecture change).
3. Identify data migration volume, acceptable downtime window, and rollback requirements.

### Phase 2: Migration Strategy & Execution
1. **Database Migrations:** Use expand-contract pattern — add new columns/tables first, backfill, migrate reads, migrate writes, drop old.
2. **Cloud Migrations:** Implement lift-and-shift for stateless services, re-platform for stateful services, and re-architect only where ROI justifies.
3. **Monolith Decomposition:** Extract bounded contexts one at a time behind API gateways with strangler-fig routing.
4. **Framework Upgrades:** Pin dependency versions, run codemods, fix deprecation warnings progressively across releases.

### Phase 3: Validation & Cutover
1. Run parallel systems (shadow traffic) comparing old vs new outputs before cutover.
2. Execute canary rollout with automated rollback triggers on error rate spikes.
3. Validate data integrity post-migration with row-count reconciliation and checksum verification.

## Verification & Quality Checklist
- [ ] Rollback procedure documented and tested in staging before production cutover.
- [ ] Data reconciliation report shows zero discrepancies between source and target.
- [ ] All downstream consumers verified functional post-migration.
- [ ] Performance benchmarks (latency, throughput) meet or exceed pre-migration baselines.

## Anti-Patterns & Constraints
- NEVER perform destructive migrations (DROP TABLE, DROP COLUMN) before confirming all reads have migrated.
- NEVER cut over to a new system without a tested rollback path.
- NEVER migrate production data without a verified backup taken immediately before cutover.
