---
sap_id: SAP-033
version: 1.0.0
status: pilot
last_updated: 2025-11-11
type: reference
audience: agents
complexity: intermediate
estimated_reading_time: 25
progressive_loading:
  phase_1: "lines 1-250"   # Quick Reference + Provider Decision
  phase_2: "lines 251-550" # Implementation Workflows
  phase_3: "full"          # Complete including security patterns
phase_1_token_estimate: 5000
phase_2_token_estimate: 11000
phase_3_token_estimate: 18000
---

# React Authentication & Authorization (SAP-033) - Agent Awareness

**SAP ID**: SAP-033
**Last Updated**: 2025-11-11
**Audience**: Generic AI Coding Agents

---

## 📖 Quick Reference

**New to SAP-033?** → Read **[README.md](README.md)** first (10-min read)

The README provides:
- 🚀 **Quick Start** - 4 authentication providers (NextAuth v5, Clerk, Supabase Auth, Auth0) with 7-30 minute setup
- 📚 **Time Savings** - 93.75% reduction (3-4 hours → 15 minutes), battle-tested security patterns
- 🎯 **Provider Decision Tree** - Self-hosted (NextAuth), rapid (Clerk), database-integrated (Supabase), enterprise (Auth0)
- 🔧 **Security Compliance** - OWASP Top 10 (8/10 coverage), SOC2 certified options, OAuth2 PKCE enforcement
- 📊 **Production Validation** - T3 Stack (NextAuth), Vercel templates, 200k+ Supabase projects, 11k+ Auth0 enterprise customers
- 🔗 **Integration** - Works with SAP-020 (Foundation), SAP-034 (Database), SAP-041 (Forms), SAP-039 (E2E Testing), SAP-035 (API Layer)

This AGENTS.md provides: Agent-specific patterns for implementing authentication and authorization in React/Next.js applications with multi-provider support.

---

## Quick Reference

### When to Use

**Use SAP-033 React Authentication when**:
- Building React apps requiring user authentication
- Need OAuth/social login (Google, GitHub, Microsoft, etc.)
- Implementing role-based access control (RBAC)
- Building multi-tenant SaaS applications
- Require enterprise SSO/SAML integration
- Need production-grade security (OWASP Top 10 compliance)

**Don't use when**:
- Building public-only content (no user accounts)
- Using headless CMS with built-in auth (Contentful, Sanity)
- Building internal tools with existing corporate SSO (use that directly)
- Static sites without dynamic content
- Mobile-only apps (consider React Native auth patterns)

### Provider Decision Matrix

| Criterion | NextAuth v5 | Clerk | Supabase Auth | Auth0 |
|-----------|-------------|-------|---------------|-------|
| **Setup Time** | 30 min | 7 min (fastest) | 20 min | 30 min |
| **Cost** | Free (self-hosted) | Free tier + $25/mo | Free tier + usage | Free tier + $35/mo |
| **OAuth Providers** | 50+ | 20+ | 10+ | 30+ |
| **Pre-built UI** | ❌ (DIY) | ✅ (best) | ✅ (good) | ✅ (enterprise) |
| **Edge Runtime** | ✅ | ✅ | ✅ | ✅ |
| **Self-Hosted** | ✅ | ❌ | ✅ (via Supabase) | ❌ |
| **Database Required** | ✅ | ❌ | ✅ (built-in) | ❌ |
| **SOC2 Certified** | N/A | ✅ | ✅ | ✅ |
| **Enterprise SSO/SAML** | ❌ | ✅ (add-on) | ❌ | ✅ |
| **Best For** | Self-hosted, flexibility | Rapid development | Supabase users | Enterprise |

**Decision Tree**:
```
Need self-hosted? → NextAuth v5
Need rapid setup (<10 min)? → Clerk
Using Supabase database? → Supabase Auth
Need enterprise SSO/SAML? → Auth0
Default choice? → NextAuth v5 (most flexible)
```

### Key Technology Versions

| Technology | Version | Why This Version |
|------------|---------|------------------|
| **NextAuth** | 5.x (beta) | Edge runtime, TypeScript-first, simpler API |
| **Clerk** | 5.x | React 19 support, improved DX |
| **Supabase** | 2.x | Native RLS, magic links, phone OTP |
| **Auth0** | 4.x | React SDK with hooks, SPA best practices |
| **React** | 19.x | Server Components, Actions API |
| **Next.js** | 15.x | App Router, middleware, edge runtime |

---

## Core Workflows

### Workflow 1: Choosing the Right Authentication Provider

**Context**: Agent needs to select authentication provider for new React project

**Decision Process**:

```typescript
// Decision logic for provider selection
const selectAuthProvider = (requirements: AuthRequirements): Provider => {
  // 1. Self-hosted requirement?
  if (requirements.selfHosted) {
    return 'NextAuth v5';
  }

  // 2. Time-critical (need auth in <10 minutes)?
  if (requirements.setupTime === 'urgent') {
    return 'Clerk'; // 7-minute setup
  }

  // 3. Already using Supabase for database?
  if (requirements.database === 'Supabase') {
    return 'Supabase Auth'; // Native RLS integration
  }

  // 4. Enterprise SSO/SAML requirement?
  if (requirements.enterpriseSSO) {
    return 'Auth0'; // Best enterprise features
  }

  // 5. Default: Flexibility and control
  return 'NextAuth v5'; // 50+ OAuth providers, open-source
};
```

**Implementation Steps**:

1. **Analyze project requirements**:
   - Budget constraints (free vs paid tiers)
   - Setup time urgency (7 min vs 30 min)
   - Self-hosted vs managed service
   - Enterprise features (SSO/SAML)
   - Existing database choice

2. **Read provider-specific setup**:
   - [NextAuth v5 Setup](./adoption-blueprint.md#path-a-nextauth-v5-setup)
   - [Clerk Setup](./adoption-blueprint.md#path-b-clerk-setup)
   - [Supabase Auth Setup](./adoption-blueprint.md#path-c-supabase-auth-setup)
   - [Auth0 Setup](./adoption-blueprint.md#path-d-auth0-setup)

3. **Verify prerequisites**:
   - SAP-020 (React Foundation) adopted → Next.js 15 project exists
   - SAP-034 (Database) adopted → Database schema ready (NextAuth/Auth0)
   - Environment variables configured

4. **Follow adoption blueprint**:
   - Install provider SDK
   - Configure OAuth providers (Google, GitHub, etc.)
   - Set up session management
   - Implement protected routes
   - Test authentication flow

---

### Workflow 2: Implementing Protected Routes (All Providers)

**Context**: Agent needs to add authentication gates to Next.js routes

**NextAuth v5 Pattern**:

```typescript
// middleware.ts (Edge runtime)
import { auth } from '@/lib/auth';
import { NextResponse } from 'next/server';

export default auth((req) => {
  const isAuthenticated = !!req.auth;
  const isAuthPage = req.nextUrl.pathname.startsWith('/login');

  if (!isAuthenticated && !isAuthPage) {
    return NextResponse.redirect(new URL('/login', req.url));
  }

  if (isAuthenticated && isAuthPage) {
    return NextResponse.redirect(new URL('/dashboard', req.url));
  }
});

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
```

**Clerk Pattern**:

```typescript
// middleware.ts (Clerk SDK)
import { authMiddleware } from '@clerk/nextjs';

export default authMiddleware({
  publicRoutes: ['/', '/about', '/contact'],
  ignoredRoutes: ['/api/webhook'],
});

export const config = {
  matcher: ['/((?!.+\\.[\\w]+$|_next).*)', '/', '/(api|trpc)(.*)'],
};
```

**Supabase Auth Pattern**:

```typescript
// middleware.ts (Supabase)
import { createMiddlewareClient } from '@supabase/auth-helpers-nextjs';
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export async function middleware(req: NextRequest) {
  const res = NextResponse.next();
  const supabase = createMiddlewareClient({ req, res });
  const { data: { session } } = await supabase.auth.getSession();

  if (!session && req.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', req.url));
  }

  return res;
}
```

**Auth0 Pattern**:

```typescript
// app/dashboard/page.tsx (Auth0 SDK)
import { withPageAuthRequired } from '@auth0/nextjs-auth0/client';

export default withPageAuthRequired(
  async function Dashboard() {
    return <div>Protected Dashboard</div>;
  },
  { returnTo: '/dashboard' }
);
```

**Agent Decision Logic**:

```typescript
// Choose pattern based on provider
const implementProtectedRoutes = (provider: Provider) => {
  switch (provider) {
    case 'NextAuth v5':
      // Use middleware.ts with auth() wrapper
      // Best for: Custom logic, multiple auth states
      return 'middleware-nextauth';

    case 'Clerk':
      // Use authMiddleware() with publicRoutes array
      // Best for: Simple public/private split
      return 'middleware-clerk';

    case 'Supabase Auth':
      // Use createMiddlewareClient() with session checks
      // Best for: RLS integration, database auth
      return 'middleware-supabase';

    case 'Auth0':
      // Use withPageAuthRequired() HOC
      // Best for: Page-level protection, simpler middleware
      return 'hoc-auth0';
  }
};
```

---

### Workflow 3: Implementing Role-Based Access Control (RBAC)

**Context**: Agent needs to restrict features by user role (admin, user, guest)

**Universal RBAC Pattern** (works with all providers):

```typescript
// lib/rbac.ts
type Role = 'admin' | 'user' | 'guest';

type Permission =
  | 'post:create'
  | 'post:edit'
  | 'post:delete'
  | 'user:manage'
  | 'settings:view';

const rolePermissions: Record<Role, Permission[]> = {
  admin: [
    'post:create', 'post:edit', 'post:delete',
    'user:manage', 'settings:view'
  ],
  user: ['post:create', 'post:edit'],
  guest: []
};

export function hasPermission(
  role: Role | undefined,
  permission: Permission
): boolean {
  if (!role) return false;
  return rolePermissions[role]?.includes(permission) ?? false;
}

// Usage in Server Components
export async function canDeletePost(userId: string, postId: string) {
  const session = await auth(); // NextAuth
  // const { userId: clerkId } = auth(); // Clerk
  // const supabase = createClient(); const { data: { user } } = await supabase.auth.getUser(); // Supabase

  if (!session?.user) return false;

  const userRole = session.user.role as Role; // From database or JWT

  return (
    hasPermission(userRole, 'post:delete') ||
    (await isPostAuthor(userId, postId))
  );
}
```

**Database Integration** (with SAP-034):

```prisma
// prisma/schema.prisma (SAP-034 integration)
model User {
  id    String @id @default(cuid())
  email String @unique
  role  Role   @default(USER)
  posts Post[]
}

enum Role {
  ADMIN
  USER
  GUEST
}

model Post {
  id       String @id @default(cuid())
  title    String
  author   User   @relation(fields: [authorId], references: [id])
  authorId String
}
```

**Server Action with RBAC**:

```typescript
// app/actions/post.ts
'use server';

import { auth } from '@/lib/auth';
import { prisma } from '@/lib/db';
import { hasPermission } from '@/lib/rbac';
import { revalidatePath } from 'next/cache';

export async function deletePost(postId: string) {
  const session = await auth();

  if (!session?.user) {
    throw new Error('Unauthorized');
  }

  const userRole = session.user.role;

  // Check permission
  if (!hasPermission(userRole, 'post:delete')) {
    throw new Error('Insufficient permissions');
  }

  // Delete post
  await prisma.post.delete({
    where: { id: postId }
  });

  revalidatePath('/posts');
}
```

---

### Workflow 4: Adding OAuth Providers

**Context**: Agent needs to add Google/GitHub/Microsoft login

**NextAuth v5**:

```typescript
// lib/auth.ts
import NextAuth from 'next-auth';
import Google from 'next-auth/providers/google';
import GitHub from 'next-auth/providers/github';

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [
    Google({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
    GitHub({
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    }),
  ],
});
```

**Clerk**:

```typescript
// Dashboard → Providers → Enable Google, GitHub (no code required)
// Clerk handles OAuth configuration automatically
```

**Supabase Auth**:

```sql
-- Dashboard → Authentication → Providers → Enable Google, GitHub
-- Add OAuth URLs:
-- Redirect URL: https://your-project.supabase.co/auth/v1/callback
-- Site URL: https://your-domain.com
```

**Auth0**:

```typescript
// Dashboard → Authentication → Social → Enable Google, GitHub
// Add callback URLs:
// Allowed Callback URLs: http://localhost:3000/api/auth/callback
// Allowed Logout URLs: http://localhost:3000
```

**Agent Decision Logic**:

```typescript
const addOAuthProvider = (provider: AuthProvider, social: 'Google' | 'GitHub') => {
  switch (provider) {
    case 'NextAuth v5':
      return {
        method: 'code',
        file: 'lib/auth.ts',
        action: 'Add provider to NextAuth config',
        envVars: [`${social.toUpperCase()}_CLIENT_ID`, `${social.toUpperCase()}_CLIENT_SECRET`]
      };

    case 'Clerk':
      return {
        method: 'dashboard',
        action: `Enable ${social} in Clerk Dashboard → Providers`,
        envVars: [] // Clerk manages OAuth credentials
      };

    case 'Supabase Auth':
      return {
        method: 'dashboard',
        action: `Enable ${social} in Supabase Dashboard → Authentication → Providers`,
        envVars: [`${social.toUpperCase()}_CLIENT_ID`, `${social.toUpperCase()}_CLIENT_SECRET`]
      };

    case 'Auth0':
      return {
        method: 'dashboard',
        action: `Enable ${social} in Auth0 Dashboard → Authentication → Social`,
        envVars: [] // Auth0 manages OAuth credentials
      };
  }
};
```

---

### Workflow 5: Session Management and Token Refresh

**Context**: Agent needs to handle session expiry and token refresh

**NextAuth v5 (JWT Strategy)**:

```typescript
// lib/auth.ts
export const { handlers, auth } = NextAuth({
  session: {
    strategy: 'jwt',
    maxAge: 30 * 24 * 60 * 60, // 30 days
  },
  callbacks: {
    async jwt({ token, user, account }) {
      if (account && user) {
        return {
          ...token,
          accessToken: account.access_token,
          refreshToken: account.refresh_token,
          accessTokenExpires: account.expires_at! * 1000,
        };
      }

      // Token still valid
      if (Date.now() < token.accessTokenExpires) {
        return token;
      }

      // Token expired, refresh it
      return refreshAccessToken(token);
    },
    async session({ session, token }) {
      session.user.id = token.sub!;
      session.accessToken = token.accessToken;
      return session;
    },
  },
});

async function refreshAccessToken(token: any) {
  try {
    const response = await fetch('https://oauth2.googleapis.com/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        client_id: process.env.GOOGLE_CLIENT_ID!,
        client_secret: process.env.GOOGLE_CLIENT_SECRET!,
        grant_type: 'refresh_token',
        refresh_token: token.refreshToken,
      }),
    });

    const refreshedTokens = await response.json();

    return {
      ...token,
      accessToken: refreshedTokens.access_token,
      accessTokenExpires: Date.now() + refreshedTokens.expires_in * 1000,
      refreshToken: refreshedTokens.refresh_token ?? token.refreshToken,
    };
  } catch (error) {
    return {
      ...token,
      error: 'RefreshAccessTokenError',
    };
  }
}
```

**Clerk (Automatic)**:

```typescript
// Clerk handles token refresh automatically
// No custom code needed
// Sessions expire after 7 days of inactivity (configurable)
```

**Supabase Auth**:

```typescript
// lib/supabase/client.ts
import { createBrowserClient } from '@supabase/ssr';

export const createClient = () => {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      auth: {
        persistSession: true,
        autoRefreshToken: true, // Automatic token refresh
        detectSessionInUrl: true,
      },
    }
  );
};
```

**Auth0**:

```typescript
// lib/auth0.ts
import { initAuth0 } from '@auth0/nextjs-auth0';

export default initAuth0({
  secret: process.env.AUTH0_SECRET!,
  issuerBaseURL: process.env.AUTH0_ISSUER_BASE_URL!,
  baseURL: process.env.AUTH0_BASE_URL!,
  clientID: process.env.AUTH0_CLIENT_ID!,
  clientSecret: process.env.AUTH0_CLIENT_SECRET!,
  session: {
    rollingDuration: 60 * 60 * 24 * 7, // 7 days
    absoluteDuration: 60 * 60 * 24 * 30, // 30 days
    autoSave: true,
  },
});
```

---

## Integration with Other SAPs

### SAP-020: React Project Foundation (REQUIRED)

**Why Required**: Next.js 15 App Router provides:
- Server Components for secure server-side session checks
- Server Actions for authentication mutations
- Middleware for route protection
- Edge runtime for global authentication

**Integration Points**:
1. **Middleware**: All providers use Next.js middleware for route protection
2. **Server Components**: Session checks in `async` server components
3. **Server Actions**: Login/logout/signup mutations via `'use server'`
4. **Environment Variables**: `.env.local` for OAuth credentials

**Setup Order**: SAP-020 → SAP-033

---

### SAP-034: Database Integration (CONDITIONAL)

**Why Conditional**: Required for NextAuth v5 and Auth0 (user/session storage), optional for Clerk/Supabase (managed)

**Integration Points**:
1. **User Model**: Store user profiles, roles, metadata
2. **Session Model**: Store active sessions (NextAuth database strategy)
3. **Account Model**: Link OAuth provider accounts to users
4. **RBAC**: Store user roles and permissions

**Example Schema** (NextAuth + Prisma):

```prisma
model User {
  id       String    @id @default(cuid())
  email    String    @unique
  name     String?
  role     Role      @default(USER)
  accounts Account[]
  sessions Session[]
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
  user              User    @relation(fields: [userId], references: [id])

  @@unique([provider, providerAccountId])
}

model Session {
  id           String   @id @default(cuid())
  sessionToken String   @unique
  userId       String
  expires      DateTime
  user         User     @relation(fields: [userId], references: [id])
}

enum Role {
  ADMIN
  USER
  GUEST
}
```

---

### SAP-041: Form Validation (RECOMMENDED)

**Why Recommended**: Login/signup forms need client and server validation

**Integration Points**:
1. **Login Forms**: Email/password validation before submission
2. **Signup Forms**: Password strength, email format, required fields
3. **Server Actions**: Validate form data before authentication calls
4. **Error Handling**: Display validation errors to users

**Example** (NextAuth + Zod):

```typescript
// app/actions/auth.ts
'use server';

import { z } from 'zod';
import { signIn } from '@/lib/auth';

const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

export async function login(formData: FormData) {
  const parsed = loginSchema.safeParse({
    email: formData.get('email'),
    password: formData.get('password'),
  });

  if (!parsed.success) {
    return { error: parsed.error.flatten() };
  }

  await signIn('credentials', {
    email: parsed.data.email,
    password: parsed.data.password,
    redirectTo: '/dashboard',
  });
}
```

---

### SAP-039: E2E Testing (RECOMMENDED)

**Why Recommended**: Authentication flows are critical and should be E2E tested

**Integration Points**:
1. **Login Flow**: Test OAuth and credentials login
2. **Protected Routes**: Verify unauthenticated redirects
3. **Session Persistence**: Test session across page reloads
4. **Logout Flow**: Verify session cleanup

**Example** (Playwright + NextAuth):

```typescript
// tests/auth.spec.ts
import { test, expect } from '@playwright/test';

test('login flow', async ({ page }) => {
  // Navigate to login
  await page.goto('/login');

  // Fill credentials
  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'password123');

  // Submit form
  await page.click('[type="submit"]');

  // Verify redirect to dashboard
  await expect(page).toHaveURL('/dashboard');

  // Verify user is authenticated
  await expect(page.locator('text=Logout')).toBeVisible();
});

test('protected route redirect', async ({ page }) => {
  // Navigate to protected route while logged out
  await page.goto('/dashboard');

  // Verify redirect to login
  await expect(page).toHaveURL('/login');
});
```

---

## Security Best Practices

### 1. Environment Variables

**Never commit sensitive credentials**:

```bash
# .env.local (gitignored)
# NextAuth v5
NEXTAUTH_SECRET="your-secret-here"
NEXTAUTH_URL="http://localhost:3000"
GOOGLE_CLIENT_ID="your-google-client-id"
GOOGLE_CLIENT_SECRET="your-google-client-secret"

# Clerk
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY="pk_test_..."
CLERK_SECRET_KEY="sk_test_..."

# Supabase Auth
NEXT_PUBLIC_SUPABASE_URL="https://your-project.supabase.co"
NEXT_PUBLIC_SUPABASE_ANON_KEY="your-anon-key"

# Auth0
AUTH0_SECRET="your-auth0-secret"
AUTH0_BASE_URL="http://localhost:3000"
AUTH0_ISSUER_BASE_URL="https://your-domain.auth0.com"
AUTH0_CLIENT_ID="your-auth0-client-id"
AUTH0_CLIENT_SECRET="your-auth0-client-secret"
```

**Production secrets**:
- Use Vercel/Netlify environment variables UI
- Never log secrets in server logs
- Rotate secrets regularly (every 90 days)

---

### 2. OWASP Top 10 Compliance

| OWASP Risk | Mitigation (SAP-033) |
|------------|---------------------|
| **A01: Broken Access Control** | RBAC patterns, middleware route protection |
| **A02: Cryptographic Failures** | HTTPS only, HTTP-only cookies, PKCE enforcement |
| **A03: Injection** | Parameterized queries (via SAP-034), input validation (SAP-041) |
| **A04: Insecure Design** | Battle-tested providers, security-first architecture |
| **A05: Security Misconfiguration** | Default secure settings, environment variable validation |
| **A07: Identification Failures** | MFA support, rate limiting (provider-managed) |
| **A08: Software/Data Integrity** | Signed JWTs, token verification |

---

### 3. Session Security

**HTTP-only Cookies** (recommended):

```typescript
// NextAuth v5
export const { handlers, auth } = NextAuth({
  cookies: {
    sessionToken: {
      name: '__Secure-next-auth.session-token',
      options: {
        httpOnly: true,
        sameSite: 'lax',
        path: '/',
        secure: process.env.NODE_ENV === 'production',
      },
    },
  },
});
```

**Avoid localStorage** for tokens (XSS vulnerability):

```typescript
// ❌ BAD: localStorage vulnerable to XSS
localStorage.setItem('token', accessToken);

// ✅ GOOD: HTTP-only cookies prevent JavaScript access
// Handled automatically by all providers
```

---

### 4. CSRF Protection

**NextAuth v5**:

```typescript
// CSRF protection enabled by default via session cookies
// No additional configuration needed
```

**Clerk**:

```typescript
// CSRF protection handled by Clerk SDK
// Uses secure session tokens
```

**Supabase Auth**:

```typescript
// CSRF protection via PKCE flow
// Enabled by default in createClient()
```

**Auth0**:

```typescript
// CSRF protection via state parameter
// Handled automatically by @auth0/nextjs-auth0
```

---

## Common Pitfalls

### Pitfall 1: Missing Environment Variables

**Symptom**:
```
Error: NEXTAUTH_SECRET is not set
Error: Missing Clerk publishable key
```

**Fix**:
1. Create `.env.local` in project root
2. Add all required environment variables
3. Restart Next.js dev server (`npm run dev`)
4. Verify `.env.local` is gitignored

---

### Pitfall 2: Middleware Not Configured

**Symptom**: Protected routes accessible without authentication

**Fix**:

```typescript
// middleware.ts MUST be in project root
export default auth((req) => {
  // Auth logic here
});

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
```

---

### Pitfall 3: Database Schema Out of Sync (NextAuth)

**Symptom**:
```
Prisma Client Error: Table 'User' not found
```

**Fix**:

```bash
# Generate Prisma schema for NextAuth
npx prisma migrate dev --name add_auth_models
npx prisma generate
npm run dev
```

---

### Pitfall 4: OAuth Redirect URI Mismatch

**Symptom**:
```
Error: redirect_uri_mismatch
```

**Fix**:
1. **NextAuth v5**: Add `NEXTAUTH_URL=http://localhost:3000` to `.env.local`
2. **Clerk**: Add `http://localhost:3000` to Clerk Dashboard → Allowed Origins
3. **Supabase**: Add `http://localhost:3000` to Supabase Dashboard → Site URL
4. **Auth0**: Add `http://localhost:3000/api/auth/callback` to Allowed Callback URLs

---

### Pitfall 5: Session Not Persisting Across Requests

**Symptom**: User logged out on page reload

**Fix**:

```typescript
// Ensure cookies are properly configured
// NextAuth v5
export const { handlers, auth } = NextAuth({
  cookies: {
    sessionToken: {
      name: '__Secure-next-auth.session-token',
      options: {
        httpOnly: true,
        sameSite: 'lax',
        path: '/',
        secure: process.env.NODE_ENV === 'production',
      },
    },
  },
});
```

---

## Learn More

### Documentation

- **[Protocol Spec](protocol-spec.md)** - Complete API reference for all 4 providers (45-min read)
- **[Awareness Guide](awareness-guide.md)** - Practical how-to workflows and decision trees (30-min read)
- **[Adoption Blueprint](adoption-blueprint.md)** - Step-by-step setup guide for each provider (25-min tutorial)
- **[Capability Charter](capability-charter.md)** - Problem statement and solution design (15-min read)
- **[Ledger](ledger.md)** - Adoption tracking and production case studies (10-min read)

### External Resources

- **NextAuth.js v5**: [Official Docs](https://authjs.dev) | [Next.js Guide](https://authjs.dev/getting-started/installation?framework=next.js)
- **Clerk**: [Official Docs](https://clerk.com/docs) | [Next.js Quickstart](https://clerk.com/docs/quickstarts/nextjs)
- **Supabase Auth**: [Official Docs](https://supabase.com/docs/guides/auth) | [Next.js Guide](https://supabase.com/docs/guides/auth/server-side/nextjs)
- **Auth0**: [Official Docs](https://auth0.com/docs) | [Next.js SDK](https://github.com/auth0/nextjs-auth0)

### Related SAPs

- **[SAP-020 (React Foundation)](../react-foundation/)** - Next.js 15 baseline (required prerequisite)
- **[SAP-034 (Database Integration)](../react-database-integration/)** - User storage for NextAuth/Auth0
- **[SAP-041 (Form Validation)](../react-form-validation/)** - Login/signup form validation

---

## Version History

- **1.0.0** (2025-11-09): Initial release
  - Multi-provider support (NextAuth v5, Clerk, Supabase Auth, Auth0)
  - Decision framework for provider selection
  - RBAC patterns and security best practices
  - 93.75% time savings validation (3-4 hours → 15 minutes)

---

**Quick Links**:
- 🚀 [Provider Decision Matrix](#provider-decision-matrix) - Choose your auth provider
- 🔧 [Protected Routes](#workflow-2-implementing-protected-routes-all-providers) - Add authentication gates
- 🎯 [RBAC Implementation](#workflow-3-implementing-role-based-access-control-rbac) - Role-based access
- 🔗 [Integration with SAP-034](#sap-034-database-integration-conditional) - Database patterns
- 🛡️ [Security Best Practices](#security-best-practices) - OWASP Top 10 compliance
