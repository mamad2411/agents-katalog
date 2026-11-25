---
name: nextjs-zenstack-auth-context-error
description: |
  Fix for "An error occurred in the Server Components render" in Next.js production builds
  when using ZenStack ORM with Better Auth. Use when: (1) Generic Server Components error
  in production with no stack trace, (2) Works in dev but fails in production, (3) Using
  manual db.$setAuth() instead of authenticated client from auth()/requireRole(). Symptoms
  include Sentry errors with digest but no details, or blank error pages. Solution: Always
  use the pre-configured db client from auth() or requireRole() result instead of manually
  creating auth context with db.$setAuth({ id, role }).
author: Claude Code
version: 1.0.0
date: 2026-02-07
---

# Next.js + ZenStack Auth Context Error Fix

## Problem

In Next.js production builds, manually creating ZenStack auth contexts with `db.$setAuth()`
can cause type mismatches that manifest as generic Server Components render errors. The
actual error details are hidden in production for security, making debugging extremely
difficult.

## Context / Trigger Conditions

**When this occurs:**
- Next.js app in **production** shows generic error page
- Sentry/error tracking shows: "An error occurred in the Server Components render. The specific message is omitted in production builds to avoid leaking sensitive details."
- Same code works perfectly in **development** environment
- Using ZenStack ORM with Better Auth
- Using Server Components or Server Actions with database queries

**Specific code pattern that triggers this:**
```typescript
// ❌ ANTI-PATTERN - Causes production errors
const authResult = await auth();
const { user } = authResult;

// Manually creating auth context
const userDB = db.$setAuth({ id: user.id, role: user.role });
```

**Error symptoms:**
- Production: Generic error page with no details
- Sentry: Error with digest ID but no stack trace
- Browser console: Empty (errors are server-side)
- Works in dev, fails in production

## Root Cause

**Type Mismatch in Production:**
1. Better Auth returns user with `role: string | null`
2. ZenStack expects `role: RoleEnum | null | undefined`
3. In development, TypeScript errors are warnings
4. In production builds, type mismatches cause runtime errors
5. Next.js hides error details for security

**Why manual $setAuth() is problematic:**
- Requires explicit type casting that's easy to forget
- Creates redundant auth contexts
- Bypasses the properly-typed auth helpers
- Makes code less maintainable

## Solution

**Always use the pre-configured database client from auth helpers:**

### Pattern 1: Server Components (Use `auth()`)

```typescript
// ✅ CORRECT
import { auth } from "@/lib/auth";

export default async function Page() {
  const authResult = await auth();

  if (!authResult.authenticated) {
    return redirect('/sign-in');
  }

  // Use db from authResult - already configured with correct types
  const { user, db: userDB } = authResult;

  const data = await userDB.profile.findMany();
}
```

### Pattern 2: Protected Routes (Use `requireRole()`)

```typescript
// ✅ CORRECT
import { requireRole } from "@/lib/auth";
import { RoleEnum } from "database/types";

export default async function InstructorPage() {
  const result = await requireRole([RoleEnum.INSTRUCTOR, RoleEnum.ADMIN]);

  if ("redirect" in result) {
    return redirect({ href: result.redirect, locale });
  }

  // Use db from result - already configured with correct types
  const { user, db: userDB } = result;

  const profile = await userDB.profile.findFirst({
    where: { userId: user.id }
  });
}
```

### Pattern 3: Server Actions (Use `getAuthContext()`)

```typescript
// ✅ CORRECT
"use server";

import { getAuthContext } from "./utils";

export async function updateProfile(data: ProfileData) {
  const auth = await getAuthContext();

  if (!auth.authenticated) {
    return auth; // Returns error response
  }

  // Use db from auth - already configured with correct types
  const { user, db } = auth;

  await db.profile.update({
    where: { userId: user.id },
    data
  });
}
```

### Anti-Pattern to Avoid

```typescript
// ❌ WRONG - Causes production errors
import { db } from "database";

const authResult = await auth();
const { user } = authResult;

// DON'T manually create auth context
const userDB = db.$setAuth({ id: user.id, role: user.role });

// Even with type casting, this is an anti-pattern:
const userDB = db.$setAuth({
  ...user,
  role: user.role as RoleEnum | null | undefined
});
```

## Verification

After applying the fix:

1. **Local verification:**
   ```bash
   pnpm lint
   pnpm types
   ```

2. **Production test:**
   - Deploy to production/staging
   - Navigate to the previously failing route
   - Verify page loads without errors
   - Check Sentry for no new occurrences

3. **Code review checklist:**
   ```bash
   # Search for the anti-pattern in your codebase
   grep -r "db\.\$setAuth({ id: user.id, role: user.role })" --include="*.ts" --include="*.tsx"

   # Should return 0 results
   ```

## Example: Real-World Fix

**Before (Broken in Production):**
```typescript
// apps/web/app/[locale]/(app)/settings/calendar/page.tsx
import { db } from "database";

export default async function CalendarPage() {
  const result = await requireRole([RoleEnum.INSTRUCTOR]);
  const { user } = result;

  // ❌ Creating new auth context manually
  const userDB = db.$setAuth({ id: user.id, role: user.role });

  const profile = await userDB.profile.findFirst({
    where: { userId: user.id }
  });
}
```

**After (Works in Production):**
```typescript
// apps/web/app/[locale]/(app)/settings/calendar/page.tsx
export default async function CalendarPage() {
  const result = await requireRole([RoleEnum.INSTRUCTOR]);

  // ✅ Use db from requireRole result
  const { user, db: userDB } = result;

  const profile = await userDB.profile.findFirst({
    where: { userId: user.id }
  });
}
```

## Notes

### Why This Happens

1. **Next.js Security**: Production builds strip error details to avoid leaking sensitive
   information ([Next.js Error Handling docs](https://nextjs.org/docs/app/getting-started/error-handling))

2. **ZenStack Auth Context**: ZenStack requires properly typed auth context for row-level
   security policies ([ZenStack Better-Auth Integration](https://zenstack.dev/docs/recipe/auth-integration/better-auth))

3. **Type Safety**: Better Auth uses discriminated unions for perfect type safety, but
   manual auth context creation bypasses these guarantees

### Related Issues

- If you see "Cannot read properties of undefined" in production but not dev, this could
  be the same root cause
- If auth-related queries work in some pages but not others, check for inconsistent auth
  context patterns

### Prevention Strategy

**Add to your project's CLAUDE.md or contributing guidelines:**

```markdown
## Database Client Usage

**ALWAYS** use the authenticated db client from auth helpers:

✅ Server Components: `const { db } = await auth()`
✅ Protected Routes: `const { db } = await requireRole([...])`
✅ Server Actions: `const { db } = await getAuthContext()`

❌ NEVER manually create auth context: `db.$setAuth({ id, role })`
```

**Add to your linting/pre-commit hooks:**
```bash
# Check for the anti-pattern
if grep -r "db\.\$setAuth({ id: user.id, role: user.role })" \
    --include="*.ts" --include="*.tsx" apps/; then
  echo "Error: Found manual auth context creation. Use auth() or requireRole() instead."
  exit 1
fi
```

## References

- [Next.js Error Handling in Production](https://nextjs.org/docs/app/getting-started/error-handling)
- [ZenStack Better-Auth Integration](https://zenstack.dev/docs/recipe/auth-integration/better-auth)
- [ZenStack Accessing Current User](https://zenstack.dev/docs/the-complete-guide/part1/access-policy/current-user)
- [Better-Auth with ZenStack Blog Post](https://zenstack.dev/blog/better-auth)
