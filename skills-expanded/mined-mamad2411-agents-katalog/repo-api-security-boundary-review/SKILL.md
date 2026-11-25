---
name: repo-api-security-boundary-review
description: Reviews API authentication, authorization, tenancy, ownership checks, privacy, sensitive fields, exports, filters, search, webhooks, and data exposure boundaries. Use when API work may expose or mutate protected resources.
---

# Repository API Security Boundary Review

Use this skill to review security boundaries in API design.

## When to Use This Skill

Use when API work involves authentication, authorization, roles, scopes, permissions, ownership, tenancy, user IDs, organization IDs, exports, reports, search, filtering, includes, expands, bulk access, webhooks, event payloads, sensitive fields, audit logging, admin operations, or elevated operations.

## Process

1. Identify caller identity.
2. Identify resource ownership and tenant boundary.
3. Define permission checks.
4. Minimize response fields.
5. Check sensitive data exposure.
6. Check logs and audit needs.
7. Check tests for unauthorized, cross-tenant, and privilege-escalation cases.

## Workflow

Use `workflows/api-security-boundary-review-workflow.md`.

## Resources

- `resources/api-auth-data-boundary-checklist.md`
