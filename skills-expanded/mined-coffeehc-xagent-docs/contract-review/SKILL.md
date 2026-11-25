---
name: contract-review
description: Use when reading, summarizing, reviewing, comparing, redlining conceptually, or extracting risks from contracts, agreements, terms, order forms, SOWs, NDAs, MSAs, DPAs, procurement terms, service terms, employment-related agreements, licensing terms, or renewal documents. Prefer this Skill for contract understanding and issue spotting, not formal legal advice or legal approval.
meta:
  version: 1
  display_name: 合同审查
---

# Contract Review

## Purpose

Review contracts and related commercial terms for structure, obligations, rights, risks, missing facts, negotiation issues, and human-review points. The Skill helps an agent understand and inspect contract language; it does not provide legal advice or approve execution.

This Skill is process-only and does not depend on legal databases, e-signature systems, contract lifecycle systems, OCR, Office automation, or scripts.

## Use When

Use for:

- summarizing or reviewing NDAs, MSAs, DPAs, SOWs, order forms, terms of service, procurement terms, vendor contracts, customer contracts, license terms, employment-related agreements, renewals, or amendments;
- extracting parties, dates, term, renewal, fees, payment, deliverables, service levels, acceptance, IP, confidentiality, data protection, liability, indemnity, termination, dispute, governing law, and assignment clauses;
- comparing versions, spotting risky or unusual terms, preparing negotiation questions, or creating a human legal-review checklist;
- translating contract content into business obligations, operational owner questions, or risk notes.

Use `document-understanding` when the task is only reading or summarizing one document without contract-specific risk review. Use `policy-analysis` for external laws and regulations. Use `compliance-review` when checking internal controls or policy adherence.

## Do Not Use When

Do not use for:

- formal legal advice, legal opinion, enforceability judgment, jurisdiction-specific legal conclusion, or final approval to sign;
- drafting binding legal language for execution without lawyer review;
- submitting, signing, redlining in a live system, sending, filing, or negotiating with counterparties;
- tax, accounting, regulatory, HR, privacy, security, or procurement approval;
- claiming a clause is valid, invalid, enforceable, or unenforceable as a definitive legal conclusion.

## Material Gate

Before reviewing, identify:

- document type, parties, jurisdiction if stated, governing law, version, date, status, and whether this is a draft, final, amendment, order form, or referenced document;
- user role and goal: buyer, seller, vendor, customer, employer, employee, investor, operator, reviewer, or neutral summary;
- review depth: quick summary, issue spotting, clause extraction, risk register, version comparison, negotiation checklist, or business-obligation handoff;
- source scope: provided text only, attachments, referenced policies, exhibits, schedules, or missing linked documents;
- risk sensitivity: financial exposure, data, IP, confidentiality, liability, termination, exclusivity, compliance, regulated industry, or urgent deadline.

If referenced documents or material clauses are missing, mark them `待确认`. Do not invent contract terms, law, party intent, or enforceability conclusions.

## Workflow

1. Confirm the contract object, source scope, user goal, and review depth.
2. Build a contract map: parties, purpose, term, effective date, renewal, commercial terms, deliverables, obligations, rights, dependencies, and referenced documents.
3. Extract explicit text separately from interpretation, business implication, and legal-review question.
4. Review clause families using `references/contract-review-rules.md`.
5. Identify risks by type: financial, operational, legal-review, compliance, privacy/data, security, IP, confidentiality, liability, indemnity, termination, exclusivity, service-level, change-control, assignment, dispute, or ambiguity.
6. Classify risk severity only when facts support it. Explain why the issue matters and who should review it.
7. If comparing versions, use `references/version-comparison-rules.md` to separate additions, removals, stricter terms, relaxed terms, ambiguous edits, and commercial impact.
8. Produce the user's requested output without presenting it as legal advice.
9. Route high-impact or jurisdiction-specific issues to qualified legal, compliance, procurement, privacy, tax, accounting, HR, or security review.

## Checks

- Document type, version, parties, dates, governing law if present, status, and inspected scope are visible.
- Direct contract text, summary, inference, and reviewer questions are separated.
- Missing referenced documents, schedules, exhibits, definitions, or attachments are marked.
- Important obligations, deadlines, notice requirements, fees, limitations, and termination triggers are not silently skipped.
- Risk labels explain business consequence and review owner.
- The output does not claim to be legal advice, enforceability analysis, or final approval to sign.

## Outputs

Return the form the user asks for: contract summary, clause extraction, obligation table, risk register, negotiation checklist, version comparison, missing-document list, legal-review questions, business-owner handoff, or concise issue-spotting notes.

## Boundary

Skill owns contract understanding workflow, clause mapping, obligation extraction, risk issue spotting, missing-document surfacing, comparison framing, and human-review checklist creation.

This Skill does not provide formal legal advice, legal opinion, enforceability judgment, compliance approval, tax advice, accounting advice, HR approval, procurement approval, privacy approval, security approval, negotiation authority, signature approval, or final business approval.

It must not run shell, Python, Node, npm, curl, MCP, OCR, legal database, CLM, e-signature, procurement, email, CRM, Office, or document-export commands by itself; those actions belong to XAgent tools visible in the current session.

## Resources

- `references/contract-review-rules.md`: clause families, risk categories, obligation extraction, and review discipline.
- `references/version-comparison-rules.md`: contract version comparison and change impact rules.
- `LICENSE`: source and license notice.
