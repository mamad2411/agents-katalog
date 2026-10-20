---
name: data-retention-job-design
description: >
  Design lawful, safe data retention and deletion jobs for owned systems: policy
  windows, batched deletes, soft vs hard delete, audit logs, legal hold, and
  observability. Use when implementing GDPR/CCPA-style retention, log expiry, or
  purging PII — coordinate legal/compliance; not for destroying evidence under hold.
---

# Data Retention Job Design

## Scope And Authorization

- **In scope:** Data stores and jobs for systems you operate with policy approval.
- **Out of scope:** Mass deletion without legal review; purging data under litigation/regulatory hold; attacking others' backups.
- Prefer dry-run and staged deletes; irreversible hard deletes need dual control for high-impact datasets.
- Pair with `cron-distributed-scheduler-safety`, privacy counsel, and `code-quality-standards`.

## When To Use

- Implementing retention for user PII, logs, analytics events, or uploads.
- “Delete my account” pipelines spanning multiple stores.
- Cost control via TTL on cold data with compliance alignment.
- Fixing unsafe `DELETE FROM table` without batches.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Distributed cron locks | `cron-distributed-scheduler-safety` |
| DB migrations | `database-migration-safety` |
| Backup/restore | backup skills |
| Secrets hygiene | `secrets-management-hygiene` |
| Implementation quality baseline | `code-quality-standards` |

## Policy inputs (must resolve before code)

| Question | Why |
| --- | --- |
| Legal basis / retention schedule | Defines windows |
| Legal hold process | Suppresses purge |
| Soft vs hard delete | Recovery and FK design |
| Derived data (search, warehouse, backups) | Full erasure path |
| User-driven vs time-driven | Different triggers |
| Audit requirements | Who deleted what when |

## Workflow

### 1. Confirm policy and success criteria

1. Written retention schedule per data class.
2. Success: jobs meet windows; holds respected; no table scans locking prod; metrics prove volume deleted; restore tested for accidental over-delete process.

### 2. Map data locations

```text
Primary DB → replicas → cache → object storage → search index → warehouse → backups/logs
```

Each needs an owner and deletion method (API, SQL, lifecycle rule).

### 3. Choose deletion mechanics

| Pattern | Use |
| --- | --- |
| Soft delete + purge job | Account deletion UX with grace period |
| Time-based batch hard delete | Logs/events past TTL |
| Storage lifecycle (S3) | Objects with prefix/date |
| Anonymization | Keep analytics without PII |
| Crypto-shredding | Destroy key for encrypted blobs |

```sql
-- Batched purge sketch
WITH victims AS (
  SELECT id FROM events
  WHERE created_at < now() - interval '90 days'
    AND legal_hold = false
  ORDER BY id
  LIMIT 1000
)
DELETE FROM events e
USING victims v
WHERE e.id = v.id;
```

### 4. Job safety controls

1. **Batch size** + sleep to protect primary.
2. **Distributed lock** so only one purger runs (`cron-distributed-scheduler-safety`).
3. **Dry-run mode** counts candidates.
4. **Max runtime** / deadline per invoke.
5. **Legal hold** table join or flag — never purge held ids.
6. **Idempotent** re-runs.

### 5. Account erasure flow

```text
Request → verify identity → soft-delete + queue → erase stores → verify → confirm to user → audit
```

1. Async workers; partial failure retries with state machine.
2. Downstream: billing, email ESP, CRM — tracked checklists.
3. Backups: document residual retention (often cannot surgically delete immediately).

### 6. Observe

| Metric | Purpose |
| --- | --- |
| `retention_candidates` | Backlog |
| `retention_deleted` | Throughput |
| `retention_errors` | Failures |
| `oldest_eligible_age` | SLA lag |
| Hold count | Suppressions |

Alert if eligible data older than policy + grace.

### 7. Verify

```bash
# Dry-run counts in staging
# Delete sample synthetic user end-to-end
# Confirm search/cache miss after purge
# Prove legal hold row skipped
```

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Delete | Batched + locked | Unbounded single transaction |
| Hold | Explicit suppress | No hold concept |
| Erasure | Multi-store checklist | DB row only |
| Float policy | Counsel-approved schedule | Engineer-invented 30 days |
| Backups | Document residual | Claim instant global erase |

## Output Checklist

- [ ] Policy schedule documented per class
- [ ] Data store map complete
- [ ] Hold mechanism implemented
- [ ] Batched job with lock and dry-run
- [ ] Multi-store erasure path for accounts
- [ ] Metrics and lag alerts
- [ ] Staging e2e verification
- [ ] Backup residual disclosure written
- [ ] Dual control for high-risk hard deletes
- [ ] Residual risks accepted by owner

## Rules

- Never purge through legal holds.
- Compliance owns schedule; engineering owns safe mechanics.
- Focus on **retention/deletion job design**.
