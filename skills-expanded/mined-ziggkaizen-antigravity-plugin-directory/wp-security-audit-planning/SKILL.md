---
name: wp-security-audit-planning
description: Plans authorized WordPress security audits by defining scope, environments, assets, evidence rules, allowed techniques, and stop conditions. Use before any site, code, access, supply-chain, or configuration review.
---

# WordPress Security Audit Planning

Use this skill before performing an audit.

## Required inputs

- Authorization owner and evidence.
- Target domains, repositories, installations, environments, and exclusions.
- Exact WordPress, PHP, database, server, plugin, theme, and WP-CLI versions when available.
- Allowed access methods and credentials.
- Allowed and prohibited test techniques.
- Maintenance window, rate limits, data-handling rules, retention, and disclosure contacts.
- Stop conditions and incident-escalation path.

## Procedure

1. Read [audit-scope-matrix.md](resources/audit-scope-matrix.md).
2. Classify each target and environment.
3. Separate code review, configuration review, runtime review, access review, supply-chain review, and external-surface review.
4. Choose passive or read-only evidence sources first.
5. Identify checks that require production access, sensitive data, or active requests.
6. Exclude those checks unless authorization is explicit.
7. Define evidence storage, redaction, and report recipients.
8. Define severity and confidence models before findings are created.
9. Record limitations and unavailable evidence.
10. Use [plan-wordpress-security-audit-workflow.md](workflows/plan-wordpress-security-audit-workflow.md) to produce the audit plan.

## Output

Produce an audit plan with target inventory, authorization, coverage, exclusions, methods, evidence rules, stop conditions, schedule, owners, and reporting path.
