---
name: golang-active-passive
description: >
  Design and operate active-passive failover for Go services: leader election,
  health/readiness, promotion, split-brain avoidance, and drills. Use for owned
  systems under authorization.
---

# Golang Active Passive

## Research grounding

Runbook for **active-passive** high availability with Go processes: one primary
serves writes (or all traffic); standby is warm/cold and takes over on failure.
Covers coordination, health, and application patterns. Skill id:
`golang-active-passive`.

## Scope And Authorization

- **In scope:** owned clusters, labs, authorized DR exercises.
- **Out of scope:** inducing failover on systems you do not operate.
- Prefer staging drills; production failovers need change windows and comms.
- Redact connection strings and credentials from notes.
- Pair code with `code-quality-standards`.

## When To Use

- Single-writer components (queue consumers, schedulers, stateful workers) in Go.
- Implementing leader election (Kubernetes lease, etcd, Consul, DB advisory lock).
- Measuring RTO/RPO for passive promotion.
- Focus tokens: **golang, active, passive**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Blue/green deploy traffic shift | `golang-blue-green` |
| Backpressure under load | `golang-backpressure` |
| Generic alerting | `golang-alerting` |
| Backup immutability | `golang-backup-immutable` |
| Multi-active conflict design | CRDT/multi-primary architecture skill |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Roles | Active (primary), passive (hot/warm/cold standby) |
| Coordination | K8s Lease/endpoints, etcd election, Redis Redlock (careful), SQL `pg_try_advisory_lock` |
| Go libs | `client-go` leaderelection, `etcd/client/v3/concurrency`, custom heartbeat |
| Health | Liveness ≠ readiness; passive may be live but not ready for writes |
| Data | Replication lag limits; promote only if lag < RPO |
| Split-brain | Fencing tokens, single-writer leases with TTL, STONITH/disk fence where needed |
| Pitfalls | Two actives after network partition; long GC pauses missing heartbeats |

## Workflow

### 1. Confirm scope and success criteria

1. Record service, data stores, RTO/RPO, environments, authorization.
2. Success: automatic or runbooked promotion within RTO; no dual-writer; drill evidence.
3. Document blast radius (which clients see errors during cutover).

### 2. Inventory

1. Classify component: stateless (prefer active-active) vs needs single writer.
2. Map state: DB primary, object store, in-memory only (lose on failover?).
3. Existing locks/elections and their TTLs.
4. Client retry/idempotency posture.

### 3. Baseline

1. Measure failover time today (manual or automatic).
2. Capture lag metrics, lease TTL, and error budget impact.
3. Version election config before change.

### 4. Implement Go active-passive

**Leader loop sketch (conceptual):**

```go
// OnStartedLeading: become active — start writers/consumers
// OnStoppedLeading: become passive — stop writers, drain, demote readiness
cfg := leaderelection.LeaderElectionConfig{
	Lock:          lock, // e.g. resourcelock.LeaseLock
	LeaseDuration: 15 * time.Second,
	RenewDeadline: 10 * time.Second,
	RetryPeriod:   2 * time.Second,
	Callbacks: leaderelection.LeaderCallbacks{
		OnStartedLeading: func(ctx context.Context) {
			setRole(RoleActive)
			startWriters(ctx)
		},
		OnStoppedLeading: func() {
			stopWriters()
			setRole(RolePassive)
		},
	},
}
```

1. Gate **write paths** on `role == active`; passive serves health or read-only if safe.
2. Use fencing: include lease generation / epoch in write requests so old primary is rejected.
3. On demotion: cancel context, flush, close producer connections, flip readiness to not-ready.
4. Configure clients with retries and idempotency keys for in-flight requests.
5. Passive warm: pre-open DB pools, warm caches read-only; avoid dual consumers on same queue without competing consumers pattern.

### 5. Verify with evidence

```bash
go test ./internal/ha/... -count=1
go test ./... -race -count=1
go vet ./...
staticcheck ./...
```

Drill checklist:

1. Kill active pod/process → passive acquires lease within TTL + RetryPeriod budget.
2. Network partition simulation (lab) → at most one writer (or both refuse writes).
3. Replication lag > RPO → promotion blocked or alerted.
4. Metrics show `ha_role{role="active"}` == 1 across cluster.

### 6. Observe and harden

1. Metrics: `leader_is_local`, `leader_transitions_total`, `replication_lag_seconds`.
2. Alert: no leader for >T; two actives detected; lag high; lease renew failures.
3. Tune LeaseDuration vs GC/STW; avoid too-aggressive TTLs on busy nodes.
4. Run scheduled failover drills; record RTO evidence.

### 7. Hand off

1. Runbook: manual promote/demote, force-release lease (dangerous), rollback.
2. On-call knows fencing and dual-writer symptoms.
3. Apply `code-quality-standards`; schedule next drill.

## Active vs passive matrix

| Mode | Active | Passive |
| --- | --- | --- |
| Hot | Serves traffic | Replicates, almost ready |
| Warm | Serves traffic | Process up, connections warm |
| Cold | Serves traffic | Started on demand (higher RTO) |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Election | Lease + fencing epoch | “Whoever starts first” |
| Writes | Guarded by role + epoch | Both nodes consume same queue |
| Health | Readiness false when passive | Readiness true always |
| Drills | Scheduled with evidence | Untested for years |
| Topic fidelity | Leader election + failover in Go | Only generic go test |

## Output Checklist

- [ ] RTO/RPO and single-writer need confirmed
- [ ] Coordination mechanism chosen and TTLs documented
- [ ] Go role gating and demotion drain implemented
- [ ] Fencing/epoch strategy defined
- [ ] Failover drill executed with timings
- [ ] Split-brain test or reasoned residual risk
- [ ] Metrics/alerts for leadership and lag
- [ ] Runbook and next drill date
- [ ] `code-quality-standards` applied

## Rules

- Authorized drills only; never random production failovers without process.
- Prefer reversible config; document force-unlock risks.
- Focus on `golang-active-passive`; route blue/green and pure backup skills nearby.
- Never paste live credentials or lease tokens into notes.
