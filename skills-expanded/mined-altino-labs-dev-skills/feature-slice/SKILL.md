---
name: feature-slice
description: >
  Frontend organization and implementation patterns.
  Invoke automatically when creating screens, components, data hooks,
  Zustand stores, or any frontend artifact (mobile or web).
---

# Feature Slice

## Platforms

- **Mobile:** React Native + Expo — `apps/mobile/` (can also run on web via react-native-web — see `react-native-web`)
- **Web:** Next.js — `apps/web/` (or whatever the project names its web app)

The folder structure is **identical** between both platforms.
Only UI components and navigation differ — logic is 100% portable.

> Sub-files: `expo-web-setup.md` (pnpm monorepo + Metro + Expo Web configuration, condensed)
> and `date-time.md` (date inputs, timezone-safe queries/grouping, condensed). The sections
> below are the full versions.

---

## What is portable vs what is not

| Layer | Portable? | Where it lives |
|---|---|---|
| DTOs, enums, API types | Yes — 100% | `packages/shared-types` |
| Pure functions (dates, formatting) | Yes — 100% | `packages/utils` |
| Design tokens (colors, spacing) | Yes | `packages/ui` |
| React Query hooks (`api/`) | Yes — same API | `features/*/api/` |
| Zustand stores (`store/`) | Yes — same API | `features/*/store/` |
| UI components | No | Inside `apps/*/` |
| Navigation and layout | No | Inside `apps/*/` |

`packages/utils` → **zero imports of React, React Native, DOM, or any framework.**

---

## Feature structure

```
features/<feature>/
├── api/              ← React Query hooks (portable)
│   ├── use-<feature>-query.ts
│   └── use-<feature>-mutation.ts
├── components/       ← platform-specific UI
│   ├── <feature>-card.tsx
│   └── <feature>-form.tsx
└── store/            ← local Zustand state (portable)
    └── <feature>.store.ts
```

---

## React Query hook pattern

```typescript
// features/orders/api/use-resource-list-query.ts
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/shared/services/api-client';
import type { OrderListResponse } from '@your-app/shared-types';

export function useOrderListQuery(userId: string) {
  return useQuery({
    queryKey: ['orders', 'list', userId],
    queryFn: () =>
      apiClient.get<OrderListResponse>(`/api/v1/orders`),
    enabled: !!userId,
    staleTime: 1000 * 60 * 2,
  });
}
```

---

## Zustand store pattern

```typescript
// features/resources/store/active-resource.store.ts
import { create } from 'zustand';
import type { ResourceResponse } from '@your-app/shared-types';

interface ActiveResourceState {
  activeResource: ResourceResponse | null;
  setActiveResource: (resource: ResourceResponse) => void;
  clearActiveResource: () => void;
}

export const useActiveResourceStore = create<ActiveResourceState>((set) => ({
  activeResource: null,
  setActiveResource: (resource) => set({ activeResource: resource }),
  clearActiveResource: () => set({ activeResource: null }),
}));
```

The global auth store lives in `shared/store/auth.store.ts`.
Feature stores live in `features/*/store/`.

---

## Shared HTTP client

Every app has a single shared HTTP client module (e.g. `src/lib/api-client.ts`). Key behaviors:

1. **Always attach `statusCode` and `code`** to every thrown error — via an `apiError(...)` helper that reads the
   standard error envelope `{ error: { code, message, details } }` (`dev-core:error-handling`).  
   The component's `catch` can then use `e.statusCode` / `e.code` (the stable machine code, e.g. `ENTITY_NOT_FOUND`)
   to tell errors apart without parsing `e.message`.

2. **Automatic token refresh** — on a 401, try to refresh the token before retrying.  
   A `skipRefresh = true` parameter disables this for public endpoints (login, register).  
   **Rule:** always pass `skipRefresh: true` for endpoints that don't require authentication — otherwise a 401 caused by wrong credentials triggers a pointless refresh attempt.

3. **Network error** (`fetch` fails before getting a response) → throws `TypeError`. Detect it with `e instanceof TypeError`, not with `!e.statusCode`.

```typescript
// src/lib/api-client.ts
export type ApiError = Error & { statusCode: number; code: string; details?: unknown };

function apiError(statusCode: number, code: string, message: string, details?: unknown): ApiError {
  const err = new Error(message) as ApiError;
  err.statusCode = statusCode;
  err.code = code;           // stable machine code from the API — branch on this, not on message
  err.details = details;     // e.g. validation errors: [{ field, message }]
  return err;
}

export async function apiRequest<T>(
  path: string,
  options: RequestInit = {},
  skipRefresh = false      // ← true for login, register and other public endpoints
): Promise<T> {
  // ... does the fetch, tries refresh on 401 if !skipRefresh ...
  if (!res.ok) {
    // Error envelope (dev-core:error-handling): { error: { code, message, details } }
    const body = await res.json().catch(() => null);
    throw apiError(
      res.status,
      body?.error?.code ?? 'UNKNOWN_ERROR',
      body?.error?.message ?? res.statusText,
      body?.error?.details,
    );
  }
  // ...
}
```

**Catch pattern in forms:**

```typescript
} catch (e: any) {
  if (e instanceof TypeError) {
    // fetch never reached the server — no internet or server down
    setError('Cannot reach the server. Check your connection.');
  } else if (e?.statusCode === 401 || e?.statusCode === 403) {
    setError('Invalid credentials.');            // context-specific message
  } else if (e?.code === 'OPTIMISTIC_LOCK_CONFLICT') {
    setError('Someone else changed this record. Reload and try again.');   // branch on the API code
  } else if (e?.statusCode === 409) {
    setError('This record already exists.');     // same
  } else {
    setError('Unexpected error. Please try again.');
  }
}
```

**Never show `e.message` directly to the user** — it is the API's developer-facing message (and `e.code` is a
machine code like `ENTITY_NOT_FOUND`), not a sentence written for users in the app's language. Map
`e.code` / `e.statusCode` to user-facing strings in the app's UI language.

---

## Mandatory configuration — Expo Web in pnpm monorepo

Apply **all** items below when creating `apps/mobile`. Any missing item causes bundling failure on web.

### 1. pnpm workspace configuration (monorepo root)

**No public hoisting needed.** pnpm 11+ no longer reads `shamefully-hoist` from `.npmrc`
(`pnpm config get shamefully-hoist` → `undefined`), so a `.npmrc` with that line is dead config.
Metro finds transitive dependencies through `resolver.nodeModulesPaths` pointing at pnpm's
internal store (`node_modules/.pnpm/node_modules`) — see `metro.config.js` below. Don't turn on
`shamefullyHoist`/`publicHoistPattern` in `pnpm-workspace.yaml` unless a concrete package fails
to resolve: it reshapes the whole `node_modules` tree.

**`pnpm-workspace.yaml`** — pnpm 11+ blocks build scripts for security.
Add `allowBuilds` for packages that need postinstall:
```yaml
packages:
  - 'apps/*'
  - 'packages/*'
allowBuilds:
  '@nestjs/core': true
  esbuild: true
```

The `pnpm` field in `package.json` was deprecated in pnpm 11 — do not use it to configure builds.
Without `allowBuilds`, pnpm prints `[ERR_PNPM_IGNORED_BUILDS]` and postinstall scripts do not run.
Decide each new entry explicitly — `true` only when the package really needs its script
(native bindings, binary download); `false` for telemetry (e.g. `@scarf/scarf` from swagger-ui)
and optional watchers. pnpm writes placeholders (`'pkg': set this to true or false`) into the
file when it meets a new one — replace them, never commit them.

**pnpm 11 `minimumReleaseAge` — supply-chain protection, keep it on.** pnpm refuses versions
published too recently (observed cutoff: 24 h, pnpm 11.5) so a compromised release has time to be caught. Rules:
- **Treat `minimumReleaseAgeExclude` as a reviewed exception** — add one only per the project's
  policy (recommended: with explicit human approval). pnpm may write one on its own during an
  install (e.g. for a 1-hour-old `vite`) — always review `git diff pnpm-workspace.yaml` after installing.
- Pick the previous mature version instead (`"vite": "^8.3.3"` while 8.3.4 is too young).
- If the lockfile (or the hidden `node_modules/.pnpm/lock.yaml`) already holds the too-young
  version, `pnpm install` fails with `ERR_PNPM_MINIMUM_RELEASE_AGE_VIOLATION` even after editing
  `package.json`. Fix: `pnpm clean --lockfile` (it deletes `node_modules` and the lockfile — recommended
  as a separate, clearly-described step), then `pnpm install`, then re-run every check: the whole graph was re-resolved.

### 2. `package.json` — required versions

```json
{
  "main": "expo-router/entry",
  "dependencies": {
    "react":     "19.1.0",
    "react-dom": "19.1.0",
    "react-native-web": "~0.21.2",
    "zustand": "^4.5.5"
  },
  "devDependencies": {
    "babel-plugin-transform-import-meta": "*"
  }
}
```

Versions shown are examples — the exact `react` / `react-dom` / `react-native-web` versions are
dictated by the installed Expo SDK (`npx expo install --fix` sets them).

**Critical rules:**
- `react` and `react-dom` **same exact version without `^`** — different versions cause fatal crash
- `zustand`: use **v4** (`^4.5.5`) — v5 has `import.meta` in `.mjs` files that breaks Hermes
- `date-fns`: use **v3** (`^3.6.0`) — v4 is ESM-only with `import.meta`

### 3. `babel.config.js` — required

```javascript
module.exports = function (api) {
  api.cache(true);
  return {
    presets: [
      [
        'babel-preset-expo',
        {
          // Transforms import.meta present in .mjs files from packages like zustand v4
          // without breaking Metro's module resolution
          unstable_transformImportMeta: true,
        },
      ],
    ],
  };
};
```

**DO NOT use `unstable_conditionNames` in metro.config** — this breaks resolution of
`"main": "expo-router/entry"` and Metro falls back to `expo/AppEntry.js`, causing a white screen.

### 4. `metro.config.js` — required

```javascript
const { getDefaultConfig } = require('expo/metro-config');
const path = require('path');

const projectRoot = __dirname;
const workspaceRoot = path.resolve(projectRoot, '../..');

const config = getDefaultConfig(projectRoot);

config.watchFolders = [workspaceRoot];

config.resolver.nodeModulesPaths = [
  path.resolve(projectRoot, 'node_modules'),
  path.resolve(workspaceRoot, 'node_modules'),
  // pnpm's internal store — this is what lets Metro resolve transitive deps
  // (e.g. expo-router → react) without public hoisting
  path.resolve(workspaceRoot, 'node_modules', '.pnpm', 'node_modules'),
];

// Resolve local workspace packages directly from src/
// Avoids needing to build packages before running the app
// Replace @your-app/* with your actual package scope (e.g. @my-app/*, @acme/*)
config.resolver.extraNodeModules = {
  '@your-app/shared-types': path.resolve(workspaceRoot, 'packages/shared-types/src'),
  '@your-app/utils': path.resolve(workspaceRoot, 'packages/utils/src'),
};

// Pin React sub-paths — Metro can't resolve react/jsx-dev-runtime from inside the pnpm virtual store
const reactPath = path.resolve(projectRoot, 'node_modules', 'react');
config.resolver.resolveRequest = (context, moduleName, platform) => {
  const PINNED = {
    'react':                 path.join(reactPath, 'index.js'),
    'react/jsx-runtime':     path.join(reactPath, 'jsx-runtime.js'),
    'react/jsx-dev-runtime': path.join(reactPath, 'jsx-dev-runtime.js'),
  };
  if (PINNED[moduleName]) return { filePath: PINNED[moduleName], type: 'sourceFile' };
  return context.resolveRequest(context, moduleName, platform);
};

// Allows require.context so Expo Router can discover routes automatically
config.transformer.unstable_allowRequireContext = true;

// Force Babel to transform zustand (uses import.meta in .mjs even in v4)
// Without this, unstable_transformImportMeta from babel-preset-expo does not reach node_modules
config.transformer.transformIgnorePatterns = [
  'node_modules/(?!(zustand|@your-app)/)',
];

module.exports = config;
```

### 5. `app.json` — include `web` in platforms

```json
{
  "expo": {
    "platforms": ["ios", "android", "web"],
    "web": { "bundler": "metro", "output": "single" },
    "plugins": ["expo-router"],
    "experiments": { "typedRoutes": true }
  }
}
```

### 6. Required explicit dependencies

pnpm does not hoist transitive dependencies automatically. Declare in `package.json`:

```json
{
  "dependencies": {
    "@babel/runtime": "*",
    "expo-constants": "<SDK-matched version>",
    "expo-linking": "<SDK-matched version>",
    "react-native-safe-area-context": "*",
    "react-native-screens": "*",
    "@react-native-async-storage/async-storage": "*"
  }
}
```

**`@babel/runtime` required and explicit** — pnpm does not guarantee hoisting it into Metro's
context, causing `Unable to resolve module @babel/runtime/helpers/interopRequireDefault`.

**Rule:** any package with native iOS/Android code that is a transitive dep of `expo-router`
(e.g. `expo-constants`, `expo-linking`) MUST be explicitly declared in `package.json` for
CocoaPods to include it. Let `npx expo install <pkg>` pick the SDK-matched version.

### 7. `.pnpm` URL issue in Expo Web — proxy required

> **pnpm version matters:** pnpm < v11 generates **relative** paths that the browser normalizes to a form Metro cannot serve → rewriting proxy needed. pnpm v11+ generates **absolute** paths Metro can serve directly → transparent proxy (no rewriting). See end of this section.

Metro, in a pnpm monorepo, resolves symlinks to physical paths and generates in the HTML:
```html
<script src="/../../node_modules/.pnpm/expo-router@.../entry.bundle?...">
```
The browser normalizes to `/node_modules/.pnpm/...`, which Metro cannot serve (404 → MIME type error → white screen).

**Solution (pnpm < v11): HTTP proxy that rewrites the HTML before it reaches the browser.**

Create `apps/mobile/web-proxy.js`:

```javascript
// web-proxy.js — rewrites .pnpm URLs in Metro's HTML
const http = require('http');
const METRO_PORT = parseInt(process.argv[2] || '8082', 10);
const PROXY_PORT = parseInt(process.argv[3] || '8081', 10);
const PNPM_RE = /src="(\/(?:\.\.\/)*node_modules\/\.pnpm\/[^"]*expo-router[^"]*\/node_modules\/expo-router\/entry\.bundle[^"]*)"/g;

http.createServer((req, res) => {
  const opts = { hostname: 'localhost', port: METRO_PORT, path: req.url, method: req.method,
                 headers: { ...req.headers, host: `localhost:${METRO_PORT}` } };
  http.request(opts, (pr) => {
    const isHtml = (pr.headers['content-type'] || '').includes('text/html');
    if (isHtml) {
      const chunks = [];
      pr.on('data', c => chunks.push(c));
      pr.on('end', () => {
        const body = Buffer.concat(chunks).toString('utf8');
        const fixed = body.replace(PNPM_RE, (_, url) => {
          const qs = url.indexOf('?') >= 0 ? url.slice(url.indexOf('?')) : '';
          return `src="/node_modules/expo-router/entry.bundle${qs}"`;
        });
        const buf = Buffer.from(fixed, 'utf8');
        const hdrs = { ...pr.headers, 'content-length': buf.length };
        delete hdrs['transfer-encoding'];
        res.writeHead(pr.statusCode, hdrs);
        res.end(buf);
      });
    } else {
      res.writeHead(pr.statusCode, pr.headers);
      pr.pipe(res);
    }
  }).on('error', e => { res.writeHead(502); res.end(e.message); })
    .end(req.read());
}).listen(PROXY_PORT, () => console.log(`Proxy: http://localhost:${PROXY_PORT} → Metro: ${METRO_PORT}`));
```

**Scripts in `package.json`:**

```json
{
  "scripts": {
    "web":       "expo start --web --port 8082 --clear",
    "web:proxy": "node web-proxy.js 8082 8081"
  }
}
```

**Usage:**
```bash
# Terminal 1
cd apps/mobile && pnpm web

# Terminal 2
cd apps/mobile && pnpm web:proxy

# Access: http://localhost:8081 (not 8082)
```

**Tokens:** `expo-secure-store` (Keychain/Keystore) on iOS/Android; AsyncStorage only as the
web fallback, because SecureStore has no web implementation — web is treated as a
lower-security context. See `dev-patterns:auth-security` → `frontend-auth.md`.

**pnpm v11+ (Expo SDK 53+, expo-router v5) — transparent proxy:**

With pnpm v11+, Metro generates **absolute** `.pnpm` paths that it can serve at HTTP 200. A rewriting proxy would break things (Metro returns 404 for the rewritten clean path). Use a transparent proxy instead:

```javascript
// web-proxy.js — transparent proxy for pnpm v11+
const http = require('http');
const METRO_PORT = parseInt(process.argv[2] || '8082', 10);
const PROXY_PORT = parseInt(process.argv[3] || '8081', 10);
http.createServer((req, res) => {
  http.request(
    { hostname: 'localhost', port: METRO_PORT, path: req.url, method: req.method,
      headers: { ...req.headers, host: `localhost:${METRO_PORT}` } },
    (pr) => { res.writeHead(pr.statusCode, pr.headers); pr.pipe(res); }
  ).on('error', e => { res.writeHead(502); res.end(e.message); }).end(req.read());
}).listen(PROXY_PORT, () => console.log(`Proxy: http://localhost:${PROXY_PORT} → Metro: ${METRO_PORT}`));
```

**Rule:** check your pnpm version before picking a proxy strategy. `pnpm --version` → v11+ = transparent; < v11 = rewriting.

### iOS Simulator alongside web — single Metro rule

**NEVER run two separate Metro instances** (one `--web`, one `--ios` on different ports).
When Expo Go loses connection and reconnects, it can pick up the wrong Metro and show:
`[runtime not ready]: React Native version mismatch — JS: <project RN>, Native: <other RN>`

**Correct pattern — one Metro serving both:**
```bash
# Terminal 1: single Metro, --ios flag ensures correct Expo Go SDK version is installed
cd apps/mobile && EXPO_ROUTER_APP_ROOT=app npx expo start --ios --port 8082 --clear

# Terminal 2: transparent proxy for the browser
node apps/mobile/web-proxy.js 8082 8081
```

- `--ios` (not `--web`): makes the Expo CLI install the Expo Go version that matches the project SDK. Without this, a stale wrong-version Expo Go stays on the simulator and Cmd+R triggers the mismatch.
- Same Metro at 8082 serves web (via proxy) and iOS at the same time — no port conflicts.
- If mismatch appears anyway: `xcrun simctl uninstall booted host.exp.Exponent`, then restart Metro with `--ios --clear`.

---

## Mobile app setup order

```bash
# 1. Create files (package.json, app.json, tsconfig, babel.config.js, metro.config.js)

# 2. Install dependencies
pnpm install

# 3. Fix package versions for compatibility with the installed Expo SDK
#    (this command reads the installed expo and adjusts all versions)
cd apps/mobile && npx expo install --fix

# 4. Start (web + iOS) — ALWAYS from apps/mobile, NEVER from monorepo root
#    Use --ios so Expo CLI installs the correct Expo Go SDK version (avoids version mismatch on Cmd+R)
cd apps/mobile && EXPO_ROUTER_APP_ROOT=app npx expo start --ios --port 8082 --clear
node web-proxy.js 8082 8081   # web at http://localhost:8081

# --clear is REQUIRED after any change to babel.config.js or metro.config.js
# Without --clear, Metro reuses corrupted cache
```

**Critical point:** if `expo start` shows "Starting project at /...monorepo-root" instead of
"Starting project at /.../apps/mobile", Metro loads the wrong project (expo/AppEntry.js)
and the screen stays white. Always confirm the CWD before starting.

---

## Naming conventions

| Artifact | Convention | Example |
|---|---|---|
| Query hook | `use-<feature>-query.ts` | `use-resource-list-query.ts` |
| Mutation hook | `use-<feature>-mutation.ts` | `use-create-resource-mutation.ts` |
| Store | `<feature>.store.ts` | `active-resource.store.ts` |
| Component | `<feature>-<role>.tsx` | `order-card.tsx` |
| Query key | `['resource', 'sub-resource', id]` | `['orders', 'list', userId]` |

---

## staleTime rules by data type

| Data type | Suggested staleTime |
|---|---|
| Real-time (confirmations, live status) | 0–2 minutes |
| Frequently changing (lists, schedules) | 2–5 minutes |
| Reference data (profiles, settings) | 10 minutes |
| Historical / reports | 30 minutes |

See the project's spec (e.g. `PROJECT.md`) or complement skill, if any, for project-specific values.

---

## React Native Web — deprecated warnings (suppress in root layout)

Expo Router and React Navigation generate two deprecation warnings in React Native Web
that come from the **internals of those libraries themselves**, not from application code.
There is no way to fix them in app code — wait for an upstream fix.

**Suppress in `app/_layout.tsx`:**

```typescript
import { LogBox } from 'react-native';

// Add OUTSIDE any component (module level):
LogBox.ignoreLogs([
  '"shadow*" style props are deprecated',
  'props.pointerEvents is deprecated. Use style.pointerEvents',
]);
```

- `"shadow*" style props` — comes from `ContextNavigator` / `_HelmetProvider` in Expo Router
- `props.pointerEvents` — comes from `TouchableOpacity` in React Native Web

---

## Date inputs — DD/MM/YYYY format

Use the app locale's display format in the UI (example below: DD/MM/YYYY). The API always
receives YYYY-MM-DD (ISO 8601). Apply an automatic mask as the user types.

```typescript
// Apply DD/MM/YYYY mask as user types
function applyDateMask(raw: string): string {
  const digits = raw.replace(/\D/g, '').slice(0, 8);
  if (digits.length <= 2) return digits;
  if (digits.length <= 4) return `${digits.slice(0, 2)}/${digits.slice(2)}`;
  return `${digits.slice(0, 2)}/${digits.slice(2, 4)}/${digits.slice(4)}`;
}

// Convert DD/MM/YYYY → YYYY-MM-DD for the API
function toIsoDate(ddmmyyyy: string): string {
  const [d, m, y] = ddmmyyyy.split('/');
  return `${y}-${m}-${d}`;
}

// Validate real date in the past
function validateDDMMYYYY(value: string): boolean {
  if (!/^\d{2}\/\d{2}\/\d{4}$/.test(value)) return false;
  const [d, m, y] = value.split('/').map(Number);
  const date = new Date(y, m - 1, d);
  return (
    date.getFullYear() === y &&
    date.getMonth() === m - 1 &&
    date.getDate() === d &&
    date < new Date()
  );
}

// In TextInput:
<TextInput
  value={birthDate}
  onChangeText={(text) => setBirthDate(applyDateMask(text))}
  placeholder="DD/MM/YYYY"   // in the app's UI language
  keyboardType="numeric"
  maxLength={10}
/>

// When sending to API:
birthDate: toIsoDate(birthDate.trim())  // converts to YYYY-MM-DD
```

---

## React Query v5 — `isLoading` is `true` for disabled queries without data

In React Query v5, `isLoading` equals `isPending` equals `status === 'pending'`.
A query with `enabled: false` that has never fetched data has `status: 'pending'` → `isLoading: true`.

**Consequence:** if a required param (e.g. `resourceId`) is empty because `useGlobalSearchParams`
returns `{}` on first render in Expo Router web, the query stays `enabled: false` → `isLoading: true`
→ infinite loading spinner.

**Solution:** use `isPending && isFetching` to test "is actually fetching", and guard before hooks:

```typescript
const { id } = useGlobalSearchParams<{ id: string }>();
const { data, isPending, isFetching } = useQuery({
  queryKey: ['items', id],
  queryFn: () => fetchItems(id!),
  enabled: !!id,
});

if (!id) return <LoadingSpinner />;             // guard AFTER hooks
if (isPending && isFetching) return <LoadingSpinner />;
```

---

## React Query — QueryClient must be created outside the component

```typescript
// CORRECT — created once at module level
const queryClient = new QueryClient({
  defaultOptions: { queries: { ... } },
});

export default function RootLayout() {
  return <QueryClientProvider client={queryClient}>...</QueryClientProvider>;
}
```

If created inside the component without `useState`, a new `QueryClient` is generated on every
render — the cache is lost on every re-render.

---

## React Query — recommended QueryClient configuration for Expo Router web

```typescript
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 2,    // 2 min default — override per query (see "staleTime rules by data type")
      gcTime: 1800000,             // 30 min in cache (avoids spinner when returning to tab)
      refetchOnWindowFocus: false, // avoids refetch on browser window focus
      retry: 1,
    },
  },
});
```

A non-zero default plus per-query values from the "staleTime rules by data type" table (real-time
data overrides it down to 0–2 min, reference data up to 10 min). `gcTime: 30min`: first visit
shows a brief spinner; returning to a screen shows cached data immediately.

**Cost of `staleTime: 0`:** every mount, `useFocusEffect` refetch and reconnect hits the API
again — more requests and server load, more background spinners and list flicker, more mobile
data. Use 0 only for queries that must be live, set on that query, not as the global default.

---

## React Query — tabs that stay mounted need `useFocusEffect` for refetch

By default, tabs in React Navigation / Expo Router do NOT unmount when switching tabs.
`refetchOnMount` only fires on the first visit.

**Solution:** add `useFocusEffect` in each individual screen that needs fresh data:

```typescript
import { useFocusEffect } from 'expo-router';
import { useCallback } from 'react';
import { useQueryClient } from '@tanstack/react-query';

const qc = useQueryClient();
useFocusEffect(useCallback(() => {
  if (id) qc.refetchQueries({ queryKey: ['module', id] });
}, [id, qc]));
```

**Do not** put `useFocusEffect` in the `_layout.tsx` of Tabs — in Expo Router web it fires
on EVERY tab change, cancelling fetches in a loop.

---

## React Query — date-dependent queries must include the local date in the query key

Any query whose result changes with the current day must include the local date in `queryKey`.
Without this, the cache from the previous day is reused after midnight — the user sees
yesterday's data until a hard refresh.

```typescript
export function useDailyItems(resourceId: string, tz: string) {
  const today = new Date().toLocaleDateString('sv-SE', { timeZone: tz }); // "2026-06-25"
  return useQuery({
    queryKey: ['resources', resourceId, 'daily', today], // key changes at midnight
    queryFn: () => getDailyItems(resourceId, tz),
    enabled: !!resourceId,
  });
}
```

**Also pass the local date to the API as a query param:**

```typescript
async function getDailyItems(resourceId: string, tz: string) {
  const date = new Date().toLocaleDateString('sv-SE', { timeZone: tz });
  return apiRequest(`/resources/${resourceId}/daily?date=${date}`);
}
```

**Why `sv-SE`:** the Swedish locale returns `YYYY-MM-DD` — the only unambiguous ISO format
that the backend accepts directly as a date string.

**When to apply:** any query for "today's schedule", "today's events", "daily summary", or any
endpoint that accepts `?date=`. Verify that the hook receives `tz` (the user's IANA timezone)
as a parameter.

---

## Detecting "today's record" — timezone-safe comparison

When a screen needs to find the record that belongs to "today", **never** compare
`.slice(0, 10)` on a UTC ISO string — that reads the UTC date, which is wrong for users
in UTC- timezones. Convert to the user's local timezone first.

```typescript
const tz = useUserTimezone();
const todayStr = new Date().toLocaleDateString('sv-SE', { timeZone: tz }); // "2026-06-26"

const todayEntry = entries.find((e) =>
  e.date_field
    ? new Date(e.date_field).toLocaleDateString('sv-SE', { timeZone: tz }) === todayStr
    : false
);
```

**Why `sv-SE`:** Swedish locale returns `YYYY-MM-DD` — unambiguous and sortable.

**Pre-condition:** this assumes the column stores real UTC timestamps (e.g. `"2026-06-26T15:00:00Z"`).
If migrating a column from `DATE` to `TIMESTAMPTZ`, the migration **must** backfill existing
rows to a real UTC time — not just cast to midnight UTC. See `migrations` § "Date and time"
(event dates / `date` → `timestamptz` backfill) for the correct pattern using `AT TIME ZONE`. Without this, `DATE '2026-06-26'` becomes
`"2026-06-26T00:00:00Z"` (midnight UTC), which in UTC-3 shows as `"2026-06-25"` — wrong.

**Writing always uses `toISOString()`** — this detection code never affects what goes to the API:
```typescript
body: { date_field: new Date().toISOString() }  // ✅ always UTC
```

**Also applies to backend filters:** pass `tz` as a query param so the backend can compute
correct UTC bounds. See `nestjs-fastify` § "Filtering `timestamptz` by local calendar date — `utcRangeForLocalDate`".

---

## Writing to PostgreSQL `date` columns — never use `toISOString()`

When a column is declared as `date` (not `timestamptz`), **never** send `toISOString()` or its slice.
At 23:30 UTC-3, `new Date().toISOString()` returns `"2026-06-26T02:30:00Z"` — PostgreSQL extracts
`2026-06-26` (the next UTC day) while the user intended `2026-06-25`.

```typescript
const tz = useUserTimezone(); // IANA timezone from the auth/user Zustand store

// ❌ NEVER — extracts UTC date, wrong for UTC- users near midnight
body: { purchased_at: new Date().toISOString() }
body: { purchased_at: new Date().toISOString().slice(0, 10) }  // same bug at day boundary

// ✅ ALWAYS — local date in the user's timezone
body: { purchased_at: new Date().toLocaleDateString('sv-SE', { timeZone: tz }) }
// → "2026-06-25"  (correct regardless of UTC offset)
```

**Rule:** `date` column → `toLocaleDateString('sv-SE', { timeZone: tz })`. `timestamptz` column → `toISOString()`.

**How to distinguish:** check the migration — `date NOT NULL` → sv-SE pattern; `timestamptz` → `toISOString()`.

**Never hardcode the timezone in the frontend.** A hard-coded default zone is acceptable only as
a backend fallback. Always read `tz` from the user's stored IANA timezone (e.g. a
`useUserTimezone()` selector on the Zustand auth store) and send it explicitly.

---

## Grouping history by local calendar date

When displaying historical records grouped by day (order history, activity log, confirmations),
always group by the **user's local date**, not the UTC date string.

**Wrong:** `.slice(0, 10)` on a `timestamptz` string — at 22:30 UTC-3, `"2026-06-26T01:30:00+00:00".slice(0, 10)`
returns `"2026-06-26"`, but the event happened on the 25th locally.

**Correct:**

```typescript
function groupByLocalDate<T>(
  items: T[],
  getTimestamp: (item: T) => string | null | undefined,
  tz: string,
): Record<string, T[]> {
  const groups: Record<string, T[]> = {};
  for (const item of items) {
    const ts = getTimestamp(item);
    const date = ts
      ? new Date(ts).toLocaleDateString('sv-SE', { timeZone: tz })
      : '';
    if (!groups[date]) groups[date] = [];
    groups[date].push(item);
  }
  return groups;
}

// Usage:
const tz = useUserTimezone();
const grouped = groupByLocalDate(confirmations, (c) => c.confirmed_at, tz);
const sortedDates = Object.keys(grouped).sort().reverse(); // descending
```

**Why `sv-SE`:** Swedish locale returns `YYYY-MM-DD` — ISO-format, unambiguous, directly sortable.

**Rule:** never use `.slice(0, 10)` on a `timestamptz` field for display grouping. Only safe for `date`
fields (and even then, prefer a `fromIsoDate()`-style parser). See `migrations` § "Date and time" for field type reference.

---

## pnpm 11 — `allowBuilds` must include `@swc/core`

If the project uses `@swc/core` (NestJS test runner or transpiler), add it to `allowBuilds`
in `pnpm-workspace.yaml`:

```yaml
allowBuilds:
  '@nestjs/core': true
  esbuild: true
  '@swc/core': true
```

Without this, pnpm 11 blocks the postinstall script and `@swc/core` fails to compile its
native bindings — `jest` or `nest build` will fail with a native module error.

---

## Stale persisted entity ID — validate against loaded list on mount

When an entity ID is persisted in AsyncStorage (e.g., "currently selected item" in a Zustand store), that ID can become **stale** between sessions:
- The entity was deleted
- The user lost access (removed from a group, permission revoked)
- The entity was archived and is no longer in the user's accessible list

On next session, the app reads the stale ID and tries to use it. Navigation using a stale ID leads to 404s, empty screens, or worse — a self-perpetuating loop where every navigation re-writes the stale ID back into the store.

### Validation pattern

After the entity list loads, compare the persisted ID against the list. If not found, clear it.

```typescript
useEffect(() => {
  if (!persistedEntityId) return;
  if (isLoadingListA || isLoadingListB) return; // wait for ALL relevant lists
  const all = [...(listA ?? []), ...(listB ?? [])];
  if (!all.find((item) => item.id === persistedEntityId)) {
    clearPersistedId(); // entity no longer accessible — clear stale reference
  }
}, [persistedEntityId, listA, listB, isLoadingListA, isLoadingListB]);
```

**Critical timing rule:** wait until all relevant lists are loaded before clearing. Clearing during loading produces false negatives — the entity appears "missing" before it was fetched.

### Guard components that navigate using the persisted ID

```typescript
// WRONG — navigates even when persistedEntityId is stale
{persistedEntityId && <QuickNavComponent entityId={persistedEntityId} />}

// CORRECT — derive the resolved entity from the list first
const resolvedEntity = allItems?.find((e) => e.id === persistedEntityId) ?? null;
{resolvedEntity && <QuickNavComponent entityId={resolvedEntity.id} />}
```

### The stale ID feedback loop (anti-pattern)

Stale IDs can create a self-perpetuating loop:
1. Hub screen reads stale ID → renders QuickNav → user navigates to detail
2. Detail layout's `useEffect` calls `setPersistedId(staleId)` → refreshes the stale ID in store
3. Back on hub screen, stale ID is still there — loop continues indefinitely

Break the loop by validating at the hub (the screen users always return to) before rendering any navigation that depends on the persisted ID.

### Where to place the validation

Validate once in the "hub" screen — the screen users always return to after navigating elsewhere (typically the dashboard or primary list screen). This single validation point propagates clean state through the rest of the app.

---

## React Navigation — use version 7, not 6

`@react-navigation/core@^6` and `@react-navigation/native@^6` cause
`ERR_PNPM_NO_MATCHING_VERSION` — v6 no longer exists on npm.
Expo SDK 52+ (`expo-router` v4 and later) depends on React Navigation v7.

```json
{
  "dependencies": {
    "@react-navigation/core": "^7.0.0",
    "@react-navigation/native": "^7.0.0"
  }
}
```

Declare transitive React Navigation dependencies explicitly in `package.json` — pnpm does not
hoist them automatically into Metro's resolution context.

---

## React Query — `mutate` vs `mutateAsync`: `onError` is mandatory on user actions

`mutate` is fire-and-forget: **without `onError`, API failures are silently swallowed**. The button seems to do nothing — no spinner, no error, no action.

```typescript
// ✗ wrong — silent failures
createOrder.mutate(dto, { onSuccess: onClose });

// ✓ correct — always include onError on user-triggered actions
createOrder.mutate(dto, {
  onSuccess: onClose,
  onError: (e: any) => setError(e?.message ?? 'Could not create.'),
});
```

**`mutate` vs `mutateAsync`:**

| | `mutate` | `mutateAsync` |
|---|---|---|
| Signature | callbacks (`onSuccess`, `onError`) | returns a `Promise` — use `try/catch` |
| When to use | synchronous handlers (`onPress`) | `async` handlers, when you need to `await` the result |
| Failure without handler | silent | throws (catchable with `catch`) |

```typescript
// mutateAsync — async handler with try/catch
async function handleSave() {
  try {
    await createOrder.mutateAsync(dto);
    onClose();
  } catch (e: any) {
    setError(e?.message ?? 'Could not create.');
  }
}
```

(For what to show the user instead of a raw `e.message`, see "Shared HTTP client" above.)

**Rule:** every `mutate` in a user-action handler (Save, Create, Confirm button) must have an explicit `onError`. Omitting it is always a bug.

---

## React Query — `setQueryData` + `invalidateQueries` for immediate feedback

`invalidateQueries` marks the query as stale and triggers a background refetch — the UI shows stale data during the round-trip. For an immediate visual transition (e.g. a card leaves "In progress" and appears in "Completed"), combine both:

```typescript
onSuccess: (updated: OrderDto) => {
  // Synchronous cache patch with the data returned by the API
  queryClient.setQueryData<OrderDto[]>(
    ['projects', projectId, 'orders'],
    (old) => old?.map((o) => o.id === updated.id ? updated : o) ?? [],
  );
  // Invalidate for an eventual refetch — guarantees consistency with the server
  queryClient.invalidateQueries({ queryKey: ['projects', projectId, 'orders'] });
},
```

**When to use:** mutations that update one item in a list (PATCH/close). `setQueryData` guarantees the immediate visual transition; `invalidateQueries` guarantees the cache eventually reflects the real server state.

**Why not only `invalidateQueries`:** the refetch is asynchronous. In lists with server-computed fields (e.g. `is_active` derived from `end_date`), the UI shows the outdated item for hundreds of milliseconds — the user sees the item stay in the wrong list even after the operation succeeded.
