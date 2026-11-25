# Supabase Skill

You are working with Supabase. Apply these conventions.

## Client Setup

- Use `@supabase/ssr` for Next.js / SvelteKit / Nuxt — it handles cookies for SSR auth automatically.
- Create a server client in Server Components / Route Handlers.
  **Next.js 15+ / 16**: `cookies()` is async — always `await` it:
  ```ts
  import { createServerClient } from '@supabase/ssr';
  import { cookies } from 'next/headers';
  export async function createClient() {
    const cookieStore = await cookies();
    return createServerClient(process.env.NEXT_PUBLIC_SUPABASE_URL!, process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!, {
      cookies: {
        getAll: () => cookieStore.getAll(),
        setAll: (cs) => cs.forEach(({ name, value, options }) => cookieStore.set(name, value, options)),
      },
    });
  }
  ```
- Never import the browser client in Server Components — always use the server client.

## Authentication

- Use `supabase.auth.signInWithOAuth()`, `signInWithPassword()`, or `signInWithOTP()`.
- Protect routes with middleware: check `supabase.auth.getUser()` in `middleware.ts`. Never trust cookies alone.
- Always call `supabase.auth.getUser()` (not `getSession()`) on the server — `getUser()` revalidates the JWT with the Auth server.

## Row Level Security (RLS)

- Always enable RLS on tables: `ALTER TABLE posts ENABLE ROW LEVEL SECURITY;`
- Write explicit policies for each operation (SELECT, INSERT, UPDATE, DELETE).
- Use `auth.uid()` inside policies to scope rows to the current user.
- Test policies with the Supabase Dashboard SQL editor using `SET LOCAL role = authenticated; SET LOCAL request.jwt.claims.sub = 'uuid';`.

## Database Operations

- Use the Supabase client for simple CRUD from the client: `supabase.from('posts').select('*').eq('user_id', userId)`.
- For complex queries, call Postgres functions via RPC: `supabase.rpc('my_function', { param: value })`.
- Use the generated TypeScript types: `supabase gen types typescript --project-id <id> > types/database.ts`.

## Storage

- Use Supabase Storage for file uploads; create buckets with RLS policies to control access.
- Generate signed URLs for private assets: `supabase.storage.from('bucket').createSignedUrl(path, 3600)`.

## Realtime

- Subscribe to Postgres changes: `supabase.channel('…').on('postgres_changes', { event: '*', schema: 'public', table: 'messages' }, callback).subscribe()`.
- Always unsubscribe on component unmount to avoid memory leaks.
