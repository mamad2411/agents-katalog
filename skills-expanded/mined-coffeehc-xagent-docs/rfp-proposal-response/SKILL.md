---
name: rfp-proposal-response
description: Use when analyzing, drafting, organizing, or reviewing RFP, RFQ, RFI, tender, bid, proposal, grant, vendor questionnaire, security questionnaire, or procurement response material. Prefer this Skill when the task needs requirement extraction, compliance matrix, answer drafting, win themes, evidence, gaps, owners, and submission readiness. Do not use for legal approval, final submission, or unsupported capability claims.
meta:
  version: 1
  display_name: RFP 与投标响应
---

# RFP Proposal Response

## Purpose

Convert proposal requirements into a structured response plan with compliance mapping, evidence, answer drafts, owners, gaps, and win themes.

## Use When

Use for:

- RFP/RFI/RFQ analysis
- tender or bid response planning
- proposal writing
- compliance matrix creation
- security or vendor questionnaire responses
- grant or procurement response drafts
- win theme development

## Material Gate

Identify:

- buyer, deadline, response format, submission rules, and evaluation criteria
- requirements, mandatory clauses, question list, attachments, and evidence needed
- product/service capabilities and approved proof points
- owners for missing answers

Do not claim capabilities, certifications, references, pricing, or commitments without evidence.

## Workflow

1. Extract requirements and submission instructions.
2. Classify each requirement as mandatory, scored, optional, unclear, or risk.
3. Build a compliance matrix with owner, status, evidence, and gap.
4. Draft answers using approved facts and proof points.
5. Identify win themes, differentiators, and customer-specific value.
6. Flag legal, security, finance, product, or executive approvals required.
7. Use `html-report-builder` for response readiness reports or matrices.

## Checks

- Mandatory requirements are not missed.
- Answers cite evidence or mark gaps.
- Submission instructions and deadline are visible.
- Unsupported claims are flagged.
- Owners are assigned for missing material.

## Outputs

- RFP summary
- compliance matrix
- proposal outline
- answer drafts
- gap and owner list
- win theme brief
- response readiness report

## Boundary

This Skill owns RFP analysis, response structure, requirement mapping, and proposal drafting. It does not own final legal approval, pricing approval, certification claims, contract commitments, portal submission, or customer communication.

It must not run shell, Python, Node, npm, curl, MCP, procurement portal, RFP portal, CRM, email, e-signature, Office, package install, submit, or external API commands by itself; those actions belong to XAgent tools visible in the current session.
