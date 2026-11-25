---
title: Approval Routing Configuration
description: Configure value-based approval routing with Sequential/Parallel/Hybrid routing types, HITL integration, cover sheet generation, and escalation rules
version: 1.0
frequency_percent: 85.0
success_rate_percent: 92.0
memory_layer: durable_knowledge
para_section: docs_construct_ai/skills/domainforge_ai/approval-routing
gigabrain_tags: disciplines, 01900_procurement, approval-routing, approval-matrix, value-based-routing, hitl-integration, escalation-rules
openstinger_context: approval-workflow, procurement-governance, financial-authorization
last_updated: 2026-03-31
related_docs:
  - docs_construct_ai/disciplines/01900_procurement/agent-data/domain-knowledge/1900_DOMAIN-KNOWLEDGE.MD
  - docs_construct_ai/disciplines/01900_procurement/agent-data/prompts/01900_PROCUREMENT_ORDER_PROMPT.md
  - docs_construct_ai/disciplines/01900_procurement/agent-data/domain-knowledge/1900_GLOSSARY.MD
  - docs_construct_ai/disciplines/01900_procurement/workflow_docs/1900_PROCUREMENT_APPROVAL_WORKFLOWS_MANAGEMENT.MD
related_skills:
  - pre-task-assessment-readiness
  - procurement-order-management
---

# Approval Routing Configuration

## Overview

Configure value-based approval routing with Sequential, Parallel, or Hybrid routing types. Integrates with HITL (Human-in-the-Loop) for confidence-based escalation, generates approval cover sheets, and manages escalation and notification rules.

**Announce at start:** "I'm using the approval-routing skill to configure an approval workflow."

## When to Use This Skill

**Trigger Conditions:**
- A new procurement order requires approval configuration
- Changing approval thresholds or authority limits
- Adding new approvers or changing approval hierarchy
- Setting up HITL thresholds for AI-assisted approvals
- Configuring escalation rules for delayed or rejected approvals

**Prerequisites:**
- Order value calculated
- Organization's approval authority matrix defined
- Approver roles and individuals assigned to each threshold level

## Step-by-Step Procedure

### Step 1: Determine Approval Threshold

Apply the value-based approval matrix:

| Order Value | Approval Required |
|-------------|-------------------|
| <$25,000 | Procurement officer approval only |
| $25,000 – $100,000 | Procurement manager + Project manager |
| >$100,000 | Procurement manager + Project manager + Finance manager + Director |
| Single-source justification | Above + Commercial/Legal review |
| Emergency procurement | Expedited: Procurement manager + Project manager (retroactive documentation) |

### Step 2: Select Routing Type

Choose the routing type based on order complexity:

#### Sequential Routing
- Approvers review and decide in specified order
- Each approver must approve before the order moves to the next approver
- **Use when:** Lower-level approvers need to validate before senior approvers review
- **Example:** Procurement officer → Procurement manager → Project manager

#### Parallel Routing
- All assigned approvers review simultaneously
- Order is approved when all approvers have approved
- **Use when:** Approvers have independent review responsibilities and no sequential dependency
- **Example:** Technical reviewer, Finance reviewer, Legal reviewer all review independently

#### Hybrid Routing
- Combines Sequential and Parallel routing
- Some approvers review in sequence while others review in parallel at certain stages
- **Use when:** Complex orders with mixed sequential and independent review needs
- **Example:** Sequential: Procurement officer → [Parallel: Technical + Finance + Safety] → Director

### Step 3: Assign Approvers

For each threshold level, assign specific individuals to approver roles.

For each approval level, select:
- **Approver Role:** The organizational role (e.g., "Procurement Manager", "Project Director")
- **Approver Name:** The specific individual currently in that role
- **Backup Approver:** Who approves if the primary approver is unavailable
- **Approval Authority:** Maximum order value this approver can authorize

### Step 4: Configure HITL Integration

Set up Human-in-the-Loop thresholds for AI-assisted approval recommendations:

| Confidence Level | HITL Action |
|------------------|-------------|
| High confidence (≥95%) | Auto-approve with human notification (human can override) |
| Medium confidence (70-94%) | Human review required before proceeding |
| Low confidence (<70%) | Full human review with detailed rationale and supporting evidence |

Configure HITL triggers:
- **Value threshold:** Any order >$100,000 requires full human review regardless of AI confidence
- **Single-source:** Any single-source order requires full human review
- **Emergency:** Any emergency procurement requires full human review with documented justification
- **New supplier:** Any order to a supplier not previously used on the project requires human review

### Step 5: Configure Cover Sheet Generation

Enable or configure approval cover sheet with the following fields:
- Order number and type
- Order description and summary
- Total value and currency
- Supplier name and tier
- Budget code/WBS
- Approval threshold and routing type
- Assigned approvers
- Deadline for approval
- Risk summary (from risk assessment)
- Special notes (single-source justification, emergency rationale, etc.)

### Step 6: Configure Escalation Rules

Define escalation behavior for delayed or rejected approvals:

| Scenario | Escalation Action | Timeline |
|----------|-------------------|----------|
| Approver non-response | Reminder notification | After 24 hours |
| Continued non-response | Escalate to backup approver | After 48 hours |
| Second non-response | Escalate to approving authority's manager | After 72 hours |
| Approval rejected | Return to initiator with comments for revision | Immediate |
| Emergency order pending | Auto-escalate to next authority level | After 12 hours |

### Step 7: Validate and Activate

Before activating the approval workflow:
1. Validate all approver roles have assigned individuals
2. Confirm backup approvers are configured for all levels
3. Verify HITL thresholds match organizational policy
4. Confirm escalation rules are correctly configured
5. Generate and review the approval cover sheet
6. Activate the approval workflow

## Success Criteria

- [ ] Approval thresholds match organizational authority matrix
- [ ] Routing type (Sequential/Parallel/Hybrid) is appropriate for order complexity
- [ ] All approver roles have assigned individuals and backups
- [ ] HITL thresholds configured and match organizational policy
- [ ] Cover sheet generation enabled with all required fields
- [ ] Escalation rules configured with realistic timelines
- [ ] Approval workflow validated and activated

## Common Pitfalls

1. **Missing Backup Approvers** — Always assign a backup approver for each approval level. If the primary approver is unavailable, the workflow will stall.
2. **Wrong Routing Type** — Don't use Parallel routing when lower-level validation is required before senior review. Use Sequential or Hybrid instead.
3. **HITL Threshold Misconfiguration** — If HITL confidence thresholds are set too high, too many orders will bypass human review. If too low, too many orders will require unnecessary human review, slowing the process.
4. **Missing Escalation Rules** — Without escalation rules, delayed approvals can indefinitely hold up procurement. Always configure escalation timeouts.
5. **Cover Sheet Incomplete** — A cover sheet missing risk information or special notes deprives approvers of context needed for informed decisions.

## Cross-References

### Related Skills
- `procurement-order-management` — Approval routing is configured as Phase 4 of order creation
- `pre-task-assessment-readiness` — Assess readiness before configuring approval routing

### Related Agents
- `Financial Compliance Specialist` (DomainForge) — Primary agent for approval threshold and financial validation
- `Procurement Strategy Specialist` (DomainForge) — Strategic approval configuration and authority limits
- `Mobile Workflow Designer` (DomainForge) — GPS-enabled and mobile approval workflows

## Example Usage

**Scenario:** Configure approval for R6.3M structural steel PO

1. **Threshold:** >$100k → Procurement manager + PM + Finance manager + Director + Legal (single-source for specialized sections)
2. **Routing Type:** Hybrid — Sequential: Procurement officer → [Parallel: PM + Finance + Legal] → Director
3. **Approvers Assigned:** Procurement Officer (J. Smith), PM (L. Brown), Finance (K. Naidoo), Legal (M. van der Merwe), Director (A. Ten