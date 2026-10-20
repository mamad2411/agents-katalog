---
name: volcano-error-handling
description: "Reusable error handling patterns for Volcano SDK apps: centralized error dispatcher with action enum, useApiCall React hook for loading/error/data state, retry with exponential backoff, retry with toast notifications, and cross-domain error message catalog."
---
# Volcano Error Handling Skill

## Role
Provide the reusable error-handling infrastructure for Volcano SDK apps. Pair with `volcano-uiux` when errors, retries, or progress appear in a user-facing interface. The other domain skills (`volcano-auth`, `volcano-database`, etc.) cover error MESSAGES per domain; this skill covers error-handling PRIMITIVES that the rest of the codebase composes on:

- A centralized error dispatcher that returns an `action` enum.
- A `useApiCall<T>` React hook for `loading`/`error`/`data` lifecycle.
- Retry utilities with exponential backoff.
- Toast-aware retry for slow-but-recoverable operations.

## When to use
- Building any non-trivial UI that fetches Volcano data.
- Refactoring scattered `if (error) return ...` into a single dispatcher.
- Adding retry around transient failures (timeouts, rate limits).
- Establishing the project's loading/error/data UI conventions.

## The Volcano Error Pattern (recap)
Every SDK method returns `{ data, error }`. `error` is `Error | null`. NEVER wrap SDK calls in try/catch expecting throws — the error comes back in the response object. Some methods (functions, downloads) include richer fields (`status`, `headers`, `version`, etc.); the `error` field is always present.

Realtime is the one exception: `await channel.subscribe()` may throw, and `realtime.onError(ctx => ...)` is the connection-level handler. See the Realtime section below.

## Centralized Error Dispatcher

The single most useful primitive: a function that maps a raw error to a `{ message, action }` pair where `action` is a small enum. This decouples error MEANING from error PRESENTATION.

```ts
// Place next to the UI code: web/lib/errors.ts for a web/ frontend,
// or the existing shared UI helper path for a non-web app.
export type ErrorAction =
  | 'redirect_login'
  | 'show_error'
  | 'retry'
  | 'wait';

export interface ErrorDecision {
  message: string;
  action: ErrorAction;
}

export function handleApiError(error: Error, context = 'Operation'): ErrorDecision {
  console.error(`${context} error:`, error);

  if (error.message.includes('No active session')) {
    return { message: 'Please sign in to continue.', action: 'redirect_login' };
  }
  if (error.message.includes('permission denied')) {
    return { message: `You don't have permission to perform this action.`, action: 'show_error' };
  }
  if (error.message.includes('timeout')) {
    return { message: 'Request timed out. Please try again.', action: 'retry' };
  }
  if (error.message.includes('rate limit')) {
    return { message: 'Too many requests. Please wait a moment.', action: 'wait' };
  }

  return { message: `${context} failed. Please try again.`, action: 'show_error' };
}
```

### Using the dispatcher
```ts
const { data, error } = await volcano.from('posts').select('*');

if (error) {
  const { message, action } = handleApiError(error, 'Loading posts');
  switch (action) {
    case 'redirect_login':
      router.push('/login');
      break;
    case 'retry':
      // queue a retry — see useApiCall + fetchWithRetry below
      break;
    case 'wait':
      showToast(message, 'info');
      break;
    default:
      showToast(message, 'error');
  }
  return;
}
```

### When to extend the dispatcher
Add a new branch when:
- A new error class (e.g., `'quota exceeded'`) needs a distinct user-visible action.
- Two existing branches collapse to the same action and message — replace the branch with a single check.

Don't add domain-specific messages here (those belong in the per-domain skills' Common Errors tables); keep the dispatcher cross-cutting.

## React Hook: `useApiCall<T>`

The canonical loading/error/data hook. Use it everywhere you fetch Volcano data inside a component.

```tsx
// hooks/useApiCall.ts
import { useState, useCallback } from 'react';

interface ApiCallState<T> {
  data: T | null;
  error: Error | null;
  loading: boolean;
}

export function useApiCall<T>() {
  const [state, setState] = useState<ApiCallState<T>>({
    data: null,
    error: null,
    loading: false,
  });

  const execute = useCallback(async (
    apiCall: () => Promise<{ data: T | null; error: Error | null }>,
  ) => {
    setState({ data: null, error: null, loading: true });
    try {
      const result = await apiCall();
      if (result.error) {
        setState({ data: null, error: result.error, loading: false });
        return { data: null, error: result.error };
      }
      setState({ data: result.data, error: null, loading: false });
      return { data: result.data, error: null };
    } catch (e) {
      const error = e instanceof Error ? e : new Error('Unknown error');
      setState({ data: null, error, loading: false });
      return { data: null, error };
    }
  }, []);

  return { ...state, execute };
}
```

### Usage
```tsx
import { useEffect, useState } from 'react';

function LoadingPosts() {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const timer = window.setTimeout(() => setVisible(true), 200);
    return () => window.clearTimeout(timer);
  }, []);

  if (!visible) return null;
  return <div role="status"><Spinner aria-hidden="true" /> Loading posts…</div>;
}

function PostList() {
  const { data: posts, error, loading, execute } = useApiCall<Post[]>();

  useEffect(() => {
    execute(() =>
      volcano
        .from<Post>('posts')
        .select('*')
        .order('created_at', { ascending: false }),
    );
  }, [execute]);

  if (loading) return <LoadingPosts />;
  if (error) return <ErrorMessage error={error} />;
  if (!posts?.length) return <Empty />;

  return <PostGrid posts={posts} />;
}
```

The pattern: render-as-state (loading/error/data), and the hook moves you between those states atomically. Three early returns at the top of the component keep the happy path linear.

## Retry with Exponential Backoff

For transient failures (timeouts, network blips, brief rate limits), wrap the call in `fetchWithRetry`. Note the explicit allowlist of NON-retryable errors — re-trying `permission denied` or `not found` will never succeed and just delays user feedback.

```ts
// Place next to the UI code: web/lib/retry.ts for a web/ frontend,
// or the existing shared UI helper path for a non-web app.
type ApiResult<T> = { data: T | null; error: Error | null };

export async function fetchWithRetry<T>(
  fn: () => Promise<ApiResult<T>>,
  maxRetries = 3,
): Promise<ApiResult<T>> {
  let lastError: Error | null = null;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    const { data, error } = await fn();
    if (!error) return { data, error: null };
    lastError = error;

    // Non-retryable errors: bail immediately.
    if (
      error.message.includes('permission denied') ||
      error.message.includes('invalid') ||
      error.message.includes('not found')
    ) {
      return { data: null, error };
    }

    // Exponential backoff: 2s, 4s, 8s ...
    if (attempt < maxRetries) {
      await new Promise(resolve =>
        setTimeout(resolve, Math.pow(2, attempt) * 1000),
      );
    }
  }

  return { data: null, error: lastError };
}
```

### Usage
```ts
const { data, error } = await fetchWithRetry(() =>
  volcano.from('posts').select('*'),
);
```

### Tuning
- **Default `maxRetries = 3`** — covers ~14 seconds total wait. Past that, the user is better served by a clear error than more silent waiting.
- **Don't retry mutations blindly.** Reads are idempotent; inserts/updates/deletes can produce duplicate rows or partial state on retry. Either retry only on confirmed-network errors, or design the mutation to be idempotent (e.g., `INSERT ... ON CONFLICT DO NOTHING` server-side).

## Retry with Toast Notification (slow-but-recoverable)

For operations the user is explicitly waiting on (a button click, a save), use a variant that surfaces progress in the UI:

```ts
interface RetryProgressOptions {
  maxRetries?: number;
  context?: string;
}

export async function fetchWithProgress<T>(
  fn: () => Promise<ApiResult<T>>,
  options: RetryProgressOptions = {},
): Promise<ApiResult<T>> {
  const { maxRetries = 3, context = 'Loading' } = options;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    const { data, error } = await fn();
    if (!error) return { data, error: null };

    if (attempt < maxRetries && error.message.includes('timeout')) {
      showToast(`${context} is taking longer than expected. Retrying...`, 'info');
      await new Promise(resolve => setTimeout(resolve, 2000));
      continue;
    }
    return { data: null, error };
  }
  // unreachable in practice; satisfy the type checker:
  return { data: null, error: new Error('retry exhausted') };
}
```

This variant only retries `timeout` errors and surfaces a toast each retry. Use it when the user is actively watching the screen.

## Realtime Error Handling

Realtime is the only place errors come through callbacks (or thrown subscriptions) instead of `{ data, error }`.

### Connection-level errors
```ts
const realtime = new VolcanoRealtime({ /* ... */ });

realtime.onError((ctx) => {
  console.error('Connection error:', ctx.message);
  if (ctx.message?.includes('authentication')) {
    refreshTokenAndReconnect();        // token expired
  } else if (ctx.message?.includes('network')) {
    showError('Connection lost. Reconnecting...');
  }
});

realtime.onDisconnect((ctx) => {
  if (!ctx.reconnect) {
    // SDK will NOT auto-reconnect. Handle manually if you want recovery.
    showError('Connection closed.');
  }
});
```

### Subscription-level errors
```ts
const channel = realtime.channel('posts', { type: 'postgres' });
try {
  await channel.subscribe();
} catch (error) {
  console.error('Subscription failed:', (error as Error).message);
  showError('Failed to subscribe to updates.');
}
```

`subscribe()` throws on failure (one of the few SDK methods that does). Wrap it in try/catch.

## Per-Domain Error Catalogs (cross-reference)

Each domain skill includes domain-specific error messages. This skill is the cross-cutting infrastructure; consult the domain skills for the specific message strings to match against:

| Domain | Skill | Common error messages |
|---|---|---|
| Auth | `volcano-auth` | `invalid email or password`, `confirm your email`, `already exists`, `password must`, `rate limit` |
| Database | `volcano-database` | `column does not exist`, `permission denied`, `No active session`, `Database name not set`, `violates unique constraint` |
| Functions | `volcano-functions` | `Function not found`, `timeout`, `rate limit`, `Internal server error` (or business-logic `data.error`) |
| Logs | `volcano-logs` | project-token authentication, invalid cursor, invalid resource or query filters |
| Locks | `volcano-locks` | `lock_held`, `lock_ownership_lost`, `lock_rate_limited` |
| Storage | `volcano-storage` | `No active session`, `Bucket not found`, `File not found`, `File too large`, `permission denied`, `invalid file type` |
| Realtime | `volcano-realtime` | `authentication` (token expired), `network`, opaque WebSocket errors (often CORS — see realtime skill's Browser Origins section) |

When a new error message starts appearing in production logs, add it to the relevant domain skill's catalog and — if it warrants a distinct action — to `handleApiError` here.

## Best Practices

### Always check errors
```ts
// Good
const { data, error } = await volcano.from('posts').select('*');
if (error) {
  handleError(error);
  return;
}
// data is non-null here

// Bad
const { data } = await volcano.from('posts').select('*');
// data could be null
```

### Provide meaningful user-facing messages
Don't surface raw `error.message` to users. Map it through `handleApiError` to a UI-appropriate string. Raw messages may leak schema details ("column `internal_flag` does not exist") or vendor terminology ("RLS policy violation").

### Log the full error for debugging
The dispatcher's `console.error(...)` line is non-negotiable. Production logs need the original error to diagnose; the user just needs the friendly message.

### Handle network issues explicitly
```ts
if (error) {
  if (typeof navigator !== 'undefined' && !navigator.onLine) {
    showError('You appear to be offline. Please check your connection.');
  } else if (error.message.includes('timeout')) {
    showError('Connection is slow. Please try again.');
  } else {
    showError('Something went wrong. Please try again.');
  }
}
```

### Clean up state on error
After an error, clear any stale data so the UI doesn't show partial state mixed with a failure indicator:
```ts
setLoading(true);
setError(null);

const { data, error } = await volcano.from('posts').select('*');

setLoading(false);
if (error) {
  setError(error.message);
  setData(null);    // <-- clear stale data
  return;
}
setData(data);
```
`useApiCall` does this for you automatically.

## Verification Checklist
- A single `handleApiError` (or equivalent) lives next to the UI code (`web/lib/errors.ts` for a `web/` frontend, or the existing shared UI helper path otherwise) and is used everywhere.
- The action enum is small and exhaustive (`redirect_login`, `show_error`, `retry`, `wait`) — no per-component string actions.
- Components use `useApiCall<T>` for fetched data, not bespoke `useState({loading, error, data})`.
- `fetchWithRetry` is wrapped around reads only, OR mutations are designed idempotent.
- `realtime.onError` is wired and discriminates between auth and network failure modes.
- `await channel.subscribe()` is wrapped in try/catch.
- No raw `error.message` leaks to the user UI; all messages are dispatched through `handleApiError`.

## Companion Skills
- `volcano-uiux` — for user-facing progress, error, and retry feedback.
- `volcano-typescript` — for type-safe error handling (`Error`, `ApiResult<T>`, generic shape).
- Domain skills — for the specific error-message strings per-domain.
- `volcano-realtime` — for the WebSocket-specific connection error semantics (Browser Origins/CORS gotcha).
