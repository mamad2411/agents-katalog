---
title: Procurement Data Extraction
description: Extract, validate, and tag structured data from procurement documents including RFQs, invoices, delivery notes, certificates, and order confirmations with provenance tracking
version: 1.0
frequency_percent: 85.0
success_rate_percent: 92.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/procurement-data-extraction
gigabrain_tags: disciplines, 01900_procurement, data-extraction, schema-validation, provenance-tracking, document-processing, ai-native-operations
openstinger_context: procurement-data-extraction, structured-data-pipeline
last_updated: 2026-03-31
related_docs:
  - docs_construct_ai/disciplines/01900_procurement/agent-data/domain-knowledge/1900_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/01900_procurement/agent-data/prompts/01900_AI-NATIVE-PROCUREMENT-OPERATIONS-PROMPT.md
  - docs_construct_ai/disciplines/01900_procurement/agent-data/domain-knowledge/1900_GLOSSARY.MD
  - docs_construct_ai/disciplines/01900_procurement/workflow_docs/1900_PROCUREMENT_INPUT_AGENT_WORKFLOW.MD
related_skills:
  - pre-task-assessment-readiness
  - workflow-implementation
  - procurement-document-generation
---

# Procurement Data Extraction

## Overview

Extract structured data from procurement documents (RFQs, invoices, delivery notes, certificates, order confirmations, BOQs, MTOs), validate against schemas, and tag all values with provenance information. This skill provides the foundational data extraction pipeline that all downstream procurement processes depend on.

**Announce at start:** "I'm using the procurement-data-extraction skill to extract and validate structured data from procurement documents."

## When to Use This Skill

**Trigger Conditions:**
- Processing a new procurement document (RFQ, invoice, delivery note, certificate, order confirmation)
- Converting scanned procurement documents to structured JSON
- Validating data extracted from ERP exports or supplier submissions
- Tagging procurement data with source provenance for audit trail

**Prerequisites:**
- Schema definition exists for target document type
- Source document accessible (file upload, scanned image, ERP export)
- Validation rules defined for required fields, value ranges, and relationships

## Step-by-Step Procedure

### Step 1: Document Type Identification

Identify the document type using classification criteria:

| Document Indicator | Classified As |
|-------------------|---------------|
| Supplier quote with pricing, validity period, delivery terms | RFQ Response / Quotation |
| Request for pricing with quantity, specifications | RFQ (Request for Quotation) |
| Supplier invoice with PO reference, line items, tax | Invoice |
| Warehouse receipt confirming delivery receipt | GRN (Goods Receipt Note) |
| Supplier acknowledgment confirming order | Order Confirmation |
| Material quantity list from drawings | BOQ / MTO |
| Test results from inspection or lab | Quality Certificate / Test Certificate |
| Shipping documentation | Bill of Lading / Delivery Note |

### Step 2: Schema Selection

Load the appropriate extraction schema based on document type:

**RFQ/Quotation Schema:**
```json
{
  "document_type": "rfq_quotation",
  "required_fields": ["quote_number", "supplier_name", "validity_date", "currency", "line_items[]"],
  "line_item_fields": ["item_code", "description", "quantity", "uom", "unit_price", "delivery_weeks"],
  "validation_rules": {
    "validity_date": "must_be_future",
    "quantity": "numeric_positive",
    "unit_price": "numeric_positive",
    "uom": "standard_units_list"
  }
}
```

**Invoice Schema:**
```json
{
  "document_type": "invoice",
  "required_fields": ["invoice_number", "invoice_date", "po_reference", "supplier_name", "total_amount", "currency", "tax_amount", "line_items[]"],
  "line_item_fields": ["po_line_reference", "description", "quantity_received", "uom", "unit_price", "line_total"],
  "validation_rules": {
    "invoice_number": "unique_format",
    "invoice_date": "must_be_past",
    "total_amount": "sum_of_line_items_plus_tax",
    "po_reference": "must_match_existing_po"
  }
}
```

### Step 3: Data Extraction

Extract data from document using appropriate method:

| Document Format | Extraction Method |
|-----------------|-------------------|
| Structured (CSV, JSON, XML) | Direct field mapping with schema validation |
| PDF (text-based) | Text parsing with regex patterns, table extraction |
| PDF (scanned/image) | OCR processing → text extraction → structured mapping |
| Image (Photo) | OCR with template matching, manual confirmation for critical fields |
| Email | Header parsing + body text extraction for key values |

**Extraction Rules:**
1. Extract all required fields — no missing required fields allowed
2. Preserve original values — do not round, truncate, or modify extracted values
3. Handle missing data gracefully — mark as "unknown" rather than guessing
4. Extract units of measure separately from quantities
5. Extract dates in ISO format (YYYY-MM-DD) regardless of source format
6. Extract currency codes (ISO 4217) and confirm they match quotation

### Step 4: Schema Validation

Validate extracted data against schema:

| Validation Type | Check | Action on Failure |
|----------------|-------|-------------------|
| Required Fields | All required fields present | Flag as incomplete, request missing values |
| Data Types | Numeric fields are numeric, dates are parseable | Correct format or flag for manual review |
| Value Ranges | Quantities positive, prices within tolerance, dates valid | Flag as potential error for review |
| Cross-References | PO reference exists in system, supplier is approved | Flag as cross-reference failure |
| Calculations | Line totals = quantity × unit price, total = sum of lines | Flag calculation discrepancy |

### Step 5: Provenance Tagging

Tag every extracted value with source provenance:

```json
{
  "value": "340.00",
  "provenance": {
    "source_document": "quotation_Q-2026-142.pdf",
    "source_field": "line_item[2].quantity",
    "extracted_by": "procurement-data-extraction skill",
    "extracted_at": "2026-03-31T14:00:00Z",
    "confidence": 0.98,
    "requires_verification": false
  }
}
```

**Provenance Requirements:**
- All extracted values must carry source document reference
- All monetary values must carry currency code and exchange rate source
- All dates must carry source format and parsed format
- All quantitative values (quantities, weights, volumes) must carry UOM
- Confidence score based on extraction method quality

### Step 6: Output Generation

Generate structured JSON output:

```json
{
  "extraction_result": {
    "document_type": "rfq_quotation",
    "source_document": "Q-2026-142.pdf",
    "extraction_status": "complete_with_warnings",
    "extracted_at": "2026-03-31T14:00:00Z",
    "data": { /* validated structured data */ },
    "provenance": { /* provenance map for all values */ },
    "validation_results": {
      "passed": 23,
      "failed": 1,
      "warnings": 1,
      "issues": [
        {
          "type": "warning",
          "field": "delivery_weeks",
          "message": "Lead time 14 weeks exceeds typical 12-week benchmark",
          "action": "flag_for_review"
        }
      ]
    }
  }
}
```

## Success Criteria

- [ ] Document type correctly classified
- [ ] All required fields extracted (no missing required data)
- [ ] All validations passed or flagged with clear issue description
- [ ] Provenance tags present on all extracted values
- [ ] Missing data marked as "unknown" (not fabricated)
- [ ] Output in structured JSON format ready for downstream processing
- [ ] Confidence score calculated for overall extraction quality

## Common Pitfalls

1. **Fabricating Missing Values** — Never invent values for missing fields. Always mark as "unknown" and flag for manual input.
2. **Rounding Without Warning** — Extract precision exactly as shown in source. Do not round quantities or prices. If rounding is required downstream, log it as a transformation.
3. **Skipping Provenance** — Every value must carry provenance. This is not optional. Downstream processes (audit, dispute resolution, quality checks) depend on knowing data origin.
4. **Ignoring Units** — "340" without a unit is meaningless. Always extract and validate UOM separately. "340 tonnes" ≠ "340 kg".
5. **Accepting Expired Quotes** — Always check quotation validity date. An expired quotation requires re-quotation or confirmation that pricing is still valid.

## Cross-References

### Related Skills
- `procurement-document-generation` — Consumes extracted data for document generation
- `procurement-order-management` — Uses extracted data for order validation
- `supplier-evaluation` — Uses extracted performance data from delivery notes and invoices
- `procurement-analyics` — Uses extracted data for spend analytics

### Related Agents
- `Procurement Strategy Specialist` (DomainForge) — Document classification validation
- `Contract Administration Specialist` (DomainForge) — Quotation terms verification
- `Procurement Analytics Specialist` (DomainForge) — Data aggregation from multiple extractions

## Example Usage

**Scenario:** Extract data from supplier quotation Q-2026-142 for 340t structural steel

1. **Identify:** Document is a supplier quotation
2. **Schema:** Load rfq_quotation schema
3. **Extract:** Parse PDF, extract quote number, supplier, dates, 3 line items
4. **Validate:** All required fields present, prices positive, delivery dates future
5. **Provenance:** Tag each value with source file, field, extraction confidence
6. **Output:** JSON with extraction results, 2 warnings flagged (14-week lead time, EXW incoterms)

## Performance Metrics

**Target Performance:**
- Extraction accuracy: >95% (matching manual data extraction from same document)
- Schema validation pass rate: >90% on first extraction
- Provenance coverage: 100% of extracted values with source tags
- Processing time: <30 seconds per document (simple), <3 minutes (scanned PDFs with OCR)