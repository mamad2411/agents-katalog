---
name: wp-security-audit-access-and-data
description: Audits WordPress users, roles, capabilities, authentication surfaces, sessions, privileged workflows, personal data, and exposure boundaries. Use for access-control and data-protection reviews.
---

# WordPress Access and Data Security Audit

## Review areas

- User inventory, inactive accounts, shared accounts, and admin concentration.
- Custom roles, added/removed capabilities, and Multisite differences.
- Application Passwords, API credentials, service accounts, and integration tokens.
- MFA, SSO, password, session, and recovery controls where present.
- Privileged admin, REST, Ajax, cron, import/export, and webhook workflows.
- Object ownership and cross-tenant or cross-user isolation.
- Personal-data collection, storage, export, erasure, retention, and logging.
- Public REST responses, feeds, sitemaps, archives, author exposure, media metadata, and debug output.
- Cookies, sessions, cache variation, and authenticated-response leakage.
- Backup, analytics, observability, and third-party data destinations.

## Principles

- Review capabilities, not role names alone.
- Review object-level authorization independently from broad capabilities.
- Treat service credentials as privileged identities with owners and expiry.
- Collect only the evidence required for the audit.
- Redact personal data and secrets.
- Do not change users, sessions, roles, or credentials during an audit.

Read [access-and-data-checklist.md](resources/access-and-data-checklist.md) and follow [audit-wordpress-access-and-data-workflow.md](workflows/audit-wordpress-access-and-data-workflow.md).
