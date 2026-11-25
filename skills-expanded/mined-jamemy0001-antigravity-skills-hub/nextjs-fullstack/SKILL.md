---
name: nextjs-fullstack
description: Fullstack Next.js 15 App Router engineering, React Server Components (RSC) boundary patterns, Server Actions with validation, and cache management.
aliases:
  - nextjs
  - next15
  - app-router
  - server-components
  - server-actions
category: "04 - Web & Frontend"
tags:
  - agent-skill
  - nextjs
  - react
  - fullstack
  - frontend
  - stage-4
---

# Next.js 15 Fullstack & App Router Architecture

Production guidelines for modern fullstack Next.js 15 applications utilizing the App Router architecture, React Server Components (RSC), type-safe Server Actions, and predictable caching strategies.

---

## Core Architectural Principles

1. **Server Components by Default**:
   - Keep components as React Server Components (RSC) by default for zero client bundle overhead and direct backend/database access.
   - Only add `'use client'` at the absolute leaf nodes that require client-side interactivity (`useState`, `useEffect`, browser event listeners).
2. **Server Actions with Schema Validation**:
   - Every Server Action must validate inputs using a strict validation schema (e.g. Zod) before executing mutations.
   - Always return typed result objects `{ success: boolean, data?: T, error?: string }` instead of throwing raw errors.
3. **Granular Caching & Invalidation**:
   - Utilize `revalidateTag(tag)` for targeted cache invalidation rather than aggressive `revalidatePath()`.
   - Wrap expensive database queries in `unstable_cache` with deterministic cache keys and tags.
4. **Streaming with Suspense**:
   - Wrap slow asynchronous data fetches in `<Suspense fallback={<Skeleton />}>` to deliver instant First Contentful Paint (FCP).

---

## Standard Patterns & Recipes

### 1. Server Component with Streaming & Fallback

```tsx
// app/dashboard/page.tsx
import { Suspense } from 'react';
import { UserStats } from '@/components/dashboard/user-stats';
import { StatsSkeleton } from '@/components/dashboard/skeletons';

export default async function DashboardPage() {
  return (
    <div className="p-8 space-y-6">
      <h1 className="text-2xl font-bold tracking-tight text-neutral-900">Dashboard</h1>
      <Suspense fallback={<StatsSkeleton />}>
        <UserStats />
      </Suspense>
    </div>
  );
}

// components/dashboard/user-stats.tsx
async function getUserStats() {
  const res = await fetch('https://api.example.com/stats', {
    next: { tags: ['user-stats'], revalidate: 300 } // Cache 5 min
  });
  if (!res.ok) throw new Error('Failed to load stats');
  return res.json();
}

export async function UserStats() {
  const stats = await getUserStats();
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div className="p-4 rounded-xl border border-neutral-200 bg-white">
        <p className="text-sm text-neutral-500">Total Users</p>
        <p className="text-2xl font-semibold">{stats.totalUsers.toLocaleString()}</p>
      </div>
    </div>
  );
}
```

### 2. Type-Safe Server Action with Zod

```ts
// actions/user-actions.ts
'use server';

import { z } from 'zod';
import { revalidateTag } from 'next/cache';

const UpdateProfileSchema = z.object({
  name: z.string().min(2, 'Name must be at least 2 characters'),
  email: z.string().email('Invalid email address')
});

export type ActionState = {
  success: boolean;
  message?: string;
  errors?: Record<string, string[]>;
};

export async function updateProfile(prevState: ActionState, formData: FormData): Promise<ActionState> {
  const validated = UpdateProfileSchema.safeParse({
    name: formData.get('name'),
    email: formData.get('email')
  });

  if (!validated.success) {
    return {
      success: false,
      errors: validated.error.flatten().fieldErrors
    };
  }

  try {
    // Perform database mutation
    // await db.user.update(...)
    revalidateTag('user-profile');
    return { success: true, message: 'Profile updated successfully' };
  } catch (err) {
    return { success: false, message: 'Internal server error' };
  }
}
```

---

## 🔗 Connected Skills (ทักษะที่เกี่ยวข้อง)
- [[Skills/claude-design/SKILL|claude-design]] — ออกแบบ UI Components, ปุ่ม Atomic และโครงสร้างหน้าเว็บที่ประณีต
- [[Skills/modern-web-guidance/SKILL|modern-web-guidance]] — ตรวจสอบมาตรฐาน Web APIs และ Core Web Vitals
- [[Skills/api-design/SKILL|api-design]] — กำหนดโครงสร้าง Route Handlers (`app/api/.../route.ts`)
- [[Skills/tdd-workflow/SKILL|tdd-workflow]] — เขียน Unit/Integration Tests ด้วย Vitest หรือ Jest

<!-- v1.1.0 synchronized: 2026-09-29 -->
