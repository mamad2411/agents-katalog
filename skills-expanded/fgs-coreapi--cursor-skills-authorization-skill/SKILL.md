---
name: authorization
description: Add FGS permission checks, roles, or AllowAnonymous/S2S exceptions. Use when securing endpoints, adding permission codes, or changing RBAC.
---

# Authorization

Read [docs/ai/authorization.md](../../../docs/ai/authorization.md).

## Steps

1. Reuse `FgsPermissionCodes` + `[RequirePermission]` on mutating (and view) actions as neighbors do.
2. New code: add constant, persist `identity.FgsPermission` seed (`FgsPermission_Seed.sql`), assign via existing RolePermission APIs — do not invent policies.
3. `[AllowAnonymous]` only for auth/invite/signup/internal-key clones.
4. Internal S2S: `X-FGS-Internal-Service-Key`; do not add JWT between services.
5. Tenant admin bypass is already in `PermissionAuthorizationFilter` — do not reimplement.

## Verify

- [ ] Permission seed + code match
- [ ] No anonymous tenant CRUD
- [ ] Tests if Role/Permission handlers changed
