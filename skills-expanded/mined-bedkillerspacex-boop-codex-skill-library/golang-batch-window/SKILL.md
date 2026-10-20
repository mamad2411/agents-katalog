---
name: golang-batch-window
description: >
  Design batch processing windows for Go jobs: schedules, capacity, conflict
  avoidance with online traffic, idempotency, and observability. Use for owned
  batch systems under change control.
---

# Golang Batch Window

## Research grounding

Runbook for **batch windows**—when and how Go batch/ETL/report jobs safely run
relative to peak traffic and maintenance. Skill id: `golang-batch-window`.

## Scope And Authorization

- **In scope:** jobs and data you own.
- **Out of scope:** overloading shared infrastructure without owners’ consent.
- Prefer feature flags and kill switches.
- Pair with `golang-backpressure`, `golang-backfill`, `golang-alerting`.

## When To Use

- Scheduling heavy Go workers (billing, reconciliation, ML feature build).
- Avoiding batch vs online interference.
- Defining catch-up behavior after missed windows.
- Focus tokens: **golang, batch, window**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Backfill algorithms | `golang-backfill` |
| Load shedding inside online path | `golang-backpressure` |
| BCP overall | `golang-bcp-notes` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concern | Guidance |
| --- | --- |
| Window | Off-peak hours + TZ documented; respect regional peaks |
| Duration cap | Hard deadline; stop/resume with checkpoint |
| Capacity | Separate queues/pools from online (`golang-backpressure`) |
| Idempotency | Safe re-run next window |
| Calendar | Skip holidays if business requires; or plan catch-up |
| Conflicts | Schema migrations vs batch; freeze policies |
| Pitfalls | Infinite catch-up stampede; no owner oncall |

## Workflow

### 1. Confirm scope and success criteria

1. Job purpose, SLA (must finish by 06:00), authorization.
2. Success: finishes inside window 95% days; online SLO unaffected.
3. Missed-window policy.

### 2. Inventory

1. Job graph dependencies (A before B).
2. Shared DB/CPU with online Go APIs.
3. Current schedule (cron/k8s CronJob/Airflow).

### 3. Baseline

1. Runtime histogram last 30 days.
2. Online error/latency during batch.

### 4. Design window

```yaml
# k8s CronJob sketch — off-peak UTC
schedule: "0 2 * * *"
concurrencyPolicy: Forbid
successfulJobsHistoryLimit: 3
```

```go
func Run(ctx context.Context) error {
	deadline, ok := ctx.Deadline()
	// or set internal stop time = windowEnd - buffer
	for hasWork() {
		if time.Now().After(stopBy) {
			return errWindowExceeded // checkpoint saved
		}
		if err := processBatch(ctx); err != nil {
			return err
		}
	}
	return nil
}
```

1. `concurrencyPolicy: Forbid` or distributed lock to prevent overlap.
2. Buffer time before online peak for slowdowns.
3. Resource quotas: CPU/mem limits; DB pool separate user.
4. Catch-up: limited parallelism; never unlimited historical replay without cap.
5. Emit `batch_window_success`, `batch_duration`, `batch_lag_seconds`.

### 5. Verify with evidence

```bash
go test ./internal/batch/... -count=1
# staging: run job; watch online SLOs
```

1. Kill mid-window → resume next run idempotent.
2. Overlap attempt → second instance exits cleanly.
3. Synthetic load: online p99 within budget.

### 6. Observe and harden

1. Alert if job not successful by window end.
2. Alert if duration trend exceeds window.
3. Review after product launches that shift traffic patterns.

### 7. Hand off

1. Calendar of windows; owner; kill switch.
2. Runbook for missed SLA (manual catch-up steps).
3. Apply `code-quality-standards`.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Schedule | Documented TZ + forbid overlap | Every 5 min heavy full scan |
| Stop | Checkpoint + deadline | Run into peak forever |
| Online | Separate pools | Starve API DB connections |
| Topic fidelity | Batch windows for Go jobs | Generic go test only |

## Output Checklist

- [ ] SLA and window defined
- [ ] Overlap prevention
- [ ] Checkpoint/idempotency
- [ ] Capacity isolation from online
- [ ] Metrics/alerts for miss/overrun
- [ ] Catch-up policy documented
- [ ] `code-quality-standards` applied

## Rules

- Online user traffic wins by default.
- Focus on `golang-batch-window`.
- Authorized job changes only.
- Always have a kill switch.
