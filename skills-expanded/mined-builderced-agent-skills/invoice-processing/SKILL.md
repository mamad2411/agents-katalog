---
name: invoice-processing
description: Extract, validate, and classify invoices from PDF, Factur-X, and UBL formats. Multi-country support with field mapping and anomaly detection.
version: "1.0.0"
last-updated: "2026-04-17"
model_tested: "claude-sonnet-4-6"
category: documents
platforms: [claude-code, codex, gemini-cli, cursor, copilot, windsurf, cline]
language: en
geo_relevance: [global, fr, eu]
priority: medium
dependencies:
  mcp: []
  skills: [fr-facturation-electronique]
  apis: []
  data: []
update_sources:
  - url: "https://fnfe-mpe.org/factur-x/"
    check_frequency: "yearly"
    last_checked: "2026-04-21"
license: MIT
---

# Invoice Processing

## When to Use

- Extracting data from PDF invoices
- Validating Factur-X or UBL structured invoices
- Classifying invoices by type, vendor, or account
- Detecting anomalies (duplicates, unusual amounts, missing fields)
- Mapping invoice fields to accounting entries

## Extraction Pipeline

```
1. INPUT: PDF / Factur-X / UBL / image
2. DETECT FORMAT: structured XML embedded? → parse directly
   No XML? → OCR + field extraction
3. EXTRACT FIELDS: map to canonical schema
4. VALIDATE: required fields, amounts, VAT consistency
5. CLASSIFY: expense category, accounting account, vendor
6. OUTPUT: structured JSON + confidence scores
```

## Canonical Invoice Schema

```json
{
  "invoice_number": "FA-2026-042",
  "invoice_date": "2026-04-15",
  "due_date": "2026-05-15",
  "supplier": {
    "name": "Fournisseur SAS",
    "tax_id": "FR12345678901",
    "address": "12 rue Example, 75001 Paris"
  },
  "buyer": {
    "name": "Client SARL",
    "tax_id": "FR98765432109"
  },
  "lines": [
    {
      "description": "Prestation conseil",
      "quantity": 5,
      "unit_price": 200.00,
      "vat_rate": 20.0,
      "line_total": 1000.00
    }
  ],
  "subtotal": 1000.00,
  "vat_amount": 200.00,
  "total": 1200.00,
  "currency": "EUR",
  "payment_terms": "30 jours net"
}
```

## Validation Rules

| Rule | Check | Severity |
|------|-------|----------|
| Required fields | invoice_number, date, supplier, total | Critical |
| Math consistency | sum(lines) = subtotal, subtotal + VAT = total | Critical |
| VAT rate validity | Rate matches country standard rates | Warning |
| Duplicate detection | Same number + supplier + amount | Critical |
| Date logic | due_date >= invoice_date | Warning |
| Currency | Valid ISO 4217 code | Warning |

## Anomaly Detection

| Anomaly | Signal | Action |
|---------|--------|--------|
| Duplicate invoice | Same number + supplier + amount +/- 5% | Block, flag for review |
| Round amount | Total is exact round number (1000, 5000) | Flag (common in fraud) |
| Weekend/holiday date | Invoice dated on non-business day | Flag |
| Unusual amount | > 3 standard deviations from vendor average | Flag for review |
| Missing VAT | Taxable transaction with 0% VAT | Flag, check exemption |

## What This Skill Does NOT Do

- Does not perform OCR (uses existing OCR output or structured XML)
- Does not approve or pay invoices (validation and extraction only)
- Does not connect to ERP systems (outputs structured data)
- Does not handle tax compliance (see `fr-comptabilite`)
