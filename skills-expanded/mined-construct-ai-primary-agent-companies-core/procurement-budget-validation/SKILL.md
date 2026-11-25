---
title: Procurement Budget Validation
description: Validate procurement orders against budget allocations, track committed spending, and enforce budget gates before order approval
version: 1.0
frequency_percent: 75.0
success_rate_percent: 95.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/01900_procurement/procurement-budget-validation
gigabrain_tags: disciplines, 01900_procurement, budget-validation, committed-cost, 3-way-match, cost-control
openstinger_context: budget-gate-validation, procurement-cost-control
last_updated: 2026-04-02
related_docs:
  - docs_construct_ai/disciplines/01900_procurement/agent-data/domain-knowledge/1900_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/01200_finance/agent-data/01200_GLOSSARY.MD
  - docs_construct_ai/disciplines/00250_commercial/agent-data/00250_COST_MANAGEMENT.MD
related_skills:
  - fin-budget-planning-control
  - procurement-cost-control
  - procurement-compliance
  - procurement-order-management
---

# Procurement Budget Validation

## Overview

Validate procurement orders against budget allocations before approval, track committed spending, enforce 3-way match (PO-GRN-Invoice), and implement budget gates. Ensures no order exceeds available budget without proper escalation.

**Announce at start:** "I'm using the procurement-budget-validation skill to validate order budgets and enforce cost controls."

## When to Use This Skill

**Trigger Conditions:**
- Before order submission for approval
- During order value calculation
- When budget availability is uncertain
- Before invoice processing
- When cost variance detected

**Prerequisites:**
- Budget data accessible via API or database
- Cost center/WBS element defined for order
- Committed cost tracking active

## Step-by-Step Procedure

### 1. Budget Availability Check

Before processing any order:

```
Available Budget = Approved Budget Line Item
                   - Already Committed (POs issued)
                   - Already Spent (Invoices paid)
                   - Encumbrances (Pending approvals)

Order Allowed = Order Value <= Available Budget
```

### 2. Pre-PO Budget Gate

| Check | Pass Condition | Fail Action |
|-------|---------------|-------------|
| Budget line exists | Cost center/WBS valid and active | Require budget code assignment |
| Available funds ≥ order value | (Budget - committed) ≥ order | Escalate to finance manager |
| Currency match | PO currency = budget currency | Apply exchange rate with date flag |
| Variance ≤ tolerance | Unit price variance < 15% from budget rate | Flag for buyer review |

### 3. Pre-Payment 3-Way Match

Before processing any invoice:

| Document | Data Verified | Match Condition |
|----------|---------------|-----------------|
| Purchase Order | Quantity, unit price, terms | Base of comparison |
| Goods Receipt Note (GRN) | Quantity received, date | GRN quantity ≤ PO quantity |
| Invoice | Amount, quantity, reference | Invoice amount = PO price × received quantity |

**Tolerance:** 100% match required for same-day processing; variances up to invoice tolerance (%) escalate to finance.