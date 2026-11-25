---
title: Procurement 5-Phase Order Creation
description: Execute the 5-phase procurement order creation wizard (Basic Info → Template Selection → Discipline Details → Approval Routing → Review & Submit) with validation gates at each phase
version: 1.0
frequency_percent: 70.0
success_rate_percent: 95.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/01900_procurement/procurement-5phase-order-creation
gigabrain_tags: disciplines, 01900_procurement, order-creation, 5-phase-wizard, validation-gates, procurement
openstinger_context: 01900_procurement_operations, skill-execution
last_updated: 2026-04-02
related_docs:
  - docs_construct_ai/disciplines/01900_procurement/agent-data/domain-knowledge/1900_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/01900_procurement/agent-data/domain-knowledge/1900_GLOSSARY.MD
  - docs_construct_ai/disciplines/01900_procurement/agent-data/prompts/01900_AI-NATIVE-PROCUREMENT-OPERATIONS-PROMPT.md
---

# Procurement 5-Phase Order Creation

## Overview
Execute the 5-phase procurement order creation wizard with structured validation gates at each phase to ensure data completeness, compliance, and proper approval routing.

**Announce at start:** "I'm using the procurement-5phase-order-creation skill for order processing."

## When to Use This Skill
**Trigger Conditions:** New procurement order request received requiring formal PO, WO, or Service Order creation

**Prerequisites:**
- Procurement domain knowledge available (1900_DOMAIN-KNOWLEDGE.MD, Part 8)
- BOQ/MTO data for quantity verification
- Approved vendor list accessible
- Budget data available for the relevant cost center/WBS
- User has appropriate creation authority

## Phase 1: Basic Information Capture

### Objective
Capture fundamental order identity and context.

### Required Fields
| Field | Validation Rule |
|-------|----------------|
| Order Title | Required, max 200 chars |
| Requesting Department | Must be valid project department |
| Cost Center / WBS | Must be valid cost allocation code |
| Order Type | Required: PO, WO, or Service Order |
| Priority | Required: Low, Normal, High, Urgent |
| Required On-Site Date | Must be >= today + minimum lead time |
| Discipline(s) | At least one: Civil, Structural, MEP, Process, Instrumentation, Electrical |

### Phase 1 Gate
**Cannot proceed without:** Order Title, Department, Cost Center, Order Type, Required On-Site Date

## Phase 2: Template Selection

### Objective
Apply order templates to pre-fill standard fields based on order type and discipline.

### Template Categories
- **Material Templates:** Structural steel, rebar, cable, pipe → standard specs, units, incoterms
- **Equipment Templates:** Transformers, pumps, valves → FAT requirements, warranty terms
- **Service Templates:** Inspection, maintenance → standard rates, billing methods
- **Work Order Templates:** Earthworks, concrete, welding → safety requirements, sign-off
- **Consumable Templates:** PPE, welding rods → pack sizes, approved vendors

### Provenance Tag
All template values tagged: `{source: "template_library", template_id: "<id>", overridden: <bool>}`

### Phase 2 Gate
**Cannot proceed without:** Template selected OR custom order marked with justification

## Phase 3: Discipline-Specific Details

### Objective
Capture detailed line items with discipline-specific specifications and provenance tracking.

### Line Item Structure
- Line Number (auto-incremented)
- Material/Service Code
- Description (template-generated or custom)
- Quantity (validated: materials ±5%, equipment exact)
- Unit of Measure (EA, M, KG, TON, L, SET, LOT)
- Unit Price (from quotation or budget, currency-tagged)
- Line Total (auto-calculated)
- Delivery Schedule
- Technical Attachments
- Provenance: `{source: "BOQ_v3" | "MTO_dwg_rev4" | "quotation_ref_Q-XXX"}`

### Validation at Phase 3
- Quantities match BOQ/MTO within tolerance
- Unit prices within budget or quotation-referenced
- At least one line item with complete data
- Total order value calculated

### Phase 3 Gate
**Cannot proceed without:** At least one complete line item, total value calculated

## Phase 4: Approval Routing

### Objective
Determine and display approval chain based on order value and type.

### USD Approval Matrix
| Order Value | Approval Chain | SLA |
|-------------|---------------|-----|
| < $25,000 | Procurement Officer | 4 hours |
| $25,000 – $100,000 | Procurement Manager + Project Manager | 24 hours |
| $100,000 – $500,000 | Above + Finance Manager | 48 hours |
| > $500,000 | Above + Executive Sponsor | 72 hours |
| Single-Source | Above + Commercial/Legal | 5 business days |

### ZAR Approval Matrix
| Order Value (ZAR) | Approval Chain |
|--------------------|----------------|
| < R500,000 | Procurement Officer |
| R500,000 – R2,000,000 | Procurement Manager + Project Manager |
| R2,000,000 – R10,000,000 | Above + Finance Manager |
| > R10,000,000 | Above + Executive approval |

### Phase 4 Gate
**Cannot proceed without:** Approval chain determined, authority confirmed

## Phase 5: Review & Submit

### Objective
Final validation, summary display, and submission confirmation.

### Pre-Submission Checklist
- [ ] All required fields populated
- [ ] Line item quantities match BOQ/MTO within tolerance
- [ ] Unit prices within budget or quotation-referenced
- [ ] Delivery dates achievable based on lead times
- [ ] Technical specifications attached
- [ ] Approval authority confirmed
- [ ] Budget availability confirmed
- [ ] Provenance sourced for all values

### On Submit Actions
1. Record order with status = PENDING_APPROVAL
2. Create audit trail entry
3. Trigger notification to first approver
4. Generate order reference number

## Success Criteria
- [ ] All 5 phases completed without gate failures
- [ ] All validation checks passed
- [ ] Approval chain correctly determined
- [ ] Order submitted with complete data
- [ ] Audit trail entry created
- [ ] Notifications dispatched to approvers
- [ ] Order reference generated and communicated

## Common Pitfalls
1. **Missing Cost Center** — Budget validation fails without valid WBS
2. **Template Override Without Justification** — Audit trail incomplete
3. **Quantity Tolerance Exceeded** — Must escalate for engineering confirmation
4. **Expired Quotation Reference** — Check validity dates before using prices
5. **Wrong Currency** — Match quotation/contract currency exactly

## Cross-References
### Related Skills
- procurement-document-generation (PO generation post-approval)
- procurement-vendor-management (supplier selection)
- procurement-records-audit-trail (audit logging)

### Related Agents
- **Primary:** Procurement Officer — Order creation execution
- **Supporting:** Procurement Coordinator — Data gathering and filing
- **Oversight:** Procurement Manager — Approval authority, escalation point

### Related Domain Knowledge
- 1900_DOMAIN-KNOWLEDGE.MD Part 8: 5-Phase Order Creation Architecture
- 1900_DOMAIN-KNOWLEDGE.MD Part 11: Approval Routing & HITL Integration