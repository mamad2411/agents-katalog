---
title: Procurement Contract Intelligence
description: Analyze contract clauses, track obligations, monitor contract health, and detect change propagation for procurement contracts
version: 1.0
frequency_percent: 25.0
success_rate_percent: 92.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/01900_procurement/procurement-contract-intelligence
gigabrain_tags: disciplines, 01900_procurement, contract-intelligence, obligation-tracking, clause-analysis, procurement
openstinger_context: 01900_procurement_operations, skill-execution
last_updated: 2026-04-02
related_docs:
  - docs_construct_ai/disciplines/01900_procurement/agent-data/domain-knowledge/1900_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/01900_procurement/agent-data/domain-knowledge/1900_GLOSSARY.MD
---

# Procurement Contract Intelligence

## Overview
Analyze contract clauses, track obligations, monitor contract health, and detect change propagation for procurement contracts.

**Announce at start:** "I'm using the procurement-contract-intelligence skill for contract analysis and monitoring."

## When to Use This Skill
**Trigger Conditions:** New contract received, contract amendment issued, periodic health check scheduled, or change analysis requested

**Prerequisites:**
- Contract document available (executed version)
- Standard form of contract for comparison
- Active orders/POs under the contract
- Obligation register maintained

## Capabilities

### 1. Clause Analysis
- Compare contract clauses against standard form
- Identify non-standard, missing, or deviant clauses
- Assign risk level per clause category:
  - **Low:** Standard clause, no deviation
  - **Medium:** Minor deviation, negotiated tolerance
  - **High:** Material deviation changes risk allocation, missing standard clause, or added non-standard clause

### 2. Obligation Tracking
- Extract deliverables, milestones, penalties, warranty, reporting obligations
- Record obligation data:
  ```
  obligation_type: deliverable | milestone | penalty | warranty | reporting
  responsible_party: buyer | supplier | shared
  status: pending | fulfilled | overdue | waived | disputed
  due_date (or relative to milestone)
  evidence_link
  ```
- Monitor upcoming obligations (30/60/90 day windows)
- Flag overdue obligations in red

### 3. Change Propagation
When contract amended:
1. Query affected orders/POs via contract_id
2. Identify pricing changes, delivery impacts, scope changes
3. Flag affected orders for review
4. Notify budget owners of potential cost impact
5. Update obligation register for new obligations

### 4. Contract Health Checks
| Check | Frequency | Trigger |
|-------|-----------|---------|
| Missing signatures | Weekly | Unsigned contracts approaching effective date |
| Expired terms | Monthly | Contracts past end date without renewal |
| Unfulfilled obligations | Weekly | Overdue obligations without extension |
| Insurance/certification expiry | Monthly | Certificates within 90-day expiry |
| Price escalation triggers | Monthly | Index-linked pricing clauses active |
| Warranty expiry alerts | Quarterly | Warranties approaching expiry |

## Procedure

### Step 1: Contract Receipt and Analysis
1. Receive executed contract document
2. Perform clause-by-clause comparison with standard form
3. Flag non-standard clauses with risk level
4. Extract all obligations and record in obligation register
5. Identify key dates (commencement, milestones, expiry, review)

### Step 2: Initial Health Check
1. Verify all required signatures present
2. Confirm insurance/certifications current
3. Verify no unfulfilled obligations at commencement
4. Confirm contract registered in contract management system

### Step 3: Ongoing Monitoring
1. Run scheduled health checks per frequency table
2. Process amendments through change propagation
3. Update obligation status as evidence submitted
4. Generate obligation alerts for upcoming due dates

### Step 4: Change Propagation Response
1. Assess amendment impact on active orders
2. Notify affected parties with impact summary
3. Update contract record with amendment history
4. Ensure previous versions remain accessible for audit

## Success Criteria
- [ ] All non-standard clauses identified and risk-rated
- [ ] All obligations extracted and recorded
- [ ] Health checks running on schedule
- [ ] Change propagation completed for amendments
- [ ] Alerts generated for upcoming/overdue obligations

## Common Pitfalls
1. **Incomplete Clause Extraction** — Must analyze entire contract, not just key clauses
2. **Missing Relative Dates** — Obligations tied to milestones need milestone tracking
3. **Obligation Evidence Gaps** — Record evidence links, not just obligation status
4. **Amendment Cascade Failure** — One amendment may affect dozens of orders