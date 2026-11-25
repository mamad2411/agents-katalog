---
name: data-privacy-retention
description: Engineers privacy into systems that store personal data - data inventory and PII classification, minimization, encryption and field-level encryption with a KMS, pseudonymization, access control and audit, retention and deletion jobs, erasure and access requests across every copy, PII-free logs, masked test data, and GDPR basics. Use when adding fields that hold personal data, designing retention or deletion, handling a data subject request, copying production data to test, or reviewing logs and analytics for PII. Not legal advice.
license: MIT
---

# Data Privacy and Retention

Personal data you don't collect can't leak, and data you delete on schedule can't be breached later. Know where every piece of personal data lives, keep it only as long as it has a purpose, and make deletion work across every copy, not just the main table.

**This skill is engineering guidance, not legal advice.** Laws differ by country and sector, and the right retention periods and legal bases are decisions for the user's privacy, legal or data protection team. Say this to the user whenever a decision depends on the law, and involve those people.

## When to use

- Adding tables, columns, events or log fields that hold personal data.
- Designing retention periods and deletion jobs.
- Implementing or running a data subject request (access, export, correction, erasure).
- Copying production data into test, staging, analytics or a vendor tool.
- Reviewing logs, traces, error reports and analytics events for personal data.

Not for: application security controls in general (use security-audit), threat analysis (use threat-modeling), or backups as such (use postgres-operations).

## Workflow

1. **Inventory**: list every place personal data is stored or sent, using the template in [references/inventory-and-erasure.md](references/inventory-and-erasure.md).
2. **Classify** each field (table below) and tag it where the schema lives.
3. **Minimize**: remove fields with no clear purpose; store less precise values where they're enough.
4. **Protect**: encryption, access control and audit, matched to the class.
5. **Set retention** per data category with the user's privacy/legal owner, and implement it as scheduled deletion.
6. **Make requests work**: access/export and erasure across every location in the inventory.
7. **Keep personal data out of logs, traces, error reports and test environments.**
8. **Verify**: tests for deletion and export, and a periodic re-check of the inventory.

## Classify

| Class | Examples | Minimum handling |
|---|---|---|
| Personal data | Name, email, phone, postal address, IP address, device and cookie IDs, account IDs linked to a person | Access control, retention period, included in erasure and export |
| Sensitive / special category | Health, biometrics, genetic data, religion, sexual orientation, political opinions, precise location, government IDs | Above, plus field-level encryption, stricter access and audit, often extra legal requirements |
| Payment card data | Card numbers, CVV | Don't store it. Use the payment provider's tokens (keeps you out of most PCI DSS scope) |
| Credentials and secrets | Passwords, API keys, tokens | Hash passwords (see security-audit); secrets belong in a secrets manager, never in data tables or logs |
| Not personal | Aggregates that can't be traced to a person | Normal handling (but small groups can re-identify people) |

Tag classification where engineers will see it, for example PostgreSQL column comments (`COMMENT ON COLUMN users.email IS 'pii:contact';`), schema annotations in the ORM, or a data catalog. Add a CI check or code review rule: new columns must have a classification.

## Minimize

- Don't collect fields "in case we need them". Each field needs a purpose the user can state.
- Store what the feature needs: a birth year or age band instead of a full date of birth, a country instead of an address, a truncated IP instead of the full one.
- Avoid free-text fields where users will type personal data you can't find later; if needed, include them in erasure.
- Don't copy personal data into new systems (search, analytics, data lake, vendor tools) without adding them to the inventory.

## Protect

- **In transit**: TLS for every connection, including internal service-to-service and database connections.
- **At rest**: storage or disk encryption. It protects against lost disks and snapshots, not against someone with application or database access.
- **Field-level (application-level) encryption** for the most sensitive fields: encrypt in the application before writing, using envelope encryption (a data key encrypts the field; a key in a KMS encrypts the data key). Rotate keys on a schedule and support re-encryption.
- **Crypto-shredding**: with one data key per user or tenant, deleting that key makes all of their encrypted data unreadable, including copies in backups.
- **Lookups on encrypted fields**: store a keyed hash (HMAC with a secret key) of the normalized value next to the ciphertext and query on that. A plain unsalted hash of an email or phone number is not protection; such values are easy to guess and brute-force.
- **Pseudonymization** (replacing identifiers with tokens or IDs, mapping kept elsewhere) reduces risk, but under GDPR pseudonymized data is still personal data. **Anonymization** must be irreversible; it is harder than it looks, so don't claim it without review.
- **Access**: least-privilege roles, no shared admin accounts, row-level security for multi-tenant data, just-in-time access to production, and audit logs for reads of sensitive data.

## Logs, traces, errors and analytics

- Log IDs, not people: `user_id=123`, not the email, name, address or request body.
- Use structured logging with an allowlist of fields, plus redaction for known patterns (emails, tokens, card-like numbers) as a safety net.
- Configure scrubbing in error trackers and APM tools, and don't attach full request bodies by default.
- Analytics events: send pseudonymous IDs and only the properties the analysis needs; respect consent where it is required.
- Give logs and traces short retention periods; they are copies of personal data too.

## Retention and deletion

- Define a retention period per data category with the privacy/legal owner (for example: inactive accounts, support tickets, raw event logs, invoices). Some data must be kept for a legal minimum (tax records); other data must be deleted after a maximum.
- Implement retention as **scheduled jobs**, not manual cleanups:
  - batched, idempotent and resumable (see the pattern in the reference);
  - with a **dry-run mode** that reports what would be deleted;
  - logging counts, not the deleted personal data;
  - monitored, with an alert when a run fails or deletes far more than usual.
- For time-based data in PostgreSQL, partition by time and drop old partitions; this is far cheaper than large `DELETE`s.
- Soft delete is not deletion. If you soft delete for an undo window, hard delete or anonymize when the window ends.
- Legal holds override deletion: the job must skip records under hold.
- **Before running any deletion job against production for the first time, or any bulk delete by hand, show the user the dry-run counts and get explicit confirmation.**

## Data subject requests

| Request | Engineering task |
|---|---|
| Access / export (portability) | Collect the person's data from every inventory location and export it in a machine-readable format (JSON or CSV) |
| Rectification | Update the data in the source of truth and propagate to copies |
| Erasure | Delete or anonymize in every location, except data the law requires you to keep (then restrict access to it) |
| Restriction / objection | Flag the record so processing for the given purpose stops |

Erasure must reach **every copy**: primary database (replicas follow), caches, search indexes, data warehouse and lake, files in object storage, logs, analytics and product tools, email and CRM tools, and third-party processors (via their deletion APIs). Backups usually can't be edited: make sure they expire within a defined period, and keep a deletion ledger (IDs only) so deletions are re-applied if a backup is ever restored. The full runbook is in [references/inventory-and-erasure.md](references/inventory-and-erasure.md).

Verify the requester's identity before acting on any request, and record what was done.

## Test and non-production data

- Don't copy raw production personal data into dev, test, staging or demos.
- Prefer synthetic data from factories (see database-testing). When realistic data is needed, mask it: replace names, emails, phones and addresses with fake but valid-format values, keep referential integrity (the same input maps to the same fake value), and scrub free text.
- Masked copies still go in the inventory, with their own access control and retention.

## GDPR basics (EU and UK GDPR)

- Every processing purpose needs a **lawful basis**: consent, contract, legal obligation, vital interests, public task, or legitimate interests.
- Principles that drive engineering: purpose limitation, data minimization, accuracy, storage limitation, integrity and confidentiality.
- **Data subject rights** include access, rectification, erasure, restriction, portability and objection. Requests generally must be answered within one month (extendable in some cases).
- **Personal data breaches** must be reported to the supervisory authority without undue delay and, where feasible, within 72 hours of becoming aware of them, unless the breach is unlikely to result in a risk to people's rights and freedoms; the affected people must also be told when the risk is high. Engineering's part: be able to tell quickly what data and whose was affected.
- Processors (vendors handling data for you) need data processing agreements; transfers outside the EU/UK have extra rules; high-risk processing may need a data protection impact assessment.

Other laws differ (for example the California CCPA/CPRA, Brazil's LGPD, Canada's PIPEDA, India's DPDP Act), as do sector rules such as HIPAA for US health data and PCI DSS for card data. Confirm with the user's privacy or legal team which ones apply.

## Anti-patterns

- **No inventory**: erasure requests miss the search index, the warehouse and the CRM.
- **Personal data in logs and error reports**, kept for years.
- **Raw production dumps in dev and test.**
- **"We'll add deletion later"**: data accumulates forever and every copy multiplies the cost of deleting it.
- **Plain hashes of emails or phone numbers called anonymization.**
- **Deletion jobs without dry run, counts or monitoring.**
- **Treating soft delete as deletion.**
- **Making legal calls in code** (retention periods, lawful basis) without the privacy or legal owner.

## Done when

- Every personal-data location is in the inventory, with class, purpose, owner and retention.
- New personal-data fields are classified and reviewed.
- Sensitive fields are encrypted at field level, with keys in a KMS; access is least-privilege and audited.
- Retention runs as monitored, dry-run-capable scheduled jobs that the user confirmed before the first production run.
- Export and erasure work end to end across every inventory location, with tests.
- Logs, traces and non-production environments contain no raw personal data.
- Legal decisions are confirmed by the user's privacy or legal team.

## References

- [references/inventory-and-erasure.md](references/inventory-and-erasure.md) — read when building the data inventory, implementing a retention job, or handling an erasure or export request: inventory template, batched deletion pattern and erasure runbook.
