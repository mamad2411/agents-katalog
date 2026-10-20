---
alwaysApply: true
---

# Next.js Server-Side Data Patterns

**All data retrieval and CRUD operations must follow server-side patterns.**

## 🔒 CRITICAL RULES

### 1. Data Retrieval - Server Components Only

**✅ CORRECT - Fetch data in Server Components:**

```typescript
// app/dashboard/page.tsx
import { auth } from "@clerk/nextjs/server";
import { db } from "@/db";
import { postsTable } from "@/db/schema";
import { eq } from "drizzle-orm";

export default async function DashboardPage() {
  const { userId } = await auth();
  
  if (!userId) {
    redirect("/sign-in");
  }
  
  // ✅ Data fetching in Server Component
  const posts = await db
    .select()
    .from(postsTable)
    .where(eq(postsTable.userId, userId));
  
  return (
    <div>
      {posts.map(post => (
        <PostCard key={post.id} post={post} />
      ))}
    </div>
  );
}
```

**❌ WRONG - Client-side data fetching:**

```typescript
// ❌ NEVER fetch data in Client Components
"use client";

import { useEffect, useState } from "react";

export default function DashboardPage() {
  const [posts, setPosts] = useState([]);
  
  useEffect(() => {
    // ❌ WRONG - Do not fetch in useEffect
    fetch("/api/posts").then(res => res.json()).then(setPosts);
  }, []);
  
  return <div>{/* ... */}</div>;
}
```

### 2. CRUD Operations - Server Actions Only

**✅ CORRECT - Use Server Actions for mutations:**

```typescript
// app/actions/posts.ts
"use server";

import { auth } from "@clerk/nextjs/server";
import { db } from "@/db";
import { postsTable } from "@/db/schema";
import { eq, and } from "drizzle-orm";
import { revalidatePath } from "next/cache";

export async function createPost(data: { title: string; content: string }) {
  const { userId } = await auth();
  
  if (!userId) {
    throw new Error("Unauthorized");
  }
  
  await db.insert(postsTable).values({
    ...data,
    userId,
  });
  
  revalidatePath("/dashboard");
}

export async function updatePost(postId: number, data: { title: string; content: string }) {
  const { userId } = await auth();
  
  if (!userId) {
    throw new Error("Unauthorized");
  }
  
  const result = await db
    .update(postsTable)
    .set(data)
    .where(
      and(
        eq(postsTable.id, postId),
        eq(postsTable.userId, userId)
      )
    )
    .returning();
  
  if (result.length === 0) {
    throw new Error("Post not found or unauthorized");
  }
  
  revalidatePath("/dashboard");
}

export async function deletePost(postId: number) {
  const { userId } = await auth();
  
  if (!userId) {
    throw new Error("Unauthorized");
  }
  
  const result = await db
    .delete(postsTable)
    .where(
      and(
        eq(postsTable.id, postId),
        eq(postsTable.userId, userId)
      )
    )
    .returning();
  
  if (result.length === 0) {
    throw new Error("Post not found or unauthorized");
  }
  
  revalidatePath("/dashboard");
}
```

**✅ CORRECT - Call Server Actions from Client Components:**

```typescript
// app/components/PostForm.tsx
"use client";

import { createPost } from "@/app/actions/posts";
import { useTransition } from "react";

export function PostForm() {
  const [isPending, startTransition] = useTransition();
  
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    
    const data = {
      title: formData.get("title") as string,
      content: formData.get("content") as string,
    };
    
    startTransition(async () => {
      await createPost(data);
    });
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <input name="title" required />
      <textarea name="content" required />
      <button type="submit" disabled={isPending}>
        {isPending ? "Creating..." : "Create Post"}
      </button>
    </form>
  );
}
```

**❌ WRONG - Using API routes for CRUD:**

```typescript
// ❌ NEVER use API routes for CRUD operations
// app/api/posts/route.ts
export async function POST(request: Request) {
  // ❌ Use Server Actions instead
  const body = await request.json();
  await db.insert(postsTable).values(body);
  return Response.json({ success: true });
}
```

**❌ WRONG - Client-side mutations:**

```typescript
// ❌ NEVER perform mutations directly in Client Components
"use client";

export function DeleteButton({ postId }: { postId: number }) {
  const handleDelete = async () => {
    // ❌ WRONG - Direct fetch to API route
    await fetch(`/api/posts/${postId}`, { method: "DELETE" });
  };
  
  return <button onClick={handleDelete}>Delete</button>;
}
```

## 📋 Guidelines

### Server Components (Data Retrieval)

1. **Default to Server Components** - Only use `"use client"` when you need:
   - Event handlers (onClick, onChange, etc.)
   - React hooks (useState, useEffect, etc.)
   - Browser-only APIs

2. **Fetch data at the component level** - No need for API routes for data fetching

3. **Always filter by userId** - See [clerk-nextjs.mdc](mdc:.cursor/rules/clerk-nextjs.mdc) for authorization rules

4. **Use Drizzle ORM** - See [drizzle-database.mdc](mdc:.cursor/rules/drizzle-database.mdc) for database patterns

### Server Actions (CRUD Operations)

1. **File organization** - Store server actions in `app/actions/` directory

2. **Always mark with `"use server"`** - At the top of the file or function

3. **Always authenticate** - Check `userId` from `auth()` before any operation

4. **Always authorize** - Verify ownership for update/delete operations

5. **Revalidate cache** - Use `revalidatePath()` or `revalidateTag()` after mutations

6. **Error handling** - Throw descriptive errors for client-side error boundaries

## ❌ FORBIDDEN PATTERNS

```typescript
// ❌ NEVER use useEffect for data fetching
useEffect(() => {
  fetch("/api/data").then(/* ... */);
}, []);

// ❌ NEVER use API routes for CRUD
export async function POST(request: Request) { /* ... */ }

// ❌ NEVER fetch in Client Components
"use client";
const data = await fetch("/api/data");

// ❌ NEVER use React Query, SWR, or similar for data fetching
const { data } = useQuery("posts", fetchPosts);

// ❌ NEVER perform database operations in Client Components
"use client";
await db.insert(postsTable).values(data);
```

## ✅ CHECKLIST

Before writing data-related code, verify:

- [ ] Data fetching is done in Server Components
- [ ] No `useEffect` or `useState` for data fetching
- [ ] CRUD operations use Server Actions, not API routes
- [ ] Server Actions are marked with `"use server"`
- [ ] Authentication is checked in Server Actions
- [ ] Authorization (ownership) is verified for mutations
- [ ] `revalidatePath()` is called after mutations
- [ ] Client Components only handle UI and user interactions

## 📚 Reference

- Next.js Server Actions: https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations
- Next.js Server Components: https://nextjs.org/docs/app/building-your-application/rendering/server-components
