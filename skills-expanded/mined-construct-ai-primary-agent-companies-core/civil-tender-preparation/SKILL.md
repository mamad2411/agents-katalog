---
title: Civil Tender Preparation
description: Assemble and manage civil engineering procurement tender packages including document compilation, compliance checking, and bid evaluation support
version: 1.0
frequency_percent: 30.0
success_rate_percent: 90.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/civil-tender-preparation
gigabrain_tags: civil-engineering, tender, procurement, bid-evaluation, procurement-packages
openstinger_context: tender-assembly, bid-management
last_updated: 2026-03-31
related_docs:
  - docs_construct_ai/disciplines/00850_civil-engineering/agent-data/domain-knowledge/00850_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/00850_civil-engineering/agent-data/domain-knowledge/00850_GLOSSARY.MD
  - docs_construct_ai/disciplines/00850_civil-engineering/agent-data/prompts/00850_CIVIL-DOCUMENTATION-WORKFLOW-PROMPT.md
related_skills:
  - pre-task-assessment-readiness
  - civil-documentation
  - civil-quantity-takeoff
  - procuring-order-management
  - supplier-evaluation
---

# Civil Tender Preparation

## Overview

Assemble and manage civil engineering procurement tender packages: compile technical documentation, verify compliance with procurement regulations, prepare evaluation criteria, and support contractor prequalification and bid evaluation. Bridges the design and procurement phases of the civil engineering workflow.

**Announce at start:** "I'm using the civil-tender-preparation skill to prepare the civil engineering tender package."

## When to Use This Skill

**Trigger Conditions:**
- Phase 4 design documentation complete and ready to compile for tender
- Procurement strategy requires tender package customization
- Addenda or tender bulletins need to be issued
- Prequalification of civil contractors required
- Bid evaluation of received tenders for civil works packages

**Prerequisites:**
- All Phase 4 cards complete (Construction Drawings, Specifications, Quantity Schedules, ITP)
- CE-PROC-001 agent or equivalent procurement capability available
- Procurement strategy approved (open tender, selective, negotiated)
- Tender type identified (lump sum, measure & value, design & build)

## Step-by-Step Procedure

### Step 1: Tender Package Compilation

**Assemble all tender documents into a coherent package:**

**Tender package contents:**
| Section | Contents | Source | Responsibility |
|---------|----------|--------|----------------|
| A | Letter of invitation and instructions to tenderers | Procurement | CE-PROC-001 |
| B | Form of tender and tender security | Procurement | CE-PROC-001 |
| C | Conditions of contract (GCC + PCC) | Procurement | CE-CONTRACT-001 |
| D | Scope of Work | SOW from civil-documentation skill | CE-DOCS-001 |
| E | Technical Specifications | Specs from civil-documentation skill | CE-DOCS-001 |
| F | Bill of Quantities | BOQ from civil-quantity-takeoff skill | CE-QS-001 |
| G | Drawings | Construction drawings from civil-documentation skill | CE-DOCS-001 |
| H | Inspection and Test Plans | ITPs from civil-documentation skill | CE-QA-001 |
| I | Evaluation criteria and score sheets | Project requirements | CE-PROC-001 |
| J | Tender submission forms and declarations | Procurement templates | CE-PROC-001 |

### Step 2: Package Completeness Verification

**Verify all required tender package components present and consistent:**

**Verification checklist:**
- [ ] All drawings referenced in specifications are included
- [ ] BOQ line items match specification requirements
- [ ] ITPs cover all construction activities in SOW
- [ ] Conditions of contract specify civil works scope correctly
- [ ] Form of tender includes all required declarations
- [ ] Evaluation criteria published to all tenderers
- [ ] Tender bulletin/addenda process defined
- [ ] Prequalification criteria (if applicable) included
- [ ] Tender security/bond requirements specified
- [ ] Submission deadline, opening date, and venue confirmed

### Step 3: Prequalification Assessment

**If selective tender, assess and shortlist qualified contractors:**

**Prequalification criteria:**
| Criterion | Weight | Assessment Method |
|-----------|--------|-------------------|
| Financial capacity | 25% | Audited accounts, bank references, annual turnover vs project value |
| Similar project experience | 25% | Project history, references, project value and complexity comparison |
| Technical capability | 20% | Key staff qualifications, plant and equipment, method statement quality |
| Safety record | 15% | LTIFR, major incidents, OHS policy, safety certifications |
| Quality management | 10% | ISO 9001 certification, QA staff qualifications, defect history |
| Local content / B-BBEE | 5% | Certification level, local employment commitments |

**Shortlist output:** 3–6 prequalified contractors for invitation to tender

### Step 4: Tender Issuance and Management

**Issue tender to contractors and manage the tender period:**

**Tender process timeline:**
| Event | Days before tender close | Responsibility |
|-------|-------------------------|----------------|
| Issue tender documents | Day -28 | CE-PROC-001 |
| Site visit (organized) | Day -21 | CE-COLLAB-001 |
| Tender briefing Q&A | Day -18 | CE-COLLAB-001 |
| Addendum 1 issued | Day -14 | CE-PROC-001 |
| Extension requests assessed | Day -10 | CE-PROC-001 |
| Tender closing | Day 0 | CE-PROC-001 |
| Tender opening (immediate) | Day 0 + 2 hours | CE-PROC-001 |

**RFI management during tender period:**
- All tenderer queries logged and tracked
- Responses issued to ALL tenderers simultaneously (fair process)
- Queries answered within 3 business days
- Addenda issued if substantive changes to tender documents

### Step 5: Bid Evaluation Support

**Support the evaluation committee in assessing received tenders:**

**Bid evaluation framework:**
```
Phase 1: Administrative Compliance Check
  [ ] Tender form completed and signed
  [ ] Tender security provided
  [ ] All declarations completed
  [ ] Tender valid period acceptable
  [ ] No material deviations from tender conditions

Phase 2: Technical Evaluation
  [ ] Method statement adequate and constructible
  [ ] Programme realistic and achievable
  [ ] Key personnel experience suitable
  [ ] Plant and equipment adequate
  [ ] Safety plan adequate
  [ ] Quality plan adequate
  [ ] Local content commitment meets minimum

Phase 3: Commercial Evaluation
  [ ] Arithmetic accuracy of BOQ pricing
  [ ] Price competitiveness vs engineer's estimate
  [ ] Payment terms acceptable
  [ ] Liquidated damages and penalties accepted
  [ ] Insurance requirements accepted
  [ ] Completeness of pricing (no missing items)

Phase 4: Clarification and Negotiation
  [ ] Clarifications received from top 2 tenderers
  [ ] Errors and omissions quantified
  [ ] Corrections applied
  [ ] Final comparison of corrected prices

Phase 5: Award Recommendation
  [ ] Lowest evaluated substantially responsive tenderer identified
  [ ] Award recommendation report prepared
  [ ] Committee approval sought
  [ ] Contract award issued
```

### Step 6: Contract Handover to Construction Support

**Transfer awarded package to Phase 5 Construction Support card:**
- Contract award documented
- All tender addenda incorporated into contract
- As-tendered drawings issued to contractor
- Pre-construction meeting scheduled
- CE-COLLAB-001 activated for construction support tracking

## Success Criteria

- [ ] Tender package complete with all required sections
- [ ] All tender components internally consistent
- [ ] Tender issued to sufficient number of qualified contractors
- [ ] Tender process fair and transparent
- [ ] Bid evaluation completed with documented recommendation
- [ ] Contract award issued to successful tenderer
- [ ] Tender period completed within planned schedule

## Common Pitfalls

1. **Incomplete Package Issuance** — Issuing tenders with missing drawings or outdated specs. Do a complete package checklist check before issuing.
2. **Unequal Treatment of Tenderers** — Issuing addenda or clarifications to only some tenderers. Always include ALL tenderers in all communications.
3. **Missing Arithmetic Check** — Not checking BOQ pricing for addition errors. The lowest price can change if a tenderer's arithmetic is wrong.
4. **Ignoring Non-Price Criteria** — Awarding on price alone. A technically superior contractor at slightly higher cost may deliver better lifecycle value.
5. **Unclear Evaluation Criteria** — Criteria not published in tender documents. Tenderers must know how they will be evaluated to submit responsive bids.

## Cross-References

### Related Skills
- `civil-documentation` — Specifications and drawings are tender inputs
- `civil-quantity-takeoff` — BOQ from quantity takeoff is a tender component
- `procurement-order-management` — General procurement workflow patterns
- `supplier-evaluation` — Prequalification uses supplier evaluation criteria
- `civil-quality-assurance` — Tender documents must include ITP requirements

### Related Agents
- `CE-PROC-001` (JS Swarm) — Primary tender processing agent
- `CE-CONTRACT-001` (JS Swarm) — Contract conditions and terms
- `CE-COLLAB-001` (JS Swarm) — Tender Q&A and contractor communication
- `CE-QS-001` (deep-agents) — BOQ and cost estimation support

## Example Usage

**Scenario:** Tender for 5km stormwater drainage package, $3.2M estimated value

1. **Package Compilation:** Tender package compiled with 6 drawings, 12 spec sections, 21-line-item BOQ, 5 ITPs, GCC/PCC contract conditions
2. **Verification:** Complete checklist confirmed. 3 addenda issued during tender period (pipe specification clarification, drawing correction, deadline extension)
3. **Prequalification:** 8 firms applied; 5 prequalified based on financial capacity and similar project experience
4. **Issuance:** Tender issued to 5 prequalified contractors on 1 March. Site visit conducted 8 March. Tender closed 28 March.
5. **Evaluation:**
   - Phase 1: 4 of 5 bids compliant (1 rejected — no tender security)
   - Phase 2: 3 of 4 technically acceptable (1 rejected — inadequate method statement)
   - Phase 3: Corrected prices — Bidder A $3.1M, Bidder B $3.4M, Bidder C $3.7M
   - Phase 5: Recommended Bidder A as lowest substantially responsive
6. **Award:** Contract issued to Bidder A on 10 April. Pre-construction meeting scheduled 18 April.

## Performance Metrics

**Target Performance:**
- Tender package compilation time: <1 week from Phase 4 completion
- Tender process duration: 4–6 weeks (from issuance to award)
- Number of qualified bids received: ≥3 per contract package
- Bid evaluation completeness: 100% of required criteria assessed
- Award recommendation turnaround: <5 working days after tender close
- Dispute rate: 0 formal protests during tender process