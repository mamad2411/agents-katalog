# SAP-033: React Authentication - Advanced Workflows

**SAP**: SAP-033 (react-authentication)
**Domain**: Workflows
**Version**: 1.0.0
**Last Updated**: 2025-11-10

---

## Overview

This file contains **4 advanced authentication workflows** for Next.js 15+ projects:

1. **Implement RBAC** (20 min) - Role-based access control
2. **Add Protected Routes** (15 min) - Middleware + component-level protection
3. **Add Magic Link Authentication** (25 min) - Passwordless email login
4. **Add OAuth Providers** (10 min/provider) - Social login integration

**For provider setup** (NextAuth, Clerk, Supabase, Auth0), see [../providers/AGENTS.md](../providers/AGENTS.md)

**For security patterns**, see [../security/AGENTS.md](../security/AGENTS.md)

**For troubleshooting**, see [../troubleshooting/AGENTS.md](../troubleshooting/AGENTS.md)

---

## Workflow 5: Implement RBAC

**Time**: 20 minutes

**Best For**: Multi-tenant apps, admin dashboards, complex permissions

**Prerequisites**: Authentication provider configured (any from providers/)

### Quick Setup Overview

**5 Steps**:
1. Define roles in database (5 min)
2. Add role to session (5 min)
3. Create authorization middleware (5 min)
4. Add role-based UI components (3 min)
5. Test role enforcement (2 min)

---

### Step 1: Define Roles in Database

**Prisma schema** (NextAuth):
```prisma
model User {
  id    String @id @default(cuid())
  email String @unique
  role  Role   @default(USER)
  // ... other fields
}

enum Role {
  USER
  ADMIN
  MODERATOR
}
```

**Run migration**:
```bash
npx prisma migrate dev --name add-user-roles
npx prisma generate
```

---

### Step 2: Add Role to Session

**NextAuth**:
```typescript
// auth.ts
import NextAuth from "next-auth";

export const { handlers, signIn, signOut, auth } = NextAuth({
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.role = user.role; // Add role to token
      }
      return token;
    },

    async session({ session, token }) {
      if (token) {
        session.user.role = token.role as string;
      }
      return session;
    }
  }
});
```

**Clerk**:
```typescript
// Clerk automatically adds org roles to session
// Access via: session.user.publicMetadata.role
```

**Supabase**:
```typescript
// Add role to user metadata
const { data, error } = await supabase.auth.admin.updateUserById(
  userId,
  { user_metadata: { role: "admin" } }
);
```

---

### Step 3: Create Authorization Middleware

**NextAuth RBAC middleware**:
```typescript
// middleware.ts
import { auth } from "@/auth";
import { NextResponse } from "next/server";

const roleRoutes = {
  admin: ["/admin"],
  moderator: ["/admin", "/moderate"],
  user: ["/dashboard"]
};

export default auth((req) => {
  const { pathname } = req.nextUrl;
  const session = req.auth;

  if (!session) {
    return NextResponse.redirect(new URL("/login", req.url));
  }

  const userRole = session.user.role as keyof typeof roleRoutes;
  const allowedRoutes = roleRoutes[userRole] || [];

  const hasAccess = allowedRoutes.some(route =>
    pathname.startsWith(route)
  );

  if (!hasAccess && pathname.startsWith("/admin") || pathname.startsWith("/moderate")) {
    return NextResponse.redirect(new URL("/unauthorized", req.url));
  }

  return NextResponse.next();
});
```

---

### Step 4: Add Role-Based UI Components

**Show/hide based on role**:
```typescript
// components/RoleGate.tsx
import { auth } from "@/auth";

export async function RoleGate({
  children,
  allowedRoles
}: {
  children: React.ReactNode;
  allowedRoles: string[];
}) {
  const session = await auth();

  if (!session || !allowedRoles.includes(session.user.role)) {
    return null;
  }

  return <>{children}</>;
}
```

**Usage**:
```typescript
// app/dashboard/page.tsx
import { RoleGate } from "@/components/RoleGate";

export default function DashboardPage() {
  return (
    <div>
      <h1>Dashboard</h1>

      <RoleGate allowedRoles={["admin"]}>
        <button>Admin Only Action</button>
      </RoleGate>

      <RoleGate allowedRoles={["admin", "moderator"]}>
        <button>Admin or Moderator Action</button>
      </RoleGate>
    </div>
  );
}
```

---

### Step 5: Test Role Enforcement

**Test cases**:
1. User with role="user" cannot access `/admin` (403 or redirect)
2. User with role="admin" can access `/admin`
3. UI elements hidden for unauthorized roles
4. Role persists across page reloads

---

### ✅ Success Criteria

- [ ] Roles defined in database
- [ ] Role available in session
- [ ] Middleware enforces role-based access
- [ ] UI components conditionally render based on role
- [ ] Unauthorized access redirects to error page

**Total Time**: 20 minutes

---

## Workflow 6: Add Protected Routes

**Time**: 15 minutes

**Best For**: Protecting specific pages or layouts

**Prerequisites**: Authentication provider configured

### Quick Setup Overview

**3 Approaches**:
1. Middleware (global protection) - 5 min
2. Server Component (page-level protection) - 5 min
3. Client Component (component-level protection) - 5 min

---

### Approach 1: Middleware (Global Protection)

**Recommended for**: Protecting entire sections (e.g., all `/dashboard/*` routes)

```typescript
// middleware.ts
import { auth } from "@/auth";
import { NextResponse } from "next/server";

export default auth((req) => {
  const { pathname } = req.nextUrl;
  const isAuthenticated = !!req.auth;

  // Define protected routes
  const protectedRoutes = ["/dashboard", "/profile", "/settings"];
  const isProtectedRoute = protectedRoutes.some(route =>
    pathname.startsWith(route)
  );

  if (isProtectedRoute && !isAuthenticated) {
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

---

### Approach 2: Server Component (Page-Level Protection)

**Recommended for**: Protecting individual pages with custom logic

```typescript
// app/dashboard/page.tsx
import { auth } from "@/auth";
import { redirect } from "next/navigation";

export default async function DashboardPage() {
  const session = await auth();

  // Protect page
  if (!session) {
    redirect("/login?callbackUrl=/dashboard");
  }

  // Optional: Role-based protection
  if (session.user.role !== "admin") {
    redirect("/unauthorized");
  }

  return <div>Dashboard (Protected)</div>;
}
```

---

### Approach 3: Client Component (Component-Level Protection)

**Recommended for**: Protecting specific UI elements

```typescript
// components/ProtectedContent.tsx
"use client";

import { useSession } from "next-auth/react";
import { redirect } from "next/navigation";

export function ProtectedContent({ children }: { children: React.ReactNode }) {
  const { data: session, status } = useSession();

  if (status === "loading") {
    return <div>Loading...</div>;
  }

  if (status === "unauthenticated") {
    redirect("/login");
  }

  return <>{children}</>;
}
```

**Usage**:
```typescript
// app/profile/page.tsx
import { ProtectedContent } from "@/components/ProtectedContent";

export default function ProfilePage() {
  return (
    <ProtectedContent>
      <h1>Profile (Protected)</h1>
      {/* Protected content */}
    </ProtectedContent>
  );
}
```

---

### ✅ Success Criteria

- [ ] Protected routes redirect unauthenticated users to login
- [ ] Callback URL preserves original destination
- [ ] Authentication state persists across reloads
- [ ] Loading states handled gracefully

**Total Time**: 15 minutes

---

## Workflow 7: Add Magic Link Authentication

**Time**: 25 minutes

**Best For**: Passwordless authentication, improved UX

**Prerequisites**: NextAuth v5 or Supabase Auth configured

### Quick Setup Overview

**6 Steps**:
1. Configure email provider (5 min)
2. Add magic link provider to auth config (5 min)
3. Create magic link login form (5 min)
4. Configure email templates (5 min)
5. Test magic link flow (3 min)
6. Handle edge cases (2 min)

---

### Step 1: Configure Email Provider

**Using Resend** (recommended):
```bash
npm install resend
```

```bash
# .env.local
RESEND_API_KEY=your-resend-api-key
EMAIL_FROM=noreply@yourdomain.com
```

---

### Step 2: Add Magic Link Provider

**NextAuth v5**:
```typescript
// auth.ts
import NextAuth from "next-auth";
import Resend from "next-auth/providers/resend";

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    Resend({
      apiKey: process.env.RESEND_API_KEY!,
      from: process.env.EMAIL_FROM!
    })
  ],

  pages: {
    verifyRequest: "/verify-request",
  }
});
```

**Supabase Auth**:
```typescript
// Already built-in, just enable in Supabase dashboard
// Authentication → Email Auth → Enable Magic Link
```

---

### Step 3: Create Magic Link Login Form

```typescript
// app/login/page.tsx
"use client";

import { signIn } from "next-auth/react";
import { useState } from "react";

export default function MagicLinkLogin() {
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    await signIn("resend", {
      email,
      redirect: false
    });

    setSubmitted(true);
  }

  if (submitted) {
    return (
      <div className="text-center">
        <h2>Check your email</h2>
        <p>We sent a magic link to {email}</p>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <h1>Sign in with magic link</h1>

      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="you@example.com"
        required
        className="w-full px-3 py-2 border rounded"
      />

      <button
        type="submit"
        className="w-full py-2 px-4 bg-blue-600 text-white rounded"
      >
        Send magic link
      </button>
    </form>
  );
}
```

---

### Step 4: Configure Email Templates

**Custom email template** (NextAuth):
```typescript
// auth.ts
export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    Resend({
      apiKey: process.env.RESEND_API_KEY!,
      from: process.env.EMAIL_FROM!,
      sendVerificationRequest: async ({ identifier, url, provider }) => {
        const { host } = new URL(url);

        await fetch("https://api.resend.com/emails", {
          method: "POST",
          headers: {
            Authorization: `Bearer ${provider.apiKey}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            from: provider.from,
            to: identifier,
            subject: `Sign in to ${host}`,
            html: `
              <h1>Sign in to ${host}</h1>
              <p>Click the button below to sign in:</p>
              <a href="${url}" style="background: #0070f3; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                Sign in
              </a>
              <p>If you didn't request this email, you can safely ignore it.</p>
            `,
          }),
        });
      },
    })
  ]
});
```

---

### Step 5: Test Magic Link Flow

**Test steps**:
1. Enter email in login form
2. Check email inbox (and spam folder)
3. Click magic link in email
4. Verify redirect to dashboard
5. Verify session persists

---

### Step 6: Handle Edge Cases

**Expired links**:
```typescript
// auth.ts
export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    Resend({
      maxAge: 5 * 60, // 5 minutes (default: 24 hours)
    })
  ]
});
```

**Rate limiting** (prevent spam):
```typescript
// app/api/auth/magic-link/route.ts
import { Ratelimit } from "@upstash/ratelimit";
import { Redis } from "@upstash/redis";

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(3, "1 h"), // 3 requests per hour
});

export async function POST(req: Request) {
  const { email } = await req.json();

  const { success } = await ratelimit.limit(email);

  if (!success) {
    return new Response("Too many requests", { status: 429 });
  }

  // Send magic link...
}
```

---

### ✅ Success Criteria

- [ ] Magic link email sent successfully
- [ ] Magic link redirects to dashboard
- [ ] Magic link expires after configured time
- [ ] Rate limiting prevents spam
- [ ] Email template branded correctly

**Total Time**: 25 minutes

---

## Workflow 8: Add OAuth Providers

**Time**: 10 minutes per provider

**Best For**: Social login (Google, GitHub, Facebook, etc.)

**Prerequisites**: Authentication provider configured

### Quick Setup Overview

**4 Steps**:
1. Register OAuth app with provider (5 min)
2. Add provider to auth config (2 min)
3. Add OAuth button to UI (2 min)
4. Test OAuth flow (1 min)

---

### Step 1: Register OAuth App

**Google**:
1. Go to https://console.cloud.google.com
2. Create new project (or select existing)
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URI: `http://localhost:3000/api/auth/callback/google`
6. Copy Client ID and Client Secret

**GitHub**:
1. Go to https://github.com/settings/developers
2. New OAuth App
3. Add callback URL: `http://localhost:3000/api/auth/callback/github`
4. Copy Client ID and Client Secret

---

### Step 2: Add Provider to Auth Config

**NextAuth v5**:
```typescript
// auth.ts
import NextAuth from "next-auth";
import Google from "next-auth/providers/google";
import GitHub from "next-auth/providers/github";
import Facebook from "next-auth/providers/facebook";

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!
    }),

    GitHub({
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!
    }),

    Facebook({
      clientId: process.env.FACEBOOK_CLIENT_ID!,
      clientSecret: process.env.FACEBOOK_CLIENT_SECRET!
    })
  ]
});
```

**Clerk**: Configure in Clerk Dashboard (no code changes needed)

**Supabase**: Configure in Supabase Dashboard → Authentication → Providers

---

### Step 3: Add OAuth Button to UI

```typescript
// components/OAuthButtons.tsx
"use client";

import { signIn } from "next-auth/react";

export function OAuthButtons() {
  return (
    <div className="space-y-2">
      <button
        onClick={() => signIn("google", { callbackUrl: "/dashboard" })}
        className="w-full py-2 px-4 bg-white border border-gray-300 rounded"
      >
        Sign in with Google
      </button>

      <button
        onClick={() => signIn("github", { callbackUrl: "/dashboard" })}
        className="w-full py-2 px-4 bg-gray-900 text-white rounded"
      >
        Sign in with GitHub
      </button>

      <button
        onClick={() => signIn("facebook", { callbackUrl: "/dashboard" })}
        className="w-full py-2 px-4 bg-blue-600 text-white rounded"
      >
        Sign in with Facebook
      </button>
    </div>
  );
}
```

---

### Step 4: Test OAuth Flow

**Test steps**:
1. Click OAuth button
2. Redirect to provider login
3. Authorize application
4. Redirect back to app (callback URL)
5. Verify session created
6. Verify user data stored in database

---

### ✅ Success Criteria

- [ ] OAuth button redirects to provider
- [ ] User can authorize application
- [ ] Callback redirects to dashboard
- [ ] Session persists across reloads
- [ ] User data saved to database

**Total Time**: 10 minutes per provider

---

## Version History

**1.0.0 (2025-11-10)** - Initial workflows extraction from awareness-guide.md
- Workflow 5: Implement RBAC (20 min)
- Workflow 6: Add Protected Routes (15 min)
- Workflow 7: Add Magic Link Authentication (25 min)
- Workflow 8: Add OAuth Providers (10 min/provider)
