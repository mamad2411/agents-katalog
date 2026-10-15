---
name: nextjs-swr-hooks
description: >
  Enforces hook development conventions for Next.js projects using SWR (stale-while-revalidate):
  file structure, fetcher patterns, key factories, SSR fallback, typing, and anti-pattern prevention.
  Use when creating, modifying, or reviewing custom React hooks with SWR in a Next.js project,
  or when user mentions "swr", "useSWR", "stale while revalidate", "swr hook",
  "swr mutation", "useSWRMutation", "swr infinite", "swr middleware".
  Do NOT use for TanStack Query projects — use nextjs-tanstack-hooks instead.
  Do NOT use for non-Next.js projects — use react-swr-hooks instead.
  Do NOT use for client state management (Zustand, Redux, Recoil, Jotai).
license: MIT
metadata:
  author: amunozdev
  version: "1.0.0"
---

## Purpose

You enforce hook development standards for Next.js projects using SWR. Every custom hook in `src/hooks/` MUST follow these rules. Apply them when creating new hooks, modifying existing ones, or reviewing hook code. Target SWR 2.x APIs (`useSWR`, `useSWRMutation`, `useSWRInfinite`).

**Scope: server state only** — data fetching, caching, revalidation, and mutations via SWR. This skill does NOT cover client state management (Zustand, Redux, Recoil, Jotai).

This skill is specifically for **Next.js App Router** projects where:
- Server Components handle initial data fetching
- Client Components use SWR hooks for client-side caching, revalidation, and mutations
- The `'use client'` directive separates server and client boundaries
- The `src/` directory and `@/` import alias are standard conventions

## When to Run

- Creating a new hook in `src/hooks/`
- Modifying an existing hook
- Reviewing hook code for quality
- Migrating legacy hooks to the correct pattern
- Adding SSR fallback data to pages using SWR
- Setting up SWR configuration or middleware

## File Structure

Every hook MUST live in its own directory with this exact layout:

```
src/hooks/
└── use-hook-name/
    ├── index.ts                    # Barrel export (named, never export *)
    ├── use-hook-name.ts            # Implementation
    ├── use-hook-name.types.ts      # Types (when needed, never inline complex types)
    └── use-hook-name.test.ts       # Co-located test
```

### Rules

1. **Directory name** = kebab-case, matches the hook name: `use-favorite-toggle/`. _Why: consistent naming enables predictable imports and automated tooling._
2. **No standalone files** — every hook gets a directory, even simple ones. _Why: uniform structure makes it trivial to add types, tests, or co-located files later without restructuring._
3. **No `export *`** in barrel — use explicit named exports. _Why: explicit exports enable tree-shaking and make the public API visible at a glance._

```typescript
// index.ts — CORRECT
export { useFavoriteToggle } from './use-favorite-toggle';
export type {
  ToggleFavoriteRequest,
  ToggleFavoriteResponse,
  UseFavoriteToggleReturn,
} from './use-favorite-toggle.types';
```

```typescript
// index.ts — WRONG
export * from './use-favorite-toggle';
```

4. **Types file** — create `use-hook-name.types.ts` when you have interfaces for params, responses, or return types. Keep types inline only for trivial cases (1-2 simple types).
5. **`'use client'` directive** — REQUIRED as the first line of every hook file that uses SWR or any React hooks (`useState`, `useEffect`, `useReducer`, `useRef`, `useSWR`, `useSWRMutation`, `useActionState`, etc.). Server Components cannot use hooks — the directive marks the client boundary.

## Data Fetching — SWR (MANDATORY)

**NEVER use manual `fetch()` + `useState` + `useEffect` for data fetching.** Always use SWR. The core pattern is `useSWR(key, fetcher, options)`. Use `useSWRMutation` for mutations (POST, PUT, DELETE) and `useSWRInfinite` for paginated or infinite-scroll data. Define reusable fetcher functions in `@/lib/fetchers/` and pass them to SWR hooks or configure a default fetcher via `SWRConfig`.

For full templates (query, mutation, infinite loading, optimistic updates), loading state guide, conditional fetching, polling, and revalidation patterns, see **[references/swr-patterns.md](references/swr-patterns.md)**.

## Key Factory — `swrKeys` (MANDATORY)

All SWR keys MUST come from the factory in `@/lib/swr-keys.ts`. **NEVER hardcode key arrays.** _Why: centralized keys prevent cache collisions and make invalidation patterns discoverable._

```typescript
// CORRECT
useSWR(swrKeys.favorites.status(itemId), fetcher)

// WRONG — hardcoded key
useSWR(['favorites', 'status', itemId], fetcher)
```

### Factory Example

```typescript
// @/lib/swr-keys.ts
export const swrKeys = {
  favorites: {
    all: ['favorites'] as const,
    status: (itemId: string) => ['favorites', 'status', itemId] as const,
  },
  user: {
    list: () => ['user', 'list'] as const,
    profile: (userId: string) => ['user', 'profile', userId] as const,
  },
  products: {
    all: ['products'] as const,
    detail: (productId: string) => ['products', 'detail', productId] as const,
  },
} as const;
```

### Conditional Fetching

Pass `null` as the key to disable fetching. SWR will not fire the request until the key is non-null:

```typescript
useSWR(userId ? swrKeys.user.profile(userId) : null, fetcher)
```

### Cache Invalidation Strategies

| Action | Code |
|--------|------|
| Revalidate one key | `mutate(swrKeys.user.profile(id))` |
| Revalidate with new data | `mutate(key, newData, { revalidate: false })` |
| Revalidate matching keys | `mutate((key) => Array.isArray(key) && key[0] === 'favorites')` |
| Bound mutate (from hook) | `const { mutate } = useSWR(key, fetcher)` |

**WARNING:** Never call `mutate` inside `useEffect` based on data changes — this creates revalidation loops. Use SWR's `onSuccess` callback or event handlers instead.

## Global Configuration — SWRConfig

Centralize default SWR options in `@/lib/swr-config.ts`. Never scatter configuration across individual hooks.

```typescript
// @/lib/swr-config.ts
export const SWR_CONFIG = {
  dedupingInterval: 2000,
  revalidateOnFocus: true,
  revalidateOnReconnect: true,
  errorRetryCount: 3,
} as const;
```

Wrap your app layout with `SWRConfig` to apply defaults and a global fetcher:

```typescript
// @/app/providers.tsx
'use client';
import { SWRConfig } from 'swr';
import { SWR_CONFIG } from '@/lib/swr-config';
import { defaultFetcher } from '@/lib/fetchers/default-fetcher';

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <SWRConfig value={{ ...SWR_CONFIG, fetcher: defaultFetcher }}>
      {children}
    </SWRConfig>
  );
}
```

## SSR Fallback Pattern

This is the key Next.js integration pattern. SWR's `fallback` option allows Server Components to pre-fetch data and pass it to client components, eliminating loading states on initial render.

### How It Works

1. **Server Component** fetches data at request time (or via `generateStaticParams`)
2. **Server Component** passes data as `fallback` to a nested `SWRConfig`
3. **Client Components** using `useSWR` with matching keys receive instant data — no loading spinner

### Server Component (fetches and provides fallback)

```tsx
// app/users/page.tsx (Server Component — no 'use client')
import { SWRConfig, unstable_serialize } from 'swr';
import { swrKeys } from '@/lib/swr-keys';
import { UserList } from './user-list';

async function fetchUsers() {
  const res = await fetch('https://api.example.com/users', { next: { revalidate: 60 } });
  return res.json();
}

export default async function UsersPage() {
  const users = await fetchUsers();
  return (
    <SWRConfig value={{ fallback: { [unstable_serialize(swrKeys.user.list())]: users } }}>
      <UserList />
    </SWRConfig>
  );
}
```

### Client Component (consumes fallback via useSWR)

```tsx
// app/users/user-list.tsx (Client Component)
'use client';
import useSWR from 'swr';
import { swrKeys } from '@/lib/swr-keys';

export function UserList() {
  const { data: users } = useSWR(swrKeys.user.list());
  // `users` is immediately available from fallback — no loading state on first render
  // SWR still revalidates in the background to keep data fresh
  return <ul>{users?.map((u) => <li key={u.id}>{u.name}</li>)}</ul>;
}
```

Use `unstable_serialize` from `swr` to convert array keys to the string format SWR uses internally. This ensures the fallback key matches the key used by `useSWR` in client components.

For the full SSR fallback pattern with error handling, nested fallbacks, and dynamic routes, see **[references/swr-patterns.md](references/swr-patterns.md)**.

## React 19 & React Compiler

Next.js has React Compiler support. If enabled, **do NOT write** manual `useMemo` or `useCallback` in new hooks — the compiler handles memoization at build time. _Why: manual memos add noise and can conflict with compiler optimizations._

Use React 19 hooks where appropriate:
- `useActionState` + `useFormStatus` for Server Action forms
- `useOptimistic` for optimistic UI updates (complements SWR's optimistic mutation pattern)
- `use()` for reading promises and context in render

For `useActionState` and `useOptimistic` templates, `use()` rules, and compiler edge cases, see **[references/react19-and-compiler.md](references/react19-and-compiler.md)**.

## Hook Composition

Hooks can (and should) compose other hooks from `@/hooks/`:

```typescript
export function useEditProfileForm(): UseEditProfileFormReturn {
  const { user } = useAuth();
  const { data: profile, isLoading: isProfileLoading } = useSWR(
    user?.id ? swrKeys.user.profile(user.id) : null,
    fetcher,
  );
  const { trigger: updateProfile, isMutating } = useSWRMutation(
    swrKeys.user.profile(user?.id ?? ''),
    updateProfileFetcher,
  );

  // Derive state, combine loading flags, etc.
}
```

Rules:
- Call hooks in consistent order (React rules of hooks)
- Pass derived values between hooks
- Keep composed hooks under 300 lines; if too large, split the composition
- Each sub-hook should handle one concern (auth, data, mutation)

### State Machines with `useReducer`

For multi-step flows (transfers, wizards), use a typed reducer as a state machine. Define discriminated union types for state and actions, then a pure `flowReducer` function with `switch` on `action.type`. Typed transitions prevent invalid state combinations. The reducer is a pure function — test it directly without `renderHook`.

```typescript
type FlowState =
  | { step: 'idle' }
  | { step: 'confirm'; recipientId: string }
  | { step: 'submitting'; recipientId: string }
  | { step: 'success'; txHash: string }
  | { step: 'error'; error: Error };

type FlowAction =
  | { type: 'START'; recipientId: string }
  | { type: 'SUBMIT' }
  | { type: 'SUCCESS'; txHash: string }
  | { type: 'FAIL'; error: Error }
  | { type: 'RESET' };

function flowReducer(state: FlowState, action: FlowAction): FlowState { /* switch on action.type */ }
```

## Types Conventions

```typescript
// use-hook-name.types.ts

export interface UseHookNameParams {
  id: string;
  enabled?: boolean;
}

export interface HookNameResponse {
  success: boolean;
  data: SomeData;
  error?: string;
}

export interface UseHookNameReturn {
  data: SomeData | null;
  isLoading: boolean;
  error: string | null;
}
```

### Discriminated Unions for Complex Return Types

When a hook has distinct states, use discriminated unions instead of nullable fields. TypeScript narrows correctly at call site:

```typescript
type UseItemResult =
  | { status: 'loading' }
  | { status: 'success'; data: Item }
  | { status: 'error'; error: Error };
```

### Tuple Returns with `as const`

For hooks returning `[value, setter]` pairs, use `as const` to preserve tuple types instead of `(T | Function)[]`:

```typescript
return [value, toggle] as const; // infers [boolean, () => void]
```

### Rules

- **No `any`** — strict TypeScript, always
- **Explicit return type** on the hook function signature
- **Separate types file** for hooks with 3+ interfaces
- **Import with `type`** keyword: `import type { ... } from './use-hook-name.types'`
- **Don't define unused types** — if an interface/type isn't imported anywhere, delete it

## Hook Size & Responsibility

| Guideline | Limit |
|-----------|-------|
| Max lines per hook | ~300 lines |
| Single responsibility | One concern per hook |
| Max `useEffect` per hook | 2 (prefer 0-1) |

If a hook exceeds 300 lines or handles multiple concerns, split it:
- Data fetching -> separate SWR hook
- Filter/form state -> separate state hook
- UI behavior -> separate UI hook
- Compose them in a parent hook or component if needed

## Testing

Use `renderHook` from `@testing-library/react` wrapped with `SWRConfig` configured with `{ dedupingInterval: 0, provider: () => new Map() }` to isolate cache between tests. Test reducers as pure functions without `renderHook`.

For full testing templates and patterns, see **[references/testing-hooks.md](references/testing-hooks.md)**.

## Shared Utilities — Don't Duplicate

Before writing mapping functions, type converters, or helpers inside a hook:

1. Check `@/lib/utils/` for existing utilities
2. Check other hooks for the same function (e.g., `itemToGridItem` exists in 6 hooks — it should be in `@/lib/utils/`)
3. If the function is used by 2+ hooks, extract it to `@/lib/utils/`
4. Shared interfaces used across hooks go in `@/types/`, not duplicated in each hook's types file

## Anti-Patterns & Verification

Before finishing any hook, check for common anti-patterns (setState during render, useEffect for fetching, manual memoization, hardcoded SWR keys, string-based error matching) and run through the verification checklist covering structure, directives, types, and build.

For the full anti-patterns table and verification checklist, see **[references/anti-patterns-checklist.md](references/anti-patterns-checklist.md)**.

## Examples

### Example 1: "Create a hook for fetching user profile"

Claude creates:
- `src/hooks/use-user-profile/` directory with `index.ts`, `use-user-profile.ts`, and `use-user-profile.types.ts`
- Hook file starts with `'use client'` directive
- Uses `useSWR(swrKeys.user.profile(userId), fetcher)` with `dedupingInterval` from `@/lib/swr-config`
- Adds query key `swrKeys.user.profile(userId)` to `@/lib/swr-keys.ts`
- Conditional fetching with `userId ? swrKeys.user.profile(userId) : null` when userId may be undefined
- Types file defines `UseUserProfileParams`, `UserProfileResponse`, and `UseUserProfileReturn`

### Example 2: "Add SSR fallback for product page"

Claude creates:
- Server Component at `app/products/[id]/page.tsx` that fetches product data
- Uses `SWRConfig` with `fallback: { [unstable_serialize(swrKeys.products.detail(id))]: product }` to pass data to client
- Client Component at `app/products/[id]/product-detail.tsx` with `'use client'` directive
- Client component uses `useSWR(swrKeys.products.detail(id))` — data is instantly available from fallback, no loading state
- SWR revalidates in the background to keep data fresh after initial render

### Example 3: "This hook has useState + useEffect for fetching, fix it"

Claude:
- Identifies the `useState` + `useEffect` + `fetch()` anti-pattern
- Refactors to use `useSWR` with a centralized fetcher from `@/lib/fetchers/`
- Adds `'use client'` directive if missing
- Removes manual loading/error state management (replaced by SWR's `isLoading`, `error`)
- Adds key to `swrKeys` factory in `@/lib/swr-keys.ts` (never hardcoded)
- Verifies against the anti-patterns checklist in `references/anti-patterns-checklist.md`
