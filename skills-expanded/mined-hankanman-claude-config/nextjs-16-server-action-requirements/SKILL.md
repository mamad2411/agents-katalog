---
name: nextjs-16-server-action-requirements
description: |
  Fix Next.js 16 build errors in "use server" files. Use when: (1) Build error "A 'use server'
  file can only export async functions, found object", (2) Need to export constants/enums from
  server action files, (3) Want to use next/headers without forcing entire module into dynamic
  rendering, (4) Server action helpers like error() or validateInput() fail type checking. Covers
  Next.js 16 strict requirements for server action files and dynamic import patterns.
author: Claude Code
version: 1.0.0
date: 2026-01-24
---

# Next.js 16 Server Action Requirements

## Problem
Next.js 16 enforces strict rules for files with the `"use server"` directive. Violations cause
build failures with cryptic error messages. Common issues include exporting non-async functions,
constants, or using static imports of `next/headers`.

## Context / Trigger Conditions
- **Build Error**: `A 'use server' file can only export async functions, found object`
- **Build Error**: Static imports of `next/headers` force modules into dynamic rendering
- **TypeScript Error**: Helper functions in server actions fail type checking
- **Next.js Version**: 16.x (these rules are stricter than Next.js 15)

## Solution

### Rule 1: All Exported Functions Must Be Async

Every exported function in a `"use server"` file must be async, even if it doesn't perform
async operations.

```typescript
"use server";

// ❌ WRONG - Synchronous exported function
export function error(message: string): ActionError {
  return { success: false, error: message };
}

// ✅ CORRECT - Async function
export async function error(message: string): Promise<ActionError> {
  return { success: false, error: message };
}
```

**Applies to all helpers:**
- `error()`, `success()` - result builders
- `validateInput()` - validation helpers
- `handleActionError()` - error handlers
- Any utility function exported from the file

### Rule 2: No Constant or Type Exports

You cannot export constants, enums, types, or objects from `"use server"` files.

```typescript
"use server";

// ❌ WRONG - Exporting constants
export const AUDIT_ACTIONS = {
  PROFILE_UPDATE: "PROFILE_UPDATE",
  PASSWORD_CHANGE: "PASSWORD_CHANGE",
};

export enum Status {
  PENDING = "PENDING",
  COMPLETE = "COMPLETE",
}
```

**Solution**: Move constants to a separate file without `"use server"`:

```typescript
// lib/constants/audit-actions.ts (no "use server")
export const AUDIT_ACTIONS = {
  PROFILE_UPDATE: "PROFILE_UPDATE",
  PASSWORD_CHANGE: "PASSWORD_CHANGE",
} as const;

export type AuditAction = typeof AUDIT_ACTIONS[keyof typeof AUDIT_ACTIONS];
```

```typescript
// lib/actions/my-action.ts
"use server";

import { AUDIT_ACTIONS } from "@/lib/constants/audit-actions";

export async function myAction() {
  // Use imported constants
  await createLog(AUDIT_ACTIONS.PROFILE_UPDATE);
}
```

### Rule 3: Use Dynamic Imports for next/headers

Static imports of `next/headers` make the entire module opt into dynamic rendering immediately.
Use dynamic imports to defer this decision.

```typescript
"use server";

// ❌ WRONG - Static import forces dynamic rendering
import { headers } from "next/headers";

export async function myAction() {
  const h = await headers();
  // ...
}
```

```typescript
"use server";

// ✅ CORRECT - Dynamic import defers dynamic rendering decision
export async function myAction() {
  const { headers } = await import("next/headers");
  const h = await headers();
  // ...
}
```

**Why this matters:**
- Static imports force the entire module into dynamic rendering at import time
- Dynamic imports defer this until the function actually runs
- Gives better control over when routes become dynamic
- Prevents unintended side effects when server action modules are imported elsewhere

**Note**: Using `headers()` still forces dynamic rendering for that specific request, but the
dynamic import pattern gives you more control over the scope.

### Rule 4: Always Await Helper Functions

Since all helper functions must be async, you must await them:

```typescript
"use server";

export async function myAction(data: unknown): Promise<ActionResult> {
  const auth = await getAuthContext();

  // ❌ WRONG - Missing await
  if (!auth.authenticated) return error("Unauthorized");

  // ✅ CORRECT - Awaiting async helper
  if (!auth.authenticated) return await error("Unauthorized");

  const validation = await validateInput(schema, data);
  if (!validation.valid) return validation;

  // ...
}
```

## Common Patterns

### Server Action Structure (Recommended)

```typescript
"use server";

import { getAuthContext, handleActionError, validateInput, type ActionResult } from "./utils";
import { mySchema } from "database/schemas";

export async function myAction(data: unknown): Promise<ActionResult> {
  // 1. Get authenticated context (handles dynamic imports internally)
  const auth = await getAuthContext();
  if (!auth.authenticated) return auth;

  // 2. Validate input
  const validation = await validateInput(mySchema, data);
  if (!validation.valid) return validation;

  // 3. Perform operation with error handling
  try {
    const result = await auth.db.myModel.create({
      data: validation.data,
    });
    return { success: true, data: result };
  } catch (err) {
    return await handleActionError(err, "my operation");
  }
}
```

### Helper Functions in utils.ts

```typescript
"use server";

// No static import of next/headers
import { z } from "zod";
import { getUser } from "@/lib/utils/auth";
import { db as dbClient, User } from "database";

export type ActionResult = { success: true } | { success: false; error: string };

// All helpers must be async and return Promise
export async function error(message: string): Promise<{ success: false; error: string }> {
  return { success: false, error: message };
}

export async function success(): Promise<{ success: true }> {
  return { success: true };
}

export async function validateInput<T>(
  schema: z.ZodSchema<T>,
  data: unknown
): Promise<ValidationResult<T>> {
  const result = schema.safeParse(data);
  return result.success
    ? { valid: true, data: result.data }
    : { valid: false, success: false, error: "Validation failed", issues: result.error.issues };
}

// getAuthContext uses dynamic import internally
export async function getAuthContext(): Promise<AuthContext | AuthError> {
  const { headers } = await import("next/headers"); // Dynamic import here
  const user = await getUser(await headers());

  if (!user) {
    return { ...(await error("Unauthorized")), authenticated: false };
  }

  const db = dbClient.$setAuth({ id: user.id, role: user.role });
  return { authenticated: true, user, db };
}
```

## Verification

After applying these patterns:

1. **Build Check**: Run `pnpm build` or `turbo build` - should complete without errors
2. **Type Check**: Run `turbo types` - should pass
3. **Lint Check**: Run `turbo lint` - should pass
4. **Runtime Test**: Verify server actions work correctly in development and production

## Migration Checklist

When converting existing server actions to Next.js 16:

- [ ] All exported functions are `async` and return `Promise`
- [ ] Constants/enums moved to separate files without `"use server"`
- [ ] `next/headers` uses dynamic imports (`await import("next/headers")`)
- [ ] All helper function calls have `await`
- [ ] Removed `"use server"` from any constant-only files
- [ ] Updated callers to await all helper functions

## Common Build Errors and Fixes

### Error: "can only export async functions"
**Cause**: Exporting constants, types, or sync functions
**Fix**: Make functions async or move exports to separate file

### Error: Module forced into dynamic rendering
**Cause**: Static import of `next/headers`
**Fix**: Use `const { headers } = await import("next/headers")`

### Error: Missing await
**Cause**: Calling async helper without await
**Fix**: Add `await` to all helper function calls

## Notes

- These rules apply to **all** files with `"use server"` directive
- Next.js 15 was more lenient - Next.js 16 enforces these strictly
- Server components (without `"use server"`) have different rules
- The `getAuthContext()` helper pattern is recommended over manual `requireAuth()` usage
- Dynamic imports add minimal overhead (module is cached after first import)

## References
- [Next.js 16 Server Actions Documentation](https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations)
- [Next.js Dynamic Imports](https://nextjs.org/docs/app/building-your-application/optimizing/lazy-loading)
- [Next.js 16 Migration Guide](https://nextjs.org/docs/app/building-your-application/upgrading)
