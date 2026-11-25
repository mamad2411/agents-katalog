---
name: data-retention-manager
description: "Data retention policy, lifecycle management, archival, secure deletion, compliance automation. Use when implementing or auditing data retention rules."
version: 1.0.0
platforms: [linux, macos]
---

# Data Retention Manager

## What It Does
Automates data retention policy enforcement across storage systems. Implements lifecycle rules for data expiration, archival, and secure deletion. Ensures compliance with regulatory requirements (GDPR, HIPAA, SOX, PCI), manages data classification tiers with appropriate retention periods, and provides audit trails for all data lifecycle events.

## Iron Laws (NEVER violate)
1. **Delete means irrecoverable** — Data past retention must be destroyed beyond recovery. No "archive forever" masquerading as deletion.
2. **Classification drives retention** — Every data class (PII, financial, operational, logs) must have a defined retention period. No "default forever."
3. **Legal hold overrides everything** — When legal hold is active, retention policies MUST NOT delete data. Deletion during legal hold = spoliation.
4. **Audit every deletion** — Every automated deletion must leave an audit trail: what was deleted, when, by which policy, and who approved the policy.

## Red Flags (STOP immediately)
- **Over-retention** — Data retained beyond policy period → compliance violation and unnecessary liability
- **Under-retention** — Data deleted before required retention period → regulatory violation
- **Legal hold bypass** — Retention policy runs while legal hold is active → potential legal consequences
- **Orphan data** — Data in unknown storage without classification or retention policy → data governance failure

## Common Rationalizations (self-deception)
- "Storage is cheap, just keep everything" → Retained data is discoverable in litigation. Every byte is potential liability.
- "We'll clean it up later" → Data accumulates exponentially. "Later" becomes "never" without automation.
- "Users won't notice if we keep data longer" → Over-retention violates GDPR data minimization principle.

## When To Use
- Implementing data retention policies for regulatory compliance
- Setting up automated data lifecycle management (archival, deletion)
- Auditing existing data retention practices
- Responding to data subject erasure requests (GDPR Right to Erasure)
- Managing data across hot/warm/cold storage tiers

## Human Partner Signals (escalate to human)
- **Legal hold activation** — Legal team requests preservation of specific data → immediate policy suspension
- **Policy conflict** — Different regulations require conflicting retention periods → legal guidance needed
- **Archive migration** — Archival format becoming obsolete → data migration decision
- **Deletion impact** — Deletion policy will remove data used by active business processes → stakeholder approval

## Pipeline
1. Classify: inventory all data stores, classify data by type and sensitivity
2. Policy: define retention periods per data class based on regulatory and business requirements
3. Implement: configure automated lifecycle rules — tiering (hot → warm → cold → delete)
4. Verify: test policies in staging — confirm data is archived/deleted as expected
5. Monitor: track policy execution, detect anomalies (data not deleted on schedule)
6. Audit: maintain deletion audit trail for compliance reporting
7. Review: quarterly policy review to ensure retention periods still match requirements

## Verification Checklist
- [ ] Every data class has a defined retention period with regulatory justification
- [ ] Automated deletion verified (data irrecoverable after policy execution)
- [ ] Legal hold mechanism tested — policies pause when hold is active
- [ ] Deletion audit trail complete with timestamps, policy references, and data identifiers
- [ ] No orphan data without classification and retention policy
- [ ] Cross-border data transfer and retention rules enforced
- [ ] Quarterly policy review scheduled and documented

## Related Skills
- `gdpr-compliance-scanner` — GDPR data minimization and right-to-erasure requirements
- `soc2-audit-prep` — Data retention as a confidentiality and privacy control
- `policy-as-code` — Retention policies encoded as automated rules
- `cloud-security-auditor` — Cloud storage lifecycle configuration audit
