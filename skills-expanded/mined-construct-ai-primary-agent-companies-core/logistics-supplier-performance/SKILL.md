---
title: Logistics Supplier Performance
description: Monitor and analyze supplier delivery performance, quality metrics, lead time accuracy, and responsiveness to support supplier management and risk mitigation
frequency: Weekly monitoring, monthly scorecarding
success_rate: 90%
tags:
  - logistics-operations
  - supplier-management
  - delivery-performance
  - quality-metrics
  - 00886_logistics-director
docs:
  - docs_construct_ai/disciplines/00886_logistics-director/agent-data/domain-knowledge/00886_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/01900_procurement/agent-data/domain-knowledge/1900_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/skills/shared/pre-task-assessment-readiness/SKILL.md
---

# Logistics Supplier Performance

## Overview

This skill enables monitoring and analysis of supplier delivery performance, quality acceptance rates, lead time accuracy, and responsiveness. Primary agent: LOG-SUP-001 Supplier Performance Agent. Supporting skills: `shared/pre-task-assessment-readiness`.

## Triggers

- Weekly delivery performance data received
- Monthly supplier scorecard generation
- Supplier delivery delays detected
- Quality issues reported
- New supplier performance baseline required
- Supplier contract review period

## Prerequisites

- Access to ERP purchase order and delivery data
- Supplier delivery confirmations and receiving logs
- Quality inspection results
- Supplier contract performance standards
- Historical supplier performance data

## Steps

### Step 1: Data Collection
- Extract delivery data from ERP (purchase orders, delivery notes, receiving logs)
- Collect quality inspection results from quality system
- Gather supplier communication logs for responsiveness assessment
- Verify data completeness and accuracy

### Step 2: Performance Calculation
- Calculate on-time delivery rate (delivered on or before due date / total deliveries)
- Calculate quality acceptance rate (accepted quantity / total received quantity)
- Calculate lead time accuracy (actual lead time vs promised lead time)
- Assess supplier responsiveness (response time to queries, issue resolution speed)

### Step 3: Supplier Scorecarding
- Apply weighted scoring to performance metrics
- Generate supplier performance scorecard
- Rank suppliers by performance category (excellent, satisfactory, poor)
- Identify trend direction (improving, stable, declining)

### Step 4: Risk Assessment
- Identify single-source dependencies
- Assess supplier financial stability
- Evaluate supplier capacity constraints
- Calculate supplier risk rating

### Step 5: Reporting and Escalation
- Generate supplier performance reports
- Flag underperforming suppliers for director review
- Recommend supplier intervention actions
- Update supplier performance database

## Success Criteria

- On-time delivery rate accurately calculated for all active suppliers
- Quality acceptance rate tracked with root cause for rejections
- Lead time accuracy monitored with variance analysis
- Supplier risk rating current and actionable
- Underperforming suppliers identified and escalated
- Supplier performance trends documented

## Common Pitfalls

1. **Incomplete delivery data**: Missing delivery confirmations lead to inaccurate performance calculation
2. **Ignoring quality vs quantity trade-offs**: Supplier may deliver on time but with quality issues
3. **Not accounting for force majeure**: External factors may unfairly penalize supplier
4. **Single metric focus**: Over-reliance on on-time delivery without considering quality and responsiveness
5. **Delayed escalation**: Waiting too long to escalate poor performance

## Cross-References

- `shared/pre-task-assessment-readiness/SKILL.md` — Pre-task verification
- `logistics-transportation-management/SKILL.md` — Delivery coordination
- `logistics-inventory-control/SKILL.md` — Stock impact of supplier delays

## Usage

Use this skill for weekly supplier performance monitoring, monthly supplier scorecarding, supplier contract reviews, and supplier issue escalation.

## Metrics

- **Data Accuracy**: 100% of deliveries tracked and confirmed
- **Performance Coverage**: 100% of active suppliers scorecarded monthly
- **Timeliness**: Supplier performance reports generated within 2 business days of month-end
- **Escalation Effectiveness**: 90%+ of escalated supplier issues resolved or mitigated
