---
name: gdpr-data-subject-export
description: >
  Engineering runbook for GDPR data subject access / portability exports (Art. 15/20
  style): locate personal data, package machine-readable export, identity verification,
  secure delivery, and audit logging. Use for systems you operate under lawful process —
  not to exfiltrate data or bypass access controls. Legal interpretation requires counsel.
---

# GDPR Data Subject Export (Engineering)

## Scope And Authorization

- **In scope:** Systems your organization operates; requests handled under company DSAR
  process with legal/privacy approval.
- **Out of scope:** Pulling personal data without a validated request; using this skill
  to harvest data from third parties; legal advice (engage privacy counsel).
- Verify requester identity per policy before any export.
- Minimize data in tickets; encrypt exports at rest and in transit; set retention on export packages.
- Pair implementation with `code-quality-standards` and privacy program owners.

## When To Use

- Building or operating a Subject Access Request (SAR/DSAR) export pipeline.
- Mapping systems of record for a data subject identifier.
- Producing JSON/CSV packages for access or portability.
- Logging fulfillment for accountability (Art. 5/30 style operational evidence).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Right to erasure / delete pipelines | `gdpr-right-to-erasure-eng` |
| Secrets hygiene | `secrets-management-hygiene` |
| Generic observability | `observability-metrics-tracing` |
| Legal opinion on lawful basis | Privacy counsel / DPO — not a skill |
| Security incident response | IR playbooks |
| Implementation quality | `code-quality-standards` |

## Concepts

| Term | Engineering meaning |
| --- | --- |
| DSAR / SAR | Request to access personal data |
| Data subject | Identified/identifiable natural person |
| Systems of record | DBs, logs, object stores, SaaS with user data |
| Portability | Structured, commonly used, machine-readable format |
| Identity assurance | AuthN strength before release |
| Third-party processors | Vendors that must be queried or instructed |
| Redaction | Exclude other people’s data, secrets, pure security logs per policy |

**Disclaimer:** Timelines, exemptions, and legal scope vary by jurisdiction and counsel
guidance. This skill is an **engineering** checklist, not compliance certification.

## Workflow

### 1. Intake and authorization gate

1. Receive ticket from privacy ops with: request id, subject identifiers, scope, due date.
2. Confirm identity verification status (**do not export** if pending).
3. Confirm legal holds / exemptions flags from privacy team.
4. Success: complete package delivered via approved channel before internal SLA.

### 2. Identity keys and search plan

Build a join key set (examples):

| Key | Sources |
| --- | --- |
| `user_id` / UUID | Primary DB |
| email / phone | Auth, CRM |
| device_id | Mobile analytics (policy-dependent) |
| customer_id | Billing |
| account handles | Social features |

Document systems in scope from ROPA/data map; do not invent scope beyond ticket.

### 3. Extract from systems of record

```text
# Pattern per system (authorized production read replicas preferred):
# 1) Query by subject keys only
# 2) Write to restricted export workspace (encrypted volume)
# 3) Record row counts + checksums, not sample PII, in ticket
```

Example categories:

- Profile & account
- Content created by user
- Transactions / orders
- Support tickets (may include agent notes — policy)
- Marketing preferences
- Auth events (minimize; often security-sensitive)

```bash
# Example: app admin CLI (illustrative)
# ./tools/dsar-export --request-id=R-123 --user-id=U-9 --out=/secure/exports/R-123/
# chmod 600 /secure/exports/R-123/*
```

### 4. Package format

Prefer machine-readable:

```text
/export/R-123/
  manifest.json      # request id, generated_at, systems[], counts, schema_version
  profile.json
  orders.csv
  messages.jsonl
  README.txt         # human summary, contact for questions
```

`manifest.json` sketch:

```json
{
  "request_id": "R-123",
  "subject_ref": "redacted-or-internal-id",
  "generated_at": "2026-07-12T00:00:00Z",
  "systems": ["users-db", "billing", "support"],
  "format_version": 1
}
```

Portability: avoid screenshots-only; use UTF-8 JSON/CSV.

### 5. Filter and quality checks

| Check | Action |
| --- | --- |
| Other data subjects in threads | Redact third-party PII per policy |
| Secrets / tokens / passwords | Never include password hashes if policy forbids; never include live session tokens |
| Blind indexes only | Do not reverse beyond stored personal data |
| Completeness | Each in-scope system either contributed files or logged “no data” |
| Accuracy | Spot-check with privacy ops (not by emailing raw PII broadly) |

### 6. Secure delivery

1. Encrypt archive (enterprise secure share, portal download, or encrypted email per policy).
2. Authenticate download (same identity assurance bar).
3. Log: who generated, who approved, who downloaded, timestamps.
4. Schedule deletion of working files after retention window (e.g. 30 days) unless legal hold.

```bash
# Example encrypt before handoff (org-standard tools may differ)
# age -r RECIPIENT_KEY -o export.tar.age export.tar
```

### 7. Audit and close

- Update DSAR ticket with manifest checksums, systems contacted, delivery proof.
- File gaps (system not queryable) as remediation stories.
- Metrics: time-to-complete, reopen rate, error rate.

## System coverage matrix

| System | Query method | Owner | SLA |
| --- | --- | --- | --- |
| Primary Postgres | SQL job | Platform | 2d |
| Object storage user media | prefix list | Media | 2d |
| SaaS CRM | Vendor export API | Sales ops | 5d |
| Logs / SIEM | Policy-limited | SecOps | Privacy call |

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Identity | Verified by privacy ops | Export on email guess |
| Scope | Data map driven | “Select * from all DBs” |
| Format | JSON/CSV + manifest | Phone photo of screen |
| Security | Encrypted share + audit | Slack DM of zip |
| Secrets | Stripped | Include API keys “found in account” |
| Legal | Counsel exceptions applied | Engineer decides legal scope alone |

## Output Checklist

- [ ] Request id, identity verification, authorization recorded
- [ ] Systems of record list completed
- [ ] Extractions with counts/checksums (no PII in ticket body)
- [ ] Machine-readable package + manifest
- [ ] Third-party PII redaction reviewed
- [ ] Secure delivery completed and logged
- [ ] Working copies deletion scheduled
- [ ] Gaps filed for unqueryable systems
- [ ] Privacy ops closure confirmation
- [ ] `code-quality-standards` applied if export tooling shipped

## Rules

- No export without validated request and identity assurance.
- Not legal advice; escalate edge cases to DPO/counsel.
- Minimize copies; encrypt; audit.
- Never paste export contents into chat logs.
- Erasure is a separate skill (`gdpr-right-to-erasure-eng`).
