---
name: golang-alert-fatigue
description: >
  Reduce alert fatigue for Go services: measure noise, dedupe, multi-window
  thresholds, symptom-based pages, and instrumentation fixes. Use for owned
  on-call systems under authorization.
---

# Golang Alert Fatigue

## Research grounding

Runbook for **cutting noisy pages** while keeping signal—focused on services
instrumented in Go (Prometheus metrics, structured logs) and Alertmanager-style
stacks. Skill id: `golang-alert-fatigue`.

## Scope And Authorization

- **In scope:** alerting you own; authorized observability changes.
- **Out of scope:** disabling another team’s critical detections without agreement.
- Prefer staging rule evaluation; production mute needs ticket + expiry.
- Redact customer payloads from alert examples.
- Pair metric code with `code-quality-standards`.

## When To Use

- On-call reports flapping alerts, duplicate pages, or “ignore this one” culture.
- Go services emit high-cardinality metrics or error logs turned into pages.
- After incidents where real signal was missed due to noise.
- Focus tokens: **golang, alert, fatigue**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Designing new alerts from scratch | `golang-alerting` |
| Anomaly model tuning | `golang-anomaly-tuning` |
| Observability instrumentation standards | `observability-metrics-tracing` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Symptom | Typical fix |
| --- | --- |
| Flapping | `for:` duration, hysteresis, longer window |
| Duplicate pages | group_by, inhibit rules, dedupe keys |
| Too sensitive | Raise threshold using SLO error budget |
| Useless page | Convert to ticket severity; page only on user impact |
| Cardinality storm | Fix Go label sets (no user IDs in metric labels) |
| Log-based pages | Sample/aggregate; prefer metrics |
| Missing owner | Drop or assign; no orphan alerts |

## Workflow

### 1. Confirm scope and success criteria

1. Team, services, paging vendor, authorization.
2. Success: e.g. pages/week down X% with zero missed SEV-1; MTTA stable/improved.
3. Freeze: do not silence without substitute coverage.

### 2. Inventory noisy alerts

1. Export last 30–90 days of pages; rank by volume and ack-without-action rate.
2. Classify: flapping, duplicate, expected batch jobs, true actionable.
3. Map each to Go metric/log source.

### 3. Baseline

1. Pages per on-call shift; % auto-resolved; false positive samples.
2. Snapshot Alertmanager config / Grafana rules hashes.

### 4. Reduce fatigue (config + Go code)

**Alertmanager-style patterns:**

```yaml
# group similar firing alerts
route:
  group_by: ['alertname', 'service', 'severity']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
inhibit_rules:
  - source_matchers: [severity="critical"]
    target_matchers: [severity="warning"]
    equal: ['service']
```

**Go instrumentation fixes:**

```go
// Bad: unbounded labels → noisy useless series
// prom.WithLabelValues(userID, path)

// Good: bounded route template + status class
httpDuration.WithLabelValues(routeTemplate, statusClass(code)).Observe(sec)
```

1. Prefer **symptom** alerts (latency SLO burn, error rate, saturation) over every cause.
2. Add `for: 5m` (or burn-rate multi-window) before paging.
3. Batch jobs: silence windows or cron-aware alerts—not permanent mute.
4. Fix root cause in code (retry storms, missing backoff) not only thresholds.
5. Every page needs runbook link; if none, ticket not page until written.

### 5. Verify with evidence

```bash
promtool check rules rules/*.yml
go test ./internal/metrics/... -count=1
go test ./... -count=1
```

1. Replay historical metrics against new rules if tooling allows.
2. Track 2 weeks post-change: page volume + incident detection lag.
3. Confirm critical path still pages with synthetic fail in staging.

### 6. Observe and harden

1. Meta-metrics: pages per service, ack time, reopen rate.
2. Quarterly “alert garbage collection” review.
3. Budget: max N paging alerts per service; rest are ticket/asynchronous.

### 7. Hand off

1. Document changes and expected volume delta.
2. Train on-call on new severity meanings.
3. Link `golang-alerting` for net-new alert design.

## Decision table

| Signal | Page? | Alternative |
| --- | --- | --- |
| User-facing SLO burn | Yes | — |
| Single replica restart | No | Ticket / warning |
| Known daily batch spike | No | Silence window |
| Disk 70% | Maybe | Trend + 90% page |
| Trace of one 500 | No | Metric aggregate |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Mute | Temporary with expiry | Permanent null route |
| Labels | Low cardinality | user_id/email labels |
| Ownership | Team + runbook | Orphan alert |
| Tuning | Data-driven thresholds | Raise until silent, miss outages |
| Topic fidelity | Fatigue reduction tactics | Generic go test only |

## Output Checklist

- [ ] Page volume baseline captured
- [ ] Top noisy alerts classified
- [ ] Grouping/inhibition/thresholds adjusted
- [ ] Go metric cardinality issues fixed
- [ ] Runbooks present for remaining pages
- [ ] Synthetic/staging proof critical still fires
- [ ] Post-change volume measured
- [ ] `code-quality-standards` applied

## Rules

- Do not “fix noise” by dropping coverage without owner agreement.
- Prefer symptom + SLO burn rates.
- Focus on `golang-alert-fatigue`; net-new design → `golang-alerting`.
- Redact PII from alert payloads and tickets.
