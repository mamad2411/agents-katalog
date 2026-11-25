---
name: golang-baseline-behavior
description: >
  Establish runtime behavior baselines for Go services: traffic, errors, resource
  use, and auth patterns for detection and capacity. Use for owned systems under
  authorization.
---

# Golang Baseline Behavior

## Research grounding

Runbook for **behavioral baselining**—what “normal” looks like for Go services—
to support detection, capacity, and change validation. Skill id:
`golang-baseline-behavior`.

## Scope And Authorization

- **In scope:** telemetry for systems you own.
- **Out of scope:** profiling users beyond policy; unauthorized monitoring.
- Prefer privacy-preserving aggregates.
- Pair with `golang-anomaly-tuning`, `golang-blue-detect`, `golang-alerting`.

## When To Use

- Before enabling anomaly detection or UEBA-like signals on Go APIs.
- Capacity planning after measuring steady-state.
- Validating deploys against pre-change behavior.
- Focus tokens: **golang, baseline, behavior**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Secure config baseline | `golang-baseline` |
| Anomaly threshold tuning | `golang-anomaly-tuning` |
| Alert design | `golang-alerting` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Signal | Baseline idea |
| --- | --- |
| RPS by route template | Hour-of-week profile |
| Error ratio | Steady-state + deploy windows |
| Latency p50/p99 | Per route |
| Auth fail rate | Per endpoint |
| Outbound call rates | Per dependency |
| Resource | CPU/mem/goroutines/GC |
| Pitfalls | Baselining during outage; user-id cardinality |

## Workflow

### 1. Confirm scope and success criteria

1. Service, environment, authorization, purpose (detect vs capacity).
2. Success: documented normal ranges; stored profiles; used by detectors/alerts.
3. Privacy review if user-level.

### 2. Inventory telemetry

1. Metrics from `client_golang`; logs; traces sample rates.
2. Label quality (route templates, not raw IDs).
3. Gaps in instrumentation.

### 3. Collect baseline window

1. Choose stable period (2–4 weeks) excluding major incidents.
2. Capture seasonal patterns (batch windows—`golang-batch-window`).
3. Store profile artifacts (versioned).

### 4. Model normal

```go
// Export gauges that help baselining
// runtime.NumGoroutine(), memstats — via collectors
```

1. Compute percentiles and MAD per hour-of-week buckets.
2. Separate weekdays/weekends if needed.
3. Mark known jobs as expected spikes.
4. Document “normal deploy fingerprint” (brief error blip ok?).

### 5. Verify with evidence

1. Replay a past incident—would it deviate from baseline? (yes expected)
2. Quiet period—false deviation rate low.
3. After major feature launch, refresh baseline deliberately.

```bash
go test ./internal/metrics/... -count=1
```

### 6. Observe and harden

1. Feed profiles into `golang-anomaly-tuning`.
2. Alert if instrumentation missing (series disappear).
3. Quarterly re-baseline schedule.

### 7. Hand off

1. Profile location + owner.
2. How on-call should interpret deviations.
3. Link detection rules.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Window | Multi-week stable | Single quiet hour |
| Labels | Route templates | Per-user series |
| Refresh | After launches | Never update |
| Topic fidelity | Behavior baselines | Generic go test only |

## Output Checklist

- [ ] Purpose and privacy scope set
- [ ] Telemetry inventory complete
- [ ] Multi-week profiles stored
- [ ] Seasonality and batch jobs noted
- [ ] Incident/non-incident validation
- [ ] Refresh cadence set
- [ ] Hand-off to anomaly/alerts done

## Rules

- Aggregates over surveillance.
- Focus on `golang-baseline-behavior`.
- Authorized telemetry only.
- Do not baseline during ongoing incidents as “normal”.
