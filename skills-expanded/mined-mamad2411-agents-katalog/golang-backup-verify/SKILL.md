---
name: golang-backup-verify
description: >
  Verify backups for Go services with restore drills: checksums, automated
  restore to staging, app smoke tests, and evidence packs. Use for owned systems.
---

# Golang Backup Verify

## Research grounding

Runbook for **proving backups work** via restore—not just job success—for data
used by Go applications. Skill id: `golang-backup-verify`.

## Scope And Authorization

- **In scope:** backups and staging restore targets you own.
- **Out of scope:** restoring into production without change control; accessing unauthorized data.
- Prefer isolated restore accounts/networks.
- Redact production data in evidence when using masked restores.
- Pair with `golang-backup-immutable`, `golang-airgap-backup`, `code-quality-standards`.

## When To Use

- Establishing or auditing backup reliability for Go services.
- Automating periodic restore tests with Go smoke checks.
- After backup system changes or ransomware tabletop.
- Focus tokens: **golang, backup, verify**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Implementing immutable storage | `golang-backup-immutable` |
| Offline media custody | `golang-airgap-backup` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Check | Guidance |
| --- | --- |
| Existence | Backup objects present within RPO |
| Integrity | Checksums/manifest match |
| Restorability | Actually restore |
| Usefulness | Go app boots and passes smoke |
| Freshness | Point-in-time meets RPO |
| Security | Restored env not public |
| Pitfalls | “Green backup job” without restore |

## Workflow

### 1. Confirm scope and success criteria

1. Systems, RPO/RTO, authorization, drill cadence.
2. Success: timed restore ≤ RTO; checksums OK; smoke tests pass.
3. Data handling (mask/anonymize if required).

### 2. Inventory

1. Backup types (snapshot, dump, logical).
2. Dependencies (KMS keys, IAM, DNS).
3. Smoke test suite for Go service.

### 3. Baseline

1. Last drill date and result (or none).
2. Current RTO measurement if any.

### 4. Run verification

```bash
# 1) Fetch backup + verify checksum
sha256sum -c MANIFEST.sha256

# 2) Restore to isolated staging DB
# pg_restore / cloud snapshot restore ...

# 3) Point Go service at restored DSN (staging)
export DATABASE_URL=...
go test ./internal/smoke/... -count=1
# or ./app && curl -fsS localhost:8080/healthz
```

```go
// Smoke tests should not mutate external prod
func TestCriticalReads(t *testing.T) {
	// select counts, login path, migration version matches expected
}
```

1. Automate weekly/monthly; store duration metrics.
2. Test key restoration (can you decrypt?).
3. Partial restore drills for large datasets if full too costly—document residual risk.

### 5. Verify with evidence

1. Screenshots/logs redacted; timestamps; who ran.
2. Compare row counts/sample hashes where safe.
3. Fail the drill if smoke fails even if restore “succeeds”.

### 6. Observe and harden

1. Dashboard: last successful verify age; alert if overdue.
2. Feed failures into backup redesign.
3. Rotate participants so knowledge is not single-person.

### 7. Hand off

1. Evidence pack location and retention.
2. Update RTO numbers in BCP (`golang-bcp-notes`).
3. Apply `code-quality-standards` to smoke tests.

## Drill cadence

| System criticality | Cadence |
| --- | --- |
| Tier 0 / payments | Monthly full or partial |
| Tier 1 | Quarterly |
| Tier 2 | Semi-annual |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Proof | Timed restore + smoke | Checkbox “backups enabled” |
| Isolation | Private staging | Restore open to Internet |
| Data | Masked if needed | Uncontrolled PII sprawl |
| Topic fidelity | Backup verification | Generic go test only |

## Output Checklist

- [ ] RPO/RTO and cadence set
- [ ] Integrity check performed
- [ ] Restore completed with timing
- [ ] Go smoke tests passed
- [ ] Evidence pack stored (redacted)
- [ ] Overdue alerts configured
- [ ] `code-quality-standards` applied

## Rules

- Untested backups are hopes, not controls.
- Focus on `golang-backup-verify`.
- Authorized restore targets only.
- Protect restored copies as production-class data.
