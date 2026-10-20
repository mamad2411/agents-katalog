---
name: multi-tenant-auth
description: Implement tenant isolation in authentication. Use when building
  multi-tenant SaaS auth.
metadata:
  tags: multi, tenant, auth
---

# Multi-Tenant Auth

## Use this skill when
- Managing tenants, users, and membership
- Isolating data and sessions per tenant
- Tenant switching and scoped tokens

## Do not use this skill when
- Single-tenant apps
- Setting up a provider (use openid-connect)

## Instructions
1. Make every tenant claim explicit: tenantId in sessions/tokens.
2. Bind all queries and decisions to tenant scope.
3. Prevent cross-tenant access in code: tenant-scoped queries, not global rows.
4. Handle shared vs isolated schema/row strategies deliberately.
5. Support tenant switching with separate scoped sessions if needed.
6. Audit tenant membership changes.
7. Test cross-tenant access attempts explicitly.

## Checklist
- Tenant claim always present and validated
- Query scoping enforced
- Cross-tenant tests exist

## Output Format
- Tenant model | scoping strategy | session/claim design | isolation tests

## Common Mistakes
- Tenant inferred from URL only
- Global queries that forget tenant filter
- Tenant IDs forgeable in tokens
