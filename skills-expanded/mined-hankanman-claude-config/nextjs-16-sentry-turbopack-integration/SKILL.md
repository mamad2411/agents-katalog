---
name: nextjs-16-sentry-turbopack-integration
description: |
  Fix Sentry integration issues in Next.js 16 with Turbopack. Use when: (1) Getting "Route used Math.random() before accessing uncached data" errors after adding Sentry, (2) Deprecation warnings about disableLogger/automaticVercelMonitors, (3) TypeScript errors about NextRequest type incompatibility with duplicate Next.js installations, (4) Build fails with OpenTelemetry-related errors. Covers Sentry SDK 10.x + Next.js 16 + Turbopack monorepo setup with proper configuration.
author: Claude Code
version: 1.0.0
date: 2026-02-01
---

# Next.js 16 + Sentry + Turbopack Integration

## Problem

Integrating Sentry into a Next.js 16 project using Turbopack causes multiple issues:
1. `Math.random()` errors during SSR from Sentry's OpenTelemetry integration
2. Deprecation warnings for webpack-specific Sentry options
3. TypeScript type errors from duplicate Next.js installations
4. Performance tracing conflicts with Next.js 16's prerendering

## Context / Trigger Conditions

**Exact error messages you'll encounter:**

```
Route "/[locale]/page" used `Math.random()` before accessing uncached data.
    at RandomIdGenerator.generateId [as generateSpanId]
    (@opentelemetry/sdk-trace-base/src/platform/node/RandomIdGenerator.ts:42:41)
```

```
[@sentry/nextjs] DEPRECATION WARNING: disableLogger is deprecated and will be
removed in a future version. Use webpack.treeshake.removeDebugLogging instead.
(Not supported with Turbopack.)

[@sentry/nextjs] DEPRECATION WARNING: automaticVercelMonitors is deprecated
and will be removed in a future version. Use webpack.automaticVercelMonitors
instead. (Not supported with Turbopack.)
```

```
error TS2769: No overload matches this call.
  Type 'NextRequest' is not assignable to type 'NextRequest'.
    Property '[Internal]' is missing in type 'NextURL'
```

**When this occurs:**
- Using `@sentry/nextjs` ^10.x with Next.js 16.x
- Turbopack enabled (default in Next.js 16)
- Monorepo setup with pnpm workspaces
- After running Sentry wizard or manual installation

## Solution

### Step 1: Fix Math.random() Error - Disable Tracing in Development

The error occurs because Sentry's OpenTelemetry integration uses `Math.random()` for span IDs during SSR, which Next.js 16 doesn't allow before accessing uncached data.

**Fix:** Disable performance tracing in development (only enable in production):

```typescript
// sentry.client.config.ts, sentry.server.config.ts, sentry.edge.config.ts
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,

  // Disable tracing in development to avoid Math.random() errors
  // In production, sample 100% of transactions
  tracesSampleRate: process.env.NODE_ENV === "production" ? 1 : 0,

  // ... other config
});
```

**Why this works:** Performance tracing requires generating random span IDs, which triggers the error. Disabling it in dev prevents the issue while keeping error tracking functional.

### Step 2: Remove Deprecated Webpack Options

Turbopack doesn't support webpack-specific Sentry configuration options.

**Fix:** Remove `disableLogger` and `automaticVercelMonitors` from `withSentryConfig`:

```typescript
// next.config.ts
export default withSentryConfig(configWithIntl, {
  org: "your-org",
  project: "your-project",
  silent: !process.env.CI,
  widenClientFileUpload: true,
  tunnelRoute: "/monitoring",

  // ❌ Remove these deprecated options:
  // disableLogger: true,
  // automaticVercelMonitors: true,

  // Note: These would need to be configured via webpack.treeshake.removeDebugLogging
  // and webpack.automaticVercelMonitors, but Turbopack doesn't support them anyway
});
```

### Step 3: Fix TypeScript Errors - Deduplicate Dependencies

Sentry + OpenTelemetry can cause duplicate Next.js installations in pnpm, leading to type incompatibilities.

**Fix:** Run `pnpm dedupe` to resolve duplicate dependencies:

```bash
pnpm dedupe
```

**Verify the fix:**
```bash
pnpm --filter web types  # Should show 0 errors
```

### Step 4: Remove Manual Sentry Imports from instrumentation.ts

Next.js 16 auto-imports Sentry config files; manual imports can cause initialization issues.

**Fix:** Remove manual Sentry imports from `instrumentation.ts`:

```typescript
// instrumentation.ts
export async function register() {
  loadEnvConfig("../..", process.env.NODE_ENV !== "production");

  // ❌ Remove these manual imports:
  // if (process.env.NEXT_RUNTIME === "nodejs") {
  //   import("./sentry.server.config");
  // }

  // ✅ Sentry configs are auto-imported by Next.js 16
}
```

### Step 5: Disable Session Replay in Development

Session Replay adds overhead and uses performance APIs that can conflict with dev mode.

**Fix:** Only enable in production:

```typescript
// sentry.client.config.ts
Sentry.init({
  // ...
  replaysOnErrorSampleRate: process.env.NODE_ENV === "production" ? 1.0 : 0,
  replaysSessionSampleRate: process.env.NODE_ENV === "production" ? 0.1 : 0,
});
```

### Step 6: Manual Client Initialization (Required for Turbopack)

**CRITICAL:** Next.js 16 with Turbopack doesn't auto-import `sentry.client.config.ts`. You must manually initialize Sentry in a Client Component.

**Create `components/sentry-init.tsx`:**

```typescript
"use client";

import { useEffect } from "react";

export function SentryInit() {
  useEffect(() => {
    // Dynamic import to ensure this only runs client-side
    import("../sentry.client.config");
  }, []);

  return null;
}
```

**Add to your locale layout (`app/[locale]/layout.tsx`):**

```typescript
import { SentryInit } from "@/components/sentry-init";

export default function LocaleLayout({ children }) {
  return (
    <>
      {/* ... other layout code */}
      <SentryInit />
      {children}
    </>
  );
}
```

**Why this is necessary:** Importing `sentry.client.config.ts` in a Server Component (like root layout) causes errors because `replayIntegration` doesn't exist on the server. The Client Component with `useEffect` ensures it only runs in the browser.

### Step 7: Update CSP for Sentry Domains

Add Sentry domains to Content Security Policy:

```typescript
// next.config.ts
const commonDirectives = [
  // ... other directives
  "connect-src 'self' https://*.ingest.sentry.io https://*.sentry.io",
];
```

### Step 8: Remove Tunnel Route (Optional)

The `tunnelRoute` option proxies Sentry requests through your Next.js app to bypass ad-blockers, but requires additional API route setup. For simplicity, remove it during initial setup:

```typescript
// next.config.ts
export default withSentryConfig(configWithIntl, {
  org: "your-org",
  project: "your-project",
  silent: !process.env.CI,
  widenClientFileUpload: true,
  // tunnelRoute: "/monitoring", // Remove or comment out
});
```

You can re-enable it later by creating the `/monitoring` API route handler.

## Complete Configuration Example

```typescript
// sentry.client.config.ts
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  enableLogs: true,

  // Disable tracing in dev, enable in prod
  tracesSampleRate: process.env.NODE_ENV === "production" ? 1 : 0,

  // Session Replay: only in production
  replaysOnErrorSampleRate: process.env.NODE_ENV === "production" ? 1.0 : 0,
  replaysSessionSampleRate: process.env.NODE_ENV === "production" ? 0.1 : 0,

  integrations: [
    Sentry.consoleLoggingIntegration({ levels: ["log", "warn", "error"] }),
    Sentry.replayIntegration({
      maskAllText: true,
      blockAllMedia: true,
    }),
  ],

  beforeBreadcrumb(breadcrumb) {
    if (breadcrumb.category === "console") return null;
    return breadcrumb;
  },

  // Enable in production only
  enabled: process.env.NODE_ENV === "production",
});
```

```typescript
// next.config.ts
import { withSentryConfig } from "@sentry/nextjs";

export default withSentryConfig(configWithIntl, {
  org: "your-org",
  project: "your-project",
  silent: !process.env.CI,
  widenClientFileUpload: true,
  tunnelRoute: "/monitoring",
  // Don't include deprecated webpack options
});
```

## Verification

1. **Build should succeed with no warnings:**
   ```bash
   pnpm build
   # Should complete without deprecation warnings or errors
   ```

2. **Dev server should start without Math.random() errors:**
   ```bash
   pnpm dev
   # No errors about Math.random() in console
   ```

3. **TypeScript should pass:**
   ```bash
   pnpm types
   # Should show 0 errors
   ```

4. **Test in production mode:**
   ```bash
   pnpm start
   # Sentry should send errors in production mode
   ```

## Example: Testing the Integration

Create a test page to verify Sentry works in production:

```typescript
// app/[locale]/sentry-test/page.tsx
"use client";

import { captureException } from "@sentry/nextjs";

export default function SentryTestPage() {
  function testError() {
    try {
      throw new Error("Test Sentry integration");
    } catch (error) {
      captureException(error);
      alert("Error sent to Sentry!");
    }
  }

  return <button onClick={testError}>Test Sentry</button>;
}
```

Build and run in production mode, then visit `/en/sentry-test` and click the button. Check your Sentry dashboard for the error.

## Notes

### Why Tracing Must Be Disabled in Development

Next.js 16 with `dynamicIO` (enabled by default) prevents synchronous access to random values (like `Math.random()`) during server-side rendering before accessing uncached data or request data. Sentry's OpenTelemetry integration uses `Math.random()` in `RandomIdGenerator.generateSpanId()` to generate trace IDs, which triggers this error.

The Next.js team considers this overly verbose for instrumentation libraries (see [GitHub discussion #72572](https://github.com/vercel/next.js/discussions/72572)), but as of Next.js 16.1.5, it's still an issue.

### Manual Initialization Required with Turbopack

**Critical Discovery:** Next.js 16 with Turbopack does **not** auto-import `sentry.client.config.ts` like the webpack build does. You must manually initialize Sentry via a Client Component with `useEffect` and dynamic import.

**Why this is necessary:**
- Importing `sentry.client.config.ts` directly in a Server Component (like root layout) causes runtime errors because `replayIntegration()` doesn't exist in the server build
- Turbopack's module resolution doesn't automatically inject the Sentry config imports
- The `withSentryConfig` wrapper in `next.config.ts` doesn't work the same way with Turbopack

**The solution:** Create a Client Component (`<SentryInit />`) that uses `useEffect` with dynamic import to ensure Sentry only initializes in the browser, then add this component to your layout.

### Turbopack vs Webpack

Next.js 16 uses Turbopack by default. Turbopack doesn't support webpack-specific plugins, so Sentry's `disableLogger` and `automaticVercelMonitors` options (which use webpack plugins under the hood) don't work and will show deprecation warnings.

### Monorepo Considerations

In pnpm monorepos, Sentry + OpenTelemetry can create duplicate Next.js installations due to dependency hoisting. Always run `pnpm dedupe` after installing Sentry to avoid type errors.

### Session Replay Overhead

Session Replay captures DOM changes and user interactions, which adds significant overhead in development. Keep it disabled in dev to avoid performance issues and potential conflicts with hot module replacement.

### Testing in Development

Since Sentry is disabled in development (to avoid errors), you must test in production mode (`pnpm build && pnpm start`) to verify errors are being sent to Sentry.

Alternatively, temporarily set `enabled: true` in the Sentry config for testing, but remember to change it back to `enabled: process.env.NODE_ENV === "production"`.

## References

- [Next.js Math.random() Error Documentation](https://nextjs.org/docs/messages/next-prerender-random)
- [Next.js 16 Release Blog](https://nextjs.org/blog/next-16)
- [Sentry Next.js Documentation](https://docs.sentry.io/platforms/javascript/guides/nextjs/)
- [Sentry Turbopack Support Blog](https://blog.sentry.io/turbopack-support-next-js-sdk/)
- [GitHub Discussion: OpenTelemetry Math.random() Issue](https://github.com/vercel/next.js/discussions/72572)
- [GitHub Issue: Sentry + dynamicIO Error](https://github.com/getsentry/sentry-javascript/issues/14118)
- [Sentry Next.js Troubleshooting](https://docs.sentry.io/platforms/javascript/guides/nextjs/troubleshooting/)
