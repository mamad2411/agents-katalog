---
name: migration-plan
description: >
  Plan system migrations — scope assessment, dependency mapping, data migration
  strategy, rollback plan, testing strategy, cutover procedure, and communication plan.
  TRIGGER when: user says /migration-plan, asks to plan a migration, move to a new
  system, migrate a database, or transition between platforms.
argument-hint: "[source system, target system, or migration description]"
user-invocable: true
---

# Migration Plan

You are a senior infrastructure and platform engineer creating a comprehensive migration plan. Produce a detailed, actionable plan that minimizes risk and ensures a safe, reversible transition.

## Process

### Step 1: Scope Assessment

Before planning, determine:
- What is being migrated? (database, service, platform, cloud provider, framework, API)
- What is the source system and target system?
- Why is this migration happening? (EOL, cost, performance, compliance, consolidation)
- What is the timeline and are there hard deadlines?
- What is the blast radius if the migration fails?
- Who are the stakeholders and decision-makers?

**Migration Type Classification**

| Type | Examples | Risk Level | Typical Duration |
|------|----------|------------|-----------------|
| Database engine | MySQL to PostgreSQL, MongoDB to DynamoDB | High | 2-8 weeks |
| Cloud provider | AWS to GCP, on-prem to cloud | Very High | 2-6 months |
| Framework/language | Monolith to microservices, Python to Go | High | 1-6 months |
| API version | REST v1 to v2, REST to GraphQL | Medium | 2-6 weeks |
| Infrastructure | VMs to Kubernetes, self-hosted to managed | High | 2-8 weeks |
| Data store | Local files to S3, Redis to Memcached | Medium | 1-4 weeks |
| Service replacement | Build vs buy, vendor swap | Medium-High | 2-8 weeks |

### Step 2: Dependency Mapping

Identify everything connected to the system being migrated:

**Upstream Dependencies (things that depend on this system)**

| Dependency | Type | Impact If Broken | Owner | Contact |
|------------|------|-----------------|-------|---------|
| *List each service, job, or user workflow* | Service / Cron / UI / External | Critical / High / Medium / Low | Team name | Contact info |

**Downstream Dependencies (things this system depends on)**

| Dependency | Type | Migration Impact | Alternative Available |
|------------|------|-----------------|----------------------|
| *List each database, API, service, or config* | DB / API / Queue / File system | Must migrate together / Can point to new target / No change needed | Yes / No |

**Checklist:**
- [ ] All upstream consumers of the system have been identified
- [ ] All downstream dependencies have been cataloged
- [ ] Shared databases or schemas used by other systems are flagged
- [ ] Cron jobs, background workers, and async consumers are accounted for
- [ ] External integrations (webhooks, third-party APIs) are documented
- [ ] Network dependencies (DNS, firewall rules, VPN tunnels) are mapped
- [ ] Data flows (ETL pipelines, replication, backups) are documented

### Step 3: Data Migration Strategy

**Choose the migration pattern:**

| Pattern | Description | Downtime | Risk | Best For |
|---------|-------------|----------|------|----------|
| Big Bang | Migrate everything at once during a maintenance window | Hours | High | Small datasets, simple schemas |
| Trickle / Incremental | Migrate data in batches over time | Minimal | Medium | Large datasets, can tolerate eventual consistency |
| Dual Write | Write to both old and new systems during transition | Zero | Medium-High | Critical systems requiring zero downtime |
| CDC (Change Data Capture) | Stream changes from source to target in real time | Zero | Medium | Large datasets with continuous writes |
| Blue-Green | Run parallel environments, switch traffic at cutover | Seconds | Low-Medium | Stateless services, infrastructure migrations |
| Strangler Fig | Gradually route traffic from old to new system | Zero | Low | Monolith decomposition, API migrations |

**Data migration checklist:**
- [ ] Source data has been profiled (row counts, data types, null rates, encoding)
- [ ] Schema mapping document created (source field -> target field, with transformations)
- [ ] Data validation rules defined (row counts, checksums, business rule assertions)
- [ ] Migration scripts are idempotent (safe to re-run)
- [ ] Large tables have a chunked/batched migration strategy
- [ ] Sequences, auto-increments, and generated IDs are handled
- [ ] Binary data, BLOBs, and file references are accounted for
- [ ] Timezone and encoding differences are resolved (UTF-8, UTC)
- [ ] Historical data retention policy is defined (migrate all vs. recent only)
- [ ] PII and sensitive data handling complies with regulations during transfer

### Step 4: Rollback Plan

Every migration must have a documented, tested rollback procedure.

**Rollback Decision Matrix**

| Signal | Severity | Action |
|--------|----------|--------|
| Data corruption detected | Critical | Immediate rollback, invoke incident response |
| Error rate > 5x baseline | Critical | Rollback within 15 minutes |
| Latency > 3x baseline | High | Investigate for 15 min, rollback if not resolved |
| Non-critical feature broken | Medium | Hotfix forward if possible, rollback if not |
| Cosmetic issues only | Low | Fix forward, no rollback needed |

**Rollback checklist:**
- [ ] Rollback procedure is documented step-by-step
- [ ] Rollback has been rehearsed in staging
- [ ] Data written to the new system during migration can be reverse-synced
- [ ] DNS/routing changes can be reverted within minutes
- [ ] Database schema rollback (down migrations) are tested
- [ ] Feature flags can disable new-system code paths instantly
- [ ] Rollback owner and escalation path are assigned
- [ ] Maximum time-to-rollback is defined and achievable
- [ ] Communication template for rollback announcement is prepared

### Step 5: Testing Strategy

**Testing phases:**

| Phase | Environment | What to Test | Success Criteria |
|-------|-------------|-------------|-----------------|
| Unit/Integration | CI | Migration scripts, schema compatibility | All tests pass |
| Dry Run | Staging | Full migration against production-like data | Data validation passes, no errors |
| Shadow Traffic | Production (read-only) | New system handles real queries correctly | Response parity > 99.9% |
| Canary | Production (partial) | Small percentage of real traffic to new system | Error rate within baseline |
| Full Cutover | Production | All traffic on new system | All SLOs met for 24-48 hours |

**Data validation tests:**
- [ ] Row count comparison between source and target
- [ ] Checksum/hash validation on critical tables
- [ ] Spot-check queries returning identical results on both systems
- [ ] Boundary value testing (min/max IDs, dates, empty strings, nulls)
- [ ] Foreign key and referential integrity verification
- [ ] Performance benchmarks (query latency, throughput) match or exceed source
- [ ] Application smoke tests pass against the new system
- [ ] End-to-end user workflows validated on staging

### Step 6: Cutover Procedure

**Pre-Cutover (T-24 hours)**
- [ ] Final dry run completed successfully in staging
- [ ] All stakeholders notified of maintenance window
- [ ] On-call team briefed and rollback procedure reviewed
- [ ] Monitoring dashboards open and alerting thresholds set
- [ ] External status page updated (if applicable)
- [ ] Runbook printed/accessible offline in case of system access issues

**Cutover Execution**
1. **Freeze** — Stop writes to the source system (maintenance mode or read-only)
2. **Final Sync** — Run the last incremental migration / CDC catch-up
3. **Validate** — Execute data validation suite, confirm row counts and checksums
4. **Switch** — Update connection strings, DNS, routing, or feature flags
5. **Verify** — Run smoke tests against production, confirm traffic is flowing
6. **Monitor** — Watch error rates, latency, and business metrics for anomalies
7. **Announce** — Notify stakeholders that cutover is complete

**Post-Cutover (T+24 to T+72 hours)**
- [ ] Monitor all SLOs continuously for 48-72 hours
- [ ] Keep the old system running in read-only mode as a safety net
- [ ] Verify backups are running against the new system
- [ ] Confirm all cron jobs and async workers are functioning
- [ ] Collect feedback from downstream consumers
- [ ] Document any issues encountered and resolutions applied

### Step 7: Communication Plan

| When | Audience | Channel | Message |
|------|----------|---------|---------|
| T-2 weeks | Engineering teams | Email + Slack | Migration overview, timeline, expected impact |
| T-1 week | All stakeholders | Email | Detailed schedule, maintenance window, contact info |
| T-1 day | On-call + leads | Slack war room | Final readiness check, runbook review |
| T-0 (start) | All stakeholders | Status page + Slack | Migration started, expected duration |
| T-0 (complete) | All stakeholders | Status page + Slack + Email | Migration complete, what to watch for |
| T+1 day | Engineering teams | Slack | Post-migration health summary |
| T+1 week | All stakeholders | Email | Final migration report, old system decommission date |

## Output Format

Present the migration plan as:

```
## Migration Plan: {Source} -> {Target}

### Summary
- Migration type: [type]
- Risk level: [Low / Medium / High / Very High]
- Estimated duration: [timeframe]
- Maintenance window: [date/time or "zero downtime"]
- Rollback time: [minutes/hours]

### Scope
- What is migrating
- What is NOT migrating (explicit exclusions)

### Dependencies
- Upstream and downstream dependency tables

### Data Migration
- Pattern chosen and rationale
- Schema mapping summary
- Validation approach

### Rollback Plan
- Trigger criteria
- Step-by-step procedure
- Responsible parties

### Testing Plan
- Phase-by-phase test plan with exit criteria

### Cutover Procedure
- Numbered step-by-step with time estimates

### Communication Plan
- Timeline with audiences and channels

### Open Risks
- Known risks with mitigation strategies
```

## Quality Checklist

Before delivering the migration plan, verify:

- [ ] Every dependency (upstream and downstream) has been identified and mapped
- [ ] Data migration strategy handles the full dataset size within the time window
- [ ] Rollback procedure is documented, tested, and achievable within the stated time
- [ ] Testing covers data integrity, performance, and end-to-end user workflows
- [ ] Cutover procedure has clear steps with owners and time estimates
- [ ] Communication plan covers all stakeholder groups at all phases
- [ ] Monitoring is in place to detect issues within minutes of cutover
- [ ] Old system decommission timeline is defined (but not rushed)
- [ ] Compliance and security requirements are met during data transfer
- [ ] The plan has been reviewed by at least one person from each affected team

## Edge Cases

Consider and address these scenarios:

- **Data volume exceeds migration window** — If the dataset is too large for a single maintenance window, use incremental/CDC migration to pre-sync most data, then only migrate the delta during cutover.
- **Schema incompatibility** — When source and target have fundamentally different data models, build an explicit transformation layer. Document every mapping and run validation on transformed data.
- **Circular dependencies** — If system A depends on system B which depends on system A, plan a phased migration with temporary compatibility shims or adapters.
- **Third-party rate limits** — When migrating data through external APIs, account for rate limits in your time estimates. Build in retry logic with exponential backoff.
- **Stateful connections** — Long-lived WebSocket connections, streaming subscriptions, or sticky sessions must be gracefully drained before cutover.
- **Timezone and locale differences** — When migrating between systems in different regions or with different default timezones, ensure all timestamps are normalized to UTC.
- **Partial migration failure** — Design migration batches so that a failure midway leaves the system in a consistent state. Use transactions or idempotent operations.
- **Compliance and audit trail** — Some regulated industries require documentation of data lineage during migration. Log every record transformation for audit purposes.
- **DNS propagation delay** — If cutover involves DNS changes, account for TTL propagation time (reduce TTL well before migration day). Consider using application-level routing instead.
- **Hidden consumers** — Legacy scripts, cron jobs, or undocumented integrations may break silently. Announce the migration broadly and monitor the old system for unexpected traffic after cutover.
