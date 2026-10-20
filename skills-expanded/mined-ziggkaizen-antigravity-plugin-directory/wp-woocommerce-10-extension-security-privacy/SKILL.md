---
name: wp-woocommerce-10-extension-security-privacy
description: Reviews a WooCommerce 10 extension's authorization, input and output handling, checkout/payment safety, webhooks, remote requests, secrets, logs, customer data, privacy lifecycle, and uninstall behavior. Use for security or privacy review and before release.
---

# wp-woocommerce-10-extension-security-privacy

Use this skill for threat modeling, code review, incident-prone flows, external integrations, payment or checkout work, customer data, logs, support diagnostics, or release approval.

## Required Inputs

- User roles, capabilities, ownership rules, entry points, and trust boundaries.
- Data inventory and classification.
- Admin actions, Ajax, REST, Store API, webhooks, cron/scheduled actions, CLI, imports, exports, and remote integrations.
- Secret storage and rotation model.
- Logging, analytics, support bundle, retention, export, erasure, and uninstall behavior.
- Transaction-sensitive operations and idempotency mechanism.

## Review Priorities

1. Authentication, authorization, object ownership, and nonce role.
2. Input validation, canonicalization, sanitization, and output escaping.
3. SQL, file, upload, redirect, remote request, SSRF, and deserialization boundaries.
4. Webhook authenticity, replay protection, ordering, retries, and duplicate delivery.
5. Payment, order, stock, coupon, tax, shipping, and customer state integrity.
6. Secret exposure in code, browser bundles, logs, errors, fixtures, and packages.
7. Personal-data minimization, consent, retention, export, erasure, and uninstall.
8. Dependency provenance, update behavior, and failure modes.

## Workflow

Use [`workflows/review-extension-security-workflow.md`](workflows/review-extension-security-workflow.md).

## Resource

Use [`resources/security-privacy-checklist.md`](resources/security-privacy-checklist.md).

## Completion Evidence

Return risk-ranked findings with path/evidence, impact, exploit or failure preconditions, concrete fix, test, and release decision. Distinguish confirmed defects from static-review candidates.
