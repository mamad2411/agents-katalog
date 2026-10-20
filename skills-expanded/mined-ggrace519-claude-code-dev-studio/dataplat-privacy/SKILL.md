---
name: dataplat-privacy
description: Warehouse-side privacy specialist. Owns PII classification, masking / tokenization, deletion propagation (DSAR / right-to-erasure), retention enforcement, and access control on sensitive columns. Auto-invoked when classifying data, enforcing retention, or processing erasure requests.
---

# Data Platform Privacy

PII in the warehouse is a regulator's first stop. Classification, masking, and
deletion are legal obligations with deadlines and audit trails — GDPR erasure
runs on a one-month clock (Art. 12: extendable by two months for complex
requests), CCPA on 45 days — not best-effort features.

## When to reach for this

- A new source or column lands and needs PII classification before merge
- Implementing or reviewing masking, tokenization, or row/column access policies
- Building DSAR / right-to-erasure propagation across marts, derived tables, and backups
- Defining retention TTLs per data class or auditing sensitive-column access

## Principles

1. **Classify at ingest.** Every new column gets a class (direct identifier,
   quasi-identifier, sensitive, financial) before the pipeline merges — retrofit
   classification never catches up.
2. **Mask in views, not by trust.** Raw PII tables get no direct grants; access
   goes through restricted views or native masking policies (Snowflake dynamic
   data masking, BigQuery policy tags) keyed to roles.
3. **Deletion is a pipeline, not a query.** Erasure walks lineage from the
   source identifier through every derived mart, is idempotent (re-runnable),
   and ends with a verification query proving zero remaining rows per table.
4. **Retention as code.** Each class maps to a TTL enforced by a scheduled job
   (partition drop or delete), with the job's run history as the audit evidence.
5. **Tokenize where joins must survive.** Salted/keyed tokenization (HMAC, vault
   lookup) preserves joinability; plain unsalted hashes of low-entropy values
   like email or phone are reversible by dictionary and don't count as
   anonymization.
6. **Audit every privileged read.** Sensitive-column access is logged with who,
   what, and when, and reviewed on a cadence — access logs are the first thing a
   regulator or incident response asks for.

## Classification → default policy

| Class | Examples | Default policy |
|---|---|---|
| Direct identifier | email, phone, full name, gov ID | tokenize; raw visible only to a break-glass role |
| Quasi-identifier | ZIP, birth date, IP, device ID | mask/generalize in views (truncate ZIP, year-only DOB) |
| Sensitive (special category) | health, biometrics, orientation, religion | restricted schema, explicit grant + audit, shortest TTL |
| Financial / payment | PAN fragments, bank accounts | never land PAN/CVV; last-4 + provider token only |
| Non-PII | product events, aggregates | standard access; still subject to retention |

## Erasure-request checklist

- [ ] Identity resolved to all entity keys (user ID, emails, device IDs, tokens)
- [ ] Lineage walked: every table/mart holding those keys enumerated, including ML feature tables
- [ ] Deletes executed in dependency order; job idempotent and logged
- [ ] Verification query per table returns zero rows; result archived as evidence
- [ ] Backups: deletion re-applied or key destroyed per documented backup policy
- [ ] Downstream syncs (reverse ETL, BI extracts, caches) purged or expired
- [ ] Completion recorded with timestamps against the regulatory deadline

## Pitfalls

- Deletion that hits the source table but not derived marts, snapshots, or
  dbt-built aggregates — lineage gaps are where erasure fails audits
- Restoring a backup silently resurrects erased subjects (no re-deletion step)
- Unsalted `md5(email)` treated as anonymized — it's pseudonymous at best
- Masking applied in the BI tool while warehouse roles can still query raw columns
- Quasi-identifier combinations (ZIP + DOB + gender) re-identifying "anonymized"
  exports; aggregate or generalize before sharing

---
*Related: `common-privacy` (app-layer consent, DSAR intake — the warehouse
fulfills what the app layer receives), `dataplat-quality` (contracts carrying
classification tags), `dataplat-etl` (deletion pipelines) · domain agent:
`dataplat-architect` (governance posture) · output/ADR format:
`playbook-conventions`*
