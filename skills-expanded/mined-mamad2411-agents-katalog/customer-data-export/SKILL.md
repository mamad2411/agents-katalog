---
name: customer-data-export
enabled: true
description: |
  Use when performing customer data export — template for handling customer data
  export requests (data portability). Covers request validation, data source
  identification, extraction and assembly, format standardization, secure
  delivery, verification, and audit trail maintenance to fulfill data subject
  access requests compliantly.
required_connections:
  - prefix: aws
    label: "AWS (or cloud provider)"
config_fields:
  - key: customer_id
    label: "Customer/Subject ID"
    required: true
    placeholder: "e.g., CUST-12345"
  - key: request_type
    label: "Request Type"
    required: true
    placeholder: "e.g., DSAR (data subject access), portability, deletion verification"
  - key: regulation
    label: "Applicable Regulation"
    required: false
    placeholder: "e.g., GDPR Art. 20, CCPA"
features:
  - COMPLIANCE
  - PRIVACY
---

# Customer Data Export Skill

Process data export for customer **{{ customer_id }}** — request type: **{{ request_type }}** under **{{ regulation }}**.

## Workflow

### Phase 1 — Request Validation

```
REQUEST DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Request ID: ___
[ ] Customer ID: {{ customer_id }}
[ ] Request type: {{ request_type }}
[ ] Regulation: {{ regulation }}
[ ] Date received: ___
[ ] Response deadline: ___ (regulatory: ___ days)
[ ] Identity verified: [ ] YES — method: ___
[ ] Request scope:
    [ ] All personal data
    [ ] Specific data categories: ___
    [ ] Specific date range: ___
```

### Phase 2 — Data Source Identification

```
DATA SOURCE MAP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Data sources containing customer data:
    System              | Data Type        | Volume  | Owner
    ____________________|__________________|_________|______
                        |                  |         |
                        |                  |         |
                        |                  |         |

[ ] Third-party systems with customer data:
    - ___: contact for retrieval: ___
    - ___: contact for retrieval: ___
[ ] Data excluded from export (with justification):
    - ___: reason: ___
    - ___: reason: ___
```

### Phase 3 — Data Extraction

```
EXTRACTION CHECKLIST
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Profile data extracted: [ ] YES
[ ] Transaction/order history extracted: [ ] YES
[ ] Communication history extracted: [ ] YES
[ ] Activity/usage logs extracted: [ ] YES
[ ] Preferences/settings extracted: [ ] YES
[ ] User-generated content extracted: [ ] YES
[ ] Third-party data retrieved: [ ] YES
[ ] Derived/inferred data included: [ ] YES  [ ] NO (justification: ___)

DATA CLEANING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Other customers' data removed from export
[ ] Internal-only fields excluded
[ ] Trade secrets / proprietary data excluded (if applicable)
[ ] Data de-identified where required
```

### Phase 4 — Assembly and Format

```
EXPORT ASSEMBLY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Export format:
    [ ] JSON (machine-readable)
    [ ] CSV (tabular data)
    [ ] PDF (human-readable summary)
    [ ] Combined package (all formats)
[ ] File structure:
    export-{{ customer_id }}/
      profile.json
      transactions.csv
      communications.json
      activity.json
      content/
      summary.pdf
[ ] Total export size: ___ MB
[ ] Export package encrypted: [ ] YES — method: ___
[ ] Checksum generated: ___
```

### Phase 5 — Secure Delivery

```
DELIVERY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Delivery method (choose one):
[ ] Secure download link (time-limited: ___ hours)
[ ] Encrypted email attachment
[ ] Self-service portal download
[ ] Physical media (for large exports)

[ ] Delivery executed — timestamp: ___
[ ] Delivery confirmation received: [ ] YES
[ ] Download link expiration: ___
[ ] Export data purged from staging after delivery: [ ] YES
```

### Phase 6 — Audit Trail

```
AUDIT RECORD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[ ] Request received: ___
[ ] Identity verified: ___
[ ] Data extracted: ___
[ ] Export delivered: ___
[ ] Total processing time: ___ days (deadline: ___ days)
[ ] Deadline met: [ ] YES  [ ] NO (reason: ___)
[ ] Audit record stored: [ ] YES — retention: ___ years
[ ] Customer notified of completion: [ ] YES
```

## Counter-Rationalizations

| Shortcut | Counter | Why |
|----------|---------|-----|
| "We can skip some steps for this case" | Adapt the workflow steps, don't skip them | Skipped steps are where incidents and oversights originate |
| "The user seems to already know what to do" | Complete all workflow phases with the user | The workflow catches blind spots that experience alone misses |
| "This is a minor case, full process is overkill" | Scale the process down, don't turn it off | Minor cases become major when unstructured; the process scales, not disappears |
| "I'll fill in the details later" | Complete each section before moving on | Deferred details are forgotten; real-time capture is more accurate |
| "The template output isn't necessary" | Always produce the structured output format | Structured output enables comparison, audit trails, and handoff to other teams |

## Output Format

Produce a data export fulfillment report with:
1. **Request summary** (customer, type, regulation, timeline)
2. **Data sources** (systems queried, data categories included)
3. **Export contents** (file listing, format, size)
4. **Delivery confirmation** (method, timestamp, verification)
5. **Audit trail** (complete timeline from request to fulfillment)
