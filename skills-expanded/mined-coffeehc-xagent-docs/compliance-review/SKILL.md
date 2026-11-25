---
name: compliance-review
description: Use when reviewing internal materials, workflows, controls, policies, procedures, reports, product behavior, operational processes, evidence, or artifacts against stated compliance requirements, internal policies, regulatory obligations, audit criteria, risk controls, or governance standards. Prefer this Skill for compliance gap analysis and evidence-based control review, not policy interpretation alone, legal advice, or final compliance approval.
meta:
  version: 1
  display_name: 合规审查
---

# Compliance Review

## Purpose

Review materials, workflows, controls, or operational evidence against defined compliance criteria. The Skill identifies applicable requirements, maps evidence to controls, finds gaps, assesses severity, and produces remediation or escalation points for human review.

This Skill is process-only and does not depend on GRC tools, ticketing systems, audit systems, legal databases, policy databases, scanners, or scripts.

## Use When

Use for:

- checking internal documents, workflows, product behavior, operating procedures, reports, logs, evidence packets, or control descriptions against known requirements;
- mapping policies, regulations, standards, audit criteria, contractual controls, privacy/security obligations, or internal governance rules to current practice;
- producing compliance gap analysis, evidence matrix, control review notes, risk register, remediation checklist, or audit-prep summary;
- reviewing whether obligations from `policy-analysis` or `contract-review` are reflected in internal process or artifacts.

Use `policy-analysis` when the main task is interpreting external policy or regulation. Use `contract-review` when obligations come mainly from a contract. Use `document-understanding` when the main task is only reading source material.

## Do Not Use When

Do not use for:

- formal legal advice, legal opinion, regulatory interpretation as final authority, audit opinion, certification, or compliance sign-off;
- penetration testing, vulnerability scanning, automated evidence collection, filing, reporting to regulators, or submitting attestations;
- creating fake evidence, backdating controls, hiding deficiencies, or claiming compliance without evidence;
- approving financial statements, tax positions, HR decisions, privacy notices, security exceptions, or regulated filings.

## Material Gate

Before reviewing, identify:

- requirement source: policy, regulation, standard, contract, audit criterion, internal control, procedure, checklist, or user-provided rule;
- review object: document, workflow, process, product behavior, control, evidence set, team practice, system configuration, or report;
- scope: jurisdiction, business unit, product, time period, data type, user group, vendor, system, and excluded areas;
- evidence available: source documents, logs, screenshots, approvals, records, tickets, policies, training records, attestations, or user statements;
- review depth: quick gap check, control mapping, audit prep, remediation plan, risk register, or management summary;
- confidence limits: missing evidence, stale policy, unclear owner, sample size, unverified implementation, or pending legal/compliance interpretation.

If requirements or evidence are missing, mark the review as incomplete and use `待确认`. Do not infer compliance from absence of evidence.

## Workflow

1. Define the compliance question, review object, requirement source, source authority, and review scope.
2. Separate requirements, evidence, interpretation, assumptions, gaps, risks, and remediation suggestions.
3. Build a requirement-to-evidence map using `references/compliance-review-rules.md`.
4. For each requirement, classify status only when evidence supports it: met, partially met, not met, not applicable, or unknown.
5. Identify gaps: missing policy, missing owner, missing procedure, missing evidence, design gap, implementation gap, monitoring gap, approval gap, training gap, retention gap, or auditability gap.
6. Assess severity based on impact, likelihood, exposure, enforcement/audit sensitivity, affected users/data, repeatability, and remediation effort.
7. Produce remediation actions with owner, evidence needed, priority, dependency, and follow-up method when known.
8. Use `references/evidence-rules.md` when evidence quality, audit readiness, or source reliability matters.
9. Route high-impact or regulated conclusions to qualified legal, compliance, risk, security, privacy, finance, HR, or audit review.

## Checks

- Requirement source and review object are explicit.
- Requirements are not mixed with assumptions.
- Evidence is linked to the requirement it supports.
- Missing evidence is not treated as proof of compliance.
- Status labels have support and uncertainty is visible.
- Gaps include risk, consequence, owner, and next evidence or remediation step when known.
- The output does not claim final legal, audit, regulatory, security, privacy, tax, HR, or financial approval.

## Outputs

Return the form the user asks for: compliance gap analysis, requirement-to-evidence matrix, control review, audit-prep checklist, risk register, remediation plan, management summary, open-question list, or handoff context. Do not force a fixed template when the user needs a short review.

## Boundary

Skill owns compliance review workflow, requirement mapping, evidence discipline, gap classification, severity framing, remediation suggestion, audit-prep structure, and escalation points.

This Skill does not provide formal legal advice, compliance approval, audit opinion, certification, regulatory assurance, security approval, privacy approval, tax advice, accounting advice, HR approval, or final business approval.

It must not run shell, Python, Node, npm, curl, MCP, scanners, GRC, ticketing, audit system, legal database, policy database, filing, regulator portal, email, CRM, Office, or document-export commands by itself; those actions belong to XAgent tools visible in the current session.

## Resources

- `references/compliance-review-rules.md`: requirement mapping, gap types, status labels, severity, and remediation rules.
- `references/evidence-rules.md`: evidence quality, audit readiness, and source reliability rules.
- `LICENSE`: source and license notice.
