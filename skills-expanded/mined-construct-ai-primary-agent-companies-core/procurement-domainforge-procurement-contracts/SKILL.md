---
name: procurement-domainforge-procurement-contracts
description: >
  Use for 01900 procurement order workflow: contract administration, procurement planning, vendor management, 
  PO creation, SOW template selection, discipline assignment, approval routing, and supplier coordination within DomainForge AI.
  Also use for procurement workflow testing, compliance validation, and order lifecycle management.
---

# Procurement Domainforge Procurement Contracts - DomainForge AI

## Role Alignment
This skill powers the **01900 Procurement Order Workflow** — covering the full lifecycle from order creation 
(CreateOrderModal 5-phase wizard), SOW generation, multi-discipline appendix assignment (Appendices A-F), 
approval matrix integration (01300), HITL review, compliance enforcement, through to logistics processing and closure.

## Overview
Manages procurement contracts and order workflows for DomainForge AI, providing contract administration, 
vendor management, procurement planning, supplier coordination, and compliance enforcement. Reports to orion-domainforge-ceo.

## When to Use
- When working on 01900 procurement order creation, approval, or fulfillment
- When validating procurement workflow compliance (authority limits, budget blocks, segregation of duties)
- When coordinating with QualityForge for procurement testing scenarios
- When cross-team procurement coordination is required
- **Don't use when:** Pure financial analysis (use finance-domainforge-finance-cost-management), 
  or logistics routing (use logistics-domainforge-supply-chain)

## Core Procedures
### Standard Workflow
1. **Receive Request** - Ingest procurement requirements from orion-domainforge-ceo or Paperclip task
2. **Analyze Requirements** - Determine order type (PO/SO/WO), complexity level, compliance needs
3. **Execute Task** - Create order, assign disciplines, configure approvals, generate SOW
4. **Quality Check** - Validate against compliance rules, authority limits, budget allocation
5. **Deliver Results** - Return completed order with audit trail

## 01900 Workflow Integration
- **CreateOrderModal**: 5-phase wizard (basic info → SOW template → discipline assignment → approval config → review/create)
- **Order Types**: purchase_order, service_order, work_order
- **Appendices**: A (Product Specs), B (QA Requirements), C (HSE/Safety), D (Training Materials), E (Logistics), F (Packing/Marking)
- **Approval Thresholds**: <$25K single approver, $25K-$100K multi-level, >$100K executive approval
- **Compliance**: Budget hard blocks, authority limits, audit trail logging, segregation of duties

## Agent Assignment
**Primary Agent:** procurement-domainforge-procurement-contracts
**Company:** DomainForge AI
**Role:** Procurement Contracts
**Reports To:** orion-domainforge-ceo

## Success Metrics
- Task completion rate: >=95%
- Quality score: >=90%
- Response time: <4 hours
- Stakeholder satisfaction: >=90%

## Error Handling
- **Error:** Task execution failure
  **Response:** Retry with adjusted approach, escalate to orion-domainforge-ceo if persistent
- **Error:** Quality validation fails
  **Response:** Re-work task, apply quality improvements, re-validate

## Cross-Team Integration
**Gigabrain Tags:** domainforge, procurement, contract-administration, vendor-management
**OpenStinger Context:** Session continuity, knowledge sharing
**PARA Classification:** Procurement, contracts
**Related Skills:** orion-domainforge-ceo, logistics-domainforge-supply-chain
**Testing Integration:** procurement-testing
**Workflow Documentation:** [01900 Procurement Order Workflow](docs-paperclip/disciplines/01900-procurement/order-workflow/README.md)
**Last Updated:** 2026-03-04

