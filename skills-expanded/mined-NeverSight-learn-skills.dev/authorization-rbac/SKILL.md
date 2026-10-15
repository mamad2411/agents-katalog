---
name: authorization-rbac
description: Use when controlling what a user may do — implement role-based access control with a central permission map, server-side checks on every mutation, and a typed `can()` helper instead of scattered role string comparisons.
---

# Authorization (RBAC)

## Overview

Authentication says *who you are*; authorization says *what you may do*. Avoid `if (role === "admin")` sprinkled everywhere — it drifts and leaks. Define a **single permission matrix** mapping roles to actions, expose one typed `can(role, action)` helper, and call it on the server before every mutation. When rules outgrow roles, graduate to resource-level checks (ownership) without changing call sites.

## When to use

- Different roles (owner/admin/member) get different capabilities.
- Any mutation needs a "is this user allowed?" check.
- You're comparing role strings inline in handlers or components.

## The pattern

```ts
// src/server/auth/permissions.ts
export type Role = "owner" | "admin" | "member";
export type Action =
  | "project:create" | "project:delete"
  | "member:invite" | "member:remove"
  | "billing:manage";

const MATRIX: Record<Role, Action[]> = {
  owner:  ["project:create", "project:delete", "member:invite", "member:remove", "billing:manage"],
  admin:  ["project:create", "project:delete", "member:invite"],
  member: ["project:create"],
};

export function can(role: Role, action: Action): boolean {
  return MATRIX[role]?.includes(action) ?? false;
}

export function authorize(role: Role, action: Action): void {
  if (!can(role, action)) {
    const e = new Error("Forbidden");
    (e as any).status = 403;
    throw e;
  }
}
```

Enforce in the action/handler, after resolving the tenant:

```ts
const { role, org } = await requireOrg(params.org);
authorize(role, "project:delete");      // throws 403 if not allowed
await deleteProject(org.id, projectId); // DAL still scopes by org_id
```

## Beyond roles

- **Resource ownership:** "only the creator or an admin can edit" → check `row.createdBy === user.id || can(role, ...)`.
- **Keep the matrix data, not code paths** — adding a permission is a one-line edit, fully typed by the `Action` union.
- **Mirror in the UI** with the same `can()` to hide buttons — but the server check is the real gate.

## Pitfalls

- **Authorizing in the client only** — hiding a button isn't security; the endpoint must check.
- **Role checks scattered inline** — they fall out of sync; centralize in the matrix.
- **Confusing tenancy with RBAC** — `multi-tenancy` ensures it's *your org's* data; RBAC ensures *you're allowed* to act on it. You need both.
- **Defaulting unknown actions to allow** — default-deny (`?? false`).
- **Forgetting ownership rules** — role alone can't express "your own drafts"; add resource checks.

## Hand-off

A typed `can()` / `authorize()` enforced on the server. Pair with `data-access-layer` (which still scopes by org) and surface allowed actions to the UI.
