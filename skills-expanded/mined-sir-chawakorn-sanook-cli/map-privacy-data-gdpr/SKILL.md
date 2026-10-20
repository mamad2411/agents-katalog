---
name: map-privacy-data-gdpr
description: Implements privacy/data-protection engineering — personal-data inventory/mapping (RoPA), lawful-basis and versioned consent capture, DSAR machine-readable export and right-to-erasure cascades across derived data/logs/backups, TTL/scheduled retention purge, and PII minimization/pseudonymization — for GDPR/CCPA-style compliance.
when_to_use: A product stores personal data and needs consent capture, data export, deletion/erasure, or retention controls. Distinct from auth-jwt-session and design-authorization-model (who may access), build-audit-logging (tamper-evident action trail), and security-review (vulnerability audit).
---

## When to Use

Reach for this skill when the requirement is **what happens to a person's data**, not who may touch it:

- "A user requested their data / file a DSAR export endpoint"
- "Implement account deletion / right to be forgotten / erasure that actually removes them everywhere"
- "Record consent for marketing/analytics — granular, withdrawable, with proof"
- "We keep PII forever — add retention limits / a purge job"
- "Map where personal data lives for our DPIA / Article 30 record of processing"
- "Stop collecting/storing PII we don't need; pseudonymize the rest"

NOT this skill:
- Logging in users, sessions, OAuth, refresh rotation → **auth-jwt-session**
- Deciding which role/tenant may read a record (RBAC/ABAC/row scoping) → **design-authorization-model**
- The tamper-evident trail of *who did what* (including who ran an erasure) → **build-audit-logging**
- Hunting injection/SSRF/access-control bugs in changed code → **security-review**
- Design-level threat enumeration over a system handling PII → **threat-model-stride**
- Backup/PITR/retention *of the datastore itself* (RPO/RTO, WAL archiving) → **design-backup-dr-recovery**

## Steps

1. **Build the data inventory first — you cannot delete or export what you haven't mapped.** Produce a machine-readable record of processing (RoPA, GDPR Art. 30). One row per (data element × store). Drive everything downstream — export, erasure, retention — off this file, not off tribal knowledge.

   ```yaml
   # privacy/inventory.yaml — source of truth for DSAR + purge + DPIA
   - element: email
     category: contact          # contact | identifier | special-category | behavioral | financial
     store: postgres.users.email
     purpose: account login, transactional mail
     lawful_basis: contract     # see step 2 table
     retention: account_lifetime_plus_30d
     subject_key: users.id
     export: true
     erase: anonymize           # delete | anonymize | retain-with-basis
   - element: ip_address
     category: identifier
     store: postgres.request_logs.ip
     purpose: fraud/abuse detection
     lawful_basis: legitimate_interest
     retention: 90d
     subject_key: request_logs.user_id
     export: true
     erase: delete
   - element: clickstream
     category: behavioral
     store: bigquery.analytics.events
     purpose: product analytics
     lawful_basis: consent
     retention: 14m
     subject_key: events.user_pseudo_id    # NOT the raw user id — see step 6
     export: true
     erase: delete
   ```
   Enumerate **every** store: primary DB, replicas, search index (Elasticsearch), caches (Redis), object storage (S3 uploads), data warehouse, application logs, third-party processors (Stripe, Segment, Intercom, Sentry), and **backups**. A store missing from this file is a store your erasure silently skips — that is the #1 compliance gap.

2. **Pin a lawful basis to every element before you collect it.** No basis = you may not process it. Pick the *narrowest* basis that fits and record it in the inventory; consent is the weakest because it's revocable and must be audited.

   | Lawful basis (GDPR Art. 6) | Use for | On erasure request |
   |---|---|---|
   | **Consent** | marketing, non-essential analytics, optional cookies | must delete; consent withdrawable any time |
   | **Contract** | login email, order/shipping data, billing | retain while contract active, then purge |
   | **Legal obligation** | tax invoices, AML/KYC records | **keep** for statutory period; refuse erasure with reason |
   | **Legitimate interest** | fraud/abuse, basic security logs | keep if LIA balancing holds; honor objection |
   | **Vital / public interest** | rare; safety-of-life | document case-by-case |

   Default new fields to **no collection** until a basis is assigned. CCPA framing differs (opt-out of "sale/share", not opt-in consent) — model both as flags on the same consent record.

3. **Capture consent as granular, versioned, withdrawable, time-stamped records — never a single boolean.** A `marketing_opt_in = true` column proves nothing and can't show *which* policy version they agreed to. Append-only consent ledger:

   ```sql
   CREATE TABLE consent_records (
     id             bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
     subject_id     uuid NOT NULL,
     purpose        text NOT NULL,      -- 'marketing_email','analytics','third_party_share'
     granted        boolean NOT NULL,   -- false row = explicit withdrawal
     policy_version text NOT NULL,      -- 'privacy-policy@2026-03-01'
     source         text NOT NULL,      -- 'signup_form','preference_center','cookie_banner'
     evidence       jsonb NOT NULL,     -- {ip, user_agent, banner_choice_ids}
     created_at     timestamptz NOT NULL DEFAULT now()
   );
   CREATE INDEX ON consent_records (subject_id, purpose, created_at DESC);
   -- current state = latest row per (subject_id, purpose); NEVER UPDATE/DELETE rows
   ```
   Withdrawal is a new `granted=false` row, not a mutation — you must be able to prove the full history. Check consent at point of use (`SELECT … WHERE subject_id=$1 AND purpose=$2 ORDER BY created_at DESC LIMIT 1`), and gate consent-based processing on it. Cookie banner: no non-essential cookies/tags fire before a `granted=true` row exists.

4. **DSAR export: assemble a complete, machine-readable package keyed off the inventory.** Iterate every row with `export: true`, pull the subject's data by `subject_key`, emit structured JSON (GDPR Art. 20 portability requires machine-readable). Include data from processors via their APIs. Authenticate the requester *hard* (re-auth + verification) — handing one user's data to another is itself a breach. Respond within the statutory window (GDPR 30 days; CCPA 45). Don't include other people's PII caught in the subject's rows (e.g. recipient emails) — redact third parties.

5. **Right-to-erasure must cascade to every store, including derived data, caches, logs, and backups — or document the backup-expiry path.** A `DELETE FROM users WHERE id=…` that leaves the subject in the search index, Redis cache, analytics warehouse, and last night's snapshot is **not** erasure. Drive a cascade from the inventory's `erase:` column:

   ```python
   def erase_subject(subject_id):
       for row in inventory:                      # one source of truth
           store = connect(row.store)
           match row.erase:
               case "delete":    store.delete(row, subject_id)
               case "anonymize": store.anonymize(row, subject_id)   # see step 6
               case "retain-with-basis":
                   log_retained(subject_id, row, reason=row.lawful_basis)  # legal hold
       invalidate_cache(subject_id)               # Redis keys, CDN signed URLs
       delete_from_search_index(subject_id)       # Elasticsearch/OpenSearch
       enqueue_processor_deletions(subject_id)    # Stripe, Segment, Intercom, Sentry APIs
       add_to_suppression_list(subject_id)        # tombstone — see below
       record_erasure(subject_id)                 # write to audit log (build-audit-logging)
   ```
   **Backups can't be selectively edited** — the defensible approach is: (a) restrict restored-backup access, (b) re-apply the erasure to any data restored from backup, and (c) let backups age out under a bounded retention (e.g. 35 days), documented in your privacy policy. Maintain a **suppression/tombstone list** so a restore or a late-arriving event for an erased subject is re-deleted, not resurrected. Erasure under a legal-hold basis (tax/AML) is refused with a recorded reason, not silently ignored.

6. **Minimize and pseudonymize — the cheapest data to protect is data you don't hold.** Per element ask: do we *need* it? Don't collect optional PII "just in case". Replace direct identifiers with a per-subject pseudonym key in analytics/derived stores so erasing the key map breaks linkage (`erase: anonymize` then becomes deleting the mapping, not rewriting a warehouse). True anonymization (irreversible, no re-identification via combination) takes data **out of GDPR scope** — prefer it for analytics/ML training sets. Tokenize or keyed-hash (HMAC with a secret salt) and delete the mapping; **never** use a plain unsalted hash you call "anonymized". Drop high-cardinality quasi-identifiers (full IP → /24, exact DOB → birth year) where the purpose allows.

7. **Enforce retention with TTL or scheduled purge jobs — retention written in a policy but not enforced in code is a fiction.** Translate each `retention:` value into a real mechanism:
   - Native TTL where the store has one: MongoDB TTL index, DynamoDB TTL attribute, Redis `EXPIRE`, BigQuery partition expiration, S3 lifecycle rules, Elasticsearch ILM.
   - A scheduled job (cron / Airflow / pg_cron) that `DELETE`s rows past `created_at + retention` for stores without TTL — run daily, log counts purged, alert on zero-purged-when-expected.
   Logs and analytics are the usual offenders (PII-laden, retained forever). Cap them explicitly.

8. **Document cross-border transfers and processor agreements.** Any element flowing to a processor outside the data's region needs a transfer mechanism (SCCs / adequacy decision) and a signed DPA. List sub-processors. Record this alongside the inventory — auditors ask for it, and a new third-party integration that isn't in the list is an unmapped data egress.

## Common Errors

- **Erasure that hits the primary DB only.** The subject survives in the search index, cache, warehouse, logs, and backups. Drive deletion from the inventory across *every* store; assert absence afterward.
- **Consent as one boolean column.** Can't prove which policy version, when, or how; an `UPDATE` erases the prior state. Use an append-only versioned ledger; withdrawal is a new row.
- **No suppression list.** A backup restore or a delayed event re-creates an erased subject ("data resurrection"). Keep a tombstone list and re-apply erasure on restore/ingest.
- **Reversible "anonymization".** A plain SHA-256 of an email is re-identifiable by dictionary attack — still personal data, still in scope. Keyed-hash/tokenize and delete the mapping, or aggregate so individuals can't be singled out.
- **Treating backups as out of scope entirely.** Ignoring them fails erasure; trying to surgically edit them corrupts them. Use bounded retention + restore-time re-erasure, and document it.
- **Weak DSAR identity check.** Emailing an export to whoever asks lets an attacker harvest a victim's data. Re-authenticate and verify before export or erasure.
- **Retention policy with no enforcement job.** "We keep logs 90 days" while the table grows unbounded. Wire a TTL or a scheduled purge and verify it actually runs.
- **Logging full PII.** Request/error logs capturing emails, tokens, full bodies become an uncontrolled PII store with infinite retention. Redact at the logger; set log retention.
- **Forgetting processors.** Deleting locally but leaving the subject in Stripe/Segment/Intercom/Sentry. Call each processor's deletion API as part of the cascade.
- **Hardcoding the store list in deletion code instead of the inventory.** A new table added without touching the deletion code is silently skipped forever. Single source of truth, generated cascade.

## Verify

- **Erasure completeness:** run `erase_subject(id)`, then query **every** store in the inventory for that subject's `subject_key` → zero rows (or only anonymized/legal-hold-retained rows with a recorded reason). This is the test that catches the forgotten store; automate it per store.
- **Resurrection resistance:** restore a backup taken before an erasure (or replay a late event) → the subject is re-suppressed, not present. Suppression list is consulted on restore/ingest.
- **Export completeness:** for a seeded subject with data in N stores, the DSAR package contains all N, is valid JSON/machine-readable, and contains **no other** subject's PII.
- **Consent gate:** withdrawing consent (new `granted=false` row) stops the gated processing on the next check; granted/withdrawn history is fully reconstructable; no non-essential tag fires before consent.
- **Retention enforcement:** advance a record past its retention window (or wait/seed) → the TTL/purge job removes it on the next scheduled run; purge job logs counts and alerts on anomalies.
- **Lawful basis coverage:** every element in the inventory has a basis; legal-obligation elements correctly *survive* an erasure request with a recorded reason.
- **Minimization:** no element is collected/stored without a row in the inventory; derived/analytics stores key on a pseudonym, not the raw identifier.
- **Transfers:** every cross-border element maps to a transfer mechanism + DPA; processor list matches actual integrations.

Done = an erasure request provably removes or anonymizes the subject across every inventoried store (with backups handled by bounded retention + restore-time re-erasure and a suppression list), the DSAR export is complete and machine-readable with no third-party PII leakage, consent is versioned/withdrawable with reconstructable history, and every retention window is enforced by a TTL or scheduled purge that demonstrably runs.
