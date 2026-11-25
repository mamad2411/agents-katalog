---
name: "rbac"
description: "RBAC multi-tenant patterns: role tables, permission checks, row-level scoping, organization isolation, middleware guards for Next.js and Express/FastAPI"
---

# RBAC Multi-Tenant Skill

## When to activate
- Building a multi-tenant SaaS where users belong to organizations
- Implementing role-based access control (admin, editor, viewer, etc.)
- Scoping database queries so users only see their organization's data
- Adding permission middleware to API routes
- Designing the database schema for roles and permissions

## When NOT to use
- Single-tenant apps where all authenticated users have the same access
- Simple boolean `isAdmin` checks — only worth the complexity at 3+ roles
- When Better Auth's built-in organization plugin covers your needs (check that first)

## Instructions

### Database schema

```typescript
// db/schema.ts — Drizzle
import { pgTable, text, uuid, timestamp, pgEnum, unique } from 'drizzle-orm/pg-core'
import { relations } from 'drizzle-orm'

export const roleEnum = pgEnum('role', ['owner', 'admin', 'editor', 'viewer'])

export const organizations = pgTable('organizations', {
  id:        uuid('id').primaryKey().defaultRandom(),
  name:      text('name').notNull(),
  slug:      text('slug').notNull().unique(),
  plan:      text('plan', { enum: ['free', 'pro', 'enterprise'] }).default('free').notNull(),
  createdAt: timestamp('created_at').defaultNow().notNull(),
})

export const users = pgTable('users', {
  id:    uuid('id').primaryKey().defaultRandom(),
  email: text('email').notNull().unique(),
  name:  text('name'),
})

// Many-to-many: users ↔ organizations with a role
export const memberships = pgTable('memberships', {
  id:             uuid('id').primaryKey().defaultRandom(),
  userId:         uuid('user_id').notNull().references(() => users.id, { onDelete: 'cascade' }),
  organizationId: uuid('organization_id').notNull().references(() => organizations.id, { onDelete: 'cascade' }),
  role:           roleEnum('role').notNull().default('viewer'),
  createdAt:      timestamp('created_at').defaultNow().notNull(),
}, (t) => ({
  uniqueMember: unique().on(t.userId, t.organizationId),  // one role per user per org
}))

// All data belongs to an organization
export const projects = pgTable('projects', {
  id:             uuid('id').primaryKey().defaultRandom(),
  organizationId: uuid('organization_id').notNull().references(() => organizations.id, { onDelete: 'cascade' }),
  name:           text('name').notNull(),
  createdById:    uuid('created_by_id').references(() => users.id),
})

// Relations
export const membershipsRelations = relations(memberships, ({ one }) => ({
  user:         one(users, { fields: [memberships.userId], references: [users.id] }),
  organization: one(organizations, { fields: [memberships.organizationId], references: [organizations.id] }),
}))
```

### Permission helper

```typescript
// lib/permissions.ts
export type Role = 'owner' | 'admin' | 'editor' | 'viewer'

const ROLE_HIERARCHY: Record<Role, number> = {
  owner:  40,
  admin:  30,
  editor: 20,
  viewer: 10,
}

// Check if role has sufficient privilege level
export function hasRole(userRole: Role, requiredRole: Role): boolean {
  return ROLE_HIERARCHY[userRole] >= ROLE_HIERARCHY[requiredRole]
}

// Permission matrix — what each role can do
export const PERMISSIONS = {
  'projects:create': ['owner', 'admin', 'editor'] as Role[],
  'projects:delete': ['owner', 'admin'] as Role[],
  'members:invite':  ['owner', 'admin'] as Role[],
  'members:remove':  ['owner', 'admin'] as Role[],
  'billing:manage':  ['owner'] as Role[],
  'org:delete':      ['owner'] as Role[],
} as const

export type Permission = keyof typeof PERMISSIONS

export function can(role: Role, permission: Permission): boolean {
  return PERMISSIONS[permission].includes(role)
}
```

### Getting the current user's role in an organization

```typescript
// lib/auth-helpers.ts
import { db } from '@/db'
import { memberships } from '@/db/schema'
import { eq, and } from 'drizzle-orm'
import type { Role } from './permissions'

export async function getUserRole(
  userId: string,
  orgId: string
): Promise<Role | null> {
  const membership = await db.query.memberships.findFirst({
    where: and(
      eq(memberships.userId, userId),
      eq(memberships.organizationId, orgId)
    ),
    columns: { role: true },
  })
  return membership?.role ?? null
}

export async function requireRole(
  userId: string,
  orgId: string,
  minRole: Role
): Promise<Role> {
  const role = await getUserRole(userId, orgId)
  if (!role || !hasRole(role, minRole)) {
    throw new ForbiddenError(`Requires ${minRole} role`)
  }
  return role
}
```

### Next.js — Server Action with RBAC

```typescript
// lib/actions/projects.ts
'use server'
import { auth } from '@/lib/auth'
import { headers } from 'next/headers'
import { requireRole, can } from '@/lib/permissions'
import { db } from '@/db'
import { projects } from '@/db/schema'

export async function createProject(orgId: string, name: string) {
  const session = await auth.api.getSession({ headers: await headers() })
  if (!session) throw new Error('Unauthorized')

  // Check permission
  await requireRole(session.user.id, orgId, 'editor')

  return db.insert(projects).values({
    organizationId: orgId,
    name,
    createdById: session.user.id,
  }).returning()
}

export async function deleteProject(projectId: string, orgId: string) {
  const session = await auth.api.getSession({ headers: await headers() })
  if (!session) throw new Error('Unauthorized')

  const role = await requireRole(session.user.id, orgId, 'admin')

  // Extra check for specific permission
  if (!can(role, 'projects:delete')) throw new ForbiddenError('Cannot delete projects')

  await db.delete(projects).where(eq(projects.id, projectId))
}
```

### Row-level scoping — every query filters by org

```typescript
// lib/queries/projects.ts
import { db } from '@/db'
import { projects } from '@/db/schema'
import { eq, and } from 'drizzle-orm'

// Always scope queries to the current organization
export async function getProjects(orgId: string) {
  return db.select().from(projects)
    .where(eq(projects.organizationId, orgId))   // ← critical: always filter by org
    .orderBy(projects.createdAt)
}

export async function getProject(projectId: string, orgId: string) {
  // Include orgId in WHERE — prevents horizontal privilege escalation
  return db.query.projects.findFirst({
    where: and(
      eq(projects.id, projectId),
      eq(projects.organizationId, orgId)         // ← validates ownership
    ),
  })
}
```

### Express/Fastify middleware

```typescript
// middleware/rbac.ts
import { getUserRole, hasRole } from '@/lib/permissions'
import type { Role } from '@/lib/permissions'

export function requireOrgRole(minRole: Role) {
  return async (req: Request, res: Response, next: NextFunction) => {
    const userId = req.user?.id
    const orgId = req.params.orgId ?? req.body.orgId

    if (!userId || !orgId) {
      return res.status(401).json({ error: 'Unauthorized' })
    }

    const role = await getUserRole(userId, orgId)
    if (!role || !hasRole(role, minRole)) {
      return res.status(403).json({ error: `Requires ${minRole} role` })
    }

    req.userRole = role  // attach for downstream use
    next()
  }
}

// Usage
router.delete('/orgs/:orgId/projects/:id',
  requireOrgRole('admin'),
  deleteProjectHandler
)

router.post('/orgs/:orgId/members/invite',
  requireOrgRole('admin'),
  inviteMemberHandler
)
```

### FastAPI dependency (Python)

```python
# dependencies/rbac.py
from fastapi import Depends, HTTPException
from .auth import get_current_user
from .db import get_db

ROLE_HIERARCHY = {"owner": 40, "admin": 30, "editor": 20, "viewer": 10}

def has_role(user_role: str, required_role: str) -> bool:
    return ROLE_HIERARCHY.get(user_role, 0) >= ROLE_HIERARCHY.get(required_role, 0)

def require_org_role(min_role: str):
    async def dependency(
        org_id: str,
        current_user = Depends(get_current_user),
        db = Depends(get_db),
    ):
        membership = await db.memberships.find_one(
            user_id=current_user.id, organization_id=org_id
        )
        if not membership or not has_role(membership.role, min_role):
            raise HTTPException(status_code=403, detail=f"Requires {min_role} role")
        return membership.role

    return dependency

# Usage
@router.delete("/orgs/{org_id}/projects/{project_id}")
async def delete_project(
    project_id: str,
    role = Depends(require_org_role("admin")),
):
    ...
```

### Inviting and managing members

```typescript
// lib/actions/members.ts
export async function inviteMember(orgId: string, email: string, role: Role) {
  const session = await auth.api.getSession({ headers: await headers() })
  if (!session) throw new Error('Unauthorized')

  await requireRole(session.user.id, orgId, 'admin')

  // Check inviter can grant this role (can't grant higher than own role)
  const inviterRole = await getUserRole(session.user.id, orgId)
  if (!inviterRole || ROLE_HIERARCHY[role] > ROLE_HIERARCHY[inviterRole]) {
    throw new ForbiddenError("Cannot grant a role higher than your own")
  }

  // Send invitation...
  await sendInviteEmail({ email, orgId, role, invitedBy: session.user.id })
}

export async function updateMemberRole(orgId: string, memberId: string, newRole: Role) {
  const session = await auth.api.getSession({ headers: await headers() })
  if (!session) throw new Error('Unauthorized')

  const actorRole = await requireRole(session.user.id, orgId, 'admin')

  // Prevent privilege escalation
  if (ROLE_HIERARCHY[newRole] >= ROLE_HIERARCHY[actorRole] && actorRole !== 'owner') {
    throw new ForbiddenError('Cannot assign role equal or higher than your own')
  }

  await db.update(memberships)
    .set({ role: newRole })
    .where(and(eq(memberships.id, memberId), eq(memberships.organizationId, orgId)))
}
```

## Example

**User:** A SaaS project management tool — owners can manage billing and delete the org, admins can invite members and delete projects, editors can create projects, viewers can only read. Implement the schema, permission helper, and middleware for Next.js Server Actions.

**Expected output:**
- `db/schema.ts` — organizations, users, memberships (with role enum), projects tables
- `lib/permissions.ts` — `PERMISSIONS` matrix, `can()`, `hasRole()`, `ROLE_HIERARCHY`
- `lib/auth-helpers.ts` — `getUserRole()`, `requireRole()`
- `lib/actions/projects.ts` — `createProject` (editor+), `deleteProject` (admin+)
- All data queries include `organizationId` filter to prevent cross-org data leaks

---
