---
name: golang-backfill
description: >
  Run safe data backfills for Go services: batching, idempotency, throttling,
  dual-write, expand/contract schema, and rollback. Use for owned databases
  under change control.
---

# Golang Backfill

## Research grounding

Runbook for **safe backfill jobs** in Go—migrating or recomputing data at scale
without outages or corruption. Skill id: `golang-backfill`.

## Scope And Authorization

- **In scope:** datastores you own; approved change windows when needed.
- **Out of scope:** unauthorized bulk data modification.
- Prefer dry-run and staging clones first.
- Redact PII in job logs.
- Pair with `database-migration-safety`, `golang-backpressure`, `code-quality-standards`.

## When To Use

- Populating new columns/fields after expand schema.
- Rehashing tokens, recomputing aggregates, repairing denormalized data.
- Large multi-tenant updates via Go workers.
- Focus tokens: **golang, backfill**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Schema migration patterns | `database-migration-safety` |
| Queue load shedding | `golang-backpressure` |
| Archival to cold storage | `golang-archival` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Principle | Guidance |
| --- | --- |
| Expand/contract | Add nullable → backfill → enforce → remove old |
| Idempotent | Re-running batch must not double-apply |
| Keyset pagination | `WHERE id > $last ORDER BY id LIMIT n` |
| Throttle | Sleep/QPS limits; respect DB CPU |
| Observability | Progress metric, lag, error samples |
| Dual-write | New path writes both while backfill runs |
| Pitfalls | Full table lock; unbounded transactions; no resume |

## Workflow

### 1. Confirm scope and success criteria

1. Table/collection size, peak traffic, authorization, rollback plan.
2. Success: 100% eligible rows processed; invariants hold; no SLO burn.
3. Abort criteria (error rate, replication lag).

### 2. Inventory

1. Indexes supporting keyset scan; FKs/triggers side effects.
2. Downstream caches to invalidate.
3. Row estimate and average row size.

### 3. Baseline

1. Snapshot metrics: lag, CPU, slow queries.
2. Prove dry-run counts match estimate.

### 4. Implement Go backfill worker

```go
func Backfill(ctx context.Context, db *sql.DB, batch int) error {
	var lastID int64
	for {
		if err := ctx.Err(); err != nil {
			return err
		}
		rows, err := db.QueryContext(ctx,
			`SELECT id, payload FROM items WHERE id > $1 ORDER BY id ASC LIMIT $2`,
			lastID, batch)
		if err != nil {
			return err
		}
		n, maxID, err := processRows(ctx, db, rows) // idempotent update
		rows.Close()
		if err != nil {
			return err
		}
		if n == 0 {
			return nil
		}
		lastID = maxID
		// checkpoint lastID to durable store for resume
		time.Sleep(50 * time.Millisecond) // throttle
	}
}
```

1. Checkpoint progress externally; safe resume after crash.
2. Small batches (100–1000) tune under load.
3. Avoid long multi-statement transactions spanning huge sets.
4. Feature flag reads of new field until complete.
5. Rate limit per tenant if multi-tenant noisy neighbor risk.

### 5. Verify with evidence

```bash
go test ./internal/backfill/... -count=1
go test ./... -race -count=1

# Staging full run; prod canary tenant first
```

1. Invariant queries: null new_col count → 0 for eligible.
2. Sampling equality checks old vs new computation.
3. Replication lag stayed under threshold.

### 6. Observe and harden

1. Dashboard: rows/sec, errors, lag, ETA.
2. Auto-pause on lag/CPU alerts.
3. Post-backfill: add NOT NULL/constraints only after verified.

### 7. Hand off

1. Record runbook params (batch, throttle) that worked.
2. Remove temporary dual-write when contract phase done.
3. Apply `code-quality-standards`.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Resume | Checkpoint IDs | Start over from 0 always |
| Tx | Small batches | One tx for 50M rows |
| Prod | Canary tenant | All tenants at once unthrottled |
| Topic fidelity | Safe Go backfills | Generic go test only |

## Output Checklist

- [ ] Scope, abort criteria, authorization set
- [ ] Dry-run counts verified
- [ ] Idempotent batched worker with checkpoint
- [ ] Throttle and lag guards
- [ ] Invariant verification queries
- [ ] Expand/contract plan completed
- [ ] `code-quality-standards` applied

## Rules

- Prefer reversible expand/contract.
- Never backfill without dry-run on realistic volume.
- Focus on `golang-backfill`.
- Authorized data changes only.
