---
name: golang-airgap-backup
description: >
  Design air-gapped backup and restore for Go services and artifact stores:
  offline media, one-way transfer, encryption, immutability, and restore drills.
  Use for owned systems under authorization.
---

# Golang Airgap Backup

## Research grounding

Runbook for **backups that leave or stay outside** the primary network path—
sneakernet/diode copies, offline vaults—covering data produced by or needed to
recover Go services. Skill id: `golang-airgap-backup`.

## Scope And Authorization

- **In scope:** owned data, labs, authorized DR programs.
- **Out of scope:** copying data you are not permitted to possess.
- Encrypt backups; control media chain-of-custody.
- Redact connection strings; never put plaintext secrets only in “offline” media without key escrow plan.
- Pair automation with `code-quality-standards`.

## When To Use

- Regulatory or ransomware resilience requires offline/air-gapped copies.
- Backing up Go artifact registries, Postgres for Go apps, or config repos into offline store.
- Proving restore into an air-gapped recovery environment.
- Focus tokens: **golang, airgap, backup**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Online immutable backups (WORM/object lock) | `golang-backup-immutable` |
| Backup verification only | `golang-backup-verify` |
| General airgap build/modules | `golang-airgap` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| What to back up | DB dumps, object stores, `go` module proxies, container images, TLS keys (escrow), configs |
| Transport | One-way diode, courier encrypted disk, approved transfer host |
| Crypto | AES-GCM or age/gpg; keys in HSM/offline escrow separate from media |
| Immutability | WORM media or offline vault without delete from prod IAM |
| Go jobs | Backup agents in Go with context timeouts, checksum manifests |
| RPO/RTO | Offline delay may increase RPO; document explicitly |
| Pitfalls | Same credentials can delete online + offline; untested encrypted restore |

## Workflow

### 1. Confirm scope and success criteria

1. Data owners, classification, RPO/RTO, authorization, media custody.
2. Success: offline copy exists within RPO; restore drill meets RTO; checksums match.
3. Who can decrypt; dual control for key access.

### 2. Inventory

1. Systems (Go services, DBs, registries) and backup sizes/churn.
2. Existing online backups (`golang-backup-immutable` / verify).
3. Transfer windows and physical security of vault.

### 3. Baseline

1. Current last successful offline backup timestamp (or none).
2. Sample restore time estimate.
3. Hash algorithm standard (SHA-256).

### 4. Implement backup pipeline

```go
// Conceptual Go backup worker steps
// 1) snapshot/export with app-consistent method
// 2) encrypt stream
// 3) write manifest: files, sizes, sha256, app version, go module sum pin
// 4) hand off to diode/courier interface
// 5) verify write + update control-plane status metric
```

```bash
# Example local evidence generation (owned systems)
pg_dump --format=custom "$DATABASE_URL" -f backup.dump
sha256sum backup.dump > backup.dump.sha256
age -r "$OFFLINE_AGE_RECIPIENT" -o backup.dump.age backup.dump
sha256sum backup.dump.age >> MANIFEST.sha256
```

1. Separate IAM: prod cannot delete offline vault.
2. Include Go-specific recovery bits: `go.mod`/`go.sum`, container digests, migration version.
3. Catalog media labels and retention.

### 5. Verify with evidence

```bash
go test ./internal/backup/... -count=1
go test ./... -count=1

# Restore drill in isolated lab/airgap
age -d -i offline.key -o backup.dump backup.dump.age
sha256sum -c backup.dump.sha256
# restore DB; boot Go service; go test smoke or /healthz
```

1. Prove encryption required (cannot restore without key).
2. Prove integrity fail detection (tamper manifest → reject).
3. Time the drill; record gaps vs RTO.

### 6. Observe and harden

1. Metrics: last offline success age; drill overdue flag.
2. Alert if offline RPO breached; alert on encrypt/transfer failures.
3. Rotate offline keys with dual control; test after rotation.

### 7. Hand off

1. Runbook: courier procedure, vault access, restore order (keys → data → app).
2. Calendar restore drills (quarterly minimum for critical).
3. Link `golang-backup-verify` for routine checks.

## Media chain-of-custody

| Step | Record |
| --- | --- |
| Create | Operator, timestamp, manifest hash |
| Transfer | Carrier, seal numbers |
| Vault | Location, dual control log |
| Restore test | Result, RTO measured |
| Destroy | Certificate of destruction |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Separation | Offline vault independent IAM | S3 “backup” same account admin |
| Crypto | Keys offline/HSM | Password on sticky note with disk |
| Proof | Timed restore drill | “Backup job green” only |
| Go recovery | Modules + migrate version included | Binary only, cannot rebuild |
| Topic fidelity | Airgap offline backup | Generic go test only |

## Output Checklist

- [ ] Scope, RPO/RTO, custody model recorded
- [ ] Data inventory complete
- [ ] Encrypted offline pipeline implemented
- [ ] Manifest checksums standard enforced
- [ ] Restore drill evidence with timings
- [ ] Alerts for stale offline copies
- [ ] Key escrow and dual control documented
- [ ] `code-quality-standards` applied to backup code

## Rules

- Authorized data only; encrypt at rest on media.
- Prefer immutable offline copies adversaries cannot wipe.
- Focus on `golang-airgap-backup`; module airgap builds → `golang-airgap`.
- Never store decryption keys on the same media as ciphertext without control.
