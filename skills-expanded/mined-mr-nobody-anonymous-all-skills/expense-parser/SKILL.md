---
name: expense-parser
description: Extract normalized vendor, date, currency, tax, line-item, and total data from receipts or invoices.
category: documents
aliases:
- expense
- receipt
- invoice
- parse
- finance
triggers:
- Parse this receipt
- Extract expense data
- Scan invoice
- Process expense
keywords:
- expense
- receipt
- invoice
- ocr
- parse
- finance
- accounting
dependencies:
- optional:ocr
risk: low
version: 1.0.0
source: custom
enabled: true
capabilities:
- expense-parser
- documents
inputs:
- task
- context
outputs:
- result
- report
lifecycle: enabled
author: Mr-Nobody-Anonymous
tags:
- documents
- expense
- invoice
- ocr
- parser
- receipt
compatibility:
  claude-code: '>=1.0'
  skillhub: '*'
  cursor: '>=0.40'
  codex: '*'
network_access: false
filesystem_access: read
credential_access: false
destructive_operations: false
---

# Expense Parser

## Purpose
Extract structured expense data from receipts and invoices including vendor name,
date, currency, tax amounts, line items, and totals. The skill normalizes data
for easy import into expense tracking systems.

## When to Use
- Processing receipt photos for expense reports
- Extracting invoice data for accounting
- Batch processing multiple receipts
- Digitizing paper documents

## When NOT to Use
- For legal or audit-verified document processing
- When original documents are required
- For real-time point-of-sale integration

## Capabilities
- OCR from images (receipt photos, scanned documents)
- Vendor name extraction and normalization
- Date parsing (multiple formats)
- Currency detection and conversion
- Tax amount identification
- Line item extraction
- Total calculation and verification
- Export to CSV, JSON, or expense system formats

## Inputs
- `source` (required) — receipt/invoice image or PDF
- `format` (optional) — json, csv, expense-format
- `currency` (optional) — native currency for conversion
- `extract_line_items` (optional, default: true)

## Workflow
1. **Receive** — Accept image or document
2. **OCR** — Extract text using OCR engine
3. **Parse** — Identify and extract fields
4. **Normalize** — Standardize dates, currencies, vendors
5. **Verify** — Cross-check totals and taxes
6. **Export** — Output in requested format

## Tools
- OCR engine (Tesseract, cloud vision, etc.)
- Receipt parsing library

## Examples
**User:** "Parse this receipt: [upload image]"
**Response:**
```
Parsed Receipt:
- Vendor: Starbucks Coffee
- Date: Feb 9, 2026
- Location: Seattle, WA
- Items:
  - Latte (Grande) - $5.45
  - Blueberry Muffin - $3.95
- Subtotal: $9.40
- Tax (10.1%): $0.95
- Total: $10.35
- Payment: Card ending 4242

Export: expense-2026-02-09-starbucks.json
Confidence: 98%
```

## Safety
- Never store original receipt images beyond processing
- Verify extracted data matches source
- Flag low-confidence extractions for review
- Handle sensitive payment info carefully (mask card numbers)

## Source
Auto-generated from openclawskills.net description.

## Notes
Maintained as part of canonical documents category.
