---
title: Procurement Approval Routing
description: Route procurement orders through value-based approval chains with authority matrix enforcement, HITL gates, and audit trail logging
version: 1.0
frequency_percent: 70.0
success_rate_percent: 95.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/01900_procurement/procurement-approval-routing
gigabrain_tags: disciplines, 01900_procurement, approval-routing, authority-matrix, HITL, value-based-routing
openstinger_context: order-approval-workflows, authority-matrix-enforcement, procurement-compliance
last_updated: 2026-04-02
related_docs:
  - docs_construct_ai/disciplines/01900_procurement/agent-data/domain-knowledge/1900_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/01900_procurement/agent-data/prompts/01900_AI-NATIVE-PROCUREMENT-OPERATIONS-PROMPT.md
  - docs_construct_ai/disciplines/01900_procurement/workflow_docs/1900_PROCUREMENT_APPROVAL_WORKFLOWS_MANAGEMENT.MD
related_skills:
  - procurement-compliance
  - procurement-order-management
  - fin-budget-planning-control
  - procurement-budget-validation
---

# Procurement Approval Routing

## Overview

Route procurement orders through value-based approval chains with authority matrix enforcement, Human-in-the-Loop (HITL) gates, and immutable audit trail logging. Ensures every order is processed by the correct approvers based on value, type, and complexity.

**Announce at start:** "I'm using the procurement-approval-routing skill to configure approval chains and enforce authority limits."

## When to Use This Skill

**Trigger Conditions:**
- Creating or modifying procurement order (> $0)
- Order value crosses approval threshold
- Approval chain needs to be determined
- HITL gate evaluation required
- Rejection handling with reason capture

**Prerequisites:**
- Authority matrix configured in system
- Order data complete (value, type, risk level)
- User roles and permissions loaded

## Step-by-Step Procedure

### 1. Determine Approval Chain

Based on order value and type, determine required approvers:

| Order Value (USD) | Order Value (ZAR) | Approval Chain |
|-------------------|-------------------|----------------|
| < $25,000 | < R500,000 | Procurement Officer |
| $25,000 - $100,000 | R500,000 - R2,000,000 | Procurement Manager + Project Manager |
| $100,000 - $500,000 | R2,000,000 - R10,000,000 | Above + Finance Manager |
| > $500,000 | > R10,000,000 | Above + Executive Sponsor |
| Single-source | Any value | Above + Commercial/Legal Review |

### 2. Configure Routing Type

| Routing Type | When to Use | Behavior |
|-------------|-------------|----------|
| Sequential | High-value, complex orders | Each approver must approve before next |
| Parallel | Low-value, routine orders | All approvers can approve simultaneously |
| Hybrid | Medium-value with specialized review | Sequential for certain steps, parallel for others |

### 3. Enforce Authority Limits

**Rules:**
- Never allow approver to approve above their authority limit
- Never allow same user to be both requestor and approver
- Never allow approval without budget availability confirmed
- Always log approval action to immutable audit trail