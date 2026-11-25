---
name: procurement-and-vendor-management
description: Use when planning, reviewing, or drafting procurement workflows, vendor comparisons, supplier evaluation, purchase justification, sourcing criteria, RFP evaluation, renewal analysis, vendor risk summaries, or negotiation preparation. Prefer this Skill when the task needs requirements, evaluation criteria, risk, total cost, stakeholder alignment, or decision recommendation. Do not use for purchase approvals, legal advice, or procurement system actions.
meta:
  version: 1
  display_name: 采购与供应商管理
---

# Procurement And Vendor Management

## Purpose

Support purchasing and vendor decisions with clear requirements, evaluation criteria, cost/risk tradeoffs, stakeholder needs, and decision evidence.

## Use When

Use for:

- vendor comparison
- procurement justification
- supplier evaluation
- RFP evaluation support
- renewal or consolidation review
- vendor risk summary
- negotiation preparation
- purchase decision brief

## Material Gate

Identify:

- business need, requester, budget, timeline, required capabilities, and constraints
- candidate vendors, pricing, contract terms, security/compliance needs, and implementation effort
- decision criteria and required approvers

Do not invent vendor capabilities, pricing, legal terms, or approval status.

## Workflow

1. Define the business requirement and must-have criteria.
2. Separate functional fit, commercial fit, implementation effort, risk, and stakeholder preference.
3. Build a comparison matrix using shared criteria.
4. Identify total cost, switching cost, lock-in, security, support, and operational risks.
5. Prepare negotiation questions or clarification requests.
6. Recommend next step with confidence and caveats.
7. Use `html-report-builder` for vendor comparison or procurement reports.

## Checks

- Criteria are shared across vendors.
- Total cost includes implementation and operating burden where known.
- Risks include owner and mitigation.
- Recommendation is not stronger than evidence.
- Legal/security review needs are flagged.

## Outputs

- vendor comparison
- procurement justification
- evaluation matrix
- renewal review
- vendor risk summary
- negotiation prep
- decision brief

## Boundary

This Skill owns procurement reasoning, vendor comparison structure, and decision brief drafting. It does not own purchase approval, contract legal review, security approval, procurement system writes, vendor communication, or payment.

It must not run shell, Python, Node, npm, curl, MCP, procurement system, ERP, vendor portal, email, CRM, payment, package install, or external API commands by itself; those actions belong to XAgent tools visible in the current session.
