---
name: golang-attack-mapping
description: >
  Map threats and detections for Go services to MITRE ATT&CK: technique coverage,
  telemetry requirements, and control gaps. Use for owned systems under
  authorization.
---

# Golang Attack Mapping

## Research grounding

Runbook for **ATT&CK mapping** of threats, logs, and controls around Go
workloads (APIs, workers, CI). Not a full ATT&CK export. Skill id:
`golang-attack-mapping`.

## Scope And Authorization

- **In scope:** systems you own; defensive mapping and authorized purple-team.
- **Out of scope:** operationalizing attacks against unauthorized targets.
- Prefer detection engineering over exploit development here.
- Redact sensitive detection logic only if policy requires; never paste secrets.
- Pair with `golang-blue-detect`, `golang-attack-trees`, `code-quality-standards`.

## When To Use

- Building a threat coverage matrix for a Go service platform.
- Linking SIEM detections to ATT&CK techniques with Go-specific telemetry.
- Gap analysis before audits or BAS exercises (`golang-bas-tools`).
- Focus tokens: **golang, attack, mapping**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Building attack trees | `golang-attack-trees` |
| Detection implementation detail | `golang-blue-detect` |
| BAS tooling ops | `golang-bas-tools` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus — sample Go-relevant techniques

| ATT&CK-ish area | Go estate examples | Telemetry |
| --- | --- | --- |
| Valid Accounts | Stolen API tokens to Go API | Auth logs, impossible travel |
| Exploit Public-Facing App | RCE/injection on Go HTTP | WAF, app errors, panic logs |
| Ingress Tool Transfer | Malicious upload endpoints | Size/type metrics, AV |
| Discovery | SSRF metadata probes | Egress logs from Go clients |
| Credential Access | Secrets in env scraped | Secret scan, anomalous reads |
| Lateral | Compromised CI OIDC → cloud | CI logs, cloud trail |
| Impact | Destructive admin API | Audit log of delete bulk |

## Workflow

### 1. Confirm scope and success criteria

1. System boundary, ATT&CK matrix version, authorization.
2. Success: matrix of techniques → controls/detections → gaps with owners.
3. Prioritize techniques by realistic exposure of the Go app.

### 2. Inventory assets and telemetry

1. Go services, admin paths, CI, cloud roles.
2. Logs/metrics available (structured slog fields, audit, gateway).
3. Existing detections and controls.

### 3. Baseline

1. Import or create empty coverage sheet (technique, status, evidence).
2. Mark not-applicable with rationale (e.g., no email in system).

### 4. Map

| Column | Content |
| --- | --- |
| Technique ID/name | e.g. T1190 |
| Procedure (Go-specific) | How it would look here |
| Prevent | Control (WAF, authz, ASVS gate) |
| Detect | Rule/metric |
| Respond | Runbook |
| Gap | Missing prevent/detect |

```go
// Ensure telemetry exists for mapping claims
// e.g. auth decisions with reason codes
logger.Info("authz_decision",
	"principal", p.ID,
	"action", act,
	"resource", res.ID,
	"decision", "deny",
	"reason", "tenant_mismatch",
)
```

1. Prefer procedures over abstract technique names.
2. Link code paths (route, job) for each procedure.
3. Score coverage: none / partial / full.

### 5. Verify with evidence

1. For each “full” detection: show rule + sample hit from staging test.
2. For prevent: show config/test evidence.
3. Update after purple-team or BAS.

```bash
go test ./internal/audit/... -count=1
go test ./... -count=1
```

### 6. Observe and harden

1. Quarterly remap after architecture changes.
2. Feed gaps into backlog with severity.
3. Align with `golang-asvs-gates` where preventative.

### 7. Hand off

1. Publish matrix to security + service owners.
2. Track coverage % KPI.
3. Link trees for deep scenarios (`golang-attack-trees`).

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Mapping | Procedure-level for Go apps | Copy entire ATT&CK unchecked |
| Detect | Proven with sample | “We have logs” |
| Scope | Authorized estate | Random Internet targets |
| Topic fidelity | ATT&CK mapping for Go | Generic go test only |

## Output Checklist

- [ ] Scope and matrix version set
- [ ] Assets/telemetry inventoried
- [ ] Technique×procedure map filled
- [ ] Gaps owned and prioritized
- [ ] Sample evidence for full coverage claims
- [ ] Review cadence scheduled
- [ ] `code-quality-standards` applied to telemetry code

## Rules

- Defensive mapping; authorized testing only.
- Evidence over checkbox coverage.
- Focus on `golang-attack-mapping`.
- Do not publish actionable exploit details beyond need-to-know.
