---
title: Commercial Quotation Analysis
description: Compare supplier quotations against BOQ benchmarks, budget rates, and evaluate commercial and technical compliance
version: 1.0
frequency_percent: 45.0
success_rate_percent: 92.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/00250-commercial/commercial-quotation-analysis
gigabrain_tags: disciplines, 00250-commercial, commercial-quotation-analysis, tender-evaluation
openstinger_context: tender-evaluation, supplier-selection
last_updated: 2026-04-01
related_docs:
  - docs_construct_ai/disciplines/00250-commercial/agent-data/domain-knowledge/00250_DOMAIN-KNOWLEDGE.MD
related_skills:
  - commercial-supplier-evaluation
  - commercial-tender-document-preparation
---

# Commercial Quotation Analysis

## Overview

Compare supplier quotations against BOQ benchmarks and budget rates, evaluating commercial and technical compliance to recommend the best value supplier.

**Announce at start:** "I'm using the commercial-quotation-analysis skill to analyze supplier quotations."

## When to Use This Skill

**Trigger Conditions:**
- Multiple quotations received for same scope
- Tender responses due for evaluation
- Budget verification needed for supplier pricing
- Single-source pricing justification

**Prerequisites:**
- Quotations received from all invited suppliers
- BOQ or scope of work available
- Budget rates approved
- Evaluation criteria defined

## Step-by-Step Procedure

### Step 1: Quotation Receipt Validation

1. Verify quotations are responsive to RFQ/RFP requirements
2. Check all suppliers quoted on same basis
3. Note late or incomplete submissions
4. Record quotation validity periods

### Step 2: Price Normalisation

1. Extract pricing from each quotation
2. Normalize to common unit of measure
3. Include all costs (delivery, taxes, duties, ancillary)
4. Convert to common currency if international
5. Adjust for commercial terms differences

### Step 3: BOQ Comparison

For each supplier quote:
1. Compare unit prices against BOQ budget rates
2. Calculate variance percentage (over/under budget)
3. Flag items exceeding 10% budget variance
4. Check quantities match BOQ/MTO exactly
5. Verify all BOQ line items quoted

### Step 4: Technical Compliance Check

1. Verify technical specifications meet requirements
2. Check proposed alternatives are equivalent
3. Verify delivery schedule meets project needs
4. Check warranty and guarantee terms
5. Verify quality certifications included

### Step 5: Supplier Capability Assessment

1. Check supplier pre-qualification status
2. Review past performance record
3. Verify financial stability
4. Assess production capacity and lead-time capability
5. Review HSSE compliance history

### Step 6: Generate Comparison Sheet

Create structured comparison:
- Side-by-side unit price comparison
- Total evaluated price per supplier
- Variance from budget
- Technical compliance score
- Delivery schedule rating
- Risk assessment rating

### Step 7: Recommendation

1. Calculate lowest evaluated compliant supplier
2. Check recommendation within budget
3. Provide award recommendation
4. Document justification and risks

## Success Criteria

- [ ] All valid quotations processed
- [ ] Prices normalized to common basis
- [ ] BOQ comparison completed for all line items
- [ ] Technical compliance assessed
- [ ] Supplier capability reviewed
- [ ] Comparison sheet generated
- [ ] Award recommendation provided with justification

## Common Pitfalls

1. **Uncomparable Bases** — Suppliers quote on different bases. Always normalize before comparing.
2. **Missing Quantities** — Suppliers may not quote all BOQ items. Flag omissions.
3. **Excluded Costs** — Look for exclusions that add to the final cost.
4. **Invalid Quotations** — Check quotation validity hasn't expired.

## Cross-References

### Related Skills
- `commercial-supplier-evaluation` — Supplier capability assessment
- `commercial-tender-document-preparation` — Tender document generation

### Related Agents
- `COM-003` Commercial Procurement Specialist Agent — Primary agent
- `COM-006` Commercial Cost Controller Agent — Supporting agent