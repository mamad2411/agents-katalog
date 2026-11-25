---
name: sentry-integration
description: Add Sentry error tracking to Supabase Edge Functions. Use when creating functions that need error monitoring.
---

# Sentry Integration for Supabase Edge Functions

## Helpers Available

Module `_shared/sentry.ts` provides:
- `initSentry()` - Initialize (call once)
- `handleError()` - Capture errors automatically
- `setSentryUser()` - Track user (optional)
- `addBreadcrumb()` - Track flow (optional)

## Usage

### Basic Pattern

```typescript
import { initSentry, handleError } from '../_shared/sentry.ts';

initSentry();

Deno.serve(async (req: Request) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders });
  }

  try {
    const result = await processData();
    return new Response(JSON.stringify({ success: true }));
  } catch (error) {
    return handleError(error, { functionName: 'my-function', corsHeaders });
  }
});
```

### With User Context

```typescript
import { initSentry, setSentryUser, handleError } from '../_shared/sentry.ts';
import { authenticate } from '../_shared/auth.ts';

initSentry();

Deno.serve(async (req: Request) => {
  try {
    const { user } = await authenticate(req);
    setSentryUser(user.id, user.email);
    
    // Your logic
    
    return new Response(JSON.stringify({ success: true }));
  } catch (error) {
    return handleError(error, { functionName: 'auth-function', corsHeaders });
  }
});
```

### With Breadcrumbs

```typescript
import { initSentry, addBreadcrumb, handleError } from '../_shared/sentry.ts';

initSentry();

try {
  addBreadcrumb('Started processing');
  const result = await process();
  addBreadcrumb('Completed', { count: result.length });
} catch (error) {
  return handleError(error, { functionName: 'processor', corsHeaders });
}
```

## Setup

1. **Set SENTRY_DSN** in `.env.local`:
   ```bash
   SENTRY_DSN=https://your-sentry-dsn@sentry.io/123456
   ```

2. **Module exists** at `supabase/functions/_shared/sentry.ts` (already created)

## What Gets Captured

✅ Error message and stack trace  
✅ Function name (tagged)  
✅ Request details  
✅ User context (if set)  
✅ Breadcrumbs (if added)  
❌ Authorization headers (auto-removed)

## Testing

```typescript
throw new Error('Test error for Sentry');
```

Check Sentry dashboard for the error with full context.
