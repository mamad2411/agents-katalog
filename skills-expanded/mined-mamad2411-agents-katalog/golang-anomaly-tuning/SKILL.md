---
name: golang-anomaly-tuning
description: >
  Tune anomaly detection for Go service metrics and security signals: baselines,
  thresholds, seasonality, feedback loops, and evaluation. Use for owned
  detection systems under authorization.
---

# Golang Anomaly Tuning

## Research grounding

Runbook for **tuning anomaly detectors** that watch Go services (RED/USE metrics,
auth failures, payload sizes)—from simple z-score/rules to service-side detectors
implemented in Go. Skill id: `golang-anomaly-tuning`.

## Scope And Authorization

- **In scope:** owned telemetry and detection stacks.
- **Out of scope:** training models on data you cannot use; attacking detectors you do not own.
- Prefer shadow mode before enforce/page.
- Redact PII from training/eval sets.
- Pair with `golang-alerting` / `golang-alert-fatigue`.

## When To Use

- Detector pages constantly or misses real incidents.
- Adding adaptive baselines to Go-generated metrics.
- Evaluating precision/recall of anomaly labels with on-call feedback.
- Focus tokens: **golang, anomaly, tuning**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Static threshold alert design | `golang-alerting` |
| Noise reduction process | `golang-alert-fatigue` |
| Abuse rate limits | `golang-abuse-prevention` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Signals | RPS, latency p99, error ratio, queue lag, login failures, payload entropy |
| Baselines | Rolling median/MAD, EWMA, seasonal (hour-of-week) |
| Go libs | Custom stats, prometheus adaptive rules, third-party AD services |
| Modes | Shadow (log only) → ticket → page |
| Eval | Precision, recall, time-to-detect, alert volume |
| Pitfalls | Training on incidents; no seasonality; high-cardinality series |

## Workflow

### 1. Confirm scope and success criteria

1. Detector name, services, owner, authorization.
2. Success metrics: e.g. precision ≥P, volume ≤V pages/week, no missed SEV-1 in sample.
3. Define positive labels (postmortems, confirmed attacks).

### 2. Inventory

1. Input metrics/logs and their quality (gaps, resets).
2. Current algorithm and thresholds.
3. Feedback channel (alert acks, “wrong” button).

### 3. Baseline

1. Pull 2–8 weeks history; mark maintenance windows.
2. Compute current FP/FN on labeled set.
3. Snapshot config version.

### 4. Tune

```go
// Example: robust z-score with MAD (illustrative)
func IsAnomaly(x float64, window []float64, k float64) bool {
	med := median(window)
	mad := medianAbsDev(window, med)
	if mad == 0 {
		return false
	}
	z := math.Abs(x-med) / (1.4826 * mad)
	return z > k
}
```

1. Start with **shadow** scoring; log `score`, `threshold`, `decision`.
2. Separate detectors per class (latency ≠ security auth anomalies).
3. Encode seasonality: compare to same weekday/hour baseline.
4. Cap maximum page rate; escalate only if sustained.
5. Allowlists for known load tests with expiry.
6. For security anomalies: prefer precision to avoid cry-wolf (`golang-alert-fatigue`).

### 5. Verify with evidence

```bash
go test ./internal/anomaly/... -count=1
go test ./... -race -count=1

# Offline eval harness
# go run ./cmd/anomaly-eval --config v2.yaml --labels labels.json --metrics hist/
```

1. Report precision/recall vs previous config.
2. Replay known incident windows → must detect within SLO minutes.
3. Synthetic inject (staging) → detect; normal deploy → no page.

### 6. Observe and harden

1. Track score distributions; threshold drift.
2. Weekly FP review samples.
3. Retrain/refresh baselines after major product launches.

### 7. Hand off

1. Document algorithm, parameters, and owner.
2. Link runbooks for true positives.
3. Promote shadow → page only with sign-off.

## Parameter guide

| Param | Too low | Too high |
| --- | --- | --- |
| k (sensitivity) | Alert storms | Missed incidents |
| window | Noisy baseline | Slow to adapt |
| min duration | Flapping | Late detect |
| min volume | Division noise | Miss low-traffic attacks |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Rollout | Shadow then enforce | Page on day-1 untested |
| Labels | Incident-linked | “Whatever paged is true” |
| Seasonality | Hour-of-week | Single global mean |
| Security | High precision track | Same tuning as latency |
| Topic fidelity | Anomaly tuning for Go signals | Generic go test only |

## Output Checklist

- [ ] Scope and success metrics defined
- [ ] Historical baseline and labels prepared
- [ ] Shadow mode evaluation recorded
- [ ] Parameters updated with evidence
- [ ] Incident replay passes
- [ ] Volume and precision meet targets
- [ ] Owner and retrain schedule set
- [ ] `code-quality-standards` applied to detector code

## Rules

- Authorized telemetry only; redaction on.
- Prefer measurable eval over intuition-only thresholds.
- Focus on `golang-anomaly-tuning`.
- Do not disable critical static alerts solely in favor of unproven anomaly models.
