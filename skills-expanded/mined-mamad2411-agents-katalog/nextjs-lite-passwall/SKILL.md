---
name: nextjs-lite-passwall
description: Add a lightweight single-password wall to any Next.js app using bcrypt + JWT cookies. Use when a project needs basic auth, a password gate, deployment protection, or when the user says "add a password" or "lock this down" for a Next.js app. Not for user accounts, multi-user auth, or high-security applications — this is a single shared password for keeping personal tools and dashboards private.
metadata:
  author: benbennitt
  version: "1.0"
---

# Next.js Password Wall

Add a single-password auth wall to any Next.js project. One password, one cookie, no database. Designed for protecting personal tools, dashboards, and internal apps you want accessible from anywhere but not public.

## When to Use

- Deploying a personal/internal Next.js app that needs basic protection
- "Add a password to this" or "lock this down before deploying"
- Need deployment protection without a full auth system

## When NOT to Use

- Multi-user auth with accounts, roles, permissions
- OAuth / social login
- Apps that already have an auth system

## Architecture

```
Request → proxy.ts → JWT cookie valid? → App
                   → No cookie/invalid  → /login (UI routes)
                   → No cookie/invalid  → 401 JSON (API routes)
                   → No secret in prod  → 503/redirect (safe lockdown)
```

Three files, one dependency (`bcryptjs`), two env vars for production.

## Implementation

### Step 1: Install dependency

```bash
npm install bcryptjs jose
npm install -D @types/bcryptjs
```

- `bcryptjs` — password hashing (pure JS, no native deps)
- `jose` — JWT signing/verification (edge-compatible, works in middleware)

### Step 2: Create `lib/auth.ts`

Session management utilities. Handles JWT creation, verification, and cookie config.

```typescript
import { SignJWT, jwtVerify } from "jose";
import { cookies } from "next/headers";

const COOKIE_NAME = "session";

function getSecret() {
  const secret = process.env.SESSION_SECRET;
  if (!secret) throw new Error("SESSION_SECRET is not set");
  return new TextEncoder().encode(secret);
}

export async function createSessionToken(): Promise<string> {
  return new SignJWT({ authenticated: true })
    .setProtectedHeader({ alg: "HS256" })
    .setIssuedAt()
    .setExpirationTime("30d")
    .sign(getSecret());
}

export async function verifySessionToken(token: string): Promise<boolean> {
  try {
    await jwtVerify(token, getSecret());
    return true;
  } catch {
    return false;
  }
}

export function getSessionCookieConfig(token: string) {
  return {
    name: COOKIE_NAME,
    value: token,
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax" as const,
    maxAge: 30 * 24 * 60 * 60, // 30 days
    path: "/",
  };
}

export async function getSessionFromCookies(): Promise<boolean> {
  const cookieStore = await cookies();
  const token = cookieStore.get(COOKIE_NAME)?.value;
  if (!token) return false;
  return verifySessionToken(token);
}

export { COOKIE_NAME };
```

**Customization notes:**
- Rename `COOKIE_NAME` to match your app (e.g. `"myapp_session"`)
- Adjust `setExpirationTime("30d")` and `maxAge` if you want shorter sessions

### Step 3: Create `proxy.ts` (or `middleware.ts` for Next.js < 16)

The proxy intercepts every request and checks for a valid session.

> **Next.js 16+** uses `proxy.ts` (exported `proxy` function). **Next.js 15 and earlier** uses `middleware.ts` (exported `middleware` function). The logic is identical — only the file name and export name differ.

```typescript
import { NextRequest, NextResponse } from "next/server";
import { jwtVerify } from "jose";

const COOKIE_NAME = "session"; // Must match lib/auth.ts

const PUBLIC_PATHS = ["/login", "/api/auth"];
const STATIC_PREFIXES = ["/_next", "/favicon"];

function isPublicPath(pathname: string): boolean {
  return (
    PUBLIC_PATHS.some((p) => pathname === p || pathname.startsWith(p + "/")) ||
    STATIC_PREFIXES.some((p) => pathname.startsWith(p))
  );
}

export async function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;

  if (isPublicPath(pathname)) {
    return NextResponse.next();
  }

  const secret = process.env.SESSION_SECRET;
  if (!secret) {
    // No secret configured
    if (process.env.NODE_ENV === "production") {
      // Production without secret = locked down (safe default)
      if (pathname.startsWith("/api/")) {
        return NextResponse.json({ error: "Auth not configured" }, { status: 503 });
      }
      const loginUrl = new URL("/login", request.url);
      loginUrl.searchParams.set("error", "not-configured");
      return NextResponse.redirect(loginUrl);
    }
    // Development without secret = auth disabled (convenience)
    return NextResponse.next();
  }

  const token = request.cookies.get(COOKIE_NAME)?.value;

  if (token) {
    try {
      await jwtVerify(token, new TextEncoder().encode(secret));
      return NextResponse.next();
    } catch {
      // Invalid/expired token — fall through
    }
  }

  if (pathname.startsWith("/api/")) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const loginUrl = new URL("/login", request.url);
  loginUrl.searchParams.set("from", pathname);
  return NextResponse.redirect(loginUrl);
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};
```

**For Next.js 15 and earlier:** rename to `middleware.ts` and change `export async function proxy` to `export async function middleware`.

### Step 4: Create login API route at `app/api/auth/login/route.ts`

```typescript
import { NextRequest, NextResponse } from "next/server";
import bcrypt from "bcryptjs";
import { createSessionToken, getSessionCookieConfig } from "@/lib/auth";

// In-memory rate limiting
const attempts = new Map<string, { count: number; resetAt: number }>();
const MAX_ATTEMPTS = 5;
const WINDOW_MS = 60_000;

function isRateLimited(ip: string): boolean {
  const now = Date.now();
  const record = attempts.get(ip);

  if (!record || now > record.resetAt) {
    attempts.set(ip, { count: 1, resetAt: now + WINDOW_MS });
    return false;
  }

  record.count++;
  return record.count > MAX_ATTEMPTS;
}

export async function POST(request: NextRequest) {
  const ip = request.headers.get("x-forwarded-for") || "unknown";

  if (isRateLimited(ip)) {
    return NextResponse.json(
      { error: "Too many attempts. Try again in a minute." },
      { status: 429 }
    );
  }

  const hash = process.env.PASSWORD_HASH;
  if (!hash) {
    return NextResponse.json({ error: "Auth not configured" }, { status: 500 });
  }

  let body: { password?: string };
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: "Invalid request" }, { status: 400 });
  }

  const { password } = body;
  if (!password || typeof password !== "string") {
    return NextResponse.json({ error: "Password required" }, { status: 400 });
  }

  const valid = await bcrypt.compare(password, hash);
  if (!valid) {
    return NextResponse.json({ error: "Wrong password" }, { status: 401 });
  }

  const token = await createSessionToken();
  const response = NextResponse.json({ ok: true });
  response.cookies.set(getSessionCookieConfig(token));
  return response;
}
```

### Step 5: Create login page at `app/login/page.tsx`

Minimal password form. Adapt styling to match the project's design system.

```tsx
"use client";

import { Suspense, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";

export default function LoginPage() {
  return (
    <Suspense>
      <LoginForm />
    </Suspense>
  );
}

function LoginForm() {
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  const searchParams = useSearchParams();

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const res = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password }),
      });

      if (res.ok) {
        const from = searchParams.get("from") || "/";
        router.push(from);
        router.refresh();
      } else {
        const data = await res.json();
        setError(data.error || "Login failed");
      }
    } catch {
      setError("Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ display: "flex", minHeight: "100vh", alignItems: "center", justifyContent: "center" }}>
      <div style={{ width: "100%", maxWidth: 320 }}>
        <form onSubmit={handleSubmit}>
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoFocus
            autoComplete="current-password"
            style={{ width: "100%", padding: 8, marginBottom: 8 }}
          />
          {error && <p style={{ color: "red", fontSize: 14 }}>{error}</p>}
          <button type="submit" disabled={!password || loading} style={{ width: "100%", padding: 8 }}>
            {loading ? "Logging in..." : "Log in"}
          </button>
        </form>
      </div>
    </div>
  );
}
```

**Styling:** This uses inline styles as a baseline. Replace with the project's component library (shadcn/ui `Button` + `Input`, Tailwind classes, etc.) to match the existing design.

### Step 6: Create password hash script at `scripts/generate-password-hash.ts`

```typescript
#!/usr/bin/env npx tsx
import bcrypt from "bcryptjs";

const password = process.argv[2];
if (!password) {
  console.error("Usage: npx tsx scripts/generate-password-hash.ts <password>");
  process.exit(1);
}

const hash = bcrypt.hashSync(password, 12);
console.log(hash);
```

### Step 7: Add security headers (optional but recommended)

Add to `next.config.ts` (or `.js`/`.mjs`):

```typescript
const securityHeaders = [
  { key: "X-Frame-Options", value: "DENY" },
  { key: "X-Content-Type-Options", value: "nosniff" },
  { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
  { key: "Strict-Transport-Security", value: "max-age=63072000; includeSubDomains; preload" },
];

// Inside your Next.js config:
// headers: async () => [{ source: "/(.*)", headers: securityHeaders }]
```

## Environment Variables

| Variable | Required | Where | Description |
|----------|----------|-------|-------------|
| `PASSWORD_HASH` | Production | Hosting env | bcrypt hash from `scripts/generate-password-hash.ts` |
| `SESSION_SECRET` | Production | Hosting env | Random string: `openssl rand -hex 32` |

**Local dev:** Neither variable is needed. Without `SESSION_SECRET`, the proxy passes all requests through — no login required during development.

**Production without vars:** The app locks down safely. API returns 503, UI redirects to login with an error. Nothing is exposed.

## Setup Commands (for deployment)

```bash
# Generate password hash
npx tsx scripts/generate-password-hash.ts your-password-here
# → Copy the output hash to PASSWORD_HASH env var

# Generate session secret
openssl rand -hex 32
# → Copy to SESSION_SECRET env var
```

## Customization Checklist

After implementing, adjust these to fit the project:

- [ ] `COOKIE_NAME` in `lib/auth.ts` and `proxy.ts` — use an app-specific name
- [ ] `PASSWORD_HASH` / `SESSION_SECRET` env var names — prefix with app name if preferred
- [ ] `PUBLIC_PATHS` in `proxy.ts` — add any routes that should be accessible without auth (webhooks, health checks, public APIs)
- [ ] Login page styling — match the project's design system
- [ ] Session duration — default is 30 days, adjust in both `lib/auth.ts` (JWT expiry + cookie maxAge)
- [ ] Rate limit thresholds — default is 5 attempts per minute per IP
