---
name: nextjs-better-auth-session-guard
description: |
  Fix session invalidation detection in Next.js 16 App Router with Better Auth.
  Use when: (1) Signed-out header but protected content still visible after sign-out,
  (2) Session changes not detected until page interaction/reload, (3) E2E tests fail
  with "should maintain session after page reload" or similar session persistence tests,
  (4) Users can view dashboard content after signing out until they click something.
  Implements dual-layer auth: server-side check (initial render) + client-side monitoring
  (runtime invalidation detection) using Better Auth's useSession hook with proper
  polling configuration.
author: Claude Code
version: 1.0.0
date: 2026-01-25
---

# Next.js Better Auth Session Guard Pattern

## Problem

In Next.js 16 App Router applications using Better Auth, session invalidation isn't
automatically detected client-side. This creates a security and UX issue where:

- User signs out → header updates to signed-out state
- Protected content (dashboard, profile, etc.) remains visible
- Content only disappears after user interaction triggers re-render
- E2E tests fail because session state isn't consistent

**Root Cause**: Server-side auth check in layouts only runs on initial render (wrapped
in Suspense). There's no client-side monitoring for session state changes after the
initial server validation.

## Context / Trigger Conditions

**Symptoms:**
- Header shows "Sign In" button but dashboard content is visible
- Users report seeing protected pages briefly after signing out
- E2E tests fail with inconsistent session state
- Test failures like "should maintain session after page reload" or "session persists"

**Environment:**
- Next.js 16+ with App Router
- Better Auth v1.4.10+
- Using server-side session checks in layouts (`auth.api.getSession()`)
- Protected routes under route groups like `(app)` or `(authenticated)`

**When This Pattern Is Needed:**
- Any app with authentication using Better Auth
- Apps that need immediate session invalidation detection
- Apps with strict security requirements (SaaS, healthcare, finance)
- Apps with E2E tests that verify session persistence

## Solution

Implement a dual-layer authentication approach following 2026 best practices:

### Layer 1: Server-Side Initial Check (Already Implemented)

Keep existing server-side validation in your layout:

```typescript
// app/[locale]/(app)/layout.tsx
async function AuthLayoutContent({ children, locale }: Props) {
  const session = await auth.api.getSession({ headers: await headers() });

  if (!session) {
    return redirect({ href: "/sign-in", locale });
  }

  return <main>{children}</main>;
}
```

### Layer 2: Client-Side Runtime Monitoring (Add This)

**Step 1: Create SessionGuard Component**

Create `components/auth/SessionGuard.tsx`:

```typescript
"use client";

import { authClient } from "auth/client";
import { useEffect, useRef } from "react";
import { useRouter } from "next/navigation"; // or your routing library

interface SessionGuardProps {
  children: React.ReactNode;
  requireAuth?: boolean;
  redirectTo?: string;
}

/**
 * SessionGuard - Client-side session monitoring component
 *
 * Monitors session state and redirects to sign-in when session becomes invalid.
 * Works alongside server-side auth check to provide real-time session invalidation detection.
 *
 * Key features:
 * - No loading spinner (server already verified auth)
 * - Uses useRef to prevent double redirects
 * - Preserves return URL for post-signin redirect
 * - Only triggers on session invalidation, not initial load
 */
export function SessionGuard({
  children,
  requireAuth = true,
  redirectTo = "/sign-in",
}: SessionGuardProps) {
  const { data: session, isPending } = authClient.useSession();
  const router = useRouter();
  const hasRedirected = useRef(false);

  useEffect(() => {
    // Only run after session check completes
    if (isPending) return;

    // Redirect if auth required but no session exists
    if (requireAuth && !session && !hasRedirected.current) {
      hasRedirected.current = true;
      // Preserve current URL for post-signin redirect
      const returnUrl = window.location.pathname + window.location.search;
      router.push(`${redirectTo}?returnUrl=${encodeURIComponent(returnUrl)}`);
    }
  }, [session, isPending, requireAuth, redirectTo, router]);

  // Render children immediately (server already verified auth)
  // This just monitors for changes after initial render
  return <>{children}</>;
}
```

**Step 2: Integrate into Layout**

Wrap your protected content in the SessionGuard:

```typescript
// app/[locale]/(app)/layout.tsx
import { SessionGuard } from "@/components/auth/SessionGuard";

async function AuthLayoutContent({ children, locale }: Props) {
  const session = await auth.api.getSession({ headers: await headers() });

  if (!session) {
    return redirect({ href: "/sign-in", locale });
  }

  return (
    <SessionGuard>
      <main>{children}</main>
    </SessionGuard>
  );
}
```

**Step 3: Configure Session Polling**

In your auth client configuration (`packages/auth/src/auth-client.ts` or similar):

```typescript
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: /* ... */,
  plugins: [ /* ... */ ],
  session: {
    fetchOnWindowFocus: true,  // Re-check when user returns to tab
    fetchOnReconnect: true,     // Re-check when network reconnects
    refetchInterval: 300000,    // Check every 5 minutes (reduces server load)
  },
});
```

**Polling Configuration Guidelines (2026 Best Practices):**
- **5 minutes (300000ms)**: Good balance for most apps
- **1 minute (60000ms)**: High-security apps requiring faster detection
- **10 minutes (600000ms)**: Low-security apps prioritizing reduced server load
- Always enable `fetchOnWindowFocus` and `fetchOnReconnect` for better UX

## Verification

### Manual Testing

1. **Sign out invalidation:**
   - Sign in → navigate to protected route (e.g., `/dashboard`)
   - Sign out in header
   - Dashboard should redirect to `/sign-in` within 1-2 seconds

2. **Session persistence:**
   - Sign in → navigate to protected route
   - Reload page (F5)
   - Should stay signed in, content remains visible

3. **Multi-tab invalidation:**
   - Sign in → open two tabs with protected route
   - Sign out in tab 1
   - Switch to tab 2 → should redirect to sign-in when focused

4. **Cookie expiry:**
   - Sign in → navigate to protected route
   - Clear cookies in DevTools
   - Reload → should redirect to `/sign-in`

### E2E Testing Patterns

**Test: Session Persistence After Reload**

```typescript
test("should maintain session after page reload", async ({ page }) => {
  const authPage = new AuthPage(page, "en");
  await authPage.goto("/");
  await authPage.signIn(TEST_USER);
  await authPage.expectSignedIn();

  // Wait for session to be fully established
  await page.waitForLoadState("networkidle");

  // Verify session cookies are set before reload
  const cookies = await page.context().cookies();
  const sessionCookie = cookies.find((c) =>
    c.name.includes("better-auth.session_token") || c.name.includes("session")
  );
  expect(sessionCookie).toBeDefined();

  // Reload page
  await page.reload({ waitUntil: "networkidle" });

  // Wait for client-side session hydration (SessionGuard + useSession)
  await page.waitForTimeout(2000);

  // Verify session persists after reload
  await authPage.expectSignedIn();
});
```

**Key Testing Insights:**
- Wait 2 seconds after reload for client-side session hydration
- Verify cookies before reload to ensure session was established
- Use `networkidle` to ensure all network requests complete

## Example: Complete Implementation

Here's a full example showing all pieces together:

**1. Auth Client Configuration:**

```typescript
// packages/auth/src/auth-client.ts
export const authClient = createAuthClient({
  baseURL: typeof window !== "undefined"
    ? window.location.origin
    : process.env.NEXT_PUBLIC_APP_URL,
  plugins: [/* your plugins */],
  session: {
    fetchOnWindowFocus: true,
    fetchOnReconnect: true,
    refetchInterval: 300000, // 5 minutes
  },
});
```

**2. SessionGuard Component:**

```typescript
// components/auth/SessionGuard.tsx
"use client";

import { authClient } from "auth/client";
import { useEffect, useRef } from "react";
import { useRouter } from "@/i18n/routing";

export function SessionGuard({ children, requireAuth = true, redirectTo = "/sign-in" }) {
  const { data: session, isPending } = authClient.useSession();
  const router = useRouter();
  const hasRedirected = useRef(false);

  useEffect(() => {
    if (isPending) return;
    if (requireAuth && !session && !hasRedirected.current) {
      hasRedirected.current = true;
      const returnUrl = window.location.pathname + window.location.search;
      router.push(`${redirectTo}?returnUrl=${encodeURIComponent(returnUrl)}`);
    }
  }, [session, isPending, requireAuth, redirectTo, router]);

  return <>{children}</>;
}
```

**3. Layout Integration:**

```typescript
// app/[locale]/(app)/layout.tsx
import { SessionGuard } from "@/components/auth/SessionGuard";

async function AuthLayoutContent({ children, locale }) {
  const session = await auth.api.getSession({ headers: await headers() });
  if (!session) return redirect({ href: "/sign-in", locale });

  return (
    <SessionGuard>
      <main>{children}</main>
    </SessionGuard>
  );
}

export default async function AppLayout({ children, params }) {
  const { locale } = await params;

  return (
    <div>
      <Suspense fallback={<HeaderSkeleton />}>
        <Header />
      </Suspense>
      <Suspense fallback={<LoadingSkeleton />}>
        <AuthLayoutContent locale={locale}>{children}</AuthLayoutContent>
      </Suspense>
    </div>
  );
}
```

## Notes

### Performance Considerations

- **SessionGuard runs client-side only**: No SSR impact, no duplicate work
- **Server check happens first**: Client monitoring is additive, not redundant
- **Configurable polling**: 5-minute default balances UX and server load
- **useRef prevents redundant redirects**: No redirect loops or duplicate navigations

### Security Considerations

- **Defense in depth**: Server-side check (initial) + client-side monitoring (runtime)
- **Both layers required**: Don't skip server-side validation thinking client is enough
- **Return URL validated server-side**: Client preserves URL but server must validate it
- **Cookie-based sessions**: Better Auth uses httpOnly cookies for security

### UX Considerations

- **No loading spinner**: Content renders immediately (server verified auth)
- **Return URL preserved**: Better UX when session expires during navigation
- **Redirect only on invalidation**: Initial page load doesn't trigger redirect
- **Multi-tab support**: `fetchOnWindowFocus` detects sign-out in other tabs

### Edge Cases Handled

- **Initial page load**: Server check runs, SessionGuard doesn't redirect
- **Page reload**: Cookies persist, session hydrates, no redirect
- **Session invalidation**: Client detects within polling interval, redirects with return URL
- **Race conditions**: `useRef` prevents double redirects
- **Network issues**: `fetchOnReconnect` re-checks when connection restored

### Known Issues (Better Auth v1.4.10)

Based on 2026 research, be aware of these Better Auth limitations:

1. **Server-side actions may not trigger useSession updates**: Sometimes navbar reading
   session state using `useSession` doesn't auto-update after server-side sign-in/sign-out.
   The SessionGuard pattern mitigates this with polling.

2. **Cache invalidation inconsistency**: `useSession().refetch()` doesn't support
   `disableCookieCache` parameter like `getSession()` does. Use polling instead of
   relying solely on refetch.

3. **Occasional state update failures**: Session state may not update ~50% of the time
   in some setups. The 5-minute polling interval ensures eventual consistency.

### Alternative Patterns (Not Recommended)

**Why not middleware-only?**
- Middleware doesn't detect runtime session changes
- CVE-2025-29927 vulnerability showed relying solely on middleware is insufficient
- Better Auth docs recommend checking session in Server Components, not just middleware

**Why not client-only?**
- Client-side checks can be bypassed
- Initial load has no protection until JavaScript loads
- Violates defense-in-depth security principles

**Why not websockets/server-sent events?**
- Adds complexity and infrastructure requirements
- Polling is simpler and works with serverless/edge deployments
- 5-minute interval is acceptable latency for most apps

## References

### Official Documentation
- [Better Auth Next.js Integration](https://www.better-auth.com/docs/integrations/next)
- [Better Auth Session Management](https://www.better-auth.com/docs/concepts/session-management)
- [Next.js Authentication Guide](https://nextjs.org/docs/app/guides/authentication)

### Best Practices (2026)
- [Top 5 Authentication Solutions for Next.js 2026](https://workos.com/blog/top-authentication-solutions-nextjs-2026)
- [Robust Security & Authentication Best Practices in Next.js 16](https://medium.com/@sureshdotariya/robust-security-authentication-best-practices-in-next-js-16-6265d2d41b13)
- [Next.js 16: What's New for Authentication](https://auth0.com/blog/whats-new-nextjs-16/)

### Known Issues
- [Better Auth Issue #3608: Server-side actions not triggering useSession updates](https://github.com/better-auth/better-auth/issues/3608)
- [Better Auth Issue #1006: useSession not always triggering state change](https://github.com/better-auth/better-auth/issues/1006)
- [Better Auth Issue #3889: Query parameter support for useSession().refetch()](https://github.com/better-auth/better-auth/issues/3889)
