---
name: golang-audit-trail
description: >
  Build tamper-evident immutable audit trails for Go systems: append-only stores,
  hash chaining, WORM retention, and verification jobs. Use for owned high-assurance
  logging under authorization.
---

# Golang Audit Trail

## Research grounding

Runbook for **immutable, tamper-evident audit trails**—stronger than basic audit
logging—using WORM storage and/or cryptographic chaining from Go writers.
Skill id: `golang-audit-trail`.

## Scope And Authorization

- **In scope:** owned audit systems; compliance-driven immutability.
- **Out of scope:** destroying trails under legal hold; unauthorized access to trails.
- Separate duties: admins of app ≠ sole custodians of trail delete power.
- Pair with `golang-audit-logging` (event content), `golang-backup-immutable`.

## When To Use

- Regulatory need for non-repudiation / immutability of security events.
- Implementing hash-chained audit logs in Go.
- Object-lock / WORM buckets for audit export.
- Focus tokens: **golang, audit, trail**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Event schema / what to log | `golang-audit-logging` |
| General backups | `golang-backup-immutable` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Control | Guidance |
| --- | --- |
| Append-only | No UPDATE/DELETE on audit table for normal roles |
| WORM | S3 Object Lock / blob immutability retention |
| Hash chain | `H_n = hash(H_{n-1} || payload_n)` |
| Signing | Optional per-batch signatures with KMS |
| Verify job | Recompute chain periodically |
| Access | Read-only investigators; break-glass dual control |
| Pitfalls | App role can DELETE; chain key on same host only |

## Workflow

### 1. Confirm scope and success criteria

1. Retention (e.g. 7 years), RPO for trail, authorization.
2. Success: cannot alter past events with app credentials; verify job green.
3. Legal hold interaction documented.

### 2. Inventory

1. Current audit sink and who can modify it.
2. Clock sync and identity of writers.
3. Existing backups of logs.

### 3. Baseline

1. Threat: malicious admin, ransomware, silent edit.
2. Choose WORM and/or chain (often both).

### 4. Implement

```go
type ChainedEvent struct {
	Seq       uint64    `json:"seq"`
	PrevHash  string    `json:"prev_hash"`
	Payload   []byte    `json:"payload"`
	ThisHash  string    `json:"this_hash"`
	Time      time.Time `json:"time"`
}

func HashEvent(prev string, payload []byte) string {
	h := sha256.New()
	_, _ = io.WriteString(h, prev)
	_, _ = h.Write(payload)
	return hex.EncodeToString(h.Sum(nil))
}
```

1. Writer service uses identity that can **Put** but not **Delete** on WORM prefix.
2. Batch export to object lock bucket with retention mode COMPLIANCE/GOVERNANCE per policy.
3. Store chain head in durable meta; alert on sequence gaps.
4. Verification: nightly Go job recomputes hashes; pages on mismatch.

### 5. Verify with evidence

```bash
go test ./internal/audittrail/... -count=1
go test ./... -race -count=1

# Attempt delete with app role → AccessDenied (cloud evidence)
# Tamper payload copy → verify job fails
```

1. Red-team role separation with owned accounts.
2. Restore-from-backup still verifies chain.

### 6. Observe and harden

1. Metrics: chain height, verify failures, write latency.
2. Key rotation for signatures without rewriting history (sign batches).
3. Drill: ransomware simulation cannot wipe WORM (authorized).

### 7. Hand off

1. Runbook for investigators and verify failure response.
2. Dual control for governance retention shorten (if allowed).
3. Link event producers to `golang-audit-logging`.

## Comparison

| Feature | Audit logging | Audit trail |
| --- | --- | --- |
| Schema | Essential | Essential |
| Immutability | Best effort | Required |
| Tamper evidence | Optional | Required |
| Delete path | Restricted | Denied / dual control |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| IAM | Write-only to WORM | Admin full delete |
| Chain | Continuous verify | Chain never checked |
| Time | NTP + monotonic seq | Trust client timestamps only |
| Topic fidelity | Immutable trails | Generic go test only |

## Output Checklist

- [ ] Threat model and retention set
- [ ] WORM and/or chain implemented
- [ ] IAM separation proven
- [ ] Verify job + alert
- [ ] Tamper test evidence
- [ ] Investigator access path
- [ ] `code-quality-standards` applied

## Rules

- Preserve trails under legal hold.
- Focus on `golang-audit-trail`.
- No shared god-mode over trail delete.
- Authorized tests only for tamper drills.
