---
title: Commercial Contract Drafting
description: Draft commercial contract documents with structured data injection, clause verification, and approval routing
version: 1.0
frequency_percent: 60.0
success_rate_percent: 85.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/00250-commercial/commercial-contract-drafting
gigabrain_tags: disciplines, 00250-commercial, commercial-contract-drafting, contract-formation
openstinger_context: contract-drafting, commercial-documentation
last_updated: 2026-04-01
related_docs:
  - docs_construct_ai/disciplines/00250-commercial/agent-data/domain-knowledge/00250_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/00250-commercial/agent-data/prompts/00250_AI-NATIVE-COMMERCIAL-PROMPT.md
related_skills:
  - commercial-clause-extraction
  - commercial-approval-routing
---

# Commercial Contract Drafting

## Overview

Draft commercial contract documents including subcontracts, service agreements, supply agreements, and variations using structured data injection, clause library verification, and approval routing integration.

**Announce at start:** "I'm using the commercial-contract-drafting skill to generate a commercial contract document."

## When to Use This Skill

**Trigger Conditions:**
- New contract/subcontract required
- Contract variation or amendment
- Standard form contract customization
- Response to counterparty draft contract

**Prerequisites:**
- Scope of work/services defined
- Pricing and payment terms agreed
- Party information available
- Approved clause library accessible

## Step-by-Step Procedure

### Step 1: Select Contract Template

Choose appropriate contract template:
| Template Type | Use Case |
|---------------|----------|
| Subcontract Agreement | Subcontracting work packages |
| Supply Agreement | Long-term material supply |
| Service Agreement | Service procurement |
| Consulting Agreement | Professional services |
| Variation Agreement | Contract modifications |
| Amendment | Contract changes |

### Step 2: Insert Parties and Project Information

1. Insert buyer/supplier details with correct legal names
2. Insert project name, project number, WBS reference
3. Insert relevant contract/PO numbers
4. Insert effective date and execution date

### Step 3: Insert Scope and Commercial Terms

1. Insert scope of work/services from approved scope document
2. Insert pricing schedule with amounts, currency, taxes
3. Insert payment terms and schedule
4. Insert performance standards and deliverables
5. Insert contract duration and milestones

### Step 4: Select and Insert Standard Clauses

From clause library, select and insert:
1. Definitions and interpretation
2. Payment and invoicing
3. Performance and deliverables
4. Variations and changes
5. Liquidated damages and penalties
6. Termination rights
7. Dispute resolution
8. Governing law
9. Insurance and bonds
10. Confidentiality
11. Force majeure

### Step 5: Customize Special Conditions

1. Insert project-specific conditions
2. Insert counterparty-specific conditions
3. Insert negotiated amendments
4. Verify no conflicting clauses exist

### Step 6: Route for Approval

1. Generate contract cover sheet
2. Route through approval workflow based on contract value
3. Track approval comments and incorporate changes
4. Obtain final approval signatures

## Success Criteria

- [ ] Correct contract template selected
- [ ] All party and project information accurate
- [ ] Scope of work/services complete and clear
- [ ] Commercial terms match agreed terms
- [ ] All standard clauses included from clause library
- [ ] Special conditions customized for project
- [ ] No conflicting clauses present
- [ ] Cover sheet generated
- [ ] Approval workflow completed

## Common Pitfalls

1. **Wrong Template** — Using the wrong contract template creates fundamental issues. Match template to contract type.
2. **Missing Scope Detail** — Vague scope leads to disputes. Incorporate detailed scope of work with measurable deliverables.
3. **Inconsistent Pricing** — Pricing in contract must match approved budget and quotation. Verify before drafting.
4. **Missing Special Conditions** — Project-specific conditions (site requirements, regulatory compliance) must be captured.

## Cross-References

### Related Skills
- `commercial-clause-extraction` — Clause library management
- `commercial-approval-routing` — Contract approval workflow
- `commercial-contract-amendment` — Post-execution amendments

### Related Agents
- `COM-002` Commercial Contract Administrator Agent — Primary agent
- `COM-013` Commercial Document Generation Agent — Supporting agent