---
name: golang-bcp-notes
description: >
  Engineering notes for business continuity of Go services: critical paths,
  RTO/RPO, dependency maps, failover drills, and comms. Use for owned systems
  under authorization.
---

# Golang BCP Notes

## Research grounding

Runbook for **business continuity planning (BCP)** from an engineering angle for
Go service portfolios—keeping critical functions available through disruptions.
Skill id: `golang-bcp-notes`.

## Scope And Authorization

- **In scope:** systems and processes you own; authorized DR drills.
- **Out of scope:** declaring disasters for others’ systems; unauthorized failovers.
- Coordinate with business BCP owners; this skill is engineering execution.
- Pair with `golang-active-passive`, `golang-blue-green`, `golang-backup-verify`.

## When To Use

- Writing technical BCP annex for Go services.
- Mapping tier-0 journeys and engineering RTO/RPO.
- Planning multi-region or degraded-mode behavior.
- Focus tokens: **golang, bcp, notes**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Backup restore proof | `golang-backup-verify` |
| Failover HA design | `golang-active-passive` |
| Deploy cutover | `golang-blue-green` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Element | Guidance |
| --- | --- |
| Business process | Checkout, login, payout—map to Go services |
| Tiering | Tier 0/1/2 recovery priority |
| RTO/RPO | Per process, approved by business |
| Dependencies | IdP, DNS, KMS, payments, DNS, CI (build-time vs runtime) |
| Degraded mode | Read-only, queue accepts, feature flags off nonessential |
| Comms | Status page, on-call, exec bridge |
| Pitfalls | Ignoring SaaS IdP dependency; backups without RTO path |

## Workflow

### 1. Confirm scope and success criteria

1. Business sponsor, processes in scope, authorization.
2. Success: documented RTO/RPO; dependency map; last drill date with results.
3. Legal/regulatory continuity requirements noted.

### 2. Inventory critical paths

1. Trace user journeys through Go services and data stores.
2. Classify tier and data criticality.
3. List single points of failure.

### 3. Baseline

1. Current HA posture and backup posture.
2. Last incident recovery times (actual RTO evidence).

### 4. Engineer continuity controls

1. HA: multi-AZ minimum for tier 0; multi-region if RTO requires.
2. Data: backups + immutability + verify (`golang-backup-*`).
3. Degraded modes implemented in Go behind flags.
4. Runbooks: loss of region, loss of DB, loss of IdP, supply-chain CI outage.
5. Secrets/KMS break-glass dual control.

```go
// Example degraded mode
if cfg.DegradedReadOnly {
	if r.Method != http.MethodGet {
		http.Error(w, "read-only mode", http.StatusServiceUnavailable)
		return
	}
}
```

### 5. Verify with evidence

1. Tabletop + technical drill (failover/restore) timed.
2. Gap list with owners.
3. Update RTO numbers from drill, not aspirations alone.

```bash
go test ./internal/degraded/... -count=1
```

### 6. Observe and harden

1. Calendar drills (semiannual tier 0).
2. Track dependency changes in architecture reviews.
3. Post-incident BCP updates mandatory.

### 7. Hand off

1. Publish BCP engineering annex; link business plan.
2. Train on-call on degraded modes.
3. Executive summary of residual risks.

## Dependency register sketch

| Dependency | Failure mode | Mitigation |
| --- | --- | --- |
| Primary DB | Outage | Failover + backups |
| IdP | Login down | Emergency cached sessions / break-glass |
| Object store | Uploads fail | Degraded queue |
| DNS | Routing fail | Multi-provider |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| RTO | Drill-measured | Marketing number |
| Scope | Journey-based | Server list only |
| Mode | Tested read-only | Hope for full capacity always |
| Topic fidelity | BCP for Go services | Generic go test only |

## Output Checklist

- [ ] Critical journeys tiered
- [ ] RTO/RPO agreed
- [ ] Dependency map complete
- [ ] Degraded modes designed/tested
- [ ] Drill evidence with timings
- [ ] Runbooks and comms linked
- [ ] Residual risk accepted by business

## Rules

- Business owns priorities; eng owns mechanisms.
- Focus on `golang-bcp-notes`.
- Authorized drills only.
- Evidence over paper plans.
