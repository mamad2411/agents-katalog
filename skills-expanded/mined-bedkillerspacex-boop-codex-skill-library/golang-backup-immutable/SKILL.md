---
name: golang-backup-immutable
description: >
  Design immutable backups for Go service data: object lock/WORM, separate
  accounts, ransomware resistance, and restore paths. Use for owned systems
  under authorization.
---

# Golang Backup Immutable

## Research grounding

Runbook for **immutable (WORM) backups** protecting data behind Go services from
ransomware and rogue delete—online object-lock patterns (offline →
`golang-airgap-backup`). Skill id: `golang-backup-immutable`.

## Scope And Authorization

- **In scope:** backup accounts and data you own.
- **Out of scope:** locking someone else’s data; evading legal deletion without counsel.
- Separate IAM so prod compromise cannot delete immutables.
- Pair with `golang-backup-verify`, `golang-airgap-backup`, `code-quality-standards`.

## When To Use

- Ransomware resilience requirements for DB/object backups.
- Configuring S3 Object Lock / Azure immutability / similar for Go backup agents.
- Splitting backup admin from production admin.
- Focus tokens: **golang, backup, immutable**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Restore drills | `golang-backup-verify` |
| Offline/airgap copies | `golang-airgap-backup` |
| Audit trail WORM | `golang-audit-trail` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Control | Guidance |
| --- | --- |
| Object Lock | COMPLIANCE mode for strong guarantees; GOVERNANCE if dual-control override needed |
| Retention | ≥ known dwell time of ransomware; align legal |
| Account split | Backup account ≠ prod account; deny delete from prod role |
| Encryption | KMS CMK with restricted admins |
| Go agent | PutObject with retention headers; no delete API in code path |
| Pitfalls | Same credentials wipe backup; mutable “backup” bucket |

## Workflow

### 1. Confirm scope and success criteria

1. Data sources, RPO/RTO, retention, authorization.
2. Success: delete attempts fail during retention; restore still works.
3. Legal deletion process if ever required.

### 2. Inventory

1. Current backup jobs (logical dumps, snapshots, volume).
2. Who can `s3:DeleteObject` / equivalent.
3. Go backup workers and their IAM roles.

### 3. Baseline

1. Last successful backup age.
2. Test delete permission map.

### 4. Implement

```bash
# Illustrative: enable object lock on bucket (account setup once)
# aws s3api put-object-lock-configuration ...

# Go upload must set retention (SDK)
# PutObject with ObjectLockMode COMPLIANCE and RetainUntilDate
```

```go
// Pseudocode IAM idea: role can Put + Get, not Delete/PutRetention shorten
```

1. Write backups only to lock-enabled prefix.
2. Versioning on; MFA delete where applicable for control plane.
3. Cross-account replication to second immutable vault optional but strong.
4. Include Go app recovery metadata (schema version, image digest).

### 5. Verify with evidence

```bash
go test ./internal/backup/... -count=1
# Attempt delete of locked object with prod role → AccessDenied
# Attempt delete with backup admin before retention end → denied (compliance)
```

1. Restore sample to staging (`golang-backup-verify`).
2. Redact credentials from evidence.

### 6. Observe and harden

1. Alert if no immutable object written within RPO.
2. Alert on any governance override use.
3. Periodic access review of backup account.

### 7. Hand off

1. Runbook: restore, extend retention, emergency legal delete path.
2. Owners for backup account root/break-glass.
3. Link airgap for offline tier.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| IAM | Split accounts | Prod admin owns backup bucket fully |
| Lock | Compliance retention | Soft delete only |
| Code | No delete in agent | “Cleanup” deletes old backups immediately |
| Topic fidelity | Immutable backups | Generic go test only |

## Output Checklist

- [ ] Retention and RPO defined
- [ ] WORM/object lock configured
- [ ] IAM separation proven with deny evidence
- [ ] Go agent writes with retention
- [ ] Restore path documented
- [ ] Alerts on backup freshness
- [ ] `code-quality-standards` applied

## Rules

- Immutability is about delete resistance; still encrypt.
- Focus on `golang-backup-immutable`.
- Authorized only.
- Do not disable lock to “save cost” without risk acceptance.
