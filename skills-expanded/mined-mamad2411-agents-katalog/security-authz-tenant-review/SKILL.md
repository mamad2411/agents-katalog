---
name: security-authz-tenant-review
description: "Review changes to object authorization, tenant isolation, roles, ownership, or workflow permissions."
---

# Security Authz Tenant Review

Check object-level authorization, tenant context, role assumptions, workflow state, negative tests, and bypass paths.

## Trigger boundary

Use this skill when a change resolves identity to an object, tenant, role, ownership, or workflow permission, or could expose cross-tenant data or actions.

Do not load it for a small local rename, comment, formatting change, or mechanical edit with no authorization, tenant, object, role, ownership, or workflow behavior impact; follow the repository's established convention directly.

## Evidence

Prefer code, tests, logs, config, API contracts, and data examples over assumptions.

## Focused References

- [01-authorization-tenant-review.md](./references/01-authorization-tenant-review.md) - Authorization Tenant Review
