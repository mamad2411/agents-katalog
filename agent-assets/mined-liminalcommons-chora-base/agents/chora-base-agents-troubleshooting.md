# SAP-033: React Authentication - Troubleshooting

**SAP**: SAP-033 (react-authentication)
**Domain**: Troubleshooting
**Version**: 1.0.0
**Last Updated**: 2025-11-10

---

## Overview

This file contains **common authentication issues and fixes** for Next.js 15+ projects.

**8 Common Issues**:
1. Session not persisting
2. OAuth callback errors
3. Middleware redirect loops
4. CSRF token mismatch
5. Database connection errors
6. Session expired unexpectedly
7. Cannot read user data in components
8. Callback URL not working

**For provider setup**, see [../providers/AGENTS.md](../providers/AGENTS.md)

**For workflows**, see [../workflows/AGENTS.md](../workflows/AGENTS.md)

**For security**, see [../security/AGENTS.md](../security/AGENTS.md)

---

## Issue 1: Session Not Persisting

**Symptom**: User signs in successfully but session lost on page reload

**Cause**: Missing or incorrect session configuration

**Fix for NextAuth v5**:

```typescript
// auth.ts
export const { handlers, signIn, signOut, auth } = NextAuth({
  session: {
    strategy: "jwt", // ✅ Use JWT for stateless sessions
    maxAge: 30 * 24 * 60 * 60 // 30 days
  },

  cookies: {
    sessionToken: {
      name: `__Secure-next-auth.session-token`,
      options: {
        httpOnly: true,
        sameSite: "lax",
        path: "/",
        secure: process.env.NODE_ENV === "production"
      }
    }
  }
});
```

**Check environment variables**:
```bash
# .env.local
NEXTAUTH_URL=http://localhost:3000  # ✅ Must match actual URL
NEXTAUTH_SECRET=your-secret-key-here  # ✅ Must be set
```

**Generate NEXTAUTH_SECRET**:
```bash
openssl rand -base64 32
```

---

## Issue 2: OAuth Callback Errors

**Symptom**: `redirect_uri_mismatch` or `invalid_client` error

**Cause**: Callback URL not configured in OAuth provider

**Fix**:

**Google OAuth**:
1. Go to https://console.cloud.google.com
2. Select project → Credentials → OAuth 2.0 Client IDs
3. Add authorized redirect URI: `http://localhost:3000/api/auth/callback/google`
4. For production: `https://yourdomain.com/api/auth/callback/google`

**GitHub OAuth**:
1. Go to https://github.com/settings/developers
2. Select OAuth App
3. Add callback URL: `http://localhost:3000/api/auth/callback/github`

**Callback URL format** (NextAuth v5):
```
{NEXTAUTH_URL}/api/auth/callback/{provider}

Examples:
- http://localhost:3000/api/auth/callback/google
- http://localhost:3000/api/auth/callback/github
- https://app.example.com/api/auth/callback/google
```

---

## Issue 3: Middleware Redirect Loops

**Symptom**: Browser shows "Too many redirects" error

**Cause**: Middleware redirects to login, login page redirects back to middleware

**Fix**:

```typescript
// middleware.ts
import { auth } from "@/auth";
import { NextResponse } from "next/server";

export default auth((req) => {
  const { pathname } = req.nextUrl;
  const isAuthenticated = !!req.auth;

  // ✅ Define public routes BEFORE checking authentication
  const publicRoutes = [
    "/",
    "/login",
    "/signup",
    "/api/auth", // ✅ CRITICAL: Allow auth API routes
  ];

  const isPublicRoute = publicRoutes.some(route =>
    pathname.startsWith(route)
  );

  // ✅ Allow public routes without authentication
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

// ✅ Configure matcher to exclude static files
export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
};
```

---

## Issue 4: CSRF Token Mismatch

**Symptom**: "CSRF token validation failed" error

**Cause**: Missing or incorrect CSRF token

**Fix for NextAuth v5**:

```typescript
// NextAuth v5 handles CSRF automatically
// Ensure cookies are set correctly

// auth.ts
export const { handlers, signIn, signOut, auth } = NextAuth({
  cookies: {
    csrfToken: {
      name: "__Host-next-auth.csrf-token",
      options: {
        httpOnly: true,
        sameSite: "lax",
        path: "/",
        secure: process.env.NODE_ENV === "production"
      }
    }
  }
});
```

**Check cookie settings**:
- `sameSite: "lax"` or `"strict"` (NOT `"none"` unless cross-domain)
- `secure: true` in production (HTTPS required)
- `httpOnly: true` always

---

## Issue 5: Database Connection Errors

**Symptom**: "Can't reach database server" or connection timeout

**Cause**: Incorrect database URL or database not running

**Fix**:

**Check DATABASE_URL**:
```bash
# .env.local
DATABASE_URL="postgresql://user:password@localhost:5432/dbname"
```

**Test connection**:
```bash
npx prisma db pull  # Test Prisma connection
```

**Check database is running**:
```bash
# PostgreSQL
pg_isready -h localhost -p 5432

# MySQL
mysql -h localhost -P 3306 -u root -p

# Check Docker containers
docker ps
```

**Connection pooling** (for serverless):
```typescript
// lib/prisma.ts
import { PrismaClient } from "@prisma/client";

const globalForPrisma = global as unknown as { prisma: PrismaClient };

export const prisma =
  globalForPrisma.prisma ||
  new PrismaClient({
    log: ["query"],
  });

if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = prisma;
```

---

## Issue 6: Session Expired Unexpectedly

**Symptom**: User logged out after short time (< configured maxAge)

**Cause**: Session maxAge too short or JWT expiration mismatch

**Fix**:

```typescript
// auth.ts
export const { handlers, signIn, signOut, auth } = NextAuth({
  session: {
    strategy: "jwt",
    maxAge: 30 * 24 * 60 * 60, // ✅ 30 days
    updateAge: 24 * 60 * 60, // ✅ Update every 24 hours
  },

  jwt: {
    maxAge: 30 * 24 * 60 * 60, // ✅ Must match session maxAge
  }
});
```

**Check clock sync**:
- JWT expiration uses server time
- Ensure server clock is synchronized (NTP)

---

## Issue 7: Cannot Read User Data in Components

**Symptom**: `session.user.id` is `undefined` or missing custom fields

**Cause**: Custom fields not added to session callback

**Fix for NextAuth v5**:

```typescript
// auth.ts
export const { handlers, signIn, signOut, auth } = NextAuth({
  callbacks: {
    async jwt({ token, user }) {
      // ✅ Add custom fields to JWT
      if (user) {
        token.userId = user.id;
        token.role = user.role;
      }
      return token;
    },

    async session({ session, token }) {
      // ✅ Add custom fields to session
      if (token) {
        session.user.id = token.userId as string;
        session.user.role = token.role as string;
      }
      return session;
    }
  }
});
```

**TypeScript types** (optional but recommended):
```typescript
// types/next-auth.d.ts
import { DefaultSession } from "next-auth";

declare module "next-auth" {
  interface Session {
    user: {
      id: string;
      role: string;
    } & DefaultSession["user"];
  }

  interface User {
    role: string;
  }
}

declare module "next-auth/jwt" {
  interface JWT {
    userId: string;
    role: string;
  }
}
```

---

## Issue 8: Callback URL Not Working

**Symptom**: After login, user redirected to wrong page

**Cause**: Callback URL not preserved or configured incorrectly

**Fix**:

**Preserve callback URL in middleware**:
```typescript
// middleware.ts
if (!isAuthenticated) {
  const loginUrl = new URL("/login", req.url);
  loginUrl.searchParams.set("callbackUrl", pathname); // ✅ Preserve original URL
  return NextResponse.redirect(loginUrl);
}
```

**Use callback URL in login**:
```typescript
// app/login/page.tsx
"use client";

import { signIn } from "next-auth/react";
import { useSearchParams } from "next/navigation";

export default function LoginPage() {
  const searchParams = useSearchParams();
  const callbackUrl = searchParams.get("callbackUrl") || "/dashboard";

  return (
    <button onClick={() => signIn("google", { callbackUrl })}>
      Sign in with Google
    </button>
  );
}
```

**Server-side redirect** (Server Actions):
```typescript
"use server";

import { signIn } from "@/auth";
import { redirect } from "next/navigation";

export async function login(callbackUrl: string) {
  await signIn();
  redirect(callbackUrl || "/dashboard");
}
```

---

## Quick Diagnostics

### Check NextAuth v5 Configuration

```bash
# 1. Verify environment variables
cat .env.local | grep NEXTAUTH

# 2. Check auth.ts exports
grep "export const" auth.ts

# 3. Test API route
curl http://localhost:3000/api/auth/providers

# 4. Check middleware
grep "export default auth" middleware.ts
```

---

### Check Database Schema

```bash
# Prisma
npx prisma validate
npx prisma format
npx prisma db pull

# Check migrations
npx prisma migrate status
```

---

### Check Session in Browser

**Console**:
```javascript
// Check cookies
document.cookie

// Check session (NextAuth v5)
fetch("/api/auth/session").then(r => r.json()).then(console.log)
```

**Network tab**:
- Check `/api/auth/session` response
- Check `/api/auth/callback/*` redirects
- Verify cookies are set

---

## Error Messages Reference

| Error Message | Cause | Fix |
|---------------|-------|-----|
| `redirect_uri_mismatch` | OAuth callback URL not configured | Add callback URL to OAuth provider |
| `CSRF token mismatch` | Cookie settings incorrect | Check `sameSite`, `secure`, `httpOnly` |
| `Can't reach database` | Database URL incorrect or DB not running | Check `DATABASE_URL`, test connection |
| `Session not found` | Session expired or not created | Check `maxAge`, verify login success |
| `Invalid session token` | JWT secret changed or token corrupted | Regenerate `NEXTAUTH_SECRET`, clear cookies |
| `Too many redirects` | Middleware redirect loop | Exclude public routes from middleware |

---

## Version History

**1.0.0 (2025-11-10)** - Initial troubleshooting extraction from awareness-guide.md
- 8 common authentication issues and fixes
- Quick diagnostics commands
- Error messages reference table
