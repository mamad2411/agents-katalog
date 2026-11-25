---
name: auth-setup
description: >
  Trigger when the user wants to add authentication to their app — sign up, sign in, session management, protected routes, or role-based access control. Also trigger for switching auth providers, debugging auth issues, or adding OAuth/SSO.
source:
  repository: armaneker/claude-code-skills
  original_path: saas-builder-kit/skills/auth-setup
  original_name: auth-setup
status: canonical
---
# Auth Setup

You are an expert in web authentication. Set up complete, production-safe auth with protected routes, sessions, and role-based access control.

## Workflow

1. **Identify the framework:** Next.js (default), Express, Fastify, other
2. **Choose the auth provider** based on requirements:
   - **NextAuth.js (Auth.js)** — best for Next.js, supports many OAuth providers + credentials
   - **Supabase Auth** — best when already using Supabase DB; built-in email/OAuth/magic links
   - **Clerk** — best when you want a full UI + managed auth with minimal code
3. **Identify required auth methods:** email+password, Google/GitHub OAuth, magic link, SSO

---

## Option A: NextAuth.js (Auth.js v5)

### Installation
```bash
npm install next-auth@beta
npx auth secret  # generates AUTH_SECRET
```

### Configuration (`auth.ts`)
```typescript
import NextAuth from 'next-auth';
import { PrismaAdapter } from '@auth/prisma-adapter';
import GitHub from 'next-auth/providers/github';
import Google from 'next-auth/providers/google';
import Credentials from 'next-auth/providers/credentials';
import { db } from '@/lib/db';
import bcrypt from 'bcryptjs';

export const { handlers, auth, signIn, signOut } = NextAuth({
  adapter: PrismaAdapter(db),
  session: { strategy: 'jwt' }, // use 'database' for server-side sessions
  providers: [
    GitHub({ clientId: process.env.GITHUB_ID!, clientSecret: process.env.GITHUB_SECRET! }),
    Google({ clientId: process.env.GOOGLE_ID!, clientSecret: process.env.GOOGLE_SECRET! }),
    Credentials({
      async authorize(credentials) {
        const { email, password } = credentials as { email: string; password: string };
        const user = await db.user.findUnique({ where: { email } });
        if (!user?.passwordHash) return null;
        const valid = await bcrypt.compare(password, user.passwordHash);
        return valid ? user : null;
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) { token.id = user.id; token.role = (user as any).role; }
      return token;
    },
    async session({ session, token }) {
      session.user.id = token.id as string;
      session.user.role = token.role as string;
      return session;
    },
  },
  pages: {
    signIn: '/login',
    error: '/login',
  },
});
```

### Route Handler (`app/api/auth/[...nextauth]/route.ts`)
```typescript
import { handlers } from '@/auth';
export const { GET, POST } = handlers;
```

### Middleware — Protect Routes (`middleware.ts`)
```typescript
import { auth } from '@/auth';
import { NextResponse } from 'next/server';

export default auth((req) => {
  const isLoggedIn = !!req.auth;
  const isProtected = req.nextUrl.pathname.startsWith('/dashboard') ||
                      req.nextUrl.pathname.startsWith('/settings');

  if (isProtected && !isLoggedIn) {
    return NextResponse.redirect(new URL('/login', req.url));
  }
});

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
```

### Server Component Auth Check
```typescript
import { auth } from '@/auth';
import { redirect } from 'next/navigation';

export default async function DashboardPage() {
  const session = await auth();
  if (!session) redirect('/login');

  return <div>Welcome, {session.user.name}</div>;
}
```

### Role-Based Access
```typescript
// Type augmentation (types/next-auth.d.ts)
declare module 'next-auth' {
  interface User { role: string }
  interface Session { user: { id: string; role: string } & DefaultSession['user'] }
}

// In a server component or API route
const session = await auth();
if (session?.user.role !== 'admin') {
  redirect('/unauthorized');
}
```

---

## Option B: Supabase Auth

### Installation
```bash
npm install @supabase/supabase-js @supabase/ssr
```

### Client Setup
```typescript
// lib/supabase/server.ts
import { createServerClient } from '@supabase/ssr';
import { cookies } from 'next/headers';

export function createClient() {
  const cookieStore = cookies();
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() { return cookieStore.getAll(); },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value, options }) =>
            cookieStore.set(name, value, options));
        },
      },
    }
  );
}
```

### Sign Up / Sign In
```typescript
// app/actions/auth.ts
'use server';
import { createClient } from '@/lib/supabase/server';
import { redirect } from 'next/navigation';

export async function signUp(email: string, password: string) {
  const supabase = createClient();
  const { error } = await supabase.auth.signUp({ email, password,
    options: { emailRedirectTo: `${process.env.APP_URL}/auth/callback` }
  });
  if (error) throw error;
  redirect('/check-email');
}

export async function signIn(email: string, password: string) {
  const supabase = createClient();
  const { error } = await supabase.auth.signInWithPassword({ email, password });
  if (error) throw error;
  redirect('/dashboard');
}
```

### Middleware
```typescript
// middleware.ts
import { createServerClient } from '@supabase/ssr';
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export async function middleware(request: NextRequest) {
  let response = NextResponse.next({ request });
  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    { cookies: { getAll: () => request.cookies.getAll(),
        setAll: (c) => { c.forEach(({ name, value, options }) => response.cookies.set(name, value, options)); } } }
  );

  const { data: { user } } = await supabase.auth.getUser();
  const isProtected = request.nextUrl.pathname.startsWith('/dashboard');

  if (isProtected && !user) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  return response;
}
```

---

## Option C: Clerk

### Installation
```bash
npm install @clerk/nextjs
```

### Provider (`app/layout.tsx`)
```typescript
import { ClerkProvider } from '@clerk/nextjs';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <ClerkProvider>
      <html><body>{children}</body></html>
    </ClerkProvider>
  );
}
```

### Middleware
```typescript
// middleware.ts
import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server';

const isProtected = createRouteMatcher(['/dashboard(.*)', '/settings(.*)']);

export default clerkMiddleware((auth, req) => {
  if (isProtected(req)) auth().protect();
});

export const config = { matcher: ['/((?!.*\\..*|_next).*)', '/', '/(api|trpc)(.*)'] };
```

### Access User in Server Components
```typescript
import { currentUser } from '@clerk/nextjs/server';
import { redirect } from 'next/navigation';

export default async function Page() {
  const user = await currentUser();
  if (!user) redirect('/sign-in');
  return <div>Hello {user.firstName}</div>;
}
```

---

## Database Schema for Auth (NextAuth Prisma Adapter)

```prisma
model Account {
  id                String  @id @default(cuid())
  userId            String
  type              String
  provider          String
  providerAccountId String
  refresh_token     String? @db.Text
  access_token      String? @db.Text
  expires_at        Int?
  token_type        String?
  scope             String?
  id_token          String? @db.Text
  session_state     String?
  user User @relation(fields: [userId], references: [id], onDelete: Cascade)
  @@unique([provider, providerAccountId])
}

model Session {
  id           String   @id @default(cuid())
  sessionToken String   @unique
  userId       String
  expires      DateTime
  user         User     @relation(fields: [userId], references: [id], onDelete: Cascade)
}

model User {
  id            String    @id @default(cuid())
  name          String?
  email         String?   @unique
  emailVerified DateTime?
  image         String?
  role          String    @default("user")
  passwordHash  String?
  accounts      Account[]
  sessions      Session[]
}
```

## Common Pitfalls — Avoid These

- **Storing passwords in plain text** — always `bcrypt.hash(password, 12)`, never less than 10 rounds
- **Relying on client-side route guards only** — always validate on the server (middleware or server component)
- **Not setting `httpOnly: true` on session cookies** — prevents XSS token theft
- **Missing CSRF protection on credentials endpoints** — NextAuth handles this; custom implementations must add it
- **Exposing JWT secret in client bundle** — `AUTH_SECRET` / `NEXTAUTH_SECRET` must only be in server env
- **Not invalidating sessions on password change** — update session version or force re-login after password reset
- **Skipping email verification** — at minimum, flag unverified accounts and limit their access

## Purpose
Add authentication (sign up, sign in, sessions) to an app.

## When to use
The user wants authentication added.

## When NOT to use
- Authorization design only (RBAC).

## Inputs
Stack, providers, user model.

## Output requirements
Working auth flows with tests.

## Example
```text
Email+password with hashed passwords, session cookie, password reset.
```

## Related skills
secure-code-guardian, firebase-auth-manager
