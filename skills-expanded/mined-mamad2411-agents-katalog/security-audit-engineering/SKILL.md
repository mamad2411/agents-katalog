---
name: security-audit-engineering
description: Run a structured application security audit. Use when planning or
  executing a security assessment.
metadata:
  tags: security, audit, engineering
---

# Security Audit Engineering

## Use this skill when
- Planning a security assessment for an app or feature
- Scoping assets, threats, and test depth
- Producing an audit report with priorities

## Do not use this skill when
- Pointed remediation in code (use full-stack-security-engineer)
- Infrastructure-specific audits (use its own skill)

## Instructions
1. Scope the audit: assets, trust boundaries, data sensitivity, threat model.
2. Choose depth: dependency scan, SAST review, manual logic review, DAST/live tests.
3. Run each chosen layer and record evidence for every claim.
4. Reconfirm high-severity findings with reproduction steps.
5. Prioritize: likelihood × impact, factoring in exposure and data sensitivity.
6. Write a report with executive summary, findings, remediation plan, and timelines.
7. Verify remediations by re-testing.

## Checklist
- Every finding has evidence/repro
- Severity is justified
- Findings map to fixes

## Output Format
- Scope | methodology | findings (sev/impact/fix) | exec summary

## Common Mistakes
- Untested claims as “vulnerabilities”
- Scope creep beyond evidence
- Reporting without remediation
