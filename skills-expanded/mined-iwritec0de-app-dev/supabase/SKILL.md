---
name: supabase
description: >-
  This skill should be used when the user asks to "integrate Supabase", "set up
  Supabase auth", "write RLS policies", "use Supabase storage", "subscribe to
  realtime changes", or mentions "supabase", "supabase auth", "RLS", "row level
  security", "supabase client", "supabase storage", "realtime", "edge function",
  "supabase migration". Provides Supabase best practices for Next.js applications
  including auth, database, storage, realtime, and edge functions.
license: MIT
metadata:
  author: Chris Kelley (hello@iwritecode.io)
  version: 1.0.0
---

# Supabase Skill

You are a Supabase expert for Next.js applications using the App Router.

## Critical Rules

- **Always enable RLS on every table** — a table without Row Level Security is open to any authenticated user by default
- **Use the server-side client for Server Components** — `createServerClient` from `@supabase/ssr` reads cookies via Next.js `cookies()`; it never leaks tokens to the browser
- **Use the browser client for Client Components** — `createBrowserClient` manages the session in the browser; it must never be used in Server Components or Route Handlers
- **Never expose the `service_role` key on the client** — it bypasses RLS entirely; keep it server-only in environment variables prefixed `SUPABASE_SERVICE_ROLE_KEY` (never `NEXT_PUBLIC_`)
- **Use database migrations for schema changes** — never edit schema through the Supabase dashboard in production; use `supabase migration new` and commit SQL files to version control
- **Always use parameterized queries** — the Supabase client does this automatically; never interpolate user input into raw SQL strings
- **Refresh sessions in middleware** — call `supabase.auth.getUser()` in `middleware.ts` on every request to keep the session cookie fresh

## Client Setup

Install the required packages:

```bash
npm install @supabase/supabase-js @supabase/ssr
```

**Server Component / Route Handler client** — reads and writes cookies via Next.js `cookies()`:

```ts
// lib/supabase/server.ts
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'
import type { Database } from '@/types/supabase'

export async function createClient() {
  const cookieStore = await cookies()
  return createServerClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() { return cookieStore.getAll() },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options)
            )
          } catch {} // Safe to ignore in Server Components; middleware handles refresh
        },
      },
    }
  )
}
```

**Client Component client** — manages the session in the browser:

```ts
// lib/supabase/client.ts
import { createBrowserClient } from '@supabase/ssr'
import type { Database } from '@/types/supabase'

export function createClient() {
  return createBrowserClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}
```

Read `reference/auth-patterns.md` for the full middleware setup, sign-in/sign-up flows, OAuth, and protected route patterns.

## Database

Always import your generated types for full type safety:

```ts
import type { Database } from '@/types/supabase'
// Generate: npx supabase gen types typescript --local > types/supabase.ts
```

Common query patterns:

```ts
const supabase = await createClient()

// Select with filter
const { data, error } = await supabase
  .from('posts')
  .select('id, title, created_at')
  .eq('user_id', userId)
  .order('created_at', { ascending: false })

// Insert
const { data, error } = await supabase
  .from('posts')
  .insert({ title, body, user_id: userId })
  .select()
  .single()

// Upsert
const { error } = await supabase
  .from('profiles')
  .upsert({ id: userId, display_name: name })
```

Read `reference/database-patterns.md` for RLS policy patterns, migrations, RPC functions, joins, and views.

## RLS Policies — Quick Reference

```sql
-- Authenticated users can read all rows
CREATE POLICY "authenticated read" ON posts
  FOR SELECT TO authenticated USING (true);

-- Users can only modify their own rows
CREATE POLICY "owner write" ON posts
  FOR ALL TO authenticated USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- Role-based access using JWT claims
CREATE POLICY "admin only" ON admin_logs
  FOR SELECT TO authenticated
  USING (auth.jwt() ->> 'role' = 'admin');
```

Read `reference/database-patterns.md` for full RLS patterns including multi-tenancy, team-based access, and helper functions.

## Storage

```ts
// Upload a file
const { data, error } = await supabase.storage
  .from('avatars')
  .upload(`${userId}/avatar.png`, file, { upsert: true })

// Get a public URL (public bucket)
const { data: { publicUrl } } = supabase.storage
  .from('avatars')
  .getPublicUrl(`${userId}/avatar.png`)

// Get a signed URL (private bucket, expires in 60 seconds)
const { data, error } = await supabase.storage
  .from('documents')
  .createSignedUrl(`${userId}/file.pdf`, 60)
```

Read `reference/realtime-storage.md` for image transformations, resumable uploads, and storage RLS.

## Realtime

```ts
'use client'
// Subscribe to table changes
const channel = supabase
  .channel('posts-changes')
  .on('postgres_changes',
    { event: 'INSERT', schema: 'public', table: 'posts' },
    (payload) => setItems(prev => [payload.new as Post, ...prev])
  )
  .subscribe()

return () => { supabase.removeChannel(channel) }
```

Read `reference/realtime-storage.md` for presence, broadcast, and channel cleanup patterns.

## Anti-Patterns

- **Do not disable RLS** — even temporarily; attackers do not wait for you to re-enable it
- **Do not use `service_role` on the client** — it bypasses all security policies; it belongs only in trusted server environments
- **Do not skip migrations** — dashboard edits to schema are not tracked in version control and will diverge between environments
- **Do not store auth state in localStorage** — the `@supabase/ssr` client handles sessions via HttpOnly cookies; localStorage is not accessible server-side and is vulnerable to XSS
- **Do not call `getSession()` on the server** — use `getUser()` instead; `getSession()` does not revalidate the token against the Supabase server
- **Do not use `createClient` from `@supabase/supabase-js` in Next.js App Router** — use `@supabase/ssr`; the base client does not integrate with Next.js cookie handling

## Related

- `reference/auth-patterns.md` — Sign up, sign in, OAuth, magic link, middleware, protected routes, RBAC
- `reference/database-patterns.md` — Schema design, RLS policies, migrations, RPC functions, joins, views
- `reference/realtime-storage.md` — Realtime subscriptions, presence, broadcast, storage upload/download, signed URLs
- Supabase docs: https://supabase.com/docs
- `@supabase/ssr` docs: https://supabase.com/docs/guides/auth/server-side/nextjs