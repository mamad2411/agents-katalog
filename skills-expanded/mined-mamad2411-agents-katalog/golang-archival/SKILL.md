---
name: golang-archival
description: >
  Implement data archival for Go services: retention tiers, cold storage jobs,
  legal hold, restore paths, and schema compatibility. Use for owned data under
  policy authorization.
---

# Golang Archival

## Research grounding

Runbook for **archiving cold data** out of primary stores used by Go services—
lifecycle policies, batch workers, and retrieval SLAs. Skill id:
`golang-archival`.

## Scope And Authorization

- **In scope:** data you own; retention policies approved by data owners.
- **Out of scope:** deleting/archiving data to evade legal holds or audits.
- Honor legal hold > lifecycle delete.
- Encrypt archives; control access.
- Pair with `golang-backup-verify`, privacy skills, `code-quality-standards`.

## When To Use

- Primary DB growth; need tiering to object storage.
- Compliance retention (keep N years, online M months).
- Building Go archival/restore workers.
- Focus tokens: **golang, archival**.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Online backups / immutability | `golang-backup-immutable` |
| Offline airgap copies | `golang-airgap-backup` |
| Anonymized analytics export | `golang-anonymize` |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Area | Guidance |
| --- | --- |
| Tiers | Hot (DB) → Warm (fast object) → Cold (glacier class) → Dispose |
| Selection | Time-based, status-based (closed tickets), size-based |
| Format | Parquet/Avro/JSONL + schema version; include checksum |
| Go jobs | Batch with keyset pagination; idempotent object keys |
| Index | Keep skinny index in DB for locate/restore |
| Legal hold | Flag suppresses delete/archive mutation |
| Pitfalls | Archiving without restore test; schema drift; missing FK children |

## Workflow

### 1. Confirm scope and success criteria

1. Data classes, retention schedule, RTO for restore, authorization.
2. Success: job archives eligible rows; primary shrinks; sample restore works.
3. Legal hold process identified.

### 2. Inventory

1. Tables/collections and growth rates.
2. Access patterns (can UI tolerate restore delay?).
3. Existing lifecycle rules on buckets.

### 3. Baseline

1. Row counts/sizes; query latency.
2. Define eligibility SQL/filter (`closed_at < now()-interval '18 months'`).

### 4. Implement Go archival worker

```go
type ArchiveBundle struct {
	SchemaVersion int             `json:"schema_version"`
	ExportedAt    time.Time       `json:"exported_at"`
	Records       json.RawMessage `json:"records"`
	SHA256        string          `json:"sha256"`
}

func (w *Worker) ArchiveBatch(ctx context.Context, limit int) error {
	rows, err := w.db.QueryContext(ctx, selectEligible, limit)
	// serialize → checksum → put object → delete/move rows in tx carefully
	// prefer: write object first, then mark archived, then delete hot rows
	return err
}
```

1. Order: **write archive → verify checksum → mark → delete hot** (never delete first).
2. Transaction strategy: avoid long locks; use batched key ranges.
3. Include children entities in same bundle or referential manifest.
4. Encryption: SSE-KMS or client-side; separate key policy.
5. Metrics: `archived_rows_total`, `archive_failures`, lag vs policy.

### 5. Verify with evidence

```bash
go test ./internal/archive/... -count=1
go test ./... -race -count=1

# Staging drill: archive one batch, restore to side table, diff counts
```

1. Checksum mismatch path rejects delete.
2. Legal hold row skipped (test).
3. Application read path: clear UX when object is archived (404 with “restore requested”).

### 6. Observe and harden

1. Alert on archive lag (policy breach) and failure rate.
2. Lifecycle dispose only after retention; dual control for early delete.
3. Schema evolution: readers support N-1 formats.

### 7. Hand off

1. Runbook: request restore, priority, SLA.
2. Data owner quarterly review of eligibility rules.
3. Link backup skills for disaster vs archival (different purpose).

## Hot vs archive vs backup

| | Archival | Backup |
| --- | --- | --- |
| Purpose | Cost/compliance tiering | Disaster recovery |
| Access | Occasional restore | Rare full restore |
| Selection | Cold subset | Full consistent snapshot |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Order | Object then delete | Delete then upload |
| Schema | Versioned bundles | Raw DB pages only |
| Hold | Skip on legal hold | Lifecycle wipes held data |
| Proof | Restore drill | “Job succeeded” |
| Topic fidelity | Archival jobs in Go | Generic go test only |

## Output Checklist

- [ ] Retention policy and legal hold path documented
- [ ] Eligibility rules defined
- [ ] Go worker idempotent with checksums
- [ ] Restore drill evidence
- [ ] Metrics/alerts for lag/failures
- [ ] Encryption and access controls
- [ ] `code-quality-standards` applied

## Rules

- Never archive to defeat litigation holds.
- Prefer reversible mark before hard delete.
- Focus on `golang-archival`.
- Protect archive encryption keys.
