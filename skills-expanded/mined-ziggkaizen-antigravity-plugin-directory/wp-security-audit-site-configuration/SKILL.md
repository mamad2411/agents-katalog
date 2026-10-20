---
name: wp-security-audit-site-configuration
description: Audits WordPress site configuration and filesystem posture using read-only evidence. Use for versions, wp-config.php, debug exposure, backups, uploads, permissions, transport, logs, and hosting-control review.
---

# WordPress Site and Configuration Security Audit

## Before starting

- Confirm authorization and environment.
- Identify whether the inspected filesystem is the actual web root, a build artifact, a backup, or a deployment checkout.
- Record WordPress, PHP, database, web-server, proxy/CDN, and hosting versions.
- Do not assume a missing WordPress constant means a control is absent; the host or deployment system may enforce it elsewhere.

## Review areas

1. Supported versions and update posture.
2. Official source and integrity expectations.
3. `wp-config.php` location, access controls, debug settings, keys/salts, file editing, filesystem method, and update policy.
4. Filesystem ownership and permissions.
5. Executable content in uploads.
6. Backup, dump, log, environment, and credential artifacts under the document root.
7. HTTPS, admin transport, proxy awareness, cookies, and trusted headers.
8. Database account privilege and separation.
9. Logging, monitoring, retention, and secret leakage.
10. Backup existence, protection, and restore evidence.
11. Site Health and approved read-only WP-CLI evidence.
12. Hosting, WAF, CDN, and server controls that cannot be inferred from WordPress files.

## Tools

Read [site-configuration-checklist.md](resources/site-configuration-checklist.md).

The bundled scanner is under the reporting skill. Run it with `--help` before use and treat every result as a signal requiring target context.

Use [audit-wordpress-site-configuration-workflow.md](workflows/audit-wordpress-site-configuration-workflow.md) for the full procedure.
