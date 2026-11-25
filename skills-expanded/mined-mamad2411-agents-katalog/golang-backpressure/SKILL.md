---
name: golang-backpressure
description: >
  Apply backpressure in Go services: bounded queues, worker pools, load shedding,
  timeouts, and client signals (429/503). Use for owned systems under load.
---

# Golang Backpressure

## Research grounding

Runbook for **backpressure and load shedding** in Go—preventing overload cascades
when producers outrun consumers. Skill id: `golang-backpressure`.

## Scope And Authorization

- **In scope:** services you own; load tests on authorized environments.
- **Out of scope:** DoS against systems you do not own.
- Prefer staging capacity tests with production-like limits.
- Pair with `retry-backoff-patterns`, `golang-abuse-prevention`, `code-quality-standards`.

## When To Use

- Go APIs/workers melting under traffic spikes.
- Designing queue consumers, `errgroup` pools, or fan-in pipelines.
- Protecting dependencies (DB, downstream HTTP) from stampeding herds.
- Focus tokens: **golang, backpressure**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Rate limit abuse controls | `golang-abuse-prevention` |
| Retry storms | `retry-backoff-patterns` |
| Active-passive failover | `golang-active-passive` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Mechanism | Go pattern |
| --- | --- |
| Bounded channel | `make(chan T, N)` + default drop/reject |
| Worker pool | fixed goroutines + job queue |
| Semaphore | `chan struct{}` or `golang.org/x/sync/semaphore` |
| Timeouts | `context.WithTimeout` on all outbound |
| Shed load | 503/429 with Retry-After |
| Queue depth metric | export length; alert |
| Pitfalls | Unbounded `go` per request; infinite retries |

## Workflow

### 1. Confirm scope and success criteria

1. Service, critical path, SLOs, authorization.
2. Success: under 2× load, p99 latency bounded; dependency not collapsed; errors are controlled 503s not total crash.
3. Define what to shed first (bulk/export vs checkout).

### 2. Inventory

1. Unbounded goroutines, channels, buffer sizes.
2. Downstream timeouts and pool sizes (DB `SetMaxOpenConns`).
3. Client retry behavior.

### 3. Baseline

1. Load test curve: RPS vs latency vs error.
2. Saturation point of DB/CPU.

### 4. Implement

```go
sem := semaphore.NewWeighted(100)

func (s *Server) Handle(w http.ResponseWriter, r *http.Request) {
	ctx := r.Context()
	if err := sem.Acquire(ctx, 1); err != nil {
		http.Error(w, "overloaded", http.StatusServiceUnavailable)
		return
	}
	defer sem.Release(1)
	// work with ctx deadlines
}
```

```go
// Non-blocking enqueue
select {
case q <- job:
default:
	return errShed // or drop oldest policy documented
}
```

1. Cap concurrency at each layer (handler, outbound client, DB).
2. Propagate context cancel when client gone.
3. Prefer fail-fast 503 over unbounded queue latency.
4. Bulkheads: separate pools for critical vs best-effort.
5. Align with client retries (Retry-After, jitter).

### 5. Verify with evidence

```bash
go test ./internal/load/... -count=1
go test ./... -race -count=1
# hey/k6 against staging with rising RPS
```

1. Prove queue never exceeds bound.
2. Prove dependency QPS capped.
3. Race detector clean on pool code.

### 6. Observe and harden

1. Metrics: in-flight, queue depth, shed count, dependency latency.
2. Alert on sustained shedding and on unbounded growth (should not happen).
3. Tune limits from evidence, not guesses.

### 7. Hand off

1. Document limits and shed policy in runbook.
2. Load test as release gate for capacity-sensitive services.
3. Apply `code-quality-standards`.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Queue | Bounded + metric | Infinite buffer “for safety” |
| Goroutines | Pool | Per-request unlimited `go` |
| Client | Timeout + jitter retry | Hammer on 503 without delay |
| Topic fidelity | Backpressure in Go | Generic go test only |

## Output Checklist

- [ ] Saturation baseline captured
- [ ] Bounds on concurrency/queues
- [ ] Shed responses defined
- [ ] Downstream pools/timeouts aligned
- [ ] Load test evidence
- [ ] Metrics/alerts
- [ ] `code-quality-standards` applied

## Rules

- Authorized load only.
- Prefer shedding to meltdown.
- Focus on `golang-backpressure`.
- Coordinate client retries to avoid amplify.
