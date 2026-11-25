---
name: nextjs-16-use-server-exports
description: |
  Fix Next.js 16 build error "A 'use server' file can only export async functions, found object".
  Use when: (1) Build fails with this exact error message, (2) You have constants, enums, or
  type exports in files with "use server" directive, (3) Exporting AUDIT_ACTIONS, validation
  schemas, or other non-function values from server action files. Solution: Separate constants
  into a new file without "use server" directive and import them where needed.
author: Claude Code
version: 1.0.0
date: 2026-01-24
---

# Next.js 16 "use server" Export Compliance

## Problem

Next.js 16 enforces strict rules for files with the `"use server"` directive: they can **only export async functions**. Any attempt to export constants, objects, enums, or type definitions from these files will cause a build error:

```
Error: A "use server" file can only export async functions, found object.
Read more: https://nextjs.org/docs/messages/invalid-use-server-value
```

This error is not immediately obvious because:
- The error message doesn't clearly indicate which export is problematic
- Many developers expect to co-locate related constants with their server actions
- TypeScript compilation succeeds but Next.js build fails

## Context / Trigger Conditions

**When to use this skill:**

1. **Exact error message**: Build fails with `A "use server" file can only export async functions, found object`
2. **File structure**: You have a file with `"use server"` at the top that exports both:
   - Async server actions (functions)
   - Constants, objects, enums, or types
3. **Common scenarios**:
   - Exporting audit action constants (e.g., `AUDIT_ACTIONS`)
   - Exporting Zod validation schemas alongside server actions
   - Exporting TypeScript enums or type definitions
   - Exporting configuration objects

**Example problematic file**:

```typescript
"use server";

// ❌ This causes the error
export const AUDIT_ACTIONS = {
  USER_CREATED: "USER_CREATED",
  USER_UPDATED: "USER_UPDATED",
} as const;

// ✅ This is allowed
export async function createUser() {
  // ... server action logic
}
```

## Solution

**Step 1: Create a new constants file (without "use server")**

Create a separate file for your non-function exports. Do NOT add `"use server"` to this file.

```typescript
// lib/constants/audit-actions.ts  (NO "use server" directive)

/**
 * Audit log action types for user management
 */
export const AUDIT_ACTIONS = {
  USER_CREATED: "USER_CREATED",
  USER_UPDATED: "USER_UPDATED",
  USER_DELETED: "USER_DELETED",
} as const;

export type AuditAction = (typeof AUDIT_ACTIONS)[keyof typeof AUDIT_ACTIONS];
```

**Step 2: Keep only async functions in your server actions file**

```typescript
// lib/actions/user.ts
"use server";

import { AUDIT_ACTIONS, type AuditAction } from "@/lib/constants/audit-actions";
import { createAuditLog } from "@/lib/utils/audit-log";

export async function createUser(data: unknown): Promise<ActionResult> {
  // ... implementation using AUDIT_ACTIONS.USER_CREATED
}

export async function updateUser(data: unknown): Promise<ActionResult> {
  // ... implementation using AUDIT_ACTIONS.USER_UPDATED
}
```

**Step 3: Update imports in other files**

Update any files that imported the constants from the server actions file:

```typescript
// Before
import { AUDIT_ACTIONS } from "@/lib/actions/user";

// After
import { AUDIT_ACTIONS } from "@/lib/constants/audit-actions";
```

**Step 4: Update test mocks**

If you have unit tests that mock the constants, update the mock paths:

```typescript
// tests/unit/actions/user.test.ts

vi.mock("@/lib/constants/audit-actions", () => ({
  AUDIT_ACTIONS: {
    USER_CREATED: "USER_CREATED",
    USER_UPDATED: "USER_UPDATED",
  },
}));
```

## Verification

After applying the fix:

1. **TypeScript check**: Run `turbo types` or `tsc --noEmit` - should pass
2. **Build**: Run `turbo build` or `next build` - should complete without errors
3. **Runtime**: Server actions should work exactly as before
4. **Tests**: Unit tests should pass with updated import paths

**Success indicators**:
- ✅ No "use server" export errors in build output
- ✅ All async server action functions still exported correctly
- ✅ Constants accessible via new import path
- ✅ TypeScript types properly inferred

## Example: Real-World Case

**Before (causes error)**:

```typescript
// lib/utils/audit-log.ts
"use server";

export const AUDIT_ACTIONS = {
  LANGUAGE_CHANGED: "LANGUAGE_CHANGED",
  TIMEZONE_CHANGED: "TIMEZONE_CHANGED",
  ACCESSIBILITY_CHANGED: "ACCESSIBILITY_CHANGED",
} as const;

export type AuditAction = (typeof AUDIT_ACTIONS)[keyof typeof AUDIT_ACTIONS];

export async function createAuditLog(params: { action: AuditAction }): Promise<void> {
  // ... implementation
}
```

**After (works correctly)**:

```typescript
// lib/constants/audit-actions.ts (NEW FILE - no "use server")
export const AUDIT_ACTIONS = {
  LANGUAGE_CHANGED: "LANGUAGE_CHANGED",
  TIMEZONE_CHANGED: "TIMEZONE_CHANGED",
  ACCESSIBILITY_CHANGED: "ACCESSIBILITY_CHANGED",
} as const;

export type AuditAction = (typeof AUDIT_ACTIONS)[keyof typeof AUDIT_ACTIONS];
```

```typescript
// lib/utils/audit-log.ts
"use server";

import type { AuditAction } from "@/lib/constants/audit-actions";

export async function createAuditLog(params: { action: AuditAction }): Promise<void> {
  // ... implementation
}

export async function getRequestMetadata(): Promise<{ ipAddress: string; userAgent: string }> {
  // ... implementation
}
```

```typescript
// lib/actions/preferences.ts
"use server";

import { AUDIT_ACTIONS } from "@/lib/constants/audit-actions";
import { createAuditLog } from "@/lib/utils/audit-log";

export async function updateLanguage(data: unknown): Promise<ActionResult> {
  // ... implementation
  await createAuditLog({
    userId: user.id,
    action: AUDIT_ACTIONS.LANGUAGE_CHANGED, // ✅ Works perfectly
  });
}
```

## Notes

**Why This Restriction Exists**:
- Server Actions in Next.js 16 rely on the async nature of exported functions for streaming, rendering, and routing
- The framework needs to track and serialize server functions differently from regular exports
- Mixing function and non-function exports makes the bundling and serialization process ambiguous

**Common Mistakes**:
- ❌ Adding `"use server"` to the new constants file (defeats the purpose)
- ❌ Using default exports for constants (makes refactoring harder)
- ❌ Forgetting to update test mocks after moving constants
- ❌ Trying to export utility functions that aren't async (these also need to be async or moved)

**Related Patterns**:
- This same pattern applies to Zod schemas, configuration objects, and TypeScript enums
- You can co-locate related constants by using a `constants/` directory structure
- Consider using barrel exports (`index.ts`) to simplify imports from multiple constant files

**Next.js 16 Async Requirements**:
- All "use server" exports must be async functions
- Utility functions in server action files must also be async (even if they don't await anything)
- Helper functions like `error()`, `success()`, `validateInput()` should be async and awaited

## References

- [Next.js: Server Actions and Mutations](https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations)
- [Next.js GitHub Discussion: "use server" async requirements](https://github.com/vercel/next.js/discussions/80293)
- [Next.js GitHub Issue: Export restrictions in "use server" files](https://github.com/vercel/next.js/issues/62926)
- [Next.js 16 Release Notes](https://nextjs.org/blog/next-16)
- [Next.js Upgrading to Version 16](https://nextjs.org/docs/app/guides/upgrading/version-16)
