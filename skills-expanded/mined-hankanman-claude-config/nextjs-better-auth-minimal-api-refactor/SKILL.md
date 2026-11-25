---
name: nextjs-better-auth-minimal-api-refactor
description: |
  Refactor Next.js + Better Auth authentication to minimal API with discriminated unions.
  Use when: (1) Too many auth helper functions causing maintenance burden, (2) Want perfect
  type safety without optional chaining, (3) Need to optimize auth performance with aggressive
  cookie caching, (4) Using Better Auth v1.4+ with Next.js 16 App Router and ZenStack ORM.
  Covers progressive refactoring from backward-compatible to breaking changes, discriminated
  union type patterns, and systematic multi-file migration.
author: Claude Code
version: 1.0.0
date: 2026-02-07
---

# Next.js Better Auth Minimal API Refactor

## Problem

Authentication code has proliferated into many helper functions (`getUser()`, `isAdmin()`,
`requireAuth()`, `getAuthenticatedUser()`, etc.) across the codebase, causing:
- Maintenance burden (multiple functions doing similar things)
- Inconsistent patterns across files
- Optional chaining everywhere (`user?.name`)
- Performance issues (multiple database queries per auth check)

## Context / Trigger Conditions

Use this skill when:
- Using **Better Auth v1.4+** with Next.js 16 App Router
- Have **ZenStack ORM** for database access with auth context
- Currently have **5+ auth helper functions** scattered across codebase
- Want **perfect TypeScript type safety** (no optional chaining)
- Need to **optimize performance** (reduce DB queries to near zero)
- Ready for **breaking changes** (not backward compatible)

## Solution

### Phase 1: Design Minimal API

**Goal**: Reduce to 4 core functions maximum

**Core Functions**:
1. `auth()` - Server components & pages (returns discriminated union)
2. `authApi(headers)` - API routes (takes headers parameter)
3. `requireRole(allowedRoles)` - Role-based access control with auto-redirects
4. `getAuthContext()` - Server actions (preferred, handles dynamic imports)

**Key Pattern**: All functions return **discriminated union**:
```typescript
type AuthResult =
  | { authenticated: false }
  | { authenticated: true; user: User; db: EnhancedDB }
```

### Phase 2: Enable Aggressive Session Caching

**File**: `packages/auth/src/auth.ts` (Better Auth config)

**Changes**:
```typescript
const SESSION_EXPIRES_IN = 7 * 24 * 60 * 60; // 7 days
const SESSION_UPDATE_AGE = 7 * 24 * 60 * 60; // 7 days (stateless - no updates)
const SESSION_COOKIE_CACHE_MAX_AGE = 15 * 60; // 15 minutes

session: {
  expiresIn: SESSION_EXPIRES_IN,
  updateAge: SESSION_UPDATE_AGE,  // Key: Set to EXPIRES_IN to disable DB writes
  cookieCache: {
    enabled: true,
    maxAge: SESSION_COOKIE_CACHE_MAX_AGE,  // Maximum allowed by Better Auth
    strategy: "jwe",  // JWE encryption (A256CBC-HS512)
  },
}
```

**Impact**: 99%+ auth checks served from 15-minute JWE cookie cache (zero DB hits)

### Phase 3: Create Unified auth() Function

**File**: `apps/web/lib/auth.ts`

**Implementation**:
```typescript
"use server";

import { auth as betterAuth } from "auth";
import { db as dbClient } from "database";
import type { User } from "database";

export type AuthResult =
  | { authenticated: false }
  | {
      authenticated: true;
      user: User;
      db: ReturnType<typeof dbClient.$setAuth>;
    };

export async function auth(): Promise<AuthResult> {
  // Dynamic import to avoid forcing module into dynamic rendering
  const { headers } = await import("next/headers");

  const session = await betterAuth.api.getSession({
    headers: await headers(),
  });

  if (!session?.user) {
    return { authenticated: false };
  }

  return {
    authenticated: true,
    user: session.user as User,
    db: dbClient.$setAuth(session.user),
  };
}

export async function requireRole(allowedRoles: string[]) {
  const authResult = await auth();

  if (!authResult.authenticated) {
    return { redirect: "/sign-in" };
  }

  const { user, db: userDB } = authResult;

  if (!user.role) {
    return { redirect: "/onboarding" };
  }

  if (!allowedRoles.includes(user.role)) {
    return { redirect: "/unauthorized" };
  }

  return { user, db: userDB };
}
```

**Key Pattern**: Use `Extract<>` utility for type-safe wrappers:
```typescript
export type AuthContext = Extract<
  Awaited<ReturnType<typeof auth>>,
  { authenticated: true }
>;

export async function getAuthContext(): Promise<AuthContext | AuthError> {
  const authResult = await auth();

  if (!authResult.authenticated) {
    return { success: false, error: "Unauthorized", authenticated: false };
  }

  return authResult;
}
```

### Phase 4: Systematic Multi-File Migration

**Strategy**: Migrate files in batches by type

**Server Components** (use `auth()` directly):
```typescript
// Before (helper function)
const user = await getUser();
if (!user) return redirect('/sign-in');

// After (discriminated union)
const authResult = await auth();
if (!authResult.authenticated) {
  return redirect('/sign-in');
}

const { user, db } = authResult;  // ✅ No optional chaining!
console.log(user.name);  // ✅ Not user?.name
```

**Server Actions** (use `getAuthContext()`):
```typescript
// Before
const auth = await requireAuth();
if (!auth.authenticated) return auth;

// After
const auth = await getAuthContext();
if (!auth.authenticated) return auth;

const { user, db } = auth;  // ✅ Perfect type narrowing
```

**Role-Based Pages** (use `requireRole()`):
```typescript
// Before
const user = await getUser();
if (!user || user.role !== 'INSTRUCTOR') {
  return redirect('/unauthorized');
}

// After
const result = await requireRole(['INSTRUCTOR', 'ADMIN']);
if ("redirect" in result) {
  return redirect({ href: result.redirect, locale });
}

const { user, db } = result;  // ✅ Guaranteed correct role
```

**Public + Authenticated Pages**:
```typescript
const authResult = await auth();

const userDB = authResult.authenticated
  ? authResult.db
  : dbClient.$setAuth(undefined);

const data = await userDB.model.findUnique({ where: { id } });
```

### Phase 5: Remove Helper Functions

After all files migrated, delete deprecated helpers:
- ~~`getUser()`~~
- ~~`isAdmin()`~~
- ~~`db()`~~
- ~~`requireAuth()`~~
- ~~`getAuthenticatedUser()`~~
- ~~`getAuthenticatedDB()`~~

**Verification**: Run TypeScript compilation:
```bash
pnpm --filter web tsc --noEmit
```

### Phase 6: Update Documentation

Update `CLAUDE.md` with new patterns:
- Remove references to deleted helpers
- Document 4 core functions
- Add usage examples for all scenarios
- Update performance metrics

## Verification

### TypeScript Compilation
```bash
pnpm --filter web tsc --noEmit
# Should show zero errors
```

### Performance Metrics
Check in production:
- **Cache hit rate**: Should be >99%
- **Auth latency**: Should be <5ms (p95)
- **Session DB queries**: Should be ~0 (only login/logout)

### Code Quality
- ✅ No optional chaining in auth code (`user.name` not `user?.name`)
- ✅ All imports from `@/lib/auth` (not scattered)
- ✅ Consistent discriminated union pattern everywhere
- ✅ TypeScript perfectly infers types after `if (!authenticated)` check

## Example

**Before** (scattered helpers, optional chaining):
```typescript
// File 1: Server component
const user = await getUser();
if (!user) return redirect('/sign-in');
console.log(user?.name);  // ⚠️ Optional chaining

const userDB = await db();
const data = await userDB.profile.findMany();

// File 2: Server action
const auth = await requireAuth();
if (!auth.authenticated) return auth;
const profile = await auth.db.profile.findUnique({ ... });

// File 3: Another server component
const user = await getAuthenticatedUser();
if (!user) return redirect('/sign-in');
const admin = await isAdmin();
```

**After** (unified, type-safe):
```typescript
// File 1: Server component
const authResult = await auth();
if (!authResult.authenticated) {
  return redirect('/sign-in');
}

const { user, db } = authResult;
console.log(user.name);  // ✅ No optional chaining!

const data = await db.profile.findMany();

// File 2: Server action
const auth = await getAuthContext();
if (!auth.authenticated) return auth;

const { user, db } = auth;
const profile = await db.profile.findUnique({ ... });

// File 3: Role-based page
const result = await requireRole(['ADMIN']);
if ("redirect" in result) {
  return redirect({ href: result.redirect, locale });
}

const { user, db } = result;  // Guaranteed ADMIN role
```

## Notes

### Discriminated Unions Best Practices

**Use `Extract<>` for derived types** (avoids circular references):
```typescript
// ✅ Good
export type AuthContext = Extract<
  Awaited<ReturnType<typeof auth>>,
  { authenticated: true }
>;

// ❌ Bad (circular reference)
export type AuthContext = {
  authenticated: true;
  user: User;
  db: ReturnType<typeof auth>['db'];  // Circular!
};
```

### Progressive Refactoring Strategy

**Option 1: Backward Compatible First**
1. Add new `auth()` function
2. Keep old helpers working
3. Migrate files gradually
4. Remove helpers only after all files migrated

**Option 2: Breaking Changes (Faster)**
1. Remove helpers immediately
2. Fix TypeScript errors in batches
3. More disruptive but cleaner

**Recommendation**: Use Option 1 for production apps, Option 2 for early-stage projects

### Better Auth Configuration

**Stateless Sessions** (no DB writes):
```typescript
updateAge: SESSION_EXPIRES_IN  // Set equal to expiresIn
```

**Cookie Cache** (max 15 minutes):
```typescript
cookieCache: {
  maxAge: 15 * 60  // Better Auth maximum
}
```

**Security**: JWE encryption ensures cookies can't be tampered with

### Common Migration Errors

**Error 1**: Duplicate variable declarations
```typescript
// ❌ Wrong
const { user, db: userDB } = result;
const userDB = await db();  // Error: userDB already declared

// ✅ Fix
const { user, db: userDB } = result;
// Use userDB directly
```

**Error 2**: Missing import after removing helpers
```typescript
// ❌ Wrong (after removing getUser)
import { getUser } from "@/lib/auth";

// ✅ Fix
import { auth } from "@/lib/auth";
```

**Error 3**: Forgetting to destructure db
```typescript
// ❌ Wrong
const authResult = await auth();
if (!authResult.authenticated) return redirect('/sign-in');

await authResult.db.profile.findMany();  // ⚠️ Works but verbose

// ✅ Better
const { user, db } = authResult;
await db.profile.findMany();
```

### Performance Impact

**Before optimization**:
- Auth check: ~10-50ms (database query)
- Cache hit rate: 0% (always queries DB)
- Session writes: Every 24 hours per user

**After optimization**:
- Auth check: ~1-5ms (cookie cache)
- Cache hit rate: >99%
- Session writes: Only on login/logout

**Estimated reduction**: 80-90% fewer DB queries, 85%+ latency reduction

## References

- [Better Auth Cookie Cache](https://www.better-auth.com/docs/concepts/session-management#cookie-cache) - Official docs on session caching
- [TypeScript Discriminated Unions](https://www.typescriptlang.org/docs/handbook/2/narrowing.html#discriminated-unions) - Official TypeScript handbook
- [Next.js 16 Server Actions](https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations) - Dynamic imports pattern
- [ZenStack Access Control](https://zenstack.dev/docs/guides/access-control) - Setting auth context with `$setAuth`
