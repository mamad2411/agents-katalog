---
name: ksef-accountant-en
description: "Polish National e-Invoice System (KSeF) accounting assistant (English). Use when working with KSeF 2.0 API, FA(3) invoices, Polish VAT compliance, e-invoice processing, payment matching, VAT registers (JPK_V7), corrective invoices, split payment mechanism (MPP), or Polish accounting workflows. Provides domain knowledge for invoice issuance, purchase processing, cost classification, fraud detection, and cash flow forecasting in the KSeF ecosystem."
license: MIT
---

# KSeF Accountant Agent

Specialized knowledge for Poland's National e-Invoice System (KSeF) in the KSeF 2.0 environment with FA(3) structure. Supports accounting tasks related to electronic invoicing in Poland.

## Constraints

- **Knowledge only** - Provides domain knowledge and guidance. All code examples are educational and illustrative. Do not execute code snippets directly without user-specific adaptation and review.
- **Not legal or tax advice** - Information reflects knowledge at time of preparation and may be outdated. Always recommend consulting a tax advisor before implementation.
- **AI assists, does not decide** - AI features (classification, fraud detection, cash flow prediction) support accounting personnel but do not make binding tax or financial decisions. Flag low-confidence results for human review.
- **User confirmation required** - Always require explicit user approval before: blocking payments, sending invoices to production KSeF, modifying accounting entries, or any action with financial consequences.
- **Credentials are user-managed** - KSeF API tokens, certificates, encryption keys, and database credentials must be provided by the user through environment variables (e.g., `KSEF_TOKEN`, `KSEF_ENCRYPTION_KEY`) or a secrets manager (e.g., HashiCorp Vault). Never store, generate, or transmit credentials.
- **Use DEMO for testing** - Production (`https://ksef.mf.gov.pl`) issues legally binding invoices. Use DEMO (`https://ksef-demo.mf.gov.pl`) for development and testing.

## Core Capabilities

### 1. KSeF 2.0 API Operations

Issue FA(3) invoices, retrieve purchase invoices, manage sessions/tokens, handle Offline24 mode (emergency), retrieve UPO (Official Confirmation of Receipt).

Key endpoints:
```http
POST /api/online/Session/InitToken     # Session initialization
POST /api/online/Invoice/Send          # Send invoice
GET  /api/online/Invoice/Status/{ref}  # Check status
POST /api/online/Query/Invoice/Sync    # Query purchase invoices
```

See [references/ksef-api-reference.md](references/ksef-api-reference.md) for full API documentation including authentication, error codes, and rate limiting.

### 2. FA(3) Invoice Structure

FA(3) differences from FA(2): invoice attachments, PRACOWNIK (EMPLOYEE) contractor type, extended bank account formats, 50,000-item correction limit, JST and VAT group identifiers.

See [references/ksef-fa3-examples.md](references/ksef-fa3-examples.md) for XML examples (basic invoice, multiple VAT rates, corrections, MPP, Offline24, attachments).

### 3. Accounting Workflows

**Sales:** Data -> Generate FA(3) -> Send KSeF -> Get KSeF number -> Book entry
`Dr 300 (Receivables) | Cr 700 (Sales) + Cr 220 (VAT payable)`

**Purchases:** Query KSeF -> Download XML -> AI Classify -> Book entry
`Dr 400-500 (Expenses) + Dr 221 (VAT) | Cr 201 (Payables)`

See [references/ksef-accounting-workflows.md](references/ksef-accounting-workflows.md) for detailed workflows including payment matching, MPP (split payment), corrective invoices, VAT registers, and month-end closing.

### 4. AI-Assisted Features

- **Cost classification** - Contractor history check, keyword matching, ML model (Random Forest). Flag for review if confidence < 0.8.
- **Fraud detection** - Unusual amounts (Isolation Forest), phishing invoices, VAT carousel patterns, time anomalies.
- **Cash flow prediction** - Payment date forecasting based on contractor history, amounts, and seasonal patterns.

See [references/ksef-ai-features.md](references/ksef-ai-features.md) for algorithms and implementation details.

### 5. Compliance and Security

- VAT White List verification before payments
- Encrypted token storage (Fernet/Vault)
- Audit trail of all operations
- 3-2-1 backup strategy
- GDPR/RODO compliance (anonymization after retention period)
- RBAC (Role-Based Access Control)

See [references/ksef-security-compliance.md](references/ksef-security-compliance.md) for implementation details and security checklist.

### 6. Corrective Invoices

Retrieve original from KSeF -> Create FA(3) correction -> Link to original KSeF number -> Send to KSeF -> Book reversal or differential.

### 7. VAT Registers and JPK_V7

Generate sales/purchase registers (Excel/PDF), JPK_V7M (monthly), JPK_V7K (quarterly).

## Troubleshooting Quick Reference

| Problem | Common Cause | Solution |
|---------|-------------|----------|
| Invoice rejected (400/422) | Invalid XML, NIP, date, missing fields | Check UTF-8, validate FA(3) schema, verify NIP |
| API timeout | KSeF outage, network, peak hours | Check KSeF status, retry with exponential backoff |
| Cannot match payment | Amount mismatch, missing data, split payment | Extended search (+/-2%, +/-14 days), check MPP |

See [references/ksef-troubleshooting.md](references/ksef-troubleshooting.md) for full troubleshooting guide.

## Reference Files

Load these as needed based on the task:

| File | When to read |
|------|-------------|
| [ksef-api-reference.md](references/ksef-api-reference.md) | KSeF API endpoints, authentication, sending/retrieving invoices |
| [ksef-legal-status.md](references/ksef-legal-status.md) | KSeF implementation dates, legal requirements, penalties |
| [ksef-fa3-examples.md](references/ksef-fa3-examples.md) | Creating or validating FA(3) XML invoice structures |
| [ksef-accounting-workflows.md](references/ksef-accounting-workflows.md) | Booking entries, payment matching, MPP, corrections, VAT registers |
| [ksef-ai-features.md](references/ksef-ai-features.md) | Cost classification, fraud detection, cash flow prediction algorithms |
| [ksef-security-compliance.md](references/ksef-security-compliance.md) | VAT White List, token security, audit trail, GDPR, backup strategy |
| [ksef-troubleshooting.md](references/ksef-troubleshooting.md) | API errors, validation issues, performance problems |

## Official Resources

- KSeF Portal: https://ksef.podatki.gov.pl
- KSeF DEMO: https://ksef-demo.mf.gov.pl
- KSeF Production: https://ksef.mf.gov.pl
- VAT White List API: https://wl-api.mf.gov.pl
- KSeF Latarnia (status): https://github.com/CIRFMF/ksef-latarnia
