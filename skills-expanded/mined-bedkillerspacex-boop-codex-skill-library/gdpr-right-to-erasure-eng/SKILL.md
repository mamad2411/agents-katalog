---
name: gdpr-right-to-erasure-eng
description: >
  Engineering runbook for GDPR-style right to erasure / delete (Art. 17 style):
  cascade deletes, soft-delete vs hard-delete, anonymization, backups/logs retention,
  legal holds, and verification. Use only under privacy-ops authorization on systems
  you operate — not to destroy evidence or third-party data. Legal calls need counsel.
---

# GDPR Right to Erasure (Engineering)

## Scope And Authorization

- **In scope:** Delete/anonymize personal data in systems you operate after privacy team
  approves an erasure request (and identity verification).
- **Out of scope:** Unilateral production wipes; destroying data under legal hold;
  attacking third-party services; legal determinations of exemptions.
- Coordinate with legal for litigation holds, fraud, statutory retention (tax, AML).
- Prefer reversible soft-delete only when policy allows temporary recovery windows —
  final state must match privacy decision (hard delete vs anonymize).
- Pair with `gdpr-data-subject-export` when access is requested alongside erasure.

## When To Use

- Implementing account deletion pipelines and worker jobs.
- Cascading erasure across microservices, search indexes, analytics, CRM.
- Handling backups, cold storage, and log rehydration constraints.
- Proving erasure with audit trails for privacy ops.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Data subject export / portability | `gdpr-data-subject-export` |
| Secrets rotation after leak | `secrets-management-hygiene` |
| Database migration patterns | `database-migration-safety` |
| Backup engineering only | backup/DR skills |
| Legal exemption analysis | DPO / counsel |
| Implementation quality | `code-quality-standards` |

## Concepts

| Approach | Use when |
| --- | --- |
| Hard delete | Remove rows/objects; no residual personal identifiers |
| Anonymization | Keep aggregate analytics if irreversible per counsel standard |
| Pseudonymization | Often **insufficient** alone for erasure — confirm with privacy |
| Soft delete | UX recovery window; must later hard-delete/anonymize |
| Cascades | Child tables, caches, CDN, email ESP, search |
| Backup lag | Erasure completes when backups expire or are rewritten per policy |
| Legal hold | Blocks erasure until released |

### Service graph

Map each store:

```text
Auth DB → Profile DB → Media bucket → Search index → Warehouse → ESP → Support SaaS
```

Each edge needs a delete/anonymize API or ticket path.

## Workflow

### 1. Authorization gate

1. Privacy ticket: request id, subject keys, exemptions applied, due date.
2. Identity verified; legal hold check **clear**.
3. If hold or exemption: document partial erasure scope — do not improvise.
4. Success: all in-scope systems report deleted/anonymized; subject cannot login; export empty.

### 2. Build deletion plan

| System | Method | Idempotent? | Owner |
| --- | --- | --- | --- |
| Primary user row | Hard delete or status=`erased` + wipe PII columns | Yes | Identity |
| Objects `user_id/*` | Lifecycle delete | Yes | Media |
| Elasticsearch | Delete-by-query | Yes | Search |
| Warehouse | Anonymize or drop partitions | Batch | Data |
| Stripe/CRM | Vendor deletion API | Vendor SLA | Finance |

Prefer **orchestrated saga** with per-system receipts over silent best-effort.

### 3. Implement delete worker

```text
# Pseudocode
# for system in plan:
#   receipt = system.erase(subject_keys, request_id)
#   store receipt (system, status, timestamp, error)
#   retry with backoff on transient failure
# on all success: mark request FULFILLED
# on permanent failure: page owner; leave ticket OPEN
```

```bash
# Example internal CLI
# ./tools/dsar-erase --request-id=R-456 --user-id=U-9 --dry-run
# ./tools/dsar-erase --request-id=R-456 --user-id=U-9 --execute
```

Idempotency: re-running must not fail if already erased; record `already_clean`.

### 4. Auth and session invalidation

1. Revoke refresh tokens, sessions, API keys, remember-me cookies.
2. Disable login; reject re-registration policy per product (may allow new account).
3. Rotate any secrets that embedded subject identifiers if applicable (rare).

### 5. Downstream and vendors

- Issue processor instructions / vendor privacy APIs.
- Remove from marketing lists and ESP suppression as required.
- Clear CDN caches for user-specific URLs.
- Search/index rebuild verification.

### 6. Backups and logs

| Store | Practical control |
| --- | --- |
| Daily DB snapshots | Erasure effective after retention elapses; document max residual window |
| WAL / binlogs | Time-bounded; do not build tools to surgically edit live WAL in panic |
| SIEM logs | Retention policy; filter/minimize PII going forward |
| Email backups | Vendor-dependent |

Privacy team must accept residual backup windows — engineer documents max age.

### 7. Verify

| Test | Expect |
| --- | --- |
| Login | Fail |
| DSAR export | Empty / not found |
| Public profile URL | 404 |
| Search by email | No hits |
| Admin internal tools | No PII fields (or tombstone without PII) |
| Re-run erase | Idempotent success |

```bash
# ./tools/dsar-export --user-id=U-9  → no data / error not found
# curl -sI https://app.example.com/u/U-9  → 404
```

### 8. Close and metrics

- Attach receipts to privacy ticket; checksum of tombstone record if used.
- Metrics: time-to-erase, systems failing SLA, backup residual days.
- Postmortem if any system missed (data resurfacing).

## Soft-delete vs hard-delete policy sketch

| Phase | State |
| --- | --- |
| T0 request | Account locked |
| T0–T7 (optional grace) | Soft-deleted; restore possible if policy allows |
| T7 | Hard delete / anonymize cascade |
| T7+R | Backups age out |

Never promise “instant global purge including all backups” unless architecture supports it.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Orchestration | Receipts per system | Delete primary only |
| Idempotency | Safe re-run | Second run crashes half graph |
| Holds | Block + document | Delete despite legal hold |
| Analytics | True anonymization reviewed | Hash email and call it anonymous |
| Verification | Export empty + 404 | “Job returned 200” |
| Secrets | No PII in logs of eraser | Log full user row on delete |

## Output Checklist

- [ ] Privacy authorization, identity, hold check recorded
- [ ] System graph and method matrix complete
- [ ] Erase executed with per-system receipts
- [ ] Sessions/tokens revoked
- [ ] Vendors instructed / APIs called
- [ ] Backup residual window documented
- [ ] Verification tests passed
- [ ] Ticket closed with evidence (no PII attached)
- [ ] Missed-system remediation filed if any
- [ ] `code-quality-standards` applied to erase tooling

## Rules

- Only with privacy-ops authorization; not legal advice.
- Never destroy data under legal hold.
- Idempotent, observable, least-privilege erase workers.
- Do not log personal data in eraser telemetry.
- Export skill is separate; do not mix packages with delete side effects casually.
