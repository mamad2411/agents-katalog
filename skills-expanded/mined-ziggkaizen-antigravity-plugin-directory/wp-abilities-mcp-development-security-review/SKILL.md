---
name: wp-abilities-mcp-development-security-review
description: Threat-models WordPress Abilities and MCP exposure. Use when reviewing permissions, users, object access, data minimization, side effects, prompt injection, transports, logs, or production risk.
---

# Security Review

## Review Areas

- Actors and trust boundaries.
- Authentication versus authorization.
- Capability and object-level checks.
- Schema abuse, oversized input, expensive queries, and repeated execution.
- Sensitive output and cross-tenant/site leakage.
- Destructive or non-idempotent behavior.
- Default-server discovery versus custom-server curation.
- Dedicated MCP users and Application Password lifecycle.
- Prompt injection and untrusted content returned to agents.
- Proxy, logs, local config, process environment, and transport security.
- Disablement, incident response, and audit evidence.

Use `workflows/threat-model-and-review-workflow.md` and `resources/mcp-security-checklist.md`.

## Non-Negotiable Rules

- Never treat `meta.mcp.public` as authorization.
- Never expose a mutating Ability with `__return_true`.
- Never commit credentials.
- Never return more data than the task requires.
- Never let untrusted content silently choose a different Ability, target object, or privileged input.
