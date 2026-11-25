---
name: supabase-pro
description: "Supabase auth, RLS, realtime, storage, edge functions, database design. Use when building or reviewing Supabase-backed applications."
---

# Supabase Pro

## Purpose

Build production-grade applications on Supabase. Covers auth, Row Level Security, realtime subscriptions, storage policies, Edge Functions, and database design patterns.

## When to Use

**Use this when:**
- Building auth flows, session handling, or protected API routes on Supabase
- Writing or auditing Row Level Security policies for any table
- Implementing realtime subscriptions, storage policies, or Edge Functions

**Use this ESPECIALLY when:**
- A table exists in Supabase without RLS enabled — any anon key request can read it
- Server-side code uses the service role key where the anon key with user context is correct
- Edge Functions need to query the database on behalf of the authenticated caller

**Don't skip when:**
- Creating any new table — RLS must be enabled and all four CRUD policies written before the table is exposed to clients
- Migrating from client-side to server-side Supabase auth (the SSR cookie pattern is mandatory for Next.js App Router)
- Setting up storage buckets — missing upload/delete policies are a common data exposure vector

## Core Patterns

### 1. Database Schema Design

```sql
-- UUIDs, timestamptz, RLS on every table
CREATE TABLE projects (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name        TEXT NOT NULL,
  description TEXT DEFAULT '',
  owner_id    UUID NOT NULL REFERENCES auth.users(id),
  status      TEXT NOT NULL DEFAULT 'active'
    CHECK (status IN ('active', 'archived', 'deleted')),
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Enable RLS on every table
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
```

### 2. Row Level Security (RLS) Policies

```sql
-- Every policy must be explicit (no public access by default)

-- Users can only see their own projects
CREATE POLICY "Users can view own projects"
  ON projects FOR SELECT
  USING (owner_id = auth.uid());

-- Users can create their own projects
CREATE POLICY "Users can create projects"
  ON projects FOR INSERT
  WITH CHECK (owner_id = auth.uid());

-- Users can update their own projects
CREATE POLICY "Users can update own projects"
  ON projects FOR UPDATE
  USING (owner_id = auth.uid())
  WITH CHECK (owner_id = auth.uid());

-- Users can delete their own projects
CREATE POLICY "Users can delete own projects"
  ON projects FOR DELETE
  USING (owner_id = auth.uid());

-- Admin override (service_role bypasses RLS)
CREATE POLICY "Admins can view all projects"
  ON projects FOR SELECT
  USING (is_admin(auth.uid()));
```

### 3. Auth Patterns

```javascript
// Server-side auth
import { createServerClient } from '@supabase/ssr'

export async function getServerClient() {
  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
    { cookies: { getAll, setAll } }
  )
  return supabase
}

// Client-side auth
import { createBrowserClient } from '@supabase/ssr'

const supabase = createBrowserClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
)

// Sign up
const { data, error } = await supabase.auth.signUp({
  email: 'user@example.com',
  password: 'password123',
  options: { data: { full_name: 'John Doe' } }
})

// Protected API route
export async function POST(req: Request) {
  const supabase = await getServerClient()
  const { data: { user } } = await supabase.auth.getUser()
  if (!user) return Response.json({ error: 'Unauthorized' }, { status: 401 })

  const { data } = await supabase.from('projects').insert({
    name: 'New Project',
    owner_id: user.id,
  })
  return Response.json(data)
}
```

### 4. Realtime Subscriptions

```javascript
// Subscribe to changes
const channel = supabase
  .channel('project-changes')
  .on(
    'postgres_changes',
    {
      event: '*',
      schema: 'public',
      table: 'projects',
      filter: `owner_id=eq.${user.id}`,
    },
    (payload) => {
      console.log('Change received!', payload)
      // Optimistic UI update
    }
  )
  .subscribe()
```

### 5. Storage Policies

```sql
-- Bucket: project-files
-- Public bucket for avatars
CREATE POLICY "Public read access"
  ON storage.objects FOR SELECT
  USING (bucket_id = 'project-files');

-- Authenticated users can upload
CREATE POLICY "Authenticated users can upload"
  ON storage.objects FOR INSERT
  WITH CHECK (
    bucket_id = 'project-files'
    AND auth.role() = 'authenticated'
  );

-- Users can only delete their own files
CREATE POLICY "Users can delete own files"
  ON storage.objects FOR DELETE
  USING (
    bucket_id = 'project-files'
    AND owner_id = auth.uid()
  );
```

### 6. Edge Functions

```typescript
// supabase/functions/generate-report/index.ts
import { serve } from 'https://deno.land/std/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

serve(async (req) => {
  const authHeader = req.headers.get('Authorization')!
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_ANON_KEY')!,
    { global: { headers: { Authorization: authHeader } } }
  )

  const { projectId } = await req.json()
  const { data: project } = await supabase
    .from('projects')
    .select('*')
    .eq('id', projectId)
    .single()

  if (!project) return new Response('Not found', { status: 404 })

  return new Response(JSON.stringify({ report: generateReport(project) }), {
    headers: { 'Content-Type': 'application/json' },
  })
})
```

### Checklist

- [ ] RLS enabled on EVERY table (no exceptions)
- [ ] Service role key only in server contexts (never client)
- [ ] Email confirmation enabled for signup
- [ ] Rate limiting on auth endpoints
- [ ] Row level security policies tested (anon user, authenticated user, different users)
- [ ] Real-time channels have appropriate filters (don't subscribe to entire tables)
- [ ] Storage buckets have proper MIME type restrictions
- [ ] Edge Functions have CORS headers for browser access
- [ ] Database functions use SECURITY DEFINER sparingly
- [ ] Migrations versioned (supabase migrations)

## Related Skills

- **postgres-pro** — Supabase is PostgreSQL; reach for postgres-pro when queries require advanced indexes, partitioning, CTEs, or zero-downtime migration techniques beyond what Supabase migrations cover
- **saas-pro** — when building a multi-tenant SaaS on Supabase, saas-pro covers subscription billing, feature flags, and usage metering that complement the auth and RLS patterns here
- **security-reviewer** — RLS policy correctness, service role key exposure, and storage bucket policies are security-critical; cross-reference when auditing any Supabase project for access control gaps
- **frontend-senior-engineer** — client-side Supabase usage (browser client, realtime subscriptions, auth state management in React/Next.js) lives in frontend code; coordinate for SSR cookie auth and optimistic UI patterns
- **backend-senior-engineer** — server-side Supabase client setup, protected API routes, and Edge Function logic are backend concerns; use when the server-side auth pattern needs to integrate with a broader API layer
- **test-engineer** — testing RLS policies requires running queries as different Postgres roles; use together when writing integration tests that verify tenant isolation or auth edge cases
