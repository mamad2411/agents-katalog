---
name: wp-woocommerce-10-audit
description: Audits a WooCommerce 10.x store or codebase for compatibility, data integrity, checkout safety, security, performance, operations, and upgrade readiness. Use for pre-release, pre-update, takeover, incident follow-up, or architecture review.
---

# WooCommerce 10 Audit

Use this skill for a structured review without making store changes.

## Audit boundaries

- Default to read-only evidence.
- Do not request or expose live payment credentials, consumer secrets, customer exports, or full order records.
- Separate source review from live-store access.
- State unavailable evidence rather than inventing results.
- Classify findings by severity, evidence, business effect, and remediation owner.

Read:

- `resources/store-audit-checklist.md`
- `workflows/audit-woocommerce-store-workflow.md`

Use the data scanner from `wp-woocommerce-10-data-and-hpos` when custom PHP is available.

## Finding format

For each finding provide:

- ID and severity.
- Evidence path, command output, or configuration.
- Commerce impact.
- Why it matters for WooCommerce 10.x.
- Safe remediation.
- Validation and rollback.
- Whether human approval is required.

## Priority model

- Critical: active compromise, payment/order corruption, exposed secrets, or destructive operation in progress.
- High: likely transaction/data loss, authorization bypass, HPOS-incompatible writes, or checkout outage risk.
- Medium: maintainability, observability, performance, test, or compatibility weakness.
- Low: documentation or minor quality improvement.

## Output expected from the agent

- Scope and versions.
- Evidence collected and missing.
- Executive risk summary.
- Prioritized findings.
- Remediation sequence.
- Release/update readiness decision.
