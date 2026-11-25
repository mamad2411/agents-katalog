---
name: wp-plugin-development-secure
description: Threat-models and reviews WordPress plugin entry points, authorization, request intent, input, output, storage, files, remote calls, secrets, privacy, and logging. Use for security-sensitive implementation or review.
---

# WordPress Plugin Security Review

Use this skill for any feature that accepts input, changes state, exposes data, handles files, calls external services, stores credentials, or processes personal data.

## Inputs to collect

- Every admin, frontend, REST, Ajax, cron, webhook, CLI, activation, upgrade, and uninstall entry point.
- Actor, authentication state, required capability, object ownership, and tenant/site scope for each action.
- Request-intent mechanism such as a nonce, signature, or authenticated machine credential.
- Input source, expected type, accepted values, normalization, and rejection behavior.
- Output context: HTML text, attribute, URL, JavaScript, JSON, SQL, header, redirect, log, or file.
- Data classification, retention, export, erasure, and logging requirements.
- Remote hosts, redirects, timeouts, response-size limits, and trust assumptions.

## Method

1. Build an entry-point and trust-boundary inventory with [request and output trust boundaries](resources/request-and-output-trust-boundaries.md).
2. Apply the [security review checklist](resources/security-review-checklist.md) to each boundary.
3. Verify authorization independently of request intent. A nonce is not a capability check.
4. Validate type, shape, range, enum membership, ownership, and state transitions before sanitizing accepted values.
5. Sanitize on ingress when storage or normalized processing requires it; escape late for the exact output context.
6. Use `$wpdb->prepare()` or higher-level WordPress APIs for variable database values. Keep identifiers from fixed allowlists.
7. Review file paths, MIME/content checks, archive handling, upload permissions, and executable-file risk.
8. Review HTTP allowlists, SSRF risk, redirect handling, timeouts, TLS verification, credentials, and response bounds.
9. Add negative tests for unauthorized, unauthenticated, stale/invalid-intent, malformed, cross-object, and replay attempts.
10. Use the [secure admin action](examples/secure-admin-action-example.md) and [secure REST endpoint](examples/secure-rest-endpoint-example.md) only as patterns, not drop-in authorization policy.
11. Run the [security review workflow](workflows/security-review-workflow.md).

## Non-negotiable rules

- Never use `is_admin()` as authorization.
- Never treat sanitization as proof that a value is allowed.
- Never expose a private mutation route with `permission_callback` set to `__return_true`.
- Never build SQL by concatenating request values.
- Never output stored values without context-aware escaping.
- Never log passwords, tokens, cookies, nonce values, personal data, or full third-party payloads by default.
- Never commit application passwords, API keys, signing secrets, or production credentials.
- Never delete user data on deactivation.
- Never perform a remote submission, destructive migration, or irreversible cleanup without explicit approval.

## Required output

Report findings by severity with:

- affected path and entry point
- threat and realistic impact
- evidence
- required fix
- negative test or verification step
- residual risk or explicit false-positive rationale
