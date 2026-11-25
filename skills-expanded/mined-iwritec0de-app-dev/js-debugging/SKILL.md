---
name: js-debugging
description: >-
  This skill should be used when the user asks to 'debug a JavaScript error',
  'fix a TypeScript error', 'debug a React component', 'fix a Next.js error',
  'debug an API route', 'fix a hydration error', 'investigate a runtime error',
  or mentions 'JS debugging', 'stack trace', 'React error boundary',
  'hydration mismatch', 'unhandled rejection', 'type error'. Provides systematic
  JavaScript/TypeScript debugging methodology for Next.js applications covering
  runtime errors, type errors, React issues, hydration mismatches, and API failures.
license: MIT
metadata:
  author: Chris Kelley (hello@iwritecode.io)
  version: 1.0.0
---

# JavaScript/TypeScript Debugging Skill for Next.js Applications

Systematic debugging methodology for JavaScript, TypeScript, and Next.js applications. Follows four phases: root cause investigation, pattern analysis, hypothesis testing, and implementation.

---

## Critical Rules

1. **No fixes without root cause.** Never apply a fix unless you understand WHY the error occurs. Guessing wastes time and introduces new bugs.
2. **Read error messages completely.** The full stack trace, including the "Caused by" chain and any nested errors. Do not stop at the first line.
3. **Check BOTH browser console AND server logs.** Next.js runs code on both sides. A client error may originate server-side and vice versa.
4. **One change at a time.** Make a single change, verify the result, then proceed. Batching changes makes it impossible to know what worked.
5. **Always create a failing test before fixing.** If you cannot reproduce it in a test, you do not understand it well enough to fix it.

---

## Phase 1: Root Cause Investigation (JS/TS-Specific)

### Reading JavaScript Stack Traces

Stack traces are read top-to-bottom. The top frame is where the error was thrown; the bottom is where execution began.

```
TypeError: Cannot read properties of undefined (reading 'map')
    at UserList (src/components/UserList.tsx:14:23)    ← Error thrown here
    at renderWithHooks (react-dom.development.js:149)
    at mountIndeterminateComponent (react-dom.development.js:258)
    at beginWork (react-dom.development.js:312)
```

Key steps:
- Look at the **first frame that references YOUR code** (not library code).
- Check the file, line number, and column number. With source maps enabled, these map to your original TypeScript.
- For async stack traces, look for `async` frames and the `... X more frames` sections — these often contain the real origin.

### Checking Browser DevTools Console

Open DevTools (Cmd+Option+I) and check the Console tab:
- Red errors are runtime exceptions
- Yellow warnings often indicate React-specific issues (key prop, deprecated APIs)
- Check the "Preserve log" checkbox to retain errors across navigations
- Filter by "Errors" to cut through noise

### Checking Terminal / Server Logs

Next.js server errors appear in the terminal where `next dev` or `next start` is running:
- Server component errors
- API route errors
- Middleware errors
- Build-time errors

Look for `[next]` prefixed lines and the full error output including any `cause` property.

### Strategic console.log at Component Boundaries

Place logs at the entry point of components to trace data flow:

```typescript
export function UserList({ users }: { users: User[] }) {
  console.log('[UserList] render', { users, type: typeof users, isArray: Array.isArray(users) });

  // If users comes from a parent, trace it there too
  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

Always log the **type** and **shape** of data, not just the value. `undefined` and `null` look the same when logged alone.

### Using the debugger Statement

Drop a `debugger` statement to trigger a breakpoint when DevTools is open:

```typescript
export async function getUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  const data = await response.json();
  debugger; // Execution pauses here — inspect `data` in DevTools
  return data;
}
```

Remove `debugger` statements before committing. Consider a lint rule (`no-debugger`) to catch these.

### TypeScript: Reading tsc Errors

Run `tsc --noEmit` to get the full list of type errors without producing output files:

```bash
pnpm tsc --noEmit
```

Read TypeScript errors from the bottom up. The last line of a TS error is usually the most specific:

```
src/components/UserList.tsx:14:5 - error TS2322: Type 'string' is not assignable to type 'number'.

14     count: userId,
       ~~~~~

  The expected type comes from property 'count' declared here:

    interface Props {
      count: number;
    }
```

The "expected type comes from" section tells you where the constraint originates.

### Using node --inspect for Server-Side Debugging

Start the Next.js dev server with the Node.js inspector:

```bash
NODE_OPTIONS='--inspect' pnpm next dev
```

Then open `chrome://inspect` in Chrome and connect to the Node.js target. You can set breakpoints in server components, API routes, and middleware.

---

## Phase 2: Common Bug Patterns (Next.js Focus)

### Hydration Mismatch

**Symptom:** "Text content does not match server-rendered HTML" or "Hydration failed because the server-rendered HTML didn't match the client."

**Cause:** The HTML rendered on the server differs from what the client renders on first pass.

**Diagnostic:**

```typescript
// BAD: This causes hydration mismatch because Date.now() differs server vs client
export function Timestamp() {
  return <span>{Date.now()}</span>;
}

// GOOD: Use useEffect for client-only values
export function Timestamp() {
  const [time, setTime] = useState<number | null>(null);

  useEffect(() => {
    setTime(Date.now());
  }, []);

  if (time === null) return <span>Loading...</span>;
  return <span>{time}</span>;
}
```

**Common causes and fixes:**
- Browser extensions injecting HTML — test in incognito mode
- `typeof window !== 'undefined'` checks in render — move to `useEffect`
- Dynamic imports that need `ssr: false`:

```typescript
import dynamic from 'next/dynamic';

const MapComponent = dynamic(() => import('./Map'), { ssr: false });
```

### "Cannot read properties of undefined"

**Diagnostic approach:** Trace the undefined value up the call chain.

```typescript
// Error: Cannot read properties of undefined (reading 'email')
// at ProfileCard (src/components/ProfileCard.tsx:8:24)

export function ProfileCard({ user }: { user: User }) {
  // Add a guard and log to find WHERE user becomes undefined
  if (!user) {
    console.error('[ProfileCard] user is undefined — check parent component');
    return null;
  }

  return <div>{user.email}</div>;
}
```

Then check the parent that passes `user` as a prop. The issue is almost always that the data has not loaded yet or an API returned an unexpected shape.

### Unhandled Promise Rejection

**Symptom:** `UnhandledPromiseRejection` or `Unhandled Runtime Error` with an async operation.

**Common causes:**

```typescript
// BAD: Missing await — the error is thrown but nobody catches it
function handleSubmit() {
  saveUser(formData); // Returns a Promise but we don't await it
}

// GOOD: Await and handle the error
async function handleSubmit() {
  try {
    await saveUser(formData);
  } catch (error) {
    console.error('Failed to save user:', error);
    setError('Failed to save. Please try again.');
  }
}
```

```typescript
// BAD: async function passed to useEffect without wrapping
useEffect(async () => {
  const data = await fetchData();
  setData(data);
}, []);

// GOOD: Define async function inside useEffect
useEffect(() => {
  async function load() {
    try {
      const data = await fetchData();
      setData(data);
    } catch (error) {
      console.error('Failed to load data:', error);
    }
  }
  load();
}, []);
```

### React Hook Rules Violation

**Symptom:** "Rendered more hooks than during the previous render" or "Hooks can only be called inside a function component."

**Rule:** Hooks must be called in the same order on every render. No conditionals, no loops, no early returns before hooks.

```typescript
// BAD: Conditional hook
export function UserProfile({ userId }: { userId: string | null }) {
  if (!userId) return <div>No user</div>; // Early return BEFORE hook

  const [user, setUser] = useState<User | null>(null); // Hook after conditional

  // ...
}

// GOOD: Hooks before any conditionals
export function UserProfile({ userId }: { userId: string | null }) {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    if (userId) {
      fetchUser(userId).then(setUser);
    }
  }, [userId]);

  if (!userId) return <div>No user</div>;

  return <div>{user?.name}</div>;
}
```

### Stale Closure

**Symptom:** A callback or effect reads an old value of state or props.

```typescript
// BAD: count is captured at the time the interval is created
export function Counter() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const id = setInterval(() => {
      console.log(count); // Always logs 0
      setCount(count + 1); // Always sets to 1
    }, 1000);
    return () => clearInterval(id);
  }, []); // Empty deps — closure captures initial count

  return <div>{count}</div>;
}

// GOOD: Use functional updater to avoid stale closure
export function Counter() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const id = setInterval(() => {
      setCount((prev) => prev + 1); // Always reads latest value
    }, 1000);
    return () => clearInterval(id);
  }, []);

  return <div>{count}</div>;
}
```

For non-state values, use `useRef` to hold a mutable reference:

```typescript
const callbackRef = useRef(onSave);
callbackRef.current = onSave; // Update on every render

useEffect(() => {
  // callbackRef.current always points to the latest onSave
  callbackRef.current(data);
}, [data]);
```

### Infinite Re-render

**Symptom:** "Maximum update depth exceeded" or the browser freezes.

```typescript
// BAD: setState called during render
export function UserList({ users }: { users: User[] }) {
  const [sorted, setSorted] = useState<User[]>([]);
  setSorted(users.sort()); // Called on every render → infinite loop
  return <ul>{sorted.map((u) => <li key={u.id}>{u.name}</li>)}</ul>;
}

// GOOD: Derive state with useMemo instead of setState
export function UserList({ users }: { users: User[] }) {
  const sorted = useMemo(() => [...users].sort((a, b) => a.name.localeCompare(b.name)), [users]);
  return <ul>{sorted.map((u) => <li key={u.id}>{u.name}</li>)}</ul>;
}
```

```typescript
// BAD: Object literal in deps causes re-run every render
useEffect(() => {
  fetchData({ page: 1, limit: 10 });
}, [{ page: 1, limit: 10 }]); // New object reference every render

// GOOD: Use primitive values or useMemo for deps
const page = 1;
const limit = 10;
useEffect(() => {
  fetchData({ page, limit });
}, [page, limit]);
```

### Module Not Found

**Diagnostic steps:**

1. Check path aliases in `tsconfig.json`:
```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

2. Check if the import is server-only being used in a client component:
```typescript
// This will fail in a client component
import { db } from '@/lib/db'; // Server-only module

// Fix: Move the data fetching to a server component or API route
```

3. Check barrel exports — a barrel file re-exporting a server module can break client bundles:
```typescript
// src/lib/index.ts (barrel)
export { db } from './db';       // Server-only
export { cn } from './utils';    // Works everywhere

// Importing `cn` from the barrel pulls in `db` too → breaks client bundle
// Fix: Import directly from the specific file
import { cn } from '@/lib/utils';
```

### API Route Errors

```typescript
// Common issues in Next.js App Router API routes

// BAD: Not parsing the request body
export async function POST(request: Request) {
  const body = request.body; // This is a ReadableStream, not parsed JSON
  // ...
}

// GOOD: Parse JSON body correctly
export async function POST(request: Request) {
  const body = await request.json();
  // ...
}

// BAD: Returning plain object (App Router requires Response)
export async function GET() {
  return { users: [] }; // Does not work
}

// GOOD: Return a Response or use NextResponse
import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({ users: [] });
}
```

Check auth middleware is not silently blocking requests. Add logging in middleware:

```typescript
// src/middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  console.log('[middleware]', request.method, request.nextUrl.pathname);
  // ...
}
```

### Build vs Runtime Errors

Some errors only appear in production builds. Always test with:

```bash
pnpm next build && pnpm next start
```

**Common causes of build-only errors:**
- Environment variables missing in production (not prefixed with `NEXT_PUBLIC_` for client access)
- Dynamic imports with expressions that cannot be statically analyzed
- Edge runtime incompatibility (Node.js APIs not available):

```typescript
// This fails on Edge runtime
import { readFileSync } from 'fs';

// Check if you're accidentally using Edge runtime:
// export const runtime = 'edge'; ← Remove if you need Node.js APIs
```

### Type Errors

**`as` casting hiding real issues:**

```typescript
// BAD: Casting masks the real problem
const user = apiResponse as User; // What if apiResponse is actually an error?

// GOOD: Validate the shape at runtime
import { z } from 'zod';

const UserSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
});

const result = UserSchema.safeParse(apiResponse);
if (!result.success) {
  console.error('Invalid user data:', result.error.flatten());
  throw new Error('Invalid user data from API');
}
const user = result.data; // Properly typed and validated
```

**strictNullChecks violations:**

```typescript
// Error: Object is possibly 'undefined'
const users = await getUsers();
const firstEmail = users[0].email; // users[0] could be undefined

// Fix: Guard against undefined
const firstEmail = users[0]?.email ?? 'No email';
// Or with explicit check
if (users.length === 0) {
  throw new Error('No users found');
}
const firstEmail = users[0].email; // Safe after length check
```

**Generic inference failures:**

```typescript
// TypeScript cannot infer the generic type
const result = useQuery({ queryKey: ['users'], queryFn: getUsers });
// result.data is unknown

// Fix: Provide the generic explicitly
const result = useQuery<User[]>({ queryKey: ['users'], queryFn: getUsers });
// result.data is User[] | undefined
```

---

## Phase 3: Diagnostic Techniques

### React DevTools

Install the React DevTools browser extension and use these features:

- **Components tab:** Inspect the component tree, view props and state for any component, and identify which component owns a piece of state.
- **Profiler tab:** Record a session, then review which components re-rendered and why.
- **Highlight updates:** Enable "Highlight updates when components render" in DevTools settings to visually see unnecessary re-renders.

### Network Tab

For API debugging, use the browser Network tab:

- Filter by `Fetch/XHR` to see API calls
- Check the **Status** column for non-200 responses
- Click a request to see the full **Request Headers**, **Request Body**, and **Response Body**
- Look for CORS errors: `Access-Control-Allow-Origin` header missing
- Check **Timing** tab to identify slow requests

### React.Profiler for Performance Debugging

Wrap suspect components to measure render times:

```typescript
import { Profiler } from 'react';

function onRender(
  id: string,
  phase: 'mount' | 'update',
  actualDuration: number,
) {
  if (actualDuration > 16) {
    console.warn(`[Profiler] ${id} ${phase} took ${actualDuration.toFixed(2)}ms`);
  }
}

export function App() {
  return (
    <Profiler id="UserDashboard" onRender={onRender}>
      <UserDashboard />
    </Profiler>
  );
}
```

### why-did-you-render for Unnecessary Re-renders

Install and configure to detect avoidable re-renders:

```typescript
// src/wdyr.ts — import this BEFORE React in your entry point
import React from 'react';

if (process.env.NODE_ENV === 'development') {
  const { default: whyDidYouRender } = await import(
    '@welldone-software/why-did-you-render'
  );
  whyDidYouRender(React, {
    trackAllPureComponents: true,
  });
}
```

Then tag specific components:

```typescript
function UserList({ users }: { users: User[] }) {
  // ...
}
UserList.whyDidYouRender = true;
```

### Next.js Specific Diagnostics

**Inspect the build output:**

```bash
ls -la .next/
# Check .next/server/ for server component output
# Check .next/static/ for client bundles
```

**Get environment info:**

```bash
pnpm next info
```

This prints Next.js version, React version, Node.js version, OS, and other relevant environment details useful for bug reports.

### NODE_OPTIONS with Next.js Dev Server

Start the dev server with the Node.js debugger attached:

```bash
NODE_OPTIONS='--inspect' pnpm next dev
```

Open `chrome://inspect` in Chrome, click "Open dedicated DevTools for Node", and you can:
- Set breakpoints in server components and API routes
- Step through middleware execution
- Inspect server-side variables and state

---

## Phase 4: Fix and Verify

### Write a Failing Test First

Before writing any fix, reproduce the bug in a test using Vitest and React Testing Library:

```typescript
// src/components/__tests__/UserList.test.tsx
import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import { UserList } from '../UserList';

describe('UserList', () => {
  it('handles undefined users without crashing', () => {
    // This test should FAIL before the fix and PASS after
    // @ts-expect-error — testing runtime behavior with bad input
    const { container } = render(<UserList users={undefined} />);
    expect(container).toBeTruthy();
  });

  it('renders an empty list when users array is empty', () => {
    render(<UserList users={[]} />);
    expect(screen.queryByRole('listitem')).toBeNull();
  });
});
```

### Fix at the Source, Not the Symptom

```typescript
// BAD: Suppressing the symptom
export function UserList({ users }: { users: User[] }) {
  try {
    return <ul>{users.map((u) => <li key={u.id}>{u.name}</li>)}</ul>;
  } catch {
    return <div>Something went wrong</div>; // Hides the real issue
  }
}

// GOOD: Fix the actual problem — handle the loading/empty state
export function UserList({ users }: { users: User[] }) {
  if (!users || users.length === 0) {
    return <p>No users found.</p>;
  }

  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}
```

### Run Type Checking After Fix

```bash
pnpm tsc --noEmit
```

This ensures your fix does not introduce new type errors. Run this before committing.

### Run the Test Suite

```bash
pnpm vitest run
```

Or for a specific test file:

```bash
pnpm vitest run src/components/__tests__/UserList.test.tsx
```

### Verify in Both Dev and Production Build

Some bugs only appear in production. Always check both:

```bash
# Development
pnpm next dev

# Production build + start
pnpm next build && pnpm next start
```

Common differences:
- Server components are fully streamed in production
- Environment variables behave differently
- CSS modules and Tailwind may purge differently
- Dynamic imports behave differently with code splitting

### If 3+ Fixes Fail, Question the Architecture

If you have attempted three fixes and none resolve the issue, the bug is likely architectural. Stop patching and reassess:
- Is the data flowing through the right components?
- Is state owned at the correct level?
- Should this be a server component instead of client (or vice versa)?
- Is the API contract correct?

---

## The 3-Strike Rule

If three fix attempts fail:

1. **Stop.** Do not attempt a fourth fix.
2. **Document** what you tried and why each attempt failed.
3. **Identify the architectural issue.** The bug is a symptom of a deeper design problem.
4. **Discuss before proceeding.** Present the findings and propose a structural change.

Continuing to apply surface-level fixes to an architectural problem creates technical debt and makes the codebase harder to maintain.

---

## Quick Reference

| Error Message | Likely Cause | Diagnostic Step | Common Fix |
|---|---|---|---|
| `Cannot read properties of undefined (reading 'X')` | Data not loaded yet or wrong shape | Add `console.log` before access, check parent component | Add null check / optional chaining / loading state |
| `Text content does not match server-rendered HTML` | Hydration mismatch | Compare server HTML (view source) with client render | Move client-only logic to `useEffect`, use `dynamic` with `ssr: false` |
| `Rendered more hooks than during the previous render` | Conditional hook or early return before hooks | Check for `if/return` before any hook call | Move all hooks above any conditional returns |
| `Maximum update depth exceeded` | `setState` called during render or infinite `useEffect` loop | Add `console.log` in the component body and `useEffect` | Use `useMemo` for derived state, fix dependency arrays |
| `Unhandled Runtime Error: [async error]` | Missing `await` or unhandled promise rejection | Check for missing `await` keywords, add `.catch()` | Add `try/catch` around async calls, await all promises |
| `Module not found: Can't resolve 'X'` | Wrong import path, server module in client | Check `tsconfig.json` paths, check `'use client'` boundary | Fix import path, move server imports to server components |
| `Type 'X' is not assignable to type 'Y'` | TypeScript type mismatch | Run `pnpm tsc --noEmit`, read full error chain | Fix the type at its source, avoid `as` casting |
| `Objects are not valid as a React child` | Rendering an object/array directly instead of JSX | `console.log` the value being rendered | Map arrays to JSX, stringify objects, extract primitive values |
| `CORS error` / `NetworkError` | API request blocked by browser CORS policy | Check Network tab for preflight OPTIONS request | Add CORS headers in API route or Next.js config `headers()` |
| `NEXT_PUBLIC_ env var undefined` | Env var not prefixed for client access | Check `.env.local` and variable naming | Prefix with `NEXT_PUBLIC_` for client-side access |
