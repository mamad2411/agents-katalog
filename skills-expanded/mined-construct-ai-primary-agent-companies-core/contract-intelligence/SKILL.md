---
title: Contract Intelligence
description: Analyze procurement contracts for clause extraction, obligation tracking, change propagation, health checking, and dispute resolution support with structured data pipeline
version: 1.0
frequency_percent: 65.0
success_rate_percent: 90.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/contract-intelligence
gigabrain_tags: disciplines, 01900_procurement, contract-intelligence, clause-analysis, obligation-tracking, change-propagation, contract-health-checking
openstinger_context: contract-analysis, procurement-legal-intelligence
last_updated: 2026-03-31
related_docs:
  - docs_construct_ai/disciplines/01900_procurement/agent-data/domain-knowledge/1900_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/01900_procurement/agent-data/prompts/01900_AI-NATIVE-PROCUREMENT-OPERATIONS-PROMPT.md
  - docs_construct_ai/disciplines/01900_procurement/agent-data/domain-knowledge/1900_GLOSSARY.MD
  - docs_construct_ai/disciplines/01900_procurement/workflow_docs/1900_PROCUREMENT_APPROVAL_WORKFLOWS_MANAGEMENT.MD
related_skills:
  - pre-task-assessment-readiness
  - workflow-implementation
  - procurement-document-generation
  - procurement-compliance
---

# Contract Intelligence

## Overview

Analyze procurement contracts to extract structured data (clauses, obligations, milestones, penalties), detect changes, propagate impacts to related orders, validate contract health, and support dispute resolution. Works with contracts in PDF, DOCX, and structured text formats.

**Announce at start:** "I'm using the contract-intelligence skill to analyze a procurement contract for clauses, obligations, and compliance requirements."

## When to Use This Skill

**Trigger Conditions:**
- Analyzing a new contract for clause extraction and risk identification
- Tracking contract obligations, milestones, and deadlines
- Detecting and analyzing contract amendments or changes
- Validating contract health (signatures, expiration, unfulfilled obligations)
- Supporting dispute resolution with evidence compilation

**Prerequisites:**
- Contract document accessible (PDF, DOCX, or text format)
- Contract type identified (supply, service, framework, subcontract)
- Related orders/POs identified for change propagation analysis
- Standard contract template available (for change detection)

## Step-by-Step Procedure

### Step 1: Contract Type Identification

Identify contract type using classification criteria:

| Contract Indicator | Classified As |
|--------------------|---------------|
| Goods/materials supply with pricing schedule | Supply Contract |
| Professional services, time-based billing | Service Contract |
| Frame agreement with call-off orders | Framework Agreement |
| Subcontractor arrangement with scope defined | Subcontract |
| Amendment to existing contract | Contract Amendment |
| Early works or letter of intent | Preliminary Agreement |

### Step 2: Clause Extraction & Classification

Extract contract clauses and classify by type:

| Clause Category | Examples | Priority |
|----------------|----------|----------|
| **Commercial** | Pricing, payment terms, penalties, variations, currency | Critical |
| **Performance** | Deliverables, specifications, quality standards, acceptance criteria | Critical |
| **Risk** | Liability limits, indemnities, insurances, force majeure | High |
| **Time** | Duration, milestones, extensions, liquidated damages | High |
| **Termination** | Termination rights, notice periods, consequences | High |
| **Administration** | Notices, change management, dispute resolution, governing law | Standard |
| **Regulatory** | Compliance requirements, permits, safety, environmental | Standard |

**Extraction Format:**
```json
{
  "contract_id": "CNT-2026-0012",
  "clause": {
    "title": "Liquidated Damages",
    "category": "time",
    "priority": "high",
    "text": "If Contractor fails to achieve Mechanical Completion by the Target Date, Contractor shall pay liquidated damages at 0.5% of the Contract Price per week of delay, up to a maximum of 10% of the Contract Price.",
    "extract_values": {
      "damage_rate": "0.5% per week",
      "damage_cap": "10% of Contract Price",
      "trigger": "failure to achieve Mechanical Completion by Target Date"
    }
  }
}
```

### Step 3: Obligation Extraction

Extract all obligations, deliverables, and milestones:

| Obligation Element | Extracted Data |
|--------------------|----------------|
| **Obligation Owner** | Party responsible (employer, contractor, subcontractor) |
| **Obligation Description** | What must be done |
| **Trigger Condition** | When obligation becomes active |
| **Deadline/Milestone** | Target date or condition for completion |
| **Consequence** | Penalty, damages, or right exercised if not fulfilled |
| **Evidence Required** | What proves obligation was fulfilled |
| **Status** | Current status based on contract state |

**Obligation Tracking Structure:**
```json
{
  "obligations": [
    {
      "id": "OBL-001",
      "owner": "Contractor",
      "description": "Submit performance bond within 14 days of contract signing",
      "trigger": "contract_execution",
      "deadline_days": 14,
      "consequence": "Employer may suspend work and recover costs",
      "evidence": "bond_certificate",
      "status": "fulfilled",
      "status_date": "2026-03-14"
    }
  ]
}
```

### Step 4: Change Detection & Impact Analysis

Compare contract against baseline or previous version:

| Change Type | Detection Method | Impact Areas |
|-------------|-----------------|--------------|
| Clause text modified | Text diff against baseline | Related orders, invoices, obligations |
| Pricing schedule updated | Value comparison | All POs at old prices, budget projections |
| Timeline changed | Date comparison | All scheduled deliverables, milestone tracking |
| Scope expanded/reduced | Text diff + obligation count | Resource plans, delivery schedules |
| Risk allocation changed | Clause addition/deletion | Insurance, guarantees, bonds |

**Impact Analysis Process:**
1. Identify changed clauses/obligations
2. Find all orders/POs referencing changed clauses
3. Calculate financial impact (price changes, damage adjustments)
4. Calculate schedule impact (date changes, milestone shifts)
5. Generate change impact report

### Step 5: Contract Health Checking

Validate current contract state:

| Health Check | Validation Criteria | Status Output |
|-------------|-------------------|---------------|
| Signatures | All required parties signed | Valid / Missing signatures |
| Effective Date | Past and within contract period | Active / Not yet effective / Expired |
| Obligations Status | All critical obligations on track | On track / At risk / Overdue |
| Expiration | Date compared to current date | Valid / Expiring within 30 days / Expired |
| Amendments | All amendments logged and incorporated | Current / Missing amendments |
| Insurance/Guarantees | Current and not expired | Valid / Expiring / Expired |
| Disputes | Any active disputes logged | Clear / Disputed |

**Health Report Format:**
```json
{
  "contract_id": "CNT-2026-0012",
  "health_check_at": "2026-03-31T14:00:00Z",
  "overall_status": "healthy",
  "checks": [
    {"check": "signatures", "status": "valid", "details": "All 3 parties signed"},
    {"check": "effective_date", "status": "active", "details": "Started 2026-01-15, expires 2026-12-31"},
    {"check": "obligations", "status": "on_track", "details": "8/8 obligations on track"},
    {"check": "expiration", "status": "valid", "details": "275 days remaining"},
    {"check": "amendments", "status": "current", "details": "2 amendments incorporated"},
    {"check": "disputes", "status": "clear", "details": "No active disputes"}
  ]
}
```

### Step 6: Dispute Resolution Support

Compile evidence for dispute scenarios:

| Evidence Type | Source | Purpose |
|---------------|--------|---------|
| **Contract Clauses** | Extracted clause text | Legal basis for claim |
| **Timeline** | Obligation dates, milestone records | Shows sequence of events |
| **Communications** | Email correspondence, RFIs, NCRs | Documentary evidence |
| **Performance Records** | Delivery notes, inspection reports | Shows actual vs. contractual |
| **Financial Records** | Invoices, payment records, variation orders | Financial impact evidence |

### Step 7: Output Generation

Generate structured outputs:

```json
{
  "contract_analysis": {
    "contract_id": "CNT-2026-0012",
    "contract_type": "supply_contract",
    "analysis_at": "2026-03-31T14:00:00Z",
    "clauses_extracted": 24,
    "obligations_extracted": 8,
    "health_status": "healthy",
    "changes_detected": 0,
    "dispute_support": {
      "active_disputes": 0,
      "evidence_compiled": false
    }
  }
}
```

## Success Criteria

- [ ] Contract type correctly classified
- [ ] All clauses extracted with correct category and priority
- [ ] All obligations extracted with deadlines and consequences
- [ ] Change detection identifies all modifications from baseline
- [ ] Impact analysis covers affected orders, obligations, and financial elements
- [ ] Health check covers all 6 validation areas
- [ ] Dispute evidence compiled (if dispute scenario applies)
- [ ] All extracted data structured and machine-readable

## Common Pitfalls

1. **Missing Obligations** — Some obligations are implicit in contract language. Look for "shall," "shall ensure," "shall cause" language.
2. **Ignoring Amendment History** — Each amendment may modify obligations. Always incorporate all amendments into the current contract state.
3. **Skipping Financial Impact Analysis** — Pricing changes affect active POs. Always calculate which orders are at old prices and require repricing.
4. **Overlooking Expiring Elements** — Insurance policies, guarantees, and bonds within contracts have expiry dates that may not match contract end date. Check them separately.
5. **Accepting Unilateral Interpretation** — When clauses are ambiguous, flag ambiguity rather than asserting a single interpretation. Disputes often arise from ambiguous language.

## Cross-References

### Related Skills
- `procurement-document-generation` — Generates contract variation notices, change orders
- `procurement-compliance` — Validates contract terms against regulatory requirements
- `procurement-order-management` — Uses contract terms to validate PO creation
- `supplier-evaluation` — Contract performance data feeds supplier scoring

### Related Agents
- `Contract Administration Specialist` (DomainForge) — Primary contract analysis and obligation tracking
- `Procurement Strategy Specialist` (DomainForge) — Negotiation strategy and risk assessment
- `Financial Compliance Specialist` (DomainForge) — Financial impact analysis of contract changes

## Example Usage

**Scenario:** Analyze supply contract CNT-2026-0012 for obligations and health status

1. **Identify:** Contract is a supply agreement for structural steel supply and delivery
2. **Extract Clauses:** 24 clauses across commercial, performance, risk, time, termination categories
3. **Extract Obligations:** 8 obligations with deadlines, 3 already fulfilled, 5 on track
4. **Check Health:** Signatures valid, contract active, obligations on track, 275 days remaining
5. **Detect Changes:** No changes detected from baseline
6. **Output:** JSON with full analysis, obligation tracking, health report

## Performance Metrics

**Target Performance:**
- Clause extraction accuracy: >95% (all clauses correctly identified and categorized)
- Obligation extraction accuracy: >98% (all obligations identified with correct deadlines)
- Change detection accuracy: >99% (all text changes identified)
- Health check completeness: 6/6 checks completed every time
- Analysis time: <2 minutes per standard contract