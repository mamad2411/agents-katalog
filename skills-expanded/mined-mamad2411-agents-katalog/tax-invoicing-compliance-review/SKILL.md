---
name: tax-invoicing-compliance-review
description: Design and audit tax, invoicing, receipt, VAT/GST/sales-tax, reverse charge, tax ID, billing address, subscription invoice, app-store receipt, marketplace seller invoice, credit note, refund document, and finance-support handoff flows. Use when money flows need compliant customer documents, tax metadata, jurisdiction handling, and audit evidence.
---

# Tax Invoicing Compliance Review

Use this skill to convert a risky product, operations, trust, or marketplace question into a concrete artifact with owners, gates, metrics, and recovery paths.

## Workflow

1. Identify seller of record, buyer type, jurisdiction, product type, tax collection party, invoice requirements, and finance owner.
2. Read `references/tax-invoicing-patterns.md`.
3. Map checkout data capture, tax calculation, invoice/receipt creation, refund/credit note, marketplace payouts, and support correction flow.
4. Separate consumer receipts, B2B invoices, app-store receipts, marketplace seller documents, and tax/accounting evidence.
5. Produce requirements matrix, document lifecycle, exception queue, and support/finance escalation plan.

## Guardrails

- Do not provide legal or tax advice; route jurisdiction-specific decisions to qualified owners.
- Do not promise invoices or tax treatment the seller-of-record cannot issue.
- Do not let support manually edit financial documents without audit and finance approval.
- Keep tax, invoice, payment, entitlement, and accounting states separate but reconciled.

## Output format

```text
Tax/invoice context:
Seller of record / buyer / jurisdiction:

Requirements matrix:
| Scenario | Required data | Document | Owner | Exception |
| --- | --- | --- | --- | --- |

Document lifecycle:
- <event> -> <document/status/support action>

Escalations:
- <tax/invoice issue> -> <finance/legal/support path>
```
