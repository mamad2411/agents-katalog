---
name: golang-blue-detect
description: >
  Build blue-team detections for Go services: telemetry fields, SIEM rules,
  behavioral signals, testing, and tuning. Use for owned environments under
  authorization.
---

# Golang Blue Detect

## Research grounding

Runbook for **detection engineering** focused on threats against Go application
platforms—content creation, testing, and maintenance. Skill id:
`golang-blue-detect`.

## Scope And Authorization

- **In scope:** telemetry and detections you own; authorized attack simulation.
- **Out of scope:** surveillance beyond policy; detections used to harm outsiders.
- Prefer high-fidelity rules; manage noise via `golang-alert-fatigue`.
- Pair with `golang-attack-mapping`, `golang-bas-tools`, `golang-audit-logging`.

## When To Use

- Writing SIEM/EDR/app detections for Go API abuse, token theft, supply chain.
- Adding detection-friendly fields to Go logs/metrics.
- Validating rules after feature launches.
- Focus tokens: **golang, blue, detect**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| ATT&CK coverage matrix | `golang-attack-mapping` |
| BAS execution | `golang-bas-tools` |
| Anomaly ML tuning | `golang-anomaly-tuning` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Detection idea | Telemetry from Go |
| --- | --- |
| Authz deny spikes | `authz_decision=deny` with reason |
| Token reuse / anomaly IP | login events + geo/ASN |
| Admin bulk export | audit action `export` volume |
| SSRF attempts | outbound to link-local from app |
| Panic/RCE probe | panic logs + unusual process if host |
| CI anomaly | deploy identity outside pipeline |
| SQLi patterns | DB error rates + WAF (app still parameterized) |

## Workflow

### 1. Confirm scope and success criteria

1. Threat scenarios prioritized, authorization, on-call for detections.
2. Success: rule with documented true positive test; false positive budget; owner.
3. Severity → page vs ticket mapping.

### 2. Inventory telemetry

1. Ensure Go services emit required fields (`golang-audit-logging`).
2. Clock sync, request IDs, principal IDs.
3. Retention sufficient for investigation.

### 3. Baseline

1. Normal rates for candidate signals (`golang-baseline-behavior`).
2. Known noisy endpoints.

### 4. Build detections

```go
// Detection-friendly structured log
logger.Warn("security_signal",
	"signal", "authz_deny",
	"principal", id,
	"route", route,
	"reason", reason,
	"request_id", rid,
)
```

1. Write rule logic (SIEM query / sigma / native) with clear entities.
2. Map to ATT&CK technique IDs.
3. Unit test pipeline with sample logs if platform allows.
4. Staging fire test using authorized simulation.
5. Document runbook: investigate steps, containment, false positive mute with expiry.

### 5. Verify with evidence

1. True positive: sim produces alert.
2. Negative: normal traffic does not page.
3. Redacted sample alert attached to detection ticket.

```bash
go test ./internal/audit/... -count=1
```

### 6. Observe and harden

1. Track FP rate; tune or disable flapping rules.
2. Coverage gaps → mapping backlog.
3. After incidents, write detection if missing (postmortem action).

### 7. Hand off

1. Detection as code in git with review.
2. Owner and last test date.
3. Link BAS continuous validation.

## Rule quality bar

| Attribute | Required |
| --- | --- |
| Owner | team |
| ATT&CK map | yes |
| Runbook URL | yes |
| Last tested | ≤ 90 days |
| Severity | defined |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Fidelity | Tested TP/FP | Unowned noisy regex |
| Telemetry | Structured fields | Unparseable printf |
| Response | Runbook | Alert only “something weird” |
| Topic fidelity | Blue detections for Go | Generic go test only |

## Output Checklist

- [ ] Scenarios prioritized
- [ ] Telemetry fields present
- [ ] Rules implemented with ATT&CK IDs
- [ ] TP/FP tests recorded
- [ ] Runbooks linked
- [ ] Owners and review dates
- [ ] Noise managed

## Rules

- Detection quality over quantity.
- Focus on `golang-blue-detect`.
- Authorized simulations only.
- Never log secrets to enable detections.
