---
name: zenstack-authenticated-db-params
description: |
  Fix TypeScript circular reference errors when passing ZenStack authenticated database
  client as function parameter. Use when: (1) TypeScript error "TS2502: 'db' is referenced
  directly or indirectly in its own type annotation", (2) Utility functions need to accept
  authenticated db from server actions, (3) Using `ReturnType<typeof db.$setAuth>` causes
  circular reference. Solves typing authenticated ZenStack clients in Better Auth + ZenStack
  projects with proper access control enforcement.
author: Claude Code
version: 1.0.0
date: 2026-01-24
---

# ZenStack Authenticated DB Parameter Pattern

## Problem
When creating utility functions that need to accept an authenticated ZenStack database client
(to enforce access control policies), TypeScript throws circular reference errors if you
try to use `ReturnType<typeof db.$setAuth>` directly in the function signature.

## Context / Trigger Conditions
- **TypeScript Error**: `TS2502: 'db' is referenced directly or indirectly in its own type annotation`
- **Project Stack**: ZenStack ORM (built on Prisma) + Better Auth
- **Scenario**: Refactoring utilities to accept authenticated `db` instead of using `baseDB` directly
- **Pattern**: Server actions call utilities and need to pass their authenticated `db` client

## Solution

### Step 1: Import db Client and Create Type Alias

Instead of importing `EnhancedPrismaClient` (which doesn't exist), import the base `db` client
and create a local type alias:

```typescript
// ❌ WRONG - EnhancedPrismaClient doesn't exist
import type { EnhancedPrismaClient } from "database";

export async function myUtil(userId: string, db: EnhancedPrismaClient) {
  // ...
}
```

```typescript
// ✅ CORRECT - Import db client and create local type
import { db as dbClient } from "database";

type AuthenticatedDB = ReturnType<typeof dbClient.$setAuth>;

export async function myUtil(userId: string, db: AuthenticatedDB) {
  // ...
}
```

### Step 2: Update Utility Function Signatures

Use the `AuthenticatedDB` type for all database parameters:

```typescript
"use server";

import { db as dbClient } from "database";

type AuthenticatedDB = ReturnType<typeof dbClient.$setAuth>;

/**
 * Check if account can be deleted
 * @param userId - User ID to check
 * @param db - Authenticated database client
 */
export async function canDeleteAccount(
  userId: string,
  db: AuthenticatedDB,
): Promise<{ canDelete: boolean; reason?: string }> {
  const activeBookings = await db.booking.count({
    where: { userId, status: "ACTIVE" }
  });

  return activeBookings === 0
    ? { canDelete: true }
    : { canDelete: false, reason: "Active bookings exist" };
}
```

### Step 3: Update Caller Sites

Server actions that use `getAuthContext()` already have the authenticated `db`:

```typescript
// In server action
import { getAuthContext } from "./utils";
import { canDeleteAccount } from "@/lib/utils/account-deletion";

export async function deleteAccount(data: unknown): Promise<ActionResult> {
  const auth = await getAuthContext();
  if (!auth.authenticated) return auth;

  // Pass the authenticated db client
  const canDelete = await canDeleteAccount(auth.user.id, auth.db);

  if (!canDelete.canDelete) {
    return { success: false, error: canDelete.reason };
  }

  // ... proceed with deletion
}
```

### Step 4: Handle Transaction Callbacks

For functions using `$transaction`, the transaction callback receives the same type:

```typescript
export async function softDeleteUser(
  userId: string,
  db: AuthenticatedDB
): Promise<void> {
  // Transaction callback infers type from db parameter
  await db.$transaction(async (tx) => {
    // tx is automatically typed as AuthenticatedDB
    await tx.user.update({
      where: { id: userId },
      data: { deletedAt: new Date() }
    });
  });
}
```

## Verification

After applying this pattern:

1. **TypeScript Check**: Run `turbo types` - should pass with no TS2502 errors
2. **Access Control**: Verify that utility functions enforce ZenStack policies:
   ```typescript
   // This should throw/return empty if user lacks access
   const result = await myUtil(userId, auth.db);
   ```
3. **Import Correctness**: Check that utilities import `db as dbClient`, not `baseDB`

## Why This Works

- **Local Type Alias**: Breaks the circular reference by creating an intermediate type
- **Consistent Import Name**: Using `db as dbClient` prevents naming conflicts with the parameter
- **Access Control Preserved**: `AuthenticatedDB` type maintains the `$setAuth()` wrapper, ensuring
  policies are enforced

## Common Mistakes to Avoid

1. **Using `baseDB` in utilities**: Always accept `db` as parameter, never import `baseDB` directly
   (bypasses access control)
2. **Forgetting to update callers**: All call sites must pass `auth.db` or `authContext.db`
3. **Mixing authenticated/unauthenticated clients**: Be consistent - utilities should always require
   authenticated clients

## Example: Complete Refactor

**Before (bypassing access control):**
```typescript
"use server";
import { baseDB } from "database";

export async function deleteUserData(userId: string) {
  await baseDB.user.delete({ where: { id: userId } });
}
```

**After (enforcing access control):**
```typescript
"use server";
import { db as dbClient } from "database";

type AuthenticatedDB = ReturnType<typeof dbClient.$setAuth>;

export async function deleteUserData(
  userId: string,
  db: AuthenticatedDB
) {
  // Access control policies automatically enforced
  await db.user.delete({ where: { id: userId } });
}
```

**Caller (server action):**
```typescript
import { getAuthContext } from "./utils";
import { deleteUserData } from "@/lib/utils/data";

export async function deleteMyData(): Promise<ActionResult> {
  const auth = await getAuthContext();
  if (!auth.authenticated) return auth;

  await deleteUserData(auth.user.id, auth.db);
  return { success: true };
}
```

## Notes

- This pattern applies to ZenStack 3.x with Better Auth integration
- The `AuthenticatedDB` type preserves all ZenStack enhanced methods (findMany, etc.)
- Each utility file needs its own `type AuthenticatedDB` declaration (not exported from database package)
- If utility functions don't need access control, consider whether they should be server actions instead

## References
- [ZenStack Access Control Policies](https://zenstack.dev/docs/guides/access-control)
- [ZenStack with Better Auth](https://zenstack.dev/docs/integrations/better-auth)
- [TypeScript ReturnType Utility](https://www.typescriptlang.org/docs/handbook/utility-types.html#returntypetype)
