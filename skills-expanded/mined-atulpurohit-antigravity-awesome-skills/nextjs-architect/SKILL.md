---
name: nextjs-architect
description: "Build production Next.js applications with App Router, Server Components, server actions, ISR, and full-stack patterns."
category: frontend
tags: [nextjs, react, ssr, ssg, app-router, fullstack]
complexity: advanced
risk: low
compatibility: [claude-code, antigravity, gemini-cli, cursor, copilot, codex-cli, autohand, kiro]
source: antigravity-official
version: "1.0.0"
date_added: "2026-07-10"
last_updated: "2026-07-10"
---

# Next.js Architect

## Purpose
Build performant, SEO-friendly Next.js applications using the App Router, Server Components, and modern data fetching patterns.

## App Router Structure
```
app/
├── (marketing)/              # Route group (no layout prefix)
│   ├── layout.tsx
│   ├── page.tsx
│   └── pricing/page.tsx
├── (dashboard)/
│   ├── layout.tsx            # Dashboard layout (auth-protected)
│   └── dashboard/
│       └── page.tsx
├── api/
│   └── webhooks/
│       └── stripe/route.ts
└── layout.tsx                # Root layout
```

## Server Components (Default)
```tsx
// app/posts/page.tsx - Runs on server, zero JS bundle
export default async function PostsPage({
  searchParams,
}: {
  searchParams: { page?: string };
}) {
  // Direct database access - no API needed
  const posts = await db.query.posts.findMany({
    where: eq(posts.status, 'published'),
    limit: 20,
    offset: (Number(searchParams.page ?? 1) - 1) * 20,
  });

  return (
    <div>
      {posts.map(post => <PostCard key={post.id} post={post} />)}
    </div>
  );
}

// Generate static metadata
export async function generateMetadata({ params }: { params: { id: string } }) {
  const post = await getPost(params.id);
  return {
    title: post.title,
    description: post.excerpt,
    openGraph: { images: [post.coverImage] },
  };
}
```

## Server Actions
```tsx
// app/actions/posts.ts
'use server';
import { revalidatePath } from 'next/cache';

export async function createPost(formData: FormData) {
  const session = await auth();
  if (!session) throw new Error('Unauthorized');

  const post = await db.insert(posts).values({
    title: formData.get('title') as string,
    body: formData.get('body') as string,
    authorId: session.user.id,
  }).returning();

  revalidatePath('/posts');
  redirect(`/posts/${post[0].id}`);
}

// In component
<form action={createPost}>
  <input name="title" required />
  <textarea name="body" required />
  <SubmitButton />
</form>
```

## Caching & Revalidation
```tsx
// Cached fetch with ISR
const data = await fetch('https://api.example.com/posts', {
  next: { revalidate: 3600 },  // Revalidate every hour
});

// On-demand revalidation
import { revalidateTag } from 'next/cache';

export async function updatePost(id: string) {
  await db.update(posts).set({ title: newTitle }).where(eq(posts.id, id));
  revalidateTag(`post-${id}`);  // Purge specific cache
}
```

## Outputs
1. App Router structure design
2. Server Component implementation
3. Server Actions for mutations
4. Authentication with NextAuth/Auth.js
5. Caching and revalidation strategy
6. Deployment configuration (Vercel/self-hosted)
