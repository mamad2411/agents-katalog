---
title: Commercial Clause Extraction
description: NLP-based extraction of contract clauses with reference tagging, obligation identification, and structured output for commercial compliance
version: 1.0
frequency_percent: 75.0
success_rate_percent: 90.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/00250-commercial/commercial-clause-extraction
gigabrain_tags: disciplines, 00250-commercial, commercial-clause-extraction, nlp, contract-analysis, clause-identification
openstinger_context: contract-analysis, clause-management, commercial-compliance
last_updated: 2026-04-01
related_docs:
  - docs_construct_ai/disciplines/00250-commercial/agent-data/domain-knowledge/00250_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/00250-commercial/agent-data/prompts/00250_AI-NATIVE-COMMERCIAL-PROMPT.md
  - docs_construct_ai/disciplines/00250-commercial/agent-data/domain-knowledge/00250_GLOSSARY.MD
related_skills:
  - commercial-contract-interpretation
  - commercial-obligation-tracking
---

# Commercial Clause Extraction

## Overview

Perform NLP-based clause extraction from commercial contracts, identifying, classifying, and tagging all contractual clauses with source references for downstream commercial operations.

**Announce at start:** "I'm using the commercial-clause-extraction skill to extract clauses from the contract document."

## When to Use This Skill

**Trigger Conditions:**
- New contract received requiring clause analysis
- Contract amendment requires clause re-evaluation
- Obligation tracking needs clause source identification
- Compliance monitoring requires clause reference verification

**Prerequisites:**
- Contract document available in text or searchable PDF format
- Contract metadata available (contract number, parties, effective date)
- Clause index or clause dictionary available for reference

## Step-by-Step Procedure

### Step 1: Document Preparation

1. Verify contract document is complete (all pages, annexures, schedules)
2. Convert to text format if necessary (OCR for scanned documents)
3. Identify document sections and structure
4. Verify contract metadata (contract number, parties, dates)

### Step 2: Clause Boundary Detection

Apply clause boundary detection:
1. Identify section headers and numbering
2. Detect paragraph-level clause boundaries
3. Identify sub-clause hierarchy (numbering patterns: 1, 1.1, 1.1.1)
4. Flag ambiguous boundaries for manual review

### Step 3: Clause Classification

Classify each identified clause into commercial clause categories:

| Clause Category | Examples | Extraction Priority |
|----------------|----------|---------------------|
| Payment Terms | Pricing, invoicing, payment schedule, currency, taxes | Critical |
| Liquidated Damages | LD rates, caps, trigger conditions | Critical |
| Termination | Termination rights, notice periods, consequences | Critical |
| Variation/Change | Change procedures, variation order process, rate adjustments | Critical |
| Dispute Resolution | Arbitration, adjudication, jurisdiction, escalation procedure | Critical |
| Force Majeure | Force majeure definition, notice requirements, consequences | High |
| Indemnity/Liability | Indemnification, liability caps, exclusions | High |
| Performance | Performance standards, deliverables, acceptance criteria | High |
| Confidentiality | Confidentiality obligations, duration, exceptions | Medium |
| Insurance | Required insurance, coverage amounts, certificates | Medium |
| Warranties/Guarantees | Warranty periods, guarantee terms, defect liability | Medium |
| Governing Law | Jurisdiction, applicable law, language | Medium |
| Subcontracting | Subcontracting rights, consent requirements | Medium |
| Compliance | Regulatory compliance, anti-corruption, environmental | Medium |

### Step 4: Clause Extraction

For each classified clause:
1. Extract clause text verbatim
2. Record source location (section number, page number, paragraph)
3. Identify key data elements within clause:
   - Monetary values (amounts, rates, caps)
   - Time periods (notice periods, durations, deadlines)
   - Conditions (triggers, requirements, exceptions)
   - References (to other clauses, documents, standards)
4. Tag with clause category and classification confidence

### Step 5: Reference and Cross-Reference Tagging

1. Identify intra-contract references (clause-to-clause references)
2. Identify external references (standards, regulations, other documents)
3. Create cross-reference map for all identified references
4. Flag broken or missing references for manual review

### Step 6: Obligation Identification

1. From payment terms: Extract payment obligations, amounts, schedules
2. From performance clauses: Extract deliverable obligations, standards
3. From compliance clauses: Extract regulatory obligations
4. From termination clauses: Extract notice obligations, handover obligations
5. Tag each obligation with source clause reference

### Step 7: Structured Output

Generate structured JSON output:
```json
{
  "contract_id": "CON-2026-XXXX",
  "extraction_date": "2026-04-01T20:00:00Z",
  "total_clauses_extracted": 0,
  "clauses": [
    {
      "clause_id": "CL-001",
      "section_number": "12.3",
      "clause_category": "Payment Terms",
      "clause_text": "...",
      "page_number": 0,
      "key_elements": {
        "monetary_values": [],
        "time_periods": [],
        "conditions": [],
        "references": []
      },
      "obligations_identified": ["OBL-001", "OBL-002"],
      "confidence": 0.95
    }
  ],
  "cross_references": [],
  "summary": {
    "by_category": {},
    "obligations_count": 0,
    "critical_clauses_count": 0
  }
}
```

### Step 8: Validation and Quality Check

1. Verify all clause categories are represented
2. Check that critical clauses (payment, LD, termination) are extracted
3. Validate that cross-references resolve within the document
4. Confirm obligation extraction completeness
5. Flag low-confidence extractions (<80%) for human review

## Success Criteria

- [ ] All contract sections processed
- [ ] Critical clause categories identified (payment, LD, termination, variation, dispute)
- [ ] Each clause tagged with source location (section, page)
- [ ] Key elements extracted (monetary values, time periods, conditions, references)
- [ ] Cross-reference map generated
- [ ] Obligations identified and linked to source clauses
- [ ] Low-confidence extractions flagged for human review
- [ ] Structured output generated and validated

## Common Pitfalls

1. **Scan Quality Issues** — Poor OCR quality leads to misidentified clause boundaries. Always verify OCR accuracy before extraction.
2. **Annexure/Schedule Separation** — Clauses in annexures and schedules are often missed. Ensure all document components are processed.
3. **Cross-Reference Resolution** — Many contracts reference clauses that don't exist or use informal references. Flag all unresolved references.
4. **Hidden Obligations** — Some obligations are embedded within non-obligation clauses (e.g., notice requirements in dispute clauses). Review thoroughly.
5. **Version Mismatch** — Ensure the document being processed matches the executed version. Check dates, signatures, and amendment references.

## Cross-References

### Related Skills
- `commercial-contract-interpretation` — Clause interpretation and meaning analysis
- `commercial-obligation-tracking` — Obligation lifecycle management
- `commercial-compliance-monitoring` — Compliance against extracted clauses

### Related Agents
- `COM-007` Commercial Clause Extraction Agent — Primary agent
- `COM-002` Commercial Contract Administrator Agent — Supporting agent