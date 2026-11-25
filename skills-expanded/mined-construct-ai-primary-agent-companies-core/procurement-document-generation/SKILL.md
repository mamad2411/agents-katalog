---
title: Procurement Document Generation
description: Generate structured procurement documents (POs, RFQs, contracts, supplier evaluations, NCRs, tenders) using template engine with structured data injection, provenance tracking, and multi-format export
version: 1.0
frequency_percent: 80.0
success_rate_percent: 94.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/procurement-document-generation
gigabrain_tags: disciplines, 01900_procurement, document-generation, template-engineering, multi-format-export, provenance-tracking, ai-native-operations
openstinger_context: procurement-document-generation, automated-documentation
last_updated: 2026-03-31
related_docs:
  - docs_construct_ai/disciplines/01900_procurement/agent-data/domain-knowledge/1900_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/01900_procurement/agent-data/prompts/01900_AI-NATIVE-PROCUREMENT-OPERATIONS-PROMPT.md
  - docs_construct_ai/disciplines/01900_procurement/agent-data/domain-knowledge/1900_GLOSSARY.MD
  - docs_construct_ai/disciplines/01900_procurement/workflow_docs/1900_CREATE_PROCUREMENT_ORDER_WORKFLOW.MD
related_skills:
  - pre-task-assessment-readiness
  - workflow-implementation
  - procurement-data-extraction
  - procurement-order-management
---

# Procurement Document Generation

## Overview

Generate structured procurement documents using a template engine pattern: templates with placeholders are populated with validated structured data from procurement systems (ERP, supplier database, order management). Supports multi-format export (PDF, DOCX, structured JSON, Excel) with provenance tracking on all populated values.

**Announce at start:** "I'm using the procurement-document-generation skill to create a procurement document from template with structured data injection."

## When to Use This Skill

**Trigger Conditions:**
- Generating a Purchase Order from approved requisition
- Creating an RFQ for supplier solicitation
- Generating a contract from negotiated terms
- Creating a supplier evaluation report
- Generating a Non-Conformance Report (NCR)
- Tender document generation
- Contract close-out documentation

**Prerequisites:**
- Template exists for target document type
- Source data extracted and validated (via `procurement-data-extraction`)
- Data provenance tags present on all source values
- Document recipient/audience identified

## Step-by-Step Procedure

### Step 1: Template Selection

Select appropriate template based on document type and complexity:

| Document Type | Complexity | Template Selection |
|---------------|-----------|-------------------|
| Purchase Order | Simple | Standard PO template with company header, line items, delivery terms, approval block |
| Purchase Order | Complex | Extended PO template with technical specifications, appendices, multi-discipline review |
| RFQ | Standard | Standard RFQ template with scope, quantities, submission deadline, evaluation criteria |
| RFQ | Complex | Extended RFQ with technical specifications, drawings, site conditions, contract terms |
| Contract | Any | Contract template with standard clauses, special conditions, pricing schedule |
| NCR | Any | NCR template with defect description, specification reference, corrective action request |
| Supplier Evaluation | Standard | Evaluation summary template with scoring, tier assignment, recommendation |
| Tender Document | Any | Tender package with invitation, instructions, evaluation criteria, draft contract |

### Step 2: Data Assembly

Assemble data from validated source systems:

| Data Category | Source System | Validation Required |
|---------------|---------------|-------------------|
| Supplier details | Supplier database | Supplier active, approved, current qualification tier |
| Order line items | Approved requisition / BOQ | Quantities match MTO, prices match quotation |
| Pricing data | Quotation / approved rates | Currency, exchange rate date, validity period |
| Delivery terms | Order configuration | Incoterms valid, delivery location exists |
| Approval information | Approval workflow | Approver roles assigned, authority limits valid |
| Technical specifications | Engineering documents | Current revision, approved by discipline lead |

**Data injection format:**
```json
{
  "template_name": "purchase_order_complex",
  "data_source": "validated_requisition_R-2026-0142",
  "injection_points": {
    "po_number": "PO-2026-0089",
    "supplier_name": "SteelWorks Ltd",
    "supplier_address": "123 Industrial Way, Johannesburg",
    "order_date": "2026-03-31",
    "delivery_date": "2026-07-15",
    "line_items": [
      {
        "item_code": "ST-W310-001",
        "description": "Structural W310 sections, Grade S355JR",
        "quantity": 340,
        "uom": "tonnes",
        "unit_price": 18500,
        "currency": "ZAR",
        "total_line": 6290000
      }
    ],
    "incoterms": "DAP Site C, Gate 3",
    "payment_terms": "30% advance, 70% on delivery",
    "approved_by": "John Smith, Procurement Manager"
  }
}
```

### Step 3: Template Rendering

Render template with injected data:

**Template Design Principles:**
1. **Structured Data Injection, Not Raw Generation** — All values come from validated sources, not LLM-generated text
2. **Provenance Tracking** — Every injected value carries source reference (e.g., `{source: "quotation_Q-2026-142", item: "concrete_C30"}`)
3. **Conditional Logic** — Optional sections added/omitted based on data availability (e.g., "if no warranty period, omit warranty clause")
4. **Regulatory Accuracy** — Current codes, standards, and regulations referenced
5. **Multi-Language Support** — Documents support all languages represented in supply chain
6. **Human Readable with Data Export** — Documents exportable as structured data for analytics

**Rendering Pipeline:**
```
TEMPLATE SELECTION (document type, complexity)
    ↓
DATA INJECTION (structured data sources → placeholder mapping)
    ↓
CONDITIONAL LOGIC (add/omit sections based on data)
    ↓
QUALITY VALIDATION (completeness, accuracy, consistency)
    ↓
DRAFT DOCUMENT (formatted output)
    ↓
PROVENANCE TAGGING (all values tagged with source)
    ↓
OUTPUT GENERATION (PDF, DOCX, JSON, Excel)
```

### Step 4: Quality Validation

Validate generated document before output:

| Validation Check | Description | Action on Failure |
|-----------------|-------------|-------------------|
| Completeness | All mandatory placeholders filled | Reject document, flag missing data |
| Data Consistency | Calculations correct (totals = sum of lines) | Reject document, flag calculation error |
| Cross-Reference | All referenced documents exist (PO refs requisition) | Reject document, flag broken reference |
| Terminology | Correct terms used (incoterms, UOM, currency) | Flag for correction |
| Formatting | Page numbers, headers, footers, page breaks | Flag for correction |

### Step 5: Multi-Format Export

Generate output in requested formats:

| Format | Use Case | Characteristics |
|--------|----------|-----------------|
| PDF | Distribution to suppliers, approval, archival | Print-ready, locked formatting, watermarked if draft |
| DOCX | Internal review, editing | Editable, tracked changes enabled |
| Structured JSON | System integration, analytics | All values with provenance, machine-readable |
| Excel | Line item analysis, comparison | Tabular data, formulas for calculations |

### Step 6: Version Control & Distribution

Manage document lifecycle:

1. **Version Number** — Generate version (v1.0 for first, v1.1 for revision)
2. **Audit Trail** — Log document generation: who, when, data sources, template version
3. **Distribution** — Route to stakeholders per approval workflow
4. **Archival** — Store in document management system with metadata tags

## Success Criteria

- [ ] Correct template selected for document type and complexity
- [ ] All data injected from validated sources (no fabricated values)
- [ ] All calculations correct (totals, taxes, currency conversions)
- [ ] All cross-references valid and resolvable
- [ ] Document passes all quality validation checks
- [ ] Provenance tags present on all populated values
- [ ] Output generated in requested format(s)
- [ ] Document logged to audit trail with version control

## Common Pitfalls

1. **Generating Text for Data Fields** — Never let the LLM generate numbers for quantities, prices, or dates. All values must come from validated source data.
2. **Missing Provenance** — If a value doesn't have a source reference, the document cannot be used for audit, dispute resolution, or quality checks.
3. **Ignoring Conditional Logic** — Not all documents need all sections. Use conditional logic to omit sections that don't apply (e.g., no warranty for off-the-shelf purchases).
4. **Skipping Quality Validation** — Always run completeness and accuracy checks before output. A document with errors distributed to a supplier damages credibility and causes rework.
5. **Forgetting Version Control** — Always version documents. An unversioned revision creates confusion about which version is current.

## Cross-References

### Related Skills
- `procurement-data-extraction` — Provides validated source data for injection
- `procurement-order-management` — Consumes generated PO documents
- `sow-generation` — Specialized document generation for scope of work
- `procurement-compliance` — Validates document compliance requirements

### Related Agents
- `Contract Administration Specialist` (DomainForge) — Contract document generation
- `Procurement Strategy Specialist` (DomainForge) — RFQ and tender document generation
- `Procurement Analytics Specialist` (DomainForge) — Document export for analytics

## Example Usage

**Scenario:** Generate Purchase Order PO-2026-0089 for 340t structural steel

1. **Template:** Select purchase_order_complex template (complexity: standard with technical specs)
2. **Data Assembly:** Load approved requisition R-2026-0142, quotation Q-2026-142
3. **Data Injection:** Populate all template fields from validated sources
4. **Quality Validation:** Verify calculations (340t × R18,500 = R6,290,000), check all references
5. **Output:** Generate PDF for supplier distribution, JSON for system integration
6. **Version Control:** Log as v1.0, route for approval, archive with metadata

## Performance Metrics

**Target Performance:**
- Template rendering accuracy: >99% (all placeholders correctly populated)
- Data accuracy: >99.9% (exact match with source data)
- Document generation time: <10 seconds (simple), <60 seconds (complex with multiple appendices)
- Review rejection rate: <5% of documents require revision after generation