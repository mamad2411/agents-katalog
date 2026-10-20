---
alwaysApply: true
---

# Clerk Authentication & Authorization

**All authentication and authorization in this project is handled by Clerk.**

## 🔒 CRITICAL SECURITY RULE

**Users can ONLY access their own data. Users MUST NOT be able to access any data that does not belong to them.**

Every data access operation must verify user ownership before returning or modifying data.

---

## 🛡️ AUTHORIZATION & DATA ACCESS CONTROL

### 1. Always Get User ID First

Every protected route or API endpoint must retrieve the authenticated user ID:

```typescript
import { auth } from "@clerk/nextjs/server";

export async function GET() {
  const { userId } = await auth();
  
  if (!userId) {
    return new Response("Unauthorized", { status: 401 });
  }
  
  // Now use userId to fetch user-specific data
}
```

### 2. Filter All Database Queries by User ID

**✅ CORRECT - Always filter by user:**

```typescript
import { auth } from "@clerk/nextjs/server";
import { db } from "@/db";
import { usersTable, postsTable } from "@/db/schema";
import { eq, and } from "drizzle-orm";

export async function GET() {
  const { userId } = await auth();
  
  if (!userId) {
    return new Response("Unauthorized", { status: 401 });
  }
  
  // Get only the current user's posts
  const userPosts = await db
    .select()
    .from(postsTable)
    .where(eq(postsTable.userId, userId));
  
  return Response.json(userPosts);
}
```

**❌ WRONG - Missing user filter (SECURITY VULNERABILITY):**

```typescript
// ❌ NEVER DO THIS - Returns ALL users' data!
const allPosts = await db.select().from(postsTable);
```

### 3. Verify Ownership Before Updates/Deletes

Always verify the resource belongs to the user before modifying:

```typescript
import { auth } from "@clerk/nextjs/server";
import { db } from "@/db";
import { postsTable } from "@/db/schema";
import { eq, and } from "drizzle-orm";

export async function DELETE(
  request: Request,
  { params }: { params: { id: string } }
) {
  const { userId } = await auth();
  
  if (!userId) {
    return new Response("Unauthorized", { status: 401 });
  }
  
  // Verify the post belongs to the user before deleting
  const result = await db
    .delete(postsTable)
    .where(
      and(
        eq(postsTable.id, params.id),
        eq(postsTable.userId, userId)  // ✅ Critical ownership check
      )
    )
    .returning();
  
  if (result.length === 0) {
    return new Response("Not found or unauthorized", { status: 404 });
  }
  
  return Response.json({ success: true });
}
```

### 4. Server Actions Authorization

Protect server actions with user ID checks:

```typescript
"use server";

import { auth } from "@clerk/nextjs/server";
import { db } from "@/db";
import { postsTable } from "@/db/schema";

export async function createPost(formData: FormData) {
  const { userId } = await auth();
  
  if (!userId) {
    throw new Error("Unauthorized");
  }
  
  const title = formData.get("title") as string;
  
  // Always set userId when creating records
  await db.insert(postsTable).values({
    title,
    userId,  // ✅ Associate with current user
  });
}
```

### 5. Protect Client Components

Use Clerk's client components to control UI visibility:

```typescript
import { SignedIn, SignedOut, useUser } from "@clerk/nextjs";

export function ProtectedComponent() {
  return (
    <>
      <SignedOut>
        <p>Please sign in to view this content</p>
      </SignedOut>
      
      <SignedIn>
        <UserContent />
      </SignedIn>
    </>
  );
}

function UserContent() {
  const { user } = useUser();
  // user.id is the Clerk user ID
  return <div>Welcome, {user?.firstName}</div>;
}
```

### 6. Database Schema Pattern

Always include a `userId` column for user-owned data:

```typescript
import { pgTable, serial, text, timestamp } from "drizzle-orm/pg-core";

export const postsTable = pgTable("posts", {
  id: serial("id").primaryKey(),
  userId: text("user_id").notNull(),  // ✅ Required for user isolation
  title: text("title").notNull(),
  content: text("content"),
  createdAt: timestamp("created_at").defaultNow(),
});
```

### 7. API Route Protection Checklist

Before any data operation, verify:

- ✅ User is authenticated (`userId` is not null)
- ✅ Query filters by `userId` for SELECT operations
- ✅ Ownership is verified before UPDATE/DELETE operations
- ✅ New records are created with the current `userId`
- ✅ Return 401 for unauthenticated requests
- ✅ Return 404 (not 403) for unauthorized resource access to avoid information leakage

---

## ✅ CLERK INTEGRATION PATTERNS

### 1. Installation
```bash
npm install @clerk/nextjs
```

### 2. Environment Variables (`.env.local`)
```bash
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=YOUR_PUBLISHABLE_KEY
CLERK_SECRET_KEY=YOUR_SECRET_KEY
```
**⚠️ Use placeholders only in code examples. Never expose real keys.**

### 3. Middleware (`middleware.ts` or `proxy.ts`)
```typescript
import { clerkMiddleware } from "@clerk/nextjs/server";

export default clerkMiddleware();

export const config = {
  matcher: [
    "/((?!_next|[^?]*\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)",
    "/(api|trpc)(.*)",
  ],
};
```

### 4. Layout (`app/layout.tsx`)
```typescript
import { ClerkProvider, SignInButton, SignUpButton, SignedIn, SignedOut, UserButton } from "@clerk/nextjs";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body>
          <header>
            <SignedOut>
              <SignInButton />
              <SignUpButton />
            </SignedOut>
            <SignedIn>
              <UserButton />
            </SignedIn>
          </header>
          {children}
        </body>
      </html>
    </ClerkProvider>
  );
}
```

### 5. Server-Side Auth & Protected Routes

```typescript
import { auth } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";

export default async function ProtectedPage() {
  const { userId } = await auth();
  
  // Protect the page - redirect if not authenticated
  if (!userId) {
    redirect("/sign-in");
  }
  
  // User is authenticated, render page with user-specific data
  return <div>Protected content for user: {userId}</div>;
}
```

### 6. Middleware Route Protection

Use `createRouteMatcher` to protect specific routes:

```typescript
import { clerkMiddleware, createRouteMatcher } from "@clerk/nextjs/server";

const isProtectedRoute = createRouteMatcher([
  "/dashboard(.*)",
  "/api/user(.*)",
]);

export default clerkMiddleware(async (auth, req) => {
  if (isProtectedRoute(req)) {
    await auth.protect();
  }
});

export const config = {
  matcher: [
    "/((?!_next|[^?]*\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)",
    "/(api|trpc)(.*)",
  ],
};
```

## ❌ FORBIDDEN PATTERNS

### DO NOT use deprecated APIs:
```typescript
// ❌ WRONG - Old middleware
import { authMiddleware } from "@clerk/nextjs";

// ❌ WRONG - Pages Router pattern
// pages/_app.tsx or pages/signin.js

// ❌ WRONG - Non-async auth
const { userId } = auth(); // Missing await
```

### DO NOT create security vulnerabilities:
```typescript
// ❌ WRONG - No user filter (exposes all users' data)
const posts = await db.select().from(postsTable);

// ❌ WRONG - No ownership check before delete
await db.delete(postsTable).where(eq(postsTable.id, postId));

// ❌ WRONG - Using ID from client without verification
export async function deletePost(postId: string) {
  // Missing: auth check and ownership verification
  await db.delete(postsTable).where(eq(postsTable.id, postId));
}

// ❌ WRONG - Trusting client-provided userId
export async function getUserData(userId: string) {
  // Never trust userId from client - always get from auth()
  return await db.select().from(postsTable).where(eq(postsTable.userId, userId));
}
```

## 🔍 VERIFICATION CHECKLIST

Before generating Clerk code, verify:

### Integration:
- [ ] Using `clerkMiddleware()` from `@clerk/nextjs/server`
- [ ] `<ClerkProvider>` wraps app in `app/layout.tsx`
- [ ] All imports from `@clerk/nextjs` or `@clerk/nextjs/server`
- [ ] Using App Router structure (`app/` not `pages/`)
- [ ] Only placeholder keys in code examples
- [ ] `auth()` called with `await`

### Authorization & Security:
- [ ] Every protected route/API checks `userId` from `auth()`
- [ ] Returns 401 if `userId` is null/undefined
- [ ] All database queries filter by `userId` for user-owned data
- [ ] UPDATE/DELETE operations verify ownership before executing
- [ ] Never trust `userId` from client/request parameters
- [ ] New records are created with `userId` from `auth()`
- [ ] Database schema includes `userId` column for user-owned tables

## 📚 Reference

Latest docs: https://clerk.com/docs/quickstarts/nextjs

**If any pattern above is violated, STOP and correct before proceeding.**
