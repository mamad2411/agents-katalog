---
name: sentry
description: Sentry error monitoring for Next.js — @sentry/nextjs setup, source maps, and capture patterns. Use when adding Sentry to the project, querying production errors, or implementing error boundaries.
---

If the project has the Sentry MCP configured (`mcp__sentry__*`), use it to query production errors, releases, and performance data.

## Setup checklist

- `NEXT_PUBLIC_ENV` in Doppler (`stg` / `prd`) — used as the Sentry environment tag
- `SENTRY_DSN` in Doppler → exposed as `NEXT_PUBLIC_SENTRY_DSN` (the DSN is safe to expose)
- `SENTRY_AUTH_TOKEN` in Doppler — build-time only, for source map uploads; never `NEXT_PUBLIC_`
- Run the wizard once: `yarn dlx @sentry/wizard@latest -i nextjs` — it scaffolds the config files and wraps `next.config.ts`
- One Sentry project per app, two environments (`stg` + `prd`) — not two projects

## The three runtimes

`@sentry/nextjs` initialises Sentry separately per runtime — all three must exist or that runtime's errors vanish silently:

| File | Runtime |
| --- | --- |
| `sentry.client.config.ts` (or the client init in `instrumentation-client.ts`) | Browser |
| `sentry.server.config.ts` | Node (server components, route handlers, server actions) |
| `sentry.edge.config.ts` | Edge (middleware) |

Each init follows the same shape:

```ts
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NEXT_PUBLIC_ENV, // "stg" | "prd"
  enabled: process.env.NODE_ENV === 'production',
  tracesSampleRate: 0.2,
});
```

The `enabled` flag is the correct way to disable Sentry in dev — do not conditionally zero `tracesSampleRate` as a substitute.

`next.config.ts` is wrapped with `withSentryConfig(nextConfig, { … })` — that wrapper is what uploads source maps during `next build` using `SENTRY_AUTH_TOKEN`. If prod stack traces show minified frames, the token was missing at build time.

## Error boundaries (App Router)

Next.js error files are the boundary mechanism — report from them rather than wrapping components by hand:

```tsx
// app/global-error.tsx — catches root layout errors
'use client';
import * as Sentry from '@sentry/nextjs';
import { useEffect } from 'react';

export default function GlobalError({ error }: { error: Error & { digest?: string } }) {
  useEffect(() => { Sentry.captureException(error); }, [error]);
  return (
    <html><body><h2>Something went wrong</h2></body></html>
  );
}
```

Per-section `app/**/error.tsx` files follow the same `captureException` pattern with a scoped, recoverable UI. Wrap segment roots — not every leaf component.

## Capture patterns

```ts
// Unexpected error with context
Sentry.withScope((scope) => {
  scope.setTag('feature', 'billing');
  scope.setUser({ id: userId }); // opaque id only — never email
  Sentry.captureException(error);
});

// Non-fatal event
Sentry.captureMessage('Stripe webhook retry', 'warning');

// Breadcrumb for manual tracing
Sentry.addBreadcrumb({ message: 'User clicked upgrade', category: 'ui' });
```

In route handlers and server actions, catch → `captureException` → rethrow or return a typed error response; swallowing the error after capture hides it from the caller.

## MCP usage

- `search_issues` — surface recent production errors
- `get_sentry_resource` — inspect a specific issue with stack trace
- `search_events` — check error frequency per release/environment

## Rules

- Set `environment` from Doppler so stg errors don't pollute prd
- Never log PII (emails, card numbers) in scope tags or breadcrumbs — opaque internal ids only
- Tag the tenant (`scope.setTag('business_id', …)`) on server-side captures — the first debugging question in a multi-tenant app is "which tenant?"
- Source maps: `SENTRY_AUTH_TOKEN` must be present in the CI/build environment; verify one readable prod stack trace after the first deploy
