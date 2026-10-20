# SAP-033: React Authentication - Provider Setup Workflows

**SAP**: SAP-033 (react-authentication)
**Domain**: Providers
**Version**: 1.0.0
**Last Updated**: 2025-11-10

---

## Overview

This file contains **4 authentication provider setup workflows** for Next.js 15+ projects:

1. **NextAuth v5** (30 min) - Self-hosted, FREE, custom UI
2. **Clerk** (7 min) - Fastest setup, $25+/mo, pre-built UI
3. **Supabase Auth** (20 min) - For Supabase projects, FREE (50k MAU)
4. **Auth0** (30 min) - Enterprise SSO, Enterprise pricing

**For advanced features** (RBAC, protected routes, magic links), see [../workflows/AGENTS.md](../workflows/AGENTS.md)

**For security patterns**, see [../security/AGENTS.md](../security/AGENTS.md)

**For troubleshooting**, see [../troubleshooting/AGENTS.md](../troubleshooting/AGENTS.md)

---

## Decision Tree: Which Provider?

```
START: Which authentication provider should I use?

├─ Q1: Need self-hosted (full control, no vendor lock-in)?
│  ├─ YES → NextAuth v5 ✅
│  │  Time: 30 min | Cost: FREE | UI: Custom
│  └─ NO → Continue to Q2
│
├─ Q2: Need rapid setup (<10 min) with pre-built UI?
│  ├─ YES → Clerk ✅
│  │  Time: 7 min | Cost: $25+/mo | UI: Pre-built
│  └─ NO → Continue to Q3
│
├─ Q3: Using Supabase for database?
│  ├─ YES → Supabase Auth ✅
│  │  Time: 20 min | Cost: FREE (50k MAU) | UI: Custom
│  └─ NO → Continue to Q4
│
├─ Q4: Enterprise SSO/SAML required?
│  ├─ YES → Auth0 ✅
│  │  Time: 30 min | Cost: Enterprise | UI: Universal Login
│  └─ NO → Continue to Q5
│
└─ Q5: Default choice (open-source, flexible)
   └─ NextAuth v5 ✅ (recommended default)
      Time: 30 min | Cost: FREE | UI: Custom
```

---

## Quick Comparison

| Criteria | NextAuth v5 | Clerk | Supabase Auth | Auth0 |
|----------|-------------|-------|---------------|-------|
| **Setup Time** | 30 min | **7 min** | 20 min | 30 min |
| **Cost** | **FREE** | $25+/mo | FREE (50k MAU) | Enterprise |
| **Pre-Built UI** | ❌ | ✅ | ❌ | ⚠️ Universal Login |
| **Self-Hosted** | ✅ | ❌ | ❌ | ❌ |
| **OAuth Providers** | 50+ | ~20 | ~15 | ~30 |
| **Best For** | Self-hosted | Rapid prototyping | Supabase projects | Enterprise SSO |
| **Session Management** | JWT or Database | JWT | JWT | JWT or Database |
| **RBAC** | Custom | Built-in | Custom | Built-in |
| **Multi-Factor Auth** | Custom | Built-in | Built-in | Built-in |

---

## Workflow 1: Set Up NextAuth v5

**Time**: 30 minutes

**Best For**: Self-hosted authentication, full control, no vendor lock-in

**Prerequisites**:
- SAP-020 adopted
- SAP-034 database configured (Prisma or Drizzle)

### Quick Setup Overview

**8 Steps**:
1. Install dependencies (3 min)
2. Create auth configuration (5 min)
3. Add API route handler (2 min)
4. Create middleware (5 min)
5. Add environment variables (2 min)
6. Update Prisma schema (4 min)
7. Create login page (5 min)
8. Test authentication (4 min)

---

### Step 1: Install Dependencies

```bash
npm install next-auth@beta @auth/prisma-adapter bcryptjs
npm install -D @types/bcryptjs
```

**Packages**:
- `next-auth@beta`: NextAuth v5 (App Router support)
- `@auth/prisma-adapter`: Prisma adapter for database sessions
- `bcryptjs`: Password hashing (for credentials provider)

---

### Step 2: Create Auth Configuration

```typescript
// auth.ts (project root)
import NextAuth from "next-auth";
import Google from "next-auth/providers/google";
import GitHub from "next-auth/providers/github";
import { PrismaAdapter } from "@auth/prisma-adapter";
import { prisma } from "@/lib/prisma";

export const { handlers, signIn, signOut, auth } = NextAuth({
  adapter: PrismaAdapter(prisma),

  session: {
    strategy: "jwt",
    maxAge: 30 * 24 * 60 * 60 // 30 days
  },

  providers: [
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!
    }),

    GitHub({
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!
    })
  ],

  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.userId = user.id;
        token.role = user.role; // Custom field
      }
      return token;
    },

    async session({ session, token }) {
      if (token) {
        session.user.id = token.userId as string;
        session.user.role = token.role as string;
      }
      return session;
    }
  },

  pages: {
    signIn: '/login',
    signOut: '/logout',
    error: '/error'
  }
});
```

**Key Configuration**:
- `adapter`: PrismaAdapter for database persistence
- `session.strategy`: "jwt" (stateless) or "database" (stateful)
- `providers`: OAuth providers (Google, GitHub, etc.)
- `callbacks`: Extend JWT and session with custom fields
- `pages`: Custom auth pages

---

### Step 3: Add API Route Handler

```typescript
// app/api/auth/[...nextauth]/route.ts
import { handlers } from "@/auth";

export const { GET, POST } = handlers;
```

**Why**: NextAuth v5 requires catch-all route for OAuth callbacks.

---

### Step 4: Create Middleware

```typescript
// middleware.ts (project root)
import { auth } from "@/auth";
import { NextResponse } from "next/server";

export default auth((req) => {
  const { pathname } = req.nextUrl;
  const isAuthenticated = !!req.auth;

  // Public routes
  const publicRoutes = ["/", "/login", "/signup", "/api/auth"];
  const isPublicRoute = publicRoutes.some(route =>
    pathname.startsWith(route)
  );

  if (isPublicRoute) {
    return NextResponse.next();
  }

  // Protected routes
  if (!isAuthenticated) {
    const loginUrl = new URL("/login", req.url);
    loginUrl.searchParams.set("callbackUrl", pathname);
    return NextResponse.redirect(loginUrl);
  }

  return NextResponse.next();
});

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
};
```

**Key Features**:
- Protects all routes except public routes
- Redirects unauthenticated users to login
- Preserves original URL in callbackUrl

---

### Step 5: Add Environment Variables

```bash
# .env.local
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-key-here

# Generate secret with: openssl rand -base64 32

# Google OAuth (get from https://console.cloud.google.com)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# GitHub OAuth (get from https://github.com/settings/developers)
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
```

**Generate NEXTAUTH_SECRET**:
```bash
openssl rand -base64 32
```

---

### Step 6: Update Prisma Schema

```prisma
// prisma/schema.prisma
model User {
  id            String    @id @default(cuid())
  name          String?
  email         String    @unique
  emailVerified DateTime?
  image         String?
  role          String    @default("user")
  accounts      Account[]
  sessions      Session[]
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt
}

model Account {
  id                String  @id @default(cuid())
  userId            String
  type              String
  provider          String
  providerAccountId String
  refresh_token     String?
  access_token      String?
  expires_at        Int?
  token_type        String?
  scope             String?
  id_token          String?
  session_state     String?
  user              User    @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@unique([provider, providerAccountId])
}

model Session {
  id           String   @id @default(cuid())
  sessionToken String   @unique
  userId       String
  expires      DateTime
  user         User     @relation(fields: [userId], references: [id], onDelete: Cascade)
}

model VerificationToken {
  identifier String
  token      String   @unique
  expires    DateTime

  @@unique([identifier, token])
}
```

**Run migration**:
```bash
npx prisma migrate dev --name add-auth-tables
npx prisma generate
```

---

### Step 7: Create Login Page

```typescript
// app/login/page.tsx
"use client";

import { signIn } from "next-auth/react";

export default function LoginPage() {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="w-full max-w-md space-y-4 p-8 bg-white shadow rounded">
        <h1 className="text-2xl font-bold text-center">Sign In</h1>

        <button
          onClick={() => signIn("google", { callbackUrl: "/dashboard" })}
          className="w-full py-2 px-4 bg-white border border-gray-300 rounded hover:bg-gray-50"
        >
          Sign in with Google
        </button>

        <button
          onClick={() => signIn("github", { callbackUrl: "/dashboard" })}
          className="w-full py-2 px-4 bg-gray-900 text-white rounded hover:bg-gray-800"
        >
          Sign in with GitHub
        </button>
      </div>
    </div>
  );
}
```

---

### Step 8: Test Authentication

```typescript
// app/dashboard/page.tsx
import { auth } from "@/auth";
import { redirect } from "next/navigation";

export default async function DashboardPage() {
  const session = await auth();

  if (!session) {
    redirect("/login");
  }

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Welcome, {session.user.name}!</p>
      <p>Email: {session.user.email}</p>
    </div>
  );
}
```

**Test Steps**:
1. Start dev server: `npm run dev`
2. Navigate to `/dashboard` (should redirect to `/login`)
3. Click "Sign in with Google" or "Sign in with GitHub"
4. Complete OAuth flow
5. Verify redirect to `/dashboard`
6. Verify user data displayed

---

### ✅ Success Criteria

- [ ] OAuth login working (Google or GitHub)
- [ ] Session persists across page reloads
- [ ] Protected routes redirect to login
- [ ] User data displayed in dashboard
- [ ] No console errors

**Total Time**: 30 minutes

---

## Workflow 2: Set Up Clerk

**Time**: 7 minutes (fastest setup)

**Best For**: Rapid prototyping, pre-built UI, minimal configuration

**Prerequisites**: SAP-020 adopted

### Quick Setup Overview

**4 Steps**:
1. Create Clerk account (2 min)
2. Install dependencies (1 min)
3. Configure Clerk Provider (2 min)
4. Add authentication components (2 min)

---

### Step 1: Create Clerk Account

1. Go to https://clerk.com
2. Sign up for free account
3. Create new application
4. Copy publishable key and secret key

---

### Step 2: Install Dependencies

```bash
npm install @clerk/nextjs
```

---

### Step 3: Configure Clerk Provider

```typescript
// app/layout.tsx
import { ClerkProvider } from "@clerk/nextjs";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body>{children}</body>
      </html>
    </ClerkProvider>
  );
}
```

**Add environment variables**:
```bash
# .env.local
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...

# Optional: Customize URLs
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL=/dashboard
NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL=/dashboard
```

---

### Step 4: Add Authentication Components

**Create sign-in page**:
```typescript
// app/sign-in/[[...sign-in]]/page.tsx
import { SignIn } from "@clerk/nextjs";

export default function SignInPage() {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <SignIn />
    </div>
  );
}
```

**Create sign-up page**:
```typescript
// app/sign-up/[[...sign-up]]/page.tsx
import { SignUp } from "@clerk/nextjs";

export default function SignUpPage() {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <SignUp />
    </div>
  );
}
```

**Protected route example**:
```typescript
// app/dashboard/page.tsx
import { auth } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";

export default async function DashboardPage() {
  const { userId } = await auth();

  if (!userId) {
    redirect("/sign-in");
  }

  return <div>Dashboard (Protected)</div>;
}
```

---

### ✅ Success Criteria

- [ ] Sign-in/sign-up pages display Clerk UI
- [ ] OAuth providers working (Google, GitHub)
- [ ] Protected routes redirect to sign-in
- [ ] Session persists across reloads

**Total Time**: 7 minutes

---

## Workflow 3: Set Up Supabase Auth

**Time**: 20 minutes

**Best For**: Projects using Supabase for database, real-time features

**Prerequisites**: SAP-020 adopted, Supabase project created

### Quick Setup Overview

**6 Steps**:
1. Install dependencies (2 min)
2. Configure Supabase client (3 min)
3. Create auth helpers (5 min)
4. Add login/signup forms (5 min)
5. Configure OAuth providers (3 min)
6. Test authentication (2 min)

---

### Step 1: Install Dependencies

```bash
npm install @supabase/ssr @supabase/supabase-js
```

---

### Step 2: Configure Supabase Client

```typescript
// lib/supabase/server.ts
import { createServerClient, type CookieOptions } from "@supabase/ssr";
import { cookies } from "next/headers";

export function createClient() {
  const cookieStore = cookies();

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return cookieStore.get(name)?.value;
        },
        set(name: string, value: string, options: CookieOptions) {
          cookieStore.set({ name, value, ...options });
        },
        remove(name: string, options: CookieOptions) {
          cookieStore.set({ name, value: "", ...options });
        },
      },
    }
  );
}
```

**Client-side**:
```typescript
// lib/supabase/client.ts
import { createBrowserClient } from "@supabase/ssr";

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );
}
```

**Environment variables**:
```bash
# .env.local
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
```

---

### Step 3: Create Auth Helpers

```typescript
// app/auth/actions.ts
"use server";

import { createClient } from "@/lib/supabase/server";
import { redirect } from "next/navigation";

export async function signIn(formData: FormData) {
  const email = formData.get("email") as string;
  const password = formData.get("password") as string;

  const supabase = createClient();

  const { error } = await supabase.auth.signInWithPassword({
    email,
    password,
  });

  if (error) {
    return { error: error.message };
  }

  redirect("/dashboard");
}

export async function signUp(formData: FormData) {
  const email = formData.get("email") as string;
  const password = formData.get("password") as string;

  const supabase = createClient();

  const { error } = await supabase.auth.signUp({
    email,
    password,
  });

  if (error) {
    return { error: error.message };
  }

  redirect("/dashboard");
}

export async function signOut() {
  const supabase = createClient();
  await supabase.auth.signOut();
  redirect("/login");
}
```

---

### Step 4: Add Login/Signup Forms

```typescript
// app/login/page.tsx
import { signIn } from "@/app/auth/actions";

export default function LoginPage() {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <form action={signIn} className="w-full max-w-md space-y-4 p-8">
        <h1 className="text-2xl font-bold">Sign In</h1>

        <input
          type="email"
          name="email"
          placeholder="Email"
          required
          className="w-full px-3 py-2 border rounded"
        />

        <input
          type="password"
          name="password"
          placeholder="Password"
          required
          className="w-full px-3 py-2 border rounded"
        />

        <button
          type="submit"
          className="w-full py-2 px-4 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Sign In
        </button>
      </form>
    </div>
  );
}
```

---

### Step 5: Configure OAuth Providers

**In Supabase Dashboard**:
1. Go to Authentication → Providers
2. Enable Google OAuth
3. Add OAuth credentials (client ID, client secret)
4. Set redirect URL: `https://your-project.supabase.co/auth/v1/callback`

**In your app**:
```typescript
"use client";

import { createClient } from "@/lib/supabase/client";

export function OAuthButtons() {
  const supabase = createClient();

  async function signInWithGoogle() {
    await supabase.auth.signInWithOAuth({
      provider: "google",
      options: {
        redirectTo: `${location.origin}/auth/callback`,
      },
    });
  }

  return (
    <button onClick={signInWithGoogle}>
      Sign in with Google
    </button>
  );
}
```

---

### Step 6: Test Authentication

```typescript
// app/dashboard/page.tsx
import { createClient } from "@/lib/supabase/server";
import { redirect } from "next/navigation";

export default async function DashboardPage() {
  const supabase = createClient();

  const { data: { user } } = await supabase.auth.getUser();

  if (!user) {
    redirect("/login");
  }

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Welcome, {user.email}!</p>
    </div>
  );
}
```

---

### ✅ Success Criteria

- [ ] Email/password login working
- [ ] OAuth login working (Google)
- [ ] Protected routes redirect to login
- [ ] Session persists across reloads

**Total Time**: 20 minutes

---

## Workflow 4: Set Up Auth0

**Time**: 30 minutes

**Best For**: Enterprise SSO, SAML, compliance requirements

**Prerequisites**: SAP-020 adopted

### Quick Setup Overview

**7 Steps**:
1. Create Auth0 account (3 min)
2. Install dependencies (2 min)
3. Configure Auth0 Provider (5 min)
4. Create auth helpers (5 min)
5. Add login/logout buttons (3 min)
6. Configure callback URLs (2 min)
7. Test authentication (10 min)

---

### Step 1: Create Auth0 Account

1. Go to https://auth0.com
2. Sign up for free account
3. Create new application (Regular Web Application)
4. Copy Domain, Client ID, Client Secret

---

### Step 2: Install Dependencies

```bash
npm install @auth0/nextjs-auth0
```

---

### Step 3: Configure Auth0 Provider

```typescript
// app/api/auth/[auth0]/route.ts
import { handleAuth } from "@auth0/nextjs-auth0";

export const GET = handleAuth();
```

**Environment variables**:
```bash
# .env.local
AUTH0_SECRET=your-secret-key
AUTH0_BASE_URL=http://localhost:3000
AUTH0_ISSUER_BASE_URL=https://your-tenant.auth0.com
AUTH0_CLIENT_ID=your-client-id
AUTH0_CLIENT_SECRET=your-client-secret
```

---

### Step 4: Create Auth Helpers

```typescript
// lib/auth0.ts
import { getSession } from "@auth0/nextjs-auth0";

export async function getUser() {
  const session = await getSession();
  return session?.user;
}
```

---

### Step 5: Add Login/Logout Buttons

```typescript
// app/login/page.tsx
import Link from "next/link";

export default function LoginPage() {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <Link
        href="/api/auth/login"
        className="py-2 px-4 bg-blue-600 text-white rounded"
      >
        Sign In with Auth0
      </Link>
    </div>
  );
}
```

---

### Step 6: Configure Callback URLs

**In Auth0 Dashboard**:
1. Go to Applications → Your App → Settings
2. Add Allowed Callback URLs: `http://localhost:3000/api/auth/callback`
3. Add Allowed Logout URLs: `http://localhost:3000`
4. Save changes

---

### Step 7: Test Authentication

```typescript
// app/dashboard/page.tsx
import { getSession } from "@auth0/nextjs-auth0";
import { redirect } from "next/navigation";

export default async function DashboardPage() {
  const session = await getSession();

  if (!session) {
    redirect("/login");
  }

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Welcome, {session.user.name}!</p>
      <a href="/api/auth/logout">Logout</a>
    </div>
  );
}
```

---

### ✅ Success Criteria

- [ ] Auth0 Universal Login working
- [ ] Session persists across reloads
- [ ] Protected routes redirect to login
- [ ] Logout redirects to home page

**Total Time**: 30 minutes

---

## Provider Comparison Summary

| Provider | Time | Cost | Best Use Case |
|----------|------|------|---------------|
| **NextAuth v5** | 30 min | FREE | Self-hosted, full control |
| **Clerk** | 7 min | $25+/mo | Fastest setup, pre-built UI |
| **Supabase Auth** | 20 min | FREE (50k MAU) | Supabase projects |
| **Auth0** | 30 min | Enterprise | Enterprise SSO/SAML |

---

## Version History

**1.0.0 (2025-11-10)** - Initial providers extraction from awareness-guide.md
- Workflow 1: NextAuth v5 setup (30 min)
- Workflow 2: Clerk setup (7 min)
- Workflow 3: Supabase Auth setup (20 min)
- Workflow 4: Auth0 setup (30 min)
- Provider decision tree and comparison table
