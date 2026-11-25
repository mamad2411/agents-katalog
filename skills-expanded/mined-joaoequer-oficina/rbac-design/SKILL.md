---
name: rbac-design
description: Role-based access control design with roles + granular permissions — role × domain matrix, N:N database modeling and an approval process before implementation. Use whenever the project involves permissions, user roles, access control, admin panels or "who can do what" questions in the system.
---

# RBAC design

Badly designed RBAC is guaranteed rework. This is the process and the model that work.

## The model: roles + granular permissions (not pure roles)

Pure roles ("admin can do everything, editor can edit") break at the first real exception. The house model:

- **Permission** = atomic action on a domain (e.g. `task:create`, `document:approve`, `report:export`).
- **Role** = named set of permissions (N:N role ↔ permission).
- **User** receives roles (N:N user ↔ role), and the system resolves the effective permission set.

```prisma
model Role {
  id          String  @id @default(uuid())
  workspaceId String
  name        String
  permissions RolePermission[]
}

model Permission {
  id     String @id @default(uuid())
  domain String   // e.g. "task", "document", "report"
  action String   // e.g. "create", "read", "update", "approve", "delete"
  roles  RolePermission[]
  @@unique([domain, action])
}

model RolePermission {
  roleId       String
  permissionId String
  role         Role       @relation(fields: [roleId], references: [id])
  permission   Permission @relation(fields: [permissionId], references: [id])
  @@id([roleId, permissionId])
}
```

Server-side check via guard/decorator (`@RequirePermission('document:approve')`). The frontend uses permissions only to hide buttons — never as real control.

## The process: matrix before code

**Do not implement RBAC straight into code.** The correct flow:

1. **Map the domains** of the system (the "areas": tasks, documents, users, reports, settings...). Medium systems have 8–15 domains.
2. **Map the real roles** of the client's operation (not the ones you imagine). Usually 5–8 roles are enough; more than that smells like roles that should be standalone permissions.
3. **Build the role × domain matrix** in a readable document (table: rows = roles, columns = domains, cells = allowed actions).
4. **Submit it for approval** by the architect/tech lead and, when it makes sense, the client. The matrix is cheap to change; code and migrations are not.
5. **Only after approval**, implement — and if implementing into an existing system, verify the real codebase first (do not implement against an imagined codebase).

## Known traps

- **Implicit permission**: an undocumented "everyone can read" becomes a security hole when requirements change. Every permission is explicit in the matrix.
- **The ever-growing God role**: the "admin" role that accumulates everything. Acceptable, but record that it is a super-user by design.
- **RBAC without tenant**: in a multi-tenant system, roles and assignments belong to the workspace (`workspaceId` on `Role`). Global roles only with a recorded decision.
- **Premature granularity**: start with standard actions (create/read/update/delete + the 2–3 domain-specific business actions, like "approve"). Do not invent 40 actions per domain on day 1.
