---
name: wp-security-audit-code-review
description: Reviews custom WordPress plugin, theme, block, REST, Ajax, cron, upload, database, and HTTP code for security weaknesses. Use for source audits and remediation verification, not for exploit development.
---

# WordPress Security Code Review

## Review model

Trace data and authority from entry point to side effect or output:

1. Entry point and reachability.
2. Authentication state.
3. Capability and object-level authorization.
4. CSRF/nonce handling where relevant.
5. Input type, shape, validation, sanitization, and canonicalization.
6. Business-state and ownership checks.
7. Database, filesystem, upload, HTTP, command, deserialization, or code-execution sink.
8. Output context and escaping.
9. Error handling, logging, and secret exposure.
10. Tests and bypass paths.

## WordPress attack surfaces

- REST routes and `permission_callback`.
- `wp_ajax_*` and `wp_ajax_nopriv_*`.
- `admin_post_*` and public form handlers.
- Shortcodes, blocks, widgets, template callbacks, and dynamic rendering.
- Cron callbacks, webhooks, imports, exports, and background jobs.
- File uploads, media processing, archives, and generated files.
- Options, metadata, user metadata, and custom tables.
- Outbound HTTP requests and redirects.
- Direct PHP file access and custom endpoints.

## Procedure

1. Read [code-security-review-checklist.md](resources/code-security-review-checklist.md).
2. Inventory entry points and privileged side effects.
3. Trace attacker-controlled values and authorization decisions.
4. Distinguish nonce checks from capabilities.
5. Review output at the final rendering context.
6. Verify dynamic SQL values and identifiers separately.
7. Review uploads, HTTP, redirects, deserialization, and secrets.
8. Confirm exploitability only when reachability and preconditions are established.
9. Use [security-finding-examples.md](examples/security-finding-examples.md) for report style.
10. Follow [review-wordpress-security-code-workflow.md](workflows/review-wordpress-security-code-workflow.md).
