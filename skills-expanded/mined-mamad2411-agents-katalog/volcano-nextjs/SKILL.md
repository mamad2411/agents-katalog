---
name: volcano-nextjs
description: Use for Next.js on Volcano and for web apps, pages, dashboards, boards, galleries, full-stack UIs, public HTTP routes, redirects, webhook ingress, middleware, API routes, server actions, and client or server SDK separation.
---
# Volcano Next.js Skill

## Role
Implement Volcano SDK in Next.js with strict client/server separation and middleware-first auth checks. This skill is self-contained: env contract, shared client pattern, AuthContext template, middleware helpers, app/pages router examples, server actions, OAuth callback, and SSR safety are embedded.

## Workflow
1. Centralize the Volcano client behind a `getVolcano()` helper used by all client components.
2. Use middleware helpers (`createServerClient`, `withAuth`, `getTokenFromRequest`) for server/middleware auth checks.
3. Keep browser-only auth actions (OAuth initiation, localStorage session) out of server-only code.
4. Validate redirect/protection behavior and hydration edge cases.

## UI/UX Pairing
Read `volcano-uiux` for every user-facing Next.js interface. It owns accessibility, responsive layout, loading and progress feedback, forms, navigation, and interface-state guidance. This skill owns the Next.js implementation and client/server boundary.

## Environment Contract
A deployed frontend builds with the project variables its `volcano-config.yaml`
entry selects. Declare them in `volcano/volcano.env` for the local server and
in `volcano/cloud.env` for the cloud project, where the API URL is
`https://api.volcano.dev`:
```env
NEXT_PUBLIC_VOLCANO_API_URL=http://localhost:8000
NEXT_PUBLIC_VOLCANO_ANON_KEY=ak-your-anon-key
NEXT_PUBLIC_VOLCANO_DATABASE=app
```
Then select them in the frontend's entry in `volcano/volcano-config.yaml`:
```yaml
# volcano-config.yaml
version: 1
frontends:
  - name: web
    variable_scope: scoped
    variables: [NEXT_PUBLIC_VOLCANO_API_URL, NEXT_PUBLIC_VOLCANO_ANON_KEY, NEXT_PUBLIC_VOLCANO_DATABASE]
```
- `NEXT_PUBLIC_*` vars are exposed to both client and server.
- Server-only secrets MUST NOT have the `NEXT_PUBLIC_` prefix.
- `web/.env.local` serves only `npm run dev`. Deploys never upload it, so a
  value kept only there is missing from every deployed build.

## Execution Environments
| Environment | SDK usage |
|---|---|
| Client Components | Full SDK — auth, queries, storage, realtime |
| Server Components | No direct SDK — call API routes, server actions, or middleware-derived data |
| Middleware | `@volcano.dev/sdk/next/middleware` helpers |
| API Routes / Route Handlers | Server client for token validation; full SDK with the bearer token for queries |

## Shared Client Pattern (lib/volcano.ts)
```ts
// lib/volcano.ts
import { VolcanoAuth } from '@volcano.dev/sdk';

let volcano: VolcanoAuth | null = null;

export function getVolcano(): VolcanoAuth {
  if (!volcano) {
    volcano = new VolcanoAuth({
      apiUrl: process.env.NEXT_PUBLIC_VOLCANO_API_URL!,
      anonKey: process.env.NEXT_PUBLIC_VOLCANO_ANON_KEY!,
    });
    volcano.database(process.env.NEXT_PUBLIC_VOLCANO_DATABASE!);
  }
  return volcano;
}
```

## AuthContext Provider (Client Component)
```tsx
// context/AuthContext.tsx
'use client';

import { createContext, useContext, useEffect, useState, useCallback, ReactNode } from 'react';
import { getVolcano } from '@/lib/volcano';
import type { User } from '@volcano.dev/sdk';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const volcano = getVolcano();

    // Restore session on mount
    volcano.initialize().then(({ user }) => {
      setUser(user);
      setLoading(false);
    });

    // React to subsequent changes
    const unsubscribe = volcano.auth.onAuthStateChange(setUser);
    return () => unsubscribe();
  }, []);

  const signIn = useCallback(async (email: string, password: string) => {
    const { error } = await getVolcano().auth.signIn({ email, password });
    if (error) throw error;
  }, []);

  const signUp = useCallback(async (email: string, password: string) => {
    const { error } = await getVolcano().auth.signUp({ email, password });
    if (error) throw error;
  }, []);

  const signOut = useCallback(async () => {
    await getVolcano().auth.signOut();
  }, []);

  return (
    <AuthContext.Provider value={{ user, loading, signIn, signUp, signOut }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within an AuthProvider');
  return ctx;
}
```

Wire in `app/layout.tsx`:
```tsx
import { AuthProvider } from '@/context/AuthContext';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en"><body><AuthProvider>{children}</AuthProvider></body></html>
  );
}
```

## Protected Page (Client Component)
```tsx
'use client';
import { useAuth } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import { getVolcano } from '@/lib/volcano';

export default function DashboardPage() {
  const { user, loading } = useAuth();
  const router = useRouter();
  const [posts, setPosts] = useState<any[]>([]);

  useEffect(() => {
    if (!loading && !user) router.push('/login');
  }, [user, loading, router]);

  useEffect(() => {
    if (!user) return;
    getVolcano()
      .from('posts')
      .select('*')
      .order('created_at', { ascending: false })
      .limit(10)
      .then(({ data }) => setPosts(data ?? []));
  }, [user]);

  if (loading) return <div>Loading...</div>;
  if (!user) return null;

  return (
    <div>
      <h1>Welcome, {user.email}</h1>
      <ul>{posts.map((p) => <li key={p.id}>{p.title}</li>)}</ul>
    </div>
  );
}
```

## Middleware (Edge auth checks)
```ts
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { createServerClient, withAuth } from '@volcano.dev/sdk/next/middleware';

export async function middleware(request: NextRequest) {
  const client = createServerClient({
    anonKey: process.env.NEXT_PUBLIC_VOLCANO_ANON_KEY!,
    apiUrl: process.env.NEXT_PUBLIC_VOLCANO_API_URL,
  });

  const user = await withAuth(request, client);

  if (request.nextUrl.pathname.startsWith('/dashboard') && !user) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
  if (request.nextUrl.pathname === '/login' && user) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }
  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*', '/login'],
};
```

## Middleware Helpers API
```ts
import {
  createServerClient,
  withAuth,
  getTokenFromRequest,
  isBrowser,
  isServer,
} from '@volcano.dev/sdk/next/middleware';

const client = createServerClient({ anonKey, apiUrl }); // apiUrl optional

const user = await withAuth(request, client);     // null when invalid/missing
const token = getTokenFromRequest(request);       // Authorization header or cookie
const { user, error } = await client.getUser(token);
const { accessToken, refreshToken, error } = await client.refreshToken(oldRefreshToken);

if (isBrowser()) { /* ... */ }
if (isServer())  { /* ... */ }
```

## API Routes — App Router (Route Handlers)
```ts
// app/api/posts/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { createServerClient, getTokenFromRequest } from '@volcano.dev/sdk/next/middleware';
import { VolcanoAuth } from '@volcano.dev/sdk';

export async function GET(request: NextRequest) {
  const client = createServerClient({
    anonKey: process.env.NEXT_PUBLIC_VOLCANO_ANON_KEY!,
    apiUrl: process.env.NEXT_PUBLIC_VOLCANO_API_URL,
  });

  const token = getTokenFromRequest(request);
  if (!token) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });

  const { user, error } = await client.getUser(token);
  if (error || !user) return NextResponse.json({ error: 'Invalid token' }, { status: 401 });

  // Use the SDK with the bearer token for queries / function calls
  const volcano = new VolcanoAuth({
    apiUrl: process.env.NEXT_PUBLIC_VOLCANO_API_URL!,
    anonKey: process.env.NEXT_PUBLIC_VOLCANO_ANON_KEY!,
    accessToken: token,
  });

  const { data, error: queryError } = await volcano.functions.invoke('get-user-posts');
  if (queryError) return NextResponse.json({ error: queryError.message }, { status: 500 });

  return NextResponse.json({ posts: data });
}
```

## API Routes — Pages Router
```ts
// pages/api/posts.ts
import type { NextApiRequest, NextApiResponse } from 'next';
import { VolcanoAuth } from '@volcano.dev/sdk';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const token = req.headers.authorization?.replace('Bearer ', '');
  if (!token) return res.status(401).json({ error: 'Unauthorized' });

  const volcano = new VolcanoAuth({
    apiUrl: process.env.NEXT_PUBLIC_VOLCANO_API_URL!,
    anonKey: process.env.NEXT_PUBLIC_VOLCANO_ANON_KEY!,
    accessToken: token,
  });
  volcano.database(process.env.NEXT_PUBLIC_VOLCANO_DATABASE!);

  const { data, error } = await volcano
    .from('posts')
    .select('*')
    .order('created_at', { ascending: false });
  if (error) return res.status(500).json({ error: error.message });

  return res.status(200).json({ posts: data });
}
```

## Cookie Sync — required for Server Actions and middleware token reads

The SDK stores tokens in localStorage by default. Server Actions, route handlers, and middleware run on the server and cannot read localStorage — they read cookies. Add a small client component that mirrors the access token to a cookie whenever auth state changes:

```tsx
// components/CookieSync.tsx
'use client';
import { useEffect } from 'react';
import { getVolcano } from '@/lib/volcano';

export function CookieSync() {
  useEffect(() => {
    const volcano = getVolcano();
    const sync = (token: string | null) => {
      const base = 'Path=/; SameSite=Lax; Secure';
      document.cookie = token
        ? `volcano_access_token=${token}; ${base}; Max-Age=3600`
        : `volcano_access_token=; ${base}; Max-Age=0`;
    };
    sync(volcano.accessToken ?? null);
    const unsub = volcano.auth.onAuthStateChange(() => {
      sync(volcano.accessToken ?? null);
    });
    return () => unsub();
  }, []);
  return null;
}
```

Mount it once, alongside the `AuthProvider`:

```tsx
// app/layout.tsx
import { AuthProvider } from '@/context/AuthContext';
import { CookieSync } from '@/components/CookieSync';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <AuthProvider>
          <CookieSync />
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
```

**Security note:** This cookie is JS-readable, which matches the SDK's localStorage exposure — the XSS surface area is identical. For higher-security postures, set an `httpOnly` cookie from an API route after sign-in and read it server-side via `getTokenFromRequest`. The client-mirrored pattern shown above is the simplest route to a working Server Action.

## Server Components & Server Actions
Server Components don't have localStorage. Three options:
1. Fetch from API routes (which validate the token).
2. Use Server Actions with the SDK and the cookie token.
3. Pass middleware-derived data via headers.

### Server Action template
```ts
// app/actions.ts
'use server';

import { cookies } from 'next/headers';
import { createServerClient } from '@volcano.dev/sdk/next/middleware';
import { VolcanoAuth } from '@volcano.dev/sdk';

export async function getPosts() {
  const cookieStore = cookies();
  const token = cookieStore.get('volcano_access_token')?.value;
  if (!token) throw new Error('Not authenticated');

  const client = createServerClient({
    anonKey: process.env.NEXT_PUBLIC_VOLCANO_ANON_KEY!,
    apiUrl: process.env.NEXT_PUBLIC_VOLCANO_API_URL,
  });
  const { user, error } = await client.getUser(token);
  if (error || !user) throw new Error('Invalid session');

  const volcano = new VolcanoAuth({
    apiUrl: process.env.NEXT_PUBLIC_VOLCANO_API_URL!,
    anonKey: process.env.NEXT_PUBLIC_VOLCANO_ANON_KEY!,
    accessToken: token,
  });
  volcano.database(process.env.NEXT_PUBLIC_VOLCANO_DATABASE!);

  const { data } = await volcano
    .from('posts')
    .select('id, title, created_at')
    .order('created_at', { ascending: false })
    .limit(10);
  return data;
}
```

```tsx
// app/posts/page.tsx
import { getPosts } from '@/app/actions';

export default async function PostsPage() {
  const posts = await getPosts();
  return <ul>{posts?.map((p) => <li key={p.id}>{p.title}</li>)}</ul>;
}
```

## Realtime in Next.js (Client Component required)
```tsx
'use client';
import { useEffect, useState } from 'react';
import { VolcanoRealtime } from '@volcano.dev/sdk/realtime';
import { getVolcano } from '@/lib/volcano';
import { useAuth } from '@/context/AuthContext';

export function LivePosts() {
  const { user } = useAuth();
  const [posts, setPosts] = useState<any[]>([]);

  useEffect(() => {
    if (!user) return;
    const volcano = getVolcano();

    volcano
      .from('posts')
      .select('*')
      .order('created_at', { ascending: false })
      .then(({ data }) => setPosts(data ?? []));

    const realtime = new VolcanoRealtime({
      apiUrl: process.env.NEXT_PUBLIC_VOLCANO_API_URL!,
      anonKey: process.env.NEXT_PUBLIC_VOLCANO_ANON_KEY!,
      accessToken: volcano.accessToken!,
    });

    realtime.connect().then(() => {
      const channel = realtime.channel('posts', { type: 'postgres' });
      channel.onPostgresChanges('INSERT', 'public', 'posts', (c) =>
        setPosts((cur) => [c.record, ...cur]));
      channel.onPostgresChanges('UPDATE', 'public', 'posts', (c) =>
        setPosts((cur) => cur.map((p) => (p.id === c.record.id ? c.record : p))));
      channel.onPostgresChanges('DELETE', 'public', 'posts', (c) =>
        setPosts((cur) => cur.filter((p) => p.id !== c.old_record.id)));
      channel.subscribe();
    });

    return () => { realtime.disconnect(); };
  }, [user]);

  return <ul>{posts.map((p) => <li key={p.id}>{p.title}</li>)}</ul>;
}
```

## Default Signup & Login Pages
When the prompt doesn't specify signup/login page design, apply the `volcano-auth` "Default Signup & Login Page UX" and the shared `volcano-uiux` rules — including the default signup-success alert — on top of the `AuthContext` from this skill. The examples below show Next.js auth wiring; add the labels, progress feedback, responsive layout, and complete states required by `volcano-uiux`.

```tsx
// app/signup/page.tsx — default signup page with a success alert
'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/context/AuthContext';

export default function SignupPage() {
  const { signUp } = useAuth();
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (submitting || success) return;
    setError(null);
    setSubmitting(true);
    try {
      await signUp(email, password);
      setSuccess(true); // default "Signup success" alert — shown even if not requested
      setSubmitting(false);
      setTimeout(() => router.push('/login'), 2000);
    } catch (err: any) {
      setError(err.message);
      setSubmitting(false);
    }
  };

  return (
    <div>
      {success && (
        <div role="alert">Signup successful! Check your email to verify your account.</div>
      )}
      {error && <div role="alert">{error}</div>}
      <form onSubmit={handleSubmit}>
        <label htmlFor="signup-email">Email</label>
        <input id="signup-email" type="email" autoComplete="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        <label htmlFor="signup-password">Password</label>
        <input id="signup-password" type="password" autoComplete="new-password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        <button type="submit" disabled={submitting || success} aria-busy={submitting}>
          {success ? 'Account created' : submitting ? 'Signing up…' : 'Sign Up'}
        </button>
        <span role="status">{submitting ? 'Creating account…' : ''}</span>
      </form>
      <Link href="/login">Already have an account? Log in</Link>
    </div>
  );
}
```

```tsx
// app/login/page.tsx — default login page (email/password)
'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useAuth } from '@/context/AuthContext';

export default function LoginPage() {
  const { signIn } = useAuth();
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (submitting) return;
    setError(null);
    setSubmitting(true);
    try {
      await signIn(email, password);
      router.push('/dashboard');
    } catch (err: any) {
      setError(err.message);
      setSubmitting(false);
    }
  };

  return (
    <div>
      {error && <div role="alert">{error}</div>}
      <form onSubmit={handleSubmit}>
        <label htmlFor="login-email">Email</label>
        <input id="login-email" type="email" autoComplete="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        <label htmlFor="login-password">Password</label>
        <input id="login-password" type="password" autoComplete="current-password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        <button type="submit" disabled={submitting} aria-busy={submitting}>
          {submitting ? 'Signing in…' : 'Sign In'}
        </button>
        <span role="status">{submitting ? 'Signing in…' : ''}</span>
      </form>
      <Link href="/signup">Need an account? Sign up</Link>
      <Link href="/forgot-password">Forgot password?</Link>
    </div>
  );
}
```

## OAuth in Next.js
OAuth initiation must be in a Client Component; the callback page reconciles the tokens. Add the OAuth button(s) to the default login page above (or use standalone, as shown) — don't replace the email/password form unless the user asks for OAuth-only login.

```tsx
// Add to app/login/page.tsx (or standalone) — OAuth button
'use client';
import { getVolcano } from '@/lib/volcano';

export function GoogleSignInButton() {
  return (
    <button onClick={() => getVolcano().auth.signInWithGoogle()}>
      Sign in with Google
    </button>
  );
}
```

```tsx
// app/auth/callback/page.tsx
'use client';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { getVolcano } from '@/lib/volcano';

export default function AuthCallbackPage() {
  const router = useRouter();
  useEffect(() => {
    getVolcano().initialize().then(({ user }) => {
      router.push(user ? '/dashboard' : '/login?error=auth_failed');
    });
  }, [router]);
  return <div>Completing sign in...</div>;
}
```

## SSR Safety
- `volcano.auth.signInWith*` (OAuth) only works in browser; calling it server-side throws.
- The SDK rejects service keys (`sk-...`) in browser environments.
- Use `isBrowser()` / `isServer()` from middleware helpers when branching.

## Best Practices
- **Single client instance** via `getVolcano()`. Don't `new VolcanoAuth(...)` in components.
- **Loading state** is a first-class case — don't render protected UI before `useAuth().loading === false`.
- **Pair `connect()` with `disconnect()`** for realtime in `useEffect` cleanup.
- **Validate tokens server-side** — do not trust client-supplied user state in API routes / actions.
- **Use `NEXT_PUBLIC_` only for non-secrets**; service keys never get this prefix.

## Verification Checklist
- User-facing interfaces pass the `volcano-uiux` verification checklist.
- Client/server responsibilities are clear and correct.
- Middleware uses `withAuth` (or equivalent) before allowing protected routes.
- Server components fetch via API routes / server actions / middleware data — never call browser SDK methods directly.
- Imports, env vars, dependencies, and init order are consistent.
- Realtime is wrapped in a Client Component with proper cleanup.

## Optional Fallback References
